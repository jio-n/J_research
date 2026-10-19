"""2026-10-18 bounded follow-up: source corrections, research gates, on-site questions."""
from collections import Counter

DATE='2026-10-18'
DIR='sources/remaining_research_20261018/'
SOURCES=[
 ('01','Beckhoff','From chatbot to intelligent agent','https://www.beckhoff.com/en-gb/company/news/from-chatbot-to-intelligent-agent.html','2025/6/13／Placing people at the heart of automation；PLC・I/O・HMI、専門家がreview・confirm・approve','2025-06-13','search_03','公式検索索引の本文を確認。ページopenは404、誌面PDFは容量超過。全文取得済みとはしない。'),
 ('02','Beckhoff','TF1700 CoAgent for Operations','https://www.beckhoff.com/en-en/products/automation/twincat/tfxxxx-twincat-3-functions/tf1xxx-system/tf1700.html','Properties／direct system access；Product status／market release on request','未記載','read_02','抽出本文を確認。命令許可リスト・毎回承認・復帰手順はこの製品説明に未記載。'),
 ('03','CloudNC','Mastercam CAM Assist：確認・調整と学習方針','https://www.cloudnc.com/ja/mastercam','仕組みStep 2–4／FAQ：顧客データで学習しない、加工性評価、編集可能CAM','未記載','read_04','機能説明を確認。削減率・他社比較は採否の定量根拠に使わない。'),
 ('04','SolidCAM','CAM Assistの生成後の編集・検証','https://help.solidcam.com/topics/solutions/cloudnc-cam-assist.htm','L11–19／プログラマーがreview・refine、既存のsimulation・verification・NC生成','未記載','read_04','既存ワークフローの説明。新規研究の独自性を証明する資料ではない。'),
 ('05','HACARUS','Check ZERO公式ソフトウェア説明','https://check.hacarus.com/ja/aisoftware/','特徴／異常箇所表示・良否アノテーション追加学習','未記載','read_03','メーカーの機能説明。競合比較・導入効果を独立した性能実証としない。'),
 ('06','NdotLight','TRINIX：物理属性生成と自己修正','https://ndotlight.com/','Physics Injection／Self-corrective Closed Loop／FAQ','未記載','read_01','質量・摩擦等の推論、シミュレーションからの修正を説明。実測正解・実機誤差・収束条件は未確認。'),
 ('07','NVIDIA','SimReady FAQ：静的検証と実行時検証','https://docs.omniverse.nvidia.com/simready/latest/simready-faq.html','What Is the Difference…Foundation；How Do I Validate My Composed Scene…（L526–538）','2026-10-14（ページ更新日）','read_03','周辺基盤の公式仕様。個別アセット検証と実行時検証を区別。TRINIXがこの検証を搭載する証拠ではない。'),
 ('08','NVIDIA','SimReady Physics Best Practices','https://docs.omniverse.nvidia.com/simready/latest/simready-asset-creation/physics-best-practices.html','Typical USDPhysics Components／Collider、Mass、materialの摩擦・密度・反発','2026-10-14（ページ更新日）','read_04','周辺基盤の公式技術説明。属性が存在することと実物に合うことは別の確認。'),
 ('09','NdotLight','DexBench共同開発の告知','https://ndotlight.com/newsroom/ndotlight-to-co-develop-dexbench-a-global-standard-for-humanoid-evaluation-with-nvidia-and-rlwrld','2026/8/7／SimReady環境・操作評価・sim-to-real gap低減の共同開発','2026-08-07','read_04','メーカーの共同開発告知。公開済み完成標準・JIMTOF実装・性能保証とはしない。'),
 ('10','ユシロ','社名変更のお知らせ','https://www.yushiro.co.jp/news/社名変更のお知らせ','旧：ユシロ化学工業株式会社→新：株式会社ユシロ；2025/4/1変更','2025-03-13','read_05','公式の旧・新社名と変更日を確認。名称の類似だけで照合していない。'),
 ('11','JIMTOF公式・ユシロ化学工業','JIMTOF2024：遠隔監視・濃度補給','https://www.jimtof.org/2024/search/jp/ESdetails?e=He5z-J4NQm8','出展説明・主な出展物／クーラントのリモート監視とフレキシブル濃度補給装置','2024（出展資料）','raw_2024','既存取得済み原典を再読。ALFREDと同じ製品・制御系統とは確認できない。'),
 ('12','JIMTOF公式・ツールディスカバリー','W1069合同掲載：切削条件カリキュレーター','https://www.jimtof.org/search/jp/ExhibitorDetails?b=W1069','有限会社ツールディスカバリー見出し／工具・被削材・加工方法、AI条件目安、登録不要','2026（展示予定）','read_05','同じ小間にイワタツール等を掲載。企業間の法人関係は推定しない。AI方式の補足仕様は未確認。'),
 ('13','ニデック／TAKISAWA','JIMTOF2026：TR-20W参考出品','https://www.nidec.com/jp/products/machine-tools/contents/machine-tool-jimtof2026/','TAKISAWA／TR-20W、主軸の切粉認識・判断・除去、参考出品','未記載','read_03','出展告知を再確認。失敗判定・再試行・力制限・動作許可は確認範囲に未記載。'),
]

