"""Editorial report data, derived from the existing atlas and bounded official follow-up."""
import csv,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
A=R/'data/research/technology_atlas_v1'
O=R/'data/research/report_v0'; O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text('utf-8'))
cards={c['card_id']:c for c in read(A/'fact_cards.json')}
ev={e['evidence_id']:e for e in read(A/'evidence_ledger.json')}
details={y:read(R/f'data/exhibitor_details_{y}.json') for y in [2024,2026]}
def source(i,title,url,locator,excerpt,pub='未記載'):
 ev[i]=dict(evidence_id=i,publisher='メーカー公式',year='製品説明',title=title,url=url,locator=locator,checked_date='2026-10-18',published_date=pub,evidence_type='公式記載（メーカー主張）。実測・独立評価ではない',exhibition_certainty='技術説明。JIMTOF2026の同機能・版の実演は未確認',cache_path='sources/report_completion_20261018',source_excerpt=excerpt)
source('RPT-S01','オークマ 加工ナビ','https://www.okuma.co.jp/solution_technology/process/','加工ナビ M-i／M-gⅡ','内蔵センサによる振動測定から主軸速度の算出・変更。M-gⅡはマイクを用い提案から人が選ぶ。')
source('RPT-S02','オークマ サーモフレンドリーコンセプト','https://www.okuma.co.jp/thermo-aniv/','サーモフレンドリーコンセプトの説明・沿革','熱を単純化する構造と熱変位制御の組合せ。2001年からの技術。')
source('RPT-S03','Mazak Accuracy / Ai Thermal Shield','https://www.mazak.com/uk-en/technology/accuracy/','Ai Thermal Shield／Smooth Thermal Shield','主軸速度・温度等を考慮した補正。加工後のワーク測定データを学習し熱変位オフセットを最適化するとの説明。')
source('RPT-S04','Vericut Force FAQ','https://archive.vericut.com/force-faq/','Force physics-based optimization','切削物理に基づき切りくず厚さ、力・動力制約を考慮して送りを最適化する説明。')
source('RPT-S05','Production Module v8.2 release','https://thirdwavesys.com/latest-news/production-module-v8-2-release/','工具たわみ・entry/exit feedrate constraints','NCレベルの最適化と工具たわみ、進入・離脱時の送り制約を説明。2019年公表で2026初の方式ではない。','2019-11-06')
def extra(cid,needle,company,item,mech,human,baseline,delta,extras=(),y24needle=None):
 d=next(x for x in details[2026] if needle in x['company_name'])
 ids=[]
 for y,n in [(2026,needle),(2024,y24needle or needle)]:
  z=next((x for x in details[y] if n in x['company_name']),None)
  if not z:continue
  eid='RPT-'+z['exhibitor_record_id']; ids.append(eid)
  ev[eid]=dict(evidence_id=eid,publisher='JIMTOF公式カタログ／出展者記述',year=y,title=z['company_name']+' JIMTOF'+str(y),url=z['detail_url'],locator=z['evidence_locator'],checked_date=z['checked_date'],published_date='未記載',evidence_type=z['evidence_type'],exhibition_certainty='2026は展示予定／現地未確認',cache_path=z['cache_path'],source_excerpt=z['exhibition_introduction']+'\n'+z['main_exhibits'])
 cards[cid]=dict(card_id=cid,company=company,item=item,booths_2026=[d['booth']],mechanism=mech,human_boundary=human,baseline_2024=baseline,observation_2026=d['exhibition_introduction']+'\n'+d['main_exhibits'],delta_type=delta,evidence_ids=ids+list(extras),unresolved='対象機種、制約、実機の性能・人の介入は要確認',product_stage='公式カタログ記載',exhibition_status='2026展示予定')
