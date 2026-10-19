"""Task-level research cards and a standalone visual atlas; preserve prior reports."""
import csv, hashlib, html, json
from collections import Counter
from pathlib import Path
from technology_categories import build_category_index
from expand_candidate_research import expand_candidates
from category_visit_priorities import build_priorities
from category_priority_html import priority_section,screening_section,PRIORITY_JS
from category_priority_html import roles_section,ROLES_JS
from priority_deepening import apply_deepening
from cross_company_synthesis import build_synthesis,draw_figures,synthesis_html
from remaining_research_followup import apply_followup,enrich_synthesis,followup_html

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/research/overview_v0'
OUT=ROOT/'data/research/technology_atlas_v1'
OUT.mkdir(parents=True,exist_ok=True)
load=lambda n:json.loads((BASE/n).read_text(encoding='utf-8'))
reviews={r['review_id']:r for r in load('company_comparison.json')}
evidence={r['evidence_id']:r for r in load('evidence_ledger.json')}
dossiers={r['review_id']:r for r in load('review_dossiers.json')}

# Additional companies found while rereading every 2026 mention of physical AI / agents.
detail_data={str(y):json.loads((ROOT/'data'/f'exhibitor_details_{y}.json').read_text(encoding='utf-8')) for y in (2024,2026)}
extra_companies=[
 (43,'三菱電機','加工監視・自動化運用・保守の負担'),
 (44,'三菱商事テクノス','ロボットと搬送機の分断・工程間の停止'),
 (45,'ケーメックス・オートメーション','配線・制御盤の工数と現場データ処理基盤'),
 (46,'テクノダイナミックス','高精度・高剛性の動力伝達要素'),
]
for number,name,need in extra_companies:
 vid=f'V{number:03}'
 ds={y:[r for r in rs if name in r['company_name']] for y,rs in detail_data.items()}
 assert len(ds['2026'])==1 and len(ds['2024'])==1
 dossiers[vid]=dict(review_id=vid,selection=name,years=ds)
 ids={}
 for y,rs in ds.items():
  ids[y]=[]
  for k,r in enumerate(rs,1):
   eid=f'EAT-{vid}-{y}-{k}';ids[y].append(eid)
   evidence[eid]=dict(evidence_id=eid,publisher=r['company_name'],year=int(y),title=f'JIMTOF{y}公式カタログ：{r["company_name"]}',url=r['detail_url'],locator='出展紹介・主な出展物（カードの製品名・機能語で検索）',checked_date='2026-10-16',published_date='未記載',evidence_type='公式掲載の出展者記述・メーカー主張',exhibition_certainty='2026展示予定・現地未確認' if y=='2026' else '2024当時の説明・事後実演確認ではない',source_record_id=r['exhibitor_record_id'],cache_path=r['cache_path'],source_excerpt='個別カードの2024・2026要旨を参照')
 reviews[vid]=dict(review_id=vid,company=name,customer_need=need,evidence_2024=ids['2024'],evidence_2026=ids['2026'],booths_2026=[r['booth'] for r in ds['2026']],limitations='適用条件・操作権限・現場効果・採用実績は未確認')

# New primary-source observations, checked with web tools on 2026-10-16.
web=[
 ('N01','ニデック','JIMTOF2026 TR-20W','https://www.nidec.com/jp/products/machine-tools/contents/machine-tool-jimtof2026/','TR-20W：フィジカルAI搭載のロボットシステム（参考出品）','台車型TR-20Wで、主軸に絡んだ切粉を認識・判断して除去する参考デモを予告。','2026展示予定・参考出品'),
 ('N02','ニデック','MGC300開発発表','https://www.nidec.com/jp/product/news/2024/news1101-03/','2024年11月1日／MGC300の出展説明','2024出展で台車型TR-20Wによるワーク搬入・搬出の自動化デモを予告。','2024当時の予定説明'),
 ('N03','Beckhoff','CoAgent for Engineering TE1700','https://www.beckhoff.com/ko-kr/products/automation/twincat/texxxx-twincat-3-engineering/te1700.html','Features／Product status','自然言語とプロジェクト文脈からPLCコード、I/O構成、HMI設計を提案。製品発表段階、投入時期は問い合わせ。','製品発表・市場投入時期要問い合わせ'),
 ('N04','Beckhoff','CoAgent for Operations TF1700','https://www.beckhoff.com/ko-kr/products/automation/twincat/tfxxxx-twincat-3-functions/tf1xxx-system/tf1700.html','Properties／Product status','実データ・ログによる診断、独自文書の参照、チャットからTwinCATコマンドや可視化照会の実行を説明。投入時期要問い合わせ。','製品発表・市場投入時期要問い合わせ'),
 ('N05','Beckhoff','TwinCAT projects with AI-assisted engineering','https://www.beckhoff.com/ko-kr/products/automation/twincat-projects-with-ai-supported-engineering/','CoAgents for development and machine operation','開発はXAE Shell、運用はHMIへ統合。運用データはADS／Analytics Loggerから参照。専門家が制御権を保持。','製品群の方式説明。日本展示版の範囲は別確認'),
 ('N06','Eplan','Eplan Copilot','https://www.eplan.com/us-en/about-us/innovations/eplan-copilot/','Based on a described task／Looking ahead／conceptual phase','現行説明は文脈に応じた回答・推奨・手順。自動操作は将来機能。盤レイアウト自動生成の例は構想段階。','現行支援と将来構想を分離'),
 ('N07','DMG森精機','Condition Agent 提供開始','https://www.dmgmori.co.jp/corporate/news/2026/20260706_conditionagent.html','2026/07/06本文・主な特長','診断用NCのデータと設計・製造知識をクラウドAIで分析しmy DMG MORIへ表示。2026年4月受注分から対象機標準。','提供開始。JIMTOFの汎用的エージェント記述と同一かは未確認'),
 ('N08','ヤマザキマザック','JIMTOF2026 Machines & Automation Systems','https://www.mazak.com/jp-en/news-media/upcoming-events/jimtof2026/','Machines & Automation Systems／Automation Systems','INTEGREX i-250S NEO＋Ez LOADER 30、VARIAXIS C-700＋拡張式パレットチェンジャを出展予定。','2026展示予定。AI機能の方式説明はない'),
]
for i,p,t,u,l,s,c in web:
 evidence['EAT-'+i]=dict(evidence_id='EAT-'+i,publisher=p,year=2024 if i=='N02' else 2026,title=t,url=u,locator=l,checked_date='2026-10-16',published_date='2024-11-01' if i=='N02' else '2026-07-06' if i=='N07' else '未記載',evidence_type='企業公式説明・メーカー主張',exhibition_certainty=c,source_excerpt=s,cache_path='',retrieval_note='webで該当箇所を確認。観察要旨を本台帳へ保存。ウェブ全文のキャッシュではない。')

phase_names=['受注・加工準備','制御開発・立上げ','段取り・搬送','加工・状態監視','検査・工具運用','工場運用・保全','共通の実装基盤・要素']
task_specs=[
 ('01',0,'図面検索・見積・調達','図面・原価・調達情報から業務を進める'),
 ('02',0,'工程設計','形状と加工履歴から加工工程を組む'),
 ('03',0,'治具設計','固定方法・クランプ構成を決める'),
 ('04',0,'CAM・NC作成','工具経路・加工プログラムを準備する'),
 ('05',0,'NC・干渉検証','実行前に衝突や削り過ぎを確認する'),
 ('06',1,'PLCコード作成','制御要求をプログラムへ変換する'),
 ('07',1,'I/O・HMI設計','機器構成と操作画面を設計する'),
 ('08',1,'学習モデル実装','学習モデルを機械制御へ組み込む'),
 ('09',1,'教示・位置合わせ','移設・再設置後の位置関係を合わせる'),
 ('10',2,'ワーク固定','治具をクランプ・アンクランプする'),
 ('11',2,'指・ハンド交換','品種に合わせて把持部を交換する'),
 ('12',2,'ワーク搬入出','素材・加工品を機械へ受け渡す'),
 ('13',2,'パレット供給','パレットを交換・保管・供給する'),
 ('14',2,'工場内搬送','部品・切粉容器などを移動する'),
 ('15',3,'加工信号解析','加工中のセンサ・制御信号を評価する'),
 ('16',3,'加工条件・NC最適化','加工負荷や条件を調整する'),
 ('17',3,'切粉処理','切粉を洗浄・認識・除去する'),
 ('18',3,'熱変位補正','温度等に伴う加工誤差を補正する'),
 ('19',4,'外観検査','表面のキズ・欠け等を検出する'),
 ('20',4,'寸法・形状計測','ワークの寸法や形状を測定する'),
 ('21',4,'測定から加工へ補正','測定結果を工具オフセットや加工へ戻す'),
 ('22',4,'刃先・摩耗判定','工具の欠け・摩耗状態を判断する'),
 ('23',4,'工具寿命・交換提案','摩耗履歴から交換時期を決める'),
 ('24',4,'工具在庫・供給','所在・入出庫・工具供給を管理する'),
 ('25',5,'生産・品質・在庫管理','工程情報と実績を結びつける'),
 ('26',5,'計画変更・負荷調整','進捗と制約を基に予定を変更する'),
 ('27',5,'異機種・旧設備の接続','設備データを取得し意味をそろえる'),
 ('28',5,'遠隔操作・例外対応','停止・エラーを遠隔から人が解消する'),
 ('29',5,'保全診断・知識支援','異常の原因と対処を調べる'),
 ('30',5,'潤滑・主軸状態管理','主軸を監視し潤滑等を調整する'),
 ('31',3,'過酷環境の撮像','油・切粉・ミスト下で画像を取得する'),
 ('32',0,'設計製造データ連携','CAD・CAM・PLM等の情報をつなぐ'),
 ('33',6,'駆動・動力伝達要素','AIが判断するための機能と機構部品の役割を区別する'),
 ('34',6,'IPC・分散I/O基盤','データ取得・処理と配線の実装を支える'),
 ('00',6,'担当タスク未特定','具体的に何の仕事を担うかを原典で補う'),
]
tasks={i:dict(task_id='TASK'+i,phase=phase_names[p],phase_index=p,task=n,purpose=g) for i,p,n,g in task_specs}
cards=[]
def add(v,t,n,dep,robot,inp,method,out,boundary,before,after,delta,roles,stage='2026展示予定・提供段階未確認',web_ids=(),question=''):
 r=reviews['V'+str(v).zfill(3)]
 # Original catalogue evidence supports exhibition presence; web evidence supports named mechanisms only.
 es=r['evidence_2024']+r['evidence_2026']+['EAT-'+w if w.startswith('N') else 'EOV-'+w for w in web_ids]
 if v==1:es=[e for e in es if 'V001-2024-2' not in e] # Additive booth is unrelated to these cards.
 if v==7:es=[e for e in es if ('V007-2026-1' not in e if t=='02' else 'V007-2026-2' not in e)]
 cid=f'FC{len(cards)+1:03}'
 cards.append(dict(card_id=cid,review_id=r['review_id'],company=r['company'],item=n,task_id='TASK'+t,phase=tasks[t]['phase'],task=tasks[t]['task'],customer_need=r['customer_need'],need_classification='調査者による課題整理（原典説明を基に分析）',deployment=dep,robot_form=robot,input=inp,mechanism=method,output=out,human_boundary=boundary,baseline_2024=before,observation_2026=after,delta_type=delta,delta_interpretation='出展説明・公式資料の記載比較。初発明年・実演成功・性能向上を証明するものではない。',roles=roles.split('/'),product_stage=stage,exhibition_status='個別JIMTOF展示未確認・企業公式製品資料のみ' if n=='Condition Agent' else '2026は動画・資料展示、実機なし' if n=='ツールソムリエ' else 'JIMTOF2026公式カタログ掲載・現地未確認',evidence_ids=es,booths_2026=r['booths_2026'],unresolved=question or r['limitations'],adoption_and_market='採用件数・受注・市場規模は本カードでは未確認',checked_date='2026-10-16'))

