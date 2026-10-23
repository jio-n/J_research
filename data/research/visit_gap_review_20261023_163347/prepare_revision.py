from pathlib import Path
from collections import Counter
import json,csv,re,unicodedata,copy
D=Path(__file__).parent;R=D.parents[2];BASE=R/'data/research/visit_priorities_20261023_152722'
d=json.loads((BASE/'research.json').read_text(encoding='utf8'));old=copy.deepcopy(d)
ex=json.loads((D/'user_visit_exclusions.json').read_text(encoding='utf8'))
triage=json.loads((D/'unlinked_triage.json').read_text(encoding='utf8'))
TAGS=['AI','フィジカルAI','自律化','自動化'];sources=[];added=[]
def source(k,publisher,title,url,locator,summary,date='未記載',quote='',scope='公式本文の該当節を確認'):
    s=dict(source_id='GR-S'+k,publisher=publisher,title=title,url=url,locator=locator,checked_date='2026-10-23',published_date=date,usage=summary,context_summary=summary,short_quote=quote,verification=scope)
    sources.append(s);return s
n1=source('01','ナガセインテグレックス','GRIDE EYE 製品説明','https://nagase-i.jp/product/product_33.html','特長／同一点比較／AI解析','機上で回転する砥石を同一位置で撮像・比較し、AIで不具合予測とドレス時期を示唆。自動ドレス実行の記載は未確認。')
n2=source('02','日本工作機械工業会・東京ビッグサイト','IMEC2026 オーラルセッション','https://www.jmtba-imec.jp/','10/28 テクニカルセッション1 16:50–17:20 川下智幸氏の講演要旨','研削液が写った画像を生成AIで変換し、その生成画像をCNN分類モデルと物体検出モデルへ入力する研究。講演紹介とブース実演を区別。',quote='研削液の影響を排除',scope='公式HTML本文の講演要旨を直接取得して確認。検索表示は本文を省略する場合あり。')
n3=source('03','科学研究費助成事業／研究代表者 川下智幸','20K04205 CNNを用いた砥石作業面解析','https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-20K04205/','研究期間／研究成果の概要','2020–2022年度の研究は砥面画像から目づまりや砥粒分布をCNNで分類し、ドレス状態とタイミングの判断を支援。','2020-04-01～2023-03-31')
n4=source('04','砥粒加工学会','ABTEC2024 プログラム','https://www.scoop-japan.com/kaigi/abtec/file/ABTEC2024_Program_final_0802.pdf','8/26 A05 第7報、A06 第8報','2024年時点で深層生成モデルによる砥面画像補正・砥面予測と3次元形状データ生成を発表。技術全文や性能値は未読。','2024-08-26',scope='公式プログラムの検索取得部分で題目・著者・時刻を確認。PDF直接取得失敗。論文本文未読。')
n5=source('05','佐世保工業高等専門学校','第9報 生成モデルを用いた砥粒切れ刃の評価','https://www.sasebo.ac.jp/articles/46453/','受賞題目／研究内容','2025年研究は2次元砥面画像から3次元データを生成し、ドレス判断に使う変化を解析。液影響除去とは別の生成用途。','2025-12-11')
n6=source('06','日本工業出版','機械と工具 2026年3月号 公開紹介','https://www.nikko-pb.co.jp/products/detail.php?product_id=6125','特集：坂口彰浩・川下智幸「生成AIによる可視化」','公開要旨は研削液等の影響を排除する可視化技術を説明。購入が必要な記事全文は未読。','2026-03',scope='出版社の商品紹介・要旨のみ確認。記事本文は未読。')
n7=source('07','ナガセインテグレックス','展示会予定','https://nagase-i.jp/','展示会情報 JIMTOF2026','2026年の企業出展を確認。東7 E7097。GRIDE EYEや生成AI研究の個別実演は明記を確認できず。')
c1=source('08','ENCY Software','Cam Agent Beta／ENCY 3.0','https://encycam.com/ency-3-0/','Cam Agent Beta／Setup Helper～Cost Estimate','自然言語で形状認識、工程・工具・切削条件の選択、工具経路生成、シミュレーション、干渉確認とGコード生成を支援。ベータ表記。実機適用・自律再試行の保証は未確認。')
c2=source('09','ENCY Software','ENCY at JIMTOF2026','https://encycam.com/events/ency-at-jimtof-2026-japan/','展示概要／Booth E1053','CAMSUPSがENCYのCAD/CAM機能を展示予定。Cam Agent Beta単体の会場実演範囲は未確認。')
c3=source('10','CAMSUPS','ENCY 3.0とCAM Agentの紹介','https://www.camsups.co.jp/','冒頭 ENCY 3.0／新着情報 10/19','国内販売元もCAM Agent搭載を紹介。10/19出展告知のリンク先は取得できず、製品全体の出展と個別ベータ機能の展示を分ける。')
a1=source('11','ANCA','MX7 ULTRA 公式カタログ','https://machines.anca.com/Anca.CNC/media/Images/Brochures/MX7-ULTRA-EN-digital_4.pdf?ext=.pdf','PDF p.2・4・5：servo／LaserUltra／runout／MTC','LaserUltraによる砥石摩耗対応、工具振れの計測補正、主軸温度の能動管理。iBalanceは作業者をガイド。学習モデルの利用は本文で確認できず。')
ac1=source('12','東京精密','JIMTOF2026 出展日程','https://www.accretech.com/jp/product/measuring/event/20261026_jimtof.html','日程／開催地域／開催会場','企業出展日程のみ確認。個別機種・自動計測パッケージの2026年展示は本文に記載なし。')
ac2=source('13','東京精密','JIMTOF2024 計測自動化','https://www.accretech.com/jp/product/measuring/event/20241105.html','⑥ DuraMax＋TARNAR／Shaftcom 自動化','2024年はDuraMaxと協働ロボット内蔵ストッカTARNARで多品種小ロット測定を自動化。2026年展示を裏付ける資料ではない。','2024-11')
k1=source('14','キーエンス','VSシリーズ AIとルール検査の融合','https://www.keyence.co.jp/products/vision/vision-sys/vs/index_pr.jsp','複数のAI×ルールベース／画作り／歩留まり可視化','良品・不良品学習とルールを組み合わせ、欠陥、検出、分類、OCR等を実行。光学・照明条件整備を含む。生成AI・行動生成の根拠ではない。')
i1=source('15','ifm','SmartLimitWatcher Deep-Dive FAQ','https://www.ifm.com/de/de/shared/industry-4-0-moneo/guide-and-support/faq-deep-dive','SmartLimitWatcher：So funktioniert／PatternMonitorとの違い','物理的に関係する複数センサの履歴から目標変数を予測し、動的な期待範囲との差を検出。単変数統計監視のPatternMonitorと区別。',scope='公式検索取得本文の該当節を確認。直接取得403。')
i2=source('16','ifm','moneo AssistantとIndustrial AI Assistant','https://www.ifm.com/ca/en/shared/industry-4-0-moneo/products/assistant','Powered by／human-in-the-loop／二種類のAssistant比較','moneo AssistantはAzure OpenAIによる自然言語支援と人を介したmoneoサービス実行。Industrial AI Assistantの機械学習による異常検知とは別機能。日本提供・個別展示は未確認。',scope='公式ページをwebツールで本文確認。直接取得403。')
e1=source('17','EROWA','JMS 4.0','https://www.erowa.com/en/products/process-control-system/jms-4','Advantages and Functions／ProductionLine／MoldLine','ERP・MES・CAD/CAMから受注情報を取り込み、機械・パレット・工程を一元管理。MoldLineは計測値と補正値のデータを工程間で接続。AI方式や自律再計画は未確認。')
o1=source('18','オプトン','GW型ロボットベンダー＋協働ロボフォーマ','https://opton.co.jp/recommend/','システム概要／RF-1000／ダイレクトティーチング','3DCADから投入・曲げ・取り出しへ接続。スキャナで設計との差を測り、ベンダーへ補正データを返す。測定軌道はダイレクト教示・再生。AI学習の記載なし。')
o2=source('19','オプトン','JIMTOF出展告知','https://opton.co.jp/','お知らせ 2026/10/16','企業のJIMTOF2026出展を告知。個別システムの実機展示は本文で未確認。','2026-10-16')
q1=source('20','クオリカ','KOM-MICSのスター精密導入','https://www.qualica.co.jp/ja/news/20260518.html','導入効果／切削抵抗一定化 脚注1','異なるメーカーの54設備を一元可視化。切削負荷の測定・分析から負荷一定となるNCプログラムの最適化案を生成する機能を紹介。AI方式や自動実機書込みは未確認。','2026-05-18')
ci1=source('21','シチズンマシナリー','JIMTOF2026 アルカプリソリューション','https://cmj.citizen.co.jp/jimtof2026/alkapply.html','シチズンクラウドサービス：見積支援／図面管理ツール','蓄積された図面と過去見積実績を使い、AIで類似図面検索・見積作成を支援。会場PCでサンプル図面による実演を明記。CNN・LLM等の方式は未記載。')
v1=source('22','CGTech','Vericut Assistant & Intelligence','https://vericut.com/ja-jp/products/ai','Vericut Assistant／Vericut Intelligence','自然言語で操作手順や製品知識へアクセスするAI支援。工具経路やNCを自律変更する機能はこの説明にない。Force最適化とは分離。')
v2=source('23','CGTech','JIMTOF2026 AIサポートと最適化','https://vericut.com/ja-jp/jimtof-2026','展示概要／さらに進化したAIサポート／個別デモ','Vericut 9.7・Icam V27とForceのデモ、強化されたAIサポートを告知。AssistantとIntelligenceの両方を個別実演するかは未確認。')
s1=source('24','スター精密','JIMTOF2026 ソフトウェア','https://star-m.jp/jimtof2026/','Software 03 SMOOSS-i','稼働可視化、加工計画、遠隔操作、プログラム管理を紹介。表示される計画をAI自動最適化すると解釈しない。')
s2=source('25','スター精密','SMOOSS-i','https://star-m.jp/products/lathe/software/smooss-i/index.html','状態監視／停止予定一覧／履歴／プログラム管理','停止予定を見積もって表示し、アラーム通知とプログラム転送・編集を支援。自動再計画は未確認。')
nx=source('26','ネクスタ','スマートF 機能紹介','https://smartf-nexta.com/typed','オプション機能：AI OCR受注登録自動化／PLC連携','受注登録のAI OCR、設備PLC・計量器との連携等を列挙。一部近日リリースを含む注記があり、AI OCR個別の提供開始と展示は未確認。')
na=source('27','不二越','ぶつからないロボット MZS05','https://www.nachi-fujikoshi.co.jp/dcms_media/other/news_20241031.pdf','PDF p.1 特長①','近接センサにより人や障害物が接近すると停止し、障害物が除かれると追加操作なしに再開。AI経路再計画・学習の根拠ではない。','2024-10-31')
nt=source('28','NTTスマートコネクト','AIアバター製造業Web接客のPoC','https://www.nttsmc.com/news/2026/20260908.html','実施概要／実施体制','中小製造業の製品案内を対話化する実証。加工条件や生産計画の判断を実行する根拠はなく、今回の現場技術候補には採用しない。','2026-09-08')

