import json
from .core import ROOT

def check():
    s=json.loads((ROOT/'submission-status.json').read_text())
    r=json.loads((ROOT/'docs/data/results.json').read_text())
    paragraphs=[p for p in (ROOT/'COMPARISON.md').read_text().strip().split('\n\n') if p.strip()]
    checks={
       'Exactly two comparison paragraphs':len(paragraphs)==2 and not any(p.startswith('#') for p in paragraphs),
       'Public repository link recorded':bool(s['repository_url']),
       'Deployed website verified and recorded':bool(s['website_url']),
       'All three methods attempted; service errors disclosed':all(v['attempted']==v['total_questions'] and v['completed']>0 for v in r['summaries'].values()),
       'Unsupported-answer review complete':all(v['reviewed_count']==v['completed'] and v['correctness_reviewed_count']==v['completed'] for v in r['summaries'].values()),
       'Student-identifiable Slack workspace recorded':bool(s['slack_workspace_name']),
       'Student-identifiable Slack channel recorded':bool(s['slack_channel_name'] and s['slack_channel_url']),
       'Invitation to raz@sdu.dk recorded':bool(s['lecturer_invitation_sent_at']),
       'Real Slack screenshot saved':bool(s['slack_screenshot'] and (ROOT/s['slack_screenshot']).is_file()),
       'Student hours recorded':s['student_hours'] is not None,
       'Cost statement recorded':bool(s['cost_statement'])}
    for label,passed in checks.items(): print(f"{'PASS' if passed else 'PENDING'}  {label}")
    return 0 if all(checks.values()) else 1
