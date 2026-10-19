"""Check the category links and the saved Excel package against the owning data."""
import hashlib,json,re,zipfile
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
data=root/'data/research/technology_atlas_v1'
read=lambda n:json.loads((data/(n+'.json')).read_text(encoding='utf-8'))
cards,rows,defs=[read(n) for n in ['fact_cards','category_index','category_definitions']]
priorities,audit=[read(n) for n in ['category_visit_priorities','candidate_screening']]
assert len(rows)==548 and len(defs)==9 and len(cards)==334
assert len(priorities)==37 and len({r['company'] for r in priorities})==28
assert len(audit)==345 and len({r['normalized_name'] for r in audit})==342
assert sum(r['disposition'].startswith('カテゴリー付与') for r in audit)==265
assert sum(r['disposition'].startswith('対象外') for r in audit)==32
assert sum(r['disposition'].startswith('分類保留') for r in audit)==1
focused=[c for c in cards if '重点' in c['review_depth'] and c['card_id'].startswith('AC')]
assert len(focused)==19
assert sum(c['review_depth']=='2024・2026の原典全文を重点比較' for c in focused)==12
assert sum(c['review_depth'].startswith('2024・2026の原典全文を重点比較') for c in focused)==13
assert sum('2024同名原典なし' in c['review_depth'] for c in focused)==6
byid={c['card_id']:c for c in cards}
assert '2024公式' in byid['AC051']['baseline_2024']
assert byid['AC225']['delta_type']=='2024から継続'
assert 'AI使用を断定せず' in byid['AC146']['delta_interpretation']
assert 'E7073内' in byid['AC146']['exhibition_status']
assert '学習・検証用データ' in byid['AC273']['delta_interpretation']
for r in priorities:
 assert set(r['card_ids'])<={c['card_id'] for c in cards}
 assert all(r[k] for k in ['why_visit','baseline_2024','observation_2026','comparison_interpretation','on_site_check'])
 assert r['category_order']==1+sum(p['category_id']==r['category_id'] for p in priorities[:priorities.index(r)])
assert {r['card_id'] for r in rows}=={c['card_id'] for c in cards}
assert {r['category_id'] for r in rows}=={d['category_id'] for d in defs}
for d in defs:
 subset=[r for r in rows if r['category_id']==d['category_id']]
 assert len(subset)==d['item_count']
 assert len({r['company'] for r in subset})==d['company_count']
assert next(c for c in cards if c['card_id']=='FC018')['booths_2026']==['E2013']
assert next(c for c in cards if c['card_id']=='FC019')['booths_2026']==['E7035']
assert not any(r['card_id'] in ['FC031','FC033','FC054'] and r['category_id']=='C08' for r in rows)

class Page(HTMLParser):
 def __init__(self):super().__init__();self.rows=0;self.companies=0;self.labels=0;self.in_dt=False;self.old_label=0
 def handle_starttag(self,t,a):
  a=dict(a);classes=a.get('class','').split()
  if t=='tr' and 'category-row' in classes:self.rows+=1
  if t=='h2' and 'company-name' in classes:self.companies+=1
  if t=='dt':self.in_dt=True
 def handle_endtag(self,t):
  if t=='dt':self.in_dt=False
 def handle_data(self,s):
  if self.in_dt and s=='システムの構成':self.labels+=1
  if self.in_dt and s=='ロボット・機械':self.old_label+=1
report=root/'outputs/JIMTOF2026_技術整理と全体マップ_v1.html'
html=report.read_text(encoding='utf-8');page=Page();page.feed(html)
assert (page.rows,page.companies,page.labels,page.old_label)==(len(rows),len(cards),len(cards),0)
assert html.count('class="priority-row"')==len(priorities)
assert html.count('class="screening-row"')==len(audit)
assert 'technology_atlas_v2' not in html
script=re.search(r'<script>(.*?)</script>',html,re.S).group(1)
(root/'.build/category_index/atlas_interactions.js').write_text(script,encoding='utf-8')