def item(id,row,item_name,task,need,input_,method,output,human,limits,stage,exhibit,exhibit_note,src,tier,themes,reason,reference,questions,related,tag_specs):
    a=next(x for x in d['audit'] if x['row_no']==row)
    tags={t:dict(status='—',reason='今回確認した原典では、このアイテムの当該機能を特定できない。技術の不存在とは断定しない。') for t in TAGS}
    for t,(status,why) in tag_specs.items():tags[t]=dict(status=status,reason=why)
    ss=src+[dict(source_id='GR-E'+str(row),publisher='JIMTOF事務局',title='2026公式出展者台帳：'+a['company'],url=a['detail_url'],locator='保存済み全出展者CSV 行'+str(row),checked_date=a['original_checked_date'],usage='企業名とブースの照合。個別技術の展示を保証しない。')]
    x=dict(id=id,legacy_ids=[],company=a['company'],listing_ids=[a['record_id']],booths=[a['booth']],halls=[{'E':'東','W':'西','S':'南'}[a['booth'][0]]+('アトリウム' if a['booth'][1]=='A' else a['booth'][1]+'ホール')],item=item_name,task=task,need=need,input=input_,method=method,output=output,human=human,limits=limits,stage=stage,exhibit=exhibit,exhibit_note=exhibit_note,sources=ss,source_ids=[s['source_id'] for s in ss],source_urls=list(dict.fromkeys(s['url'] for s in ss)),tags=tags,tag_names=[t for t in TAGS if tags[t]['status']!='—'],depth='企業・研究機関の技術説明まで照合',as_of='2026-10-23',new_review=True,refinement_review='今回原典照合',fresh_review_ids=[s['source_id'] for s in src],company_sites=a['company_urls'],task_ids=[],task_categories=[task],taxonomy_basis='個別機能を原典照合',manufacturer_claim='方式・機能はメーカーまたは研究者の説明。現地性能検証前。',physical_ai_class='実機動作へのAI判断接続は未確認',connection=input_+' → '+method+' → '+output,novelty_note=reference,advance=method,check='／'.join(questions),baseline='従来の定型自動化・手動調整との比較。独立した性能保証ではない。',recommendation='優先訪問' if tier in ['A','B'] else '比較候補',recommend_reason=reason,visit_group='／'.join(themes),overview='対象：'+task+'。方式：'+method+' 出力：'+output,explanation_basis='原典の文脈要約。優先理由・質問は調査者の分析。',technical_attention=reference,booth_priority_note='2026公式台帳に企業名・小間を照合。個別アイテムの展示確度は別欄。',visit_analysis=dict(themes=themes,tier=tier,priority_reason=reason,reference_value=reference,questions=questions,related=related,authorship='優先度・注目理由・質問は調査者の分析。',analysis_basis='今回、企業・研究機関の一次資料の該当節を確認'),suggested_rank=999)
    added.append(x);return x