# Roles denote the described function, never a maturity ranking.
add(1,'14','AMR 1000','工場通路・チップバケット搬送','自律走行搬送ロボット','チップバケット等。認識センサ・経路入力は未記載','AMRで切粉容器等を運搬','容器の工場内搬送','積み降ろし・通路障害・異常時の介入条件は未確認','AMR 2000／WH-AMR 10を掲載','AMR 1000とチップバケット搬送を具体記載','搬送対象・構成の追加記載','動作',question='容器の受渡しも自動か。混雑・位置ずれ・満杯時に誰が対応するか。')
add(1,'13','MATRIS WPH 210','工作機械周辺の供給セル','ワーク＆パレットハンドリングシステム。関節構成未確認','ワークとパレット、品種別段取り条件','ワークとパレット両方を供給する変種変量生産向け構成','工作機械への供給','把持・治具・品種切替の事前準備範囲は未確認','PH Cell 500、MATRIS Light、Robo2Go Millingを掲載','MATRIS WPH 210を日本初公開と記載','搬送対象・構成の追加記載','動作')
add(1,'29','工作機械へのAIエージェント実装（名称・担当不明）','工作機械。CNC／HMI／クラウドの位置は未記載','ロボットではない／具体対象未確認','未記載','AIエージェント実装との記述のみ','具体的に助ける仕事は未記載','助言・操作・承認の境界が不明','MXとデータ収集・可視化・分析を掲載','AIエージェント実装を明記','2026具体化・機能差未確定','未特定',question='製品名、実装先、ユーザーの依頼例、実行する操作と承認点を実演で確認する。')
add(1,'29','Condition Agent','診断NC→クラウド解析→my DMG MORI','工作機械の主軸・送り軸・ATC・APCが診断対象','診断専用NC動作のデータ、設計・製造データ','クラウドAIで異常兆候を分析','コンポーネント状態の診断・通知','現場操作で診断開始。修理・部品交換まで自律実行する説明なし','2024カタログから同サービスの機能は比較できない','2026年4月受注分から対象機標準。従来WALC CAREの診断対象・分析を拡張との公式説明','2024個別比較不能','認識/判断','提供開始・対応機限定',('N07',),'診断頻度、誤警報、後付け対象機、診断後の保全意思決定。名称だけで生成AIエージェントに分類しない。')
add(2,'12','生成AIによるロボット駆動','ロボットのオープンプラットフォーム','ファナックロボット。展示対象機種・軸構成は未特定','生成AI利用との記述。音声・画像等の入力は未記載','生成AIをロボット駆動へ利用する事例','具体的な搬送・組付け等のタスクは未特定','許可動作、教示、停止、承認は未確認','AI高速バラ積み、協働ロボット、ROBOGUIDEを掲載','生成AI駆動・フィジカルAI・オープンプラットフォームを明記','2026具体化・機能差未確定','動作',question='どのロボットが何を動かすか。指示→動作生成→検証→実行の分担と対応できない作業は。')
add(2,'16','フィジカルAI CNC','CNC','工作機械の制御装置。ロボット本体ではない','未記載','知的作業を安全に自動化するとのメーカー説明','担当する知的作業の例は未記載','自動変更できるパラメータ・承認・安全確認は未確認','Series 500i-A、段取り支援、Smart Digital Twinを掲載','フィジカルAI CNCを明記','2026具体化・機能差未確定','未特定')
add(2,'05','FANUC Smart Digital Twin','加工前の仮想機械環境','デジタル上の工作機械','機械・サーボのモデル。詳細入力未確認','加工前の挙動確認を支援','実機前の検討・検証','モデルと実機の一致、検証外事象への対処は未確認','Smart Digital Twinを掲載','同名製品を継続掲載','2024から継続','認識/判断')
add(3,'12','ARMROID／OMR20','複合加工機内／工作機械横','ビルトインロボット／移動式協働ロボット','ワークと品種別プログラム。AI知覚方式は未記載','機内・移動式のロボットで自動化を構成','加工機とのワーク受渡し等。各機の展示動作は未確認','手作業とロボット運用の切替、品種切替の介入範囲を要確認','ARMROID、OMR20、smarTwinCELLを掲載','ARMROIDとLB3000 EX III＋OMR20等を掲載','2024から継続','動作',question='機内型と移動式の使い分け、再配置・品種変更・切粉処理の負担を比較する。')
add(3,'18','熱変位制御・AI知能化','工作機械の加工制御','工作機械','熱状態等。具体センサ・AI入力は未記載','独自の熱変位制御とAI活用を説明。両者の方式関係は不明','加工品質維持を支援','自動補正範囲と校正・学習条件は未確認','知能化技術・Green-Smart Machineを掲載','熱変位制御とAIを具体記載','2026具体化・機能差未確定','判断/動作')
add(4,'12','INTEGREX＋Ez LOADER 30','INTEGREX i-250S NEO周辺','Ez LOADER 30。今回確認資料ではロボット詳細未確認','ワーク・搬送プログラムの具体仕様未確認','工作機械とローダの組合せ','自動化セルのワーク供給。展示動作は要確認','AIに任せる判断範囲は資料から確認できない','自動化トータルサポートを訴求。今回構成の直接比較は不可','メーカー特設ページで機械・ローダ組合せを確認','2026具体化・機能差未確定','動作',web_ids=('N08',))
add(5,'06','TwinCAT CoAgent for Engineering：PLC','TwinCAT 3 XAE Shell','ソフトウェア支援','自然言語の要求、既存プロジェクト構造、ライブラリ・文書','文脈に基づくPLC Structured Text等のコード提案','コード案・最適化・文書化','専門家が制御権を保持。実機書込み・妥当性検証の自動範囲は未確認','同名の2024詳細を取得できず比較不能','2026カタログはPLC支援を掲載。製品ページで実装先・入出力を確認','2024個別比較不能','判断','製品発表・投入時期要問い合わせ',('N03','N05'),'生成コードの検証・修正・採用、実機ダウンロードの各権限は。')
add(5,'07','TwinCAT CoAgent for Engineering：I/O・HMI','TwinCAT開発環境','ソフトウェア支援','チャット要求、画面スケッチ、プロジェクト文脈','I/O構成・HMIレイアウトを提案','構成案・画面案','採用・修正・動作確認の自動化範囲は未確認','2024詳細不足','2026のHMI支援記述を製品ページのI/O・画面設計で具体化','2024個別比較不能','判断','製品発表・投入時期要問い合わせ',('N03',))
add(5,'29','TwinCAT CoAgent for Operations','TwinCAT HMI。ADS／Analytics Loggerで運転データ参照','ソフトウェア支援','ライブ変数、ログ、KPI、アラーム、独自マニュアル','症状から仮説・データ照合・診断と対処案を作成。チャットからコマンド実行も説明','診断・作業手順・レポート・TwinCATコマンド','専門家が制御権を保持。コマンド許可・承認・操作上限は未確認','2024詳細不足','一般的なアラーム対策支援をHMI・データ接続・実行機能へ具体化','2024個別比較不能','認識/判断/動作','製品発表・投入時期要問い合わせ',('N04','N05'),'参照専用と書込み操作をどう区別するか。診断結果を再確認するループと失敗時の停止条件は。')
add(5,'08','TwinCAT Machine Learning Creator','モデル開発→ONNX／PLCパイプライン','ソフトウェア開発ツール','画像・時系列等の学習データ。用途ごとに設定','モデルを自動構築・最適化し制御側へ実装','制御で利用する学習モデル','学習データ、目的、評価・再学習はエンジニアが設定。対話エージェントとは別機能','2024詳細不足','2026はノーコードでAI作成しPLC実装と記載','2024個別比較不能','判断','既存製品方式確認・2026掲載',('W01',))
add(5,'15','TwinCAT CNC：切削信号の解析・独自制御','PCベースCNCリアルタイム環境','工作機械・CNC','多様なセンサ信号・制御情報','高速サンプリング・FFT・C++／Simulinkの独自ロジックを接続','切削状態モニタリング・独自CNCフィードバック','制御ロジック設計・安定性確認・機種適合は開発者の範囲。AI使用は必須ではない','2024詳細不足','2026は3つの機能開発事例を具体記載','2024個別比較不能','認識/判断/動作')
add(6,'32','Eplan P8／Pro Panel','電気設計→3D制御盤設計→製造','設計ソフトウェア','回路図・部品・接続・3D盤データ','設計資産の標準化・再利用と製造データの一貫化','回路・帳票・盤設計データ','設計判断・最終承認を自律化する説明ではない','電気設計から盤製造までのデータ接続を掲載','同じデータ中心の設計製造連携を掲載','2024から継続','判断')
add(6,'07','Eplan Copilot','Eplan Platform上の対話インタフェース','ソフトウェア支援','自然言語の作業要求・設計知識と操作文脈','文脈に応じた回答・推奨・段階的操作手順','知識検索・操作支援','自動操作は将来機能。自動盤レイアウト例は構想段階と公式明記','2024はデータ連携・3D盤設計','2026はCopilotによる知識・操作支援を追加記載','担当タスクの追加記載','判断','支援機能紹介。自動操作・盤レイアウト自動生成は将来構想',('N06',),'現在利用できる操作を実演で区切る。構想段階の効果見込みを現行成果に含めない。')
add(7,'02','ESPRIT EDGE ProPlanAI','CAMの工程計画','ソフトウェア支援','過去の加工ジョブ、形状特徴、PMI等','過去ジョブから加工工程を予測し計画へ利用','加工工程の提案・再利用','未学習形状・機種差・承認・NC検証との接続は要確認','同名2024詳細なし。別名称・旧法人との照合は未完了','2025.2で導入説明、2026.1で旋削・複合・スイス型の商用範囲を説明','2024個別比較不能','判断','メーカーが商用提供範囲を説明・顧客実績未確認',('W02',))
add(7,'20','MAESTRO／PRESTO／品質ソフト群','測定・自動検査・品質解析','三次元測定機／自動検査ステーション','寸法・形状・CT・品質データ','測定機とPC-DMIS、VG、Q-Das等を紹介','測定・解析・品質情報','個々の測定から加工への自動補正接続は未確認','同名2024詳細なし','2026品質ブースで測定・検査・解析から工程改善を訴求','2024個別比較不能','認識/判断')
add(8,'04','Mastercam＋CAMAssist','CAMプログラミング','ソフトウェア支援','加工形状・工具等。AIの参照データは未記載','CAMAssistで従来手作業だったCAM工程を自動化すると説明','CAM準備作業の支援','対象加工・自動化範囲・人の修正と検証は未確認','Mastercamと工具・ホルダ連携を掲載','CAMAssistの手作業自動化を追加記載','担当タスクの追加記載','判断')
add(9,'05','Vericut：Gコード検証','加工前のデジタル機械環境','機械・工具・治具・ワークの仮想モデル','実行NC、工具・治具・ワーク・機械モデル','干渉・削り過ぎ・削り残しをシミュレーション','実行前の不具合検出','モデルの更新・入力一致・検証結果の採否が必要','同方式に加えCNCプリチェック・実機モニターまで説明','検証・デジタルツインを継続掲載','2024から継続','認識/判断')
add(9,'16','Vericut Force／Optimizer','NCプログラム最適化','ソフトウェア','NCと刃物負荷等の加工モデル','負荷を考慮してNCを最適化','最適化されたNC','AIの新機能・従来版の性能差・実機適用条件は未確認','Forceによる刃物負荷最適化を掲載','AI活用・独立Optimizerを掲載するが具体方式差は不足','2026具体化・機能差未確定','判断')
add(10,'32','Fusion／FeatureCAM／PLM連携','設計・CAM・製造データ基盤','クラウドソフトウェア','設計モデル・加工・製造関連データ','CAD/CAMとPLM・AI支援を組み合わせる提案','設計製造の情報連携','AIが担当する具体タスクと自動確定範囲は未確認','クラウドFusionとFeatureCAM自動プログラミングを掲載','AI・PLMを強調。個別AI方式の比較はできない','2026具体化・機能差未確定','判断')
add(11,'27','OPC UA情報モデルとエージェント連携','制御機器→OPCサーバー→上位システム','通信ソフトウェア','PLC・CNC・ロボットの異なる通信仕様・データ構造','情報モデルでデータの意味をそろえて交換','上位システムやエージェントへのデータ接続','読出しと制御書込み、アクセス権・状態解釈は別確認','OPC UA情報モデル・多ベンダー接続を説明','AIエージェントへの連携シナリオを明記','担当タスクの追加記載','認識',question='どのデータモデルでどのエージェントに渡すか。書込み権限とデータ鮮度をどう扱うか。')
add(12,'27','Facteye／Resolana','旧設備・設備品質データの収集と集約','データ基盤','設備稼働・品質等','既設設備情報の収集・可視化とデータ分析・AI利用','設備と品質を関連づける情報','データからの自動制御・全工場最適化は未確認','データ収集・対話AI・基盤連携を説明','旧設備・品質との連携課題を具体化','2026具体化・機能差未確定','認識/判断')
add(13,'25','Smart Craft MES','現場MESとERP・周辺システム','業務ソフトウェア','生産・品質・在庫・指示・実績','記録・指示・トレーサビリティを一元化しAPI連携','現場の工程・実績情報','AI分析の内容・入力定着・判断権限は未確認','2024詳細なし','2026機能説明あり','2024個別比較不能','認識/判断')
add(14,'26','MonoRevo：工程計画・スケジューリング','クラウド工程管理','業務ソフトウェア','工程、納期、設備・作業者負荷、進捗','工程設計・計画・進捗をまとめて予定変更へ対応','工程計画・負荷の可視化と自動スケジューリング','計画制約・再計画の確定権限・失敗時の介入は未確認','2024詳細なし','2026は工程設計・自動スケジューリングを説明','2024個別比較不能','判断')
add(14,'01','MonoRevo：類似図面検索・自動見積','工程管理のAI補助機能','業務ソフトウェア','図面等。原価・学習データ範囲は未記載','AIによる類似図面検索・自動見積を説明','類似図面・見積支援','見積の前提・責任・人による確定点は未確認','2024詳細なし','2026は図面検索・見積を記載','2024個別比較不能','認識/判断')
add(15,'27','SOFIXCAN Ω Eye','古い機械の操作パネル前','カメラによる後付け観測','ランプ・文字・各種メーター画像','画像から数値・状態を読みModbus等でPLCへ書込み','既設機の稼働情報','読取誤り・画像品質・PLC書込み先の確認が必要','メーター読取自動連係を掲載','Ω Eyeと読取対象・連携方法を具体化','2026具体化・機能差未確定','認識')
add(15,'14','SOFIXCAN Fleeter＋AI Forecast：ミニ工場','複数機器・搬送の連携フレームワーク','搬送機器。ロボット構成は未特定','上位指示・機器状態、時系列データ等','搬送フレームワーク、異常予兆AI、3D等を接続するデモ','機器間の搬送連携・異常予兆','機器別コンポーネント開発が必要。未知例外の自律復帰は未確認','メーター読取、切粉除去、AI熱変位補正を掲載','2026は連携するミニ工場展示','搬送対象・構成の追加記載','認識/判断/動作','ミニ工場の展示デモ予定・商用無人工場実績ではない')
add(16,'28','X-Area Remote','複数設備・ロボットの遠隔管制','搬送ロボット等＋遠隔操作端末','設備状態・映像・エラー情報','複数台を一元監視し必要時に人が遠隔操作','現場駆け付けを減らす例外対応','人によるエラー対応を含む。AI支援と自律完結を分ける','2024詳細なし。2022年に工場内けん引車の実証あり','2026は遠隔監視・操作サービスを展示予定','2024個別比較不能','認識/動作','既存サービス方式確認・2026展示予定',('W05','W09'),'通常時の監視台数、介入頻度、遠隔で復帰できないエラーと通信断時の処理。')
add(17,'20','自動測定／MiCAT Planner・MiBOT系','三次元測定・計測プラットフォーム','ロボット連携測定。2026の個別構成は要確認','CAD・測定対象・測定結果','測定プログラム作成と測定作業を自動化','測定結果・品質情報','計測から加工補正への全機種接続は未確認','MiBOT・MiCAT Planner等を掲載','計測データ活用・プラットフォームを強調','2024から継続','認識/判断/動作')
add(18,'21','Renishaw Central＋IPC','測定機・工作機械→Central→制御装置','プローブ／ゲージと工作機械','計測、装置状態、アラーム','IPCで工具オフセットや機械変数を更新','加工へのクローズドループ補正','機種接続・計測不確かさ・補正上限は要確認','Centralを掲載済み','Centralを継続。新プローブ等を追加掲載','2024から継続','認識/判断/動作','既存方式・メーカー自社工場事例あり',('W03',),'どの寸法がどのオフセットを変えるか。誤計測時の補正抑止と顧客実績を確認する。')
add(19,'20','FormControl X／DIGILOG','工作機械内の形状・工具計測','機上プローブ／レーザ工具測定','ワーク形状・工具の測定値','機上3D測定、工具計測・欠け検知・補正','機外への移動を抑える測定・補正','熱状態・校正・機種適合の限界は未確認','FormControl X、LC50 DIGILOGの機上計測・補正を掲載','LC54、GrindingControlを追加掲載','2024から継続','認識/判断/動作')
add(20,'15','ARTIS／BLU／VTS','加工機・研削工程の監視・計測','センサ・測定システム','加工・工具・研削の計測信号','工具・工程監視と機上計測','状態監視・品質制御の支援','個別の閾値・AI使用・自動停止や補正範囲は未確認','ARTIS等の監視・計測群を掲載','同名群を継続しスキルレス化を訴求','2024から継続','認識/判断')
add(21,'19','HACARUS Check ZERO','外観検査AIソフトウェア／日東商事ブース','カメラ画像を扱うAI。ロボット必須ではない','少量良品画像、運用後の良品・不良品画像','良品学習で開始しデュアルチューニングで追加調整','外観異常の判定','品種・照明変化、見逃しと過検出、追加学習の判断は要確認','HACARUS同名の2024詳細なし','2026で良品学習と追加調整を説明','2024個別比較不能','認識/判断','2026展示予定・外観AI製品方式確認',('W06',))
add(22,'19','HACARUS Check：協働ロボット多面検査','検査セル','協働ロボット＋カメラ＋照明。機種・姿勢生成方式未確認','ワークの側面・裏面等の画像','ロボットで多角度撮像しAIでキズ・欠け等を判定','立体物の多面外観検査','姿勢教示・撮像順序・再撮像・不良排出の権限は未確認','日東商事は放電加工機2機種を紹介','AI検査システムと協働ロボットによる多面撮像を追加','担当タスクの追加記載','認識/判断/動作',question='ロボットのタスクは撮像のための姿勢変更。AIが動作も生成するのか、固定教示かを区別する。')
add(23,'22','VT122＋VTC 6.0','工作機械の工具ビジョン検査','工具撮像・解析システム','工具画像','VTC 6.0のAI摩耗診断・工具長機能','摩耗状態の診断・工具検査','交換指示・自動交換までの接続は未確認','VT122工具検査を掲載','AI摩耗診断と工具長機能を明記','担当タスクの追加記載','認識/判断')
add(24,'22','ツールコラージュ','工具を置く撮像・検査装置','カメラ式工具検査装置','アッセンブリ工具の刃先画像','AIで診断箇所を認知し欠け・摩耗を判定・記録','刃先状態の判定','ユーザーの判定基準学習・適用工具・撮像条件が必要','診断箇所自動認知とAI摩耗判定を説明済み','撮像・AI・判定記録を継続掲載','2024から継続','認識/判断')
add(24,'23','ツールコラージュアナライザー','工具検査の分析ソフト','ソフトウェア','現場の摩耗幅・摩耗量データ','摩耗量を蓄積・学習し寿命と交換時期を予測','寿命予測・交換タイミングの提示','工具交換の自動実行は記載なし。加工条件差・予測誤差は未確認','2024展示は主に欠け・摩耗判定。寿命推定研究は2023にも発表','2026はアナライザーと寿命・交換提案を具体掲載','担当タスクの追加記載','判断','2026展示予定・寿命推定研究自体は既存',('W08',))
add(24,'24','ツールソムリエ','工具収納・管理とロボット供給の構成','工具入出庫ロボット。詳細構成未確認','工具登録情報・所在・管理画面の選択','工具管理、機械、ロボット、プリセッターを連携','選択した工具を工具台車へ搬送する構成','管理画面の選択を起点にする説明。完全自律な補充判断は未確認','工具収納・情報管理を掲載','ロボット供給を説明するが2026は実機を出展しない','2026具体化・機能差未確定','認識/動作','説明動画・資料のみ。実機展示なし',question='実稼働事例と連携機種を確認。会場でロボット実演を見たという記録は付けない。')
add(25,'10','ナットランナー治具','ロボットのワーク固定工程','ナットランナー装着ロボットハンド','治具の締結部。AI認識は未記載','メカ構造でクランプ・アンクランプし油圧・エア配管を不要化','治具へのワーク固定・解除','締結確認・締付トルク・ワークばらつき対応は要確認','ロボット用治具・メカ式ツール交換を掲載','ナットランナー治具の種類追加を説明','搬送対象・構成の追加記載','動作')
add(25,'11','メカ式フィンガー交換','ロボットハンド先端','ロボットハンド＋ばね式交換機構','交換対象のフィンガー','追加配線・配管なしに単純動作で交換','品種に応じた把持部の変更','適合する指・交換精度・把持確認は要確認','メカ式ツールチェンジャーを掲載','ばねを用いたフィンガー交換を具体掲載','2026具体化・機能差未確定','動作')
add(26,'12','マテハンホルダ','既設工作機械の主軸','クーラント圧で動作するホルダ','主軸スルークーラント圧・ワーク','既存の圧力源を利用したワーク搬送','工程間のワーク受渡し','形状・重量・機種・搬送経路の適合条件は未確認','高圧洗浄と自動プリセットを掲載','マテハンホルダを具体紹介','搬送対象・構成の追加記載','動作')
add(26,'17','BoostMaster','工作機械の主軸・クーラント回路','主軸回転で駆動する増圧ツール','主軸回転と低圧クーラント','回転で増圧して切屑の排出・洗浄に利用','切粉処理','絡まりを認識して除去するAI方式との効果比較は未実施','最大15MPaの高圧洗浄方式を既に説明','BoostMasterとして切屑処理の自動化を説明','2024から継続','動作')
add(27,'13','パレット自動化／MAS・ラインエンジニアリング','加工機から生産ライン','パレットシステム等。2026個別構成未確認','パレット・作業・設備情報の詳細は未記載','機械・パレット・ソフト・ライン設計・保守を組み合わせる','加工と供給・運用の支援','ラインの再計画・例外復帰の自律範囲は未確認','DA300自動化パッケージ・DA500パレット等を掲載','MAS、生産ライン全体と保守を訴求','2026具体化・機能差未確定','動作')
add(28,'13','5軸＋マルチパレット／MiOS','変種変量加工のセル','工作機械と多面パレットシステム','加工プログラム・指示・画像・ワークオフセット等','加工データをプロジェクト単位で管理し供給・無人運転を支援','多品種のパレット加工','事前段取り・工具準備・異常時対応の自動範囲は未確認','5軸＋多パレット、MiOS4、CAMの一貫支援を説明','旋削機能等で加工対象を広げる提案','2024から継続','判断/動作')
add(29,'09','RoboSync：移設後の位置復旧','機械・ロボット・ストッカー間','ロボット＋ビジョン・マーカ。関節構成未確認','各設備のマーカ画像','移動後にマーカを読み相対位置を補正','再設置の位置合わせ','人の移設・復旧操作を含む。未知トラブルの自律復帰の証明ではない','New Robot System等を掲載。RoboSync同一機能は未確認','既存パレット・台車の利用と位置復旧を具体説明','2026具体化・機能差未確定','認識/判断/動作','既存製品方式確認・2026展示予定',('W04',),'どの位置ずれを補正できるか。治具・台車が変わると何を再教示するか。')
add(30,'17','TR-20W：主軸の切粉除去','旋盤の主軸周辺','台車型ロボットシステムTR-20W。アーム軸構成は未確認','主軸に絡んだ切粉の状態。センサ方式は未記載','フィジカルAIで状況を認識・判断して除去する予定デモ','絡まった切粉の除去','把持具・除去力・除去後確認・停止と人への引継ぎは未確認','2024のTR-20Wはワーク搬入・搬出の自動化デモを予告','2026は切粉絡まり判断・除去を参考出品','担当タスクの追加記載','認識/判断/動作','参考出品・現地未検証',('N01','N02'),'切粉形状や絡まり方が変わっても対応できるか。除去成功の判定、失敗時の再試行・停止条件は。')
add(31,'12','HS4200＋レール走行ロボット','4主軸旋盤と素材・完成品のパレット間','ガントリーレール取付ロボット。軸構成未確認','素材・完成品の位置・搬送指示。知覚方式未記載','走行範囲を広げ1台で素材・完成品のパレタイジング','素材・完成品の搬送','品種別教示・把持・失敗時の介入範囲は未確認','HS4200と機上ロボットのスライドレール搬送を説明','ガントリーレールで素材・完成品パレタイジングを具体紹介','2024から継続','動作')
add(31,'09','HS4200：フィジカルAI自動段取り替え','HS4200のロボットセル','フィジカルAI搭載のレール走行ロボット','段取り指示・対象。音声や画像などの入力方式は一次資料では未確認','誰でも簡単な自動段取り替えとのメーカー説明','具体的に交換・変更する対象は未記載','治具・爪・位置・プログラム等のどこを自動化するか未確認','レールロボット搬送は既存。AI段取りの記載は確認できず','2026はフィジカルAIによる自動段取り替えを明記','担当タスクの追加記載','判断/動作',question='交換するのは爪・治具・品種設定・動作プログラムのどれか。自然言語指示の有無と人の段取り残作業は。')
add(32,'29','振動診断AI・遠隔監視','設備診断・主軸周辺','軸受・回転機械の診断システム','振動等。2026個別AI入力は未記載','2024はAIによる高度診断、2026はトライボロジー中心の総論','設備保全・診断支援','2026の同機能提供範囲は資料不足','AI振動診断・遠隔監視を掲載','2026総論から個別AI機能差を比較できない','2026具体化・機能差未確定','認識/判断',question='AI診断は2026のどの製品・展示に継承されるか。記載減を機能撤退と解釈しない。')
add(33,'30','Adaptive Lubrication／主軸監視','主軸・軸受・潤滑系','主軸関連システム','状態監視情報。潤滑制御の具体入力は未確認','適応潤滑と監視・主軸構成を紹介','信頼性と潤滑負荷の改善を狙う','自動調整の条件・AI使用・効果実測は未確認','監視・潤滑を掲載','Adaptive Lubrication等を具体掲載','2026具体化・機能差未確定','認識/動作')
add(34,'21','HGM-DX：測定フィードバック研削','超硬工具の両面研削ライン','研削機＋自動ハンドリング＋ドレッシング＋測定','加工後の厚み・刃先高さ','測定値を研削機に返して加工公差を自動補正','無人研削の寸法補正','補正上限、測定不確かさ、異常値への対応は未確認','超硬インサートの製造・検査自動化を説明','HGM-DXで測定→研削の補正経路を具体記載','担当タスクの追加記載','認識/判断/動作')
add(35,'14','ATP：工具製造の工程間搬送','工具研削・放電・計測をまたぐセル','複数工程・他社設備を含む自動搬送システム','工具・工程情報。詳細仕様未確認','ATPで複数の加工・測定工程を接続','工程間の搬送と生産連携','機種別連携・工具切替・停止復帰の詳細は未確認','ATP、他社機連携を掲載','ATPを日本初公開とするが版・対象の差は不明','2024から継続','動作')
add(36,'20','M3MH：既設機での機上計測','既設3軸・5軸加工機','機上測定システム','CAD・機上測定データ','オフライン測定計画と機上の形状評価・工程制御を紹介','載せ替えを抑える測定・工程情報','校正・機械精度・対応機種・補正先の詳細は未確認','機上評価・CAD計画・リアルタイム工程制御を説明済み','後付け・工数削減を再訴求','2024から継続','認識/判断')
add(37,'20','NEXIV・CT・ロボットビジョン等','外観・寸法・内部品質の評価','画像測定・CT・ロボット関連計測','画像・CT・測定対象','異なる計測手段で工程別の品質を評価','外観・寸法・内部品質の情報','一体化した自律補正やAIの性能向上は資料から不明','ロボット測定・自動搬送・インライン検査を掲載','計測・画像・CT・ビジョンの統合的訴求','2024から継続','認識/判断')
add(38,'29','ミロクルAI保全ナビ／分析レポート','保全クラウドの対話・分析機能','ソフトウェア支援','保全履歴・現場の音声入力・質問','記録を整形し類似トラブルのヒント、KPIと分析解説を生成','保全記録・診断のヒント・分析レポート','設備への操作指示・修理実行は説明なし。AIオプションと本体を区別','2024詳細なし','2026は保全ナビ・分析・ヘルプを個別説明','2024個別比較不能','判断','本体とは別のAIオプション・提供範囲未確認')
add(38,'27','ミロクルAIメーター読み取り','スマホ等の点検入力','撮像端末＋AI読取','メーター画像','画像から値を読み点検欄へ反映','数値と画像の点検記録','読取確認・対応計器・オフライン条件は未確認','2024詳細なし','2026はα版と明記','2024個別比較不能','認識','α版・AIオプション')
add(39,'03','BreylSimulator','加工用クランプ・治具設計','設計ソフトウェア','クランプ構成・設計ルールDB','ルールDBを用いて設計・構成案を提案','治具設計の候補','ルール外の形状や制約、設計採否は要確認。生成AI方式と扱わない','BreylSimulatorとルールDBを掲載','同製品に加えAI・XR等を紹介','2024から継続','判断')
add(40,'25','TECHS系：スマホ実績・購買API','生産管理と現場入力・購買','業務ソフトウェア','実績・購買・商品DB等','スマホ入力と購買APIで転記・連携の負担を抑える','生産実績・購買情報','AIによる自律購買や全体計画の確定とは未確認','AI・IoT、生産管理4500社超を既に掲載','購買API・スマホ機能を具体化','2026具体化・機能差未確定','認識/動作',question='導入社数は生産管理全体とAI機能を区別。機能ごとの利用・受注・業務削減実績は。')
add(41,'01','匠フォース：業務AIエージェント','見積・設計・調達・原価管理業務','業務ソフトウェア','現場ノウハウ等。参照データと接続システムは未記載','AIが作業を進め人が承認・判断するとの説明','業務処理の支援。個々の操作列は未記載','人が承認・判断と明記。承認箇所・外部システム操作権限は未確認','2024詳細なし','2026は業務範囲と人の承認役を説明','2024個別比較不能','判断/動作',question='見積1件の入力→検索→計算→提案→承認→登録を実演で追い、各段階の実行者を確認する。')
add(42,'31','RW耐環境ビジョンユニット','工作機械内部・製造ライン','回転機構・エア制御を備えた耐環境撮像ユニット','油・水・ミスト・粉塵・切粉下の画像','回転とエアでレンズ汚れを抑え、画像をAI解析へ渡す','切粉蓄積・工具折損等の検知用画像と判定','画像品質・清掃・見逃し・検出後の停止や除去は未確認','2024詳細なし','2026は耐環境撮像とAIによる切粉・工具異常検知を具体説明','2024個別比較不能','認識/判断')
add(43,'15','NC MachiningAID（2024）／2026 CNC省人化','CNCと加工工程','工作機械の加工監視','加工信号等。今回カタログでは入力方式未記載','2024はAI・機械学習で加工異常・工具摩耗・作業ミスを検知すると説明','加工工程の監視・検知','2026の個別製品名・機能継承・自動停止権限は未確認','2024にNC MachiningAIDの3種類の検知タスクを記載','2026は設計から加工・保守までのAI省人化を訴求するが、個別差分は不明','2026具体化・機能差未確定','認識/判断',question='2024の3検知がどの製品へ継承・拡張されたか。AIを新搭載したとは説明しない。')
add(43,'26','放電加工の新開発スケジューラ','放電加工機の自動化運用','MG12R・SV12P等の放電加工機周辺','加工予定・設備等。入力と制約は未記載','新開発スケジューラによる自動化運用を提案','放電加工の計画・運用支援','自動確定する工程・工具・順序と人の承認は未確認','2024はMX600、SV-P等とラインDXを掲載','2026はMG12R・SV12Pと新開発スケジューラを記載','担当タスクの追加記載','判断')
add(43,'28','遠隔保守サポート／スマート保全','装置メーカーと納品先工場のデジタル接続','遠隔保守システム','装置情報等。個別データ仕様未記載','デジタル接続で復旧迅速化、保全の計画対応化を支援','保守・保全業務の支援','遠隔で操作可能な範囲、顧客承認・現場作業は未確認','2024はクラウドアプリ・ラインDX等を掲載','2026は遠隔保守とスマート保全を明示','2026具体化・機能差未確定','認識/判断')
add(44,'14','ロボット＋AMRの工程間連携デモ','ロボットとAMRの連携セル','ロボット＋自律走行搬送ロボット。型式未確認','ワーク・工程情報。具体データ・知覚方式未記載','工程を止めずにワークをつなぐ連携デモを予告','ワークの工程間受渡し・搬送','ロボットとAMR間の位置合わせ・待合せ・エラー対処とAIの担当は未確認','Mech Mind×FANUCのビジョン、S-CART、重量物RGV等を個別掲載','2026はロボットとAMRの連携を具体展示しフィジカルAIと呼ぶ','搬送対象・構成の追加記載','動作','連携デモ予定・AIの担当範囲未特定',question='どの認識・判断がAIか。設備状態・受渡し位置・作業順をどう同期し、片方停止時にどう復帰するか。')
add(45,'34','産業用IPC／VARIO-X・分散I/O','機械の制御・データ処理基盤','産業用IPC・分散I/O・省配線機器','機器・センサの現場データ','省配線・省スペース化とデータ収集・処理環境を構成','AIを載せるための基盤。特定AI作業の実演とは別','AIモデル・タスク・実機判断は今回記載なし','Vario-X・IIoT省配線・安全I/Oと協働ロボットのケーブル保護展示','2026はIPCとVARIO-XをAI活用基盤として説明','2026具体化・機能差未確定','認識','実装基盤の展示予定・AI応用そのものは未特定')
add(46,'33','歳差ローラカム式減速機','ロボット等へ適用を想定する駆動要素','カム式減速機。搭載ロボットは未特定','モータの回転','動力伝達の機械要素。フィジカルAIに最適とのメーカー訴求','トルク・精度・剛性等を担う部品','認識・判断・タスク生成のAI機能を備えるとは記載なし','DSR・DM9・GTB減速機等を掲載','歳差ローラカム式減速機を初公開と記載','搬送対象・構成の追加記載','動作','機構部品の新製品展示予定・AI搭載実績未確認',question='物理AI向けという用途提案と、実際の搭載機・作業・採用実績を分けて確認する。')

