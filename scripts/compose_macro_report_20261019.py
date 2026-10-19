"""Editorial content for three separately designed research deliverables."""
import csv
import json
from pathlib import Path
from analyze_macro_20261019 import norm, short

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/research/macro_20261019'
corpus = json.loads((OUT/'corpus.json').read_text(encoding='utf-8'))
byyear = {y:{r['key']:r for r in corpus if r['year']==y} for y in [2024,2026]}
cards = json.loads((ROOT/'data/research/technology_atlas_v1/fact_cards.json').read_text(encoding='utf-8'))
cardmap = {c['card_id']:c for c in cards}

sources = []
def src(n,title,url,locator,date='2026-10-19',published='掲載日記載なし'):
    sources.append(dict(id=f'S{n:02}',title=title,url=url,locator=locator,checked=date,published=published))
src(1,'JIMTOF2026 開催概要','https://www.jimtof.org/jp/outline.html','会期・開場時間・東4〜6ホール休館')
src(2,'JIMTOF2026 企画展示と特別企画','https://www.jimtof.org/jp/evt_show.html','ロボティクス企画・きさげロボット・AM ZONE')
src(3,'2026年版ものづくり白書 概要','https://www.meti.go.jp/report/whitepaper/mono/2026/pdf/gaiyo.pdf','20ページ AIロボティクス戦略の整理',published='2026-05')
src(4,'日工会 会員104社の出展見どころ','https://www.jmtba.or.jp/news/news-16826/','104社・10月26日に完全版公開予定',published='2026-10-15')
src(5,'DMG森精機 JIMTOF2026','https://www.dmgmori.co.jp/sp/jimtof/jimtof2026/','GX Flex・AMR・工具管理から保全までの連携')
src(6,'DMG MORI Condition Agent','https://www.dmgmori.co.jp/corporate/en/news/2026/20260706_conditionagent_e.html','対象機と2026年4月受注分からの標準提供。検索収録と既存根拠台帳で確認',published='2026-07-06')
src(7,'マザック JIMTOF2026','https://www.mazak.com/discover/jp-ja/jimtof2026/','工程集約・E1001・AI紹介動画の公開予定')
src(8,'オークマ JIMTOF2026','https://www.okuma.co.jp/english/show/jimtof/2026/','ARMROID・OMR20・Tower APC・AI and Intelligent Technologies')
src(9,'ファナック 新商品発表展示会2026','https://www.fanuc.co.jp/ja/profile/news/article/article33.html','FAコーナ デジタルで確認してから適用するフィジカルAI CNC')
src(10,'三菱電機 JIMTOF2026 出展案内','https://fa-site.mitsubishielectric.co.jp/fa/events-seminars/exhibitions/2026/jimtof2026/index.html','CNC・省人化ソリューションと実機展示なしの注記')
src(11,'NIDECグループ JIMTOF2026','https://www.nidec.com/jp/products/machine-tools/contents/machine-tool-jimtof2026/','TR-20W 切粉除去は参考出品・Nidec NC Twin')
src(12,'ジェイテクト JIMTOF2026','https://toyoda.jtekt.co.jp/jimtof2026/','Mill-Plan・ファインティーチレス・工場マネジメント')
src(13,'ミツトヨ JIMTOF特設サイト','https://www.mitutoyo.co.jp/jimtof/','MiSTARと加工機の連携・RA-Robot・品質管理DXセミナー')
src(14,'レニショー JIMTOF2024 Central紹介','https://www.renishaw.com/jp/renishaws-new-smart-manufacturing-data-platform-showcases-smart-factory-automation-at-imts-2024--48184','2024年時点のRenishaw Central展示',published='2024年の展示案内')
src(15,'Renishaw Centralと工程制御','https://www.renishaw.com/jp/smart-manufacturing-data-platform-for-industrial-process-control--47853','計測データ収集・処理・工程制御。既存根拠台帳も参照')
src(16,'Hexagon JIMTOF2026 国内初展示','https://prtimes.jp/main/html/rd/p/000000027.000148625.html','E2013・E7035・ProPlanAIとMAESTRO',published='2026-10-14')
src(17,'ESPRIT EDGE リリース履歴','https://hexagon.com/products/esprit-edge/release-highlights','2025.2 ProPlanAI導入・2026.1旋削等の商用拡張・2026.2も掲載')
src(18,'CloudNC Mastercam向け提供開始','https://www.cloudnc.com/news-room/cam-assist-the-first-ai-plug-in-for-cam-is-now-available-for-mastercam','3軸・3+2軸、北米販売を含む提供開始発表',published='2024-07-25')
src(19,'CloudNC CAM Assist for Mastercam','https://www.cloudnc.com/ja/mastercam','戦略生成とプログラマーの確認・調整。版と国内提供条件は現地確認')
src(20,'Beckhoff TwinCAT Chat','https://www.beckhoff.com/en-en/company/press/twincat-chat-using-innovative-chatbot-technology-in-twincat-engineering-2023-04.html','PLCコード作成支援の既存性',published='2023-04')
src(21,'Beckhoff CoAgent 技術発表','https://www.beckhoff.com/en-us/company/press/open-model-independent-ai-assistance-for-automation-programming-and-controls-engineering-2026-06.html','PLC・I/O・HMI、Operationsは今後の拡張との記載',published='2026-06-23')
src(22,'HACARUS Check ZERO 正式販売','https://hacarus.com/ja/press-release/20250707-news/','少量良品学習・追加学習。発売は2025年',published='2025-07-07')
src(23,'OPC UA情報モデルとAIエージェント','https://opcconnect.opcfoundation.org/2026/06/toward-realizing-ai-utilization-in-manufacturing-exploring-the-potential-of-integrating-the-opc-ua-information-model-with-ai-agents/','MCP Adapterは提供計画。既存台帳EDP-06と照合',published='2026-06')
src(24,'中村留 JIMTOF2026','https://www.nakamura-tome.co.jp/lp/jimtof2026/','RoboSync・既存台車／パレットの利用・E2027')
src(25,'パナソニック AI支援型遠隔操作の実証','https://news.panasonic.com/jp/press/jn260713-1','障害物停止時の人による遠隔回避。別会場の実証',published='2026-07-13')
src(26,'匠フォース AIエージェント発表','https://prtimes.jp/main/html/rd/p/000000031.000057137.html','引合受領から見積書作成・人の確認修正承認',published='2026-07-17')
src(27,'東京精密 JIMTOF2026','https://www.accretech.com/jp/product/measuring/event/20261026_jimtof.html','出展日程確認。具体展示内容の記載不足')
src(28,'松浦機械 JIMTOF2026','https://exhibition-matsuura.com/entrance/','MX-850T PC4・MX-520T PC7・GibbsCAM2026')

