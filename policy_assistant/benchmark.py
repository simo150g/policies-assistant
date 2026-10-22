"""Runs are persisted; manual evidence reviews remain separate and auditable."""
import hashlib
import json
import statistics
import time
from pathlib import Path
from .core import ROOT, Gemini, ProviderError, build_index, fingerprint, llm_answer, load_policies, rules_answer, utcnow
METHODS = ('rules','full','vector')

def digest(result):
    return hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()

def run(methods, delay=4.0):
    policies=load_policies()
    questions=json.loads((ROOT/'evaluation/questions.json').read_text())
    run_id=utcnow().replace(':','-')
    archive=ROOT/'evaluation/runs'/run_id
    archive.mkdir(parents=True)
    provider=Gemini() if any(m!='rules' for m in methods) else None
    index=None
    if 'vector' in methods:
        path=ROOT/'local/vector-index.json'
        if not path.exists():
            raise ProviderError('Build the vector index first.')
        index=json.loads(path.read_text())
    run_data={'run_id':run_id,'created_at':utcnow(),'database_sha256':fingerprint(policies),
              'questions_sha256':hashlib.sha256(json.dumps(questions,sort_keys=True).encode()).hexdigest(),
              'method_order':'rotated per question','records':[],
              'index_preparation':{k:v for k,v in index.items() if k not in {'vectors','policy_ids'}} if index else None}
    for n,q in enumerate(questions):
        order=list(methods[n%len(methods):])+list(methods[:n%len(methods)])
        for method in order:
            print(f"{q['id']} / {method}",flush=True)
            try:
                result=rules_answer(q['question'],policies) if method=='rules' else llm_answer(q['question'],policies,method,provider,index)
                if method!='rules' and delay:
                    time.sleep(delay)
            except (ProviderError,ValueError) as e:
                result={'method':method,'status':'error','error':str(e),'measured_at':utcnow()}
            run_data['records'].append({'question_id':q['id'],'result':result,'result_sha256':digest(result)})
            (archive/'results.json').write_text(json.dumps(run_data,indent=2)+'\n')
    (ROOT/'evaluation/latest-run.txt').write_text(run_id)
    export(run_data)
    return archive

def export(run_data=None):
    if run_data is None:
        run_id=(ROOT/'evaluation/latest-run.txt').read_text().strip()
        run_data=json.loads((ROOT/'evaluation/runs'/run_id/'results.json').read_text())
    questions=json.loads((ROOT/'evaluation/questions.json').read_text())
    if run_data['questions_sha256'] != hashlib.sha256(json.dumps(questions,sort_keys=True).encode()).hexdigest():
        raise ValueError('Questions changed since the run. Restore them or collect a new benchmark.')
    if run_data['database_sha256'] != fingerprint(load_policies()):
        raise ValueError('Policy database changed since the run. Collect a new benchmark.')
    review_path=ROOT/'evaluation/reviews.json'
    reviews=json.loads(review_path.read_text()) if review_path.exists() else []
    approved={(r['question_id'],r['method'],r['result_sha256']):r for r in reviews}
    by_question={q['id']:{**q,'results':{}} for q in questions}
    for row in run_data['records']:
        result=row['result']
        method=result['method']
        expected=set(by_question[row['question_id']]['expected_policy_ids'])
        cited={c['policy_id'] for c in result.get('citations',[])}
        result=dict(result)
        result['result_sha256']=row['result_sha256']
        result['expected_policy_recall']=len(cited & expected)/len(expected) if expected and result['status']!='error' else None
        result['review']=approved.get((row['question_id'],method,row['result_sha256']))
        # Exact source-only extracts cannot introduce new factual policy claims.
        # This is NOT a correctness or relevance judgement.
        if method=='rules' and result['status']!='error':
            result['review']={'unsupported':False,'answer_correct':None,'note':'Source-only template verified against the database. Answer relevance/correctness still requires review.','reviewer':'deterministic source-integrity check'}
        by_question[row['question_id']]['results'][method]=result
    summaries={}
    for method in METHODS:
        records=[q['results'][method] for q in by_question.values() if method in q['results']]
        ok=[r for r in records if r['status']!='error']
        reviewed=[r for r in ok if r.get('review') and isinstance(r['review'].get('unsupported'),bool)]
        recalls=[r['expected_policy_recall'] for r in ok if r.get('expected_policy_recall') is not None]
        totals=[r['usage']['total_tokens'] for r in ok if r.get('usage',{}).get('total_tokens') is not None]
        summaries[method]={'completed':len(ok),'attempted':len(records),'total_questions':len(questions),'errors':len(records)-len(ok),
           'median_ms':statistics.median(r['response_ms'] for r in ok) if ok else None,
           'mean_generation_tokens':statistics.mean(totals) if totals else None,
           'mean_expected_policy_recall':statistics.mean(recalls) if recalls else None,
           'unsupported_count':sum(r['review']['unsupported'] for r in reviewed),'reviewed_count':len(reviewed),
           'unsupported_rate':sum(r['review']['unsupported'] for r in reviewed)/len(reviewed) if reviewed else None}
    comparison=(ROOT/'COMPARISON.md').read_text().strip().split('\n\n')
    report={'schema_version':1,'run_id':run_data['run_id'],'created_at':run_data['created_at'],'database_sha256':run_data['database_sha256'],
            'policy_count':len(load_policies()),'summaries':summaries,'questions':list(by_question.values()),
            'index_preparation':run_data.get('index_preparation'),'comparison_paragraphs':comparison,
            'comparison_status':'provisional' if any(s['completed']<len(questions) or s['reviewed_count']<len(questions) for s in summaries.values()) else 'review_ready'}
    (ROOT/'docs/data/results.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'docs/data/policies.json').write_text(json.dumps(load_policies(),indent=2)+'\n')
    return report