extra('RPT001','Third Wave','Third Wave Systems Japan','Production Module／AdvantEdge','Production ModuleはNCレベルの切削負荷解析と最適化。AdvantEdgeの刃先FEMとは分ける。','モデル・工具・材料・制約設定と採用判断の運用は未確認。','同名2024詳細なし。Production Moduleの工具たわみ等は2019年公式発表にも記載。','2024展示比較不能・方式は以前から存在',['RPT-S05'])
extra('RPT002','西部商工','西部商工','ACM','主軸負荷を監視し加工中の送りを自動調整。既存NCプログラムを変更せず導入する説明。','設定する負荷限界・許可範囲・停止復帰の担当は未確認。','2024もACMの主軸負荷監視と送りの適応制御を説明。','2024から継続')
extra('RPT003','アズビルTACO','アズビル（TACO共同出展）','U4DM01 NC旋盤予兆検知','NC旋盤の刃具破損検知。既存機への後付けと他加工機への適用を説明。','2024は設定と学習開始操作を記載。2026の検知後処置・停止権限は未確認。','2024アズビルはU4D NC旋盤パッケージを参考出展。独自アルゴリズム・後付け・設定学習を記載。','参考出展からComing soon表記・性能差未確認',y24needle='アズビル株式会社')
extra('RPT004','神崎高級','神崎高級工機','FD100 ギヤチェッカー','加工前の歯車状態確認と自動歯合わせ。計測情報を使う条件最適化は開発中。','最適化の方式・人の承認・自動反映範囲は未公表。','2024はFX260/GX150とミネラルキャストによる熱安定・振動減衰を説明。','機種・段取り機能の具体化／最適化は開発中')
extra('RPT005','東京貿易','東京貿易テクノシステム','RBY Series 双腕移動ヒューマノイド','双腕移動ヒューマノイドのテレオペレーションと作業教示を参考出展。','テレオペレーション・教示に人が関与。自律の対象タスクは未確認。','2024同名展示との個別差は未照合。','2024個別比較未完了')
# Theme case rows: each short claim is an editorial paraphrase of the cited record.
topics=[]
def topic(i,domain,title,problem,insight,rows):
 out=[]
 for cid,mechanism,human,change,ai in rows:
  c=cards[cid];out.append(dict(case_id=f'{i}-{len(out)+1}',card_id=cid,company=c['company'],item=c['item'],booth=' / '.join(c['booths_2026']),official_mechanism=mechanism,human_boundary=human,year_change=change,ai_status=ai,evidence_ids=c['evidence_ids'],full_record=c,statement_type='公式記載の要約。AI区分は明示／未確認を表示。人の役割の推定は分析と明記。'))
 topics.append(dict(topic_id=i,domain=domain,title=title,problem=problem,insight=insight,cases=out))
topic('B01','D1','図面検索・見積作成','過去図面と原価を探し、案件ごとに見積を組み立てる負担。','OCR・検索・原価計算・承認は別の仕事。見積額の根拠と確定者を追う。',[
 ('AC195','図面のOCR登録と関連文書管理。顧客事例では読取り結果を人が修正。','登録・読取り確認は人。図面の誤関連や改訂の検出は未確認。','2024の同名詳細なし。2026初登場とは断定しない。','AI/OCRを明記'),
 ('FC062','図面認識・類似案件参照・原価計算から見積書案を作る。','担当者が根拠を確認・修正・承認。社外自動送信は未確認。','2024比較不能。2026/7の企業発表で一連の処理を具体化。','AIエージェントを明記'),
 ('FC028','類似図面検索と自動見積を説明。','見積前提の設定・確定者、計算ロジックは未確認。','2024個別比較不能。','AIを明記')])
topic('B02','D1','工程・CAMプログラムの作成','工具・機械・段取り制約を織り込む工程作成の技能依存。','履歴予測と加工戦略の生成を分ける。生成案の採用と実機運転は別工程。',[
 ('FC018','過去ジョブと形状特徴から工程を予測するProPlanAI。','過去データを準備。確認画面はあるが最終NC採用権限は未公表。','2024比較不能。2025の旋削betaから2026の商用範囲拡張を確認。','AI予測を明記'),
 ('FC020','工具・材料・機械等の条件から加工戦略・経路・条件案を生成。','人が前提を設定し、戦略案を確認・調整してCAMへ送る。','Mastercam対応は2024/7に発表済み。2026の出展記述が具体化。','AI CAMを明記'),
 ('AC131','SolidCAM向けに3軸・3+2軸の戦略と経路案を生成。','工具・保持等を設定し、生成案を編集・採用。最終制御権は人。','2024はSolidCAM等。2026はAI支援を追加記載。','AI CAMを明記')])
topic('B03','D2','NC送り最適化・加工中の適応制御','負荷変動による過負荷と、余裕のある区間の加工時間。','加工前にNCを書き換える方式と、加工中に送りを変える方式を比較する。',[
 ('FC022','Forceは切削物理と力・動力制約を使い加工前に送りを最適化。','材料・工具・限界条件とNC採用が必要〈分析〉。運用詳細は未確認。','Forceは2024掲載済み。2026のAI訴求とOptimizerの方式差は未確認。','Forceの物理モデルとAI訴求を分離'),
 ('RPT001','Production ModuleはNCレベルの負荷解析。刃先FEMのAdvantEdgeとは別。','モデル・材料・工具の設定と採用判断が必要〈分析〉。','2024展示比較不能。工具たわみ等は2019年にも公式説明。','学習AIの使用は未確認'),
 ('RPT002','ACMは実測主軸負荷を使い加工中の送りを自動調整。','負荷限界の設定者・停止復帰の手順は未確認。','2024も負荷監視と送り制御を記載。基本方式は継続。','AI/機械学習は未確認')])
