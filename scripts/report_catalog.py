"""Keep the broad candidate directory separate from the 57 researched comparisons."""
import csv,json,pathlib,re
R=pathlib.Path(__file__).resolve().parents[1]
P=R/'data/research/technology_atlas_v1'
O=R/'data/research/report_v0'

# Membership was read against the cached exhibitor descriptions. A membership
# identifies a relevant task, not proof that the exhibitor uses AI for that task.
GROUPS={
'B01':'FC028 FC062 AC195 AC074 AC232 FC061',
'B02':'FC018 FC020 FC023 FC060 AC024 AC031 AC047 AC061 AC074 AC076 AC095 AC098 AC117 AC119 AC131 AC194 AC215 AC284',
'B03':'FC022 FC015 FC064 AC082 AC115 AC136 AC175 AC191 AC289',
'B04':'FC011 FC012 FC016 FC017 AC018 AC240',
'B05':'FC009',
'B06':'FC033 FC054 AC021 AC052 AC085 AC276',
'B07':'FC036 FC037 AC088 AC107 AC154 AC221 AC252',
'B08':'FC038 FC039 FC040 FC063 FC064 FC035 AC271 AC257',
'B09':'FC004 FC013 FC052 FC053 FC058 AC003 AC007 AC014 AC071 AC153 AC183 AC210 AC225 AC231 AC288',
'B10':'FC042 FC043 FC048 FC051 AC012 AC017 AC027 AC033 AC036 AC037 AC045 AC057 AC063 AC068 AC075 AC081 AC105 AC151 AC157 AC163 AC184 AC187 AC192 AC198 AC201 AC214 AC227 AC243 AC249 AC278',
'B11':'FC001 FC002 FC008 FC010 FC044 FC046 FC047 FC050 FC055 FC067 AC001 AC009 AC013 AC019 AC039 AC040 AC041 AC058 AC069 AC073 AC090 AC091 AC093 AC094 AC123 AC129 AC130 AC139 AC140 AC141 AC164 AC171 AC177 AC179 AC186 AC188 AC193 AC224 AC232 AC235 AC246 AC269 AC271 AC287',
'B12':'FC045 FC049 AC006 AC016 AC022 AC028 AC030 AC050 AC051 AC066 AC083 AC086 AC089 AC097 AC108 AC120 AC122 AC126 AC127 AC133 AC146 AC160 AC174 AC181 AC201 AC212 AC213 AC223 AC229 AC230 AC238 AC242 AC262 AC264',
'B13':'FC003 FC013 FC030 FC031 FC058 FC066',
'B14':'FC026 FC027 FC061 FC065 AC025 AC026 AC039 AC041 AC070 AC074 AC095 AC103 AC106 AC109 AC156 AC180 AC211 AC220 AC226',
'B15':'FC014 FC024 FC025 FC029 FC059 FC068 AC008 AC145 AC185 AC240',
'B16':'FC007 AC019 AC082 AC098 AC172 AC273 AC286',
'B17':'FC005 FC006 AC019 AC143 AC159',
'B18':'FC007 FC016 FC021 FC023 FC060 AC018 AC024 AC031 AC055 AC061 AC074 AC076 AC082 AC095 AC098 AC111 AC117 AC119 AC194 AC215 AC228 AC258 AC286',
'B19':'FC019 FC032 FC034 FC056 FC057 AC029 AC046 AC060 AC063 AC068 AC077 AC088 AC121 AC125 AC142 AC148 AC151 AC155 AC162 AC166 AC176 AC190 AC206 AC209 AC215 AC218 AC220 AC232 AC246 AC257 AC279 AC280 AC297',
'B20':'FC045 FC053 AC016 AC023 AC056 AC113 AC127 AC134 AC137 AC150 AC169 AC173 AC185 AC203 AC205 AC231 AC234 AC241 AC269 AC293',
'B21':'FC044 FC068 FC069 AC002 AC007 AC008 AC027 AC030 AC064 AC065 AC066 AC067 AC072 AC078 AC079 AC083 AC113 AC137 AC143 AC145 AC158 AC165 AC168 AC169 AC175 AC182 AC189 AC208 AC210 AC222 AC233 AC240 AC250 AC254',
'B22':'AC001 AC010 AC011 AC015 AC021 AC032 AC034 AC041 AC043 AC048 AC049 AC054 AC059 AC069 AC077 AC086 AC096 AC100 AC101 AC102 AC110 AC114 AC116 AC118 AC123 AC129 AC139 AC149 AC151 AC156 AC160 AC167 AC170 AC171 AC174 AC179 AC188 AC193 AC197 AC198 AC199 AC209 AC212 AC213 AC219 AC220 AC224 AC235 AC236 AC238 AC244 AC245 AC247 AC248 AC251 AC252 AC256 AC260 AC268 AC272 AC275 AC276 AC280 AC282 AC289 AC291 AC292 AC298',
'B23':'FC041 AC038 AC042 AC062 AC104 AC124 AC138 AC216 AC217 AC265 AC295',
'B24':'FC016 FC023 FC026 AC074 AC104 AC152 AC195 AC207 AC228 AC232 AC279 AC286 AC295',
'B25':'AC098 AC204 AC245',
}
EXTRA=[
('B18','D1','CAD・金型設計・NC検証','形状の設計変更や加工前の確認に手間がかかる。','CAD/CAM統合、ルールによる設計支援、NCシミュレーション。'),
('B19','D3','自動計測・測定計画・品質データ','測定の段取り・搬送・記録に人手が残り、結果が加工改善につながりにくい。','自動測定、測定プログラム作成、ロボット計測、品質データの管理。'),
('B20','D4','クーラント・潤滑・清掃の省人化','補充・濃度管理・切粉処理などの保守作業で運転が途切れる。','自動希釈・補給、ろ過、状態監視、清掃機構。'),
('B21','D6','安全監視・自動化を支える機器','無人運転やロボット導入には、安全確保と機器・配線・力の伝達が必要。','安全センサー、画像による人検出、ハンド・力覚・駆動・接続部品。'),
('B22','D4','自動加工セル・工程集約','設備間の持替えや繰返し作業が、人手・待ち時間・品質差につながる。','自動加工サイクル、工程集約、ローダー・加工・計測を組み合わせるセル。'),
('B23','D5','工具データ・在庫・購買','工具を探す・登録する・補充する手間や、在庫情報の分断がある。','工具データベース、プリセット・在庫管理、貸出記録、ルールによる購買。'),
('B24','D1','図面・設計データの管理と連携','図面・工具・品質・工程情報が別々に保存され、再利用しにくい。','図面・文書管理、CADデータ変換、標準工具データ、設計と品質の連携。'),
('B25','D5','作業分析・技能継承・教育','作業を記録・分析し、改善点や技能を共有する負担がある。','動画の作業分節、視線分析、訓練用シミュレーション、運用支援。'),
('B00','D0','用途の詳細が未確認の候補','取得した説明だけでは、関連する個別タスクを確定できない。','分類保留。AI・自動化という語だけで具体的な方式を割り当てない。'),
]
OVERRIDES={
'AC074':('図面管理・CAM・稼働可視化','NAZCA5 GEMBACO、CAD/CAM、LINKA3を紹介。図面管理へのAI使用は未確認。'),
'AC232':('加工・計測セルと図面・設備管理','加工機・協働ロボット・三次元測定機のセルと「ゲンバト」を紹介。'),
'FC061':('購買見積・発注・受入と実績入力','TECHSの購買APIとスマートフォン実績入力。部品の加工見積AIとは別。'),
'AC018':('油圧・電気回路の設計と動作確認','Automation Studioで回路を設計・シミュレーション。生成AIによる設計とは未確認。'),
'AC240':('電気・制御盤設計と盤製作の連携','電気設計から制御盤製作への工程連携を紹介。筐体・盤内配線・エッジ用機器も展示。'),
'AC024':('CAMの自動プログラミングとNC検証','CAMWorks・SOLIDWORKS CAMの自動プログラミング、EurekaのGコード検証を紹介。'),
'AC031':('5軸等の加工プログラム作成と事前検証','hyperMILL・Mastercam・OneCNC・Vericut。AUTOMATION CenterによるCAM自動化を紹介。'),
'AC047':('CAMプログラミングの自動化','hyperMILLとプログラミング自動化のコンセプトを紹介。AI方式の詳細は未確認。'),
'AC061':('部品・金型の加工プログラム作成','Speedy mill Next・Cimatron等のCAD/CAM。AIによる工程判断の範囲は未確認。'),
'AC076':('設計からNCプログラム作成への連携','TopSolidのCAD/CAM統合と、穴あけから5軸・複合加工までのプログラム作成支援。'),
'AC095':('部品・金型のCAD/CAMと生産管理','CAM-TOOL・EXCESS-HYBRIDⅡ・PartsCAM等。AI・DXの紹介内容と機能の対応は未精査。'),
'AC117':('部品・金型の設計と加工プログラム作成','GO2camによる部品加工、Cimatronによる金型・電極設計からCAMまでを紹介。'),
'AC119':('スキャンした形状から加工プログラムを作る','Mastercamとロボドリルでの加工、FlexSim等のデジタル化支援を紹介。'),
'AC194':('CAD/CAMとNCシミュレーション','Fusion、FeatureCAMによるプログラム自動化、ENCYのNCシミュレーションを紹介。'),
'AC215':('3D計測と金型補修・加工の連携','ZEISSの3D測定とCAMデータ活用、Tebis等のCAD/CAM・MESを紹介。'),
'AC284':('3Dモデルからレーザー加工へ','3Dモデル解析対応の自社CAMと5軸・レーザー加工制御を組み合わせる。'),
}
METHODS={
'B01':'OCR・類似図面検索、過去案件の参照、原価計算。図面管理と購買APIは関連用途として区別。',
'B02':'加工特徴の認識、履歴からの工程予測、工具経路・条件案の生成、CAD/CAMによるプログラミング。',
'B03':'物理シミュレーションによるNC事前最適化、負荷信号に応じた送り制御、切削力の計測。',
'B04':'対話によるPLCコード・I/O・HMI作成支援、電気設計資産の標準化、回路シミュレーション。',
'B05':'熱変位の構造・制御による抑制、温度を用いる補正、びびりに応じた主軸回転調整。',
'B06':'寸法・刃先形状を計測し、工具オフセットや加工条件へ反映。ルール補正とAI補正を区別。',
'B07':'良品との差を捉える画像学習、多面撮像と搬送、外観判定・数量計数。',
'B08':'刃先画像の診断、加工信号の監視、工具破損検出、摩耗履歴による寿命・交換時期の推定。',
'B09':'振動・電流・温度の状態監視、異常診断、記録やマニュアルを用いる保全知識支援。',
'B10':'爪・ハンド・工具・治具の交換機構、位置復旧、プリセット・芯出し・着座確認。',
'B11':'ローダー・協働ロボット・AMR・パレットシステムと加工機を組み合わせる。',
'B12':'画像・3D認識からの動作や軌道生成、力追従、工具の摩耗補償。固定手順の自動化も併記。',
'B13':'設備データ・文書を参照する対話支援、予測による運用支援、人が操作する遠隔介入。',
'B14':'MES・生産管理・自動日程調整、実績収集、設備稼働の可視化、API連携。',
'B15':'AutoML、ONNXなどのモデル実装、OPC UA・ゲートウェイ・OCRによる設備接続。',
'B16':'工作機械の仮想検証、工場・訓練シミュレーション、CADからの形状・物理属性データ生成。',
'B17':'生成AIを使うロボット駆動、ビジョン内蔵協働ロボット、人型・遠隔教示、開発中の最適化。',
}
SPLIT_EXHIBITS=[
 ('SUB001','FC047',['B02'],'GIBBSCAM2026','5軸・複合加工等の加工プログラム作成','2026公式出展説明でGIBBSCAM2026の展示・実演を記載。自動化・AIの具体範囲は未精査。'),
 ('SUB002','FC055',['B02'],'HELITRONIC TOOL STUDIO','切削工具の設計と加工プログラム作成','2026公式出展説明で、工具設計から加工プログラム作成までを支援するソフトウェアとして掲載。AI使用の記載は未確認。'),
 ('SUB003','AC098',['B02','B19'],'NX CAM／NX CMM','加工と測定のプログラムを準備する','2026公式の主な出展物にNX CAMとNX CMMを掲載。工作機械ツインや人型ロボットとは別の展示アイテム。各ソフトの生成AI機能・2024との機能差は未精査。'),
]

