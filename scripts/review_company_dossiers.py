"""Print evidence from both years for the explicit cross-domain review set."""
import argparse,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/research/overview_v0'
names=['DMG森精機','ファナック','オークマ','ヤマザキマザック','ベッコフオートメーション','EPLAN','Hexagon Manufacturing Intelligence','ジェービーエムエンジニアリング','CGTech','オートデスク','たけびし','シーイーシー','Smart Craft','ものレボ','ソフィックス','パナソニックプロダクションエンジニアリング','ミツトヨ','レニショー','ブルーム-ノボテスト','マーポス','HACARUS','日東商事','ハイデンハイン','モリマシナリー','イマオコーポレーション','エヌティーツール','牧野フライス製作所','松浦機械製作所','中村留精密工業','TAKISAWA','シマダマシンツール','日本精工','日本エスケイエフ','Wintech Automation','Walter Maschinenbau','Innovalia Metrology','ニコン','ミロクリエ','UEL','テクノア','匠技研工業','興和オプトロニクス']
def norm(s):return re.sub(r'\s+','',unicodedata.normalize('NFKC',s)).casefold()
details={y:json.loads((ROOT/'data'/f'exhibitor_details_{y}.json').read_text(encoding='utf-8')) for y in (2024,2026)}
dossiers=[]
for i,name in enumerate(names,1):
 d={'review_id':f'V{i:03}','selection':name,'years':{str(y):[r for r in details[y] if (norm(r['company_name']) in ('uel株式会社','株式会社uel') if name=='UEL' else norm(name) in norm(r['company_name']))] for y in details}}
 dossiers.append(d)
(OUT/'review_dossiers.json').write_text(json.dumps(dossiers,ensure_ascii=False,indent=2),encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int,default=len(names));p.add_argument('--full',action='store_true');args=p.parse_args()
for d in dossiers[args.start-1:args.end]:
 print('\n'+d['review_id']+' '+d['selection'])
 for year,rows in d['years'].items():
  if not rows:print(year+' 詳細データなし：比較不能');continue
  for r in rows:
   text=r['exhibition_introduction']+'\n'+r['main_exhibits']
   print(year+' '+r['booth']+' '+r['exhibitor_record_id']+' '+(text if args.full else text[:680]))