p=root/'outputs/JIMTOF2026_カテゴリー別出展索引_v1.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 xml=[ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')) for i in range(1,8)]
 for sh in xml:
  assert not [c for c in sh.findall('.//m:c',ns) if c.get('t')=='e']
  assert sh.find('m:sheetViews/m:sheetView/m:pane',ns).get('ySplit')=='6'
  assert sh.find('m:tableParts',ns) is not None
 tables=[ET.fromstring(z.read(f'xl/tables/table{i}.xml')) for i in range(1,13)]
 assert [t.get('ref') for t in tables]==['A6:F16','A22:H32','A37:H43','A6:G11','A17:J22','A29:J34','A39:J51',f'A6:X{len(priorities)+6}',f'A6:K{len(rows)+6}',f'A6:AB{len(cards)+6}','A6:D15',f'A6:H{len(audit)+6}']
 assert all(t.find('m:autoFilter',ns) is not None for t in tables)
 def cells(sh):return {c.get('r'):c for c in sh.findall('.//m:c',ns)}
 v,a,b,d,s=[cells(sh) for sh in xml[2:]]
 def value(c):return c.find('m:v',ns).text if c.find('m:v',ns) is not None else ''
 for i,r in enumerate(priorities,7):
  assert [value(v[f'{col}{i}']) for col in ['A','B','D','E','F','G','H','I','L','O','P']]==[r['category'],str(r['category_order']),r['company'],' / '.join(r['booths_2026']),r['exhibits'],r['why_visit'],r['baseline_2024'],r['observation_2026'],r['on_site_check'],'\n'.join(r['card_ids']),r['card_ids'][0]]
  assert 'HYPERLINK(' in v[f'P{i}'].find('m:f',ns).text
  assert [value(v[f'{col}{i}']) for col in ['S','T','U','V','W','X']]==[r[k] for k in ['ai_judgment','execution','human_preparation','human_approval','human_exception','limits']]
 for i,r in enumerate(rows,7):
  assert [value(a[f'{col}{i}']) for col in ['A','B','C','D','E','F','G','H']]==[r['category'],r['subcategory'],r['company'],r['item'],' / '.join(r['booths_2026']),r['classification_basis'],r['relation_scope'],r['card_id']]
  formula=a[f'H{i}'].find('m:f',ns).text
  assert 'HYPERLINK(' in formula and 'MATCH(' in formula and r['card_id'] in formula
 for i,c in enumerate(cards,7):
  assert value(b[f'A{i}'])==c['card_id'] and value(b[f'B{i}'])==c['company']
  assert value(b[f'H{i}'])==c['system_configuration']
  if 'deepening' in c:
   assert [value(b[f'{col}{i}']) for col in ['V','W','X','Y','Z','AA','AB']]==[c['deepening'][k] for k in ['ai_scope','ai_judgment','execution','human_preparation','human_approval','human_exception','limits']]
 for i,definition in enumerate(defs,7):assert int(value(d[f'D{i}']))==definition['item_count']
 for i,r in enumerate(audit,7):assert [value(s[f'{col}{i}']) for col in ['A','B','C','D','F']]==[r['company'],r['booth'],r['disposition'],r['reason'],r['url']]
 wb=ET.fromstring(z.read('xl/workbook.xml'))
 assert [s.get('name') for s in wb.findall('m:sheets/m:sheet',ns)]==['横断比較・技術マップ','共通課題・研究候補','カテゴリー別訪問優先','カテゴリー索引','展示詳細','カテゴリー定義','候補仕分け']
 sm,rs=[cells(sh) for sh in xml[:2]]
 funcs=['基盤・入力整備','判定・表示','提案・生成','ソフト実行','実機動作']
 positions=read('technology_method_positions')
 for i,m in enumerate(read('method_comparison'),7):
  assert value(sm[f'A{i}'])==m['method_id']+' '+m['method']
  for col,func in zip('BCDEF',funcs):
   expected='\n\n'.join(f"{p['company']} {p['card_id']}\n{p['task']}\n【{p['status']}】" for p in positions if p['method_id']==m['method_id'] and p['function']==func) or '今回の配置なし'
   assert value(sm[f'{col}{i}'])==expected
 for i,r in enumerate(read('method_comparison'),23):
  assert [value(sm[f'{col}{i}']) for col in 'BCDEFGH']==[r['mechanism'],r['human_boundary'],r['comparison'],r['year_change'],' / '.join(r['card_ids']),' / '.join(r['evidence_ids']),r['statement_type']]
 for i,r in enumerate(read('year_change_patterns'),38):
  assert [value(sm[f'{col}{i}']) for col in 'BCDEF']==[r['baseline'],r['current'],r['interpretation'],' / '.join(r['card_ids']),' / '.join(r['evidence_ids'])]
 for i,r in enumerate(read('common_issues'),7):
  assert [value(rs[f'{col}{i}']) for col in 'BCDEF']==[r['observed_facts'],r['shared_issue'],r['limits'],' / '.join(r['card_ids']),' / '.join(r['evidence_ids'])]
 for i,r in enumerate(read('research_candidates'),18):
  assert [value(rs[f'{col}{i}']) for col in 'BCDEFGHIJ']==[r['customer_problem'],r['technical_approach'],r['experiment'],r['metrics'],r['adoption_condition'],' / '.join(r['card_ids']),' / '.join(r['evidence_ids']),r['stage'],r['statement_type']]
 for i,r in enumerate(read('research_candidates'),30):
  assert [value(rs[f'{col}{i}']) for col in 'ABCDEFGHIJ']==[r['theme_id']+' '+r['decision'],r['existing_capabilities'],r['remaining_hypothesis'],r['check_first'],r['experiment_gate'],r['adoption_condition'],' / '.join(r['card_ids']),' / '.join(r['evidence_ids']),r['assessment_date'],r['assessment_status']]
 for i,r in enumerate(read('open_questions'),40):
  assert [value(rs[f'{col}{i}']) for col in 'ABCDEFGHIJ']==[r['question_id']+' '+r['title']+'\n'+' / '.join(r['companies'])+'\n'+' / '.join(r['booths_2026']),r['known_facts'],r['question'],r['requested_evidence'],r['experiment_gate'],r['unresolved'],' / '.join(r['card_ids']),' / '.join(r['evidence_ids']),r['status'],r['checked_date']]

