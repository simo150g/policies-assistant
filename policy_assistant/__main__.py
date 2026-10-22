import argparse
import json
import sys
from .core import ROOT, Gemini, ProviderError, answer_question, build_index, load_env, load_policies

def main():
    parser=argparse.ArgumentParser(description='Policy assistant coursework tools')
    sub=parser.add_subparsers(dest='command',required=True)
    ask=sub.add_parser('ask'); ask.add_argument('question'); ask.add_argument('--method',choices=['rules','full','vector'],default='rules')
    bench=sub.add_parser('benchmark'); bench.add_argument('--methods',nargs='+',choices=['rules','full','vector'],default=['rules','full','vector']); bench.add_argument('--delay',type=float,default=4.0)
    bench.add_argument('--resume',help='Resume an existing run ID without repeating successful answers')
    bench.add_argument('--workers',type=int,default=1)
    idx=sub.add_parser('index'); idx.add_argument('--delay',type=float,default=1.0)
    srv=sub.add_parser('serve'); srv.add_argument('--port',type=int,default=8765)
    sub.add_parser('export'); sub.add_parser('slack'); sub.add_parser('check')
    args=parser.parse_args()
    load_env()
    try:
        if args.command=='ask': print(json.dumps(answer_question(args.question,args.method),indent=2))
        elif args.command=='index': build_index(load_policies(),Gemini(),ROOT/'local/vector-index.json',args.delay)
        elif args.command=='benchmark':
            from .benchmark import run
            print(run(args.methods,args.delay,args.resume,args.workers))
        elif args.command=='export':
            from .benchmark import export
            export(); print('Website results exported.')
        elif args.command=='serve':
            from .server import serve
            serve(args.port)
        elif args.command=='slack':
            from .slack_bot import start
            start()
        elif args.command=='check':
            from .submission import check
            return check()
    except (ProviderError,ValueError,FileNotFoundError) as e:
        print(str(e),file=sys.stderr); return 1
    return 0

if __name__=='__main__': sys.exit(main())