def apply_followup(cards,evidence,category_rows,reviews,screening):
 by={c['card_id']:c for c in cards}
 for number,publisher,title,url,locator,published,cache,note in SOURCES:
  eid='ERF-'+number
  evidence[eid]=dict(evidence_id=eid,publisher=publisher,year=2024 if number=='11' else 2025 if number in ['01','10'] else 2026,title=title,url=url,locator=locator,published_date=published,checked_date=DATE,evidence_type='周辺基盤の公式仕様・個別出展製品の搭載確認とは別' if number in ['07','08'] else '企業／開発元／展示会の公式説明',exhibition_certainty='展示予定・製品説明・共同開発告知・周辺仕様を区別。現地実演の確認ではない。',cache_path='sources/detail_2024_EXH-2024-ecba0726f588a525.html' if cache=='raw_2024' else DIR+cache+'.json',source_excerpt=locator,retrieval_note=note)
 updates={
  'FC011':dict(source_ids=['ERF-01'],human_approval='公式2025/6/13：専門家が生成結果を確認・確定・実行承認する方針。コンパイル・実機書込み・起動の個別画面と権限は未確認',delta_interpretation='PLCコード支援は2023、CoAgentのPLC・I/O・HMI支援と専門家の実行承認方針は2025/6に説明済み。2026は展示記述の具体化として比較し、同年初搭載としない。'),
  'FC012':dict(source_ids=['ERF-01'],human_approval='公式2025/6/13：人が結果を確認・調整し、実行を承認する方針。I/O・HMIの変更反映、実機適用の個別権限は未確認',delta_interpretation='PLC・I/O・スケッチからのHMI作成は2025/6に説明済み。2024展示との差は未確定。2026をI/O・HMI支援の初登場とはしない。'),
  'FC013':dict(source_ids=['ERF-02'],limits='10/18の製品ページでも製品発表・投入時期要問合せ。命令ごとの許可・人の承認・二重実行防止・失敗復帰は未記載。Engineeringの承認方針だけでOperationsの毎回承認を断定しない'),
  'FC020':dict(source_ids=['ERF-03']),
  'AC131':dict(source_ids=['ERF-04']),
  'FC036':dict(source_ids=['ERF-05'],human_approval='公式：人が良否アノテーションを追加。更新モデルの採用承認、独立評価・旧版への差戻し、最終出荷判定は未記載'),
  'AC273':dict(source_ids=['ERF-06','ERF-07','ERF-08','ERF-09'],limits='TRINIXは物理属性の推論と自己修正を説明済み。NVIDIAのアセット検証は周辺基盤の既存機能で、TRINIXへの搭載確認とは別。DexBenchは共同開発告知。実測正解・収束条件・実機誤差と公開ベンチの提供範囲は未確認'),
  'AC234':dict(source_ids=['ERF-10','ERF-11'],baseline_2024='公式社名変更告知で旧社名ユシロ化学工業と照合。2024のE1005ではクーラントのリモート監視システムとフレキシブル濃度補給装置を掲載。',delta_type='旧社名照合：監視・補給は2024既存、ALFRED固有差未確定',delta_interpretation='2025/4/1の社名変更を公式確認。ALFREDの初公開と、監視・濃度補給方式の初登場を分離。2024装置と同じ製品か、濃度補給機能を継承したか、AI利用は未確認。',source_status='公式出展説明まで・ALFRED追加仕様未確認／2024旧社名原典と社名変更を補足照合',limits='旧社名の2024原典を照合済み。ALFREDの自動補給・AI判断・2024装置との接続／機能差は未確認。2024濃度補給の説明をALFREDの仕様へ流用しない'),
  'AC136':dict(source_ids=['ERF-12'],limits='10/18のW1069公式合同掲載でも条件目安・共有まで。AIの算定、考慮制約、実加工の確認手順は未公開。補足技術資料未確認を保持'),
  'FC049':dict(source_ids=['ERF-13']),
 }
 for cid,changes in updates.items():
  c=by[cid];d=c['deepening']
  for key,value in changes.items():
   if key=='source_ids':continue
   if key in ['baseline_2024','delta_type','delta_interpretation']:c[key]=value
   else:d[key]=value
  for eid in changes['source_ids']:
   if eid not in c['evidence_ids']:
    c['evidence_ids'].append(eid);c['source_locations'].append(dict(evidence_id=eid,url=evidence[eid]['url'],locator=evidence[eid]['locator']))
   if eid not in d['source_ids']:d['source_ids'].append(eid)
  c['mechanism']=d['ai_judgment'];c['output']=d['execution']
  c['human_boundary']='事前準備：'+d['human_preparation']+'／承認：'+d['human_approval']+'／例外対応：'+d['human_exception']
  c['unresolved']=d['limits']+' 現地質問は追補の確認表を参照。'
  if cid=='AC234':c['review_depth']='2024・2026の原典全文を重点比較（公式社名変更で照合・10/18追補）'
  r=next(r for r in reviews if r['card_id']==cid)
  for key in ['human_approval','limits','source_status']:r[key]=d[key]
  for key in ['baseline_2024','delta_type','delta_interpretation']:r[key]=c[key]
  r.update(evidence_ids=c['evidence_ids'],source_urls=[evidence[e]['url'] for e in c['evidence_ids']],checked_date=DATE)
 for r in category_rows:
  if r['card_id'] in updates:
   c=by[r['card_id']];r['evidence_ids']=list(dict.fromkeys(r['evidence_ids']+c['deepening']['source_ids']));r['source_urls']=list(dict.fromkeys(evidence[e]['url'] for e in r['evidence_ids']))
 for r in screening:
  if 'AC234' in r['card_ids']:r['reason']+=' 10/18追補：公式社名変更で旧社名の2024原典を照合。監視・補給の継続とALFRED固有差を分離。'
 aliases=[dict(alias_id='ALIAS01',company_2024='ユシロ化学工業株式会社',company_2026='株式会社ユシロ',effective_date='2025-04-01',basis='公式社名変更告知の旧・新社名と変更日で確認',evidence_ids=['ERF-10','ERF-11'],source_urls=[evidence[e]['url'] for e in ['ERF-10','ERF-11']],scope='この1社の分析上の照合。年度別原マスターを改変しない。',checked_date=DATE)]
 return aliases,dict(checked_date=DATE,source_records=len(SOURCES),updated_cards=len(updates),updated_companies=len({by[c]['company'] for c in updates}),alias_confirmations=1,scope='未確認事項の追補。28社全資料の全件再取得ではない。',cache_files=9,limits=['Beckhoff2025記事は検索索引で確認。本文openは404、誌面PDFは容量超過。','カネテックLPは再度Cache miss。別サイトで回避せず、既存の公式索引確認と質問を保持。','ALFREDの2026詳細ページのweb抽出は失敗。保存済み10/16原文を保持。追加仕様は未確認。'],remaining=['ToolDiscoveryのAI算定方式・制約、ALFRED固有仕様は公開資料で補完できず現地確認へ。','実機の停止・再試行・復帰と操作権限は製品別に確認待ち。確認表12件を保存。','研究候補は公開情報に基づく条件付き判断。実験・現地検証・最終1枚は未実施。'])


