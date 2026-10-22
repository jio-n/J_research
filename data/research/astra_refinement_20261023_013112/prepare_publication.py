"""Copy only the two new edition directories into the clean existing publishing checkout."""
from pathlib import Path
import json,hashlib,subprocess,shutil
D=Path(__file__).parent;R=D.parents[2];C=R/'.build/strategy_publish_20261021'
assert not subprocess.check_output(['git','-C',str(C),'status','--porcelain'],text=True).strip(),'Publishing checkout must be clean'
manifest=json.loads((D/'manifest.json').read_text(encoding='utf8'))
paths=[x['path'] for x in manifest['files']]+[(D/'manifest.json').relative_to(R).as_posix()]
prefixes=[f'outputs/{D.name}/',f'data/research/{D.name}/']
assert all(any(p.startswith(pre) for pre in prefixes) for p in paths)
assert not any('_private' in Path(p).parts for p in paths)
for p in paths:assert not (C/p).exists(),('Destination already exists',p)
for p in paths:
 target=C/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/p,target)
 assert hashlib.sha256((R/p).read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
print(json.dumps({'copied':len(paths),'prefixes':prefixes,'checkout':str(C)}))