# A card carries its own source-location hints, rather than only a company-level citation.
task_needs={
 '00':'具体的な担当タスクと対応する顧客課題は、今回確認した資料では未特定',
 '01':'図面・原価・調達情報を探し、見積等を作る反復作業の負担',
 '02':'加工工程を決める技能への依存と、過去の加工ノウハウの再利用',
 '03':'ワーク形状と固定制約に合う治具構成を考える負担',
 '04':'CAM・NC作成にかかる手作業と加工ノウハウへの依存',
 '05':'実機試行で発覚する干渉・削り過ぎ・設定違いの防止',
 '06':'PLCコード作成・文書参照など制御開発の反復作業',
 '07':'I/O・操作画面・電気設計ツールを使うための知識と設計作業',
 '08':'AIモデルの作成・評価からPLC等への組込みに要する専門技能',
 '09':'移設・再配置・品種変更のたびに生じる位置合わせと段取り作業',
 '10':'ワーク固定・解除の手作業と、自動化に伴う配管・配線の負担',
 '11':'多品種に対応するロボット把持部の交換・再設定',
 '12':'素材・加工品の受渡し作業と機械の待ち時間',
 '13':'多品種加工でのパレット準備・供給と長時間運転の段取り',
 '14':'部品・容器等の運搬と、設備間の受渡し・連携の負担',
 '15':'加工中の異常・工具状態を把握するための監視と診断技能',
 '16':'加工負荷や条件を適正化する技能と現場での試行',
 '17':'切粉の蓄積・絡まりにより自動加工が停止し、人が除去する負担',
 '18':'熱変位などによる加工品質のばらつきと補正の負担',
 '19':'目視検査の工数・判定ばらつき、不良画像不足による立上げ負担',
 '20':'測定待ち、機外への運搬・載せ替え、測定プログラム準備の負担',
 '21':'測定結果を加工条件・オフセットへ手動で戻す調整と品質ばらつき',
 '22':'刃先の欠け・摩耗を目視で判定する技能と検査工数',
 '23':'工具の過早交換・摩耗による不良を抑える交換時期の判断',
 '24':'工具の所在不明・重複購入と入出庫・供給作業の負担',
 '25':'生産・品質・在庫・購買の分散情報、現場入力と転記の負担',
 '26':'納期・工程・負荷が変わる際の生産計画調整',
 '27':'旧設備・異機種の情報取得とデータ形式・意味の不一致',
 '28':'設備エラー時の現場駆け付けと、遠隔からの状態把握・対処',
 '29':'異常原因・保全対処の属人化と、記録・診断情報を調べる負担',
 '30':'主軸の信頼性維持と潤滑・監視に伴う運用負荷',
 '31':'油・水・切粉・ミストで必要な画像を安定して得られない問題',
 '32':'設計・加工準備・製造間のデータ分断と設計資産の再利用',
 '33':'要求トルク・精度・剛性等に合う動力伝達要素の選択',
 '34':'配線・制御盤の工数や空間、現場データ処理環境の実装負担',
}
for c in cards:
 if c['item'] in ['工作機械へのAIエージェント実装（名称・担当不明）','フィジカルAI CNC','生成AIによるロボット駆動']:
  c.update(task_id='TASK00',task=tasks['00']['task'],phase=tasks['00']['phase'])
 c['company_need_context']=c['customer_need']
 c['customer_need']=task_needs[c['task_id'].replace('TASK','')]
 if c['delta_type']=='搬送対象・構成の追加記載':c['delta_type']='対象・構成・要素の追加記載'
 if c['item']=='TwinCAT Machine Learning Creator':c['roles']=['判断','動作']
 ds=dossiers[c['review_id']]
 tokens=[s.strip() for s in c['item'].replace('＋','／').replace('：','／').replace('（','／').split('／') if len(s.strip())>=3]
 tokens+=['フィジカルAI','AIエージェント','切粉','アナライザー','Copilot','スケジューラ','VARIO-X','歳差']
 locations=[]
 for eid in c['evidence_ids']:
  e=evidence[eid];entry=dict(evidence_id=eid,url=e['url'],locator=e['locator'])
  if e.get('source_record_id'):
   rec=next(r for rs in ds['years'].values() for r in rs if r['exhibitor_record_id']==e['source_record_id'])
   text=rec['exhibition_introduction']+'\n'+rec['main_exhibits']
   terms=[s for s in tokens if s in text]
   entry['find_terms']=list(dict.fromkeys(terms))[:4]
   entry['local_cache']=rec['cache_path']
   entry['locating_note']='製品名・機能語で検索。語がない年度は基準点・比較限界の根拠。'
  locations.append(entry)
 c['source_locations']=locations