trends = [
dict(id='T1',title='生産準備と制御開発を支援するAI',short='生産準備AI',finding='AIの対象は検査だけでなく、工程案、CAM、見積、PLCやHMIの作成支援へ広がっている。',
 need='熟練者に集中する見積、工程設計、NC作成、制御プログラミングの負担を減らし、多品種への対応を速める。',
 past='2024年以前にもCAM自動化やAI支援は存在する。CloudNCは2024年7月にMastercam向けCAM Assistを発表し、Beckhoffも2023年にTwinCAT Chatを紹介している。',
 now='2026年の出展では、HexagonのProPlanAI、JBMのCAMAssist、BeckhoffのCoAgent、匠フォースなど、既存の業務環境に組み込む提案が並ぶ。ProPlanAIは2025.2で導入を説明し、2026.1で旋削・複合・スイス型へ商用範囲を拡張した。',
 mechanism='履歴学習による工程予測、加工戦略生成、自然言語からのコード案、図面認識と原価計算は異なる方式である。学習源、対象加工、必要な事前設定を分けて比較する。',
 implication='生成時間だけでなく、修正と検証を含む総準備時間、初回加工の合格率、履歴が少ない部品での対応力を見る。',
 limit='生成した案を採用して実機を動かすまでの自動化は製品ごとに異なる。海外版の機能と会場で利用できる国内版も照合が必要。',
 question='図面や3Dモデルから何が出力され、誰がどこで修正・承認するか。非対応部品では何が起きるか。',refs=['S16','S17','S18','S19','S20','S21','S26'],cards=['FC018','FC020','FC011','FC012','FC062']),
dict(id='T2',title='CNCとロボットに接続するフィジカルAI',short='フィジカルAI',finding='自然言語や状況認識をCNC・ロボットの作業へ接続する展示が具体化している。',
 need='教示・設定の負担や、切粉絡まりのように長時間運転を止める付帯作業を減らす。',
 past='2024年にもAIバラ積みピッキング、ロボット搬入出、デジタルツインは存在する。ロボットそのものが2026年に新登場したわけではない。',
 now='ファナックはフィジカルAI CNCと生成AIによるロボット駆動を掲げる。TAKISAWAはTR-20Wが切粉の絡まりを判断して除去する参考出品を予告。シマダマシンツールもAI段取り替えを記載するが、自動化する具体範囲の確認が必要。',
 mechanism='AIが認識・提案した結果を、仮想検証、機械指令、インターロックに接続する。ファナックの別の2026年展示報告では、デジタルで確認してから適用する構成を説明している。',
 implication='完成したデモの動きより、対象状態のばらつき、失敗検出、再試行、停止後の復帰、人の介入頻度が無人運転への寄与を左右する。',
 limit='参考出品・開発構想・商用製品を分ける。AI用途向け減速機やIPCは基盤・部品であり、自律作業を実現した機械とは数えない。',
 question='状況を変えた場合にも動作するか。判断できない時に何を停止し、誰がどの手順で復帰するか。',refs=['S09','S11','S02'],cards=['FC005','FC006','FC049','FC051','FC068','FC069']),
dict(id='T3',title='段取りと付帯作業を含めた自動化',short='段取りと付帯作業',finding='加工機への搬入出に加え、爪・工具交換、切粉回収、異形ワーク把持など、人手が残る仕事を扱う提案に注目する。',
 need='多品種少量生産では、機械が自動運転していても、段取り替え、工具補給、切粉処理で人が呼ばれる。',
 past='DMG森精機のAMR、オークマのARMROID・OMR20、松浦の多パレットとMiOS、牧野の自動化パッケージはいずれも2024年から存在する。',
 now='DMG森精機はGX Flexによるワーク・爪・工具交換、AMR 1000によるチップバケット搬送を紹介。中村留は既存台車を使うRoboSync、FUJIは異形・重量ワークの把持、ツガミはコレット交換と機外測定を含む自動化を展示予定。',
 mechanism='ロボット、パレット、交換機構、治具、工具管理、工程設計を組み合わせる。固定手順やメカ機構でも省人効果を生み、AI利用は必須条件ではない。',
 implication='切削時間やロボットの速度だけでなく、品種切替時間、必要な事前段取り、補充間隔、連続運転中の呼出し回数で比較する。',
 limit='搬送可能なことと、品種切替・復旧まで無人であることは別。半自動の重量物着脱も、完全自動と表示しない。',
 question='8時間の連続運転で、人が準備・補充・回収・復帰に使う時間はどれだけ残るか。',refs=['S05','S08','S24','S28'],cards=['FC001','FC002','FC008','FC042','FC045','FC046','FC047','FC048']),
dict(id='T4',title='計測と診断を加工判断へつなぐ品質管理',short='品質と状態診断',finding='計測の自動化に加え、加工へのフィードバック、工具の継続使用・交換判断、追加学習を含む運用が重要になっている。',
 need='検査待ち、工具摩耗の見逃し、過剰な工具交換、品質のばらつきを抑えたい。',
 past='Renishaw Central、ミツトヨの自動計測、工具摩耗判定や設備AI診断は2024年にも掲載されている。計測フィードバックそのものを2026年初の技術とは扱わない。',
 now='ミツトヨはMiSTARと加工機を接続する工程を提案。HexagonはMAESTROとPRESTO、ハイデンハインはVT 122のAI摩耗診断、モリマシナリーは寿命・交換時期提案を具体化。HACARUS Check ZEROは良品学習と追加学習を紹介する。',
 mechanism='寸法・画像・摩耗・稼働信号を取得し、判定、補正、交換提案へ返す。ルールによる補正、統計処理、学習AIの役割を分ける。',
 implication='検査精度と処理時間に加え、切粉・ミスト下の撮像、誤判定、補正上限、異常値の扱いを確認する。加工・測定双方を含む工程能力で評価する。',
 limit='Check ZEROは2025年発売。寿命予測も以前から研究されている。新しい展示名や国内初展示を、技術の初発明や全面的な自律品質保証とは解釈しない。',
 question='測定結果から何を自動変更するか。誤判定や測定不確かさで、過補正・過剰交換をどう防ぐか。',refs=['S13','S14','S15','S16','S22'],cards=['FC032','FC033','FC036','FC038','FC039','FC040','FC063']),
dict(id='T5',title='保全と工場運用を支援するDXとAI',short='工場運用DX',finding='可視化・記録の基盤に、保全支援、業務分析、遠隔介入を重ねる提案が見られる。',
 need='設備停止、記録の散在、旧設備からのデータ収集、現場ごとの管理方法の違いを減らしたい。',
 past='2024年にもFIELD system、OPC UA接続、設備AI診断、稼働可視化、生産管理が存在する。データを収集するだけで自律工場になるわけではない。',
 now='DMG森精機はCondition Agent、三菱電機は遠隔保守・スマート保全、ミロクリエは保全記録を使うAI支援を紹介。パナソニックはX-Area Remoteで複数設備の監視・操作を提案。SOFIXはミニ工場で連携構成を示す。',
 mechanism='既設設備のデータ取得、意味の統一、履歴管理を土台に、診断、計画、対処案、遠隔操作を接続する。情報の取得と設備への指令は別の権限として扱う。',
 implication='入力負担、異なるメーカーとの接続、現場で使う対処手順、呼出し削減、復旧時間で評価する。',
 limit='Condition Agentの名称だけで設備操作を行うエージェントとは判断しない。X-Area Remoteの別実証では、人が遠隔から障害物を回避しており、自動復帰の証拠にはしない。',
 question='アラーム後に、誰が判断し、誰が操作するか。既存MESや設備データをどこまで再利用できるか。',refs=['S05','S06','S10','S12','S25'],cards=['FC004','FC025','FC026','FC030','FC031','FC058','FC059','FC065','FC066']),
dict(id='T6',title='AIと実機を結ぶデータと仮想検証の基盤',short='データと仮想検証',finding='競争の比較軸として、AIモデル単体に加え、データの接続、検証、制御への組込みが重要になる。',
 need='生成結果が機械・工具・治具と整合しない問題や、シミュレーションと現物の差を減らす。',
 past='2024年にもSiemens Xcelerator・SINUMERIK ONE、Vericut、OPC UA情報モデルが存在し、仮想検証や接続基盤は継続したテーマである。',
 now='シーメンスは設計から品質保証までのDigital Thread、ニデックはNidec NC Twin、BeckhoffはMLモデルのPLC実装を提案。たけびしはAIエージェントとの連携シナリオを記載する。',
 mechanism='機械モデルと実機の設定、工具・材料・品種のデータをそろえ、シミュレーションで検証した結果を設備の許可された処理へ接続する。',
 implication='データをつなぐ費用、モデル更新工数、変更後の再検証、他社機との連携、操作ログを含めて比較する。',
 limit='接続規格やMCP対応は、任意の機械操作を安全に自動実行できる保証ではない。たけびしのMCP Adapterは、確認した記事では提供計画。国外のヒューマノイド実証とJIMTOFの展示機を同一視しない。',
 question='データの意味と版を誰が管理するか。生成案の仮想検証と、実機適用の承認をどこで行うか。',refs=['S03','S09','S17','S21','S23'],cards=['FC007','FC014','FC015','FC021','FC022','FC024']),
]

