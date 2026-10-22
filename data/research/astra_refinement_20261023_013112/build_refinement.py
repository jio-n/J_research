"""Build a new research edition only. Raw downloads are private and are not published."""
from pathlib import Path
import json,csv,copy,re,collections,hashlib,unicodedata
R=Path(__file__).resolve().parents[3]; D=Path(__file__).parent; O=R/'outputs'/D.name
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,obj): (D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
base=load(R/'data/research/four_tag_20261022/research.json'); data=copy.deepcopy(base)
items={x['id']:x for x in data['items']}; changes=[]; evidence=[]
TAGS=['AI','フィジカルAI','自律化','自動化']
def source(key,url,publisher,title,locator,summary,limit='',quote='',published='未記載',mode='今回本文照合'):
 s=dict(source_id=key,url=url,publisher=publisher,title=title,locator=locator,checked_date='2026-10-23',published_date=published,usage=mode,short_quote=quote,context_summary=summary,not_evidence_for=limit,verification=mode)
 evidence.append(s); return s
def edit(id,why,srcs=(),tags=None,**fields):
 x=items[id]; before={k:copy.deepcopy(x.get(k)) for k in fields}
 if tags:before['tags']={t:copy.deepcopy(x['tags'][t]) for t in tags}
 x.update(fields)
 if tags:
  for t,(status,reason) in tags.items():x['tags'][t]={'status':status,'reason':reason}
 for s in srcs:
  x['sources']=[v for v in x['sources'] if v['url']!=s['url']];x['sources'].insert(0,copy.deepcopy(s))
 x['refinement_review']='今回原典照合' if srcs else '既存根拠の再整理'
 if srcs:x['depth']='企業・公式出展資料を今回照合'
 x['as_of']='2026-10-23'
 changes.append(dict(id=id,reason=why,before=before,after={k:copy.deepcopy(x.get(k)) for k in before},source_ids=[s['source_id'] for s in srcs]))
 return x
K=source('AR01','https://www.komatsu.jp/ja/newsroom/2026/20261022_01','コマツ','JIMTOF2026に出展','CX500／KOM-Scheduler／Gate Keeper／KOMTAS／KOM-MICS', '画像による切りくず堆積検知、工具交換時期の予測、加工異常のしきい値設定を別機能として展示。Gate Keeperはコンセプト展示。','切りくずの自動除去、全工場の自動再計画、KOMTASの機械学習方式は確認できない。',published='2026-10-22')
C=source('AR02','https://www.cgsys.co.jp/jp/cam-tool/function_features.html','C&Gシステムズ','CAM-TOOL 機能紹介','AI切削条件算出／Ver20.1・Ver22.2','データマイニングにより工具・材質・加工条件から切削条件を算出。ユーザーの過去条件も学習できる。','2026年に初めて実用化した機能ではない。加工中の閉ループ制御や機械への自動適用は不明。',quote='AI技術の「データマイニング手法」を活用し')
CE=source('AR03','https://www.cgsys.co.jp/jp/products/event_ct.html','C&Gシステムズ','CAM-TOOL 展示会情報','JIMTOF2026','CAM-TOOLの出展を告知。','AI切削条件算出の特定バージョン・実演内容までは未確認。')
M=source('AR04','https://www.mazak.com/jp-ja/technology/productivity/','ヤマザキマザック','生産性向上 MAZATROL DX','SOLID MAZATROL／VIRTUAL MACHINING／CUTTING ADVISER／SETUP GUIDE','形状モデル・工具情報・過去プログラムを活用する自動プログラミングと、仮想検証・条件解析・段取り支援を統合。','各モジュールがすべてAIであるとは言えない。工程設計の共同開発AIと既存製品は別。')
F=source('AR05','https://www.fanuc.co.jp/ja/product/cnc/physical-ai-cnc/index.html','ファナック','フィジカルAI CNC','CONCEPT／MCP／デジタルツイン／実現すること','生成AIの解析・提案を仮想環境で検証し、人が承認して実機へ適用する。プログラム・設定・アラーム対応を支援。','完全無人加工や無承認の自動復旧を証明しない。',quote='その結果をオペレータが確認・承認した上で実機へ適用できます。')
FE=source('AR06','https://www.fanuc.co.jp/ja/JIMTOF2026/','ファナック','JIMTOF2026 特設ページ','FA／ROBOT','フィジカルAI CNC、Smart Digital Twin、生成AIを用いたロボット駆動事例等を予告。','溶接・VLA・キッティングの個別事例のJIMTOF展示を特定できない。')
FW=source('AR07','https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260911.html','ファナック','AI溶接エージェント','図面読取／条件・動作生成／展示と販売予定','図面を撮影して生成AIが溶接条件とロボット動作を生成。ユーザーは確認・変更し実行する。国際ウエルディングショーで展示を予告、12月末販売予定。','JIMTOF展示の証拠ではない。多品種の成功率や溶接品質保証の範囲は未確認。',published='2026-09-11')
FK=source('AR08','https://www.fanuc.co.jp/ja/product/robot/academia/case_study/ai-agent-robot-kitting-system.html','ファナック','AIエージェントとマスタレス認識によるキッティング','自然言語指示／注文票／部品認識','注文内容を解釈し、部品・トレーの認識とロボット動作へ接続する事例。','未知物への一般化性能、失敗時再試行、JIMTOFでの個別実演は不明。')
FV=source('AR09','https://www.fanuc.co.jp/ja/product/robot/academia/case_study/imitation-learning-ai-robot.html','ファナック','模倣学習AIロボット','リーダー・フォロワー／VLA／Tシャツ折り畳み','教示中の画像と動作、言語ラベルで学習し、視覚・言語から動作を推論する。','方式の新しさと、未学習の布・失敗からの復帰・現場稼働率は別。JIMTOF展示未確認。')
FT=source('AR10','https://www.fanuc.co.jp/ja/product/robot/academia/case_study/moving-parts-ai-tracking-screwdriving.html','ファナック','移動ワークへのAI追従ねじ締め','3D認識／追従／定トルク締結','動く部品のねじ位置を認識し、ロボットが追従して締結する。','1msの追従記載をAI推論の周期とは読まない。VLA採用は未確認。')
FH=source('AR11','https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260930.html','ファナック・日立','フィジカルAI実装に向けた戦略的協業','カスタマーゼロ／実証／2027年度','日立の茨城県内の工場を実証先とし、部品形状変化への対応や認識・動作生成、品質・タクトを検証する計画。','ファナック自社工場での実証とは書かれていない。計画は展示実証・量産性能の証拠ではない。',published='2026-09-30')
AB=source('AR12','https://www.abejainc.com/news/20261016/2','ABEJA・ヤマザキマザック','製造業のフィジカルAI実現に向けた協業','Engineering AI Agent／Scheduling AI Agent／Robotics','工程設計の技能と生産計画の制約を取り込み、人を含む検証を伴うAIエージェントを開発する構想。','製品版の提供・実演成功・工場全体の最適化達成は証明しない。',published='2026-10-16')
AI=source('AR13','https://www.aist.go.jp/aist_j/news/pr20260702.html','産業技術総合研究所','製造AX拠点','製造データ取得支援／匿名化・構造化','製造現象の理解に基づくデータ取得と、共有可能な形への加工を支援する。AI開発の前に取得設計が必要。','データ量だけでAI精度や加工モデルの精度が上がるとは言えない。',quote='製造工程の現象理解に基づく製造データ取得の支援',published='2026-07-02')
DG=source('AR14','https://www.dmgmori.co.jp/corporate/news/2026/20260706_geniac.html','DMG森精機','GENIAC採択：生産設備データと製造フィジカルAI','自律的AI開発基盤／対象設備・データ','100社・1,000設備・100TB規模を目指すデータ取得と、異常検知から品質・電力予測、セル最適化へ展開する計画。','数値は目標。データ取得完了・収益改善実績ではない。今回は再取得失敗のため保存済み公式本文で再照合。',quote='市場投入済みの設備から継続的にデータを収集・学習・評価する仕組み',published='2026-07-06',mode='既存保存本文を今回再照合（再取得失敗）')
OK=source('AR15','https://www.okuma.co.jp/smart-factory/osp-suite/osp-ai.php','オークマ','OSP-AI','AI機械診断／AI加工診断','機械診断は診断運転から異常箇所を提示。加工診断は制御情報の異常レベルに応じ工具を自動退避する。','診断後の修理・復帰の自律化や、あらゆる工具・加工への適用は未確認。')
MW=source('AR16','https://www.moduleworks.com/see-you-at-jimtof-2026/','ModuleWorks','See you at JIMTOF 2026','SmartRoughing／FeedControl／NGSP／CAS／MDES','工具経路・切削負荷の最適化から機上シミュレーション、衝突防止、データ交換までを提示。','FeedControlの物理量による送り最適化を機械学習AIと推定しない。',published='2026-10-15')
RE=source('AR17','https://www.renishaw.com/jp/smart-manufacturing-data-platform-for-industrial-process-control--47853','レニショー','Renishaw Central','IPC／工作機械への補正／ダッシュボード','測定・加工状態を収集し、IPCで機械変数に補正を返す。分析・監視表示も提供。','閉ループ制御の説明はあるが、学習AIを使う証拠にはならない。')
PH=source('AR18','https://www.phoxter.co.jp/automated-logistics/products/stelladrive','Phoxter','StellaDrive','移動方式／生成AIチャットボット','SLAM等の移動機能と、任意の保守・初動対応チャット機能を分けて説明。','生成AIがAMRの走行軌道を生成するとは扱わない。')
PE=source('AR19','https://www.phoxter.co.jp/news/jimtof2026','Phoxter','JIMTOF2026に出展','良品学習／6軸ロボット連携／全方位AI外観検査','良品のみの学習と難検査ワーク、多視点のロボット検査を予告。','AIが撮像姿勢を再計画するとは記載されていない。',published='2026-10-19')
ND=source('AR20','https://ndotlight.com/','NdotLight','TRINIX / Physical AI','SimReady／物理属性・ジョイント／USD・URDF・MJCF','CADや3Dデータを学習・シミュレーション環境に適した形式へ変換する支援。','推定した物性値が実測同定済みとは限らない。物理AIの動作本体と区別する。')
AU=source('AR21','https://www.autonomiq.de/','autonomIQ','simplymill','CAD hochladen／設定／Prüfen & Exportieren','CAD形状・材料・工具・機械条件から経路を作り、人が確認してNCを出力する構成。','モデルの学習法・誤り率・実機検証条件は非公開。')
JT=source('AR22','https://toyoda.jtekt.co.jp/jimtof2026/','ジェイテクト','JIMTOF2026','Mill-Plan／fine-teachless／mJM','工具・姿勢・条件を含む工程設計、仮想教示と実機誤差の補正、運用支援を提示。','工程設計自動化と幾何補正の説明だけで機械学習AIとしない。')
GH=source('AR23','https://www.jimtof.org/search/jp/ESdetails?e=8ealehgmk8o','サイバーRC／JIMTOF','GH5 出展説明','主な出展物／3D画像とAI補正','カメラで工具形状を認識し、設定された幅・角度へ加工を補正するホーニングを訴求。','AIモデルの種類、精度と再試行条件は未公開。')
KA=source('AR24','https://www.jimtof.org/search/jp/ESdetails?e=ekM3exgIAtc','カネテック／JIMTOF','AI・2Dカメラ・マグネットピンセット','主な出展物','カメラ・AIと磁気ハンドで小ねじのばら積みピッキングを行う構成を提示。','検出・把持点・重なり解消のどこをAIが決めるか、学習法や復帰能力は未公開。')
TM=source('AR25','https://www.tm-robot.com/ja/product/ai-vision','Techman Robot','AI Vision','AI Training／TMflow／AI Vision','AI学習と画像判断をTMflowのビジョンノードへ統合。画像認識とロボット位置決めを製品体系で提供。','今回の実演がAIで動作を変えるか、従来の位置検出かは現地確認。VLAの証拠はない。')
SH=source('AR26','https://smd.co.jp/news/jimtof2026/','シマダマシンツール','JIMTOF2026に出展','HS4200／SAM','HS4200と投入・加工・排出・梱包をつなぐSAMを案内。','公式カタログのフィジカルAI段取り替えについて、方式の説明はない。',published='2026-10-06')
SH2=source('AR27','https://www.jimtof.org/search/jp/ESdetails?e=xntdeqgs_F4','シマダマシンツール／JIMTOF','HS4200 出展説明','主な出展物','フィジカルAIを用いた自動段取り替えを掲載。','名称だけでは生成AI・VLA・再試行などの能力を特定できない。')
TD=source('AR28','https://www.jimtof.org/search/jp/ESdetails?e=2N7pXq5Aehs','ツールディスカバリー／JIMTOF','AI切削条件計算','主な出展物','工具・材料・工程を選び、AIによる切削条件のガイドを得るWebツール。','AIモデルの種類、再学習、精度保証は未公開。')
NS=source('AR29','https://www.jimtof.org/search/jp/ESdetails?e=hzAGGAi5wL4','日本精工／JIMTOF','2026出展説明','出展紹介／主な出展物','トライボロジー等の製品群を案内。','このページから旧版の振動診断AIの2026展示を特定できない。')
BU=source('AR30','https://www.jimtof.org/search/jp/ESdetails?e=XR5ASqmy4zw','BUFFOLI TRANSFER／JIMTOF','2026出展説明','出展紹介／実機展示の有無','ターンキーライン、AI検査・予知保全を訴求。展示はワーク・映像。','実機展示はないと明記。AIの具体的方式は不明。')
IT=source('AR31','https://www.jimtof.org/search/jp/ESdetails?e=7ypX6WR51KU','伊藤忠マシンテクノス／JIMTOF','2026出展説明','フィジカルAI向け開発／ロボット教示／FMS','ロボット制御の二次開発や統合支援を提示。','実機の特定自律作業が完成したという証拠ではない。')
IW=source('AR32','https://www.iwatatool.co.jp/jimtof/','イワタツール','JIMTOF2026','TRIエンジニアリングのロボット加工','穴・面・タップ・ベルトサンダー等を含むロボット加工を展示。','このページにはAIの認識・判断対象を特定する記載がない。')
ME=source('AR33','https://fa-site.mitsubishielectric.co.jp/fa/events-seminars/exhibitions/2026/jimtof2026/index.html','三菱電機','JIMTOF2026','放電加工機／新開発スケジューラ','放電加工の運用を支えるスケジューラを出展。','最適化アルゴリズム・AIの利用・再計画の制約は未公開。')
FA=source('AR34','https://www.fact-cam.co.jp/pages/about/jimtof2026-v2.html','フアクト','JIMTOF2026','出展情報／Fusion／NCGO／実機検証','Fusion・ポスト・NC作成・導入支援。自社告知の小間はS3017。','既存公式一覧はS3013。小間相違は現地案内で最終確認。AI担当機能はこの告知では未特定。')
CL=source('AR35','https://www.cloudnc.com/ja/mastercam','CloudNC','CAM Assist for Mastercam','工具・材料・機械設定／加工方向／生成・確認','工具・保持・加工方向等を設定し、生成した工程・経路を人が調整してCAMに取り込む。','NC出力後の実機運転まで自律化したとは扱わない。')
MK=source('AR36','https://www.makinoseiki.co.jp/exhibition/jimtof2026.html','牧野フライス精機','JIMTOF2026','SG10EX／monocam2／AGE30FX','工具の画像計測と自動補正、再研削のスケジュール機能を紹介。','自動計測・補正だけでは学習AIの証拠にならない。')

edit('FC006','未特定だった対象タスクを製品公式説明から具体化。自動復旧は提案と実機適用を分離。',[F,FE],task='工程設計・NC生成／加工条件提案／保全支援',need='プログラム準備、CNC設定、異常原因の調査にかかる技能依存と工数を減らす。',input='加工情報・設備状態・自然言語による指示。許可されたCNC／ツイン機能をMCPで呼び出す。',output='プログラム・条件・操作案、仮想検証結果。オペレータ承認後に実機適用。',human='目標・条件の指定、仮想検証の確認、実機適用の承認。失敗後の復帰・権限設計は要確認。')
edit('FT-Z01','参照先の現在の製品はMAZATROL DX。旧名称と共同開発AIを混在させない。',[M],item='MAZATROL DX／SOLID MAZATROL',task='工程設計・NC生成／加工条件決定／段取り検証',input='3D形状、工具ライブラリ、過去の加工プログラム、必要に応じ実加工データ。',method='SOLID MAZATROLのパターン学習によるプログラミング。仮想加工で干渉を確認し、CUTTING ADVISERで条件を解析、SETUP GUIDEで準備を支援。',output='MAZATROLプログラム、条件案、工具・治具等の段取り情報。',human='工具・機械の条件整備、結果確認、実際の段取り。全モジュールの自動実行範囲は要確認。',limits='共同開発する工程設計AIとは別製品。パターン学習と条件解析を同一AIとみなさない。',advance='工程設計・仮想検証・段取り支援の製品統合。2026初登場を意味しない。')
edit('AC095','公式製品資料でAIの担当機能と入力を確認。呼称のみから機能記載へ。',[C,CE],item='CAM-TOOL AI切削条件算出',task='加工条件決定',need='工具・材料・加工条件の組合せごとの条件探索と技能依存を減らす。',input='工具・ワーク材質・加工条件、ユーザーの過去の切削条件。',method='データマイニングによる切削条件算出。ユーザー条件の学習にも対応。',output='加工に用いる切削条件の候補。',human='工具・材料の選択、学習データ整備、算出条件の採否と試加工。',limits='AI切削条件算出はVer20.1にも記載。Ver22.2の適用拡張と、今回の実演機能は区別。',exhibit='製品出展・当該機能未確認',exhibit_note='CAM-TOOLの出展を告知。AI切削条件算出の版・実演対象は未確認。',recommendation='比較訪問',recommend_reason='経験条件の学習と物理モデル型の送り最適化を比較できる。',check='学習に必要な成功・失敗条件の件数、未学習材への適用、推奨条件の信頼度と試加工の扱い。',tags={'AI':('機能記載','データマイニングで工具・材質等から切削条件を算出。')})
edit('FT-O01','機械診断と加工診断の出力・人の残作業を分離。',[OK],input='機械診断：診断運転中の制御データ。加工診断：主軸・送り軸等の加工中制御情報。',method='機械診断は異常・異常箇所を推定。加工診断は異常レベルを評価し閾値超過で工具を退避。',output='診断箇所の表示／加工異常時の工具退避。修理の自動化は確認できない。',human='機械診断の開始、診断結果に基づく整備、工具確認・再開。しきい値と適用機種の設定条件は要確認。')
edit('FC009','熱変位制御の説明とOSP-AIを別アイテムへ整理。AI利用未確認を非AIの断定にはしない。',item='熱変位制御（AI利用未確認）',tags={'AI':('—','この熱変位制御アイテムの学習モデル利用を確認できない。OSP-AIはFT-O01で別記。')})
edit('FT-M01','切削負荷による送り最適化と機械学習を区別。',[MW],method='SmartRoughingで送り・回転・切込み等を設定。FeedControlは切削力、切りくず厚、トルク、動力等の制約から送りを最適化。',limits='機械学習の採用は未確認。加工モデルの校正条件と、機上での動的再計算範囲は確認が必要。')
edit('FT-M02','機上検証・干渉防止・データ交換の連携範囲を明確化。',[MW])
edit('FC033','測定から機械変数への補正を確認。閉ループと学習AIは別。',[RE],method='測定・加工状態・アラームをオンプレミスに収集。IPCで測定結果から工作機械の変数へ補正を返す。',human='測定・補正対象と許容範囲の設定、アラーム時の処置。補正承認条件は要確認。',depth='企業・公式出展資料を今回照合')
for id,s in [('FT-F01',FW),('FT-F02',FK),('FT-F04',FV),('FT-F03',FT)]:edit(id,'公式事例の技術を再照合。個別のJIMTOF展示を引き続き未確認とする。',[s,FE],exhibit='展示未確認',exhibit_note='会社のJIMTOF出展は確認。特定の事例・デモが今回展示される明記は未確認。')
edit('FT-F01','発売予定・他展示会の告知をJIMTOF実演と分離。',stage='国際ウエルディングショーで展示予告／2026年12月末販売予定',human='図面撮影、生成された条件・動作の確認または調整、実行指示。',limits='公開情報は図面→条件・動作生成の構成。学習外図面の成功率、品質検証、異常後復帰は未確認。')
edit('AC273','データ変換基盤と動作AIを区別。',[ND],input='CAD・3D形状とシミュレーション用途の条件。',method='物理属性・ジョイント等を推定し、USD／URDF／MJCF等のSimReady資産を生成する。',output='シミュレーション・学習環境で使う3Dデータ。',human='属性・拘束の妥当性確認、実測値による校正、対象ロボットでの検証。',limits='推定物性の実測検証、接触モデル精度、実機動作の成功率は未確認。',advance='生成・変換基盤。自律動作の完成度とは別軸。')
edit('FT-A01','AI CAMの人による設定・確認を具体化。',[AU],input='CAD形状、材料、工具、機械・加工制約。',human='加工条件・工具等を設定し、結果を確認してNCをエクスポートする。',limits='アルゴリズム詳細、加工品種ごとの検証、既存CAMとの性能差は未確認。')
edit('FT-J01','工程設計の自動化とAI採用を分離。',[JT])
edit('FC020','生成前の準備と生成後の人の確認を補足。',[CL],input='3Dモデル、工具、材料、ワーク保持、機械、加工方向・回避領域。',human='条件と工具を整備。生成された工程・経路を確認・修正しCAMへ取り込み、ポスト処理後の実機適用を判断。')
edit('AC209','工具計測と補正の展示を再照合。',[MK])
edit('AC085','AI補正は公式出展説明にあるがモデル種類・適応能力は不明。',[GH],input='機内カメラによる工具形状の画像、目標の幅・角度等。',method='3D画像とAIによる形状認識・補正をうたい、ホーニングを目標幅・角度へ調整する。',human='数値・対話式の条件設定、加工品の準備、結果確認。',limits='学習法、精度、未学習形状、失敗後の補正・再試行条件は未公開。')
edit('AC051','AI・カメラ・磁気ハンドの接続を確認。AI担当の細部は留保。',[KA],input='小ねじ等のばら積み画像、ハンド・ワークの設定。',method='2DカメラとAIの認識を協働ロボット・磁気ピンセットのピッキングに使う構成。',limits='検出と把持点計画の担当分界、重なり解消、把持失敗の判定・再試行は未確認。')
edit('AC159','AI Visionの学習機能を確認。VLAや今回のAIによる動作変更は認定しない。',[TM],method='AI学習と画像判断をTMflowのビジョンノードへ統合。内蔵カメラによる位置決めとロボット作業を提供。',human='画像の準備・学習、TMflowでのタスク設定、安全領域・把持条件の設定。',limits='AI画像判断と従来位置検出の使い分け、今回の実演対象、AIが動作を変える範囲は未確認。',tags={'AI':('機能記載','学習画像によるAI VisionとTMflowへの組込みを開発元資料で確認。'),'フィジカルAI':('呼称・用途記載','AI視覚とロボットを提供するが、今回のタスクでAI出力が動作をどう変更するか未確認。')})
edit('FC051','企業出展告知とAI段取り替えの詳細不足を併記。',[SH,SH2],limits='段取りの何をAIが認識・計画するか未公開。ロボット＋AIの名称からVLA・自律復帰を推定しない。',exhibit='出展説明に掲載',check='ワーク・治具の変更を何で認識し、どの段取り動作を再生成するか。人の教示量、失敗時の復帰、新旧方式の差を実演で確認。')
edit('AC136','AIの用途が切削条件計算と確認できたため、呼称だけの分類を修正。',[TD],input='工具・材料・加工工程の選択情報。',method='スマートフォン等のWeb画面で指定した条件からAIが推奨切削条件を計算する。',output='切削条件のガイド。',human='入力条件の選択と推奨値の採否、試加工・機械設定。',tags={'AI':('機能記載','工具・材料・工程から切削条件を算出するAI用途を公式説明で確認。')},limits='モデル・学習データ・推奨精度の根拠は未確認。')
edit('FC052','2026公式説明を再確認したが個別AI機能の展示を確定できない。',[NS],exhibit='展示未確認',exhibit_note='企業は2026出展。振動診断AIは既存資料の比較候補として保持し、2026の個別展示は未確認。')
edit('AC252','実機展示なしを明示。',[BU],exhibit='映像・資料展示',exhibit_note='公式説明で実機展示なし。ワークサンプル・映像による紹介。AI検査・予知保全の詳細は未公表。')
edit('AC019','フィジカルAI開発支援と特定の自律作業を区別。',[IT])
edit('AC022','ロボット加工の実演告知を確認。AIの担当機能は未確認。',[IW],method='ロボットを用いる穴・面・タップ・ベルトサンダー等の加工実演。AIによる加工指導は既存出展説明の訴求で、詳細未確認。',limits='AIが工具経路・加工条件・補正のどれを決めるか今回の企業告知では不明。')
edit('FC065','企業の特設ページでもスケジューラの展示を確認。',[ME],exhibit='展示予定を明記',exhibit_note='企業の2026特設ページで放電加工機の新開発スケジューラを明記。AI採用・最適化範囲は未確認。')
edit('AC194','新しい企業告知と元の一覧の小間相違を記録。AIの担当機能は未確認。',[FA],booths=['S3017'],item='Fusion／ポスト・NCGO・CAM導入支援',method='FusionでCAD・CAM・シミュレーションを連携。ポスト作成とブラウザNCGOでNC出力・現場導入を支援。',exhibit_note='企業特設はS3017。元の公式一覧S3013と相違があるため、会場案内で最終確認。',limits='AI担当範囲は未確認。旧版のFeatureCAM・ENCYを今回同一展示と断定しない。')
edit('FT-P01','6軸ロボットとのAI検査実演は確認。姿勢のAI再計画は確認できない。',[PE],human='良品画像の準備、判定閾値と撮像・ロボット条件の設定。再撮像の判断を誰が行うか要確認。')
for x in list(items.values()):
 if 'StellaDrive' in x['item']:edit(x['id'],'生成AIの保守支援とSLAM走行を明確に分離。',[PH],method='走行はSLAM・LiDAR等の移動技術。生成AIは保守・トラブル初動のチャット支援として追加する構成。',limits='生成AIによる経路・動作生成は未確認。障害回避性能とチャットの回答精度は別に評価。')

edit('AC077','10/22の新告知でCX500と計測ステーションの位置付けを具体化。',[K],item='CX500＋パレット／Gate Keeper',task='段取り交換／工程内検査',input='加工ワーク・パレット、検査用画像、加工予定。',method='6枚単位で拡張するリニアパレットと工具ストッカーで連続運転。パレット待機中のワークを画像検査するGate Keeperをコンセプト提示。',output='連続加工のワーク供給、外部搬送・段取りを減らした検査。',human='ワーク・工具・検査条件の準備、判定後の処置。',exhibit='製品＋コンセプト展示',exhibit_note='CX500等の製品展示と、Gate Keeperのコンセプト展示を区別。10/22企業告知。',stage='CX500等：製品紹介／Gate Keeper：コンセプト展示',limits='検査AI利用、検査結果の加工補正への自動フィードバックは未確認。',recommendation='比較訪問',recommend_reason='加工・パレット待機・検査の工程接続を具体的に確認できる。',check='測定待ち時間とラインのボトルネック、検査判定の方式、補正・不良品排出の接続範囲。')
def add(id,item,task,need,input,method,output,human,limits,tagdict,check,reason):
 x=copy.deepcopy(items['AC077']);x.update(id=id,legacy_ids=[],item=item,task=task,need=need,input=input,method=method,output=output,human=human,limits=limits,check=check,recommend_reason=reason,exhibit='展示予定を明記',exhibit_note='コマツの2026年10月22日付告知で個別機能を明記。',stage='JIMTOF2026展示予定／提供条件は現地確認',advance='2026告知の新機能。アルゴリズム・性能は個別確認。',recommendation='比較訪問',sources=[copy.deepcopy(K)],baseline='今回追加。元の出展者IDへ紐付け。')
 x['tags']={t:{'status':'—','reason':'この機能の公開説明では担当範囲を確認できない。非利用を断定するものではない。'} for t in TAGS}
 for t,(status,reason2) in tagdict.items():x['tags'][t]={'status':status,'reason':reason2}
 items[id]=x;changes.append(dict(id=id,reason='10/22の新告知から個別タスクとして追加。',before=None,after={'item':item},source_ids=['AR01']))
add('AR-C01','KOM-MICS AI予知保全（切りくず検知）','切りくず監視・保全','切りくず堆積による停止・品質悪化を防ぐ。','機内カメラ画像。','AIが切りくずの堆積増加・異常を画像で検知する。','洗浄を促す通知。','通知を受けて洗浄・処置する。撮像・学習・閾値設定は現地確認。','AIが洗浄・除去動作を実行する記載はない。',{'AI':('機能記載','機内画像から切りくずの異常な堆積を検知。'),'自動化':('機能記載','監視・通知を自動化。物理除去は別。')},'切りくず材質・照明変化への頑健性、誤報・見逃し、通知後の対応時間と洗浄との接続。','TAKISAWAの認識→除去と、AI検知→人の対応の境界を比較。')
add('AR-C02','KOMTAS 異常判定しきい値の自動設定','工具状態監視・加工異常検知','加工監視の条件設定を省力化する。','加工負荷等の監視データ。信号・学習期間の詳細は要確認。','正常・異常を判定するしきい値を自動設定する。AI方式は告知から確認できない。','加工異常監視の判定条件。','適用工程の選択、判定結果の確認、異常時の処置。','自動設定のアルゴリズム、追従更新、工具停止制御は未確認。',{'自律化':('限定機能','しきい値設定をシステム側で行う。自己更新範囲は未確認。'),'自動化':('機能記載','判定条件の設定工数を自動化。')},'正常学習期間、工具交換後の再設定、誤検知率、停止・退避とのインターフェース。','AIと非AIを混同せず、監視の導入工数を比較できる。')
add('AR-C03','KOM-Scheduler','生産計画・工具交換計画','長時間運転中の工具不足と生産停止を防ぐ。','加工予定・工具の使用状況等。入力仕様は要確認。','生産スケジュールを表示し、工具不足と交換時期を予測する。','スケジュールと工具交換タイミングの提示。','計画の入力・調整、工具補給・交換の実施。','自動再計画、最適化目的関数、機械学習採用は未確認。',{'自動化':('機能記載','計画表示と工具不足・交換時期の予測を支援。')},'工具寿命の実測値と計画が接続するか。突発停止・急な割込み時に再計画するか。','生産計画と設備・工具状態の接続を現物で確認する候補。')
# Retire one non-specific aggregate, retaining the old ID and rationale in a separate ledger.
retired=items.pop('FC003');save('retired_items.json',[{'item':retired,'reason':'一般的なAIエージェント搭載という総称。独立した対象機能が特定できないため、具体機能のFC004とFT-D01へ統合。その他エージェントの存在を否定しない。','replacement_ids':['FC004','FT-D01']}])
changes.append(dict(id='FC003',reason='具体機能と重複する総称を統合。',before={'item':retired['item']},after=None,source_ids=['AR14']))

taxonomy=[('P01','工程設計・NC生成','形状・図面から工程・工具経路・NCを準備する。'),('P02','加工条件最適化','工具・材料・負荷から条件を推奨または調整する。'),('P03','工具状態・加工監視','摩耗・破損・加工異常を検知し保護・交換へつなぐ。'),('P04','寸法計測・補正','測定値を評価し寸法・熱変位・形状を補正する。'),('P05','外観検査・識別','良否・欠陥・個体・姿勢を画像等で識別する。'),('P06','段取り・工具交換','治具・工具・ワークを交換し位置合わせする。'),('P07','搬送・供給','設備間・設備内のワーク・工具を搬送する。'),('P08','ロボット作業・教示','認識・教示・計画を把持・加工・組立動作へつなぐ。'),('P09','保全・周辺作業','設備診断、清掃、切りくず、潤滑等を支援する。'),('P10','生産計画・運用','工程・工具・設備・在庫の計画と運用を管理する。'),('P11','データ・シミュレーション基盤','データ接続、モデル化、仮想検証、学習を支える。'),('P12','制御ソフト・設計支援','PLC・HMI・設計・図面検索等のエンジニアリングを支援する。'),('P13','加工・仕上げ自動化','切削・研削・仕上げ等の加工動作を自動化する。'),('P14','担当機能要確認','公開説明から担当範囲を十分に特定できない。')]
override={'FC006':['P01','P02','P09','P11'],'FT-Z01':['P01','P02','P06','P11'],'FT-O01':['P03','P09'],'AC077':['P06','P05'],'AR-C01':['P09'],'AR-C02':['P03'],'AR-C03':['P10'],'AC273':['P11'],'FT-F01':['P08','P01'],'FT-F02':['P08','P07'],'FT-F04':['P08'],'FT-F03':['P08'],'AC085':['P13','P04'],'AC051':['P08','P07'],'AC159':['P08','P05'],'FC051':['P06','P08'],'FT-P01':['P05'],'FT-M02':['P11','P01'],'AC019':['P11','P08'],'FC033':['P04','P11'],'AC209':['P04','P13'],'AC095':['P02'],'AC136':['P02'],'FC065':['P10'],'AC194':['P01'],'FC009':['P04']}
rules=[('P02',r'条件|送り|回転数|負荷を予測'),('P03',r'加工信号|刃先|摩耗|工具寿命|工具損傷|刃具破損'),('P04',r'計測|補正|熱変位|寸法'),('P05',r'検査|識別|撮像'),('P06',r'段取り|交換|固定|治具'),('P07',r'搬送|供給|搬入|パレット'),('P08',r'教示|把持|組立|遠隔操作|キッティング'),('P09',r'保全|異常診断|切粉|周辺|環境管理|アラーム|潤滑'),('P10',r'生産計画|運用|負荷調整|在庫管理|調達'),('P01',r'工程設計|プログラム|CAM|NC作成|NC生成'),('P11',r'接続|データ連携|モデル実装|I/O基盤'),('P12',r'PLC|HMI|設計|図面検索'),('P13',r'加工・仕上げ|自動処理')]
tn={id:name for id,name,_ in taxonomy}
for x in items.values():
 x.setdefault('refinement_review','既存台帳を継承（今回個別本文未再照合）')
 cats=override.get(x['id']) or [id for id,p in rules if re.search(p,x['task'])] or ['P14'];x['task_ids']=cats;x['task_categories']=[tn[k] for k in cats]
 x['taxonomy_basis']='個別精査による割当' if x['id'] in override else '既存の対象タスクを標準カテゴリへ対応付け（技術の追加認定ではない）'
 x['source_ids']=list(dict.fromkeys(s['source_id'] for s in x['sources']));x['source_urls']=list(dict.fromkeys(s['url'] for s in x['sources']));x['tag_names']=[t for t in TAGS if x['tags'][t]['status']!='—']
 x['manufacturer_claim']='メーカーの製品・展示説明。能力の独立実証ではない。'
 x['physical_ai_class']='対象機能未確認／今回非認定'
 if x['tags']['フィジカルAI']['status']=='関連基盤':x['physical_ai_class']='開発・学習基盤'
 elif x['tags']['フィジカルAI']['status']=='呼称・用途記載':x['physical_ai_class']='呼称／動作への接続要確認'
 elif x['tags']['フィジカルAI']['status']=='機能記載':x['physical_ai_class']='認識・予測→限定動作・補正'
 if x['id'] in ['FC006','FT-F01','FT-F02']:x['physical_ai_class']='生成AI・エージェント→物理実行（承認条件を確認）'
 if x['id']=='FT-F04':x['physical_ai_class']='VLA・模倣学習→動作生成'
 x['connection']=x['input']+' → '+x['method']+' → '+x['output']
 x['novelty_note']=x['advance']+'。公開記載の有無と、2026初登場・性能優位性を区別する。'
# Selected review outcomes where the item was kept intentionally.
data['items']=list(items.values());data['as_of']='2026-10-23';data['title']='JIMTOF2026 技術動向・訪問選定 改訂版'
for a in data['audit']:
 linked=[x for x in data['items'] if a['record_id'] in x['listing_ids']]
 a['item_ids']=[x['id'] for x in linked];a['tag_names']=[t for t in TAGS if any(t in x['tag_names'] for x in linked)]
 if linked:a['status']='候補あり'
 if a['record_id'] in retired['listing_ids']:a['reason']+=' 新版では総称FC003を具体機能に統合。'
 if a['record_id'] in items['AC077']['listing_ids']:a['reason']+=' 10/22企業告知で個別機能3件を追加。'
 if a['record_id'] in items['AC194']['listing_ids']:a['reason']+=' 小間相違：元一覧S3013、企業告知S3017。元の小間欄は保存。'
for m in data['majors']:
 m['item_ids']=[i for i in m['item_ids'] if i!='FC003']
 if any(i in m['item_ids'] for i in ['AC077']):m['item_ids']+=['AR-C01','AR-C02','AR-C03']
norm=lambda s:re.sub(r'[\s・･,，.．()（）]','',unicodedata.normalize('NFKC',s)).replace('株式会社','').replace('合同会社','').lower()
stat=data['stats'];stat.update(candidate_items=len(items),candidate_companies=len({norm(x['company']) for x in items.values()}),tag_counts={t:dict(collections.Counter(x['tags'][t]['status'] for x in items.values() if x['tags'][t]['status']!='—')) for t in TAGS},depth_counts=dict(collections.Counter(x['depth'] for x in items.values())),audit_status=dict(collections.Counter(a['status'] for a in data['audit'])),refined_items=len({c['id'] for c in changes if c['id'] in items}),fresh_review_items=sum(x['refinement_review']=='今回原典照合' for x in items.values()),reviewed_sources=len(evidence),recommendations=sum(x['recommendation']!='通常候補' for x in items.values()))
data['limitations']=[f"全1,146掲載行・806説明本文を持つ既存母集団を継承。新版は{len(items)}候補。未掲載の全製品を網羅する調査ではない。",f"今回の原典照合は{stat['fresh_review_items']}候補と戦略資料を優先。残りは従来の確認深度を明示して継承。取得ログは精読件数に含めない。","機能記載はメーカーの説明の確認であり、精度・成功率・量産実績の独立実証ではない。","AI・フィジカルAIの呼称、基盤、限定機能を含む集計。導入率・先端技術の普及率ではない。","展示予定は2026年10月23日までの公開情報。特定の版・機能・実演条件は会場で確認する。","DMG森精機の一部サイトは今回再取得に失敗。保存本文・前版の確認日を区別して使用。","顧客課題・推奨・接続の意義・開発余地は調査者の分析。個別顧客のヒアリング結果ではない。","物理AIは本調査の作業定義で分類。業界統一規格ではなく、VLA等の新規性は別軸。"]
save('research.json',data);save('evidence_review.json',evidence);save('change_log.json',changes);save('task_taxonomy.json',[dict(id=i,name=n,definition=d) for i,n,d in taxonomy])
def writecsv(name,fields,rows):
 with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
fields=['id','company','booths','item','task_categories','task','need','input','method','output','human','AI','フィジカルAI','自律化','自動化','physical_ai_class','exhibit','exhibit_note','stage','recommendation','recommend_reason','check','limits','refinement_review','source_urls']
rows=[]
for x in items.values():
 r={k:(' / '.join(x.get(k,[])) if isinstance(x.get(k),list) else x.get(k,'')) for k in fields}
 for t in TAGS:r[t]=x['tags'][t]['status']
 rows.append(r)
writecsv('candidate_items.csv',fields,rows)
writecsv('tag_reasons.csv',['id','company','item','tag','status','reason'],[dict(id=x['id'],company=x['company'],item=x['item'],tag=t,**x['tags'][t]) for x in items.values() for t in TAGS])
writecsv('recommended_visits.csv',fields,[r for r in rows if r['recommendation']!='通常候補'])
af=['row_no','record_id','company','booth','status','reason','item_ids','tag_names','description_available','detail_url'];writecsv('all_exhibitor_audit.csv',af,[{k:' / '.join(a[k]) if isinstance(a[k],list) else a[k] for k in af} for a in data['audit']])
save('original_quotes_reference.json',load(R/'data/research/quotation_evidence_20261022/quotes.json'))
print(json.dumps(stat,ensure_ascii=False))