n=item('GR-N01',517,'GRIDE EYE・生成AI画像変換＋CNN砥面解析','砥石状態監視・ドレス判断','熟練者の音・触感や固定加工量に頼るドレス時期を、砥面状態の定量評価で判断したい。','回転中に機上取得する同一点の砥面画像。研削中画像には研削液が映り込む。','生成AIは研削液の影響を除く画像変換を担当。変換後画像をCNNの分類モデルと物体検出モデルへ入力し、砥面状態を評価する。','砥面の可視化、状態分類・検出と定量評価。製品説明は不具合予測・ドレス時期の示唆。','撮像条件、学習用画像と状態ラベルの準備。判定の妥当性確認。自動ドレスや加工条件変更を誰が承認するかは未確認。','生成モデル名（GAN・拡散等）、液除去後の形態保存、湿潤条件の汎化、処理遅延、商品版への搭載、実機への閉ループ適用は未確認。','GRIDE EYE製品紹介あり。液影響除去＋CNN連結はIMEC2026で紹介する研究。','企業出展確認・個別展示未確認','東7 E7097。IMECは10/28 16:50–17:20の講演。講演とブース実演を混同しない。',[n1,n2,n3,n4,n5,n6,n7],'A',['熟練者知識の形式化','自律制御'],'生成AIの新規性を、液影響のある画像を解析可能にする役割と、従来CNN判定の継続に分けて比較できる。ドレス判断という現場タスクに直結し、ユーザー指定の優先訪問先。','2020–2022年度はCNNによる砥面状態分類。2024年に生成モデルの画像補正・予測を既に発表。2026年は生成画像をCNN分類・検出へ接続する構成が明確。2025年の2D→3D生成は別研究で、同一製品への実装を推定しない。',[
 '生成AIで液影響を除いた後、既存CNN分類器と検出器をそのまま使うのか、生成画像で再学習したのか。モデル構成と変更箇所を示せるか。',
 '生成方式はGAN・拡散・別方式のどれか。湿潤像と乾燥像の同位置ペア、砥粒や目づまりの正解データをどう作るか。',
 '砥粒欠損・目づまりを生成器が消したり描き足したりしないことを、画像評価だけでなく検出精度・ドレス判断精度でどう検証するか。',
 '砥石種類、粒度、研削液、流量、照明が変わった場合の適用範囲・再学習・不確かな画像の棄却条件は何か。',
 '撮像から生成・CNN判定までの遅延は何msか。連続研削中の実処理か、加工の合間に撮像する方式か。',
 'ドレス時期の通知までか、自動ドレス・条件変更まで接続するか。人の承認、品質保証、停止条件はどこに入るか。',
 '2024年第7・8報、2025年第9報から今回までの改善点は何か。商品版GRIDE EYE、研究デモ、今回ブースで見られる機能を分けて示せるか。'
 ],'生成AIの液影響除去、CNN分類・物体検出、2D→3D砥粒評価、ドレス制御への接続。各々の実演・パネル・提供段階を確認。',{'AI':('機能記載','生成AIで画像変換し、CNN分類・物体検出で状態を評価。生成AIはLLMへの置換を意味しない。'),'自動化':('機能記載','回転中砥面の撮像と画像解析を自動化。ドレス動作の自動化は未確認。')})
n['history']=[['2020–2022年度','機上画像から砥面状態をCNN分類。定量評価によりドレス判断を支援。','GR-S03'],['2024年','第7報は深層生成モデルの画像補正・予測、第8報は3次元形状データ生成。研究題目の確認範囲。','GR-S04'],['2025年','2次元画像から3次元データを生成して砥粒形態を評価する第9報。液影響除去と別用途。','GR-S05'],['2026年','液影響を除く生成AI画像変換とCNN分類・物体検出を連結。商品版への搭載・ブース実演は未確認。','GR-S02／06']]
n['role_comparison']=[['生成AI','湿潤画像を解析に適した画像へ変換。形態を捏造しないことの検証が課題。'],['CNN','変換後画像の状態分類と物体検出。観察結果を定量化する後段。'],['制御','ドレス時期の示唆は製品説明あり。自動実行・条件最適化との閉ループは未確認。']]

