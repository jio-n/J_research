"""Compile the manually read strategy evidence; no automated keyword inference."""
from pathlib import Path
import json
import html
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/research/strategy_keywords_20261021'
OUT.mkdir(parents=True, exist_ok=True)
sources = []
def source(id, publisher, title, date, kind, url, locator, context, scope='本文の該当節を確認', extra_urls=None):
    sources.append(dict(id=id, publisher=publisher, title=title, published_date=date, kind=kind, url=url, extra_urls=extra_urls or [], locator=locator, context=context, reading_scope=scope, checked_date='2026-10-21'))

source('S01','産総研','製造AX拠点を始動','2026-07-02','公的研究機関の構想',
 'https://www.aist.go.jp/aist_j/news/pr20260702.html','「産総研を核とした製造AX拠点」「GENIAC事業の活用」',
 '現象理解を踏まえるデータ取得、外部利用可能なデータ整備、モデル開発、現場への還元を担う構想。個社の開発だけで完結しない仕組みを示す。')
source('S02','DMG森精機','GENIAC事業に採択：生産設備データエコシステムと製造フィジカルAI基盤','2026-07-06','企業の開発計画',
 'https://www.dmgmori.co.jp/corporate/news/2026/20260706_geniac.html','協力企業・設備数、データ整備、権利処理の段落',
 '協力企業約100社・約1,000台、約100TB規模のデータ整備を計画。匿名化・構造化・権利処理を経てAI開発等へ利用する方針。完成済みの規模ではない。','検索結果の本文抽出を確認・直接オープン未確認')
source('S03','MONOist／WALC・DMG森精機の取材発言','DMG森精機が挑む工作機械のフィジカルAI','2026-07-08','取材記事・当事者発言',
 'https://monoist.itmedia.co.jp/mn/articles/2607/08/news026.html','「100社、1000台の設備から最大1kHz」「工作機械におけるフィジカルAIの姿」',
 '物理現象を捉える時間粒度と社会実装負荷を考慮して取得周期を選ぶ説明。異常検知、品質・電力予測、生産セルへの段階展開と、物理モデル活用の考えを示す。')
source('S04','ABEJA','マザックと製造現場のフィジカルAI実装に向けた業務連携','2026-10-16','企業の共同開発計画',
 'https://www.abejainc.com/news/20261016/2','共同開発の概要（1）〜（3）・今後の展望',
 '加工工程・スケジュールのエージェントとロボット学習環境を開発する方針。人の関与と顧客環境への継続適応を打ち出す。販売・運用実績の証明とは区別。')
source('S05','MONOist／マザックの取材発言','加工の工程設計をAIエージェントで自動化','2026-10-19','取材記事・当事者発言',
 'https://monoist.itmedia.co.jp/mn/articles/2610/19/news039_2.html','「人の『意図』を学習」「ノウハウを学び固有モデルへ」',
 'マザトロールの構造化された加工意図、顧客修正の追加学習、自社データによる基盤モデルと顧客固有モデルの関係を説明。PoC段階で提供形態は未確定。',
 extra_urls=['https://monoist.itmedia.co.jp/mn/articles/2610/19/news039.html'])
source('S06','ファナック・日立','フィジカルAI実装の共同事業化に向けた戦略的パートナーシップ','2026-09-30','企業の共同実証・展開計画',
 'https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260930.html','共同実証の概要・戦略的パートナーシップの背景',
 '固定条件で対応しにくい段取り替え等を対象に、日立の工場を実証先とする。現場ルールを学習し、実装・運用経験を他の顧客へ展開する計画。')
source('S07','MONOist／ファナックの取材発言','ファナックとフィジカルAI、現場主義の開発思想','2026-07-02','取材記事・当事者発言',
 'https://monoist.itmedia.co.jp/mn/articles/2607/02/news043.html','全3ページ：開発思想、学習の横展開、オープン化、ソフトPLC',
 '顧客の困りごとを出発点とし、学習成果の他拠点への還元と外部AIの取り込みを構想。現状の横展開の不足、データ主権、ロボット側の制御保護にも言及。',
 extra_urls=['https://monoist.itmedia.co.jp/mn/articles/2607/02/news043_2.html','https://monoist.itmedia.co.jp/mn/articles/2607/02/news043_3.html'])
source('S08','ファナック','Googleの技術を活用したAIエージェントがロボットを操る','2026-05-13','企業の技術・実演発表',
 'https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260513.html','オープンプラットフォーム・Geminiによるセル実演の説明',
 '自然言語の指示、物体認識、複数ロボットの動作を結ぶ実演を紹介。外部AI開発環境と既存ロボット群を接続する戦略の資料。')
source('S09','ファナック・富士通','フィジカルAIの社会実装に向けた事業検討','2026-07-16','企業の協業検討',
 'https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260716.html','背景・富士通社長コメント',
 'ロボット、設備、人、業務アプリを結び、計画から実行・品質・保守までの最適化を目指す。検討開始という段階を保持する。')
