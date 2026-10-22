import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from policy_assistant.core import *
from policy_assistant.slack_bot import format_answer

class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.policies=load_policies()
    def test_database_integrity(self):
        self.assertEqual(len(self.policies),98)
        self.assertEqual(len({p['id'] for p in self.policies}),98)
    def test_direct_question_keeps_approval_condition(self):
        r=rules_answer('How many days per week may I work remotely?',self.policies)
        self.assertEqual(r['citations'][0]['title'],'Remote Work Policy')
        self.assertIn('manager approval',r['answer'])
        self.assertEqual(r['usage']['total_tokens'],0)
    def test_no_match_abstains(self):
        r=rules_answer('zyxwvut',self.policies)
        self.assertEqual(r['status'],'not_found'); self.assertFalse(r['citations'])
    def test_every_rule_quote_is_exact(self):
        questions=json.loads((ROOT/'evaluation/questions.json').read_text())
        lookup={p['id']:p['policy_text'] for p in self.policies}
        for q in questions:
            r=rules_answer(q['question'],self.policies)
            self.assertTrue(all(c['quote']==lookup[c['policy_id']] for c in r['citations']))
    def test_invalid_question(self):
        for q in ['',None,42,'x'*2001]:
            with self.assertRaises(ValueError): rules_answer(q,self.policies)
    def test_hallucinated_citation_detected_and_not_posted(self):
        a={'answer':'Unlimited holiday.','status':'answered','limitation':'','citations':[{'policy_id':self.policies[0]['id'],'quote':'Unlimited holiday.'}]}
        r=check_answer(a,self.policies)
        self.assertEqual(r['citation_check'],'failed')
        self.assertNotIn('Unlimited holiday',format_answer(r))
    def test_unknown_citation_detected(self):
        a={'answer':'Something','status':'answered','limitation':'','citations':[{'policy_id':'fake','quote':'something'}]}
        self.assertEqual(check_answer(a,self.policies)['citation_check'],'failed')
    def test_grounded_source_does_not_prove_answer(self):
        p=self.policies[0]
        a={'answer':'An unsupported inference','status':'answered','limitation':'','citations':[{'policy_id':p['id'],'quote':p['policy_text']}]}
        r=check_answer(a,self.policies)
        self.assertEqual(r['citation_check'],'passed')
        self.assertNotIn('unsupported',r)  # Requires a substantive review.
    def test_vector_retrieval_and_stale_index(self):
        class Fake:
            embedding_model='test'
            def embed(self,text,task): return [0.,1.],None
        ps=self.policies[:2]
        index={'database_sha256':fingerprint(ps),'embedding_model':'test','dimensions':2,'policy_ids':[p['id'] for p in ps],'vectors':[[1.,0.],[0.,1.]]}
        results,t=retrieve('question',ps,Fake(),index,k=1)
        self.assertEqual(results[0],ps[1]); self.assertIsNone(t)
        with self.assertRaises(ValueError): retrieve('q',self.policies,Fake(),index)
    def test_methods_use_same_provider_and_differ_only_in_context(self):
        class Fake:
            embedding_model='test'; model='same-model'
            def embed(self,text,task): return [1.,0.],11
            def generate(self,question,policies):
                self.context=policies
                p=policies[0]
                return {'answer':p['policy_text'],'status':'answered','limitation':'','citations':[{'policy_id':p['id'],'quote':p['policy_text']}]}, {'input_tokens':5,'output_tokens':6,'total_tokens':11}, 'same-model-v1'
        fake=Fake(); ps=self.policies[:8]
        full=llm_answer('q',ps,'full',fake)
        self.assertEqual(len(fake.context),8)
        index={'database_sha256':fingerprint(ps),'embedding_model':'test','dimensions':2,'policy_ids':[p['id'] for p in ps],'vectors':[[1.,0.]]*8}
        vector=llm_answer('q',ps,'vector',fake,index)
        self.assertEqual(len(fake.context),5)
        self.assertEqual(full['model'],vector['model'])
        self.assertEqual(vector['usage']['embedding_tokens'],11)
    def test_failed_generation_is_not_an_abstention(self):
        provider=Gemini(key='test')
        with patch.object(provider,'request',return_value={'candidates':[{'finishReason':'MAX_TOKENS'}]}):
            with self.assertRaises(ProviderError): provider.generate('q',self.policies)
    def test_unknown_token_usage_not_zero(self):
        p=self.policies[0]
        a={'answer':p['policy_text'],'status':'answered','citations':[{'policy_id':p['id'],'quote':p['policy_text']}],'limitation':''}
        provider=Gemini(key='test')
        raw={'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':json.dumps(a)}]}}]}
        with patch.object(provider,'request',return_value=raw):
            answer,usage,version=provider.generate('q',self.policies)
        self.assertIsNone(usage['total_tokens'])
    def test_two_paragraphs(self):
        paragraphs=(ROOT/'COMPARISON.md').read_text().strip().split('\n\n')
        self.assertEqual(len(paragraphs),2)
    def test_env_never_executes_shell(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'.env'; p.write_text('POLICY_TEST_LITERAL=$(echo nope)\n')
            load_env(p); self.assertEqual(os.environ.pop('POLICY_TEST_LITERAL'),'$(echo nope)')

if __name__=='__main__': unittest.main()
