from pathlib import Path
import json,hashlib,sys
D=Path(__file__).parent; R=D.parents[2]; snap=D/'_private/original_hashes.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--record' in sys.argv:
    files=[p for folder in ['outputs','data/research','scripts'] if (R/folder).exists() for p in (R/folder).rglob('*') if p.is_file() and not p.name.startswith('~$') and '_private' not in p.parts and 'node_modules' not in p.parts and D.name not in p.parts]
    files += [p for p in R.iterdir() if p.is_file() and p.suffix.lower() in ['.md','.json','.py','.mjs','.ps1']]
    obj={str(p.relative_to(R)).replace('\\','/'):digest(p) for p in files}
    snap.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(dict(recorded=len(obj))))
else:
    obj=json.loads(snap.read_text(encoding='utf8'));changed=[s for s,h in obj.items() if not (R/s).exists() or digest(R/s)!=h]
    result=dict(checked=len(obj),unchanged=len(obj)-len(changed),changed=changed)
    (D/'preservation_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False));assert not changed