item('GR-C01',201,'ENCY 3.0 Cam Agent（Beta）','工程設計・工具選定・NC生成','形状から工程・工具・条件を決め、干渉を確認してNCを作るCAM担当の工数を削減。','部品モデル、機械・材料・座標、工具ライブラリと自然言語指示。','AIエージェントが特徴認識、加工戦略・工具・切削条件の選定、工具経路生成とシミュレーションを支援。マクロ記録・再生は別機能。','加工工程、工具経路、干渉チェック、Gコードと時間・コスト見積。','機械・材料・座標等を準備し、生成工程とシミュレーション結果を確認・承認。','ベータ。生成モデル、対応加工範囲、失敗再計画、人の介入点、実機安全保証は未確認。','ENCY 3.0内でBeta機能を公開。','ENCY出展明記・Agent個別実演未確認','E1053でENCY展示を公式告知。Cam Agentの実演可能範囲は別途確認。',[c1,c2,c3],'A',['AIエージェント','熟練者知識の形式化'],'単なる操作FAQより先へ進み、工程・工具・条件の決定から検証まで連結する候補。FANUCの人承認付きCNC支援と比較したい。','自然言語支援、CAM機能呼出し、シミュレーション、Gコードまでの担当範囲を比較できる。ロボット向けOLP機能の存在だけで、実機の学習型自律動作とは認定しない。',['未知形状から工程・工具・条件を選ぶ際、LLM推論、規則、加工フィーチャDB、既存CAM計算をどう分担するか。','工具欠落・干渉・到達不能を検知すると、エージェント自身が工程を再構成するか。途中承認・手動修正箇所はどこか。','Betaの対象機種・加工方式・日本語対応と、今回実演できるモデル→NCの範囲は何か。'],'Cam Agent Betaと、ルール／マクロの自動化、ENCY RobotのOLPを別々に確認。',{'AI':('機能記載','Cam Agentの工程・工具・条件選択とCAM処理を公式説明。'),'自律化':('人承認付き','CAM工程生成と検証を連続支援するが、実機適用の完全自律性は未確認。'),'自動化':('機能記載','工具経路とGコードの生成、シミュレーションを自動化。')})
item('GR-A01',50,'MX7 ULTRA：LaserUltra・MTC・振れ補正','工具研削の機上計測・補正制御','バッチ研削中の寸法変動、砥石摩耗、温度変動によるばらつきを抑える。','工具切れ刃のレーザ計測、振れ情報、主軸温度と運転条件。','LaserUltraで輪郭計測と砥石摩耗補正。iGrindで振れを計測補正し、MTCが主軸温度を能動管理。','工具形状・振れの補正、主軸の熱安定化。','工具形状・公差・補正上限を準備。iBalanceの推奨を用いたバランス調整は人の作業。','具体的な学習モデルは未確認。公差値はカタログの条件内。AIMS連携の2026展示は未確認。','市販機のメーカー説明。','機種は保存済み出展説明に記載','E1066の主出展物はMX7 ULTRA。各補正機能の会場デモ内容は未確認。',[a1],'B',['自律制御'],'ナガセの砥面状態判断と対比し、計測値を補正に戻す既存の閉ループ制御を確認できる。','ナノメートル軸制御と機上計測・能動温度管理の組合せ。AI呼称を使わず、制御で達成できる領域の比較基準。',['LaserUltraの計測結果はどの補正量へ反映し、いつ再研削するか。補正限界で自動停止するか。','MTCは温度一定化か熱変位予測補正か。学習モデルを使う部分はあるか。','今回AIMS・外部測定との接続まで見られるか。機内補正と工場のデータ連携を分けて説明できるか。'],'LaserUltra、MTC、iGrind振れ補正、AIMSの有無を個別確認。',{'自律化':('限定機能','計測値に基づく寸法・振れの補正と主軸温度の能動管理。'),'自動化':('機能記載','計測・補正を研削サイクルへ組み込む。')})
item('GR-T01',484,'DuraMax＋TARNAR：多品種自動計測（技術照会対象）','検査段取り・搬送・三次元計測','多品種小ロットの測定に伴う投入・段取り待ちを削減。','測定対象ワーク、測定プログラム、ストッカの配置と品種情報。','協働ロボット内蔵ストッカから三次元測定機へ投入し、測定を連続化。','自動供給・回収と三次元測定結果。','治具・品種・測定プログラム・ロボット受渡しの事前準備。','技術根拠は2024年の公式展示紹介。2026年同機種展示やAI測定経路生成は未確認。','過去の展示で紹介済みの自動計測方式。','企業出展確認・個別展示未確認','東7 E7044。2026公式ページは日程のみ。2024のE7027と混同しない。',[ac1,ac2],'B',['全体最適'],'検査工程を加工・搬送と接続するための多品種計測セルを比較する候補。','搬送の自動化と、品種変更に追従して測定を自律生成する機能の差を見る。2024年実績を2026年新規性と扱わない。',['2026年はTARNAR連携または後継の自動計測セルが見られるか。','新規品の治具・把持・測定プログラムを誰が何時間で準備するか。品種切替に画像認識やAIを使うか。','寸法NGは加工機へ補正値を返すか。基準座標と補正許容範囲を誰が管理するか。'],'DuraMax・TARNAR、Shaftcom自動化、加工機への寸法補正接続。',{'自動化':('機能記載','ロボット搬送と計測サイクルの自動接続を2024公式資料で確認。2026展示は未確認。')})
item('GR-K01',187,'VSシリーズ：良品・不良品学習AI＋ルール検査','外観検査・異常識別','ルールで表しにくい欠陥と、寸法・位置等の確定的検査を同じ装置で扱う。','照明・光学ズームで取得する画像、良品・不良品の学習データ。','AI欠陥・検出・分類・OCRとルール検査を組合せる。画作りと判定条件の調整を支援。','欠陥の検出・分類結果と検査画像・歩留まり情報。','撮像、学習例、しきい値、検査順序とNG処理を設定。','CNN・基盤モデル等の内訳は公開ページで未確認。行動生成や未知ワークへの適応実証は確認できない。','メーカー製品紹介あり。','企業出展確認・個別展示未確認','南4 S4021。VSやVS-Gの個別展示は未確認。',[k1],'B',['熟練者知識の形式化'],'ナガセの生成前処理＋CNNと比較し、画像品質の整備、学習判定、ルールの分担を確認する。','AI検査でも撮像条件とルールの設計が性能を左右する。生成AI・フィジカルAIとは自動的に同一視しない。',['良品学習・不良品学習のどちらが必要か。未知欠陥と反射・液付着の区別をどう評価するか。','AIと幾何・寸法ルールをどう組み合わせ、NGの理由を現場に示すか。','今回展示機種と、少数画像学習・追加学習・画像保存の具体的な操作を見られるか。'],'VSとVS-Gの展示機種、画作り、学習追加、NG出力後のライン連携。',{'AI':('機能記載','良品・不良品学習の欠陥・分類・検出・OCRを説明。'),'自動化':('機能記載','設定した検査処理を画像入力ごとに実行。')})
item('GR-I01',3,'moneo SmartLimitWatcher：動的しきい値監視','設備状態監視・異常検知','運転条件で正常値が変わるため、固定しきい値の誤警報を減らす。','物理的に関係する複数のセンサ時系列と監視する目標変数。','履歴から予測モデルを学習し、予測目標値と動的な期待範囲を作って実測との差を監視。','異常度・警告・アラーム。','正常履歴、関連変数、感度と警報条件を選び、状態変化時は監視を見直す。','生成AI対話支援とは別。詳細アルゴリズム、日本の提供版、2026実演、機械の自動是正は未確認。','機械学習によるメーカー製品説明。','企業出展確認・個別展示未確認','南3 S3061。機能の説明は海外公式資料。国内展示を事前確認。',[i1,i2],'B',['自律制御'],'複数センサの物理的関係から正常範囲を学ぶ方式は、加工状態監視・データ取得サービスの設計比較に有用。','多変量予測に基づく動的しきい値と、単変数統計監視やLLMの説明生成を切り分ける。',['どの変数を物理的関係ありと選ぶか。運転モード変更や材料変更で学習を分けるか。','異常履歴がなくても開始できるか。真の故障と条件変化を分け、誤警報をどう測るか。','警報から設備停止・条件変更まで実行できるか。日本向け提供版と今回のデモ対象は何か。'],'SmartLimitWatcher、PatternMonitor、LifetimeEstimatorと生成AI Assistantを別機能として確認。',{'AI':('機能記載','センサ履歴から予測モデルと正常範囲を学習。'),'自律化':('限定機能','条件依存の期待範囲から継続的に異常を検出。設備の自動是正は未確認。'),'自動化':('機能記載','状態監視と警報を自動実行。')})
item('GR-I02',3,'moneo Assistant：生成AIによるIIoT操作支援','設備データ照会・監視システム操作','監視データと専門知識を探し、定型的なmoneo操作を行う工数を減らす。','自然言語指示、許可されたmoneoデータとifmの情報。','Azure OpenAIの言語機能とmoneoサービスを統合し、人を介して定型操作を実行。','自然言語の説明・推奨とmoneo内のサービス操作。','アクセス権設定と実行承認。データや応答の妥当性確認。','実行可能サービスの種類と取消、安全境界、日本提供版・今回展示は未確認。物理設備の走行・加工を生成する根拠はない。','海外公式クラウド機能の紹介。','企業出展確認・個別展示未確認','南3 S3061。日本向け導入・実演は要照会。',[i2],'B',['AIエージェント'],'生成AIの担当がチャット応答だけか、データ取得・設定等のツール実行までかを比較できる。','機械学習型の異常検知と、生成AI型の自然言語操作を分離し、権限と人承認の設計を見る。',['どのmoneoサービスを実行できるか。読出し、設定書込み、アラーム変更の権限を分けて示せるか。','提案の根拠データ、実行ログ、承認、取消・ロールバックをどう残すか。','日本提供と今回の展示対象か。物理設備制御へ接続する場合の責任範囲はどこか。'],'自然言語照会だけのデモと、人承認付きサービス実行の両方を確認。',{'AI':('機能記載','生成AIの自然言語理解とmoneoサービス連携。'),'自律化':('人承認付き','人を介してmoneoの定型サービスを実行すると説明。'),'自動化':('機能記載','情報取得と定型システム操作を支援。')})
item('GR-E01',131,'JMS 4.0 ProductionLine／MoldLine','工程横断ジョブ管理・計測データ連携','異機種設備、パレット、計測・清掃等の工程を一元的に管理する。','ERP・MES・CAD/CAMの受注データ、機械状態、ワークID、測定値と補正値。','ジョブ・パレット・工程を中央管理し、順序・優先度を制御。MoldLineは計測と補正の自動データフローを接続。','セル・工程の指示と状態管理、計測・補正情報の受渡し。','ジョブ優先度、工程、接続機械、IDと補正の整合を設定。','AI学習、停止時の自動再計画、工場全体での最適性は原典で未確認。','メーカーの市販システム説明。','企業出展確認・個別展示未確認','南1 S1068。JMS各版の個別実演は未確認。',[e1],'B',['全体最適'],'工程をまたぐデータと指示を実際に受け渡す管理層として、工作機械単体の自律化と比較したい。','異機種・異工程のID、測定値、補正値を接続する構成。AIがなくても工程接続を実現できる反例になる。',['ジョブの順序・優先度は人が決めるか、自動計算か。故障・工具不足時の再配分範囲はどこまでか。','測定値とオフセットを加工機へ渡す際、単位・座標・加工面・品番をどう照合するか。','JMSのどの版とオプションを今回は見られるか。他社制御装置を含む実例はあるか。'],'ProductionLineとMoldLine、ロボットセル、計測補正連携の展示有無。',{'自動化':('機能記載','工程情報・ジョブ・パレットと測定補正データの自動接続。')})
item('GR-O01',160,'GWベンダー＋RF-1000：3D計測フィードバック','パイプ曲げ・自動測定・形状補正','職人の試し曲げと修正作業を減らし、投入から良品化まで接続する。','3DCAD形状、加工済みパイプの3Dスキャンと設計差分。','ロボットベンダーが投入・曲げ・取出しを行い、協働ロボフォーマの測定差を補正データとして戻す。','曲げ補正値と補正加工。','曲げ型と加工条件を準備。測定軌道は手動ダイレクト教示・再生。','補正の学習方式、反復回数・収束保証、異材対応は未確認。ロボット＋スキャナという構成だけでフィジカルAIとはしない。','メーカーのシステム紹介。','企業出展確認・個別展示未確認','東1 E1007。2026出展告知のみ確認、構成一式の展示は要照会。',[o1,o2],'B',['自律制御','全体最適'],'CAD→曲げ→計測→補正の閉ループが具体的で、ユーザー関心の工程接続をAI以外の方式と比較できる。','生成AIやVLAを使わない計測・幾何補正でも実現する適応範囲を見極める。人の教示負担が重要。',['補正は角度・長さ・ねじれのどの誤差を扱い、何回で収束するか。許容外ではどう停止するか。','測定軌道と把持・受渡しを新規品へ展開するのに、CAD自動計算と人の教示がそれぞれどれだけ必要か。','材料ロットやスプリングバックの変化は再学習か、幾何計算で補正か。今回の実機デモ範囲はどこまでか。'],'GW-SWV-15、RF-1000、補正フィードバックの実演。',{'自律化':('限定機能','測定した設計差を曲げ補正へ戻す限定的な閉ループ。'),'自動化':('機能記載','投入・曲げ・取出し・計測を接続。')})
item('GR-Q01',219,'KOM-MICS：切削負荷可視化・NC最適化支援','設備データ収集・加工条件改善','異メーカー機の負荷と稼働をそろえ、工具と加工条件を見直したい。','設備稼働状態、加工中の切削抵抗、任意接続の電力量。','データをクラウド収集して横断可視化。切削抵抗一定化機能で負荷一定となる加工プログラム最適化を提案。','改善判断のためのデータとNC最適化提案。','工具・材料・工程との対応付け、改善案の評価と実機適用判断。','AI学習・自動実機書込み・オンライン制御はこの説明では未確認。導入事例の改善量は個別条件の結果。','54設備を接続したメーカー公表事例あり。','企業出展確認・個別展示未確認','東1 E1058。事例の説明とJIMTOFでの個別展示は分離。',[q1],'B',['自律制御','全体最適'],'データ基盤を可視化で終わらせず、NC条件の改善提案へ結びつける具体例として比較する。','54設備の一元管理と、3台での加工改善事例。負荷一定化はAIと同義ではなく、制御・最適化の役割を質問する。',['切削抵抗はセンサで測るか、主軸・軸モータ情報から推定するか。機械間でどう校正するか。','負荷一定化のNC最適化は物理モデル、経験則、AIのどれか。変更・承認・実機転送を誰が行うか。','54設備の可視化から生産計画や工程再配分まで連携するか。今回見られる機能は何か。'],'切削抵抗一定化、異メーカーのデータ取得、承認後のNC反映経路。',{'自動化':('機能記載','設備情報の収集と加工プログラム最適化提案を支援。実機適用は未確認。')})
item('GR-CI01',349 if False else next(a['row_no'] for a in d['audit'] if 'シチズンマシナリー' in a['company']),'見積支援／図面管理ツール（アルカプリ）','類似図面検索・見積作成','過去図面・見積実績の探索と転記を減らし、見積品質を安定させる。','顧客が保有する過去図面と見積実績、新規のサンプル図面。','AI技術で類似図面を検索し、過去実績に基づく見積作成を支援。','類似図面と見積作成支援結果。','図面・実績の登録、検索結果・加工内容・最終見積の確認。','特徴量・検索モデル・見積計算の内訳は未確認。NC生成や加工条件決定までの連結は確認できない。','クラウドサービスとして紹介。','会場PCでの実演を明記','南2 S2002。サンプル図面を使った見積・図面管理の実演。',[ci1],'B',['熟練者知識の形式化'],'既存台帳は自動旋盤の加工・計測連携が中心で、見積経験の再利用というAI担当が抜けていた。','過去の実績をどの単位で形式化し、形状類似と加工工数・価格をどう関連付けるかが比較点。',['形状の類似と加工工程の類似をどう区別するか。材料・公差・ロット・設備差を見積へ反映するか。','熟練者が価格や工程を修正した理由は学習・検索へ戻せるか。誤った類似例を排除できるか。','サンプルだけでなく自社図面へ展開する登録工数・権利・データ分離と、NC工程への連結範囲はどうか。'],'図面検索と見積推定の内訳、アルカートCNCウィザードとの連携。',{'AI':('機能記載','AI技術による類似図面検索と見積支援を出展ページで説明。'),'自動化':('機能記載','図面探索と見積作成を支援。最終見積は人が確認。')})
item('GR-V01',next(a['row_no'] for a in d['audit'] if 'CGTech' in a['company']),'Vericut Assistant／Intelligence：操作・知識支援','NC検証ソフトの操作支援・知識検索','検証ソフトの使い方と機能情報を探す時間を減らす。','自然言語の操作質問と製品知識。','AIアシスタントが操作手順のガイダンスや機能説明を返す。','操作手順・説明。','ガイダンスの確認と、実際の検証設定・NC修正・実機適用。','工程自動設計やAIによるNC条件変更はこのAIツール説明では未確認。Forceの物理最適化と別。','Vericut 9.6で導入されたAI機能と説明。','AI支援を出展告知・個別実演範囲未確認','南3 S3014。強化AIサポートの告知あり、両アシスタントの実演範囲は要確認。',[v1,v2],'C',['AIエージェント'],'名称がAIでも判断・実行の担当範囲が異なる比較例として、CAM AgentやCNC連携と並べる。','製品知識の対話検索を、加工条件の物理モデル最適化やツール実行と混ぜない。',['回答を表示するだけか、検証設定や最適化機能を実際に呼び出せるか。','機械構成・NC・アラーム等のユーザープロジェクトを理解するか。根拠、守秘、誤回答の扱いはどうか。','今回のAIデモとForceデモで、AIが決めた箇所を画面上で区別できるか。'],'Assistant、Intelligence、Forceの役割を別々に確認。',{'AI':('機能記載','AIによる自然言語ガイダンスと知識検索。'),'自動化':('機能記載','操作情報の探索・提示を自動支援。')})
item('GR-ST01',next(a['row_no'] for a in d['audit'] if a['company']=='スター精密株式会社'),'SMOOSS-i：監視・計画表示・遠隔操作','加工実績収集・停止予定把握・プログラム管理','設備停止や刃具交換の予定を把握し、プログラム管理と現場作業を効率化。','NCの運転・停止・加工数、加工予定数、プログラムと作業記録。','稼働履歴の収集、停止予定表示、アラーム通知とプログラム転送を接続。','状態一覧・残時間・通知・プログラム管理。','加工予定と作業記録の設定、プログラム編集・転送判断、現場処置。','展示紹介の加工計画という語だけでは自動スケジューリングを認定しない。AI・自動再計画は未確認。','メーカーの市販ソフト説明。','2026特設ページに展示紹介','南1 S1003。具体的な遠隔操作のデモ範囲は現地確認。',[s1,s2],'C',['全体最適'],'自動旋盤本体の候補に埋もれていたソフト機能を分け、計画表示と実行判断の境界を確認する。','監視・計画・プログラムがつながる段階と、AIが自動再計画する段階を混同しない。',['加工計画は人が入力するか、制約に従い自動編成するか。停止で残り工程を再配分できるか。','切削条件や補正値の変更と遠隔承認に、権限・記録・機械側インターロックがあるか。','SMOOSS-iと他社MES・スケジューラを接続できるか。今回のソフト操作を見られるか。'],'SMOOSS-iの計画、遠隔操作、履歴とPU-Advanceとの違い。',{'自動化':('機能記載','稼働情報収集・停止予定表示・通知とプログラム管理を支援。')})
item('GR-NX01',596,'スマートF：AI OCR受注登録・PLC連携','受注情報入力・実績収集','手書き・転記と設備実績の手入力を減らす。','受注帳票、設備PLC、計量器と既存システムデータ。','オプションとしてAI OCR受注登録自動化、PLC・計量器・既存システム連携を列挙。','受注登録と生産管理向け実績データ。','帳票対応、マスタ整備、読取結果の確認と連携設定。','一部近日提供を含む表示のため、各機能の提供開始・AI方式・展示は未確認。AI生産計画とは認定しない。','オプション一覧に記載、提供状況要確認。','企業出展確認・個別展示未確認','南4 S4010。OCRとPLCの個別デモ・リリース状況は要確認。',[nx],'C',['全体最適'],'計画の前提になる受注と現場実績をどう集めるか、入力自動化の不足領域を補足できる。','AI OCRとPLC連携は異なる担当機能。OCRの存在を生産計画AIの存在へ広げない。',['AI OCRはどの帳票・項目を読み、誤読や品目マスタ不一致を誰が修正するか。正式提供済みか。','PLC実績と受注・工程・ロットをどのIDで対応付けるか。','実績変化から計画を自動更新するのか、担当者の生産調整を支援するのか。今回の展示範囲は何か。'],'AI OCR、PLC接続、既存システム連携。正式提供済みと予告機能を分離。',{'AI':('呼称・用途記載','AI OCR受注登録自動化を機能一覧に記載。方式・提供時期未確認。'),'自動化':('機能記載','受注登録やPLC・計量器とのデータ連携。提供範囲要確認。')})
item('GR-NA01',652,'COPARO MZS05：近接検知・停止再開（技術照会対象）','協働搬送の安全停止・動作再開','人との接触前に停止し、協働作業時の待ちと不安を減らす。','本体の接近センサ信号と、教示済みのロボット動作。','人・障害物の接近を検知して減速・停止。障害物除去後は追加操作なしで動作を再開。','安全側の停止と動作再開。','動作教示、ハンド・ワークを含むリスク評価、適用条件・安全距離の設定。','近接検知は学習型の行動生成や障害物回避経路計画の根拠ではない。2026展示は未確認。','2024年公表製品。','企業出展確認・個別展示未確認','機械系は東3 E3009、工具は西1 W1092。MZS05の展示先・実演は事前確認。',[na],'C',['自律制御'],'状態に応じた停止再開を、AIによる経路の自動再構成と区別する比較候補。','追加操作なしの再開があっても、固定の安全動作か未知環境での動作判断かを分ける。',['接近を検知した後は停止・再開のみか、迂回や再把持を計画するか。','ハンド・ワークがセンサを覆う場合と、導体・非導体等の対象差の検知限界は何か。','2026会場の展示機種・場所はどこか。新シリーズでAIを使う機能があるなら入力と出力を示せるか。'],'MZS05または後継、近接検知、再開操作、AI機能の有無。',{'自律化':('限定機能','接近に応じた停止と、障害物除去後の追加操作なし再開に限定。'),'自動化':('機能記載','教示済み搬送の自動実行と停止再開。')})

