import pathlib,json,re,unicodedata,csv
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
def read(s):return json.loads((R/s).read_text(encoding='utf-8-sig'))
gap=read('data/research/visit_gap_review_20261023_163347/research.json')
astra=read('data/research/astra_refinement_20261023_013112/research.json')
current=read('data/research/overlap_column_20261025_172348/link_plan.json')
def key(s):
 s=unicodedata.normalize('NFKC',s).casefold();s=re.sub(r'\([^)]*\)','',s)
 return re.sub(r'[\s.,・/&-]','',s.replace('株式会社','').replace('有限会社',''))
selected={key(v[0]) for sh in current['sheets'] for v in sh['values']}
allrows=list(csv.DictReader((R/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig')))
byid={r['exhibitor_record_id']:r for r in allrows}
items={x['id']:dict(x,_source='visit_gap_review_20261023_163347') for x in gap['items']+gap['excluded_items']}
for x in astra['items']:
 if x['id'] not in items:items[x['id']]=dict(x,_source='astra_refinement_20261023_013112')
 elif '今回原典照合' in x.get('refinement_review',''):
  old=items[x['id']];items[x['id']]=dict(old,**{k:v for k,v in x.items() if k not in ['visit_analysis','suggested_rank']},_source='astra_refinement_20261023_013112＋gap訪問分析')
outside=[];covered=[]
for x in items.values():
 keys={key(x['company'])}|{key(byid[i]['company_name']) for i in x.get('listing_ids',[]) if i in byid}
 if keys&selected:covered.append(x)
 else:outside.append(x)
(D/'_private/outside_raw.json').write_text(json.dumps(outside,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'_private/all_items.json').write_text(json.dumps(list(items.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'current_companies':len(selected),'union_items':len(items),'outside_items':len(outside),'outside_companies':len({key(x['company']) for x in outside}),'already_listed_items':len(covered)},ensure_ascii=False))
for x in outside:
 tags=x.get('tag_names',[])
 if 'AI' in tags or 'フィジカルAI' in tags or '自律化' in tags or x.get('visit_analysis',{}).get('tier')=='A':
  print(x['id'],x['company'],','.join(x.get('booths',[])),x['item'],'｜',','.join(tags),'｜',x.get('exhibit',''))
