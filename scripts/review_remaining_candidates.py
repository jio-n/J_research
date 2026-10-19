"""Print bounded, source-located slices of the remaining candidate descriptions."""
import argparse,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
evidence=read('data/research/technology_atlas_v1/evidence_ledger.json')
used={e.get('source_record_id') for e in evidence if e['year']==2026 and not e['evidence_id'].startswith('EEX-')}
rows=[r for r in read('data/research/overview_v0/candidate_universe.json') if r['year']==2026 and r['record_id'] not in used]
p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int,default=75);p.add_argument('--full',action='store_true');p.add_argument('--compare',default='');a=p.parse_args()
terms=r'フィジカル|エージェント|(?<![A-Za-z])AI(?![A-Za-z])|自律|自動化|ロボット|自動搬送|無人|(?<![A-Za-z])(?:DX|IoT|MES|CAM|CAD)(?![A-Za-z])|デジタル|生産管理|工程管理|監視|シミュレ|最適化|自動測定|自動検査|予知|補正'
for i,r in enumerate(rows,1):
 if a.compare:
  if i not in [int(x) for x in a.compare.split(',')]:continue
  old=read('data/exhibitor_details_2024.json')
  import unicodedata
  norm=lambda s:re.sub(r'\s+','',unicodedata.normalize('NFKC',s)).casefold()
  matches=[d for d in old if norm(d['company_name'])==r['normalized_name']]
  print(f'N{i:03} {r["company_name"]} [{r["booth"]}]')
  print('2024: '+(' / '.join(d['exhibition_introduction']+' '+d['main_exhibits'] for d in matches) or '同一名称の詳細なし'))
  print('2026: '+r['exhibition_content']+' '+r['main_exhibits'])
  continue
 if not a.start<=i<=a.end:continue
 text=r['exhibition_content']+'\n'+r['main_exhibits']
 sentences=[s.strip() for s in re.split(r'(?<=[。!?])|\n',text) if s.strip()]
 matched=[s for s in sentences if re.search(terms,s,re.I)]
 excerpt=' / '.join(matched or sentences)
 print(f'N{i:03} {r["company_name"]} [{r["booth"]}] '+(text if a.full else excerpt[:135]))