deep=read('priority_deepening')
assert len(deep)==33 and len({r['company'] for r in deep})==28
assert {r['card_id'] for r in deep}=={cid for r in priorities for cid in r['card_ids']}
assert sum(r['source_status'].startswith('公式出展説明まで') for r in deep)==2
assert html.count('class="role-row"')==33
assert '2024/7/25' in byid['FC020']['baseline_2024']
assert 'CAPTO' in byid['AC214']['baseline_2024'] and '初披露' in byid['AC214']['baseline_2024']
assert '顧客のMastercamデータで学習しない' in byid['FC020']['mechanism']
assert '2024' in byid['FC014']['baseline_2024'] and 'ONNX' in byid['FC014']['baseline_2024']
assert '2025年7月9日販売開始' in byid['FC036']['product_stage']
assert '同一機体か未確認' in byid['AC098']['human_boundary']

result=dict(status='passed',categories=9,companies=309,cards=len(cards),category_associations=len(rows),visit_priorities=len(priorities),priority_companies=28,candidate_rows=len(audit),html_company_headings=len(cards),system_configuration_labels=len(cards),excel_tables=12,excel_sheets=7,excel_detail_links=len(rows)+len(priorities),checks=['HTMLとExcelの全カテゴリー対応一致','訪問順37件・年度差分・現地確認事項の一致','候補345掲載の判定・理由の一致','展示詳細334件の構成・企業名','Excelフィルター・固定見出し・リンク式・表示値','Excelパッケージとエラー値','方式配置35件・比較10件・年度変化6件・共通課題5件・研究候補5件の全内容一致','追補の研究判断5件・現地確認12件を全セル照合','元CSV/JSONの整合性はtechnology_atlas_v1_validationで確認'],html_browser_interaction='file://のブラウザー自動観察はポリシー制限のため未検証',native_excel_open='未確認。保存内容・式・リンク先・画像プレビューを検証。',workbook_path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
result['deepening']=dict(companies=28,items=33,checks=['全優先カードと深掘り対象の一致','AI判断・実行・人の事前準備・承認・例外対応のExcel全行一致','2024と2026の初登場年の混同防止','HTML横断表33行・出典とカードへのリンク'])
(root/'checkpoints/category_workbook_v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
cp=root/'checkpoints/technology_atlas_v1.json'
checkpoint=json.loads(cp.read_text(encoding='utf-8'));checkpoint.update(category_workbook_path=str(p),category_validation='checkpoints/category_workbook_v1.json')
cp.write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