configuration_overrides={
 'FC003':'工作機械に実装するAIエージェント。ソフトウェア構成・接続先は未記載',
 'FC004':'診断専用NCプログラム、クラウドAI解析、my DMG MORIの状態表示',
 'FC007':'工作機械・サーボの仮想モデルとデジタルツイン環境',
 'FC011':'TwinCAT開発環境、生成AI・専門エージェント、プロジェクト・文書の参照',
 'FC012':'TwinCAT開発環境、対話型AI、I/O構成・HMI画面の設計支援',
 'FC013':'TwinCAT HMIのチャット、運転データ接続、文書参照、診断・コマンド実行機能',
 'FC014':'学習モデル自動構築・最適化ツールとONNX／PLC向け実装パイプライン',
 'FC016':'Electric P8の回路・部品データとPro Panelの3D制御盤設計',
 'FC017':'Eplan Platformに統合された対話型AI支援',
 'FC018':'ESPRIT EDGE CAMとProPlanAIの工程予測機能',
 'FC020':'MastercamとCAMAssistのCAM作業支援機能',
 'FC021':'Gコードのシミュレーションと機械・工具・治具・ワークの仮想モデル',
 'FC022':'Vericut Force／OptimizerによるNC最適化ソフトウェア',
 'FC023':'Fusion／FeatureCAM等のCAD・CAMとPLM・データ連携',
 'FC024':'OPC UA情報モデル対応サーバーと上位システム・エージェントへの接続',
 'FC025':'Facteyeのデータ収集とResolanaの集約・分析基盤',
 'FC026':'MESの生産・品質・在庫管理とERP等へのAPI連携',
 'FC027':'クラウド工程管理と工程計画・自動スケジューリング機能',
 'FC028':'クラウド工程管理とAI類似図面検索・自動見積機能',
 'FC040':'工具検査データを蓄積・学習し寿命・交換時期を分析するソフトウェア',
 'FC058':'保全クラウド、AI分析レポート、対話・音声による保全ナビ',
 'FC059':'メーター画像読取AIと点検入力機能（α版）',
 'FC060':'クランプ構成ルールDBと治具設計提案ソフトウェア',
 'FC061':'生産管理ソフトウェア、スマホ実績入力、購買API連携',
 'FC062':'見積・設計・調達・原価管理向けAIエージェント。接続構成は未記載',
 'FC065':'放電加工機の新開発スケジューラ。連携構成は未記載',
 'FC066':'装置と納品先工場をデジタル接続する遠隔保守・保全サービス',
}
for c in cards:
 c['system_configuration']=configuration_overrides.get(c['card_id'],c['robot_form'])
 record_ids={evidence[e].get('source_record_id') for e in c['evidence_ids'] if evidence[e]['year']==2026}
 c['booths_2026']=list(dict.fromkeys(r['booth'] for r in dossiers[c['review_id']]['years']['2026'] if r['exhibitor_record_id'] in record_ids)) or c['booths_2026']