source('S10','NEC','AIネイティブに向けて進化する製造業変革コンセプトMX','2026-08-19','企業の構想・対談',
 'https://jpn.nec.com/manufacture/monozukuri/iot_mono/2026-08/02.html','5つのバリューチェーン・AI-Ready Data・チェーン横断の協創空間',
 '設計・調達・生産等の連携と、部門の異なる目的を持つエージェントの協調を構想。完成した一式のサービスではないと明記。DMGのMXとは別の用語。')
source('S11','Siemens','From agile to autonomous: adaptive production','2026-07-08','企業の戦略解説',
 'https://blogs.sw.siemens.com/nx-manufacturing/from-agile-to-autonomous-building-adaptive-production-with-digital-twins-and-industrial-ai/','data continuity・always-live twin・scaling problem',
 '設計と運用の連続データ、現状を反映するツイン、追跡可能な実行を重視。既設設備への接続、横展開、意思決定権限を課題とする。実績・優位性の表現は自社主張。')
source('S12','Siemens','CES 2026：産業用AI革命を加速するテクノロジー','2026-01-06','企業の製品・提携発表',
 'https://press.siemens.com/jp/ja/pressrelease/pr-20260106-1','Digital Twin Composer・NVIDIA提携・バリューチェーンのCopilot',
 'リアルタイム情報、シミュレーション、産業ソフトを結ぶ方針。個別支援機能に加え、設計・生産・運用をまたぐ基盤の競争を示す。JIMTOF出展確認とは別。')
source('S13','東芝／東芝・Microsoftの対談','製造現場の知見を生かしてAIエージェントを活用するには（2/2）','2026-03-06','当事者対談',
 'https://www.global.toshiba/jp/company/digitalsolution/articles/digicon/2026/82-2.html','4〜6節：データ整備、人材、共創',
 '装置ログに報告や周辺情報を添える必要、入力負荷、標準化、計算処理とAIの分担を議論。工場全体へ広げる際のデータ・業務の難しさにも言及。')
source('S14','Hexagon／製品技術担当者','The next step in CAM isn’t new. It’s already here.','2026-04-29','企業の顧客対話・製品解説',
 'https://blog.manufacturing.hexagon.com/advanced-manufacturing/cam-software/the-next-step-in-cam-isnt-new-its-already-here/','Real needs・Where the real friction sits・shared capability',
 '過去の加工判断を毎回組み立て直す負担と、ソフトが自分の仕事の進め方を学ぶニーズを紹介。機能の追加だけでなく判断の再利用・一貫性を価値とする。')
source('S15','Hexagon／製品担当者','Tailored vs Cloud AI: CAM automation path','2025-10-01','企業の方式比較',
 'https://blog.manufacturing.hexagon.com/advanced-manufacturing/cam-software/tailored-vs-cloud-ai-choosing-the-right-cam-automation-path/','Tailored solutions・Cloud-based AI・combined solution',
 '反復業務に合わせる個別構築と、多様な部品へ適応するクラウド型の違いを説明。両者を組み合わせる選択肢も提示。メーカーの方式比較として扱う。')
source('S16','umati','About: vision, promise, mission','', '標準化団体の説明',
 'https://umati.org/about/','vision・promise・setting the standard',
 'OPC UAの共通意味定義と実装要件を通じ、機械とITの接続負荷を減らす。接続規格への対応だけで工程全体の制御が完成するとは解釈しない。')
source('S17','山善・ものづくり研究所','EMO2025から考える技術トレンドとJIMTOF2026の注目点','2026-02-19','商社の展示会解説・見解',
 'https://monoken.yamazen.co.jp/blog/articles/jimtof/emo-hannover2025-report','技術テーマ・JIMTOFの注目テーマ',
 '前後作業・人の動きまで含む工程設計、段取り、日々の設定・管理負担を着眼点に挙げる。引用元と執筆者の見解が混在するため独立した実証数とは数えない。')
source('S18','Mono Que／日本物流新聞','JIMTOF2026：注目の出展内容を速報＆フカボリ','2026-10-13（更新表示）','業界紙の取材・展望',
 'https://monoque.jp/feature/contents/f9797930f725f7ac84f44b2030940395c12f5a47/','冒頭の市場・出展動向、工程集約とフィジカルAI',
 '顧客の実利に沿う多様な出展になると展望。AIだけで全展示を説明せず、工程集約や他の改善技術と並行して見る根拠になる。')
source('S19','日本工作機械輸入協会','JMTIA NEWS 223号：2026年年頭所感','2026','業界団体会長の見解',
 'https://www.jmtia.gr.jp/uploads/photos1/286.pdf','PDF 3ページ目（印刷ページ2）、年頭所感',
 '安定した品質・生産性の長期維持と、生産システム全体の提案を重視する見解。定型生産に従来型設備が持つ強みも述べる。','PDFの年頭所感のみ確認・全28ページ精読ではない')