cards['FC022']['evidence_ids']+=['RPT-S04']
# Refresh the already created case reference list after supplementary source attachment.
topics[-1]['cases'][0]['evidence_ids']=cards['FC022']['evidence_ids']
topic('B04','D1','PLC・HMI・電気設計の支援','要求から制御コード・画面・設計情報へ落とす手間。','文書回答、コード生成、設定変更、実機書込みを同じ自動化として扱わない。',[
 ('FC011','要求とプロジェクト文脈からPLCコード案を提案。','専門家が確認・確定・実行承認。書込みや起動の個別権限は未確認。','PLCコード支援は2023発表済み。2026初の方式ではない。','生成AI支援を明記'),
 ('FC012','I/O構成とHMI生成・操作を支援するEngineering機能。','専門家のレビュー方針。構成誤りの検証・差戻しは未確認。','I/O・HMI支援は2025/6にも公式説明。','生成AI支援を明記'),
 ('FC017','Eplan Copilotが文脈に応じた回答・推奨・手順を生成。','意思決定は人。設計変更の自動採用は現機能と確認できない。','2024の盤設計・データ連携に対し、2026はCopilotを記載。','AI Copilotを明記')])
# Product-only comparison records retain the exhibitor booth without asserting exhibition of that feature.
for cid,base,item,src in [('RPT006','FC010','Ai Thermal Shield（製品資料による比較）','RPT-S03'),('RPT007','FC009','加工ナビM-i／M-gⅡ（製品資料による比較）','RPT-S01')]:
 cards[cid]={**cards[base], 'card_id':cid,'item':item,'evidence_ids':[src]+cards[base]['evidence_ids'],'mechanism':ev[src]['source_excerpt'],'observation_2026':'製品公式資料による比較例。同機能・版のJIMTOF2026展示搭載は未確認。','human_boundary':'製品資料に示す役割以外の運用・更新採否・権限は未確認。','unresolved':'当該ブースの展示機能と版、2024との直接差分。','product_stage':'製品公式資料あり／展示同一性は未確認','exhibition_status':'出展企業は確認。同機能の展示搭載は未確認','baseline_2024':'製品資料の比較。2024同一機能・版の直接比較は未確認','delta_type':'展示の年度差分未確認'}
cards['FC009']['evidence_ids']+=['RPT-S02']
topic('B05','D2','熱変位補正・びびり抑制','温度変化や振動に伴う精度・面品位のばらつき。','構造設計、実測による適応、学習モデルを分け、補正範囲と外れ条件を見る。',[
 ('FC009','熱を単純化する構造と熱変位制御を組み合わせる。','校正・補正限界・条件変化時の人の関与は未確認。','熱安定化は既存技術。2026のAI訴求だけで補正全体をAIとしない。','熱補正へのAI適用は未確認'),
 ('RPT006','温度・回転等を考慮。加工後測定の学習で熱変位補正を最適化。','測定準備・更新採否・補正限界の設定者は未確認。','製品資料の比較例。同機能の2026展示搭載・年度差は未確認。','学習を明記／展示搭載未確認'),
 ('RPT007','M-iは振動計測から主軸速度を自動変更。M-gⅡは速度候補を提示。','M-iは設定後に自動制御。M-gⅡは人が候補を選ぶ。','既存製品技術の比較例。2024/2026の機能増分は未確認。','自動制御／学習AIは未確認')])
topic('B06','D2','計測から加工へのフィードバック','検査結果を次の加工に戻す待ち時間と補正のばらつき。','計測・推定・補正量決定・実行のどこにAIがあるかを分ける。',[
 ('FC033','Renishaw Central＋IPCで工具オフセットや機械変数を更新。','計測不確かさ、補正上限、異常値の抑止条件は未確認。','Centralは2024掲載済み。2026も継続。','自動補正／AI使用は未確認'),
 ('FC054','HGM-DXは測定値を研削機へ返し加工公差を自動補正。','補正上限と誤計測時の対応は未確認。','2024は製造・検査自動化。2026は測定→研削を具体記載。','自動補正／AI使用は未確認'),
 ('AC085','GH5は機内3D画像で刃先を測り、幅・角度の目標へAI補正。','目標値は人が設定。過研磨・測定不能時の停止復帰は未確認。','2024のGM5等から、2026はGH5の測定・加工一体化を記載。','AI制御を明記／方式非開示')])
