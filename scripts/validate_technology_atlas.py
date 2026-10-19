"""Bounded integrity checks and a static preview of the simple SVG figure."""
import csv, hashlib, json, re, xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/research/technology_atlas_v1'
load=lambda n:json.loads((OUT/n).read_text(encoding='utf-8'))
cards=load('fact_cards.json');tasks=load('technology_taxonomy.json');ev=load('evidence_ledger.json')
ids={c['card_id'] for c in cards};eids={e['evidence_id'] for e in ev}
assert len(cards)==len(ids)==334
assert len({c['review_id'] for c in cards})==309
assert len(tasks)==36
assert len(ev)==len(eids)==626
assert {c['task_id'] for c in cards}<={t['task_id'] for t in tasks}
for c in cards:
 assert c['evidence_ids'] and set(c['evidence_ids'])<=eids
 assert all(c[k] for k in ['deployment','system_configuration','input','mechanism','output','human_boundary','baseline_2024','observation_2026','unresolved'])
 assert {s['evidence_id'] for s in c['source_locations']}==set(c['evidence_ids'])
for e in ev:
 assert e['url'].startswith('https://') and e['locator']
 if e.get('cache_path'):assert (ROOT/e['cache_path']).exists()
for r in load('technology_relationships.json'):
 assert set(r['from_cards']+r['to_cards'])<=ids
 assert set(r['evidence_ids'])<=eids
for stem in ['fact_cards','technology_taxonomy','evidence_ledger','task_comparison_2024_2026','technology_relationships','category_index','category_definitions','candidate_screening','category_visit_priorities','priority_deepening','method_comparison','technology_method_positions','year_change_patterns','common_issues','research_candidates','open_questions','company_alias_confirmations']:
 js=load(stem+'.json')
 with (OUT/(stem+'.csv')).open(encoding='utf-8-sig',newline='') as f:cs=list(csv.DictReader(f))
 assert len(js)==len(cs)
 for c,j in zip(cs,js):
  assert all(c[k]==(json.dumps(j[k],ensure_ascii=False) if isinstance(j.get(k),(list,dict)) else str(j.get(k,''))) for k in c),(stem,j.get('card_id',j.get('evidence_id','')))
report=ROOT/'outputs/JIMTOF2026_技術整理と全体マップ_v1.html'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.cards=0;self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag=='article' and 'card' in a.get('class','').split():self.cards+=1
 def handle_data(self,data):self.text.append(data)
page=Page();page.feed(report.read_text(encoding='utf-8'))
docids=page.ids
assert len(docids)==len(set(docids))
assert page.cards==len(cards)
for href in page.links:
 if href.startswith('#'):assert href[1:] in docids,href
 elif not href.startswith('https://'):assert (report.parent/href).resolve().exists(),href
assert '重点42社' not in ''.join(page.text) and '残る300' not in ''.join(page.text)
byname={c['item']:c for c in cards}
assert '参考出品' in byname['TR-20W：主軸の切粉除去']['product_stage']
assert '実機なし' in byname['ツールソムリエ']['exhibition_status']
assert '未確認' in byname['Condition Agent']['exhibition_status']
assert '投入時期要問い合わせ' in byname['TwinCAT CoAgent for Operations']['product_stage']
assert '将来構想' in byname['Eplan Copilot']['output']
assert '2024から継続'==byname['Renishaw Central＋IPC']['delta_type']

# Rasterize only the authored rect/text primitives. This is an image preview,
# not a browser engine or an HTML interaction test. Use the same installed font.
svg=ET.parse(ROOT/'outputs/JIMTOF2026_技術全体マップ_v1.svg').getroot()
canvas=Image.new('RGB',(1600,950),'white');draw=ImageDraw.Draw(canvas)
font_dir=Path('C:/Windows/Fonts')
regular=font_dir/'meiryo.ttc';bold=font_dir/'meiryob.ttc'
assert regular.exists() and bold.exists()
overflows=[]
for el in svg.iter():
 tag=el.tag.split('}')[-1];a=el.attrib
 if tag=='rect':
  x,y,w,h=[float(a.get(k,0)) for k in ['x','y','width','height']]
  box=(round(x),round(y),round(x+w),round(y+h))
  draw.rounded_rectangle(box,radius=float(a.get('rx',0)),fill=a.get('fill','white'),outline=a.get('stroke'),width=1)
 elif tag=='text':
  size=int(a.get('font-size',16));f=ImageFont.truetype(str(bold if a.get('font-weight')=='bold' else regular),size)
  text=''.join(el.itertext());x,y=float(a['x']),float(a['y'])
  fill='white' if 'fill:white' in a.get('style','') else '#203b50'
  draw.text((x,y),text,font=f,fill=fill,anchor='ls')
  if x+draw.textlength(text,font=f)>1595:overflows.append(text)
assert not overflows,overflows
png=ROOT/'outputs/JIMTOF2026_技術全体マップ_v1.png'
canvas.save(png)
result=dict(status='passed',fact_cards=len(cards),companies=309,task_categories=len(tasks),evidence_records=len(ev),checks=['カード必須項目・根拠参照','出典URL・原典キャッシュ','CSV/JSON全件一致','HTML内リンク・出力ファイル','展示確度の重要な区別','SVG構文・文字の図外はみ出し'],preview_path=str(png),html_browser_interaction='未検証：ブラウザーのURLポリシーがfile://の自動観察を拒否。回避は実施せず。',sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [report,png,OUT/'fact_cards.csv']})
(ROOT/'checkpoints/technology_atlas_v1_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
cp=ROOT/'checkpoints/technology_atlas_v1.json'
checkpoint=json.loads(cp.read_text(encoding='utf-8'));checkpoint.update(status='成果物保存・整合性検証済み。ブラウザー操作は未検証',validation_path='checkpoints/technology_atlas_v1_validation.json',next_action='研究候補5件の既存機能との重複・権限・失敗復帰・適用条件を現地質問と限定実験で確認し採否を検討。最終1枚は未集約。')
cp.write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