source('S20','日本総研','フィジカルAIを日本の勝ち筋にするために','2026-08-14','調査機関の見解',
 'https://www.jri.co.jp/page.jsp?id=114749','公表要旨のフィードバックループ',
 '顧客課題への小さな導入、実環境データによる改良、新規開発を循環させることを提言。日本に優位があると自動的に見なさない点も重要。','HTML公表要旨を確認・PDF本文未確認')
source('S21','KPMGコンサルティング','フィジカルAIで変わるロボティクスの競争条件','2026-08-18','コンサルティング会社の分析',
 'https://kpmg.com/jp/ja/insights/2026/08/ai-emergingtech-10.html','2つのループ・導入後の改善力・投資評価',
 'その場の実行と学習更新を区別。失敗・修正・環境条件を対応させる運用、現場全体の制約に基づく効果評価を重視する分析。')
source('S22','オークマ','JIMTOF2026特設サイト','', '公式展示予定',
 'https://www.okuma.co.jp/english/show/jimtof/2026/','Three Solutions for Enhanced Productivity',
 '工程集約、多品種少量の自動化、AI・知能化を並列に提示。現場価値の実現手段がAIだけでないことを展示構成でも確認できる。')
source('S23','安川電機','決算補足説明資料：AIロボティクス領域拡大','2026-01-09','企業の事業・技術説明',
 'https://www.yaskawa.co.jp/wp-content/uploads/2026/01/20260109_haihu.pdf','PDF 16ページ目、スライド15',
 'モーションとAIの融合を掲げ、変種変量、人の実演による教示、未自動化作業への適用を提示。個別作業の成果を工場全体の自律化実績とはしない。','PDFの関連スライドを確認')
source('S24','MONOist／DMG森精機社長インタビュー','工作機械のソフトウェアデファインド化とMX','2025-09-26','当事者インタビュー',
 'https://monoist.itmedia.co.jp/mn/articles/2509/27/news004.html','全2ページ：アプリ追加、更新、CAD/CAM・ERP接続、ツイン',
 '機械にアプリを追加・更新し、CAD/CAMから工具管理・ERPまで接続する構想を説明。シミュレーションとAIを組み合わせる発想にも言及。',
 extra_urls=['https://monoist.itmedia.co.jp/mn/articles/2509/27/news004_2.html'])
source('S25','MONOist／DMG森精機社長インタビュー','工作機械の各ユーザーにAIエージェントを','2026-06-15','当事者インタビュー',
 'https://monoist.itmedia.co.jp/mn/articles/2606/15/news047_2.html','「工作機械の各ユーザーにAIエージェントを」',
 '加工・修理・試験加工の経験を、工具や保持方法の提案、復旧支援、開発へ活用する将来像。顧客向け価値と社内開発の改善を同じ知識資産で結ぶ。')
source('S26','DMG森精機','CELOS ClubにCondition Agentを搭載','2026-07-06','企業のサービス発表',
 'https://www.dmgmori.co.jp/corporate/news/2026/20260706_conditionagent.html','サービスの導入・標準搭載・予兆保全の説明',
 '自動化で停止影響が増すことを背景に、設備保全をデジタルサービスへ組み込む。AIサービスの価値と課金・利益率の実績は別々に確認すべき。','検索結果の本文抽出を確認・直接本文未確認')
source('S27','DMG森精機','2026年度上半期決算リリース','2026-08-04','企業IR・経営方針',
 'https://www.dmgmori.co.jp/corporate/ir/ir_news/2026/20260804_release.html','MRO等の利益率寄与・Machining Intelligence・GENIAC',
 '加工ノウハウの活用と、高い限界利益を持つMRO等の拡大を説明。ただしMROの収益性をAIサブスク単独の収益性に読み替えない。','検索結果の本文抽出を確認・直接本文未確認')
source('S28','DMG森精機','統合報告書2022：サービス・デジタル垂直統合','','企業IR・過去の計画',
 'https://www.dmgmori.co.jp/corporate/ir/ir_library/pdf/2022_ar_j.pdf','VALUE CHAIN・テクニウムのサービス説明',
 '生産計画ソフトの定額提供と機械データ・セル制御・工具管理の接続方針が既に示されている。2026年に初めて登場した発想とはしない。','検索結果の本文抽出を確認・PDF本体未確認')
source('S29','DMG森精機','統合報告書2025ダイジェスト：MROと開発の連環','2026','企業IR・対談',
 'https://www.dmgmori.co.jp/corporate/ir/ir_library/pdf/2025_ir_digest_j.pdf','エンジニアリング商社モデル・MROと開発の連環',
 '平均復旧時間の短縮と、現場の不具合経験を開発へ返す仕組みを説明。エンジニアリングチェーン全体の販売と同義には扱わない。','検索結果の本文抽出を確認・PDF本体未確認')