topic('B07','D3','外観検査・撮像と追加学習','少量不良データ、撮像ばらつき、見逃しと過検出。','判定モデルの改善と、撮像・搬送・出荷判定の自動化を分ける。',[
 ('FC036','ZEROは良品との差で異常を検出し、人の良否注釈で追加調整。','人が画像・注釈を準備。更新モデル採用と出荷判定の権限は未確認。','追加学習は2025/7発表済み。2026だけの新機能としない。','AI異常検知を明記'),
 ('FC037','協働ロボットで多角度撮像し、AIで傷・欠けを判定。','姿勢教示・再撮像・不良排出の権限は未確認。','日東商事2024の放電加工機展示から、AI検査を追加記載。','AI検査＋ロボット撮像'),
 ('FC034','機上3D測定と工具計測・欠け検知・補正を組み合わせる。','校正・熱状態・機種適合の条件は未確認。','2024のFormControl X等を継続し、2026はLC54等を追加。','計測／AI使用は未確認')])
topic('B08','D3','工具摩耗の判定・交換判断','工具を早く捨てすぎず、欠損や品質悪化を避ける判断。','摩耗の画像診断と、残寿命予測・交換実行は別段階。',[
 ('FC039','刃先の診断箇所を認知し、欠け・摩耗をAI判定・記録。','対象工具と撮像条件を準備。継続使用の最終決定者は未確認。','AI摩耗判定は2024にも説明済み。2026は継続。','AI画像判定を明記'),
 ('FC038','VT122にVTC 6.0のAI摩耗診断・工具長機能を記載。','判定閾値と自動交換への接続は未確認。','2024はVT122検査。2026はAI摩耗診断を追加記載。','AI摩耗診断を明記'),
 ('FC064','2024のMachiningAIDは加工異常・工具摩耗・作業ミスをAI検知。','2026の継承機能と自動停止・交換権限は未確認。','2026はAI省人化の総論。個別機能の進化は比較不能。','2024はAI明記／2026個別不明')])
topic('B09','D3','設備・刃具の異常検知と保全','故障や工具破損の兆候を捉え、点検・交換につなぐ負担。','現在の異常検知、将来時点の予測、保全の決定を切り分ける。',[
 ('AC225','稼働中の電流・振動等を新品状態と比較し劣化・異常を診断。','計測後の点検・交換の最終決定者、誤警報時の扱いは未確認。','プライマリドクタのAI診断は2024から継続。','AI診断を明記'),
 ('RPT003','U4DM01はNC旋盤の刃具破損検知と後付け適用を説明。','2024は設定・学習開始操作あり。停止や交換権限は未確認。','2024参考U4Dから2026 Coming soon表記。性能差は不明。','独自アルゴリズム／AI方式未確認'),
 ('FC052','2024はAI振動診断と遠隔監視を紹介。','2026の個別機能、保全判断への接続は資料不足。','2026の総論だけでは2024比の増分を判定できない。','2024はAI明記／2026個別不明')])
topic('B10','D4','爪・治具・ハンドと位置の段取り','多品種で繰り返す機械的交換と再教示の負担。','センサーレス設定・メカ機構・マーカー補正はAIと別の有効な方式。',[
 ('AC214','Smart Terrace Advは爪等の交換。寸法入力から動作を設定。','人が寸法入力。初期プログラムはメーカーが組込み。','CAPTO等の交換は2024初披露済み。2026はAdv構成等に注目。','自動化／学習AIは未確認'),
 ('FC042','ナットランナーとメカ機構でワークを締結する治具。','人が治具・フック等を設計選定。着座・締結異常の扱いは未確認。','2024も具体治具あり。2026は種類追加を記載。','機械的自動化'),
 ('FC048','RoboSyncは移設後にマーカーを読み相対位置を補正。','人の移設・復旧操作を含む。未知トラブルの自律復帰とは別。','2026は位置復旧を具体説明。同一機能の2024版は未確認。','位置補正／AI使用は未確認')])
topic('B11','D4','ワーク・パレット・切粉の搬送','品種・量の変化に合わせて人の供給往復を減らす。','搬送対象、機内への受渡し、容器交換までを分けて省人範囲を見る。',[
 ('FC002','MATRIS WPH 210がワークとパレット両方を供給。','把持・治具・品種切替の事前準備と異常対応は未確認。','2024のPH Cell等に対しWPH 210を日本初公開と記載。','自動化／AI判断は未確認'),
 ('FC008','ARMROID機内ロボット、OMR20等で工作機械の自動化を構成。','手動との切替と品種変更の介入範囲は未確認。','ARMROID・OMR20は2024にも掲載。2026も継続。','ロボット自動化'),
 ('AC186','AMRで切粉容器を回収。実演と模型を併記。','満杯・こぼれ・ドッキング失敗・容器交換の対応は未確認。','2024のろ過・集中処理から、2026はAMR回収を追加記載。','搬送自動化／AI配車は未確認')])