for x in added:
    for s in x['sources']:
        if not s['url']:
            s.update(url='https://github.com/jio-n/J_research/blob/main/data/exhibitors_2026_with_details.csv',title='保存済みJIMTOF2026全出展者台帳',locator='CSV内のexhibitor_record_id・企業名で照合。候補JSONのlisting_idsに対象IDを保持。',usage='公式サイトから保存済みの台帳。会社とブースの対応を確認。今回ライブ出展本文を取得した意味ではない。')
    x['source_urls']=list(dict.fromkeys(s['url'] for s in x['sources']))

def norm(s):return re.sub(r'[^a-z0-9一-龥ぁ-んァ-ヶー]','',unicodedata.normalize('NFKC',s).lower().replace('株式会社',''))
excluded=[]
for e in ex['companies']:
    aa=[a for a in d['audit'] if norm(a['company'])==norm(e['company'])]
    assert aa,e
    e['master_booths']=list(dict.fromkeys(a['booth'] for a in aa))
    e['booth_check']='一致' if e['booth'] in e['master_booths'] else '共同出展の枝番差（写真は親小間、台帳は枝番付き）。企業名で照合。'
    xx=[x for x in d['items'] if norm(x['company'])==norm(e['company'])]
    e.update(record_ids=[a['record_id'] for a in aa],item_ids=[x['id'] for x in xx],decision='訪問対象外（ユーザー判断）',technical_judgment='関連性の否定ではない。訪問しない理由の詳細は未提示。',decision_date='2026-10-23')
    for x in xx:
        x['visit_decision']=e['decision'];x['exclusion_company']=e['company'];excluded.append(x)
        if x in d['items']:d['items'].remove(x)
    for a in aa:a['visit_decision']=e['decision']