source('S30','経済産業省・GENIAC','データエコシステム採択事業者（第4期）','', '公的事業の採択説明',
 'https://geniac.meti.go.jp/selection_4/data/index.html','FingerVision等の共同開発概要',
 '視覚だけでなく触覚・言語・動作を扱うモデルと、そのためのデータセット設計を掲げる共同事業。参加可能性や利用条件は個別確認が必要。')
source('S31','三菱電機・アーヘン工科大学','CNC上で加工誤差を補正するエッジデジタルツイン','2026-03-25','企業の研究成果発表',
 'https://www.mitsubishielectric.co.jp/ja/pr/2026/0325/','背景・データ選別とコンパクトな物理モデル',
 '高頻度取得と必要情報の選別、物理モデルの小型化、リアルタイム補正を組み合わせる。研究結果の適用条件を一般化しない。AIモデルとの混同も避ける。')
source('S32','Mono Que／日本物流新聞・企業取材','イワタツール：JIMTOFで多企業による多様な提案','2026-10-09','取材記事・展示予定',
 'https://monoque.jp/news/7299bcaab1e600d161b3837c77fb9d51cb916563/','ロボット切削・マルチプロセッシング・加工条件アプリ',
 '工具・ロボット・加工知識を複数企業が持ち寄る出展。画像からのパス生成や複数工程の連続作業を、展示予定として紹介する。')

source('S33','オムロン','IT-OT融合が切り拓く製造業のDX','2026-09-18','企業の戦略・技術解説',
 'https://www.omron.com/jp/ja/edge-link/news/769.html','IT-OT融合が進まない理由・共通言語化・i-BELT Hub',
 '計画と現場の乖離、異なる層に分断したデータを課題とし、実績・原因系の情報・原価を結ぶ構想。データの階層構造と意味付けをエージェント活用の前提とする。')
source('S34','大和総研','フィジカルAIの社会実装に向けた課題','2026-04-24','調査機関の分析',
 'https://www.dir.co.jp/report/research/economics/japan/20260424_025726.html','公表要旨：開発・検証と導入の障壁',
 '開発時の試行環境の不足と、導入時の個別調整・横展開の負担を分けて論じる。モデル性能だけで事業化を説明しないための参考見解。','HTML公表要旨を確認・PDF本文未確認')

keywords = []
def kw(id, group, label, expressions, source_ids, context, question):
    keywords.append(dict(id=id,group=group,label=label,source_expressions=expressions,source_ids=source_ids,context=context,development_question=question,interpretation_type='語群の整理と開発上の問いは本調査の分析'))

