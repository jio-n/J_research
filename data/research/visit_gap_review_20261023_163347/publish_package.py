from pathlib import Path
import json,hashlib,shutil
D=Path(__file__).parent;R=D.parents[2];O=R/'outputs'/D.name
target=R/'.build/strategy_publish_20261021'
files=[p for p in D.iterdir() if p.is_file() and p.name!='manifest.json']+[p for p in O.iterdir() if p.is_file()]
assert all(D.name in p.parts and '_private' not in p.parts for p in files)
manifest=dict(edition=D.name,created='2026-10-23',scope='Two new directories only. Existing research and outputs unchanged.',files=[dict(path=str(p.relative_to(R)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(files)])
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
files.append(D/'manifest.json')
for folder in [D,O]:assert not (target/folder.relative_to(R)).exists(),'Refuse to replace a previously published folder'
for p in files:
    dst=target/p.relative_to(R);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
    assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(dst.read_bytes()).digest()
print(json.dumps(dict(files=len(files),new_prefixes=[str(D.relative_to(R)).replace('\\','/'),str(O.relative_to(R)).replace('\\','/')]),ensure_ascii=False))
