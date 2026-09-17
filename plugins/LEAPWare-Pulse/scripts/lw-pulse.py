#!/usr/bin/env python3
"""Read canonical tasks and source-bound evidence once; emit concise status facts."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def absolute(value):
    """Resolve an already-absolute path, rejecting anything that is not one."""
    candidate = Path(value)
    if not candidate.is_absolute():
        raise ValueError('absolute() needs an absolute path, got a relative one')
    if '..' in candidate.parts:
        raise ValueError('absolute() refuses ".." segments')
    return candidate.resolve()


def relative(root, value):
    """Join value under root, rejecting anything that would land outside root."""
    if not isinstance(value, str) or value == '':
        raise ValueError('relative() needs a non-empty string, not %r' % (value,))
    candidate = Path(value)
    if candidate.is_absolute():
        raise ValueError('relative() refuses an absolute value')
    if '..' in candidate.parts:
        raise ValueError('relative() refuses ".." segments')
    joined = root / candidate
    if not joined.resolve().is_relative_to(root):
        raise ValueError('relative() refuses a value that escapes root')
    return joined


def decode(raw):
    try:
        return json.loads(raw.decode('utf-8'))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError('invalid JSON') from error


def report(args):
    root=absolute(Path(args.root).absolute())
    path=relative(root,args.tasks)
    with path.open('rb') as stream: raw=stream.read(262145)
    if len(raw)>262144: raise ValueError('task document exceeds 256 KiB')
    rows=re.findall(r'^\s*- \[([ xX])\] (.+)$',raw.decode('utf-8'),re.M)
    result={'tasks':{'path':args.tasks,'checked':sum(x.lower()=='x' for x,_ in rows),'total':len(rows)},
            'verification':'unknown','delivery':dict(source_fixed='unknown',pushed='unknown',packaged='unknown',active='unknown'),
            'tokens':'unknown'}
    if bool(args.spec)!=bool(args.evidence): raise ValueError('spec and evidence must be supplied together')
    if args.spec:
        # No acceptance runner is bundled: lw-acceptance.py was removed as
        # private-origin (CTO decision); a clean-room runner ships in D1.
        # Until then, spec/evidence input is still fully checked for shape and
        # freshness, but source-bound verification cannot be performed.
        try:
            specpath=relative(root,args.spec)
            with specpath.open('rb') as stream: specraw=stream.read(8193)
            if len(specraw)>8192: raise ValueError('spec exceeds 8 KiB')
            spec=decode(specraw)
            relative(root,args.evidence)
            head=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,timeout=3,check=True).stdout.strip()
            if spec['candidate']!=head: raise ValueError('stale evidence candidate')
            result['error']='no acceptance runner bundled: lw-acceptance.py removed (private-origin); rebuilt clean-room in D1'
        except (ValueError,OSError,KeyError,TypeError,RecursionError,subprocess.SubprocessError) as error:
            result['error']=str(error)
        result['verification']='unverified'
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',required=True); p.add_argument('--tasks',default='openspec/tasks.md')
    p.add_argument('--session',required=True); p.add_argument('--occurrence',default='')
    p.add_argument('--spec'); p.add_argument('--evidence'); args=p.parse_args()
    try: result=report(args); code=0
    except (ValueError,OSError,KeyError,TypeError,RecursionError,subprocess.SubprocessError) as error:
        result={'error':'invalid report input: '+str(error)}; code=1
    print(json.dumps(result,ensure_ascii=True)); return code
if __name__=='__main__': raise SystemExit(main())