# Each tuple is a reviewed paraphrase, not a catalogue-text copy.
editorial = [
('DMG森精機','工作機械の大手','GX Flex、AMR、MATRIS WPH、DX Office','2024の工程集約・AMR・DXを継続し、搬送対象と爪・工具交換、保全までの構成を具体化。','工具交換と切粉回収を含む全体の無人時間。AIエージェントとCondition Agentの担当の違い。','A',['S05','S06']),
('ヤマザキマザック','工作機械の大手','INTEGREX、自動化、デジタル・AI連携','2024から工程集約と自動化を提案。2026はINTEGREXを軸に加工領域を拡張。AIの新機能差は要確認。','工程集約後の段取りと、AIが実際に変更する設定・加工条件。','A',['S07']),
('オークマ','工作機械の大手','ARMROID、OMR20、タワーAPC、OSP・AI知能化','ARMROID・OMR20は2024から継続。2026は新機種とAI・熱変位制御を訴求。','手動と自動の切替工数、品種切替、熱変位制御とAIの役割分担。','A',['S08']),
('牧野フライス製作所','工作機械の大手','MAS、生産ラインエンジニアリング、5軸・パレット','2024に自動化パッケージ。2026はライン全体とソフト・保守を含む提案を記載。','機械以外の段取り、再計画と停止復帰で人が担う仕事。','B',[]),
('ファナック','制御とソフトウェア','フィジカルAI CNC、生成AIロボット、Smart Digital Twin','2024のAIバラ積み・CNC・ツインに対し、2026は生成AIとフィジカルAIを明示。','提案から仮想検証、実機適用までの画面と承認点。','A',['S09']),
('三菱電機','制御とソフトウェア','CNC省人化、放電加工スケジューラ、遠隔保守','2024にもAI診断あり。2026は設計・加工・保守をつなぐ省人化を訴求。','CNCは最新案内で実機展示なし。資料と相談でAI機能・適用機・権限を確認。','A',['S10']),
('シーメンス','制御とソフトウェア','Digital Thread、SINUMERIK ONE、Heller Tokn、Equator','2024のXcelerator・NX・CNCから、2026は設計と品質保証をつなぐ構成を訴求。','CAD／CAM／測定データを接続する実際の手順と版管理。','A',[]),
('ジェイテクト','工作機械の大手','Mill-Plan、ファインティーチレス、工場マネジメント','2024の研削・操作支援に対し、2026は設備・人作業・情報・エネルギーを横断。','オフライン教示の現合修正をどれだけ減らせるか。','B',['S12']),
('ニデックマシンツール','工作機械の大手','Nidec NC Twin、門形・歯車加工','2024の機械・歯車ソリューションを継続。2026は大型機の仮想検証を具体化。','NC Twinの実機差と更新工数。TAKISAWAのAI展示と分けて見る。','B',['S11']),
('ニデックオーケーケー','工作機械の大手','VB-X650、パレット・拡張マガジン、GC53RⅡ','2024から5軸・自動化。2026は省人化オプションと研削自動化を具体記載。','工具・パレット容量と、有人段取りが残る範囲。','B',['S11']),
('ソディック','工作機械の大手','ワイヤ放電＋搬送、精密切削自動化、IoT','2024にもAMR・ワークチェンジャ。2026は機械と搬送・IoTの組合せを訴求。','放電と後工程をつなぐ段取り・電極やワイヤ関連の停止要因。','B',[]),
('アマダ','工作機械の大手','新型レーザ・バンドソー、DPG150、プレス自動化','2024にはAI-TASと自動計測補正を掲載。2026は5機種と省スペース化を訴求。','AI表記が減っても機能後退とは判断しない。計測・補正と段取り自動化を確認。','B',[]),
('ブラザー工業','精密加工と自動化','SPEEDIOの大容量工具搭載、5軸、PC-1','2024のNC機能・暖機レス支援から、2026は工具容量と多品種段取りを強調。','工具本数増加が補充・段取り時間をどれだけ変えるか。','B',[]),
('松浦機械製作所','精密加工と自動化','MX-520T PC7、MX-850T PC4、MiOS、GibbsCAM','2024から多パレット・MiOS4。2026は旋削と5軸の集約で加工対象を拡張。','MiOSで未完段取りをどう検知し、長時間運転の準備を完了するか。','B',['S28']),
('シチズンマシナリー','精密加工と自動化','FA-Friendly、ATC、自動計測、複合加工','2024からデジタルとFA支援。2026はATC・自動計測等の融合を訴求。','棒材交換以外の検査、刃具管理、切粉処理の有人作業。','B',[]),
('スター精密','精密加工と自動化','加工支援、ソフトウェア、ロボット部品加工','2024の医療向け実演から、2026はロボット・医療・ドローン・自動車の4分野。','ヒューマノイド部品の加工需要と、自社機でAIを使う機能を区別。','B',[]),
('ツガミ','精密加工と自動化','TMA8Fのコレット交換・機外測定、VA3Sの搬送','2024にも自動運転システム。2026は交換・計測・外段取りの実演を具体記載。','多品種の切替時、コレット・工具・測定プログラムを誰が設定するか。','B',[]),
('オーエスジー','工具と加工支援','MONOlithbox、Aブランド工具','2024にも工具自販機と省人化提案。2026は工具管理DXとして継続訴求。','工具在庫と加工計画・補充をどうつなぐか。','B',[]),
('三菱マテリアル','工具と加工支援','ヘッド交換式工具、加工ソリューション、再資源化','2024の工具・DX提案から、2026はリサイクル・ソリューション・新製品を重点化。','交換作業と工具寿命の安定化が無人運転に与える効果。AI機能は未確認。','B',[]),
('京セラ','工具と加工支援','VIMOA、EASY TOOL GUIDE、切削工具','2024からセンシングと工具選定。2026はVIMOAとCAM連携事例を具体記載。','検出後の停止・条件変更・工具交換までの接続範囲。','B',[]),
('タンガロイ','工具と加工支援','MATRIX 360、工具・自動化対応システム','2024の工具・コスト改善から、2026は工具管理と省人化も訴求。','使用実績と在庫・補充のつながり。AIとの関係は確認できない。','B',[]),
('ミツトヨ','計測と品質保証','MiSTARと加工機、RA-Robot、計測プラットフォーム','2024の自動測定・MiCATから、2026は加工から測定までの連携を具体化。','ワーク投入後に測定・判定・加工補正のどこまで自動で進むか。','A',['S13']),
('東京精密','計測と品質保証','精密測定機器の出展。具体的な2026展示は確認課題','一覧でE7044を確認。保存CSVの2026説明は空欄。2024の自動測定を今回予定に転用しない。','測定自動化、加工機接続、データ活用の出展機と実演時間を現地確認。','B',['S27']),
('レニショー','計測と品質保証','Renishaw Central、Equator、新プローブ','Centralは2024にも展示。2026は計測で自動化を支える提案を継続。','IPCの補正先・上限・不確かさ、他社機の接続を比較。','A',['S14','S15']),
('ハイデンハイン','計測と品質保証','VT 122、VTC 6.0のAI摩耗診断','2024にVT 122。2026は工具長とAI摩耗診断を具体記載。','摩耗診断が交換指示や自動交換までつながるか。','B',[]),
('ベッコフオートメーション','制御とソフトウェア','TwinCAT CoAgent、ML Creator、オープンCNC','2023からコード支援。2026はPLC・I/O・HMIと運用支援を訴求。2024展示詳細は不足。','国内提供版、EngineeringとOperationsの提供段階、実機変更の承認。','A',['S20','S21']),
('Hexagon Manufacturing Intelligence','制御とソフトウェア','E2013のProPlanAIとE7035のMAESTRO・PRESTO','2025.2でAI工程予測導入、2026.1で加工対象拡張。2026は国内初展示。2024同名照合は不足。','履歴の準備量、未経験部品の工程案、CAMと検査をつなぐデータ。','A',['S16','S17']),
('住友電気工業','工具と加工支援','SumiSmall、交換式ドリル、安定切粉処理','2024からセンシング・GX・DX。2026は安定加工、長寿命、資源制約への提案が中心。','切粉・欠損・交換負担を減らす条件。2026個別AI機能は未確認。','B',[]),
('中村留精密工業','精密加工と自動化','RoboSync、Protona、複合旋盤','2024にもロボットシステム。2026は既存台車利用と省スペースを具体化。','移設・品種切替の復旧工数、ストッカー不要の適用条件。','A',['S24']),
('FUJI','精密加工と自動化','異形ワーク把持、重量物の半自動着脱、Quist','2024からターンキーと工具管理。2026はつかみ方と難しいワークの扱いに焦点。','全自動と半自動を分け、重量・形状の適用範囲と残る人手を確認。','B',[]),
('TAKISAWA','精密加工と自動化','TR-20Wの切粉除去、工程集約、減速機部品加工','2024の搬入出用TR-20Wに対し、2026は状況判断を伴う切粉除去を参考出品。','除去失敗時の停止・再試行と、学習していない切粉への適応。','A',['S11']),
('オートデスク','制御とソフトウェア','Fusion、Fusion Manage、クラウド・PLM','2024からFusionとCAM自動化。2026はAIと製品データ・PLMの統合を強調。','個別AIタスク、必要ライセンス、データの持出しと検証工程。','B',[]),
('ニコン','計測と品質保証','NEXIV、CT、ロボットビジョン','2024からロボット測定・自動搬送・インライン検査。2026は計測と内部解析を横断。','検査工程とロボット動作の接続。2026の個別AI機能差は未確認。','B',[]),
]
majors = []
dossiers = json.loads((OUT/'major_dossiers.json').read_text(encoding='utf-8'))
for i,(target,group,exhibits,delta,question,priority,refs) in enumerate(editorial,1):
    d=next(r for r in dossiers if r['target']==target)
    sids=[]
    for year,urls in [(2026,d['urls_2026']),(2024,d['urls_2024'])]:
        for j,url in enumerate(urls,1):
            sid=f'C{i:02}-{year}-{j}'
            sources.append(dict(id=sid,title=f"{d['company']} {year}公式出展説明",url=url,locator='出展説明・主な出展物',checked='2026-10-16',published=f'{year}開催分'))
            sids.append(sid)
    majors.append(dict(id=f'M{i:02}',company=d['company'],name=target,group=group,booths=d['booths'],exhibits=exhibits,delta=delta,question=question,priority=priority,refs=refs+sids,has_text_2026=bool(d['text_2026'])))