kw('K01','ニーズの変化','固定条件の反復から、状況に応じた判断へ',['状況の変化','自律化'],['S06','S07','S23'],'品種や配置、段取りが変わると人の判断が必要になる領域が対象。単なる動作速度の競争から適用できる作業を広げる発想。','顧客が人を残している作業は何か。変化の種類と頻度は何か。')
kw('K02','ニーズの変化','変種変量への対応と再計画',['変種変量生産','生産スケジュールの最適化'],['S23','S04','S05'],'欠品・割込み・設備停止に合わせて工程や優先順位を見直す。柔軟性をロボット動作と工場計画の両面で見る。','正常時の最適化に加え、変更後に実行可能な計画へ戻せるか。')
kw('K03','ニーズの変化','考え直しを減らし、判断を再利用する',['learn how he works','shared capability'],['S14','S05'],'熟練者が毎回再構成する工程・工具・検査の判断を、次の部品や別の担当者で使うニーズ。','出力結果だけでなく、選択理由と修正の履歴を残せるか。')
kw('K04','ニーズの変化','前後作業を含む工程設計',['工程設計','段取り短縮'],['S17','S19','S32'],'段取り・搬送・検査・人の作業を含め、全体の流れとして提案する。個別装置の自動化率だけでは効果が分からない。','前後工程の待ち・持替え・人の介入を含む削減効果は何か。')
kw('K05','ニーズの変化','止めないことと、早く戻すこと',['平均復旧時間','Condition Agent'],['S29','S26','S21'],'自動化の進展で停止の影響が増す。検知だけでなく、原因の切り分け・復旧・保全への接続が価値になる。','検知後、誰のどの行動まで支援すると停止時間が減るか。')
kw('K06','データと現象','現象理解から取得データを設計する',['現象理解','製造データ取得'],['S01','S03','S31'],'取得点・周期・条件・結果の対応を、理解したい現象から設計する視点。汎用的に大量保存するだけでは足りない。','自社の加工現象の知見を、取得設計・評価データのサービスへ展開できるか。')
kw('K07','データと現象','時間粒度と社会実装負荷の両立',['最大1kHz','リアルタイム'],['S03','S31'],'状態監視と加工現象の理解では必要な粒度が違う。高頻度取得、通信・保存・計算負荷の設計を一緒に見る。','何を取り逃すと判断できないか。必要情報だけを残す方法はあるか。')
kw('K08','データと現象','ログに意図・原因・介入を添える',['加工意図','作業報告','意味付け'],['S05','S13','S21'],'機械がどう動いたかに加え、なぜ変更したか、何が起きたかを対応させる。暗黙知の具体的な取得対象が見える。','現場の入力負担を増やさず、理由や修正を自然に回収できるか。')
kw('K09','データと現象','AIが使える形への整備',['AI-Ready Data','共通言語化'],['S10','S13','S16','S33'],'設備・業務・品質を同じ対象や工程に結び、意味のそろった情報にする。接続と利用可能性は異なる。','各社・旧設備のデータを解釈して用途に渡す部分に負担が残っていないか。')
kw('K10','データと現象','横断的なデータ循環と利用条件',['製造データエコシステム','権利処理'],['S01','S02','S30'],'データの整備、外部開発、現場還元を企業間で循環させる構想。利用権や利用目的を整えることも開発基盤の一部。','自前取得・共同取得・外部基盤参加を、用途ごとに選べるか。')
kw('K11','モデルと学習','物理モデルとデータの組み合わせ',['物理モデル','デジタルツイン'],['S03','S24','S31'],'加工の現象モデルと測定情報を組み合わせる方向。学習モデルを大きくする以外にも、ドメイン知識を生かす開発経路がある。','自社の現象モデルが有効な範囲と、実データで補う範囲はどこか。')
kw('K12','モデルと学習','共通の基盤から顧客固有モデルへ',['基盤モデル','ユーザーの固有モデル'],['S05','S04'],'共通データで出発点を作り、顧客の修正や運用で適応する構想。共通化と顧客のノウハウの扱いが重要になる。','顧客ごとの精度改善と、他顧客へ転用できる学びをどう区別するか。')
kw('K13','モデルと学習','導入後に改善する仕組み',['継続的な学習','学習・更新ループ'],['S04','S21','S20'],'現場データ、失敗、人の修正、評価、配信を循環させる。その場の推論・動作変更とモデルの再学習は区別する。','更新が顧客の品質・処理量・介入時間を改善したと確認できるか。')
kw('K14','モデルと学習','一つの現場の学びを別拠点へ',['1台が学んだことを全世界へ還元'],['S07'],'プログラムのコピーに加え、データと最適化成果を展開する将来像。現時点でも容易ではないと当事者が述べる領域。','設備・材料・作業条件の違いを越える適用可否の評価を提供できるか。')
kw('K15','モデルと学習','顧客になる自社工場・実証現場',['カスタマーゼロ','実機での動作検証'],['S06','S04','S13'],'自社工程で学習・検証し、運用経験を顧客サービスへつなぐ。ただし自社の成功だけでは他現場の有効性は確定しない。','自社導入を、顧客向け開発の評価・データ取得の場として使えるか。')
kw('K16','モデルと学習','視覚の先にある接触・力の情報',['VTLA','触覚'],['S30','S23'],'繊細な手作業の対象として、見る情報に触れる情報を組み合わせる開発がある。ロボットの外形だけを見ない。','顧客作業の成否を決める、現在は測れていない情報は何か。')
kw('K17','工程間の接続','設計から運用へ続く情報',['digital thread','5つのバリューチェーン'],['S11','S10','S09'],'計画・設計・実行・品質・保守の情報を連続させ、変更を他工程へ反映する方向。接続範囲は資料ごとに異なる。','自社サービスは何を受け取り、どの工程へ結果を返すのか。')
kw('K18','工程間の接続','実績を次の判断に返す',['always-live twin','改善サイクル'],['S11','S31','S01'],'実データで状態を更新し、予測・判断・制御を変え、結果を確認する循環。可視化画面を作るだけでは閉じない。','提案が実行されたか、品質・計画が改善したかまで追跡できるか。')
kw('K19','工程間の接続','判断と実行を結ぶエージェント',['Agentic AI','Physical AI'],['S04','S08','S09'],'業務上の判断・指示と、機械・ロボットによる作業を接続する。どこまで実行権限があるかを確認する必要がある。','提案・指示生成・自動実行のどこまでを顧客が必要としているか。')
kw('K20','工程間の接続','部門や設備の目的を調整する',['協調','orchestrate decisions'],['S10','S11','S05'],'複数の制約や目的を調整し、設備や人へ役割を割り当てる。単体の最適化を足し合わせるだけでは済まない。','品質・納期・稼働・在庫が衝突したときの優先順位を扱えるか。')
kw('K21','工程間の接続','既設設備の情報を活かしてつなぐ',['Brownfield integration','OPC UA'],['S11','S16','S24'],'既存の機械・ソフト・運用を抱える工場への適用が課題。接続規格、データの意味、更新方法を分けて考える。','設備更新を前提にしない接続・適用方法に価値を出せるか。')
kw('K22','事業と競争','機械の機能をソフトで育てる',['ソフトウェアデファインド','アプリケーション'],['S24'],'出荷後の追加機能や更新を通じて機械の価値を変える。ハードの販売だけでは捉えにくい接点を作る方向。','自社の技術を継続更新する機能・サービスとして提供できるか。')
kw('K23','事業と競争','生産システム全体を提案する',['生産システム全体','一気通貫'],['S19','S17','S24'],'周辺機器・ソフト・運用を含む提案へ対象が広がるという業界の見解。全体を自社だけで保有することとは別。','全体提案の中で自社が担う必須機能や専門サービスは何か。')
kw('K24','事業と競争','継続サービスと顧客接点',['サブスクリプション型','CELOS Club','MRO'],['S28','S26','S27'],'定額ソフトや設備保全のサービスが確認できる。AIの精度向上がそのまま利益率を高めるという因果は、追加検証が必要。','継続して支払われる成果は何か。顧客別調整・運用費用を抑えられるか。')
kw('K25','事業と競争','保守・現場経験を開発へ返す',['MROと開発の連環','加工データ版、修理データ版'],['S29','S25'],'現場で得た問題・対応の経験を、支援サービスや製品開発に再利用する。顧客価値と社内改善を結ぶ知識資産になる。','サービス提供の過程で、次の商品を強くするデータを取得できるか。')
kw('K26','事業と競争','基盤・得意技術・販路を持ち寄る',['オープンプラットフォーム','共同事業化'],['S07','S08','S09','S32'],'外部AI、制御、データ、顧客接点を組み合わせる開発が増えている事例群。参加するだけで差別化できるとは限らない。','外部基盤を使いつつ、自社が持ち続ける技術・データ・接点は何か。')
kw('K27','運用と差別化の手掛かり','技術が動くことから、運用が続くことへ',['実行ループ','学習・更新ループ','横展開'],['S21','S13','S20','S34'],'介入、停止、復旧、更新、他現場への展開に残る負担が事業化の制約になる。未解決市場の存在自体は未検証。','モデルの精度だけでなく、顧客の導入・維持負担を下げられるか。')
kw('K28','運用と差別化の手掛かり','従来方式とAIを用途に応じて組み合わせる',['ルールベース','combined solution'],['S07','S15','S18','S22'],'標準化できる作業と変化の大きい作業では手段が違う。全体最適や自律化の構想に、すべての展示を無理に当てはめない。','AIを使うことで初めて解ける困りごとは何か。従来方式との比較はあるか。')

