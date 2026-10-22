"""Local-only backend. Public GitHub Pages serves saved evidence, never secrets."""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from .core import ROOT, ProviderError, answer_question

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'docs'),**kwargs)
    def log_message(self,*args): pass
    def send_json(self,value,status=200):
        body=json.dumps(value).encode()
        self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/status':
            return self.send_json({'local':True,'gemini_configured':bool(os.getenv('GEMINI_API_KEY')),'index_ready':(ROOT/'local/vector-index.json').exists()})
        super().do_GET()
    def do_POST(self):
        if self.path!='/api/answer': return self.send_json({'error':'Not found'},404)
        # Block cross-site requests; no CORS allowance or public listening interface.
        origin=self.headers.get('Origin')
        host=self.headers.get('Host')
        if host not in {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'} or (origin and urlparse(origin).netloc!=host):
            return self.send_json({'error':'Only same-origin local requests are accepted.'},403)
        if self.headers.get('Content-Type','').split(';')[0]!='application/json': return self.send_json({'error':'JSON required'},415)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=10000: raise ValueError('Invalid request size.')
            request=json.loads(self.rfile.read(length))
            if not isinstance(request,dict) or request.get('method') not in {'rules','full','vector'}: raise ValueError('Choose a valid method.')
            self.send_json(answer_question(request.get('question'),request['method']))
        except (ValueError,ProviderError,FileNotFoundError) as e: self.send_json({'error':str(e)},400)

def serve(port):
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'Local policy assistant: http://127.0.0.1:{port}',flush=True)
    server.serve_forever()