def enrich(d):
 cards=json.loads((P/'fact_cards.json').read_text('utf-8'))
 ev={x['evidence_id']:x for x in json.loads((P/'evidence_ledger.json').read_text('utf-8'))}
 ev.update({x['evidence_id']:x for x in d['evidence']})
 official_names={x['detail_url']:x['company_name'] for x in json.loads((R/'data/exhibitor_details_2026.json').read_text('utf-8'))}
 cases={c['card_id']:c for t in d['topics'] for c in t['cases']}
 for k,c in cases.items():
  if k.startswith('RPT'):cards.append(c['full_record'])
 for k,parent,ts,item,target,tech in SPLIT_EXHIBITS:
  base=next(c for c in cards if c['card_id']==parent)
  cards.append({**base,'card_id':k,'item':item,'task_id':'TASK99','task':target,'mechanism':tech,'baseline_2024':'この展示アイテムの2024掲載内容・機能差は未精査。同社の他製品の差分を流用しない。','observation_2026':tech,'delta_interpretation':'2026出展説明で当該アイテムを確認。2024との個別機能比較は保留。','human_boundary':'作成条件、修正・採用判断、実行前の確認範囲は未精査。','split_parent':parent})
 memberships={k:[tid for tid,ids in GROUPS.items() if k in ids.split()] for k in [c['card_id'] for c in cards]}
 for k,parent,ts,item,target,tech in SPLIT_EXHIBITS:memberships[k]=ts
 for t in d['topics']:
  for c in t['cases']:
   if t['topic_id'] not in memberships[c['card_id']]:memberships[c['card_id']].append(t['topic_id'])
 topics=[dict(topic_id=t['topic_id'],domain_id=t['domain'],title=t['title'],problem=t['problem'],technology=t['insight']) for t in d['topics']]
 for t in topics:t['technology']=METHODS[t['topic_id']]
 topics += [dict(topic_id=k,domain_id=did,title=name,problem=need,technology=tech) for k,did,name,need,tech in EXTRA]
 byid={t['topic_id']:t for t in topics}
 directory=[]
 for c in cards:
  k=c['card_id'];cc=cases.get(k);ids=list(dict.fromkeys(c['evidence_ids']+ (cc['evidence_ids'] if cc else [])))
  es=[ev[i] for i in ids]; links={str(y):list(dict.fromkeys(e['url'] for e in es if e['year']==y and 'jimtof.org/' in e['url'] and 'ESdetails' in e['url'])) for y in [2024,2026]}
  ts=memberships[k] or ['B00'];manual=OVERRIDES.get(k)
  target=cc['target'] if cc else manual[0] if manual else (c['task'] if c.get('task_id','TASK99')!='TASK99' or c.get('split_parent') else ' ／ '.join(byid[i]['title'] for i in ts))
  tech=cc['official_mechanism'] if cc else manual[1] if manual else c['mechanism']
  name=next((official_names[e['url']] for e in es if e['year']==2026 and e['url'] in official_names),c['company'])
  company_key=re.sub(r'\s+','',name)
  year_status='個別比較あり' if cc else '両年説明あり・機能差未判定' if links['2024'] and links['2026'] and c.get('task_id','TASK99')=='TASK99' else '比較記録あり' if links['2024'] and links['2026'] else '年度資料不足・比較不能'
  directory.append(dict(card_id=k,company=c['company'],company_key=company_key,item=c['item'],booths=c['booths_2026'],topic_ids=ts,domain_ids=list(dict.fromkeys(byid[i]['domain_id'] for i in ts)),target=target,technology=tech,need=c.get('customer_need','') if c.get('task_id','TASK99')!='TASK99' else ' ／ '.join(dict.fromkeys(byid[i]['problem'] for i in ts)),need_type='課題・用途の整理は分析。顧客調査による需要検証ではない。',depth='詳細比較済み' if cc else '個別タスク整理' if c.get('task_id','TASK99')!='TASK99' else '出展説明の一次分類',classification='出展説明・既存カードに基づく調査者の分類（分析）',baseline_2024=c['baseline_2024'],observation_2026=c['observation_2026'],year_change=cc['year_change'] if cc else c.get('delta_interpretation','機能差未判定'),year_status=year_status,human_boundary=cc['human_boundary'] if cc else c['human_boundary'],exhibition_status=c['exhibition_status'],product_stage=c['product_stage'],evidence_ids=ids,exhibitor_urls_2024=links['2024'],exhibitor_urls_2026=links['2026'],source_urls=list(dict.fromkeys(e['url'] for e in es)),case_id=cc['case_id'] if cc else '',checked_date=c.get('checked_date',''),related_note='関連（図面・文書管理）。AI見積の直接事例ではない。' if k in ['AC074','AC232'] else '関連（購買API）。加工原価見積AIとは別。' if k=='FC061' else ''))
 for t in topics:
  rows=[c for c in directory if t['topic_id'] in c['topic_ids']]
  t.update(card_ids=[c['card_id'] for c in rows],row_count=len(rows),company_count=len({c['company_key'] for c in rows}))
 catalog=dict(as_of='2026-10-19',topics=topics,entries=directory,evidence=[ev[i] for i in sorted({i for c in directory for i in c['evidence_ids']})],scope=dict(atlas_cards=334,additional_research_cards=7,split_exhibit_cards=3,directory_rows=len(directory),company_name_keys=len({c['company_key'] for c in directory}),classified_rows=sum(c['topic_ids']!=['B00'] for c in directory),pending_card_ids=[c['card_id'] for c in directory if c['topic_ids']==['B00']],topic_associations=sum(len(c['topic_ids']) for c in directory),comparison_rows=len(cases),note='取得済み334候補＋追加調査7＋既存説明から別展示を分離3カード。各社の全製品を分解した件数ではない。テーマ重複・同一企業の複数掲載を含む。2026公式詳細820件の関連語検索を補助に実施。詳細URLのない619掲載行は未取得。'))
 d['catalog']=catalog
 d['evidence']=catalog['evidence'];d['scope']['source_count']=len(d['evidence'])
 (O/'technology_directory.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),'utf-8')
 rows=[]
 for c in directory:
  for tid in c['topic_ids']:
   t=byid[tid];rows.append(dict(domain_id=t['domain_id'],topic_id=tid,topic=t['title'],**{k:v for k,v in c.items() if k not in ['topic_ids','domain_ids']},source_locators='\n'.join(i+': '+ev[i]['locator'] for i in c['evidence_ids'])))
 with (O/'technology_directory.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
 return d

if __name__=='__main__':
 p=O/'report.json';d=enrich(json.loads(p.read_text('utf-8')));p.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
 print(json.dumps(d['catalog']['scope'],ensure_ascii=False))