gaps = [
 dict(label='現象を捉える取得設計・データの品質評価',basis=['K06','K07','K09','K11'],hypothesis='加工現象の知見を、センサー・周期・条件・品質結果の対応設計へ落とし込み、モデル開発を支援する余地。',verify='既存サービスとの差、利用可能な顧客データ、取得後の改善効果、費用負担を確認する。'),
 dict(label='判断の意図・修正・失敗を残す仕組み',basis=['K03','K08','K12','K13'],hypothesis='ログだけでは足りない判断理由や修正を、作業の中で負担少なく収集して学習へ渡す余地。',verify='既存CAMや各社の固有モデル機能がどこまで対応するか。現場に入力の便益があるか。'),
 dict(label='モデルを顧客ごとに適用・評価する仕組み',basis=['K12','K14','K15','K27'],hypothesis='共通モデルの適用範囲を判定し、少ないデータで調整・検証し、更新後も効果を確認する余地。',verify='独自の評価データ・現象モデルが必要か。顧客や基盤提供者が外部へ任せる部分か。'),
 dict(label='既存設備と上位の判断・計画をつなぐ機能',basis=['K17','K18','K20','K21'],hypothesis='現場の状態を計画が扱える制約や能力に変換し、指示と結果を戻す接続部分に余地。',verify='既存MES・CNC・基盤との差分、接口、実行権限、障害時の対応を確認する。'),
 dict(label='導入後の継続改善を成果として提供',basis=['K05','K13','K24','K25'],hypothesis='データ取得・モデル改善・保全を束ね、品質や復旧時間等の改善を継続サービス化する余地。',verify='AI単独の効果、継続支払意思、更新・保守の原価、他顧客への再利用性を検証する。'),
]
notes = [
 'これは戦略・潮流のキーワード探索であり、市場シェアや業界全体の採用率を測定した調査ではない。',
 '複数ページからなる同一インタビューは1資料として数える。転載・引用を独立した裏付け件数に加算しない。',
 '本文の該当節、HTML公表要旨、検索結果からの本文抽出を区別する。検索抽出のみの資料は根拠の強さを下げて扱う。',
 '原典の短い語句と、調査側が付けたラベル・解釈を区別する。発表された構想や計画を実用済みとしない。',
 '企業がいう基盤モデルという名称だけでは、モデル構造、学習方法、ゼロからの学習、独占保有を確定できない。',
 '提言の種は未充足を確定した市場ではない。競合・顧客への確認を経て初めて差別化領域と判断する。',
 'ユーザーの重点は顧客向け製品・サービスの開発。自社導入は改善効果に加え、顧客向け開発のデータ取得・検証という観点でも扱う。',
 '既存の2024/2026全出展者集計とは別の追加調査。今回の資料数・語句数からマクロ普及率を算出しない。',
]
pending = [
 'AI精度向上→サービス価値向上→サブスクの収益性改善という連鎖は事業仮説。継続率・単価・提供原価等の裏付けは未取得。',
 'DMG森精機のエンジニアリング商社モデルと、エンジニアリングチェーン全体を売るという整理は同義ではない。',
 '各共通データ基盤への参加・データ利用条件、対象加工、提供形式、費用、成果の権利は未調査。',
 '全体最適の対象は単体機、セル、ライン、工場、企業間で異なる。各社の範囲を追加照合する必要がある。',
 '顧客業種・自社技術・アクセス可能なデータが未特定のため、自社の開発優先度や投資判断は未確定。',
]
payload=dict(title='JIMTOF2026・製造AIの戦略キーワード探索',checked_date='2026-10-21',stage='キーワード収集・文脈確認。最終構成・開発提言の確定前',sources=sources,keywords=keywords,gap_hypotheses=gaps,method_notes=notes,open_questions=pending)
(OUT/'strategy_keywords.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')