visits=[]
def visit(target,why,ask,mins=30):
    c=next(m for m in majors if m['name']==target)
    visits.append(dict(id=f'V{len(visits)+1:02}',company=c['company'],name=target,booths=c['booths'],why=why,ask=ask,minutes=mins,status='展示予定・現地未確認',refs=c['refs']))
visit('ファナック','CNCとロボットの両方で生成AIの判断と実行の境界を比較できる。','プロンプトから仮想検証、実機指令までを見せてもらい、承認・停止点を確認。',45)
visit('DMG森精機','工程集約、工具・爪交換、AMR、保全を含む連携の広さを確認できる。','ワーク以外の工具・切粉・保全に残る有人作業を一つの運転シナリオで確認。',45)
visit('オークマ','機内ロボット・移動式協働ロボット・APCを比較できる。','品種切替の準備時間、手動への切替、AI知能化の実際の担当を確認。',35)
visit('ヤマザキマザック','工程集約と自動化・デジタル・AIを組み合わせる大手の基準点。','機械ごとのAI機能と、段取り・プログラム作成をどこまで省けるか確認。',35)
visit('Hexagon Manufacturing Intelligence','CAMの履歴学習と品質自動化を別ブースで比較できる。','E2013では履歴不足時の工程案、E7035では測定から工程改善へのデータ経路。',60)
visit('ベッコフオートメーション','生成AI支援とリアルタイム制御へのAI実装を同時に比較できる。','CoAgentの国内提供段階、I/OやHMIの反映、変更承認と復帰を確認。',30)
visit('TAKISAWA','長時間無人運転を止める切粉絡まりを扱う具体的なAI参考出品。','想定と違う切粉を提示した時の検出・除去・失敗復帰。参考出品から製品化への条件。',30)
visit('ミツトヨ','加工と測定をつなぐ自動化を確認し、AI以外の有効な方式と比較できる。','MiSTAR連携の対象工程、合否後の自動補正と人の判断範囲。',30)
visit('レニショー','2024から継続する計測フィードバックの成熟した比較対象。','CentralとIPCの接続条件、補正上限、測定異常の扱い。',25)
visit('シーメンス','設計・加工・品質保証をつなぐデータの経路を確認できる。','実機とモデルの変更同期、部品・工具・測定データの版管理。',30)
visit('三菱電機','加工から保守までの省人化と、AI診断・運用ソリューションを比較できる。','CNCは実機展示なし。資料と相談で具体機能・対象機・自動変更範囲を確認。',25)
visit('中村留精密工業','既存設備へ導入する際のレイアウトと段取り負担を比較できる。','台車・パレットの適用条件と、移設・品種変更後の復旧操作。',25)