category_rows,category_definitions=build_category_index(cards,evidence)
for c in cards:c['review_depth']='個別タスクの重点整理（従来69カード）'
candidate_screening=expand_candidates(cards,evidence,category_rows,category_definitions)
deepening_reviews,deepening_coverage=apply_deepening(cards,evidence,category_rows)
alias_confirmations,followup_coverage=apply_followup(cards,evidence,category_rows,deepening_reviews,candidate_screening)
deepening_coverage['followup_checked_date']='2026-10-18'
deepening_coverage['source_status_counts']=dict(Counter(r['source_status'] for r in deepening_reviews))
visit_priorities=build_priorities(cards,category_definitions)
phase_names.append('追加候補（出展説明単位）')
tasks['99']=dict(task_id='TASK99',phase=phase_names[-1],phase_index=len(phase_names)-1,task='追加候補・タスク分解待ち',purpose='出展説明単位で分類。個別製品・実装方式の精査は未完了')

def save(stem,rows):
 (OUT/(stem+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (OUT/(stem+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
  w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)

save('fact_cards',cards)
save('category_index',category_rows)
save('category_definitions',category_definitions)
save('candidate_screening',candidate_screening)
save('category_visit_priorities',visit_priorities)
save('priority_deepening',deepening_reviews)
synthesis,synthesis_coverage=build_synthesis(cards,evidence)
synthesis['open_questions']=enrich_synthesis(synthesis,cards,evidence)
synthesis['company_alias_confirmations']=alias_confirmations
synthesis_coverage.update(analysis_date='2026-10-18',supplement_checked_date='2026-10-18',open_questions=len(synthesis['open_questions']),alias_confirmations=1)
for stem,rows in synthesis.items():save(stem,rows)
synthesis_figures=draw_figures(synthesis)
taxonomy=[]
for t in tasks.values():
 ids=[c['card_id'] for c in cards if c['task_id']==t['task_id']]
 taxonomy.append(dict(**t,card_ids=ids,coverage='具体カードあり' if ids else '今回の具体カードなし・未調査／未分解（技術不存在を意味しない）'))
save('technology_taxonomy',taxonomy)
used={e for c in cards for e in c['evidence_ids']}
save('evidence_ledger',[e for i,e in evidence.items() if i in used])
comparisons=[{k:c[k] for k in ['card_id','company','item','task','baseline_2024','observation_2026','delta_type','unresolved','evidence_ids']} for c in cards]
save('task_comparison_2024_2026',comparisons)

relations=[
 ('工程案からNC検証へ',['FC019','FC021'],['FC022'],'方式間の比較・接続仮説','過去ジョブやCAM支援が出す案を、実行NC・工具・治具・機械モデルで検証する。これら製品間の実装済み連携を示す線ではない。'),
 ('計測から加工補正へ',['FC033'],['FC033'],'同一製品構成の接続を原典で確認','Renishaw Central＋IPCは計測等から機械変数・工具オフセットの更新へつなぐ。AIが必須の方式ではない。'),
 ('厚み測定から研削補正へ',['FC049'],['FC049'],'同一製品構成の接続を原典で確認','HGM-DXは加工後測定値を研削機へ返す構成。'),
 ('撮像から判断・除去へ',['FC058'],['FC045'],'方式間の比較・接続仮説','撮像安定化と切粉除去を一連の仕事として比較する観点。興和とTAKISAWAが接続している証拠はない。'),
 ('設備データから診断・遠隔対処へ',['FC025','FC026','FC030'],['FC014','FC031'],'方式間の比較・接続仮説','情報モデル・旧機画像・設備データを診断や遠隔操作へ渡す際の意味と権限を調べる。製品間接続は未確認。'),
]
# Resolve relation IDs by product names to prevent positional shifts in future card edits.
byname={c['item']:c['card_id'] for c in cards}
relations[0]=(relations[0][0],[byname['ESPRIT EDGE ProPlanAI'],byname['Mastercam＋CAMAssist']],[byname['Vericut：Gコード検証']],*relations[0][3:])
relations[1]=(relations[1][0],[byname['Renishaw Central＋IPC']],[byname['Renishaw Central＋IPC']],*relations[1][3:])
relations[2]=(relations[2][0],[byname['HGM-DX：測定フィードバック研削']],[byname['HGM-DX：測定フィードバック研削']],*relations[2][3:])
relations[3]=(relations[3][0],[byname['RW耐環境ビジョンユニット']],[byname['TR-20W：主軸の切粉除去']],*relations[3][3:])
relations[4]=(relations[4][0],[byname['OPC UA情報モデルとエージェント連携'],byname['Facteye／Resolana'],byname['SOFIXCAN Ω Eye']],[byname['TwinCAT CoAgent for Operations'],byname['X-Area Remote']],*relations[4][3:])
edges=[]
for i,(n,a,b,k,s) in enumerate(relations,1):
 es=sorted({e for c in cards if c['card_id'] in a+b for e in c['evidence_ids']})
 edges.append(dict(relation_id=f'REL{i:02}',name=n,from_cards=a,to_cards=b,classification=k,description=s,evidence_ids=es))
save('technology_relationships',edges)
company_count=len({c['review_id'] for c in cards})
explicit_label_records=[]
for r in detail_data['2026']:
 if not any(k in r['exhibition_introduction']+' '+r['main_exhibits'] for k in ['フィジカルAI','エージェント']):continue
 matched=[vid for vid,d in dossiers.items() if any(x['exhibitor_record_id']==r['exhibitor_record_id'] for x in d['years']['2026'])]
 assert len(matched)==1
 explicit_label_records.append(dict(company=r['company_name'],booth=r['booth'],record_id=r['exhibitor_record_id'],review_id=matched[0],card_ids=[c['card_id'] for c in cards if c['review_id']==matched[0]],url=r['detail_url'],scope='取得済み2026詳細820行で上記語を明示した掲載のみ。別表現・未掲載の技術は対象外。'))
save('explicit_ai_label_review',explicit_label_records)
coverage=dict(checked_date='2026-10-16',listing_rows={'2024':1281,'2026':1146},linked_details_retrieved={'2024':988,'2026':820},candidate_2026_name_keys=342,reviewed_company_keys=company_count,fact_cards=len(cards),task_categories=len(tasks),populated_task_categories=len({c['task_id'] for c in cards}),cards_by_phase=dict(Counter(c['phase'] for c in cards)),cards_by_delta=dict(Counter(c['delta_type'] for c in cards)),evidence_records=len(used),new_primary_web_pages=len(web),card_comparison_scope=f'商品・タスク単位の記載比較。{company_count}社全ての全製品を分解したものではない。',remaining=[f'2026候補342名称キー全てを同じ深さで分析していない。重点は{company_count}社','一覧に詳細URLがない619行と原典説明欠損には未捕捉の可能性','ロボットの軸・センサ・ハンド、AIモデル・操作権限、成功率・導入実績・市場規模は個別に未確認','2024詳細がない企業と名称変更の法人照合は比較不能を保持','2026は展示予定。参考出品、動画のみ、製品発表、既存製品を分離','主張の圧縮・研究テーマ選定・最終1枚への集約は次工程'])
coverage['explicit_label_scan']=dict(searched_detail_rows=820,terms=['フィジカルAI','エージェント'],matched_listing_rows=len(explicit_label_records),reviewed_listing_rows=len(explicit_label_records),limitations='語を明示した掲載に限る。AI全社の網羅・採用率ではない。CoAgent等の別表現も別途重点レビュー。')
coverage['category_index']=dict(categories=len(category_definitions),associations=len(category_rows),companies=company_count,items=len(cards),scope='候補345掲載・342名称キーを一次仕分け。既存の重点69カードと追加候補の出展説明単位カードは精査深度を区別。',definitions=category_definitions)
coverage['candidate_screening']=dict(rows=len(candidate_screening),name_keys=342,dispositions=dict(Counter(r['disposition'] for r in candidate_screening)),additional_tagged_records=len(cards)-69,additional_focused_reviews=19,additional_two_year_fulltext_comparisons=12,additional_focused_without_2024=7,coverage_basis='凍結した2026関連候補集合。キーワードで拾わなかった他の出展者全ての非該当を保証するものではない。')
coverage['visit_priorities']=dict(rows=len(visit_priorities),categories=9,companies=len({r['company'] for r in visit_priorities}),basis='カテゴリー内の調査者による訪問順案。性能・市場規模・採用率のランキングではない。')
coverage['remaining'][0]='候補集合345掲載は一次仕分け済み。追加候補の全製品・入力・権限・年度差分を同じ深さで精査したものではない。分類保留1掲載あり。'
coverage['card_comparison_scope']='従来69用途は個別タスクで整理。追加265掲載は出展説明単位で分類し、うち19掲載を重点整理（両年全文比較12掲載・2024同名原典なし7掲載）。未精査の年度差は未判定を保持。'
coverage['new_primary_web_pages']=len(web)+2
coverage['priority_deepening']=deepening_coverage
coverage['cross_company_synthesis']=synthesis_coverage
coverage['remaining_followup']=followup_coverage
coverage['candidate_screening'].update(additional_two_year_fulltext_comparisons=13,additional_focused_without_2024=6,official_alias_comparisons=1)
coverage['card_comparison_scope']='従来69用途と追加265掲載を整理。追加重点19掲載のうち両年原典比較13掲載（同名12＋公式社名変更照合1）、2024未照合6掲載。'
coverage['remaining'][-1]='研究開発候補5件は仮説として保存。既存機能との重複・適用条件を確認して採否を決める。最終1枚への集約は未着手。'
coverage['remaining']=deepening_coverage['remaining']+coverage['remaining']
(OUT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')

H=lambda s:html.escape(str(s),quote=True)
def link(c):return f'<a class="chip" href="#{c["card_id"]}">{H(c["company"])} · {H(c["item"])}</a>'
def table(headers,rows):return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+H(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def pairs(c,fields):return '<dl>'+''.join('<dt>'+H(label)+'</dt><dd>'+H(c[k])+'</dd>' for k,label in fields)+'</dl>'
def source(e):
 return f'<div class="source" id="{e["evidence_id"]}"><a href="{H(e["url"])}" target="_blank" rel="noopener">{H(e["evidence_id"])} · {H(e["title"])}</a><p>{H(e["locator"])} ／確認 {H(e["checked_date"])}</p><p>{H(e["exhibition_certainty"])}</p></div>'

# A compact visual overview precedes the complete matrix. Nodes are representative,
# linked to the full cards; positions are an analytical classification, not integrations.
nodes=[
 (0,0,'MonoRevo：類似図面検索・自動見積','ものレボ','類似図面を探す'),
 (0,1,'ESPRIT EDGE ProPlanAI','Hexagon','加工履歴→工程案'),
 (0,1,'Mastercam＋CAMAssist','JBM','CAM作業を支援'),
 (0,0,'Vericut：Gコード検証','CGTech','実行NCの不具合検出'),
 (1,0,'TwinCAT CNC：切削信号の解析・独自制御','Beckhoff','信号取得・FFT解析'),
 (1,1,'TwinCAT CoAgent for Engineering：PLC','CoAgent 開発〈製品発表〉','要求→PLCコード案'),
 (1,1,'TwinCAT CoAgent for Engineering：I/O・HMI','CoAgent 開発〈製品発表〉','I/O・画面設計案'),
 (1,2,'TwinCAT Machine Learning Creator','TwinCAT MLC','学習モデル→制御実装'),
 (2,0,'RoboSync：移設後の位置復旧','中村留 RoboSync','マーカで位置を認識'),
 (2,1,'HS4200：フィジカルAI自動段取り替え','シマダ HS4200','AI段取り〈対象不明〉'),
 (2,2,'AMR 1000','DMG森精機 AMR','チップバケット搬送'),
 (2,2,'ARMROID／OMR20','オークマ','機内型／移動式ロボット'),
 (3,0,'RW耐環境ビジョンユニット','興和 RW','切粉・油の中を撮る'),
 (3,1,'TR-20W：主軸の切粉除去','TAKISAWA TR-20W','切粉絡まりを判断'),
 (3,2,'TR-20W：主軸の切粉除去','TR-20W〈参考出品〉','主軸の切粉を除去'),
 (3,2,'BoostMaster','NTツール','クーラントで切粉処理'),
 (4,0,'ツールコラージュ','モリマシナリー','刃先を自動撮像'),
 (4,0,'HACARUS Check：協働ロボット多面検査','日東商事／HACARUS','ロボットで多面撮像'),
 (4,1,'ツールコラージュアナライザー','モリマシナリー','摩耗→寿命・交換提案'),
 (4,1,'HACARUS Check ZERO','HACARUS ZERO','少量良品から異常判定'),
 (4,2,'Renishaw Central＋IPC','レニショー','計測→工具オフセット'),
 (4,2,'HGM-DX：測定フィードバック研削','Wintech HGM-DX','厚み測定→研削補正'),
 (5,0,'SOFIXCAN Ω Eye','SOFIX Ω Eye','旧機メーターを読む'),
 (5,1,'TwinCAT CoAgent for Operations','CoAgent 運用〈製品発表〉','運転データ→原因・対処'),
 (5,1,'Condition Agent','DMG〈製品資料のみ〉','診断NC→クラウド分析'),
 (5,2,'X-Area Remote','パナソニック','人が遠隔で例外対処'),
 (5,2,'ロボット＋AMRの工程間連携デモ','三菱商事テクノス','ロボットとAMRを連携'),
]
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="950" viewBox="0 0 1600 950" role="img" aria-label="製造工程と認識・判断・動作の技術マップ"><rect width="1600" height="950" fill="#fff"/><style>text{font-family:Meiryo,\'Yu Gothic\',sans-serif;fill:#203b50}a:hover rect{stroke:#b57912;stroke-width:3}</style>',
 '<text x="35" y="43" font-size="26" font-weight="bold">製造工程 × 認識・判断・動作</text><text x="35" y="75" font-size="17">代表例の配置図。1製品が複数の役割に現れる場合あり。企業間接続や成熟度の順位は表さない。</text>']
for x,p in enumerate(phase_names[:6]):
 sx=150+x*237
 svg.append(f'<rect x="{sx}" y="100" width="227" height="55" rx="4" fill="#214b63"/><text x="{sx+10}" y="135" style="fill:white" font-size="18" font-weight="bold">{H(p)}</text>')
for y,(role,sub) in enumerate([('認識','見る・集める'),('判断','計画・提案・診断'),('動作・実装','実行・制御・適用')]):
 sy=170+y*195
 svg.append(f'<rect x="20" y="{sy}" width="118" height="185" fill="#e8f0f5"/><text x="30" y="{sy+80}" font-size="19" font-weight="bold">{role}</text><text x="30" y="{sy+110}" font-size="12">{sub}</text>')
 for x in range(6):
  sx=150+x*237
  svg.append(f'<rect x="{sx}" y="{sy}" width="227" height="185" fill="{["#f0f7fb","#eef7f6","#f5f5f0"][y]}"/>')
  matches=[n for n in nodes if n[:2]==(x,y)]
  for k,(_,_,name,company,label) in enumerate(matches):
   cid=byname[name];ny=sy+12+k*78
   svg.append(f'<a href="#{cid}"><rect x="{sx+9}" y="{ny}" width="209" height="70" rx="4" fill="white" stroke="#b7cdd7"/><text x="{sx+18}" y="{ny+21}" font-size="13">{H(company)}</text><text x="{sx+18}" y="{ny+46}" font-size="15" font-weight="bold">{H(label)}</text><text x="{sx+178}" y="{ny+63}" font-size="10">{cid}</text></a>')
svg.append('<rect x="20" y="770" width="1557" height="73" rx="4" fill="#e9eef2"/><text x="35" y="798" font-size="18" font-weight="bold">共通基盤：データの意味・接続／撮像品質／IPC・分散I/O／機構・駆動要素</text><text x="35" y="827" font-size="16">たけびし OPC UA ／ 興和 耐環境撮像 ／ ケーメックス IPC・VARIO-X ／ イマオ 治具・指交換 ／ テクノダイナミックス 減速機</text>')
svg.append('<text x="35" y="877" font-size="17">人の境界：コード・工程案の採否、実機操作の承認、段取り準備、異常後の復帰。各カードに確認範囲を記載。</text><text x="35" y="910" font-size="16">AIの具体担当が不明な例：ファナック フィジカルAI CNC、DMG森精機の工作機械AIエージェント。役割を推定で埋めない。</text><text x="35" y="938" font-size="14">CoAgentの市場投入時期は要問い合わせ。Condition Agentと会場のエージェントの同一性は未確認。2026現地は未検証。</text></svg>')
map_svg=''.join(svg)
(ROOT/'outputs/JIMTOF2026_技術全体マップ_v1.svg').write_text(map_svg,encoding='utf-8')

css='''*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:76px}body{margin:0;background:#f5f7fa;color:#182b3c;font:15px/1.7 "Yu Gothic UI","Meiryo",sans-serif}header{background:#132c40;color:white;padding:45px max(28px,calc((100vw - 1360px)/2)) 32px}header p{max-width:1080px;color:#d9e6ef}h1{font-size:32px;line-height:1.45;margin:0 0 14px}h2{font-size:25px;line-height:1.4;margin:0 0 16px}h3{font-size:18px;margin:0 0 10px}nav{position:sticky;top:0;z-index:5;background:white;border-bottom:1px solid #d3dce4;padding:12px 24px;display:flex;gap:18px;flex-wrap:wrap}a{color:#006b78;text-decoration:none}a:hover{text-decoration:underline}nav a{font-weight:bold}main{max-width:1420px;padding:28px;margin:auto}section{margin-bottom:35px;background:white;padding:28px;border:1px solid #dce4eb;border-radius:8px}p{margin:8px 0 13px}.note{padding:13px 17px;background:#fff4dc;border-left:4px solid #c58b22}.muted{color:#536b7a}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:25px}.stat{background:#244256;padding:14px}.stat strong{display:block;font-size:29px}.stat span{font-size:13px;color:#d5e4ed}.scroll{overflow:auto}table{width:100%;border-collapse:collapse;min-width:850px}th,td{text-align:left;vertical-align:top;border:1px solid #dce4eb;padding:12px}th{background:#e9f0f5;font-weight:700}td:first-child{min-width:130px}td{min-width:180px}.chip{display:block;font-size:13px;line-height:1.55;border-left:3px solid #158c94;background:#edf7f7;padding:7px 9px;margin:0 0 7px}.empty{font-size:13px;color:#677d8d}.phase th{background:#244b62;color:white}.taskname{font-weight:bold}.small{font-size:13px}button,input,select{font:inherit;padding:9px 12px;border:1px solid #bcccd6;border-radius:4px;background:white}button{cursor:pointer;background:#006d77;color:white}.filters{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}input{flex:1;min-width:220px}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.card{border:1px solid #cedce4;border-top:4px solid #117a83;border-radius:5px;padding:22px;scroll-margin-top:88px}.card:target{outline:3px solid #d99a1c;background:#fffdf3}.id{color:#557080;font-size:13px}.tag{display:inline-block;font-size:12px;border:1px solid #cbd8df;padding:2px 7px;margin:4px 5px 5px 0;background:#f4f8fb}dl{margin:12px 0;display:grid;grid-template-columns:115px 1fr;gap:7px 12px}dt{font-weight:bold;color:#466274}dd{margin:0;overflow-wrap:anywhere}.delta{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:#f1f5f8;padding:12px;margin:14px 0}.delta b{display:block;color:#236b7c}details{margin-top:14px;border-top:1px solid #dce4eb;padding-top:10px}summary{cursor:pointer;font-weight:bold;color:#006b78}.source{font-size:13px;padding:12px 0;border-bottom:1px solid #e1e8ed;scroll-margin-top:90px}.source p{margin:3px 0}.flows{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.flow{padding:18px;background:#f4f7fa;border:1px solid #d8e3ea}.arrow{text-align:center;font-size:27px;color:#427c88}.flow.dashed{border:2px dashed #b6913f;background:#fffaf0}.guide{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.guide>div{padding:16px;background:#edf4f7}.printonly{display:none}@media(max-width:850px){.cards,.flows,.guide{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}header{padding:28px}main{padding:12px}section{padding:18px}h1{font-size:25px}dl{grid-template-columns:95px 1fr}nav{position:static}}@media print{nav,.filters,.export{display:none}body{background:white;font-size:10pt}header{background:white;color:#182b3c;padding:10mm}header p{color:#182b3c}.stats{display:none}main{padding:0}section{border:0;padding:5mm;break-before:page}.cards{display:block}.card{break-inside:avoid;margin-bottom:10mm}details>*{display:block}details{display:block}table{font-size:8pt;min-width:0}.scroll{overflow:visible}.chip{font-size:8pt}.flows{display:block}.flow{break-inside:avoid;margin:6mm 0}.printonly{display:block}}'''
css+='''.company-name{font-size:25px;font-weight:750;line-height:1.45;color:#123c55;margin:3px 0 8px;overflow-wrap:anywhere}.card h3{font-size:18px;font-weight:600;color:#305b70}.booth-label{font-weight:700;color:#234e65;margin:8px 0}.category-links{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}.category-tag{font-size:13px;border:1px solid #a5c9cf;border-radius:4px;padding:4px 8px;background:#eef8f8}.category-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:18px 0}.category-button{text-align:left;color:#173d50;background:#f0f6f8;border:1px solid #c8dce4;padding:14px}.category-button strong{display:block;font-size:18px}.category-button span{font-size:13px}.category-table td{font-size:14px}.category-table td:nth-child(3){min-width:170px;font-weight:bold}.category-table td:nth-child(4){min-width:230px}.category-table td:nth-child(5){min-width:95px}.category-table td:nth-child(6),.category-table td:nth-child(7){min-width:230px}.category-table td:first-child{min-width:145px}@media(max-width:850px){.category-grid{grid-template-columns:1fr}.company-name{font-size:23px}}[hidden]{display:none!important}'''
parts=[f'<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JIMTOF2026 技術整理・事実カード・全体マップ</title><style>{css}</style><header><p>JIMTOF2026 事前調査 ／ 中間成果物 v1 ／ 2026-10-16</p><h1>製造のどの仕事を、何に、どこまで任せるか</h1><p>工程と具体タスクを起点に、ロボット・AI支援・従来の自動化を比較する。配置は調査者の分析、機能はメーカー説明。2026の現地実演・効果は未検証。</p><div class="stats"><div class="stat"><strong>{len(tasks)}</strong><span>仕事の細分類</span></div><div class="stat"><strong>{len(cards)}</strong><span>技術・用途別の事実カード</span></div><div class="stat"><strong>42</strong><span>重点企業名称キー</span></div><div class="stat"><strong>{len(used)}</strong><span>出典レコード</span></div></div></header>',
 '<nav><a href="#read">読み方</a><a href="#categories">カテゴリーから探す</a><a href="#map">工程×役割マップ</a><a href="#robots">ロボット比較</a><a href="#agents">AI支援の実装先</a><a href="#relations">関係図</a><a href="#comparison">2024→2026</a><a href="#cards">事実カード</a><a href="#coverage">範囲・残件</a></nav><main>',
 '<section id="read"><h2>最初に見る3つの観点</h2><div class="guide"><div><h3>どの工程の、何の仕事か</h3><p>見積からNC、段取り、加工、検査、保全まで。同じ「AI」でも工程案の生成と切粉除去は別の仕事。</p></div><div><h3>認識・判断・動作のどこか</h3><p>画像判定、工程提案、実機操作を分ける。3つそろうだけで未知状況にも対応する自律性を認定しない。</p></div><div><h3>どこまで確認できたか</h3><p>既存方式、追加記載、比較不能を分ける。展示・製品発表・参考出品・動画のみも区別。</p></div></div><p class="note">全体マップは重点42社の配置図です。2026候補342名称キー全てを同じ深さで分析した地図ではありません。空白は技術の不存在を意味しません。</p></section>',
 '<section id="map"><h2>01　工程 × 担当する役割</h2><p>各リンクから個別カードへ。複数の役割を持つカードは複数セルに表示します。掲載数の大小は市場規模・普及率ではありません。</p>']
maprows=[]
for p in phase_names:
 maprows.append([f'<strong>{H(p)}</strong>','<span class="empty">工程内の役割を比較 ↓</span>','','',''])
 for t in taxonomy:
  if t['phase']!=p:continue
  cs=[c for c in cards if c['task_id']==t['task_id']]
  maprows.append([f'<span class="id">{t["task_id"]}</span><br><span class="taskname">{H(t["task"])}</span>',*[''.join(link(c) for c in cs if r in c['roles']) or '<span class="empty">今回のカードなし</span>' for r in ['認識','判断','動作','未特定']]])
parts.append('<div class="scroll">'+map_svg.replace('width="1600" height="950"','width="100%" style="min-width:1100px;height:auto"',1)+'</div><details><summary>全タスク・全カードの配置を開く</summary>'+table(['工程・タスク','認識・データ取得','判断・計画・提案','動作・制御・業務操作','具体役割が未特定'],maprows)+'</details></section>')
physical_names=['AMR 1000','MATRIS WPH 210','生成AIによるロボット駆動','ARMROID／OMR20','HACARUS Check：協働ロボット多面検査','RoboSync：移設後の位置復旧','TR-20W：主軸の切粉除去','HS4200＋レール走行ロボット','HS4200：フィジカルAI自動段取り替え','マテハンホルダ','BoostMaster','X-Area Remote','ロボット＋AMRの工程間連携デモ']
physical=[c for n in physical_names for c in cards if c['item']==n]
parts.append('<section id="robots"><h2>02　ロボット・機械は、何をしているか</h2><p>「フィジカルAI」はメーカーがそう呼ぶケースと、固定教示・マーカ・機構・遠隔操作を並べて比較します。ロボットの有無とAI動作生成の有無は別です。</p>')
parts.append(table(['具体例','形態・実装先','対象と仕事','認識・判断の方式','人の仕事・限界','2024との差'],[[link(c),H(c['robot_form'])+'<br>'+H(c['deployment']),H(c['task'])+'<br>'+H(c['output']),H(c['input'])+'<br>'+H(c['mechanism']),H(c['human_boundary'])+'<br><b>'+H(c['product_stage'])+'</b>',H(c['baseline_2024'])+' → '+H(c['observation_2026'])] for c in physical])+'</section>')
agent_names=['TwinCAT CoAgent for Engineering：PLC','TwinCAT CoAgent for Engineering：I/O・HMI','TwinCAT CoAgent for Operations','Eplan Copilot','ESPRIT EDGE ProPlanAI','ミロクルAI保全ナビ／分析レポート','匠フォース：業務AIエージェント','Condition Agent','工作機械へのAIエージェント実装（名称・担当不明）']
agents=[c for n in agent_names for c in cards if c['item']==n]
parts.append('<section id="agents"><h2>03　AI支援は、どこに入り、何を助けるか</h2><p>エージェントと呼ばれる製品に加え、比較対象のCAM予測・保全AIも表示します。予測やQ&amp;Aだけでエージェント型の自律実行を認定しません。</p>')
parts.append(table(['具体例','実装先／入力','助ける仕事・出力','実行・承認の境界','提供段階'],[[link(c),H(c['deployment'])+'<br>'+H(c['input']),H(c['mechanism'])+'<br>'+H(c['output']),H(c['human_boundary']),H(c['product_stage'])] for c in agents])+'</section>')
parts.append('<section id="relations"><h2>04　技術間の接続と、人が引き継ぐところ</h2><p>実線は同一製品構成内で原典確認した接続、破線は調査者が置いた比較・接続の仮説。企業間の提携・実装済み接続を推測しません。</p><div class="flows">')
for e in edges:
 cls='flow dashed' if '仮説' in e['classification'] else 'flow'
 parts.append(f'<div class="{cls}"><span class="id">{e["relation_id"]} · {H(e["classification"])}</span><h3>{H(e["name"])}</h3>'+''.join(link(c) for c in cards if c['card_id'] in e['from_cards'])+'<div class="arrow">↓</div>'+''.join(link(c) for c in cards if c['card_id'] in e['to_cards'])+f'<p>{H(e["description"])}</p></div>')
parts.append('</div><p class="note">横断比較で確認したい継ぎ目：提案→検証→採用、計測→補正許可、認識→実機操作、停止→復帰→再開。各製品がすべてを自動で担うとは確認できていません。</p></section>')
parts.append('<section id="comparison"><h2>05　2024から何が変わったと読めるか</h2><p>商品名の変化より、担当する仕事と任せる範囲を比較します。「追加記載」はその年の初発明・初販売の意味ではありません。</p>')
parts.append(table(['具体例','2024の基準点','2026の記載・公式補足','差分の扱い'],[[link(c),H(c['baseline_2024']),H(c['observation_2026']),H(c['delta_type'])] for c in cards])+'</section>')
parts.append('<section id="cards"><h2>06　技術・用途別の事実カード</h2><p>冒頭は確認した機能と方式。顧客課題は調査者の整理、提供段階はメーカー説明です。原典・原文検索語を展開すると、該当箇所を確認できます。</p><div class="filters"><input id="query" aria-label="カード検索" placeholder="会社・製品・仕事・方式・未確認事項を検索"><select id="phase" aria-label="工程で絞る"><option value="">全工程</option>'+''.join('<option>'+H(p)+'</option>' for p in phase_names)+'</select><button id="reset">解除</button><button id="openall">出典を全て開く</button></div><p id="count" class="muted"></p><div class="cards">')
for c in cards:
 search=json.dumps(c,ensure_ascii=False)
 parts.append(f'<article class="card" id="{c["card_id"]}" data-phase="{H(c["phase"])}" data-search="{H(search)}"><div class="id">{c["card_id"]} ／ {c["task_id"]}</div><h2 class="company-name">{H(c["company"])}</h2><h3>{H(c["item"])}</h3><p class="booth-label">2026ブース：{H("・".join(c["booths_2026"]))}</p><span class="tag">{H(c["phase"])} · {H(c["task"])}</span><span class="tag">{H(c["product_stage"])}</span><div class="category-links">'+''.join(f'<a class="category-tag" href="#categories" data-category="{t["category_id"]}">{H(t["category"])}</a>' for t in c['categories'])+'</div>')
 fields=[('customer_need','顧客課題〈分析〉'),('deployment','実装先'),('system_configuration','システムの構成'),('input','入力'),('mechanism','AIの判断／方式'),('output','実行・出力')]
 if 'deepening' in c:
  d=c['deepening'];parts.append('<p class="note small"><b>訪問優先の深掘り：</b>'+H(d['ai_scope'])+'<br>'+H(d['source_status'])+'</p>')
  for k in ['human_preparation','human_approval','human_exception']:c[k]=d[k]
  fields += [('human_preparation','人の事前準備'),('human_approval','人の承認'),('human_exception','人の例外対応')]
 else:fields += [('human_boundary','人・権限の境界')]
 parts.append(pairs(c,fields))
 parts.append(f'<div class="delta"><div><b>2024</b>{H(c["baseline_2024"])}</div><div><b>2026</b>{H(c["observation_2026"])}</div></div><p class="small"><b>比較判定：</b>{H(c["delta_type"])}</p><p class="note small"><b>確認する点：</b>{H(c["unresolved"])}</p><p class="small muted">{H(c["exhibition_status"])}。採用件数・受注・市場規模は未確認。</p><details><summary>出典・該当箇所（{len(c["evidence_ids"])}件）</summary>')
 for eid in c['evidence_ids']:
  e=evidence[eid]
  # Per-card search terms keep the original location findable without reproducing the entire catalogue.
  loc=next(s for s in c['source_locations'] if s['evidence_id']==eid)
  terms=' ／ 原文検索語：'+H('・'.join(loc['find_terms'])) if loc.get('find_terms') else ''
  parts.append(f'<p class="source"><a href="#{eid}">{eid}</a> ／ <a href="{H(e["url"])}" target="_blank" rel="noopener">原典を開く</a><br>{H(e["locator"])}{terms}</p>')
 parts.append('</details></article>')
parts.append('</div></section><section id="coverage"><h2>07　分析範囲と次の調査</h2>')
parts.append(f'<p>公式一覧：2024年1,281行／2026年1,146行。詳細リンクのある988件／820件は取得済み。今回のカードは重点42社、{len(cards)}用途。2026候補342名称キーのうち、残る300名称キーは同じ深さの分析をしていません。</p><p>2024の資料がある会社でも、すべての個別製品・タスクの差分を比較できるわけではありません。図の役割分類・接続仮説は調査者の分析です。</p><ul>'+''.join('<li>'+H(x)+'</li>' for x in coverage['remaining'])+'</ul><p>次は未特定のタスク・認識方式・操作権限を優先して公式技術資料で補い、各分野の競合方式・適用条件を比較します。その後に動向を抽出し、研究課題と最終1枚を編集します。</p><p class="export"><a href="../data/research/technology_atlas_v1/fact_cards.csv">事実カードCSV</a> ／ <a href="../data/research/technology_atlas_v1/technology_taxonomy.csv">技術分類CSV</a> ／ <a href="../data/research/technology_atlas_v1/task_comparison_2024_2026.csv">年度差分CSV</a> ／ <a href="../data/research/technology_atlas_v1/evidence_ledger.csv">出典台帳CSV</a></p></section><section id="sources"><h2>出典台帳</h2>')
parts.extend(source(e) for i,e in evidence.items() if i in used)
parts.append('''</section></main><script>
const query=document.querySelector('#query'),phase=document.querySelector('#phase'),cards=[...document.querySelectorAll('.card')];
function filter(){const q=query.value.toLocaleLowerCase();let n=0;cards.forEach(c=>{c.hidden=!(c.dataset.search.toLocaleLowerCase().includes(q)&&(!phase.value||c.dataset.phase===phase.value));if(!c.hidden)n++});document.querySelector('#count').textContent=n+' / '+cards.length+'件表示'}
query.addEventListener('input',filter);phase.addEventListener('change',filter);document.querySelector('#reset').onclick=()=>{query.value='';phase.value='';filter()};document.querySelector('#openall').onclick=()=>document.querySelectorAll('.card details').forEach(d=>d.open=true);
function reveal(){const id=decodeURIComponent(location.hash.slice(1)),c=document.getElementById(id);if(c?.classList.contains('card')){query.value='';phase.value='';filter();c.scrollIntoView()}else if(c?.classList.contains('source'))c.closest('details')?.setAttribute('open','')};window.addEventListener('hashchange',reveal);filter();reveal();
</script></html>''')
category_html=['<section id="categories"><h2>カテゴリーから企業・展示・ブースを探す</h2><p>同じ展示を複数カテゴリーから探せます。メーカーがカテゴリー名を明示したものと、内容から調査者が分類したものを区別します。対象は重点46社・69カードです。</p><p class="note"><b>自動化</b>は固定手順やルールによる作業も含みます。<b>自律化</b>は状況に応じた判断・実行の限定タスクとメーカーの提案を、範囲を明記して掲載します。いずれも工場全体の完全無人化を認定するタグではありません。</p><div class="category-grid">']
for d in category_definitions:
 category_html.append(f'<button type="button" class="category-button" data-category="{d["category_id"]}"><strong>{H(d["category"])}</strong><span>{d["company_count"]}社 ／ {d["item_count"]}展示アイテム</span></button>')
category_html.append('</div><details><summary>カテゴリーの定義・分類境界</summary>'+table(['カテゴリー','対象','分類上の境界'],[[H(d['category']),H(d['definition']),H(d['boundary'])] for d in category_definitions])+'</details><div class="filters" id="category-results"><select id="category-select" aria-label="カテゴリーで絞る"><option value="">全カテゴリー</option>'+''.join(f'<option value="{d["category_id"]}">{H(d["category"])}</option>' for d in category_definitions)+'</select><input id="category-query" aria-label="企業・展示・ブースを検索" placeholder="企業名・展示名・ブース・仕事を検索"><button id="category-reset" type="button">解除</button></div><p id="category-count" class="muted"></p><div class="scroll"><table class="category-table"><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['カテゴリー','細分類','企業','展示・カードへ','2026ブース','関連範囲・展示確度','分類根拠・理由'])+'</tr></thead><tbody>')
for r in category_rows:
 category_html.append(f'<tr class="category-row" data-category="{r["category_id"]}" data-search="{H(json.dumps(r,ensure_ascii=False))}"><td>{H(r["category"])}</td><td>{H(r["subcategory"])}</td><td>{H(r["company"])}</td><td><a href="#{r["card_id"]}">{H(r["item"])}</a><br><span class="id">{r["card_id"]}</span></td><td>{H("・".join(r["booths_2026"]))}</td><td>{H(r["relation_scope"])}<br><span class="small muted">{H(r["exhibition_status"])} ／ {H(r["product_stage"])}</span></td><td>{H(r["classification_basis"])}<br>{H(r["classification_reason"])}</td></tr>')
category_html.append('</tbody></table></div><p class="small muted">カテゴリー間で企業・展示が重複するため、各カテゴリーの件数は足し合わせられません。</p><p><a href="JIMTOF2026_カテゴリー別出展索引_v1.xlsx">Excelのカテゴリー索引を開く</a> ／ <a href="../data/research/technology_atlas_v1/category_index.csv">索引CSV</a></p></section>')
category_html[0]=category_html[0].replace('対象は重点46社・69カードです。',f'分類対象は{company_count}名称キー・{len(cards)}カード／追加候補です。追加分は出展説明単位の一次分類で、従来69用途の精査とは深度を分けています。')
parts.insert(3,followup_html(synthesis,followup_coverage)+synthesis_html(synthesis,synthesis_coverage,synthesis_figures)+roles_section(deepening_reviews,category_definitions,cards)+priority_section(visit_priorities,category_definitions)+''.join(category_html)+screening_section(candidate_screening))
category_js='''const categorySelect=document.querySelector('#category-select'),categoryQuery=document.querySelector('#category-query'),categoryRows=[...document.querySelectorAll('.category-row')];
function filterCategories(){const q=categoryQuery.value.toLocaleLowerCase();const companies=new Set(),items=new Set();let n=0;categoryRows.forEach(r=>{r.hidden=!!((categorySelect.value&&r.dataset.category!==categorySelect.value)||!r.dataset.search.toLocaleLowerCase().includes(q));if(!r.hidden){n++;const v=JSON.parse(r.dataset.search);companies.add(v.company);items.add(v.card_id)}});document.querySelector('#category-count').textContent=companies.size+'社・'+items.size+'展示アイテム（カテゴリーとの対応 '+n+'行）'}
document.querySelectorAll('[data-category]:not(.category-row)').forEach(b=>b.addEventListener('click',()=>{categorySelect.value=b.dataset.category;categoryQuery.value='';filterCategories();document.querySelector('#category-results').scrollIntoView()}));categorySelect.addEventListener('change',filterCategories);categoryQuery.addEventListener('input',filterCategories);document.querySelector('#category-reset').onclick=()=>{categorySelect.value='';categoryQuery.value='';filterCategories()};filterCategories();'''
category_js=category_js.replace("[data-category]:not(.category-row)",".category-button,.category-tag")
category_js=category_js.replace("document.querySelector('#category-count').textContent", "priorityCategory.value=categorySelect.value;filterPriorities();document.querySelector('#category-count').textContent")
category_js=category_js.replace("document.querySelector('#category-results').scrollIntoView()", "document.querySelector('#priority-results').scrollIntoView()")
parts[-1]=parts[-1].replace('</script>',ROLES_JS+PRIORITY_JS+category_js+'</script>')
report=ROOT/'outputs/JIMTOF2026_技術整理と全体マップ_v1.html'
report_text=''.join(parts).replace('<strong>42</strong>',f'<strong>{company_count}</strong>').replace('重点42社',f'重点{company_count}社').replace('2026候補342名称キーのうち、残る300名称キーは同じ深さの分析をしていません。',f'2026候補342名称キー全てを同じ深さで分析したものではありません。取得済み2026詳細820行を横断し、「フィジカルAI」「エージェント」を明示した{len(explicit_label_records)}掲載は全件、今回のカードで扱っています（これらの語がない技術は別途調査）。')
report_text=report_text.replace('<a href="#categories">カテゴリーから探す</a>','<a href="#priorities">訪問優先・年度比較</a><a href="#categories">カテゴリーから探す</a><a href="#screening">候補仕分け</a>')
report_text=report_text.replace('<nav>','<nav><a href="#followup">10/18追補・候補の絞込み</a><a href="#synthesis">28社の比較図・技術マップ</a><a href="#research-candidates">共通課題・研究候補</a><a href="#ai-human">AIの判断・実行・人の関与</a>',1)
report_text=report_text.replace('両年全文比較12掲載・2024同名原典なし7掲載','両年原典比較13掲載（同名12＋公式社名変更1）・未照合6掲載')
report_text=report_text.replace('次は未特定のタスク・認識方式・操作権限を優先して公式技術資料で補い、各分野の競合方式・適用条件を比較します。その後に動向を抽出し、研究課題と最終1枚を編集します。','28社の方式比較・年度変化・共通課題と研究候補5件を上部に保存しました。次は操作権限・失敗復帰・既存機能との重複を確認し、研究候補の採否を検討します。最終1枚への集約は未着手です。')
report_text=report_text.replace('重点企業名称キー','分類対象の企業名称キー').replace('仕事の細分類','仕事の細分類＋未分解枠').replace('技術・用途別の事実カード</span>','事実カード・追加候補</span>')
report_text=report_text.replace(f'全体マップは重点{company_count}社の配置図です。','図は従来の重点46社から選んだ代表例です。追加候補はカテゴリー索引・訪問優先リストで探索できます。')
report_text=report_text.replace(f'今回のカードは重点{company_count}社、{len(cards)}用途。',f'今回の分類対象は{company_count}名称キー、従来69用途と追加265掲載。')
report_text=report_text.replace('会社・製品・仕事・方式・未確認事項を検索','会社・製品・仕事・方式・未確認事項を検索')
report_text=report_text.replace('.card:target{','.priority-company{font-size:19px;color:#173c55}.priority-row{scroll-margin-top:90px}.priority-row[hidden],.category-row[hidden],.screening-row[hidden],.card[hidden]{display:none!important}.card:target{')
for c in cards:
 marker=f'<div class="id">{c["card_id"]} ／ {c["task_id"]}</div>'
 report_text=report_text.replace(marker,marker+f'<p class="small muted">整理深度：{H(c["review_depth"])}</p>')
report_section=ROOT/'data/research/report_v0/section.html'
if report_section.exists():
 from report_completion_html import integrate
 report_text=integrate(report_text,report_section.read_text('utf-8'))
report.write_text(report_text,encoding='utf-8')
checkpoint=dict(**coverage,report_path=str(report),data_path=str(OUT),resume_command='python scripts/build_technology_atlas.py',status='成果物保存・最低限検証待ち',canonical_spec_sha256=hashlib.sha256((ROOT/'JIMTOF2026_Codex_Project_Spec_v0.md').read_bytes()).hexdigest())
(ROOT/'checkpoints/technology_atlas_v1.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(coverage,ensure_ascii=False,indent=2))