ex['excluded_item_count']=len(excluded)
(D/'user_visit_exclusions.json').write_text(json.dumps(ex,ensure_ascii=False,indent=2),encoding='utf8')
assert not any(norm(x['company']) in {norm(e['company']) for e in ex['companies']} for x in added)
d['items']+=added
for x in d['items']:
    x['visit_decision']='未選定'
    x['_order']=0.5 if x['id']=='GR-N01' else 0.8 if x['id']=='GR-C01' else x.get('suggested_rank',999)
d['items'].sort(key=lambda x:(x['visit_analysis']['tier'],x['_order']))
for i,x in enumerate(d['items'],1):x['suggested_rank']=i;x.pop('_order',None)
for x in added:
    a=next(a for a in d['audit'] if a['record_id']==x['listing_ids'][0]);a['item_ids'].append(x['id']);a['tag_names']=list(dict.fromkeys(a['tag_names']+x['tag_names']));a['status']='候補あり（今回追加）';a['reason']='企業・研究公式資料で個別技術を補足。個別展示未確認はアイテムに明記。'

review=[]
for x in added:
    review.append(dict(company=x['company'],booth='／'.join(x['booths']),record_ids=x['listing_ids'],item_ids=[x['id']],decision='候補追加',basis=x['item']+'。'+x['exhibit'],depth='企業・研究公式の技術説明を確認',urls=x['source_urls'],remaining=x['limits']))