for cid,why,ask in [
('FC020','CAMの自動生成を履歴学習型ProPlanAIと比較する。','生成前の工具・材種・保持条件設定と、出力後の修正・NC検証に要する時間。'),
('FC036','少量良品学習と追加学習の運用を見る。','油汚れや撮像変動を含む見逃し・過検出、更新後の独立評価。'),
('FC040','工具摩耗の検出から交換時期提案までの広がりを見る。','材種・加工条件が変わる時の寿命予測と、実機展示範囲。'),
('FC024','設備データをAIエージェントに渡す接続基盤を確認する。','MCP Adapterの提供状況、情報モデル、読出しと書込みの権限。'),
('FC031','複数設備の監視と遠隔介入の運用を確認する。','停止時の人の介入回数と、通信遅延・切断時の安全停止。'),
('FC062','機械外の業務AIが、現場知識をどう再利用するか確認する。','見積の根拠、担当者の修正・承認、再学習に必要な案件数。'),
('FC063','AIの前提となる機内撮像の安定性を見る。','ミスト・油・切粉条件、視界不良時の誤判定と清掃・保守。'),
]:
    c=cardmap[cid]
    visits.append(dict(id=f'V{len(visits)+1:02}',company=c['company'],name=c['company'],booths=c['booths_2026'] if isinstance(c['booths_2026'],list) else [c['booths_2026']],why=why,ask=ask,minutes=25,status='展示予定・現地未確認。'+('ツールソムリエは実機出展なし。対象はアナライザー。' if cid=='FC040' else ''),refs=c['evidence_ids'],card_id=cid))