ASSESSMENTS=[
 ('T01','優先検証：既存CAMとの連携へ限定','加工性評価、工程の編集・シミュレーション・NC生成は既存機能。顧客のMastercamデータを学習しないという説明も確認。','生成器の再開発より、工具・保持・機械・版変更による修正理由と検証結果の対応付けを検討。','同じ部品の生成前後CAM、ポスト後NC、変更した制約と人の修正理由を見せてもらう。','既存CAM／検証製品を使った総工数を測れること。既存連携のみで十分なら研究を縮小。',['FC020','AC131','FC021'],['ERF-03','ERF-04','EDP-20']),
 ('T02','条件付き優先：操作APIと権限の確認待ち','Engineeringは専門家の承認方針を説明済み。Operationsは命令実行を掲げるが提供時期・許可範囲は未確定。','承認画面そのものより、許可済み命令の実行前状態・二重実行防止・失敗後の再開整合性に範囲を絞る。','Operationsの読取／書込命令、承認単位、実行ID、通信断時の扱いを限定デモで確認。','利用可能APIとログ、模擬設備での評価許可が必要。なければ読取・提案支援までにする。',['FC011','FC012','FC013','FC024','AC295'],['ERF-01','ERF-02','EDP-06','EDP-18']),
 ('T03','現地確認優先：作業完了と引継ぎを限定評価','TAKISAWAは切粉除去を参考出品。Kanetecは既存ピックにAI明示、TEDは3D軌道生成だが学習AIは未確認。','AIという名称で統一せず、切粉除去／部品ピックを別タスクとして完了判定・限定再試行・人の復帰を比較。','除去未完了・複数個把持等の失敗例、検出信号、停止と人への引継ぎを見せてもらう。','対象・成功条件・接触制限・取得可能ログが確認できてから実験。参考展示だけで実用効果を判定しない。',['FC049','AC051','AC146','FC031'],['ERF-13','EDP-01','EEX-WTED','EDP-24']),
 ('T04','既存製品活用優先：追加学習の研究は縮小','ZEROは良品学習、良否の追加アノテーション、異常箇所表示を提供。追加学習そのものは研究の空白ではない。','条件別の独立評価・更新承認・旧版への差戻しに、現場で未充足の要求があるかを先に確認。','更新前後の別データ評価、版管理、更新の採否・復旧画面、現場のラベル工数を確認。','既存製品設定で十分なら導入・運用改善にとどめる。条件別悪化と総工数を測れる場合だけ研究化。',['FC036','FC039','AC225'],['ERF-05','EDP-14','EDP-12','EDP-13']),
 ('T05','条件付き優先：既存検証後の実機差に限定','物理属性生成・自己修正はTRINIXの説明範囲。周辺基盤には静的アセット検証があり、DexBench共同開発も告知。','属性チェックや一般ベンチを再実装せず、製造タスクの接触条件で残る実機差と、どの属性を直すべきかの評価へ絞る。','推定／実測の属性、自己修正の誤差指標、使う検証ルール、DexBenchの公開範囲を確認。','利用可能なモデルと測定できる実機課題が前提。既存チェック・ベンチで解決するなら独自開発を見送る。',['AC273','AC098','FC021'],['ERF-06','ERF-07','ERF-08','ERF-09','EDP-17','EDP-20']),
]