topic('B12','D4','認識を伴うピック・付帯加工・除去','形状や絡まりが変わる物理作業に固定手順で対応しにくい。','何を見て何を動かすかに加え、完了判定と失敗後の人への引継ぎを比較する。',[
 ('FC049','TAKISAWAは切粉の絡まりを判断し主軸の切粉を除去する参考出品。','許可動作、除去失敗の検出・再試行・人への引継ぎは未確認。','2024 TR-20Wは搬入出。2026は切粉除去を追加記載。','フィジカルAI訴求／参考出品'),
 ('AC051','カメラ・協働ロボット・磁気ピンセットで小径ねじ等をピック。','複数個吸着・空振り等の処理、AI担当の詳細は未公開。','同種構成は2024あり。2026はAIを明記、性能増分は不明。','AIを明記／担当詳細不明'),
 ('AC146','3Dスキャンから不定形ワークを認識し面取り等の軌道を生成。','加工条件設定、干渉確認、誤認識時の停止・品質承認は未公開。','2024同名比較不能。2026の具体タスクは確認。','3D認識・軌道生成／方式詳細不明')])
topic('B13','D5','現場エージェント・遠隔介入','停止や例外発生時、情報を集めて対処を判断する負担。','診断提案・予測・指令・人の遠隔操作を、実行主体別に分ける。',[
 ('FC013','Operationsは機械データと文書から原因仮説・対処案を作る。','専門家が制御権保持。毎回承認・書込権限・失敗復帰は未公開。','2024比較不能。製品発表・投入時期要問合せ。','AIエージェント／提供段階に留意'),
 ('FC030','AI Forecastの予測とFleeterの機器連携をミニ工場で紹介。','予測から指令への権限、通信・搬送失敗時の復帰は未公開。','Fleeterミニ工場は2025にも予告済み。2026初とはしない。','予測と連携を分離／一体自律は未確認'),
 ('FC031','X-Area Remote実証では停止車両を人が遠隔操作して回避。','運行担当者が介入。実証はセーフティドライバー搭乗。','2026/7実証で人の担当を具体確認。2024個別比較不能。','AI支援型との説明／回避操作は人')])
topic('B14','D5','工場データ・計画・資源の連携','現物・工具マスター・進捗が分断し変更に追従しにくい。','データ一元化・ルール自動処理・AI最適化を分け、正本と承認点を確認する。',[
 ('AC295','WinToolは工具情報と工程資源を連携。在庫ルールで購買要求。','管理者承認後ERPへ送信。AIによる自律発注とは記載なし。','工具・CAM・在庫連携は2024から継続。2026は資源の一貫性を強調。','DX＋ルール自動化'),
 ('FC026','Smart Craft MESは記録・指示・履歴を一元管理しAPI連携。','AI分析の内容や判断権限、入力作業の残りは未確認。','2024個別比較不能。','DX／AI判断は未確認'),
 ('FC027','MonoRevoは工程設計・計画・進捗をまとめ自動計画を支援。','計画制約・再計画確定者・例外対応は未確認。','2024個別比較不能。2026は自動スケジューリングを記載。','自動計画／AI方式は未確認')])
topic('B15','D6','AIモデル作成・機器接続の基盤','データの意味づけと、作ったAIを現場へつなぐ負担。','モデルを作れること、機器につながること、実機で任せられることは別条件。',[
 ('FC014','ML Creatorは学習・モデル選択を自動化し、解析とONNX出力を支援。','人がデータ・注釈・目的を準備。実機採用基準は要確認。','データ分割・ONNX統合は2024公式資料にも記載。','AutoMLを明記'),
 ('FC024','OPC UA情報モデルで機器情報をエージェントへ連携する構想。','公開するデータ・メソッド、書込権限、承認と復帰は未確認。','2024は多ベンダー接続。2026はAI連携シナリオを追加。','DX接続基盤／自身のAI判断なし'),
 ('FC025','既設設備のデータ収集・可視化を品質やAI利用へ接続。','自動制御や工場全体最適化の実装は未確認。','収集・対話AIは2024にも説明。2026は連携課題を具体化。','DX基盤＋AI利用')])
topic('B16','D6','デジタルツイン・物理学習用データ','仮想上での確認・学習と実機の結果をつなぐための準備。','加工検証、訓練用ツイン、物理AIの学習用資産は用途を分ける。',[
 ('FC007','Smart Digital Twinで加工前の挙動確認を支援。','モデルと実機の一致や、検証対象外事象の扱いは未確認。','同名ツインは2024から継続。','仮想検証／AIの使用は未確認'),
 ('AC098','Tokn工作機械ツイン、Equator品質保証、ヒューマノイドを別展示。','海外HMND実証とJIMTOFの機体・タスクの同一性は未確認。','Toknの仮想訓練は2024完了の公式事例あり。','加工検証と物理AI実証を分離'),
 ('AC273','TRINIXはCADから形状・物理属性等を生成し検証・自己修正を説明。','実測値と推定値の区別、人の承認、収束しない時の対応は未公開。','2024同名比較不能。DexBenchは共同開発告知で完成済み標準とはしない。','AI生成／実機誤差は未確認')])