# Import only evidence referenced by curated cases, without copying source prose.
ledger=json.loads((ROOT/'data/research/technology_atlas_v1/evidence_ledger.json').read_text(encoding='utf-8'))
if isinstance(ledger,dict):
    ledger=list(ledger.values())
for c in [cardmap[cid] for t in trends for cid in t['cards']]+[cardmap[v['card_id']] for v in visits if 'card_id' in v]:
    for eid in c['evidence_ids']:
        if any(s['id']==eid for s in sources):continue
        e=next((e for e in ledger if e.get('evidence_id')==eid),None)
        if e:
            sources.append(dict(id=eid,title=e.get('title',eid),url=e['url'],locator=e.get('locator',e.get('evidence_locator','原典該当機能')),checked=e.get('checked_date','2026-10-16'),published=str(e.get('year',''))+'年資料'))

review=[]
exclusions={2024:{'YEU LIAN ELECTRONICS CO., LTD.':'AI/AOはアナログ入出力の文脈。人工知能の証拠としない。'},2026:{'三旺株式会社':'供給対象の産業・用途としてのAI。自社のAI機能は特定できない。','西部電機株式会社':'AI関連分野は加工対象の需要。AI実装機能の証拠ではない。','Formnext':'セミナーのAI翻訳。加工・製造AIの展示件数に含めない。','Theta Precision Co., Ltd.':'AI産業向けスピンドルの需要。自社のAI機能の証拠ではない。','WALSIN LIHWA CORPORATION':'AIサーバー向け材料。製造工程でAIを使うという説明ではない。'}}
for r in corpus:
    if 'AI明示' not in r['tags']:continue
    exc=exclusions[r['year']].get(r['company'])
    review.append(dict(year=r['year'],company=r['company'],decision='技術件数から除外' if exc else '関連提案候補として保持',reason=exc or 'AIを含む製品・サービス・研究開発・基盤の提案。実装確定／性能確認の件数とはしない。',source_urls=r['urls']))

