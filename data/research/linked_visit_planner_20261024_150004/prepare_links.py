from pathlib import Path
import json,csv,re,hashlib
D=Path(__file__).parent;R=D.parents[2]
data=json.loads((R/'data/research/photo_visit_planner_20261024_074920/transcription.json').read_text(encoding='utf8'))
catalog=list(csv.DictReader((R/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig')))
def norm(s):return re.sub(r'（.*?）|\(.*?\)|株式会社|有限会社|[\s.,・]','',s).lower()
links=[]
for key,sheet in [('ai','AI・フィジカルAI'),('automation','自動化・自律化50社')]:
 for i,x in enumerate(data[key],2):
  name,booth=x['values'][:2]
  if x['id']=='P32':name='株式会社ナベル';x['values'][0]=name
  found=[y for y in catalog if norm(y['company_name'])==norm(name)]
  exact=[y for y in found if y['booth']==booth];found=exact or found
  assert len(found)==1,(name,booth,len(found))
  links.append(dict(id=x['id'],sheet=sheet,cell=f'A{i}',text=name,url=found[0]['detail_url'],kind='JIMTOF公式出展者ページ',match_company=found[0]['company_name'],match_booth=found[0]['booth'],locator='企業名／小間番号／主な出展物'))
tech={
'P01':('https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260911.html','図面読取／溶接条件・動作生成'),
'P02':('https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260930.html','日立との戦略的パートナーシップ／実証計画'),
'P03':('https://ndotlight.com/newsroom/ndotlight-proposes-a-new-3d-data-standard-for-the-physical-ai-era-with-trinix','TRINIX／SimReady'),
'P04':('https://www.itcmt.co.jp/news/exhibition/','JIMTOF2026／HATS／Fuzzy Studio／加工監視'),
'P05':('https://smd.co.jp/news/jimtof2026/','HS4200／自動化ソリューション'),
'P06':('https://smd.co.jp/lineup/shimada_automation_module/','SHIMADA AUTOMATION MODULE'),
'P07':('https://www.sofix.co.jp/products/sofixcan_fleeter/','SOFIXCAN Fleeter／工場自律化'),
'P08':('https://www.sofix.co.jp/products/sofixcan_ai_forecast/','SOFIXCAN AI Forecast'),
'P09':('https://www.mamezou.com/news/press-release/20250805','関連研究：自然言語によるティーチング。今回展示を証明するリンクではない'),
'P11':('https://infosys.beckhoff.com/content/1033/tcinfosys3/7666870155.html','TwinCAT CNC／外部補正・HLI・リアルタイム機能'),
'P12':('https://www.beckhoff.com/en-en/products/automation/twincat/texxxx-twincat-3-engineering/te1700.html','TwinCAT CoAgent for Engineering'),
'P13':('https://www.nidec.com/jp/products/machine-tools/contents/machine-tool-jimtof2026/','TAKISAWA／TR-20W／参考出品'),
'P14':('https://www.dmgmori.co.jp/corporate/news/2026/20261019_serviceagent.html','my DMG MORI サービスエージェント'),
'P15':('https://www.dmgmori.co.jp/corporate/news/2026/20260706_conditionagent.html','Condition Agent'),
'P16':('https://www.dmgmori.co.jp/corporate/news/2026/20260706_geniac.html','GENIAC／製造フィジカルAI構想'),
'P17':('https://prtimes.jp/main/html/rd/p/000000031.000057137.html','匠技研工業自社発表／見積AIエージェント'),
'P18':('https://takumi-force.jp/','匠フォース／図面検索・見積の製品説明'),
'P19':('https://www.mitsubishielectric.co.jp/ja/pr/2026/1021_rd/','ヒューマノイドとCNC工作機械の連携／AI加工タスクプランナー'),
'P23':('https://www.okuma.co.jp/smart-factory/osp-suite/osp-ai.php','OSP-AI／機械診断・加工診断'),
'P24':('https://www.okuma.co.jp/english/product/it-products/osp-p500.php','OSP-P500／デジタルツイン・操作支援'),
'P25':('https://mori-machinery.com/wp-content/uploads/2023/06/%E7%86%9F%E7%B7%B4%E8%80%85%E3%81%AE%E7%B5%8C%E9%A8%93%E7%9F%A5%E3%82%92%E3%82%82%E3%81%A8%E3%81%AB%E5%88%87%E5%89%8A%E5%B7%A5%E5%85%B7%E3%81%AE%E6%AC%A0%E3%81%91%E3%83%BB%E6%91%A9%E8%80%97%E3%83%BB%E5%AF%BF%E5%91%BD%E3%82%92%E6%8E%A8%E5%AE%9A%E3%81%99%E3%82%8BAI%E3%82%92%E9%96%8B%E7%99%BA.pdf','メーカーのAI工具摩耗・欠損推定技術資料。写真の製品名表記は保持'),
'P27':('https://check.hacarus.com/ja/aisoftware/','HACARUS Check／AI検査ソフトウェア'),
'P28':('https://optical.kowa-opt.co.jp/camera-rw/','Rotary Wiper／刃先欠損・切粉巻付き・AI異常検知'),
'P29':('https://nexus.hexagon.com/documentationcenter/en-US/bundle/espritedge-2025.4-onlinehelp/page/concepts/ProPlanAI.html','ProPlanAI公式技術マニュアル／学習データ・特徴・工程計画'),
'P30':('https://nexus.hexagon.com/home/product/odyssee/','ODYSSEE／機械学習・縮約モデル・予測'),
'P31':('https://nexus.hexagon.com/home/product/nexus-materials-enrich/','Nexus Materials Enrich／物理モデル・機械学習・FAQ'),
'P32':('https://www.bellows.co.jp/products/tm-robot','ナベル／TM AI Cobot'),
}
overrides={('P32','F'):('https://www.tm-robot.com/ja/product/ai-vision','Techman AI Vision／認識とロボット連携'),('P32','G'):('https://www.tm-robot.com/ja/product/ai-vision','Techman AI Vision／学習・位置決め')}
for i,x in enumerate(data['ai'],2):
 company_link=next(y for y in links if y['id']==x['id'])
 for col in ['D','F','G']:
  url,locator=overrides.get((x['id'],col),tech.get(x['id'],(company_link['url'],'主な出展物・技術説明。個別の追加製品資料は今回確定できず')))
  links.append(dict(id=x['id'],sheet='AI・フィジカルAI',cell=f'{col}{i}',text=x['values'][ord(col)-65],url=url,kind='技術詳細' if url!=company_link['url'] else '公式出展説明',locator=locator))
obj=dict(source_workbook='outputs/photo_visit_planner_20261024_074920/JIMTOF2026_ユーザー選定_調査企業一覧.xlsx',headers=data['headers'],ai=data['ai'],automation=data['automation'],links=links,changes=[dict(sheet='AI・フィジカルAI',cell='A33',before='株式会社ベル',after='株式会社ナベル',reason='前回の写真転記誤読。写真10とW2041公式出展者を照合。')],policy='7列・2シート・行順・コメントを維持。通常のセルリンクは1セル1件。未確認の質問をリンク先が回答済みとは意味しない。展示未確認の注記を保持。')
(D/'link_plan.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
assert len(links)==178
with (D/'link_index.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','sheet','cell','text','url','kind','locator'],extrasaction='ignore');w.writeheader();w.writerows(links)
source=R/obj['source_workbook'];(D/'_private/source_sha256.txt').write_text(hashlib.sha256(source.read_bytes()).hexdigest())
print(json.dumps({'company_links':82,'technical_cell_links':96,'unique_urls':len(set(x['url'] for x in links))}))