topic('B17','D4','展示段階と自律化の境界','人型やAIという名称だけでは任せられる仕事を判断できない。','具体タスク・実行主体・提供段階が揃うまで、将来像と実用機能を分ける。',[
 ('FC005','ファナックは生成AIによるロボット駆動事例を展示予定。','機体・対象タスク・教示・停止・承認の具体範囲は未確認。','2024はAIバラ積み等。2026は生成AI駆動を追加記載。','生成AIを明記／担当範囲未確認'),
 ('RPT005','RBY双腕移動ヒューマノイドはテレオペと作業教示の参考出展。','人が遠隔操作・教示。自律作業の範囲は未確認。','2024の個別差は未照合。','人型機体／自律AIは未確認'),
 ('RPT004','FD100に歯合わせ・前加工計測。計測による条件最適化は開発中。','最適化方式と人の承認、自動反映範囲は未公表。','2024の構造改善等に対し段取りを具体化。開発中を実用済みとしない。','自動化／条件最適化は開発中')])
domains=[
 dict(id='D1',name='工程・制御プログラム生成',tags='AX / AIエージェント / 自動化',topics=['B01','B02','B04'],rows=[
 '〈分析〉図面・加工工程・制御設計の準備をAIが支援。実機運転開始まで一括自動化した証拠は不足。',
 '〈公式要約〉ProPlanAIは履歴から工程予測、CAM Assistは戦略案生成、CoAgentはPLC/I/O/HMI支援。\n〈年度差〉CAM支援は2024以前にも存在。2026は対応工程・設計作業を具体化。',
 '〈分析〉部品・機械・工具・保持の前提と、生成案の確認をつなぐ運用が重要。\n〈未確認〉未知形状・欠品・版変更時の手戻りと、最終採用者の権限。',
 '〈提言・仮説 R1〉既存CAMとNC検証を前提に、段取り変更時の影響確認を研究候補にする。\nVericutの版・オフセット確認は既存。既存機能で埋まる範囲を先に除外する。']),
 dict(id='D2',name='加工品質・能率の安定化',tags='AX / 自律化（限定制御） / 自動化',topics=['B03','B05','B06'],rows=[
 '〈分析〉加工前の予測、加工中の適応制御、計測後の補正は役割が違う。AI以外の有効な方式も並存。',
 '〈公式要約〉Force/Production Moduleは加工前、ACMは負荷→送り、Centralは測定→オフセット。\n〈年度差〉Force・ACM・Centralは2024にも記載。GH5等は計測と補正の構成を具体化。',
 '〈分析〉材料・工具・熱状態が変わった際に、モデルや測定が通用する範囲を把握する。\n〈未確認〉補正上限、誤測定時の抑止、条件変更後の再設定工数。',
 '〈提言・仮説 R2〉熱・工具・測定の変化に対する「補正を続ける／保留する」条件を比較する。\n既存補正の再開発を避け、適用外条件の判定と人への引継ぎに絞る。']),
 dict(id='D3',name='検査・工具・設備状態の判断',tags='AX / DX / 判定自動化',topics=['B07','B08','B09'],rows=[
 '〈分析〉画像・電流・振動を判定へ使う。摩耗診断、将来予測、交換実行は別の到達点。',
 '〈公式要約〉ZEROは良品学習と追加調整、モリはAI摩耗判定、ムラテックは状態のAI診断。\n〈年度差〉摩耗・設備診断は2024にも記載。ZERO追加学習は2025、VTC 6.0は2026に追加記載。',
 '〈分析〉単体の判定精度に加え、撮像・対象切替・再判定・保全決定までの運用を評価する。\n〈未確認〉見逃しと過検出の両立、工具別の限界、更新モデルの採用基準。',
 '〈提言・仮説 R2〉既存検査製品を比較対象に、条件変化時の判定保留と独立評価を検討する。\n追加学習そのものは既存機能。独自方式の必要性は実データ確認後に判断する。']),
 dict(id='D4',name='段取り・搬送・付帯作業の省人化',tags='自動化 / 自律化 / フィジカルAI',topics=['B10','B11','B12','B17'],rows=[
 '〈分析〉交換・供給の定型自動化に、認識を使うピックや切粉除去が加わる。機体の名称だけでは比較しない。',
 '〈公式要約〉MMKは爪等交換、WPH 210はワーク/パレット、TAKISAWAは切粉判断・除去の参考出品。\n〈年度差〉爪交換・磁気ピック・ロボット搬入出は2024にも存在。2026は対象作業・構成を拡張。',
 '〈分析〉導入の焦点は、教示・治具準備の削減と、失敗を検出して止める・引き継ぐ範囲。\n〈未確認〉複数個把持、絡まり残り、容器交換、復帰時間。人型の遠隔教示も別区分。',
 '〈提言・仮説 R3〉切粉除去や不定形ピックの1作業に絞り、完了確認と失敗引継ぎを比較する。\n成功率に加え介入回数・復帰時間・品種変更の準備工数を評価する。']),
 dict(id='D5',name='工場運用・業務の連携と判断支援',tags='DX / AX / AIエージェント',topics=['B13','B14'],rows=[
 '〈分析〉情報連携、計画、対処案、実行許可を分けると、AIが助ける箇所と人の仕事が見える。',
 '〈公式要約〉Operationsは診断案、WinToolは承認後ERP連携、X-Area Remoteは人の遠隔回避。\n〈年度差〉工具・工程情報の連携は2024から継続。2026はエージェント・接続場面を具体化。',
 '〈分析〉例外時にはデータの鮮度・対象設備・実行結果と、指令の権限を揃える必要がある。\n〈未確認〉予測から指令への接続、二重実行、通信断後の復帰と承認。',
 '〈提言・仮説 R4〉API・状態取得・権限が確認できた場合に、限定指令の実行管理を研究する。\nAPI未公開なら着手を保留し、既存ワークフローと遠隔支援の適用を先に検討する。']),
 dict(id='D6',name='AI実装・検証の基盤',tags='DX / AX / デジタルツイン / フィジカルAI基盤',topics=['B15','B16'],rows=[
 '〈分析〉学習、接続、仮想検証の基盤は現場展開を支える。ただし基盤の導入だけでは自律化を示さない。',
 '〈公式要約〉ML Creatorは学習とONNX出力、OPC UAは意味づけ接続、TRINIXは物理属性等の生成。\n〈年度差〉AutoML・ツイン・接続は2024以前にも存在。2026はAI連携・物理学習用途を具体化。',
 '〈分析〉入力データと実機の差が、検証・学習の結果をどこまで変えるかを確認する。\n〈未確認〉推定物理属性の正解、自己修正の収束、JIMTOF実演と海外実証の対応。',
 '〈提言・仮説 R5〉SimReady化の速度だけでなく、実機との誤差評価に未対応範囲があるか確認する。\n既存アセット検証や共同開発中ベンチとの重複を除き、実機データ取得可能なら候補化する。'])]