for company,reason,urls in [
 ('NTTスマートコネクト','製造業Web接客のAI実証は確認。加工・検査・搬送・計画等の現場タスクを担当する技術とは確認できず、今回追加保留。',[nt['url']]),
 ('伊藤忠テクノソリューションズ','保存済み説明が不足。会社名からシミュレーション・フィジカルAIの個別展示を推定しない。追加原典未確認。',[]),
 ('GUGEN','保存済み説明が不足。IoT分野というだけで学習・判断機能を割り当てない。追加原典未確認。',[]),
 ('GENIO Solutions','保存済み説明が不足。対象タスクと展示製品を特定できず、追加原典未確認。',[]),
 ('ミクロン精密','研削機の型式はあるが個別AI・適応制御機能と2026実演を未確認。研究計画と市販機を接続して認定しない。',[]),
 ('日進機械製作所','一般的な精度・能率説明から自律制御を認定できず。個別技術資料は追加未確認。',[]),
 ('長島精工','説明不足。制御方式・判断の担当と展示アイテムは追加未確認。',[]),
 ('豊和工業','保存済み紹介不足。企業の出展と、ロボット・自動ラインの個別展示を分けて保留。',[]),
 ('SHODA','WebServiceは監視・支援との記載。自動判断や機械実行の範囲を特定できず、今回は追加保留。',[]),
 ('大昭和精機','工具の高精度化・段取り改善が中心。具体的なAI・自律判断を現行保存資料では特定できず。',[]),
 ('アメテック','計測器の一般説明のみで、AI・自動測定タスクを特定できず。追加原典未確認。',[])
]:
    aa=[a for a in d['audit'] if norm(company) in norm(a['company'])]
    review.append(dict(company=company,booth='／'.join(dict.fromkeys(a['booth'] for a in aa)),record_ids=[a['record_id'] for a in aa],item_ids=[],decision='追加保留（非該当と断定しない）',basis=reason,depth='公式技術本文確認' if urls else '保存済み台帳の説明確認・追加深掘り未完了',urls=urls,remaining='個別製品の担当機能と2026年展示を確認。'))

