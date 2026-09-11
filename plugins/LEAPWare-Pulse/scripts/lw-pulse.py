#!/usr/bin/env python3
"""Read canonical tasks and source-bound evidence once; emit concise status facts."""
import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from learning.storage import decode, relative
from lw_learning_bridge import capture, retrieve

def report(args):
    root=Path(args.root).absolute()
    path=relative(root,args.tasks)
    with path.open('rb') as stream: raw=stream.read(262145)
    if len(raw)>262144: raise ValueError('task document exceeds 256 KiB')
    rows=re.findall(r'^\s*- \[([ xX])\] (.+)$',raw.decode('utf-8'),re.M)
    result={'tasks':{'path':args.tasks,'checked':sum(x.lower()=='x' for x,_ in rows),'total':len(rows)},
            'verification':'unknown','delivery':dict(source_fixed='unknown',pushed='unknown',packaged='unknown',active='unknown'),
            'tokens':'unknown'}
    if bool(args.spec)!=bool(args.evidence): raise ValueError('spec and evidence must be supplied together')
    if args.spec:
        try:
            specpath=relative(root,args.spec)
            with specpath.open('rb') as stream: specraw=stream.read(8193)
            if len(specraw)>8192: raise ValueError('spec exceeds 8 KiB')
            spec=decode(specraw)
            head=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,timeout=3,check=True).stdout.strip()
            if spec['candidate']!=head: raise ValueError('stale evidence candidate')
            module_spec=importlib.util.spec_from_file_location('pulse_acceptance',Path(__file__).with_name('lw-acceptance.py'))
            module=importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(module)
            with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                code=module.command_verify(argparse.Namespace(root=str(root),spec=str(specpath),evidence=str(relative(root,args.evidence))))
            if code: raise ValueError('source evidence rejected')
            result['verification']='source-bound pass'; result['delivery']['source_fixed']=head
        except (ValueError,OSError,KeyError,TypeError,RecursionError,subprocess.SubprocessError) as error:
            result['verification']='unverified'
            result['capture']=capture(root,'leapware-pulse','evidence',args.session,error,args.occurrence)
    result['learning']=retrieve(root,'leapware-pulse','status')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',required=True); p.add_argument('--tasks',default='openspec/tasks.md')
    p.add_argument('--session',required=True); p.add_argument('--occurrence',default='')
    p.add_argument('--spec'); p.add_argument('--evidence'); args=p.parse_args()
    try: result=report(args); code=0
    except (ValueError,OSError,KeyError,TypeError,RecursionError,subprocess.SubprocessError) as error:
        result={'error':'invalid report input','capture':capture(args.root,'leapware-pulse','report',args.session,error,args.occurrence)}; code=1
    print(json.dumps(result,ensure_ascii=True)); return code
if __name__=='__main__': raise SystemExit(main())