QUESTIONS=[
 ('Q01',['AC136'],'ToolDiscoveryのAI条件目安','工具・被削材・加工方法から条件を表示・共有。','AIは何を最適化し、機械剛性・突出し・保持を考慮するか。成立しない条件を警告するか。','同一工具・材種で保持や機械条件だけを変えた算定例。','考慮制約と適用外条件が示せれば条件助言の比較へ進む。','追加技術資料未確認。計算・学習方式と実加工の承認は保留。',['ERF-12']),
 ('Q02',['AC234'],'ALFREDと2024監視・補給の差','旧社名を照合し、2024の遠隔監視・濃度補給を確認。','ALFREDは2024装置のどこを変更したか。自動補給は接続できるか。AI判断は存在するか。','両年の構成図・型式、pH／濃度センサと補給系統、校正・汚れ時の画面。','固有差と実行範囲が分かれば監視／制御を区別して更新。','2024の補給機能をALFRED仕様として流用しない。',['ERF-10','ERF-11']),
 ('Q03',['FC011','FC012'],'CoAgent Engineeringの実行承認','2025資料で専門家による確認・確定・承認方針。','生成案の採用と、コンパイル・PLC書込・運転開始は別の承認か。誰が変更履歴を戻せるか。','生成案→差分→承認→適用の画面と、権限別の操作ログ。','設計成果物と実機操作の境界が分かればT02の範囲を決める。','一般方針から毎回承認・安全機能の搭載を推測しない。',['ERF-01']),
 ('Q04',['FC013','FC024'],'Operationsの命令・権限・復帰','命令実行を説明。提供時期要問合せ。MCP Adapterは提供計画。','読取と書込の許可、毎回承認、古い状態・通信断・二重実行、失敗後の再開はどう扱うか。','許可命令一覧、状態前提、失敗ログ、権限設定と実行ID。','APIとログを使えるなら模擬PLCで整合性評価。','公開ページで未確認。Engineeringの方針をOperationsの実装証拠にしない。',['ERF-02','EDP-06']),
 ('Q05',['FC020','AC131','FC021'],'生成CAM→ポスト後NCの検証','人が案を調整し、既存の検証・NC生成へ進む。','工具・保持・機械・ポストの版変更が生成案とNCにどう反映され、未検出制約を誰が直すか。','同一部品の条件変更例、編集前後CAM、NC検証結果、修正理由。','既存フローとの差分・総工数が測れるならT01を検証。','ベンダー間の実装済み自動連携は未確認。',['ERF-03','ERF-04','EDP-20']),
 ('Q06',['FC049'],'TR-20Wの切粉除去と失敗復帰','主軸切粉を認識・判断・除去する参考出品。','完了は何で検知し、除去できない切粉・接触・工具異常でいつ止め、何回再試行するか。','正常／未完了の動画と判定信号、力・接触条件、人への通知と再開手順。','取得可能信号と限定タスクを確認後にT03の実験を定義。','現地未検証。センサ種・力制限・成功率は未公開。',['ERF-13']),
 ('Q07',['AC051'],'磁気ピックのAI担当と二個取り','2Dカメラ・協働ロボット・磁気把持。AIの担当未特定。','AIは検出・把持点・複数個吸着・再試行のどこを判断するか。誤把持をどう検知するか。','AI入出力、空振り／二個取りの失敗判定と人への引継ぎ。','AI担当と成否判定が分かればT03の比較例へ。','LP本文取得はCache miss。既存方式とAI追加時期は区別。',['EDP-01']),
 ('Q08',['AC146'],'TEDの形状認識→加工許可','レーザ3D形状から軌道生成し面取り等を説明。','学習AIを使うか。干渉・取り残しをどう確認し、反り・二枚取りで止めて誰が再開するか。','入力スキャン、生成軌道、干渉確認、許可画面、失敗時ログ。','方式と許可・停止条件が分かればAI方式と幾何方式を比較。','教示不要を無制限の未知形状対応としない。',['EEX-WTED']),
 ('Q09',['AC085'],'GH5の補正上限と測定異常','人の目標幅・角度に対して画像測定と自動調整。','補正上限、測定不能・過研磨の停止判定、目標変更の権限、完了確認は何か。','設定値と測定値・補正量の履歴、限界例と停止復帰の説明。','補正の範囲・成否指標が開示されればT03の閉ループ比較。','PDF本体は容量上限で未取得。索引確認の範囲を越えない。',['EDP-02']),
 ('Q10',['FC036','FC039','AC225'],'検査・診断モデルの更新採否','ZEROは人の追加ラベルを利用。画像・時系列診断は用途で基準が違う。','更新前後を別データで比較できるか。誰が採用し、条件別悪化で旧版に戻せるか。','更新履歴、独立評価群、条件別の見逃し・過検出、採否・差戻し画面。','既存機能で不足する要求が確認された場合のみT04を研究化。','追加学習があるだけで独立評価・自動差戻しがあるとはしない。',['ERF-05','EDP-12','EDP-13']),
 ('Q11',['AC273'],'SimReadyの自己修正と実物の差','TRINIXは属性推論・自己修正、周辺基盤はアセット検証。','誤差の正解・収束条件は何か。推定値と実測値を分けられるか。DexBenchは何が利用可能か。','属性の由来、修正履歴、検証ルール、実機との比較、公開成果物の範囲。','モデル・実測対象が使えるならT05の限定比較。','公式共同開発告知は完成標準や性能保証とは別。',['ERF-06','ERF-07','ERF-08','ERF-09']),
 ('Q12',['FC030','AC039','AC186'],'予測→搬送指示→停止復帰','Fleeterは上位命令、FNSは統合指示、白山はAMR回収を説明。','予測が実際に配車・計画を変えるか。遅延・機械停止・回収失敗で誰が再計画し承認するか。','上位命令と装置状態の時系列、遅延時の画面、再計画と人の引継ぎ。','判断と指令の接続・権限が確認できればT02／T03の拡張例。','AIによる再計画や予測からの自動指令は未確認。',['EDP-21','EDP-22','EDP-25','EDP-29']),
]

