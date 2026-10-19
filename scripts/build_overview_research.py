"""Materialize the source-linked cross-company analysis for the one-slide v0."""
import csv,html,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/research/overview_v0'
def load(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def save(stem,rows):
 (OUT/(stem+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 keys=list(dict.fromkeys(k for row in rows for k in row))
 with (OUT/(stem+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()} for row in rows)
dossiers=load('review_dossiers.json');annotations=load('review_annotations.json');coverage=load('coverage.json')
assert len(dossiers)==len(annotations)==42
evidence=[];reviews=[]
for d,a in zip(dossiers,annotations):
 assert d['review_id']==a[0]
 ids={}
 for year,records in d['years'].items():
  ids[year]=[]
  for n,r in enumerate(records,1):
   eid=f"EOV-{d['review_id']}-{year}-{n}";ids[year].append(eid)
   evidence.append(dict(evidence_id=eid,publisher=r['company_name'],year=int(year),title=f"JIMTOF{year}公式カタログ：{r['company_name']} ({r['booth']})",url=r['detail_url'],locator='main > div.col-md-8.mb-5 の出展紹介、見出し「主な出展物」直後',checked_date='2026-10-16',published_date='未記載',evidence_type='公式掲載の出展者記述（メーカー主張）',exhibition_certainty='2026展示予定・現地未確認' if year=='2026' else '2024当時の出展説明・実演実施の事後確認ではない',source_record_id=r['exhibitor_record_id'],cache_path=r['cache_path'],source_excerpt=(r['exhibition_introduction']+'\n'+r['main_exhibits'])[:180]))
 reviews.append(dict(review_id=a[0],company=d['selection'],domain=a[1],customer_need=a[2],technical_mechanism=a[3],observed_2024_2026_difference=a[4],limitations=a[5],comparison_status='両年の出展説明を比較（性能・実装実績は未比較）' if ids.get('2024') else '2024詳細不足のため年度差分は比較不能。新規出展・進化なしとは判定しない',evidence_2024=ids.get('2024',[]),evidence_2026=ids.get('2026',[]),urls_2024=[r['detail_url'] for r in d['years']['2024']],urls_2026=[r['detail_url'] for r in d['years']['2026']],booths_2026=[r['booth'] for r in d['years']['2026']],review_basis='Codexが両年の説明文を読み、顧客課題・方式・差分を意味内容で比較。候補抽出の語数を結論に使っていない'))
web=[
 ('W01','Beckhoff','TwinCAT 3 Machine Learning Creator','https://www.beckhoff.com/en-za/products/automation/twincat/texxxx-twincat-3-engineering/te3850.html','製品説明冒頭、Product status','データからAIモデルを自動構築し精度・遅延を最適化。ONNXとPLCopen XMLのパイプラインを出力する。','公開日未記載','既存製品の方式確認。2026展示はEOV-V005-2026-1で別確認'),
 ('W02','Hexagon','ESPRIT EDGE Release Highlights','https://hexagon.com/products/esprit-edge/release-highlights','2025.2 PROPLANAI、2026.1 ProPlanAI for Turning, Mill-Turn & Swiss','過去の加工ジョブから特徴と工程を予測。2025.2の導入説明、2026.1の旋削・複合・スイス型向け商用提供説明を確認。','リリース番号で特定、日付未記載','メーカーの提供状況。対象機種や契約、顧客実績は未確認'),
 ('W03','レニショー','Renishaw Central データプラットフォーム','https://www.renishaw.com/jp/smart-manufacturing-data-platform-for-industrial-process-control--47853','メカニズム、現場でのクローズドループ、導入効果','計測・状態・アラームを集約し、IPCで工作機械の変数や工具オフセットを更新。自社工場の導入事例を掲載。','公開日未記載','2024にも展示掲載済み。既存方式の実装例であり2026新規とはしない'),
 ('W04','中村留精密工業','RoboSync','https://www.nakamura-tome.co.jp/products/automation/robosync/','製品の特長 > 簡単復旧、簡単操作','ビジョンとマーカで機械・ロボット・ストッカー間を位置決め。移動後にマーカを読み復旧する方式。','公開日未記載','自律的な未知例外復帰の証明ではない'),
 ('W05','パナソニック プロダクションエンジニアリング','X-Area','https://www.panasonic.com/jp/company/ppe/products/x-area.html','サービス概要、システム構成','複数ロボット・設備の遠隔監視・操作を一元化し、人がエラー対応する。異なるメーカーとの連携を説明。','公開日未記載','人の介入を含む運用方式。無人運用・同時台数の保証ではない'),
 ('W06','HACARUS','AI外観検査ソリューション HACARUS Check','https://hacarus.com/ja/technology/hacarus-check-series/','2026.04.06本文','良品学習による立上げ、異常箇所の可視化、撮像ハード構成を説明。','2026-04-06','メーカー製品説明。独立評価の精度ではない'),
 ('W07','DMG森精機','Condition Agent 提供開始','https://www.dmgmori.co.jp/corporate/news/2026/20260706_conditionagent.html','2026/07/06プレスリリース > 診断専用NCプログラム、標準搭載、既設機キット','診断用NC動作のデータをクラウド解析。主軸・送り軸・ATC・APCを診断し、対象既設機へのキット導入を説明。','2026-07-06','公式検索取得本文で確認。直接ページ取得はタイムアウト。個別JIMTOF展示と同一とは未確認'),
 ('W08','モリマシナリー','工具の欠け・摩耗・寿命を推定するAI研究発表','https://mori-machinery.com/wp-content/uploads/2023/06/%E7%86%9F%E7%B7%B4%E8%80%85%E3%81%AE%E7%B5%8C%E9%A8%93%E7%9F%A5%E3%82%92%E3%82%82%E3%81%A8%E3%81%AB%E5%88%87%E5%89%8A%E5%B7%A5%E5%85%B7%E3%81%AE%E6%AC%A0%E3%81%91%E3%83%BB%E6%91%A9%E8%80%97%E3%83%BB%E5%AF%BF%E5%91%BD%E3%82%92%E6%8E%A8%E5%AE%9A%E3%81%99%E3%82%8BAI%E3%82%92%E9%96%8B%E7%99%BA.pdf','2023年6月2日、成果と今後の展望','工具寿命の推定は2023年の研究発表にも存在。2026の展示記述だけで手法の初発明年とは判定しない。','2023-06-02','公式検索の該当箇所で確認。研究段階の数値を商用性能に転用していない'),
 ('W09','パナソニックHD','工場敷地内でのX-Area Remote実証','https://tech.panasonic.com/jp/td/news/20221124.html','2022/11/24 NEWS & TOPICS','2022年に自律運転けん引車へ遠隔管制を搭載した工場実証を発表。','2022-11-24','2024出展比較はできないが、2026に初めて遠隔管制が生まれたという解釈を否定する根拠')
]
for id,pub,title,url,loc,summary,date,limit in web:
 evidence.append(dict(evidence_id='EOV-'+id,publisher=pub,year=0,title=title,url=url,locator=loc,checked_date='2026-10-16',published_date=date,evidence_type='企業公式資料・メーカー主張',exhibition_certainty=limit,source_record_id='',cache_path='',retrieval_note='公式ウェブの該当箇所を確認し、本台帳に要点を保存。ページ全文のローカルキャッシュは作成していない。',source_excerpt=summary))
def refs(*numbers,years=(2024,2026)):
 return [e['evidence_id'] for e in evidence if any(e['evidence_id'].startswith(f'EOV-V{n:03}-{y}-') for n in numbers for y in years)]
claim_specs=[
 ('C01','メーカー説明の横断整理','加工準備の技能依存に対して、加工履歴・知識によるAI支援とデジタルツイン検証を組み合わせる提案が見られる。',refs(2,6,7,8,9,10,39)+['EOV-W01','EOV-W02'],'全社の採用率や共通効果は測定していない'),
 ('C02','メーカー説明の横断整理','多品種・狭い現場の段取りには、機構・ビジョン位置合わせ・交換機構・搬送を組み合わせた柔軟な加工セルが提案されている。',refs(1,3,25,26,27,28,29,31,35)+['EOV-W04'],'AIを使わない機械的方式も含む。段取り時間と適用条件は現地確認'),
 ('C03','メーカー説明と既存製品方式','品質ばらつきや停止に対し、機上計測・工具画像・制御信号を補正、工具交換、保全判断へつなぐ方式がある。',refs(5,17,18,19,20,21,23,24,32,33,34,36,42)+['EOV-W01','EOV-W03','EOV-W06','EOV-W07'],'計測補正・工具寿命予測・良否判定は別機能。全てがAIでも閉ループでもない'),
 ('C04','メーカー説明の横断整理','現場情報の分断には共通情報モデル・MES・データ基盤、運用例外には遠隔支援が提案されている。',refs(11,12,13,14,15,16,38,40,41)+['EOV-W05'],'共通データ基盤だけで自律的な工場最適化は成立しない'),
 ('C05','2024一次資料の確認','AI判定、自動CAM、機上計測、ロボット段取り、データ連携は2024の出展説明に既に存在する。',refs(2,3,6,8,9,10,11,12,15,17,18,19,24,25,32,35,36,39,40,years=(2024,)),'2026からの一律のAI化や自動化開始とは説明しない'),
 ('C06','両年の記載差分と公式製品資料','2026の追加・具体化として、CAM／制御設計のAI支援、工具寿命・交換提案、工程・運用の接続が確認できる。',refs(1,2,6,8,11,15,23,24,30,31,34,40)+['EOV-W02','EOV-W08'],'出展記述の差と、方式の初発明・効果実証は区別。寿命推定研究は以前にも存在'),
 ('C07','反証・比較限界','継続する方式・製品が多く、全社一律の進化、性能向上、完全自律はこの比較から立証できない。',refs(3,4,9,12,18,19,20,25,32,35,36,39,40)+['EOV-W08','EOV-W09'],'新製品・初公開の語だけでは機能差を認定しない。説明不足は比較不能'),
 ('C08','業界方向の予測・仮説','今後の研究重点は、個別工程の自動化に加え、準備・品質・運用をつなぐ限定範囲の自律化へ広がると予測する。',refs(1,2,5,7,11,15,16,17,24,29,30,34)+['EOV-W03','EOV-W05'],'重点42社からの分析仮説。業界全体の実装成熟度や市場比率を示すものではない'),
 ('C09','研究提案・仮説','加工履歴と設備制約で候補を生成し、NC・治具・干渉を検証して人が承認する加工準備AIを研究する。',refs(2,6,7,8,9,39)+['EOV-W02'],'市販機能の単純な再現を避け、未学習品種での制約充足と検証を研究差分にする'),
 ('C10','研究提案・仮説','機上計測と刃先画像の信頼度を評価し、補正・工具交換・停止を選ぶ品質制御を研究する。',refs(18,19,20,21,23,24,34,36,42)+['EOV-W03','EOV-W06'],'補正量の上限と計測不確かさを扱い、無制限な自動補正は行わない'),
 ('C11','研究提案・仮説','異機種セルの状態と作業前提を共通化し、例外復帰と再計画を行い、難例を人へ引き継ぐ方式を研究する。',refs(11,12,14,15,16,25,26,29,30,35)+['EOV-W04','EOV-W05'],'AIロボット単体の汎化性能だけで、工場全体の自律化を約束しない')
]
claims=[dict(claim_id=i,classification=k,claim=t,evidence_ids=es,limitations=l) for i,k,t,es,l in claim_specs]
themes=[
 dict(theme_id='R1',claim_id='C09',name='検証付き加工準備AI',customer_need='多品種の工程・治具・NC準備工数と技能依存',technical_method='加工履歴と図面／形状から工程候補を提案し、設備・工具・治具制約を照合。実行NCのシミュレーションと人の承認を必須化',research_difference='生成速度より、未学習品種での制約充足・誤り検出・修正履歴の再利用を対象にする',comparison_baseline='従来CAMテンプレート／ルールDB、熟練者による手作業準備',experiment='類似形状と未学習形状、工具・設備変更を含む部品群で準備と初品までを比較',metrics='準備時間、初品良品率、検証で捕捉した誤り、人の修正回数、対応できない入力の棄却率',barriers='履歴品質・暗黙制約・機種差・検証モデルの鮮度・誤った提案の実機流出',industry_relevance='工程集約ほど準備の知識負荷が増える。工作機械・CAM・治具・制御設計をまたぐ共通課題',market_and_adoption='市場規模未算定。類似製品と商用提供説明はあるが本提案の採用実績ではない',field_gate='対応加工と契約条件、未学習形状の失敗例、NC検証範囲、導入顧客の初品までの実測を確認',status='研究提案・要現地確認'),
 dict(theme_id='R2',claim_id='C10',name='計測信頼度を考慮した品質制御',customer_need='品質ばらつき、不良、過早工具交換、無人加工中の停止',technical_method='機上寸法・形状、刃先画像、制御時系列を関連付け、計測不確かさと工程状態を推定。補正上限内の調整、工具交換、停止を選択',research_difference='検出の正答率だけでなく、センサ汚れ・温度・工具差を含む誤補正と見逃しの影響を最小化',comparison_baseline='固定寿命交換、固定閾値監視、従来の計測オフセット補正',experiment='材質・工具ロット・熱状態・撮像汚れを変え、加工品質と交換判断を比較',metrics='不良率、工具費／良品、誤補正率、見逃し率、計測時間、良品数／人時',barriers='計測と加工の相関、センサ校正、ドリフト、遅延、補正限界、学習データ不足',industry_relevance='加工機、計測機、工具、外観AIの分断を結ぶ。既設機への適用を重視',market_and_adoption='市場規模未算定。既存閉ループの自社工場事例はあるが、複合センサ方式の一般化実績ではない',field_gate='校正・計測誤差・閾値設計、対応工具と品種、誤補正事例、交換判断の責任分担を確認',status='研究提案・要現地確認'),
 dict(theme_id='R3',claim_id='C11',name='異機種セルの例外復帰・再計画',customer_need='段取り変更、切粉・把持・搬送エラーで停止する少人数運用',technical_method='設備・工具・品種・作業の共通状態モデルと前後条件を作成。復帰可能な手順を制約探索し、残作業を再計画。未知状態は停止し人へ遠隔引継ぎ',research_difference='認識・ロボット操作単体に留めず、異機種間の状態整合と再開許可、保守・計画への接続を研究',comparison_baseline='固定シーケンスと現場駆け付け、単独AMR／ロボットの手動復帰',experiment='品種切替、位置ずれ、切粉絡まり、工具交換、搬送滞留を注入し復帰と再計画を比較',metrics='復帰時間、現場介入回数、計画達成率、誤再開率、統合・再設定工数',barriers='機種別インターロック、観測できない状態、通信と権限、責任境界、未知例外',industry_relevance='セル、治具、搬送、MES、保全をまたぐ運用負荷を抑える。固定自動化で十分な工程は対象外',market_and_adoption='市場規模未算定。遠隔支援・位置復旧・参考展示を、完全自律の採用実績と混同しない',field_gate='切粉除去参考機の失敗条件、ロボット移動後の再教示、同時遠隔監視台数と介入率、受注とPoCを確認',status='研究提案・要現地確認')
]
item_specs=[
 ('V001','AIエージェントの工作機械実装','準備・運用支援','2026展示予定。具体権限・方式は未確認'),
 ('V001','AMR 1000／MATRIS WPH 210','搬送対象と多品種ハンドリング','2026展示予定。AMR方式自体は2024にも存在'),
 ('V002','フィジカルAI CNC','知的作業の自動化','2026展示予定。モデル・許可動作は未確認'),
 ('V002','生成AIロボット駆動・オープンプラットフォーム','教示負荷と柔軟な開発','2026展示予定。商用範囲と実績未確認'),
 ('V005','TwinCAT MLC','データからモデル構築、ONNX／PLCパイプライン','既存製品方式はW01。2026カタログにも掲載'),
 ('V005','TwinCAT CoAgent','PLC・HMI開発、アラーム対応の対話支援','2026展示予定。自動実行権限は未確認'),
 ('V007','ProPlanAI／Esprit Edge','過去ジョブから工程提案とツイン検証','2026展示予定、W02は製品提供範囲を補足'),
 ('V007','MAESTRO／PRESTO／品質プラットフォーム','測定・検査・解析・品質データ連携','2026展示予定。閉ループ適用範囲は未確認'),
 ('V008','CAMAssist','CAMプログラミング支援','2026本文に追加記載。2024の不在証明ではない'),
 ('V006','Eplan Copilot','設計知識・操作支援','2026展示予定。自律回路確定とは記載されていない'),
 ('V018','Renishaw Central＋IPC','計測結果から変数・工具オフセット更新','既存製品方式をW03で確認。Centralは両年掲載'),
 ('V019','FormControl X／DIGILOG','機上形状・工具計測と補正','既存方式継続。LC54・GrindingControlは2026追加記載'),
 ('V021','HACARUS Check ZERO','良品学習と運用中の追加調整','2026展示予定。照明・品種変化への頑健性は未確認'),
 ('V023','VT122＋VTC6.0','画像によるAI摩耗診断','2026本文でAI機能明記。VT122本体は2024にも掲載'),
 ('V024','ツールコラージュ／アナライザー','撮像・摩耗量学習・寿命と交換提案','2026展示予定。AI判定は2024にも存在'),
 ('V024','ツールソムリエ','工具情報・収納・入出庫連携','2026は説明動画・資料。実機を展示すると書かない'),
 ('V034','HGM-DX','自動測定値を研削へフィードバック','2026展示予定。数値改善の独立検証なし'),
 ('V029','RoboSync','ビジョン・マーカによる移動後位置復旧','2026展示予定。W04で方式確認'),
 ('V030','TR-20W切粉除去','フィジカルAIによる切粉の判断・除去','参考出品。量産標準機能とはしない'),
 ('V016','X-Area Remote','複数設備の遠隔監視・例外操作','2026展示予定。W05で人の介入を含む構成確認'),
 ('V011','OPC UA情報モデル＋エージェント連携','機器データの意味統一と上位連携','情報モデルは2024既存。2026は連携シナリオ追加'),
 ('V012','Facteye／Resolana','旧機・設備・品質データの収集集約','2026展示予定。2024にも収集・AI活用基盤'),
 ('V013','Smart Craft MES','生産・品質・在庫・ERP連携','2026展示予定。2024詳細不足'),
 ('V014','MonoRevo','工程設計・計画変更・進捗とAI補助','2026展示予定。2024詳細不足'),
 ('V015','Fleeter／AI Forecast／ΩEye','搬送・予兆と旧機観測の組合せ','2026ミニ工場デモ。商用自律工場の証明ではない'),
 ('V025','ナットランナー治具／メカ式指交換','追加配管配線を減らす段取り自動化','2026展示予定。類似のロボット治具は2024にも掲載'),
 ('V026','マテハンホルダ／BoostMaster','主軸の既存動力・圧力を使う搬送・切粉処理','2026展示予定。AI以外の低負荷方式として比較'),
 ('V036','M3MH','既設機の機上計測と測定計画','両年掲載。2026新規方式とはしない'),
 ('V038','ミロクルカルテAIオプション','保全記録・点検入力・分析支援','2026展示予定。メータ読取はα版'),
 ('V039','BreylSimulator／InforLoom','ルールDBによる治具計画・データ連携','2024にも掲載。AI・XRは2026追加紹介'),
 ('V040','TECHSと購買API・スマホ実績','調達と現場入力の業務連携','2026本文に提供日・追加機能を記載。AI採用件数とは別'),
 ('V041','匠フォース','見積・設計・調達を人の承認付きで支援','2026出展者説明。方式・実績は未確認'),
 ('V042','RW耐環境ビジョン＋AI解析','撮像の安定化を前提とする異常監視','2026展示予定。定量検出性能は未確認')
]
items=[]
for n,(v,name,method,certainty) in enumerate(item_specs,1):
 r=next(x for x in reviews if x['review_id']==v)
 items.append(dict(item_id=f'TOV{n:03}',company=r['company'],item=name,customer_need=r['customer_need'],mechanism=method,certainty=certainty,difference_2024=r['observed_2024_2026_difference'],limitations=r['limitations'],evidence_ids=r['evidence_2026']+r['evidence_2024']))
questions=[]
for t in themes:
 questions.append(dict(theme_id=t['theme_id'],theme=t['name'],technical_questions=t['field_gate'],common_questions='顧客の困りごとと開発理由、方式選択理由、適用範囲・制約、2024との差、今後の方向性。市場規模は対象工程数・顧客数・算定根拠を確認。受注・採用・PoC・引き合いは実績と見通しを分ける',acceptance_metrics=t['metrics'],adoption_status='現地未確認',market_size='未算定。裏付けのない金額を提言根拠にしない'))
visit_specs=[
 ('V001','R1/R3','AIエージェントが読める情報・実行できる操作と承認境界は何か。AMR運用の介入率はどれだけか'),
 ('V002','R1/R3','フィジカルAI CNCと生成AIロボットの具体タスク、停止条件、2024比の手作業削減を実演で確認したい'),
 ('V005','R1/R2/R3','モデルの精度・最大遅延・異常時の扱い、CNCへの書込権限、CoAgent出力の検証方法は何か'),
 ('V007','R1/R2','ProPlanAIの履歴必要量・対象加工・未知形状での失敗とNC検証範囲は何か。品質データはどこへ返るか'),
 ('V011','R3','OPC UA情報モデルで機種差を吸収できる範囲と、エージェントの読取・書込・認可をどう区別するか'),
 ('V015','R3','ミニ工場で扱える例外は何か。旧機観測から搬送・再計画へ接続する開発工数と実顧客実績はあるか'),
 ('V016','R3','一人当たり監視台数と介入頻度、通信断時の停止、現場復旧が必要になる例外は何か'),
 ('V018','R2','IPC補正の対象機と補正上限、計測不確かさ、誤補正防止、他社機接続工数を教えてほしい'),
 ('V021','R2','良品必要数、照明・材質・品種変更時の再学習、見逃し／過検出の評価母集団とチューニング方法は何か'),
 ('V024','R2','摩耗量から寿命への対応と予測区間、工具・材質差への適応、2024比の増分は何か。実機／動画の範囲も確認したい'),
 ('V029','R3','マーカ位置復旧の必要精度・再教示時間、機種差・把持失敗への対応、未知状態では誰が再開許可するか'),
 ('V030','R3','参考出品の切粉除去で扱える材質・絡み方、成功率、失敗時停止、商品化と受注の状況は何か'),
 ('V034','R2','測定誤差・温度変化・遅延をどう補正量へ反映するか。誤補正と無人運転時間の実測はあるか')
]
visits=[]
for v,t,q in visit_specs:
 r=next(x for x in reviews if x['review_id']==v)
 visits.append(dict(company=r['company'],booths=r['booths_2026'],research_themes=t,priority='暫定重点・事前レビューで訪問確定',why=r['customer_need'],technical_questions=q,common_questions=questions[0]['common_questions'],evidence_ids=r['evidence_2026'],source_urls=r['urls_2026'],status='未訪問・未聴取'))
save('visit_priority',visits)
for stem,rows in [('company_comparison',reviews),('evidence_ledger',evidence),('claims',claims),('research_themes',themes),('technology_items',items),('field_questions',questions),('slide_mapping',[dict(slide=1,claim_id=c['claim_id'],evidence_ids=c['evidence_ids']) for c in claims])]:save(stem,rows)
eids={e['evidence_id'] for e in evidence}
assert all(set(c['evidence_ids'])<=eids and c['evidence_ids'] for c in claims)
coverage['semantic_review']={'selected_company_keys':42,'with_both_year_descriptions':sum(bool(r['evidence_2024']) and bool(r['evidence_2026']) for r in reviews),'technology_items':len(items),'evidence_records':len(evidence),'claim_count':len(claims),'research_themes':len(themes),'limits':'重点42社の意味内容比較。全候補の方式を同じ深さで分析したものではない。社名部分一致による別会社UELは除外済み。法人沿革が必要な名称変更候補は自動で同一視していない。'}
(OUT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
esc=lambda x:html.escape(str(x))
def table(rows,fields):
 return '<table><thead><tr>'+''.join('<th>'+esc(label)+'</th>' for key,label in fields)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc('; '.join(row.get(key,[])) if isinstance(row.get(key),list) else row.get(key,''))+'</td>' for key,label in fields)+'</tr>' for row in rows)+'</tbody></table>'
body='<h1>JIMTOF2026 事前共有v0：根拠と横断比較</h1><p>確認日 2026-10-16。2026はメーカーの展示予定・製品説明に基づく。効果・受注・市場規模の独立検証、現地確認は未実施。</p><p>全掲載2,427行、取得詳細1,808行を対象に一次抽出。2026候補345行／342名称キー、重点42社を内容比較。詳細URLなし619行は未捕捉の可能性があり、候補数を市場比率・採用率に使わない。</p>'
body+='<h2>本編の主張と根拠</h2>'+table(claims,[('claim_id','Claim'),('classification','区分'),('claim','主張'),('evidence_ids','根拠ID'),('limitations','限界')])
body+='<h2>研究提案（仮説）</h2>'+table(themes,[('theme_id','ID'),('name','テーマ'),('customer_need','課題'),('technical_method','技術方式'),('research_difference','研究上の差分'),('metrics','評価'),('barriers','障壁'),('field_gate','現地確認')])
body+='<h2>42社の顧客課題・技術方式・年度差分</h2>'+table(reviews,[('review_id','ID'),('company','企業'),('domain','領域'),('customer_need','顧客課題'),('technical_mechanism','方式'),('observed_2024_2026_difference','2024との比較'),('limitations','限界'),('comparison_status','比較状態'),('evidence_2024','2024根拠'),('evidence_2026','2026根拠')])
body+='<h2>暫定視察優先先と技術固有の質問</h2>'+table(visits,[('company','企業'),('booths','ブース'),('research_themes','テーマ'),('why','確認する課題'),('technical_questions','固有質問'),('common_questions','共通質問')])
body+='<h2>出典台帳</h2>'
for e in evidence:
 body+=f'<details id="{esc(e["evidence_id"])}"><summary>{esc(e["evidence_id"])}　{esc(e["title"])}</summary><p><a href="{esc(e["url"])}">原典を開く</a></p><p>該当箇所：{esc(e["locator"])}／確認日：{esc(e["checked_date"])}</p><p>{esc(e["source_excerpt"])}</p><p>{esc(e["exhibition_certainty"])}</p></details>'
document='<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JIMTOF2026 v0 横断比較と根拠</title><style>body{font:15px/1.65 system-ui,sans-serif;margin:28px;color:#163044}h1{font-size:26px}h2{margin-top:36px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #bac8d2;padding:8px;vertical-align:top;min-width:80px}th{background:#eaf2f4}details{border-bottom:1px solid #ccd6de;padding:10px}summary{cursor:pointer}a{color:#006879}@media print{body{margin:10px}table{font-size:10px}}</style>'+body+'</html>'
(ROOT/'outputs/JIMTOF2026_v0_根拠と横断比較.html').write_text(document,encoding='utf-8')
print(json.dumps(coverage['semantic_review'],ensure_ascii=False,indent=2))
