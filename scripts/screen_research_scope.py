"""Broad discovery only; keyword hits are candidates, not technical conclusions."""
import csv,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/research/overview_v0'
OUT.mkdir(parents=True,exist_ok=True)
patterns={
 'AI・自律':r'(?<![A-Za-z])AI(?![A-Za-z])|人工知能|機械学習|深層学習|自律|エージェント|machine learning|deep learning|autonomous',
 '加工準備・ツイン':r'デジタルツイン|シミュレ|自動プログラ|(?<![A-Za-z])(?:CAD|CAM)(?![A-Za-z])|工程設計|工程計画|見積|digital twin|simulation',
 '自動化・省人':r'自動化|省人|省力|無人|ロボット|ハンドリング|自動搬送|自動計測|自動測定|自動検査|automation|robot|unmanned',
 '計測・状態適応':r'機上計測|加工監視|状態監視|異常検|予知|予防保全|適応制御|補正|インプロセス|in.process|condition monitoring',
 '工場データ・運用':r'(?<![A-Za-z])(?:DX|AX|IoT|MES|APS|OPC)(?![A-Za-z])|データ連携|データ活用|稼働監視|稼働管理|工程管理|生産管理|工具管理|最適化|デジタル化|smart factory'
}
def norm(name):return re.sub(r'\s+','',unicodedata.normalize('NFKC',name)).casefold()
allrows=[]
report={}
for year in (2024,2026):
 master=json.loads((ROOT/'data'/f'exhibitors_{year}.json').read_text(encoding='utf-8'))
 details=json.loads((ROOT/'data'/f'exhibitor_details_{year}.json').read_text(encoding='utf-8'))
 byid={r['exhibitor_record_id']:r for r in details}
 rows=[]
 for m in master:
  d=byid.get(m['exhibitor_record_id'],{})
  text=d.get('exhibition_introduction','')+'\n'+d.get('main_exhibits','')
  hits=[k for k,p in patterns.items() if re.search(p,text,re.I)]
  if hits:
   sentences=re.split(r'(?<=[。.!?])\s*|\n',text)
   selected=[s.strip() for s in sentences if s.strip() and any(re.search(patterns[k],s,re.I) for k in hits)]
   rows.append(dict(year=year,company_name=m['company_name'],normalized_name=norm(m['company_name']),booth=m['booth'],record_id=m['exhibitor_record_id'],candidate_dimensions=';'.join(hits),discovery_excerpt=' / '.join(selected)[:380],exhibition_content=d.get('exhibition_introduction',''),main_exhibits=d.get('main_exhibits',''),detail_url=m['detail_url'],cache_path=d.get('cache_path',''),status='機械抽出候補・意味内容の精査前'))
 report[str(year)]={'listing_rows':len(master),'details_retrieved':len(details),'candidate_rows':len(rows),'candidate_name_keys':len({r['normalized_name'] for r in rows}),'dimensions':{k:len({r['normalized_name'] for r in rows if k in r['candidate_dimensions'].split(';')}) for k in patterns}}
 allrows.extend(rows)
with (OUT/'candidate_universe.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
(OUT/'candidate_universe.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2),encoding='utf-8')
report['caveat']='名称キーの重複除去。法人同一性未確認。各区分は重複し、掲載文の語による候補抽出であり採用率・市場比率・技術成熟度を表さない。詳細URLなし619行と原典説明なし行には未捕捉の可能性。'
(OUT/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
seen=set()
for r in allrows:
 if r['year']==2026 and r['normalized_name'] not in seen:
  seen.add(r['normalized_name'])
  print(f"{r['record_id']} {r['company_name']} [{r['candidate_dimensions']}] {r['discovery_excerpt']}")