main=dict(id='MAIN',name='JIMTOF2026　AI・DX・自律化・自動化の事前調査',tags='公開公式資料による事前共有 v0　2026年10月18日',topics=[t['topic_id'] for t in topics],rows=[
 '〈分析〉6分野で整理。準備の生成、加工の補正、検査・診断、物理作業、工場運用、実装基盤に広がる。\nAIが提案する仕事、制約内で自動実行する仕事、人が承認・介入する仕事が組み合わされている。',
 '〈公式要約〉CAM Assistは工程案、ACMは負荷→送り、GH5は測定→補正、TAKISAWAは切粉除去を紹介。\n〈年度差〉最適化・AI摩耗判定・段取り自動化は2024にも存在。2026は対象作業・構成の具体化が目立つ〈分析〉。',
 '〈分析〉比較軸はAIの呼称より、入力→判断→実行→完了確認の範囲と、品種変更・例外時に残る人手。\n〈未確認〉提供段階、適用限界、介入率と採用実績。展示予定・製品資料を商用の無人運転実績と扱わない。',
 '〈提言・仮説〉優先確認は R1 生成後の変更影響、R2 条件変化時の補正・判定保留、R3 物理作業の完了・失敗引継ぎ。\nR4 指令の実行管理、R5 仮想と実機の誤差は条件付き候補。既存機能との重複を除き、現地確認後に着手を判断。'])
