"""Read the existing source cache; no network or source mutation."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and d.get('href','').startswith('http'):self.urls.append(d['href'])
cards=read('data/research/technology_atlas_v1/fact_cards.json')
priorities=read('data/research/technology_atlas_v1/category_visit_priorities.json')
ev={e['evidence_id']:e for e in read('data/research/technology_atlas_v1/evidence_ledger.json')}
ids={i for r in priorities for i in r['card_ids']}
for c in cards:
 if c['card_id'] not in ids:continue
 urls=[]
 for eid in c['evidence_ids']:
  e=ev[eid]
  if not e.get('cache_path') or e['year']!=2026:continue
  parser=Links();parser.feed((root/e['cache_path']).read_text(encoding='utf-8'))
  urls.extend(u for u in parser.urls if not any(x in u for x in ['jimtof.org','facebook','twitter','instagram','youtube','tokyo-bigsight']))
 print(c['card_id'],c['company'],list(dict.fromkeys(urls)))