def enrich_synthesis(data,cards,evidence):
 by={c['card_id']:c for c in cards}
 def attach(r,eids):
  r['evidence_ids']=list(dict.fromkeys(r['evidence_ids']+eids));r['source_urls']=[evidence[e]['url'] for e in r['evidence_ids']];r['source_locators']=[f"{e}: {evidence[e]['locator']}" for e in r['evidence_ids']]
 def row(stem,key,value):return next(r for r in data[stem] if r[key]==value)
 for r in data.values():
  for x in r:x.update(analysis_date=DATE,supplement_checked_date=DATE)
 m=row('method_comparison','method_id','M01');m['year_change']='PLC支援は2023、I/O・HMI支援と人の承認方針は2025/6に説明済み。2026のOperationsは製品発表・投入時期要問合せ。';m['human_boundary']='人が要求・スケッチ等を用意。Engineeringは専門家が結果を確認・承認する方針を明示。Operationsの命令単位の承認は別途確認。';attach(m,['ERF-01','ERF-02'])
 m=row('method_comparison','method_id','M10');m['year_change']='ToolDiscoveryは2024比較不能。ユシロは公式社名変更で2024の遠隔監視・濃度補給を照合。ALFRED固有差は未確定。';attach(m,['ERF-10','ERF-11','ERF-12'])
 y=row('year_change_patterns','change_id','Y01');y['current']='CoAgentのI/O・HMI支援と専門家の確認・承認は2025/6に説明済み。2026はOperationsの診断・命令実行を説明。';y['interpretation']='I/O・HMIを2026の初搭載としない。Operationsは製品発表・投入時期要問合せ。個別の操作権限・復帰は未確認。';attach(y,['ERF-01','ERF-02'])
 y=row('year_change_patterns','change_id','Y05');y['pattern']='接続・監視基盤の具体化';y['baseline']='たけびしは2024にOPC UA接続。ユシロは旧社名で遠隔監視・濃度補給を掲載。';y['current']='2026はMCP Adapter提供計画、TRINIXのSimReady生成、ALFREDのコントローラー・監視画面を説明。';y['interpretation']='ユシロを社名変更で照合。監視方式そのものは既存。ALFRED固有差・AI・自動補給は未確認。MCP計画と実装も分ける。';y['card_ids'].append('AC234');attach(y,['ERF-10','ERF-11'])
 y=row('year_change_patterns','change_id','Y06');y['card_ids'].remove('AC234')
 for iid,eids in [('I01',['ERF-03','ERF-04']),('I02',['ERF-02']),('I03',['ERF-13']),('I04',['ERF-05']),('I05',['ERF-06','ERF-07','ERF-08','ERF-09'])]:attach(row('common_issues','issue_id',iid),eids)
 i=row('common_issues','issue_id','I05');i['limits']='静的なアセット検証は既存。NdotLightはDexBench共同開発も告知。独自研究は既存機能との重複を避け、実物との差・適用条件の未確認部分へ絞る。'
 for tid,decision,existing,hypothesis,first,gate,ids,eids in ASSESSMENTS:
  t=row('research_candidates','theme_id',tid);t.update(decision=decision,existing_capabilities=existing,remaining_hypothesis=hypothesis,check_first=first,experiment_gate=gate,assessment_date=DATE,assessment_status='公開情報に基づく条件付き判断。実験・採用決定は未実施。')
  t['stage']='研究開発候補・未採否／'+decision
  if tid=='T01':t['technical_approach']='既存CAM・NC検証を使い、工具／ホルダ・保持・機械・ポストの版変更から、生成案の修正と検証結果までの差分を対応付ける。修正理由の再利用はローカルな作業知識として扱い、顧客データの外部学習を前提にしない。'
  if tid=='T02':t['technical_approach']='製品が備える承認・権限設定を先に確認。その上で、限定命令の実行前状態・実行ID・重複防止・失敗後の再開整合性を評価する。公開APIの範囲を越える実機操作は研究の前提にしない。'
  if tid=='T04':t['technical_approach']='既存の良品学習と追加アノテーションを利用し、更新前後を条件別の独立データで比較する。更新承認・版管理の既存実装を確認し、不足する評価手順や採否判断だけを研究範囲とする。'
  if tid=='T05':
   t['technical_approach']='既存のアセット検証と実行時確認を通したモデルを基準に、推定／実測の物理属性とその誤差を記録する。製造タスクの限定接触で仮想と実機を比較し、修正すべき属性と作業結果の対応を評価する。'
   t['experiment']='単純形状の把持・配置に限定し、同じ検証を通した生成属性／実測属性／手作業モデルを比較。既存ベンチの利用範囲と重複を先に確認し、一般ベンチの新設を目的にしない。'
  # Comparison cards can span more than one issue; retain the original factual basis too.
  t['card_ids']=list(dict.fromkeys(t['card_ids']+ids));attach(t,eids)
  issue=row('common_issues','issue_id',t['issue_id']);issue['card_ids']=list(dict.fromkeys(issue['card_ids']+ids));attach(issue,eids)
 questions=[]
 for qid,ids,title,fact,question,proof,gate,hold,eids in QUESTIONS:
  questions.append(dict(question_id=qid,title=title,companies=list(dict.fromkeys(by[c]['company'] for c in ids)),booths_2026=list(dict.fromkeys(b for cid in ids for b in by[cid]['booths_2026'])),known_facts=fact,question=question,requested_evidence=proof,experiment_gate=gate,unresolved=hold,card_ids=ids,evidence_ids=eids,source_urls=[evidence[e]['url'] for e in eids],status='公開情報で未解決・現地／技術担当への確認待ち',checked_date=DATE))
 return questions