research=[
 dict(id='R1',name='生成工程の変更影響と確認の支援',basis=['B02','B03','B04'],hypothesis='工具・保持・機械の変更時、既存検証で覆えない影響の説明と確認が残る可能性。',existing='Vericutは2024に版違い・オフセットのpre-checkを説明。CAMには加工性評価や編集もある。',approach='既存CAM/NC検証の出力と変更情報を対応づけ、未検証範囲を人へ示す。',decision='最初は既存機能の実演を確認。未対応の変更例とデータが得られなければ見送る。',metrics='危険な変更の見逃し、再確認時間、追加の設定工数',priority='現地確認を優先／研究着手は未決定'),
 dict(id='R2',name='条件変化時の補正・判定の保留と引継ぎ',basis=['B05','B06','B07','B08','B09'],hypothesis='工具・熱状態・測定条件が変わるとき、補正を続けてよい条件の整理が課題になる可能性。',existing='熱補正・IPC・良品学習・追加学習は既存。メーカー標準の異常値処理の範囲は未確認。',approach='既存の補正・検査を比較対象に、条件変化の識別と保留・再計測・人への引継ぎを評価。',decision='誤差と異常データが取れ、標準機能の未対応が確認できた場合のみ着手。',metrics='過補正、見逃し/過検出、保留率、再調整時間',priority='現地確認を優先／適用工程を1つに限定'),
 dict(id='R3',name='変動する物理作業の完了確認・失敗引継ぎ',basis=['B10','B11','B12','B17'],hypothesis='把持や切粉除去の成功動作に比べ、完了と失敗を認識し引き継ぐ範囲に差がある可能性。',existing='画像認識・自動交換・位置復旧は既存。参考出品の失敗処理は公開不足。',approach='切粉除去等の1作業で、認識・動作・完了確認と再試行/停止/人の介入を比較する。',decision='許容動作、停止条件、実機・ワークが得られること。既存機能で足りれば研究しない。',metrics='未完了の見逃し、介入回数、復帰時間、品種変更の準備工数',priority='現地確認を優先／汎用ロボット開発には広げない'),
 dict(id='R4',name='限定されたエージェント指令の実行管理',basis=['B13','B14','B15'],hypothesis='提案を指令へ移す時に、設備状態・権限・実行結果の整合が課題になる可能性。',existing='人の承認、ERPワークフロー、OPC UA接続は既存。許可・二重実行防止の範囲は未公開。',approach='1種類の指令で状態確認・承認・結果照合を扱い、通信断後の再送を含め比較。',decision='API、権限モデル、状態取得が確認できるまで保留。',metrics='誤指令、重複実行、未完了の見逃し、承認待ち時間',priority='条件付き候補'),
 dict(id='R5',name='物理学習用データの実機との差の評価',basis=['B16'],hypothesis='生成した形状・摩擦等の属性が実機成功に与える差を、既存検証で覆えない可能性。',existing='TRINIXの物理属性推論・自己修正、NVIDIA検証、DexBench共同開発告知がある。',approach='実測属性と生成属性で同一タスクの結果を比較し、誤差に効く項目を特定。',decision='公開済みベンチ・検証機能の範囲を確認。実機データが取れなければ保留。',metrics='タスク成功の差、属性誤差、修正回数、測定準備時間',priority='条件付き候補')]
allcases=[c for t in topics for c in t['cases']]
used=sorted({i for c in allcases for i in c['evidence_ids']})
ledger=[ev[i] for i in used]
scope=dict(as_of='2026-10-18',listing_rows={'2024':1281,'2026':1146},detail_rows={'2024':988,'2026':820},without_detail_url={'2024':293,'2026':326},candidate_name_keys=342,atlas_cards=334,priority_companies=28,report_topics=len(topics),report_case_rows=len(allcases),report_company_labels=len({c['company'] for c in allcases}),source_count=len(ledger),limits=['全公表出展社総数との突合は未完了。掲載行は企業数と異なる。','詳細URLのない619行は個別内容未取得。候補分類は全社の深掘りを意味しない。','2026は展示予定。製品資料で補った機能の当該ブースでの実演は未確認。','2024同名原典なし・仕様不足は比較不能と明記。未掲載を新規発明や撤退と判定しない。','顧客課題の横断整理は分析。普及率・市場規模・性能優位・採用実績の独立確認は未実施。','現地調査・帰着後v1は未実施。iPhoneでのローカルHTML運用は未確認。'])
report=dict(scope=scope,main=main,domains=domains,topics=topics,research=research,evidence=ledger)
from report_narrative import revise
report=revise(report,cards,ev)
from report_catalog import enrich
report=enrich(report)
scope=report['scope'];allcases=[c for t in report['topics'] for c in t['cases']];ledger=report['evidence'];research=report['research']
for name,obj in [('report',report),('evidence_ledger',ledger),('case_comparison',allcases)]:
 (O/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2),'utf-8')
def csvout(name,rows):
 with (O/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
csvout('case_comparison',[{**{k:v for k,v in c.items() if k!='full_record'},'source_urls':'\n'.join(ev[i]['url'] for i in c['evidence_ids']),'source_locators':'\n'.join(i+': '+ev[i]['locator'] for i in c['evidence_ids'])} for c in allcases])
csvout('evidence_ledger',ledger)
csvout('research_candidates',research)
csvout('claims',report['claims'])
assert all(i in ev for c in allcases for i in c['evidence_ids'])
assert len({t['topic_id'] for t in topics})==len(topics)
(R/'checkpoints/report_completion_v0.json').write_text(json.dumps(dict(status='編集内容保存・PPTX作成中',plan=['薄い加工技術を補完（完了）','17テーマの根拠補足と6分野の4項目まとめを作成','本編1枚を編集','リンク対応・体裁を1回確認し保存'],scope=scope),ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(scope,ensure_ascii=False,indent=2))
