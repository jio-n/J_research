"""Re-edit the existing research by manufacturing task, with source lineage."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/research/technical_guide_20261022'
OUT = ROOT / 'outputs/technical_guide_20261022'

def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')

directory = read('data/research/report_v0/technology_directory.json')
entries = {e['card_id']: e for e in directory['entries']}
cases = {e['card_id']: e for e in read('data/research/report_v0/case_comparison.json')}
ledger = {e['evidence_id']: e for e in read('data/research/report_v0/evidence_ledger.json')}
quotes = {e['quote_id']: e for e in read('data/research/quotation_evidence_20261022/quotes.json')['quotes']}
majors = read('data/research/macro_20261019/major_dossiers.json')
strategy = read('data/research/strategy_review_20261021/strategy_review.json')

# Rows are editorial comparisons, not automatic keyword classifications.
# Format: card, display product, task, method, technical description, status, field check.
def row(card, product, task, method, description, status, check, company=None, quote_ids=()):
    e = entries[card]
    c = cases.get(card, {})
    sources = []
    ids = list(c.get('evidence_ids', e['evidence_ids']))
    if card == 'FC039':
        ids += cases['FC040']['evidence_ids']
    for eid in ids:
        s = ledger.get(eid)
        if s and s.get('url') and s['url'] not in [a['url'] for a in sources]:
            sources.append({'id': eid, 'url': s['url'], 'title': s['title'], 'locator': s.get('locator', '')})
    for s in c.get('full_record', {}).get('source_locations', []):
        if s['url'] not in [a['url'] for a in sources]:
            sources.append({'id': s['evidence_id'], 'url': s['url'], 'title': s.get('locator', ''), 'locator': s.get('locator', '')})
    for u in e.get('exhibitor_urls_2026', []):
        if u not in [a['url'] for a in sources]:
            sources.append({'id': '展示告知', 'url': u, 'title': 'JIMTOF2026 出展説明', 'locator': '出展紹介・主な出展物'})
    for qid in quote_ids:
        q = quotes[qid]
        sources.append({'id': qid, 'url': q['source_url'], 'title': q['title'], 'locator': q['locator']})
    return dict(card_id=card, company=company or e['company'], product=product,
                booth='／'.join(e['booths']), task=task, method=method,
                description=description, status=status, check=check, sources=sources,
                original_case_id=c.get('case_id'), quote_ids=list(quote_ids))

def cat(id, name, need, distinction, topics, rows):
    return dict(id=id, name=name, need=need, distinction=distinction,
                legacy_topic_ids=topics, rows=rows)

categories = [
cat('T01', '工程設計・NCプログラム生成',
    '多品種部品の加工準備時間短縮、熟練者の工程・工具選定ノウハウの再利用。',
    '工程案の生成、工具経路の生成、ポスト処理後のNC検証を区別する。', ['B02','B18'], [
    row('FC018','ESPRIT EDGE ProPlanAI','加工工程の立案','特徴認識・工程予測',
        '部品特徴・PMI・過去ジョブを用いて加工工程案を生成。2026.1では旋削・複合・スイス型の商用範囲を説明。',
        '製品機能／展示予定','対象形状と加工法、工程案の修正箇所、採用までの確認工数。',company='Hexagon'),
    row('FC020','Mastercam＋CAMAssist','工具経路・条件の作成','AIによるCAM作成支援',
        '形状、工具、材種、機械・保持条件から工程・経路・条件案を生成。CAM上で修正・検証し、人がポスト処理する。',
        '展示予定','3軸・3+2軸の対応範囲、干渉回避、生成後に残る手作業。',company='JBMエンジニアリング'),
    row('AC131','CAM Assist for SolidCAM','工具経路・条件の作成','AIによるCAM作成支援',
        'SolidCAM環境で3軸・3+2軸の加工戦略と経路案を生成。既存CAM運用への組込み方を比較する。',
        '展示予定','工具DBの流用、修正・検証、Mastercam版との対応差。',company='タクテックス'),
]),
cat('T02', 'NC加工条件最適化・適応制御',
    '加工時間短縮と過負荷・工具破損の抑制。鋳鍛造品などの取り代変動への対応。',
    '加工前のモデルベース最適化と、加工中の実測フィードバック制御は適用場面が異なる。', ['B03'], [
    row('FC022','Vericut Force／Optimizer','加工前の送り最適化','切削物理モデル',
        'NCと切削モデルに基づき送りを事前に最適化。Forceの物理ベース機能とOptimizerの機能範囲は版別に確認する。',
        '展示予定','材料・工具モデルの設定、負荷制約、実加工との差と修正方法。'),
    row('RPT001','Production Module／AdvantEdge','送り最適化・切削解析','NC負荷解析／刃先FEM',
        'Production ModuleはNCレベルの負荷解析・最適化。AdvantEdgeは刃先近傍のFEM解析で、対象と計算粒度が異なる。',
        '展示告知＋製品資料','材料モデル、切削力・温度の検証、NC最適化への受渡し。',company='Third Wave Systems'),
    row('RPT002','ACM','加工中の送り調整','主軸負荷フィードバック',
        '主軸負荷をリアルタイム監視し送りを自動調整。既存NCを変更せず導入する説明。負荷が変動する荒加工等が対象。',
        '展示予定','制御周期・目標負荷、急変時の制限、時間短縮と工具寿命の両立。',company='西部商工'),
]),
cat('T03', '熱変位補正・びびり抑制',
    '暖機・環境温度・切削振動による寸法精度と面品位の変動を抑制。',
    '熱変位の予測補正、構造設計、びびり抑制の主軸速度制御を別の機能として比較する。', ['B05'], [
    row('RPT006','Ai Thermal Shield','熱変位の予測・補正','測定データを用いる学習',
        '温度・主軸速度等を考慮し、加工後のワーク測定データを学習して熱変位オフセットを最適化するとの製品説明。',
        '既存製品資料／個別展示未確認','学習に必要な測定・運転条件、再学習、対象展示機への搭載。',company='ヤマザキマザック'),
    row('FC009','サーモフレンドリーコンセプト','熱変位の抑制・補正','構造設計・熱変位制御',
        '熱変形を単純化する機械構造と熱変位制御を組み合わせる。2026告知のAI機能との対応は個別確認が必要。',
        '熱変位制御を展示告知','補正対象、環境・暖機条件、AIの入力と補正担当範囲。'),
    row('RPT007','加工ナビ M-i／M-gⅡ','びびり抑制','振動解析・主軸速度調整',
        'M-iは内蔵センサの振動から主軸速度を算出・変更。M-gⅡはマイクを使い速度候補を提示し、人が選択する。',
        '既存製品資料／個別展示未確認','自動変更と推奨表示の差、対象加工・工具、制御の安定範囲。',company='オークマ'),
]),
cat('T04', '工具状態監視・寿命予測',
    '工具の早期交換を減らしつつ、突発欠損・不良品の連続発生を防止。',
    '現在の摩耗判定、将来の寿命予測、交換指令の実行は別段階。', ['B08'], [
    row('FC039','ツールコラージュ／アナライザー','欠け・摩耗判定、交換時期提案','刃先画像AI・摩耗履歴解析',
        '刃先画像で欠け・摩耗を判定・記録。別機能のアナライザーは摩耗履歴から寿命・交換時期を提案する。',
        '展示予定','工具・材種別の必要履歴、汚れへの耐性、交換判断の責任分担。'),
    row('FC038','VT 122＋VTC 6.0','機上工具検査','画像計測・AI摩耗診断',
        'ビジョンシステムVT 122とVTC 6.0によるAI摩耗診断・工具長計測を出展説明に記載。',
        '展示予定','摩耗量・欠けの判定基準、撮像条件、測定後のCNC連携。'),
    row('FC035','ARTIS／BLU／VTS','工具・加工プロセス監視','加工信号監視・工具計測',
        '工具・機械・加工プロセスの監視と工具計測を組み合わせる。製品ごとの信号・判定・停止出力を比較する。',
        '展示予定','破損検出と摩耗推定の差、監視閾値、停止・補正の出力先。'),
]),
cat('T05', '計測・外観検査・加工補正',
    '測定・検査の省人化、見逃し・過検出の低減、測定結果からの加工精度安定化。',
    '画像の良否判定、寸法計測、工具オフセット補正は入力・出力が異なる。', ['B06','B07','B19'], [
    row('FC033','Renishaw Central＋IPC','計測結果の加工フィードバック','計測データ・プロセス制御',
        '計測・装置状態等を集約し、IPCで工具オフセットや機械変数を更新。測定から加工補正までを接続する。',
        '展示予定','補正ルール、対象CNC、外れ値の扱い、補正を止める条件。',company='レニショー'),
    row('FC036','HACARUS Check ZERO','外観の異常判定','良品学習・追加学習',
        '少量の良品画像との差で異常を検出。人が良品・不良品ラベルを追加し、見逃し・過検出を調整する。',
        '販売済み／展示予定','不良種類別の評価、追加学習後の再評価、撮像条件の許容差。'),
    row('AC085','GH5','刃先形状の補正加工','機内3D画像・AI補正',
        '機内3D画像で工具刃先を測り、目標とする幅・角度へホーニングを補正するとの出展説明。',
        '展示予定','画像精度、補正量・収束条件、最終形状の合否判定。',company='サイバーRC'),
]),
cat('T06', 'ロボット認識・動作生成',
    'ワーク形状・位置・切粉状態の変化による教示負担と、自動運転の中断を削減。',
    '認識、軌道生成、実行、完了確認の担当範囲で比較。フィジカルAIの呼称と確認済み機能を併記する。', ['B12','B17'], [
    row('FC049','TR-20W','主軸に絡む切粉の除去','状況認識・判断・除去',
        '絡まった切粉の状況を判断して除去するフィジカルAI搭載デモを予告。センサ・学習方式は非公開。',
        '参考出品','絡まり方を変えた実演、除去完了の判定、失敗時の再試行。'),
    row('AC146','3D形状認識加工システム','不定形ワークの面取り・皿もみ','3D認識・加工軌道生成',
        'レーザースキャンした形状から加工軌道を生成。図面・パタン教示不要との説明。AI方式の利用は未確認。',
        '共同ブースで展示予定','未登録形状の対応範囲、干渉確認、取り残しと加工品質。',company='東京エレクトロンデバイス'),
    row('FC005','生成AIによるロボット駆動','具体作業は未公表','生成AI・オープンプラットフォーム',
        '生成AIによるロボット駆動事例を予告。入力、動作生成、検証、実行の構成と対象作業は現地確認が必要。',
        '展示予定／詳細未公表','既知・未知条件への対応、AI担当処理、成功率と介入条件。',company='ファナック'),
]),
cat('T07', '段取り・搬送・加工セル自動化',
    '多品種・変量生産での品種切替え、供給・回収、長時間無人運転に残る人手を削減。',
    '段取り機構、位置補正、供給システム、工程間搬送を区別。AI利用の有無より対応する変動条件を見る。', ['B10','B11','B22'], [
    row('FC002','MATRIS WPH 210','ワーク・パレット供給','ハンドリングシステム',
        'ワークとパレットの両方を供給するシステム。品種・ロットの変化に応じた供給と切替えが比較点。',
        '日本初公開予定','ワーク・治具の事前準備、切替え手順、無人継続を妨げる作業。'),
    row('FC048','RoboSync','移設後の位置復旧','マーカー認識・相対位置補正',
        '移設後にマーカーを読み、工作機械との相対位置を補正。既存パレット・台車を利用する省スペース構成。',
        '展示予定','再教示の残作業、位置誤差の許容範囲、品種変更時の設定。'),
    row('FC008','ARMROID／OMR20','機内作業・ワーク供給','機内ロボット／移動式協働ロボット',
        '機内組込みのARMROIDと、機械脇へ配置するOMR20を出展。設置方式と段取り負担を比較する。',
        '展示予定','担当作業、品種切替え、安全領域、停止後の復帰手順。'),
]),
cat('T08', '設備診断・予知保全',
    '故障の事前把握、診断・復旧時間短縮、保全知識の属人化解消。',
    '専用診断動作、通常稼働データの異常検知、対話型の原因・対処支援を区別する。', ['B09','B13'], [
    row('FC004','Condition Agent','機械状態の診断','診断用NC・クラウド分析',
        '診断専用NCを実行してデータを取得し、クラウドで分析。2026年4月受注分から対象機へ標準搭載する説明。',
        '提供開始／個別展示未確認','診断対象部位、通常運転ログとの差、異常判定後の保全手順。',quote_ids=['Q26']),
    row('AC225','プライマリドクタサービス','稼働中の劣化・異常診断','電流・振動等のAI解析',
        '稼働中の電流・振動等を新品状態と比較し劣化・異常を診断するとの説明。',
        '展示予定','負荷・加工条件の違いの補正、故障モード別の検知性能。',company='ムラテックCCS'),
    row('FC013','TwinCAT CoAgent for Operations','原因診断・運用支援','生成AI・設備データ／文書参照',
        'ライブデータ、ログ、保守文書から原因仮説・対処案を生成。コマンド実行も説明するが権限範囲は未公開。',
        '製品発表／投入時期要問合せ','原因の裏付け、実行可能な命令、人の承認、失敗時の復旧。',company='ベッコフ'),
]),
cat('T09', '生産スケジューリング・MES',
    '納期・設備負荷・進捗変化への計画調整と、指示・実績・履歴の分断解消。',
    '日程を決めるスケジューラと、指示・実績を管理するMESを分けて比較する。', ['B14','B23'], [
    row('FC027','MonoRevo','工程計画・負荷調整','自動スケジューリング',
        '工程設計・計画・進捗をまとめて管理し、自動スケジューリングを支援。AIの担当処理は未確認。',
        '展示予定','設備・作業者・工具の制約、割込時の再計画、計画の確定者。'),
    row('FC026','Smart Craft MES','作業指示・実績・履歴管理','MES・API連携',
        '作業記録、指示、履歴を一元管理し外部システムとAPI連携。自動最適計画の実装とは分けて扱う。',
        '展示予定','設備実績との接続、計画系との更新周期、現場入力の負担。'),
    row('AC295','WinTool','工具・工程資源の管理','工具DB・在庫ルール連携',
        '工具情報と現物・工程資源を連携し、在庫ルールに基づく購買要求を扱う。',
        '展示予定','計画に必要な工具可用性、CAM・プリセット・在庫の対応。',company='WinTool'),
]),
cat('T10', '制御ソフトウェア開発支援',
    'PLCプログラミング、I/O構成、HMI・電気設計に必要な開発工数の削減。',
    'プログラムや設計案の生成はエンジニアリング支援。設備の自律運転とは別に評価する。', ['B04'], [
    row('FC011','TwinCAT CoAgent for Engineering','PLCコード作成','生成AI・プロジェクト文脈参照',
        '要求と既存プロジェクトの文脈に基づきPLCコード案を提案。人が確認し制御プロジェクトへ採用する。',
        '展示告知＋製品資料','既存コード・ライブラリの参照、生成コードの検証と採用手順。',company='ベッコフ'),
    row('FC012','TwinCAT CoAgent for Engineering','I/O・HMI作成','生成AIによる構成・画面支援',
        'I/O構成とHMI生成・操作を支援。PLCコード生成と同じ製品内でも対象成果物を分けて確認する。',
        '展示告知＋製品資料','要件からの構成生成、変更整合性、実機接続前の検証。',company='ベッコフ'),
    row('FC017','Eplan Copilot','電気設計の支援','生成AI・設計文脈参照',
        '設計の文脈に応じた回答・推奨・手順を生成。設計データをどこまで自動作成するかを確認する。',
        '展示予定','回答支援と設計変更の範囲、標準回路・部品DBの利用。'),
]),
cat('T11', '製造データ基盤・デジタルツイン',
    '設備・工程データの連携、AIの制御実装、仮想検証・学習に必要なデータ準備。',
    '設備接続、モデル作成・実装、工作機械の仮想検証、物理シミュレーション用データは異なる基盤機能。', ['B15','B16','B24','B25'], [
    row('FC014','TwinCAT Machine Learning Creator','AIモデル作成・制御実装','AutoML・ONNX',
        '人が用意したデータから学習・モデル選択・評価を支援。ONNX等で出力し、制御側へ実装する。',
        '展示予定／既存基盤','必要データ・ラベル、推論周期、更新時の評価・差戻し。',company='ベッコフ'),
    row('AC098','Digital Thread／工作機械ツイン','設計・加工・品質の連携','デジタルスレッド・機械ツイン',
        'SINUMERIK ONEを搭載したHeller Toknの工作機械ツインと、Equatorによる工程内品質保証を実演予定。',
        '展示予定','設計変更・加工条件・測定結果のデータ対応と更新の自動化。',company='シーメンス'),
    row('AC273','TRINIX','物理シミュレーション用データ作成','CAD生成・SimReady変換',
        'CAD等から形状・関節・物理属性を生成し、USD／URDF／MJCF等へ出力するとの説明。',
        '展示予定／実機精度未検証','質量・摩擦の実測と推定の区別、生成物の検証、実機との差。',company='NdotLight'),
]),
]

trends = [
    ['工程設計のAI化','技能依存低減・準備時間短縮','特徴認識、過去工程の再利用、CAM工程案の生成','ProPlanAI、CAMAssist。マザックは工程設計AIを共同開発。'],
    ['加工制御の高度化','品質安定・工具寿命延長・加工時間短縮','物理モデルによる事前最適化と、実測による補正・適応制御','Vericut Force、ACM、Ai Thermal Shield、Renishaw IPC。'],
    ['ロボット作業の適応化','多品種対応・教示削減・停止時間短縮','状態認識から動作・軌道を変更する作業自動化','TR-20Wは切粉除去の参考出品。ファナックは生成AI駆動事例を予告。'],
    ['工程間のデータ統合','計画・実績・品質の連携','デジタルスレッド、MES、再計画、AI学習基盤','シーメンスの設計・加工・品質連携。DMG・マザックの開発構想。'],
]
company_strategy = [
    ['DMG森精機','加工・保全・生産セル','AMR 1000、MATRIS WPH 210、AIエージェント実装を展示告知。Condition Agentは診断用NCとクラウド分析。','GENIACで市場投入設備のデータ収集・学習・還元基盤を計画。'],
    ['ヤマザキマザック','工程設計・生産計画・段取り','INTEGREX、自動化・デジタル・AIソリューションを告知。個別の工程設計AIの展示内容は要確認。','ABEJAと共同開発。MAZATROLの加工意図・判断結果を使う工程設計等を目指す。'],
    ['ファナック','CNC知的作業・ロボット動作','フィジカルAI CNC、生成AIによるロボット駆動、オープンプラットフォームの事例を告知。','日立の工場をカスタマーゼロに共同実証。2027年度の事業化を目指す。'],
    ['オークマ','加工精度・機内作業・供給','熱変位制御、ARMROID、OMR20、多面APC。構造・制御・搬送の組合せで品質と稼働率を改善。','2026告知のAI機能と各既存制御機能の対応範囲を現地確認。'],
    ['シーメンス','設計・加工・品質保証','NX、SINUMERIK ONE、工作機械ツイン、Equatorによる工程内品質保証。','Digital Threadを軸に工程間データを連携。全工場の自律運営の達成とは区別。'],
]
priorities = [
    ['工程設計・CAM','Hexagon ProPlanAI　E2013\nJBM CAMAssist　E2002','対象形状と工程・経路生成、人の修正工数を比較。'],
    ['加工最適化・制御','CGTech Force　S3014\n西部商工 ACM　S3020','加工前の送り最適化と加工中の負荷適応制御を比較。'],
    ['ロボット適応動作','ファナック　S2001\nTAKISAWA TR-20W　E3013','状態変化に対する判断・動作変更、失敗後の復帰を確認。'],
    ['計測・加工補正','レニショー Central＋IPC　E7089\nハイデンハイン VT 122　E7043','寸法補正と工具状態判定が実機運用へ戻る範囲を確認。'],
    ['加工セル・段取り','DMG MATRIS WPH 210　E8005\nオークマ ARMROID／OMR20　E3028','品種切替え、事前準備、無人運転に残る人作業を比較。'],
    ['工程設計AI・生産計画','ヤマザキマザック　E1001\nものレボ MonoRevo　W3042','共同開発の展示有無と、計画制約・割込時の再計画を確認。'],
    ['工程統合・AI実装','シーメンス　E3006\nベッコフ　E2028','データの工程間連携とAIモデルの制御実装を確認。'],
]

# All 33 requested major companies remain visible with concrete exhibits.
# A missing company detail is left missing, rather than filled with guessed AI claims.
major_notes = [
('MATRIS WPH 210／AMR 1000','段取り・搬送','供給・搬送の接続と品種切替え。'),
('INTEGREX／AIソリューション','工程集約・工程設計AI','共同開発AIの実演有無と準備・計画の自動化範囲。'),
('ARMROID／OMR20','機内作業・供給','機内組込みと移動式の段取り・復帰。'),
('MASシリーズ／生産ラインエンジニアリング','加工セル・ライン統合','加工・供給・計測を統括する範囲。'),
('フィジカルAI CNC／生成AIロボット','知的作業・ロボット動作','AIが変更する判断・動作と変動条件。'),
('CNC省人化／新開発スケジューラ','加工支援・自動化運用','計画制約、加工・保全へのAI適用。'),
('SINUMERIK ONE／工作機械ツイン','デジタルスレッド','設計・加工・品質データの受渡し。'),
('G5P250G／工場ソリューション','熟練研削・資源管理','熟練加工の再現方法と人・設備の管理。'),
('MVR-Hx／Nidec NC Twin','加工前検証','機械・制御モデルの再現範囲。'),
('VB-X650／パレットストッカ','長時間無人運転','段取り、工具・パレットの容量制約。'),
('ALN600G＋搬送ロボット','放電加工の自動化','供給・加工・例外処理の連携。'),
('SDEW8010iⅢ＋ALFAS03KR','プレス加工自動化','供給から加工までの人作業と切替え。'),
('SPEEDIO／PC-1','工程集約・段取り削減','工具本数・外段取り・パレット交換。'),
('MX-520T PC7／MiOS 4','多品種の無人運転','パレット・工具・運転順の管理。'),
('自動計測／FA連携／LFV','自動盤の連続運転','計測補正・切粉対策とFA接続。'),
('SB-12RⅡほか／各種支援','小物部品加工・工程支援','自動化機能の担当工程。人型部品加工とAIロボットを区別。'),
('TMA8F／VA3S＋ロボット','段取り・測定・供給','コレット交換と機外測定の連続運転。'),
('MONOlithbox','工具管理DX','工具在庫・現物・工程データの対応。'),
('DXAS／RS0112ほか','工具・加工プロセス改善','加工条件選定・デジタル連携の有無。AI機能は未確認。'),
('VIMOA／EASY TOOL GUIDE','加工監視・工具選定','取得信号、分析対象、工具選定への反映。'),
('MATRIX 360','工具管理','工具在庫管理と加工・購買情報の連携。'),
('自動計測／計測プラットフォーム','計測自動化・品質データ','測定の自動化と加工工程支援の接続。'),
('出展内容の保存情報なし','内容未確認','E7044は登録済み。展示品とAI・自動化機能を現地確認。'),
('Renishaw Central／Equator','計測・加工補正','IPCの補正先、閾値、異常時の扱い。'),
('VT 122＋VTC 6.0','工具検査・摩耗診断','画像判定からCNCへの情報連携。'),
('TwinCAT CNC／ML Creator／CoAgent','AI実装・制御開発','データ取得、モデル評価、実機制御の接続。'),
('ProPlanAI／MAESTRO／PRESTO','工程設計・品質保証','CAMと品質保証は別ブース。用途別に比較。'),
('SumiSmall／WEZMほか','工具・工程集約','条件設定・工具データ提供の範囲。AI機能は未確認。'),
('RoboSync／Protona','供給段取り・NC作成','移設後の位置補正とプログラム作成の負担。'),
('VN40／TN400ⅡR／Quist','異形ワーク・段取り','把持・表裏加工・備品管理の自動化範囲。'),
('TR-20W','切粉除去','絡まり認識、除去動作、完了・失敗判定。参考出品。'),
('Fusion／Fusion Manage','CAD/CAM・PLM','AI支援対象と設計・製造データの連携。'),
('NEXIV／MV5X／ロボットビジョン','計測・認識','計測・認識結果が加工・搬送へ戻る範囲。'),
]
assert len(major_notes) == len(majors) == 33
major_index = [dict(company=m['target'], booth='／'.join(m['booths']),
                    exhibit=n[0], task=n[1], check=n[2], urls=m['urls_2026'])
               for m,n in zip(majors,major_notes)]

guide = dict(date='2026-10-22', title='JIMTOF2026 AI・自律化・自動化 技術動向と視察ガイド',
             main_slides=3, categories=categories, trends=trends,
             company_strategy=company_strategy, priorities=priorities, majors=major_index,
             physical_ai=dict(
                 definition='AIが現実環境を知覚し、その状態に応じて物理的な行動を選択・生成・調整する技術。',
                 definition_status='本調査の作業定義。業界統一規格ではない。',
                 criteria=[['適用タスク','搬入出、切粉除去、面取りなど、担当作業を特定する。'],
                           ['認識・判断方式','画像・力覚等の入力と、学習モデル／幾何処理／ルールの担当を確認する。'],
                           ['動作の適応範囲','位置・形状・状態を変えた際の動作変更と、再教示の必要量を確認する。'],
                           ['完了・失敗処理','完了確認、再試行、人への引継ぎ、許可された動作範囲を記録する。']],
                 note='固定設置・単一タスクでも適応動作を持ち得る。VLAや基盤モデルの使用は別項目で確認し、名称だけで最新方式と判定しない。',
                 quote_ids=['Q07','Q41']),
             evidence_groups=[['工程設計・現場適応の開発方向',['Q05','Q07','Q06','Q14']],
                              ['製造データ・物理モデル・工程統合',['Q02','Q01','Q24','Q11']]],
             scope=directory['scope'], signals=strategy['text_signals'],
             research_notes=[
                 '2024・2026の全出展者照合2,427掲載行を土台とし、両年に説明文がある同名538件で文言を比較。',
                 '技術候補344件を索引に維持。57件の詳細比較から、方式差が読める33行を本編で比較。33行は市場シェア・採用率の標本ではない。',
                 '顧客ニーズは出展説明・記事を踏まえた課題整理であり、顧客アンケートによる需要量の推計ではない。',
                 '2026出展予定、既存製品の参考情報、共同開発計画を区別。現地性能・展示機の版は未確認。',
                 '旧比較カードRPT006・RPT007には元カードから継承した不適切な入出力欄があるため、本版は公式製品資料RPT-S03・RPT-S01の方式記述を採用。',
             ])
write(DATA / 'content.json', json.dumps(guide,ensure_ascii=False,indent=2)+'\n')

H = html.escape
def table(headers, rows, cls=''):
    return '<div class="table-scroll"><table class="'+cls+'"><thead><tr>'+''.join('<th>'+H(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+H(str(x)).replace('\n','<br>')+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def source_links(r):
    return ' '.join('<a href="'+H(s['url'],quote=True)+'" target="_blank" rel="noopener">'+H(s['id'])+'</a>' for s in r['sources'])

parts=['''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JIMTOF2026 技術動向と視察ガイド</title>
<style>
:root{--ink:#193647;--teal:#087b81;--muted:#536774;--line:#cfdbdf;--pale:#edf4f5}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f7f9fa;color:var(--ink);font:15px/1.75 "Noto Sans JP","Yu Gothic",sans-serif}header,main{max-width:1320px;margin:auto;padding:32px 34px}header{background:var(--ink);color:white;max-width:none;padding:40px max(34px,calc((100vw - 1252px)/2))}h1{font-size:29px;line-height:1.5;margin:0 0 12px}h2{font-size:24px;margin:0 0 14px;border-bottom:3px solid var(--teal);padding-bottom:9px}h3{font-size:19px;margin:25px 0 10px}p{margin:8px 0 14px}.meta{font-size:13px;color:#d6e5e9}.lede{font-size:17px;line-height:1.9;max-width:1100px}nav{display:flex;gap:8px 20px;flex-wrap:wrap;padding:18px 0;border-bottom:1px solid var(--line)}a{color:var(--teal);text-underline-offset:3px}nav a{font-weight:bold}section{background:white;padding:27px 28px;margin:26px 0;scroll-margin-top:20px}.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:12px 13px}th{background:var(--ink);color:white;font-weight:600}tbody tr:nth-child(even){background:#f3f7f7}.comparison{min-width:990px;table-layout:fixed}.comparison th:nth-child(1){width:21%}.comparison th:nth-child(2){width:16%}.comparison th:nth-child(3){width:36%}.comparison th:nth-child(4){width:27%}.product{font-weight:700;font-size:15px;line-height:1.6}.status,.sources{display:block;font-size:12px;color:var(--muted);margin-top:7px}.sources a{margin-right:8px}.need{font-size:16px}.distinction{border-left:4px solid var(--teal);padding:8px 14px;background:var(--pale);margin:17px 0}.quote{margin:20px 0 24px;padding:0 0 0 20px;border-left:3px solid var(--teal)}blockquote{margin:0 0 6px;font-size:18px;font-weight:650;line-height:1.8}.quote p{font-size:14px;margin:5px 0}.quote cite{font-size:13px;font-style:normal;color:var(--muted)}.small{font-size:13px;color:var(--muted)}input,select{font:inherit;padding:9px 11px;border:1px solid #aebfc8;border-radius:3px}input{width:55%}.controls{display:flex;gap:14px;flex-wrap:wrap;margin:15px 0}#atlas{font-size:13px;min-width:1030px}#atlas td:nth-child(1){width:26%}#atlas td:nth-child(2){width:17%}#atlas td:nth-child(3){width:36%}#atlas td:nth-child(4){width:21%}.count{font-weight:bold}.legend{font-size:13px;color:var(--muted);margin-bottom:18px}footer{max-width:1250px;margin:20px auto 50px;padding:0 30px;color:var(--muted);font-size:13px}@media(max-width:750px){header,main{padding:23px 16px}h1{font-size:24px}section{padding:21px 16px}h2{font-size:21px}input{width:100%}}@media print{body{background:white;font-size:10pt}header{background:white;color:var(--ink);padding:0}.meta{color:var(--muted)}nav,.controls,#atlas-section{display:none}main{padding:0;max-width:none}section{padding:12px 0;margin:14px 0;break-inside:auto}h2{break-after:avoid}.comparison{min-width:0}table{font-size:9pt}tr,.quote{break-inside:avoid}a{color:inherit}header h1{font-size:23pt}}
</style><header><h1>JIMTOF2026 AI・自律化・自動化<br>技術動向と視察ガイド</h1><div class="meta">公開資料による事前整理　2026年10月22日　現地未確認</div><p class="lede">加工準備の技能依存低減、加工品質の安定化、多品種対応、工程間の連携を軸に、技術の適用タスクと実現方式を比較する。視察先は、製品名と比較すべき機能から選定する。</p></header><main>''']
parts.append('<nav><a href="#trends">技術動向</a><a href="#strategy">主要メーカー</a><a href="#visits">視察優先ブース</a><a href="#physical">フィジカルAI</a><a href="#majors">主要33社</a><a href="#evidence">原文根拠</a><a href="#atlas-section">全344件索引</a></nav>')
parts.append('<section id="trends"><h2>1. 技術動向</h2>'+table(['技術領域','顧客ニーズ','技術の方向','企業・製品例'],trends)+'<p class="distinction">工程・工場全体の最適化は主要な開発方向。一方、具体的な製品比較では、工程案生成、異常診断、補正、供給などの個別機能と、相互の接続範囲を確認する必要がある。</p><p class="small">上表は資料横断の分析。個別の製品仕様は以下の比較表と原典に紐付けた。</p></section>')
parts.append('<section id="strategy"><h2>2. 主要メーカーの開発対象と実現技術</h2>'+table(['企業','ターゲット','公開済みの製品・展示告知','共同開発・今後の方向'],company_strategy)+'<p class="small">DMGのGENIAC、マザックとABEJA、ファナックと日立の計画を、2026会場で完成・実演済みとは扱わない。根拠は末尾の原文集および出典台帳。</p></section>')
parts.append('<section id="visits"><h2>3. 視察優先ブース</h2><p>優先度は今回の調査目的への適合と方式比較のしやすさで設定。会場内の移動順は未設定。</p>'+table(['調査テーマ','企業・製品・ブース','比較・確認内容'],priorities)+'</section>')
parts.append('<section><h2>4. カテゴリ別技術比較</h2><p>顧客ニーズを共通条件とし、各社の<strong>対象タスク、実現方式、入出力、確認事項</strong>を揃えて比較する。</p><nav>'+''.join('<a href="#'+c['id']+'">'+c['id']+' '+H(c['name'])+'</a>' for c in categories)+'</nav></section>')
for c in categories:
    parts.append('<section id="'+c['id']+'"><h2>'+c['id']+' '+H(c['name'])+'</h2><p class="need"><strong>顧客ニーズ：</strong>'+H(c['need'])+'</p><p class="distinction">'+H(c['distinction'])+'</p><div class="table-scroll"><table class="comparison"><thead><tr><th>企業・製品・ブース</th><th>対象タスク／実現方式</th><th>技術内容</th><th>現地で確認する内容</th></tr></thead><tbody>')
    for r in c['rows']:
        parts.append('<tr><td><span class="product">'+H(r['company'])+'<br>'+H(r['product'])+'</span><br>'+H(r['booth'])+'<span class="status">'+H(r['status'])+'</span></td><td><strong>'+H(r['task'])+'</strong><br>'+H(r['method'])+'</td><td>'+H(r['description'])+'<span class="sources">出典：'+source_links(r)+'</span></td><td>'+H(r['check'])+'</td></tr>')
    parts.append('</tbody></table></div></section>')
p=guide['physical_ai']
parts.append('<section id="physical"><h2>5. フィジカルAIの調査基準</h2><p class="need"><strong>作業定義：</strong>'+H(p['definition'])+'</p><p class="small">'+H(p['definition_status'])+'</p>'+table(['評価項目','記録する内容'],p['criteria'])+'<p class="distinction">'+H(p['note'])+'</p><p>TR-20WはメーカーがフィジカルAIと呼ぶ切粉除去の参考出品。東京エレクトロンデバイスは認識・軌道生成が具体的だがAI方式は未確認。ファナックは生成AI駆動を告知しているが、対象タスクと適応範囲は未公表。この三者を同じ完成度として報告しない。</p></section>')
parts.append('<section id="majors"><h2>6. 主要33社の展示・確認項目</h2><p class="legend">大手企業を漏らさないための追加索引。AI機能が未確認の企業も、具体的な工具・加工・自動化の展示内容で整理した。</p><div class="table-scroll"><table><thead><tr><th>企業・ブース</th><th>展示品・ソリューション</th><th>対象タスク</th><th>確認事項</th></tr></thead><tbody>')
for m in major_index:
    name=H(m['company'])
    if m['urls']: name='<a href="'+H(m['urls'][0],quote=True)+'">'+name+'</a>'
    parts.append('<tr><td><strong>'+name+'</strong><br>'+H(m['booth'])+'</td><td>'+H(m['exhibit'])+'</td><td>'+H(m['task'])+'</td><td>'+H(m['check'])+'</td></tr>')
parts.append('</tbody></table></div></section><section id="evidence"><h2>7. 技術動向の原文根拠</h2><p>以下は原文の短い連続抜粋。引用の直後に発言者・記事種別と、技術比較への対応を付記した。<a href="../JIMTOF2026_原文エビデンス集_20261022.html">全46抜粋の原文集</a>も参照できる。</p>')
qids=[q for g in guide['evidence_groups'] for q in g[1]]+['Q41']
for qid in qids:
    q=quotes[qid]
    parts.append('<div class="quote"><blockquote>「'+H(q['excerpt_original'])+'」</blockquote><cite>'+H(qid+' '+q['attribution']+'　'+q['published_date'])+'</cite><p><a href="'+H(q['source_url'],quote=True)+'">'+H(q['title'])+'</a>　'+H(q['locator'])+'</p><p><strong>文脈・対応論点：</strong>'+H(q['context_paraphrase'])+'</p><p class="small">'+H(q['not_evidence_for'])+'</p></div>')
parts.append('</section><section id="atlas-section"><h2>8. 全344件 技術・出展索引</h2><p>本編の比較行に採用しなかった候補も残した。分類は既存の詳細ディレクトリの用途別分類。確認深度は候補ごとに異なる。</p><div class="controls"><input id="query" placeholder="企業名・製品名・対象タスクを検索" aria-label="企業名・製品名・対象タスクを検索"><select id="topic" aria-label="カテゴリ"><option value="">全用途</option>'+''.join('<option value="'+H(t['topic_id'])+'">'+H(t['title'])+'</option>' for t in directory['topics'])+'</select><span id="count" class="count"></span></div><div class="table-scroll"><table id="atlas"><thead><tr><th>企業・製品・ブース</th><th>対象タスク</th><th>技術内容・確認深度</th><th>現地確認事項・出典</th></tr></thead><tbody id="atlas-body"></tbody></table></div></section>')
parts.append('<section id="scope"><h2>9. 調査範囲と比較上の留意点</h2><ul>'+''.join('<li>'+H(x)+'</li>' for x in guide['research_notes'])+'</ul><h3>同名538件の出展説明における明示件数</h3>'+table(['用語群','2024年','2026年'],[[s['theme'],s['wording_2024'],s['wording_2026']] for s in strategy['text_signals'][:4]])+'<p class="small">同名かつ両年度に本文がある企業の文言集計。複数カテゴリの重複あり。採用率・性能・新機能数は表さない。詳細URLのない掲載や説明文のない企業があり、全社の技術を完全に分解した調査ではない。</p><p><a href="../../data/research/technical_guide_20261022/content.json">本レポートの構造化データ</a>／<a href="../../data/research/report_v0/case_comparison.json">詳細比較57件</a>／<a href="../../data/research/strategy_review_20261021/exhibitor_coverage_all_2024_2026.csv">全出展者照合CSV</a></p></section></main><footer>JIMTOF2026 事前調査。企業発表・出展告知は性能の独立評価とは区別する。出典へのリンクと掲載位置は構造化データに保存。</footer>')
payload=json.dumps(directory['entries'],ensure_ascii=False).replace('<','\\u003c')
parts.append('<script type="application/json" id="atlas-data">'+payload+'</script><script>const entries=JSON.parse(document.getElementById("atlas-data").textContent);const esc=s=>String(s??"").replace(/[&<>\"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",\'"\':"&quot;"}[c]));function render(){const q=document.getElementById("query").value.toLowerCase();const t=document.getElementById("topic").value;const rows=entries.filter(e=>(!t||e.topic_ids.includes(t))&&[e.company,e.item,e.target,e.technology].join(" ").toLowerCase().includes(q));document.getElementById("count").textContent=rows.length+" / 344件";document.getElementById("atlas-body").innerHTML=rows.map(e=>`<tr><td><strong>${esc(e.company)}</strong><br>${esc(e.item)}<br>${esc(e.booths.join("／"))}</td><td>${esc(e.target)}</td><td>${esc(e.technology)}<span class="status">${esc(e.depth)}／${esc(e.exhibition_status)}</span></td><td>${esc(e.human_boundary)}<span class="sources">${(e.exhibitor_urls_2026||[]).map((u,i)=>`<a href="${esc(u)}">2026出展${i+1}</a>`).join(" ")}</span></td></tr>`).join("")}document.getElementById("query").addEventListener("input",render);document.getElementById("topic").addEventListener("change",render);render();</script></html>')
write(OUT/'JIMTOF2026_技術動向と視察ガイド_20261022.html',''.join(parts)+'\n')
print(f'HTML: {len(categories)} categories, {sum(len(c["rows"]) for c in categories)} comparison rows, {len(major_index)} majors, {len(entries)} atlas entries')