S={s['id']:s for s in sources}
esc=html.escape
def refs(ids):
    return ' '.join(f'<a href="#source-{i}" class="ref">{i} {esc(S[i]["publisher"].split("／")[0])}</a>' for i in ids)
groups=list(dict.fromkeys(k['group'] for k in keywords))
counts=Counter('検索抽出のみ' if s['reading_scope'].startswith('検索結果') else '本文・公表要旨' for s in sources)
cards=''
for g in groups:
    cards+=f'<section><h2>{esc(g)}</h2><div class="grid">'
    for k in [x for x in keywords if x['group']==g]:
        cards+=f'<article><div class="meta">{k["id"]} · 整理ラベル</div><h3>{esc(k["label"])}</h3><p class="terms">原典で拾った語句：{esc(" ／ ".join(k["source_expressions"]))}</p><p>{esc(k["context"])}</p><p class="question">開発上の問い〈分析〉：{esc(k["development_question"])}</p><div>{refs(k["source_ids"])}</div></article>'
    cards+='</div></section>'
source_html=''
for s in sources:
    extras=' '.join(f'<a href="{esc(u,quote=True)}" target="_blank" rel="noopener">続きのページ</a>' for u in s['extra_urls'])
    source_html+=f'<article id="source-{s["id"]}" class="source"><div class="meta">{s["id"]} · {esc(s["publisher"])} · {esc(s["published_date"] or "公表日未確認")} · {esc(s["kind"])}</div><h3><a href="{esc(s["url"],quote=True)}" target="_blank" rel="noopener">{esc(s["title"])}</a></h3><p>{esc(s["context"])}</p><p class="meta">該当箇所：{esc(s["locator"])}<br>確認範囲：{esc(s["reading_scope"])} ／ 確認日 {s["checked_date"]}</p>{extras}</article>'