report=dict(title='JIMTOF2026 AIと自動化の動向調査',date='2026-10-19',catalogue_date='2026-10-16',census=json.loads((OUT/'census.json').read_text(encoding='utf-8')),sources=sources,trends=trends,majors=majors,visits=visits,ai_review=review,
 findings=[
 'AIの訴求は全体集計と同名企業の比較の両方で増えている。生産準備、制御開発、運用支援が具体的な比較対象になっている。',
 '自動化は2024からの継続が大きい。2026では爪・工具交換、切粉処理、計測連携など、人手が残る対象作業と構成の広がりを比較する。',
 'フィジカルAIとエージェントは注目テーマだが、参考出品、提供予定、基盤・部品を含む。商用の自律工場が一般化したとは判断できない。',
 '視察では生成・判定のデモに加え、実機適用の検証、承認、例外復帰までを確認すると、導入判断に必要な差が見える。'],
 route=[
 dict(day='1日目 東展示棟',blocks=[('10:00〜11:15','東1','マザック E1001、牧野 E1024を比較。工程集約とライン自動化の違いを確認。'),('11:15〜12:30','東2','Hexagon CAM E2013、JBM E2002、Beckhoff E2028。生成案と検証を比較。'),('13:15〜14:30','東3','オークマ E3028、TAKISAWA E3013、シーメンス E3006。'),('14:30〜15:30','東7','ミツトヨ E7085、レニショー E7089。必要に応じHexagon品質 E7035。'),('15:45〜16:45','東8','DMG森精機 E8005。関心に応じジェイテクト E8003、ニデックの詳細は東3で確認。')]),
 dict(day='2日目 南と西展示棟',blocks=[('10:00〜11:30','南2','ファナック S2001、三菱電機 S2003。必要に応じシチズン S2002。'),('11:30〜12:30','南1','HACARUS／日東商事 S1031。検査と追加学習の運用を確認。'),('13:15〜14:30','南3','匠技研 S3011、たけびし S3015、モリ S3048、興和 S3104から関心の高い2件を選択。'),('14:45〜15:45','西','OSG W1070、京セラ W1046等で工具管理と監視。遠隔管制はパナソニック W3086。'),('16:00〜16:45','再訪または南4','重要な未回答を再確認。きさげロボット企画は南4。移動時間を優先して調整。')])],
 one_day='1日しかない場合は東と南に絞り、マザック、Hexagon CAM、Beckhoff、オークマ、TAKISAWA、DMG森精機、ファナックを中心に、計測はミツトヨかレニショーのどちらかを選ぶ。西の工具・周辺は別担当または事前資料で補完する。',
 questions=[('生産準備AI','生成時間、修正時間、検証時間、初回加工合格率','図面不足、未知形状、工具欠品で何が起きるか。'),('ロボットと付帯作業','品種切替時間、連続運転時間、介入回数','切粉形状やワーク位置が変わると、再試行と停止はどう変わるか。'),('計測と補正','見逃し率、過検出率、測定時間、工程能力','補正上限、測定異常、油汚れをどう扱うか。'),('保全と工場DX','入力時間、接続工数、停止時間、復旧時間','診断後の操作・修理を誰が担うか。'),('データと制御基盤','モデル更新工数、実機差、ログ、再検証時間','生成案と実機の設定の版を、どう一致させるか。')])
(OUT/'report_content.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'ai_context_review.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(review[0]));w.writeheader();w.writerows(review)
print(json.dumps({'majors':len(majors),'visits':len(visits),'trends':len(trends),'sources':len(sources),'reviewed_ai_wording':len(review)},ensure_ascii=False))