by_record={}
for v in review:
    for r in v['record_ids']:by_record.setdefault(r,[]).append(v)
ex_records={r for e in ex['companies'] for r in e['record_ids']}
for q in triage:
    rr=by_record.get(q['record_id'],[])
    q['review_depth']='台帳の語句・製品分野による一次点検（個別技術の精読を意味しない）'
    q['decision']='追加調査未完了・候補認定保留'
    q['reason']='情報不足を非該当と断定しない。'
    q['new_item_ids']=[];q['review_urls']=[]
    if rr:
        q['review_depth']='／'.join(dict.fromkeys(v['depth'] for v in rr));q['decision']='／'.join(dict.fromkeys(v['decision'] for v in rr));q['reason']='\n'.join(v['basis'] for v in rr);q['new_item_ids']=[i for v in rr for i in v['item_ids']];q['review_urls']=list(dict.fromkeys(u for v in rr for u in v['urls']))
    if q['record_id'] in ex_records:q['decision']='訪問対象外（ユーザー判断）';q['reason']='関連技術の可能性を残したまま、ユーザーが今回は訪問しないと指定。'
    q.pop('exhibition_content',None);q.pop('main_exhibits',None)
(D/'unlinked_triage.json').write_text(json.dumps(triage,ensure_ascii=False,indent=2),encoding='utf8')
d['excluded_items']=excluded;d['user_exclusions']=ex;d['gap_review']=review;d['additional_sources']=sources
d['edition']=D.name;d['planner_version']=D.name;d['base_file']=str(BASE.relative_to(R)).replace('\\','/')+'/research.json'
d['previous_edition_stats']=old['stats'];st=d['stats'];st['candidate_items']=len(d['items']);st['candidate_companies']=len({norm(x['company']) for x in d['items']});st['researched_items_including_user_excluded']=len(d['items'])+len(excluded)
for k in ['retrieval_unique_urls','retrieval_body_success_unique','refined_items','fresh_review_items','reviewed_sources','recommendations']:st.pop(k,None)
st['priority_counts']=dict(Counter(x['visit_analysis']['tier'] for x in d['items']));st['tag_counts']={t:dict(Counter(x['tags'][t]['status'] for x in d['items'] if x['tags'][t]['status']!='—')) for t in TAGS};st['overlapping_tag_items']=sum(sum(x['tags'][t]['status']!='—' for t in TAGS)>1 for x in d['items']);st['interest_counts']=dict(Counter(t for x in d['items'] for t in x['visit_analysis']['themes']));st['depth_counts']=dict(Counter(x['depth'] for x in d['items']));st['linked_master_rows']=sum(bool(a['item_ids']) for a in d['audit']);st['audit_status']=dict(Counter(a['status'] for a in d['audit']));st['user_excluded_companies']=len(ex['companies']);st['user_excluded_items']=len(excluded);st['new_items']=len(added)
d['analysis_scope']['current_gap_review']=dict(base_items=390,unlinked_master_rows=794,triage_counts=dict(Counter(q['triage'] for q in triage)),focused_review_entries=len(review),added_items=len(added),additional_primary_sources=len(sources),user_excluded_companies=27,excluded_existing_items=len(excluded),note='全794行は語句と製品分野で一次点検。個別公式資料まで確認した範囲は追加候補と原典確認済み行。未確認企業の全製品を非該当とはしない。原典数は出典台帳の単位で、全て全文精読ではない。')
d['analysis_scope']['scope_note']='前版の技術分類は継承。今回追加分の根拠・限界を個別記載。ユーザー指定27社は技術評価を消さずに訪問計画から除外。'
(D/'research.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def csvout(name,rows,headers):
    with (D/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=headers);w.writeheader()
        for a in rows:w.writerow({k:'／'.join(a.get(k,[])) if isinstance(a.get(k),list) else a.get(k,'') for k in headers})
csvout('user_visit_exclusions.csv',ex['companies'],['company','booth','master_booths','booth_check','decision','technical_judgment','decision_date','record_ids','item_ids'])
csvout('gap_review.csv',review,['company','booth','decision','depth','basis','remaining','item_ids','urls'])
csvout('unlinked_triage.csv',triage,['row_no','record_id','company','booth','triage','signals','review_depth','decision','reason','new_item_ids','review_urls','listing_url'])
csvout('recommended_visits.csv',[dict(id=x['id'],company=x['company'],booth=x['booths'],priority=x['visit_analysis']['tier'],item=x['item'],reason=x['visit_analysis']['priority_reason'],exhibit=x['exhibit']) for x in d['items'] if x['visit_analysis']['tier'] in ['A','B']],['id','company','booth','priority','item','reason','exhibit'])
print(json.dumps(dict(active=len(d['items']),added=len(added),excluded_companies=27,excluded_items=len(excluded),priorities=st['priority_counts'],tag_counts=st['tag_counts']),ensure_ascii=False))