gap_html=''.join(f'<article><h3>{esc(g["label"])}</h3><p>{esc(g["hypothesis"])}</p><p class="question">未充足の確認：{esc(g["verify"])}</p><p class="meta">関連：{", ".join(g["basis"])}</p></article>' for g in gaps)
doc='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>製造AIの戦略キーワード探索 | JIMTOF2026</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f6f8;color:#203448;font-family:Meiryo,"Yu Gothic",sans-serif;line-height:1.9}header{background:#12394a;color:#fff;padding:42px max(24px,calc((100vw - 1180px)/2))}header h1{font-size:32px;line-height:1.5;margin:8px 0 18px}header p{max-width:1040px}.stats{display:flex;gap:30px;flex-wrap:wrap}.stats b{font-size:30px;display:block;color:#9ee0cf}.stats span{font-size:13px}main{max-width:1236px;padding:25px 28px;margin:auto}nav{display:flex;gap:18px;flex-wrap:wrap;background:#fff;padding:15px 24px;border-bottom:1px solid #d5e0e5}a{color:#125f79;overflow-wrap:anywhere}h2{font-size:25px;margin:36px 0 18px}h3{font-size:19px;line-height:1.6;margin:8px 0 12px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:17px}article{background:#fff;border:1px solid #d3dfe5;border-top:3px solid #267e89;padding:22px}p{margin:10px 0}.meta{font-size:12px;color:#667885}.terms{font-size:13px;color:#3b6674;background:#eef6f7;padding:9px 12px}.question{font-size:14px;background:#fff5dc;padding:12px;border-left:3px solid #c49b3c}.ref{font-size:12px;display:inline-block;margin:4px 7px 0 0}.note{background:#e6f0f5;padding:20px 24px;border-left:4px solid #267e89}.source{margin:12px 0;scroll-margin-top:20px}.source h3{font-size:17px}li{margin:7px 0}.pending{border-left-color:#c49b3c;background:#fff5dc}footer{margin-top:38px;padding:20px 0;border-top:1px solid #cddbe2;color:#667885;font-size:12px}@media(max-width:760px){.grid{grid-template-columns:1fr}main{padding:18px}header{padding:28px 20px}header h1{font-size:26px}article{padding:18px}.stats{gap:20px}}@media print{nav{display:none}header{background:white;color:#203448;padding:12px}.stats b{color:#203448}main{max-width:none;padding:0}.grid{display:block}article{break-inside:avoid;margin:12px 0}a{color:inherit}}
</style></head><body>'''
doc+=f'<header><p>JIMTOF2026 追加調査 · 2026年10月21日</p><h1>製造AIの戦略・潮流を読む<br>記事から拾ったキーワードと、その文脈</h1><p>顧客に嬉しい製品・サービスの開発を中心に、ニーズ、データ、モデル、工程間の接続、事業戦略を調査。自社導入による改善と、開発のデータ取得・検証にも目を向けます。</p><div class="stats"><span><b>{len(keywords)}</b>整理した語群</span><span><b>{len(sources)}</b>資料（複数ページは1件）</span><span><b>{counts["本文・公表要旨"]}</b>本文・公表要旨を確認</span><span><b>{counts["検索抽出のみ"]}</b>検索本文抽出のみ</span></div></header>'
doc+='<nav><a href="#keywords">キーワード</a><a href="#seeds">差別化の手掛かり</a><a href="#limits">未確認の論点</a><a href="#sources">出典台帳</a></nav><main>'
doc+='<div class="note"><b>この段階の読み方</b><p>記事で使われている語句と、調査側の整理・分析を区別しています。語の出現数から普及率を判断せず、各社の構想を実現済みとは扱いません。完成レポートの構成や自社の開発優先度を、ここで確定するものではありません。</p></div>'
doc+='<section><h2>追加で確認できたこと</h2><p>前回はマザックの公式発表だけではモデル開発の詳細を確定できないとしましたが、10月19日の当事者取材記事に、自社データによる基盤モデルと顧客固有モデルの関係が説明されています（S05）。モデルの構造や独占保有まで確定するものではありません。</p><p>また、加工現象を理解するためのデータ取得と、モデル開発基盤・エコシステムへの参加は、製品開発の手段として検討すべき論点です（S01・S03）。「自前の基盤を必ず作る」という結論ではなく、取得対象、利用条件、自社の知見を持つ領域を確認する必要があります。</p></section>'
doc+='<div id="keywords"></div>'+cards
doc+='<section id="seeds"><h2>差別化の手掛かり〈未充足は未確認〉</h2><p>資料から浮かんだ調査候補です。競合が存在しない領域や、投資すべきテーマとして確定したものではありません。</p><div class="grid">'+gap_html+'</div></section>'
doc+='<section id="limits"><h2>まだ裏付けが必要な論点</h2><div class="note pending"><ul>'+''.join(f'<li>{esc(n)}</li>' for n in pending)+'</ul></div><h2>調べ方と集計上の注意</h2><ul>'+''.join(f'<li>{esc(n)}</li>' for n in notes)+'</ul></section>'
doc+='<section id="sources"><h2>出典台帳</h2><p>企業の構想・当事者発言・業界見解・公的資料を区別。記事全文は転載せず、短い語句と本調査による要旨、該当節を記録しています。</p>'+source_html+'</section><footer>本資料は公開情報に基づく事前調査です。第三者の文章・商標等の権利は各権利者に帰属します。2026年の展示予定と現地確認済みの内容は区別してください。</footer></main></body></html>'
target=ROOT/'outputs/JIMTOF2026_戦略キーワード探索_20261021.html'
target.write_text(doc,encoding='utf-8')
assert len({s['id'] for s in sources})==len(sources)
assert len({k['id'] for k in keywords})==len(keywords)
assert all(set(k['source_ids']) <= S.keys() for k in keywords)
assert all('http' in s['url'] and s['context'] and s['locator'] for s in sources)
print(json.dumps({'sources':len(sources),'keywords':len(keywords),'reading_scope_counts':counts,'html_bytes':target.stat().st_size},ensure_ascii=True))