def followup_html(data,coverage):
 import html
 H=lambda x:html.escape(str(x),quote=True)
 def refs(r):return ' '.join(f'<a href="#{cid}">{cid}</a>' for cid in r['card_ids'])+'<details><summary>根拠</summary>'+''.join(f'<p><a href="#{eid}">{eid}</a></p>' for eid in r['evidence_ids'])+'</details>'
 out=['<section id="followup"><h2>10/18追補：未確認事項と研究候補を絞る</h2><p>公式根拠13件を追補し、10カードを更新しました（既存ページの再確認・保存済み2024原典の再読を含む）。全出展社・全資料の再取得ではありません。</p><div class="guide"><div><h3>ユシロの2024基準を補完</h3><p>公式社名変更で旧社名を照合。遠隔監視・濃度補給は2024にも掲載。ALFREDの初公開と、監視方式の初登場を分けました。</p></div><div><h3>承認方針は既存</h3><p>CoAgent EngineeringのI/O・HMI支援と専門家の確認・承認は2025に説明済み。Operationsの命令単位の権限や失敗復帰とは別に確認します。</p></div><div><h3>研究の空白を再点検</h3><p>CAMの検証、ZEROの追加学習、SimReadyの属性チェックは既存機能です。研究候補はその先の制約変更・更新採否・実機差へ限定します。</p></div></div><p class="note">公開情報不足は機能の不存在を示しません。実験・現地実演・導入効果は未検証。1枚への集約は未着手です。</p><h3>研究候補5件の現時点の扱い</h3><div class="scroll"><table><thead><tr><th>候補・扱い</th><th>既存機能</th><th>残る研究仮説</th><th>最初の確認・開始条件</th><th>根拠</th></tr></thead><tbody>']
 for r in data['research_candidates']:
  out.append(f'<tr><td><a href="#{r["theme_id"]}"><b>{r["theme_id"]} {H(r["theme"])}</b></a><p>{H(r["decision"])}</p></td><td>{H(r["existing_capabilities"])}</td><td>{H(r["remaining_hypothesis"])}</td><td>{H(r["check_first"])}<p class="note">{H(r["experiment_gate"])}</p></td><td>{refs(r)}</td></tr>')
 out.append('</tbody></table></div><details><summary>公開情報で残った12論点：企業・ブース、質問、見たい証拠、研究の開始条件</summary><div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['論点／訪問先','確認した事実','現地・技術担当への質問','見たい証拠','開始条件・保留する点','根拠'])+'</tr></thead><tbody>')
 for r in data['open_questions']:
  out.append(f'<tr id="{r["question_id"]}"><td><b>{r["question_id"]} {H(r["title"])}</b><p>{H("・".join(r["companies"]))}<br>{H("・".join(r["booths_2026"]))}</p></td><td>{H(r["known_facts"])}</td><td>{H(r["question"])}</td><td>{H(r["requested_evidence"])}</td><td>{H(r["experiment_gate"])}<p class="note">{H(r["unresolved"])}</p></td><td>{refs(r)}</td></tr>')
 out.append('</tbody></table></div></details><p><a href="../data/research/technology_atlas_v1/open_questions.csv">確認表CSV</a> ／ <a href="../data/research/technology_atlas_v1/company_alias_confirmations.csv">社名変更照合CSV</a></p></section>')
 return ''.join(out)
