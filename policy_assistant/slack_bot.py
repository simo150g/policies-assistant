"""Local Slack Socket Mode app, limited to the coursework channel."""
import os
import re
import time
from .core import ProviderError, answer_question

def format_answer(result):
    if result.get('citation_check')=='failed':
        return 'I could not verify the answer against the supplied policies. Please rephrase your question. No unverified answer has been posted.'
    text=result['answer']
    for c in result.get('citations',[]):
        text+=f"\n\nRelevant policy: {c['title']}\n“{c['quote']}”"
    if result.get('limitation'): text+='\n\nLimitations: '+result['limitation']
    text+=f"\n\nMethod: {result['method']} · {result['response_ms']:.0f} ms"
    return text[:11000]

def start():
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
    except ImportError:
        raise ValueError('Install the Slack dependencies using: python3 -m pip install -r requirements.txt') from None
    for key in ['SLACK_BOT_TOKEN','SLACK_APP_TOKEN','SLACK_CHANNEL_ID']:
        if not os.getenv(key): raise ValueError(f'{key} is not configured in .env.')
    method=os.getenv('SLACK_METHOD','full')
    if method not in {'rules','full','vector'}: raise ValueError('Invalid SLACK_METHOD.')
    if method!='rules' and not os.getenv('GEMINI_API_KEY'): raise ValueError('Gemini key is needed for the selected Slack method.')
    app=App(token=os.environ['SLACK_BOT_TOKEN'])
    seen={}
    @app.event('app_mention')
    def mention(event,say,body):
        if event.get('channel')!=os.environ['SLACK_CHANNEL_ID'] or event.get('bot_id'): return
        now=time.monotonic()
        for key in list(seen):
            if seen[key]<now-600: del seen[key]
        event_id=body.get('event_id')
        if event_id in seen: return
        seen[event_id]=now
        # Strip Slack mention identifiers; do not send user identity or channel history to the LLM.
        question=re.sub(r'<@[A-Z0-9]+>','',event.get('text','')).strip()
        thread=event.get('thread_ts') or event['ts']
        if not question:
            say(text='Ask me a question about the supplied company policies, for example: How many days may I work remotely?',thread_ts=thread); return
        try: text=format_answer(answer_question(question,method))
        except (ProviderError,ValueError,FileNotFoundError): text='The policy service is unavailable or the question is invalid. Please ask the student running this bot to check the local setup.'
        # Plain text prevents generated markup from mentioning users or linking to external URLs.
        say(text=text,blocks=[{'type':'section','text':{'type':'plain_text','text':text[:2900]}}],thread_ts=thread,unfurl_links=False,unfurl_media=False)
    print(f'Starting local Slack assistant with {method} method. Only the configured test channel is enabled.',flush=True)
    SocketModeHandler(app,os.environ['SLACK_APP_TOKEN']).start()
