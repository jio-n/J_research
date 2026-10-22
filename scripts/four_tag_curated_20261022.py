"""Source-reviewed additions and corrections; no tag inheritance across a company."""
import re
import unicodedata

def norm(s):return re.sub(r'[\s・･,，.．()（）]','',unicodedata.normalize('NFKC',s)).replace('株式会社','').replace('合同会社','').lower()

def enrich(items,rows,date,tagnames):
    index={x['id']:x for x in items}
    sources={}
    def source(key,publisher,url,title,locator,quote=''):
        sources[key]={'source_id':key,'publisher':publisher,'url':url,'title':title,'locator':locator,'checked_date':date,'usage':'技術説明・展示の根拠（今回本文を確認）','short_quote':quote}
        return key
    source('FT01','ファナック','https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260911.html','AI溶接エージェント（2026/9/11）','概要／図面読み取り／溶接条件・動作生成／発売予定','部品の図面を読み取り、ロボットの溶接プログラムを自動で生成')
    source('FT02','ファナック','https://www.fanuc.co.jp/ja/JIMTOF2026/','JIMTOF2026 特設ページ','FA／ROBOT：フィジカルAI CNC・オープンプラットフォーム等')
    source('FT03','ファナック','https://www.fanuc.co.jp/ja/product/cnc/physical-ai-cnc/index.html','フィジカルAI CNC 特設ページ','CONCEPT／MCP／デジタルツイン検証／実現すること','その結果をオペレータが確認・承認した上で実機へ適用できます。')
    source('FT04','ファナック','https://www.fanuc.co.jp/ja/product/robot/academia/case_study/ai-agent-robot-kitting-system.html','AIエージェントによるキッティング','自然言語指示／マスタレスAIワーク認識')
    source('FT05','ファナック','https://www.fanuc.co.jp/ja/product/robot/academia/case_study/moving-parts-ai-tracking-screwdriving.html','動く部品を追いかけ、ねじ締め','ワーク追従／3次元空間リアルタイム追従')
    source('FT06','ファナック','https://www.fanuc.co.jp/ja/product/robot/academia/case_study/imitation-learning-ai-robot.html','人の作業を模倣するAIロボット','遠隔操作データ／VLA模倣学習／自律折り畳み','VLA(Vision-Language-Action)の基盤モデルに対する模倣学習')
    source('FT07','DMG森精機','https://www.dmgmori.co.jp/corporate/news/2026/20261019_serviceagent.html','my DMG MORI サービスエージェント（2026/10/19）','提供開始／マニュアル検索／診断・問い合わせ生成／GENIACは今後')
    source('FT08','DMG森精機','https://www.dmgmori.co.jp/corporate/news/2026/20261016_jimtof2026.html','JIMTOF2026出展（2026/10/16）','東8 E8005：GX Flex／AMR／DX体験エリア')
    source('FT09','ModuleWorks','https://www.moduleworks.com/see-you-at-jimtof-2026/','See You at JIMTOF2026（2026/10/15）','physics-based machining／NGSP・CAS・MDES／GPU simulation')
    source('FT10','Phoxter','https://www.phoxter.co.jp/news/jimtof2026','JIMTOF2026出展（2026/10/19）','展示の見どころ1～4／S4028')
    source('FT11','Phoxter','https://www.phoxter.co.jp/automated-logistics/products/stelladrive','StellaDrive','AI CHATBOT／SLAM・2Dコード／後方LiDAR','生成AIによるトラブルシューティングChatbotを搭載（オプション）。')
    source('FT12','GAZIRU','https://gaziru.co.jp/blogs/19gxg1fly3zd','JIMTOF2026出展（2026/9/30）','GAZIRU.z V5とGAZIRU.eye／東3 E3008')
    source('FT13','GAZIRU','https://gaziru.co.jp/eye','GAZIRU.eye 異常検知','正常画像のみ／エンジン選択／REST API／個別システム構築')
    source('FT14','GAZIRU','https://gaziru.co.jp/blogs/4j7fi3f3fiyg','AI異常検知と個体識別技術（2026/9/7）','2：教師なし異常検知／3：微細紋様照合／5：履歴連携')
    source('FT15','CKD','https://www.ckd.co.jp/en/event/jimtof2026/','JIMTOF2026（2026/9/23）','W4064／robot handling・assembly／FSH・FSB・QREC等')
    source('FT16','autonomIQ','https://www.autonomiq.de/','Intelligente CAM-Software für die CNC-Fertigung','KI-Unterstützung／Geometrieerkennung／Werkzeugauswahl／NC-Code')
    source('FT17','米沢工機','https://www.yonek.co.jp/news/event/yonezawa-jimtof2026','米沢工機JIMTOF2026共同展示','E3008／GAZIRU・SmartMore・安川電機等')
    source('FT18','ジェイテクト','https://toyoda.jtekt.co.jp/jimtof2026/','JIMTOF2026 特設サイト','Mill-Plan／ファインティーチレスツール／mJM画像キャプション')
    source('FT19','オークマ','https://www.okuma.co.jp/smart-factory/osp-suite/osp-ai.php','OSP-AI','AI機械診断／AI加工診断：異常レベルと工具退避')
    source('FT20','オークマ','https://www.okuma.co.jp/event/jimtof/2026/','JIMTOF2026 特設サイト','AIコーナー／知能化コーナー／ARMROID等')
    source('FT21','牧野フライス精機','https://www.makinoseiki.co.jp/exhibition/jimtof2026.html','JIMTOF2026 出展のご案内','SG10EX／monocam2：画像認識計測と自動補正')
    source('FT22','ナベル','https://www.bellows.co.jp/products/tm-robot','TM AI Cobot','内蔵ビジョン・AI／製品群')
    source('FT23','ヤマザキマザック','https://www.mazak.com/jp-ja/technology/productivity/','生産性向上技術','Smooth CAM Ai：3Dモデル・過去プログラムの学習')
    source('FT24','ヤマザキマザック','https://www.mazak.com/discover/jp-ja/jimtof2026/','JIMTOF2026 特設サイト','出展機・AI活用紹介。個別製品の展示範囲は要確認')
    source('FT25','ニデックグループ','https://www.nidec.com/jp/products/machine-tools/contents/machine-tool-jimtof2026/','JIMTOF2026 特設サイト','TAKISAWA TR20W：切りくず除去・参考出展')
    source('FT26','不二越','https://acs-l.jp/corp/nachi/jimtof26.html','JIMTOF2026出展（公式ニュースからリンク）','工作機械E3009／工具W1092：新機種は会場初公開')
    source('FT27','Siemens','https://www.siemens.com/en-us/company/insights/industrial-ai-changes-automation-engineers-work/','Industrial AI changes automation engineering','Eigen Engineering Agent：PLC・ECAD・プロジェクト生成／人のレビュー')

    def tags(x,defs):
        x['tags']={t:{'status':'—','reason':'今回の資料では当該機能を裏付けない。'} for t in tagnames}
        for tag,(state,reason) in defs.items():x['tags'][tag]={'status':state,'reason':reason}
    def update(cid,sourceids,defs=None,**kw):
        x=index[cid];x.update(kw);x['new_review']=True;x['depth']='企業・開発元の技術資料まで照合'
        for s in sourceids:
            if sources[s]['url'] not in [z['url'] for z in x['sources']]:x['sources'].append(sources[s])
        if defs is not None:tags(x,defs)
        return x
    def add(cid,company,item,sourceids,defs,**kw):
        rr=[r for r in rows if norm(r['company_name'])==norm(company)]
        x={'id':cid,'legacy_ids':[],'company':company,'listing_ids':[r['exhibitor_record_id'] for r in rr],'booths':list(dict.fromkeys(r['booth'] for r in rr)),
           'item':item,'task':'','need':'','input':'','method':'','output':'','human':'','limits':'','exhibit':'展示未確認','exhibit_note':'出展企業は一覧掲載。個別アイテムの展示は未確認。','stage':'企業の製品・事例紹介','sources':[],
           'depth':'企業・開発元の技術資料まで照合','new_review':True,'as_of':date,'baseline':'2024との同一機能・版の比較は未確認。','advance':'方式・適応範囲は個別確認','check':'','recommendation':'通常候補','recommend_reason':'','visit_group':''}
        items.append(x);index[cid]=x;return update(cid,sourceids,defs,**kw)

    update('FC004',['FT08'],exhibit='展示予定を明記',exhibit_note='10/16公式出展発表でCondition AgentをDX体験エリアの展示として明記。従来の「展示未確認」から更新。')
    update('FC006',['FT02','FT03'],{
      'AI':('機能記載','生成AIが加工情報を解釈し改善案・操作案を生成する。'),
      'フィジカルAI':('機能記載','生成AIとCNC・デジタルツインをMCPで接続し、検証・人承認を経て実機へ適用する構成。'),
      '自律化':('人承認付き','提案・検証はシステム側で実施するが、実機適用はオペレータの確認・承認を介する。'),
      '自動化':('機能記載','加工準備、シミュレーション、画面操作・設定等の処理を支援。')},
      input='加工情報・ノウハウ、自然言語の作業指示。',method='生成AIをMCPでCNC・デジタルツインへ接続。改善案を仮想検証し、人の承認後に実機適用する。',output='加工準備・条件提案・CNC設定の支援。',human='実機適用前にオペレータが確認・承認する。',limits='製品名だけで完全自律加工と判断しない。「自動復旧」の説明も原因推定・対策提案まで。',exhibit='展示予定を明記',exhibit_note='公式JIMTOF特設ページにフィジカルAI CNCを明記。個別デモ範囲は現地確認。',advance='生成AI・MCP・デジタルツイン検証／人承認あり',check='MCPで許可する読取り・書込み操作、仮想モデルの精度、検証不能時の停止、人承認の単位を確認。')
    update('FC005',['FT02'],exhibit='展示予定を明記',exhibit_note='オープンプラットフォームを使う生成AIロボット駆動事例を予告。以下の個別事例がすべて展示されるとは確認できない。')
    add('FT-F01','ファナック株式会社','AI溶接エージェント',['FT01','FT02'],{
      'AI':('機能記載','Gemini Enterpriseが図面を解釈し溶接条件・ロボット動作を生成。'),
      'フィジカルAI':('機能記載','図面から生成したプログラムをCRXの実溶接へ接続する。'),
      '自律化':('人承認付き','条件・動作を生成するが、人による採用・調整が可能。無監督の品質保証とは別。'),
      '自動化':('機能記載','プログラム準備からロボット溶接までを接続。')},
      task='図面解釈・溶接条件／動作生成',need='溶接の条件設定・教示に必要な経験と準備工数を減らす。',input='CRXタブレットTPのカメラで撮影した部品図面。',method='Google CloudのGemini Enterpriseを利用し、電流・電圧等の条件とロボット動作を生成。',output='ロボット溶接プログラムとCRXによるアーク溶接。',human='生成した条件・動作を利用でき、必要に応じ人が調整する。',limits='未知形状への一般化、溶接品質評価、治具・干渉の検証、自動再試行の範囲は未確認。',stage='9月の溶接展示会で実演発表／12月末出荷予定',exhibit='展示未確認',exhibit_note='国際ウエルディングショーの実演と発売予定は公式確認。JIMTOFの個別展示名としては未確認。',advance='生成AIによる図面→条件・動作→物理作業',check='JIMTOFで実演されるか。図面の適用形式、ロボット座標・治具設定、生成結果の安全検証と人の修正量を確認。')
    add('FT-F02','ファナック株式会社','AIエージェント・マスタレス認識によるキッティング',['FT04','FT02'],{
      'AI':('機能記載','自然言語の理解と物体名によるマスタレス認識を利用。'),
      'フィジカルAI':('機能記載','指示・注文票の解釈をロボットの部品・トレー搬送へ接続。'),
      '自律化':('限定機能','自然言語で作業ロジックを変更してキッティングを実行する事例。'),
      '自動化':('機能記載','撮影・OCR・搬送作業を連携。')},task='注文解釈・部品認識・キッティング',need='品種変更ごとの認識マスタと搬送ロジックの準備を減らす。',input='自然言語指示、注文票画像、ワーク画像。',method='AIエージェントと「ボルト」「ギヤ」等の名称によるマスタレス認識を接続する。',output='指示された部品・トレーの搬送とキッティング。',human='開始指示を人が与える。エラー時の確認・復帰は未公表。',limits='対象部品の広さ、取り違え・把持失敗・注文矛盾の扱いは未確認。',advance='意味指示による作業変更／認識マスタ準備の削減',check='事例の実演有無、未登録部品の認識、指示変更後の動作再構成と失敗復帰を確認。')
    add('FT-F03','ファナック株式会社','AI追従ねじ締め',['FT05','FT02'],{
      'AI':('機能記載','メーカーはAIによる3次元ワーク認識・追従と説明。'),
      'フィジカルAI':('機能記載','移動中のワークを認識してねじ締め位置・動作へ反映。'),
      '自律化':('限定機能','動く対象への追従を制御する。'),
      '自動化':('機能記載','動的な位置認識とねじ締めを接続。')},task='移動ワーク認識・追従組立',need='停止・固定が難しい部品のねじ締めを自動化する。',input='3次元的に動くワークの状態。センサ構成は未確認。',method='ねじ締め位置を自動認識し、動くワークへ追従して締め付ける。',output='移動中のワークへのねじ締め。',human='ワーク・ねじ・トルク等の事前設定と異常対応の詳細は未公開。',limits='学習モデル、視野遮蔽・速度変化・ねじ不良への対応は未確認。',advance='動的ワークへの認識・追従／モデル詳細は未公開',check='固定ワークの繰返しとの差、追従可能な変位・速度、ねじ締め失敗の判定と復帰を確認。')
    add('FT-F04','ファナック株式会社','VLA模倣学習・双腕柔軟物操作',['FT06','FT02'],{
      'AI':('機能記載','視覚・言語・動作を使うVLA基盤モデルへの模倣学習。'),
      'フィジカルAI':('機能記載','視覚と言語から行動を推論し、変形するTシャツの折り畳み動作を生成。'),
      '自律化':('限定機能','教示データから学習したモデルが作業中の行動を推論する。'),
      '自動化':('機能記載','双腕で柔軟物を操作する。')},task='模倣学習・変形物ハンドリング',need='形状が一定しない対象の作業を、手順固定ではなく実演学習で扱う。',input='遠隔操作時の動作・カメラ画像と、言語指示ラベル。',method='リーダ・フォロワ操作で収集したデータでVLA基盤モデルを模倣学習する。',output='視覚と言語に応じた双腕動作。',human='人が遠隔操作で学習データを収集し、言語ラベルを付ける。',limits='加工部品への移行、データ量・成功率・未知状態・再試行は未確認。',stage='公式の活用事例。製造現場の量産性能とは別。',advance='VLA・模倣学習と動作生成を明記',check='展示有無、使用モデル、実演データの収集量、初期姿勢を変えた試行・未学習品種・失敗復帰を確認。')

    add('FT-D01','ＤＭＧ森精機株式会社','my DMG MORI サービスエージェント',['FT07','FT08'],{
      'AI':('機能記載','Azure上の大規模言語モデルでマニュアルに基づく回答と問い合わせ内容を生成。'),
      '自動化':('機能記載','対話内容からサービスリクエストの必要情報を自動作成する。')},task='保全問診・マニュアル検索・修理依頼生成',need='夜間・休日の不具合初動と、保全知識・情報探索の不足を補う。',input='機番に応じた公開マニュアル、MRO知見を反映した問診、顧客の回答。',method='選択式を中心とした対話で症状を整理し、マニュアルに基づく対処案と問い合わせ文を生成する。',output='解決策・サービスリクエスト文案。',human='顧客が対処を試し、未解決ならリクエストを送信する。機械の自動復旧ではない。',limits='GENIAC診断データを使うアラーム自動診断は今後の計画。現在機能と混同しない。',exhibit='展示予定を明記',exhibit_note='10/19公式発表でJIMTOFデモを明記。',stage='10/19提供開始を発表',advance='メーカー文書・保全知見を接続した生成AI支援',check='機番別の回答根拠、曖昧な故障症状の問診、誤提案の検出、診断データとの今後の接続を確認。')
    add('FT-D02','ＤＭＧ森精機株式会社','GX Flex 工具・チャック爪・ワーク交換',['FT08'],{'自動化':('機能記載','ガントリローダでワーク搬送に加え工具・チャック爪を交換。')},task='多品種の段取り・ワーク供給',need='夜間の品種切替に残る工具・爪交換の手作業を減らす。',input='シャフト・フランジワーク、工具・チャック爪と段取り条件。',method='NTX 2500との組合せで複数の交換対象を扱う新開発ガントリローダ。',output='多品種加工の搬送・段取り替え。',human='段取り情報の登録、把持可否・干渉の確認と異常復帰は要確認。',limits='AI認識・自律段取り計画の説明はない。',exhibit='展示予定を明記',exhibit_note='10/16出展発表で新開発GX Flexを明記。',stage='世界初公開予定',advance='交換対象の拡張／AI使用は未確認',check='爪・工具交換の対象、段取り情報の生成方法、交換ミス検知と復帰を確認。')
    add('FT-D03','ＤＭＧ森精機株式会社','AMR 2000 工具搬送',['FT08'],{'自律化':('用途記載','自律走行ロボットによる工具搬送。経路・配車の判断方式は要確認。'),'自動化':('機能記載','加工機間の工具搬送を紹介。')},task='工具の工程間搬送',need='工具受渡しの人手と設備待ち時間を減らす。',input='工具と搬送要求。',method='AMR 2000を用いた工具搬送ソリューション。',output='工作機械間の工具受渡し。',human='搬送要求・工具IDの登録と停止後復帰の担当は未確認。',limits='AIモデル・群制御・自律再計画を確認できない。',exhibit='展示予定を明記',exhibit_note='10/16出展発表に記載。',check='工具管理との同期、優先順位・配車、閉塞時の再計画と受渡し安全を確認。')

    add('FT-M01','ModuleWorks GmbH','SmartRoughing／FeedControl',['FT09'],{'自動化':('機能記載','加工物理モデルから荒加工条件・NC区間の送りを最適化する。')},task='加工条件決定・送り最適化',need='熟練者の試し削り・条件調整と負荷変動を減らす。',input='機械・工具・材料、切削力・切屑負荷・主軸トルク等のモデル。',method='SmartRoughingは送り・回転・切込を、FeedControlは経路中の送りを加工物理で最適化。',output='加工条件・送りの最適化案。',human='モデル設定・適用限界と採用時の確認は要確認。',limits='学習AIの記載はない。オンライン実測の適応制御とも区別する。',exhibit='展示予定を明記',exhibit_note='10/15公式出展記事に記載。小間S4005は元一覧に基づく。',advance='加工物理モデルによる最適化／AIと区別',check='モデル同定に必要な実測、材料・工具の適用範囲、予測誤差、最適化後の検証を確認。')
    add('FT-M02','ModuleWorks GmbH','NGSP＋CAS＋MDES',['FT09'],{'自動化':('機能記載','機上プログラミング・機械照合・リアルタイム干渉回避を共通データで接続。')},task='機上プログラミング・段取り検証・干渉回避',need='NC到達後の手修正と段取り不一致による衝突リスクを減らす。',input='加工データ・デジタルツイン・カメラによる機械確認。',method='NGSP、ツイン、カメラ照合、CASをMDESのデータ表現で結ぶ。',output='プログラムから加工までの連続した確認・回避。',human='プログラム承認・不一致時の介入条件は未確認。',limits='個別モジュールのAI方式・回避指令と安全機能の範囲は未確認。',exhibit='展示予定を明記',exhibit_note='10/15出展記事で相談・紹介を案内。',advance='工程接続・機械照合／AI方式は未確認',check='カメラ照合の対象、実機モデルとのズレ、CASが止める・変更する制御、MDES接続先を確認。')
    add('FT-P01','株式会社Phoxter','StellaDeepVision Studio／StellaController2.0',['FT10'],{'AI':('機能記載','良品のみのモデル構築とAI・ルール検査の併用。'),'自動化':('機能記載','多視点の画像取得と外観判定を自動化。')},task='良品学習・難検査ワークの外観検査',need='不良サンプル不足と複雑鋳物・シールの目視検査を解消する。',input='良品画像、鋳造部品・オイルシール等の検査画像。',method='新しい数理モデルによる良品学習とルール検査を併用。6軸ロボット連携の多面検査を実演予定。',output='欠陥判定・多方向からの検査。',human='撮像・良品範囲・判定基準の準備と再学習条件は要確認。',limits='AI判定でロボットの視点・動作を変更するかは不明。固定撮像＋AI検査だけでは先端フィジカルAIと認定しない。',exhibit='展示予定を明記',exhibit_note='10/19公式出展記事、S4028。',stage='10月新発売の学習プラットフォームを展示予定',advance='良品学習／動作適応・新モデル詳細は要確認',check='必要画像のばらつき、不良流出・過検出、既存方式との差、検査NG時の再撮像・搬送変更を確認。')
    add('FT-P02','株式会社Phoxter','StellaDrive＋保守AIチャットボット',['FT11'],{'AI':('機能記載','オプションの生成AIチャットボットが復旧手順を回答。'),'自律化':('限定機能','SLAM・2Dコードに対応するAMR搬送。'),'自動化':('機能記載','設備・PLCと連携する搬送。')},task='自律搬送・トラブル初動支援',need='物流の人手とAMR停止時の専門家待ち時間を減らす。',input='LiDAR等の走行情報と人が入力するトラブル質問。',method='AMR走行と、復旧手順を答える生成AIオプションを組み合わせる。',output='搬送と人への保守手順提示。',human='復旧手順を受けて現場作業者が初期対応する。',limits='生成AIが経路やロボット動作を生成する説明はない。AI搭載AMRという名称からフィジカルAIへ自動分類しない。',advance='AIの担当は保守対話／自律走行とは機能分離',check='JIMTOF展示有無、走行制御とチャットボットの分離、停止・復帰の人の作業を確認。')
    add('FT-G01','株式会社GAZIRU','GAZIRU.eye 良品学習AI検査',['FT12','FT13','FT14'],{'AI':('機能記載','正常画像による教師なし異常検知。'),'自動化':('機能記載','画像から異常箇所・良否を出力し、API経由で検査システムへ接続。')},task='異常検知・検査立上げ',need='多品種少量で集めにくい不良画像と検査員不足を補う。',input='正常画像、運用時の検査画像。',method='良品学習後に異常スコア・ヒートマップを出力。複数エンジンの選択・並列実行に対応。',output='画像の良否・異常箇所とAPI応答。',human='事前検証でモデル・パラメータ・閾値を選ぶ。ライン制御は個別のシステム構築。',limits='異常スコアの可視化は因果的な説明の保証ではない。汚れ・照明・品種変動への性能は要検証。',exhibit='展示予定を明記',exhibit_note='GAZIRU公式出展記事でE3008とGAZIRU.eyeを明記。',advance='少数正常画像でのモデル構築／個体履歴連携',check='新品種での立上げ、NGの定義・閾値、API後の排出制御、加工条件との対応付けを確認。')
    add('FT-G02','株式会社GAZIRU','GAZIRU.z V5 タグレス個体識別',['FT12','FT14'],{'自動化':('機能記載','表面の微細紋様を撮像・照合し、個体と製造・検査履歴を結び付ける。')},task='個体識別・工程データ紐付け',need='刻印・タグが難しい部品でも、加工条件と検査結果を個体単位で追う。',input='表面の微細紋様画像と登録画像データベース。',method='個体固有パターンを照合し位置・角度・倍率のずれを補正する。',output='個体識別番号と履歴連携。',human='適切な撮像条件と工程を経ても識別できる表面の選定が必要。',limits='学習AIの具体方式は未確認。表面変化・洗浄・加工後の再識別性は適用試験が必要。',exhibit='展示予定を明記',exhibit_note='E3008でV5紹介と公式に記載。',advance='加工・品質データの個体対応基盤／AI方式は未確認',check='加工で表面が変わる際の追跡、工程間の照明差、誤一致率とID再発行の条件を確認。')
    add('FT-SM01','株式会社スマートモア','AIデスクトップ外観検査',['FT17'],{'AI':('呼称・用途記載','共同出展者の公式発表でAI外観検査を案内。'),'自動化':('機能記載','卓上の外観検査を装置化する提案。')},task='卓上外観検査',need='小ロットの目視検査を省力化する。',input='対象部品の外観画像。撮像構成は未確認。',method='AIを用いた卓上検査を共同展示者が予告。学習法・モデルは未確認。',output='外観判定。判定項目・排出制御は未確認。',human='品種登録・学習・撮像条件の準備量は未確認。',limits='展示予定の一次根拠は共同出展者の発表。型式・不良検出性能は未確認。',exhibit='展示予定を明記',exhibit_note='米沢工機の共同展示案内、E3008。',check='型式、良品のみ／不良学習の別、判定基準設定、品種追加時の準備工数を確認。')
    add('FT-C01','ＣＫＤ株式会社','FSH／FSB／QREC・組立自動化',['FT15'],{'自動化':('構成要素','倣い把持・柔軟支持・段取り調整等で搬送・組立の自動化を構成。')},task='柔軟把持・段取り・組立',need='部品形状・姿勢への対応と、組立の段取り工数を減らす。',input='把持対象ワーク・形状と組立条件。',method='3D吸着ハンド・柔軟支持・クイック調整・ロボット回転機器等を組み合わせる。',output='搬送、Oリング・小物組立、ねじ締め等の工程構成。',human='選定・段取り・設定条件は個別設計。',limits='機械的な倣いを学習AIとは数えない。製品別の実演・デジタル紹介の区分を確認する。',exhibit='展示予定を明記',exhibit_note='9/23公式イベントページ、W4064。',advance='機構による柔軟対応／AI方式の説明なし',check='対応形状・姿勢、設計変更なしで使える範囲、空圧・I/O制御、教示削減量を確認。')
    add('FT-A01','autonomIQ','simplymill／AI CAM',['FT16'],{'AI':('機能記載','形状認識・工具選定・経路生成にAIを使うと公式説明。'),'自動化':('機能記載','3D CADから加工戦略・NCを生成。')},task='CADからの工程設計・NC生成',need='単品・少量部品のCAMプログラミングと見積準備を減らす。',input='3D CAD、機械の工具ライブラリ、材料・公差。',method='形状特徴を識別し工具・加工戦略・経路を決め、NCを生成すると公式説明。',output='加工計画とNCコード。',human='公式フローに確認・エクスポート工程がある。実行承認と安全検証の詳細は未確認。',limits='適用機種・ポスト処理・加工可否判定の実証範囲は未確認。自動実機切削までの接続を確認できないためフィジカルAIとは未分類。',exhibit='展示未確認',exhibit_note='元一覧にE1061で出展。simplymillのJIMTOF個別展示内容は未確認。',advance='AI CAMの新興候補／対応範囲は未検証',check='JIMTOF展示機能、使うモデル・物理計算、工具DB、対応軸数・加工機、検証・NC生成の制約を確認。')
    add('FT-J01','株式会社ジェイテクト','Mill-Plan',['FT18'],{'自動化':('機能記載','工具選定・姿勢・切削条件を含む加工工程の自動設計を紹介。')},task='工程設計・工具／条件選定',need='熟練者に依存する加工準備を省力化する。',input='加工対象・機械・工具等。入力仕様の詳細は要確認。',method='工具・姿勢・条件を含む工程設計を自動化する。',output='加工工程案。',human='採用・修正・検証の手順は未確認。',limits='AIモデル利用を明示する資料は今回確認できない。',exhibit='展示予定を明記',exhibit_note='公式JIMTOF特設に掲載。',check='CAD入力からの自動範囲、ルール／AIの別、工具DBと条件の同定、修正・検証工数を確認。')
    add('FT-J02','株式会社ジェイテクト','ファインティーチレスツール',['FT18'],{'自律化':('限定機能','デジタルと実機の誤差を測り、オフライン動作プログラムを補正。'),'自動化':('機能記載','ロボットの現場合わせを省力化。')},task='ロボット校正・オフライン教示補正',need='シミュレーションから実機への移行で生じる現場の微調整を減らす。',input='デジタルモデルと実機の誤差計測。',method='測定した誤差に基づき動作プログラムを補正する。',output='実機に合わせたロボット動作。',human='計測準備・誤差モデル設定・実機適用の確認範囲は未公開。',limits='AI学習モデルや未知作業の生成を示す説明ではない。',exhibit='展示予定を明記',exhibit_note='公式JIMTOF特設に掲載。',advance='計測に基づく教示補正／AIとは区別',check='補正する座標・機械誤差、計測時間・再校正条件、複雑工具・複数設備への適用を確認。')
    add('FT-J03','株式会社ジェイテクト','mJM AI相談室365／Remote Care',['FT18'],{'AI':('呼称・用途記載','公式画像説明でAIによるアラーム初期対応提案を案内。')},task='設備アラームの初期診断支援',need='設備トラブル発生時の確認・相談待ちを減らす。',input='設備異常・アラーム情報。接続・入力仕様は未確認。',method='AIで初期対応を提案し、人のコンタクトセンターと接続する構成。',output='対処案と遠隔支援。',human='提案後の処置・遠隔支援は人が担う構成。',limits='確認根拠は特設サイトの画像キャプション。モデル・自動復旧の範囲は未公開。',exhibit='展示予定を明記',exhibit_note='公式JIMTOF特設ページに紹介。',check='取得アラーム・ログ、回答の根拠、人への引継ぎ、サービス提供段階を確認。')
    add('FT-O01','オークマ株式会社','OSP-AI 機械診断／加工診断',['FT19','FT20'],{'AI':('機能記載','制御情報から機械・ドリル加工の異常を診断。'),'フィジカルAI':('機能記載','加工診断の異常レベルに応じ工具退避へ接続する限定的な例。'),'自律化':('限定機能','異常閾値を超えた際に機械が工具を退避。'),'自動化':('機能記載','異常監視・保護動作を接続。')},task='機械自己診断・加工異常保護',need='突発工具損傷と機械停止によるワーク不良・ダウンタイムを減らす。',input='主軸・送り軸・加工の制御情報。',method='AIが異常・異常箇所を診断。加工異常レベルが一定値を超えると工具を退避する。',output='診断結果・自動退避。',human='診断開始、閾値設定、退避後の点検・復帰は要確認。',limits='一部特別仕様。今回の特設はAIコーナーを予告するが、同機能・版の個別実演は未確認。',exhibit='展示未確認',exhibit_note='AIコーナーの予告と製品資料は確認。同版・同機能の実演を明記した資料は未確認。',advance='AI診断→保護動作／既存製品技術と区別',check='診断用運転と加工中監視の違い、ドリル以外の適用、退避指令・復帰条件、新版の追加能力を確認。')
    update('AC209',['FT21'],exhibit='展示予定を明記',exhibit_note='SG10EX＋monocam2の画像認識測定・自動補正を公式に実演予告。',input='内蔵ビジョンで取得するエンドミル側面形状。',method='monocam2で工具を機内測定し、研削へ自動補正を返す。',output='工具形状の測定値と研削補正。',human='測定基準・補正限界・再測定の設定は要確認。',advance='機内光学計測の閉ループ化／AI方式の説明なし')
    update('AC159',['FT22'],input='内蔵ビジョン画像と教示・設定条件。',method='ビジョン・AIを内蔵するTM AI Cobot。展示タスクでの認識・動作変更範囲は未確認。',output='協働ロボットの作業。個別対象動作は要確認。',limits='AI Cobotという製品呼称だけで未知物・未知作業への一般化を認めない。')
    add('FT-Z01','ヤマザキマザック株式会社','Smooth CAM Ai',['FT23','FT24'],{'AI':('機能記載','過去に作成した加工プログラムの加工パターンを学習。'),'自動化':('機能記載','3DモデルからMAZATROLプログラムを生成。')},task='3D形状からの加工プログラム生成',need='熟練者の加工パターンを再利用してプログラミング工数を減らす。',input='3Dモデル、過去の加工プログラム。',method='形状に適した加工パターンを学習させ、プログラムを生成する。',output='MAZATROLプログラム。',human='学習元プログラムの選定と修正・採用・加工前確認の手順は要確認。',limits='2026特設のAI活用紹介は確認したが、同機能・版の個別展示は未確認。ABEJAとの将来の工程設計AI開発とは区別する。',exhibit='展示未確認',exhibit_note='企業公式製品資料。個別の搭載展示機・版は未確認。',advance='加工パターンの再利用・学習／新規性は別確認',check='誰のどの加工判断を学習するか、過去プログラムの必要量、材料・工具変更時の適用と人の修正を確認。')
    update('FC049',['FT25'],exhibit='参考出展予定',exhibit_note='公式特設でTR20Wによる切粉の認識・判断・除去を参考出品と明記。',check='未知の絡まり・絡まり方の変化への対応、認識センサ・学習法、接触力・除去完了判定、失敗後の再試行を確認。')
    add('FT-SI01','シーメンス株式会社','Eigen Engineering Agent',['FT27'],{'AI':('機能記載','TIA Portalのプロジェクト文脈に基づきPLC・HMI・構成を生成するAIエージェント。'),'自動化':('機能記載','PLCコード・テスト生成、コンパイルエラー修正、ECADデータからの構成を自動処理。')},task='PLC・HMI・装置プロジェクト生成',need='制御設計・電気設計間の転記と、PLCプログラミング・検証の手作業を減らす。',input='TIA Portalプロジェクト、機械の自然言語説明、XML・AML等の電気設計情報。',method='プロジェクト内のデバイス・ロジック等を利用し、PLCコード・試験や標準に沿う構成を生成・修正する。',output='PLC／HMIコード、テスト、デバイス構成・TIAプロジェクト。',human='エンジニアが生成結果をレビューする。実機への適用・権限管理は別に確認が必要。',limits='コードの生成・検証と実機の自律運転は異なる。個別アイテムのJIMTOF展示は未確認。',advance='プロジェクト文脈を使う制御開発エージェント',check='JIMTOF展示有無、生成・テスト・自己修正の範囲、既存設計規約、安全制御のレビュー・承認を確認。')
    # Fill comparison records with their own input/output; do not inherit a different product's fields.
    for cid,fields in {
      'RPT001':dict(input='NC、工具・材料・加工形状と切削モデル。',method='Production ModuleでNC区間の切削負荷を解析し送りを最適化。AdvantEdgeの刃先FEMとは分ける。',output='最適化NCと加工負荷の解析結果。',human='材料・工具モデルの設定と最適化後NCの検証・採用は人が行う〈分析〉。'),
      'RPT002':dict(input='加工中の実測主軸負荷。',output='負荷変化に応じた送り速度の自動調整。',limits='負荷限界・停止復帰・被削材ばらつきの許容範囲は未確認。'),
      'RPT003':dict(input='NC旋盤の稼働信号。信号種類・検出周期の詳細は要確認。',output='刃具破損・異常兆候の検知。',limits='検知後の停止指令と独自アルゴリズムの内容は未確認。'),
      'RPT004':dict(input='前加工後の歯車測定値。',output='歯合わせ・前加工状態の計測。',limits='計測による条件最適化は開発中。自律最適化の完成品とは扱わない。'),
      'SUB002':dict(input='工具の設計・加工条件。',output='工具加工プログラム。',limits='生成の自動範囲・AI使用・人の検証量は未確認。'),
      'SUB003':dict(input='CAD形状と加工・測定条件。',output='加工・測定プログラム。',limits='生成AI機能と、従来のルールによるプログラム生成を区別する必要がある。'),
    }.items():index[cid].update(fields)
    x=index['RPT006']
    x['tags']['AI']={'status':'機能記載','reason':'温度等と加工後の測定結果から熱変位補正を学習・最適化する。'}
    x['tags']['フィジカルAI']={'status':'機能記載','reason':'学習した補正を加工機の位置精度制御へ接続する限定例。未知作業の生成とは別。'}
    x['advance']='学習型熱変位補正／既存製品技術・展示搭載未確認'
    for cid in ['FC052','FC064']:
        index[cid]['exhibit']='展示未確認'
        index[cid]['exhibit_note']='2026の企業出展は確認。個別AI機能は2024等の比較情報を含み、同版・同機能の展示は未確認。'
    for cid,reason in {
      'FC004':'診断専用NC動作によるデータ取得とクラウド診断を自動処理する。診断開始・修理は人の関与と分ける。',
      'FC058':'音声・履歴から保全記録の整形と分析レポート生成を省力化する。機械修理の実行とは別。',
      'FC062':'引合・図面・過去見積から見積書のたたき台を生成する。人が確認・修正する。',
      'FC064':'AIによる加工異常・工具摩耗等の検知を自動処理する比較情報。2026同一機能の展示は未確認。',
    }.items():index[cid]['tags']['自動化']={'status':'機能記載','reason':reason}

    # Practical visit recommendations: purpose and exhibit uncertainty remain visible per item.
    recs={
      'FC006':('優先訪問','S2001：生成AI・MCP・ツイン検証・人承認を具体的に比較できる。','生成AI・フィジカルAI'),
      'FT-F01':('事前確認','先端的な図面→動作生成の比較基準。JIMTOFで見られるかを事前・現地で確認。','生成AI・フィジカルAI'),
      'FT-F02':('事前確認','品種・指示変更への対応を確かめる有力事例。個別展示は未確認。','生成AI・フィジカルAI'),
      'FT-F04':('事前確認','VLA・模倣学習と動作生成の明確な参照例。個別展示は未確認。','生成AI・フィジカルAI'),
      'FC049':('優先訪問','E3013：無人加工の阻害要因である切粉処理を、認識・判断・除去まで扱う参考展示。','生成AI・フィジカルAI'),
      'AC085':('比較訪問','E7074：工具形状の認識・AI補正を物理加工へ返す範囲を比較する。','加工・計測の閉ループ'),
      'FC051':('比較訪問','S1013：自動段取り替えのフィジカルAI呼称について、交換対象・認識・動作変更を確かめる。','生成AI・フィジカルAI'),
      'FT-D01':('優先訪問','E8005：提供開始済み・デモ予定の保全AI。データ基盤の将来構想と現在機能を比較できる。','大手メーカーのAI実装'),
      'FC004':('優先訪問','E8005：診断専用NC動作・設計製造情報・クラウドAIの組合せを確認する。','大手メーカーのAI実装'),
      'FT-Z01':('比較訪問','E1001：熟練加工パターンの学習と工程準備。搭載展示の有無を先に確認する。','大手メーカーのAI実装'),
      'FC010':('比較訪問','E1001：既存の搬送自動化とAIによる準備・判断機能を分けて確認する。','段取り・工程接続'),
      'FT-O01':('比較訪問','E3028：AI診断が通知で終わる機能と工具退避へつながる機能を比較する。','大手メーカーのAI実装'),
      'FC064':('比較訪問','E1036：CNCのAI支援と実機動作の接続、新版の担当タスクを確認する。','大手メーカーのAI実装'),
      'FC018':('優先訪問','E2013：部品特徴・PMI・過去ジョブを使うAI工程設計。CAMAssistと比較する。','工程設計・プログラム生成'),
      'FC020':('優先訪問','E2002：形状・工具・材種から工程案を生成し、人が検証する実務範囲を比較する。','工程設計・プログラム生成'),
      'AC131':('比較訪問','S1016：SolidCAM運用に組み込むAI生成。Mastercam側との差を確認する。','工程設計・プログラム生成'),
      'FT-A01':('事前確認','E1061：既存大手CAMと異なる新興AI CAMの候補。展示内容・対応機種を先に確認。','工程設計・プログラム生成'),
      'FT-J01':('優先訪問','E8003：工具・姿勢・条件を含む工程自動設計。AI方式か従来最適化かを確認する。','工程設計・プログラム生成'),
      'FT-M01':('優先訪問','S4005：加工物理モデルとAIの役割分担を考える比較先。モデル校正用データも確認する。','加工モデル・データ基盤'),
      'FT-M02':('比較訪問','S4005：工程間データの連続性と実機段取り照合・干渉回避の接続を確認する。','加工モデル・データ基盤'),
      'FC011':('優先訪問','W4012：生成した制御コード案を人がどう検証・適用するかを確認する。','制御開発・エージェント接続'),
      'FT-SI01':('事前確認','E3006：BeckhoffのCoAgentと比較する制御開発AI。個別展示の有無を先に確認する。','制御開発・エージェント接続'),
      'FC024':('比較訪問','S3048：OPC UA情報モデルとMCP接続。AI本体と接続基盤の役割を確認する。','制御開発・エージェント接続'),
      'AC273':('比較訪問','S3057：形状に加えて関節・物理属性を学習用データへ変換する範囲を確認する。','加工モデル・データ基盤'),
      'FT-P01':('優先訪問','S4028：良品学習と6軸多面検査を具体的に比較。固定撮像と動作適応の境界を確認する。','検査AI・品質データ'),
      'FT-G01':('優先訪問','E3008：良品学習とAPI連携を、Phoxter・HACARUSと比較する。','検査AI・品質データ'),
      'FT-G02':('比較訪問','E3008：加工条件・検査データを現物個体へ結び付ける基盤を確認する。','検査AI・品質データ'),
      'FC036':('比較訪問','S3027：少量良品学習と運用中の再学習・誤判定修正を比較する。','検査AI・品質データ'),
      'FC033':('優先訪問','E7089：計測結果が工具オフセット・機械変数へ返る範囲と補正限界を確認する。','加工・計測の閉ループ'),
      'AC209':('比較訪問','E7090：工具研削の機内画像計測と自動補正。AI方式との違いを確認する。','加工・計測の閉ループ'),
      'FC046':('比較訪問','E1024：加工・パレット・ソフト・保守を接続するライン構成を確認する。','段取り・工程接続'),
      'FC047':('比較訪問','E2011：多品種パレット加工とプロジェクト単位の加工データ管理を確認する。','段取り・工程接続'),
      'FC048':('比較訪問','S1001：移設後のマーカ読取りによる位置補正。学習AIと幾何補正を比較する。','段取り・工程接続'),
      'FT-D02':('比較訪問','E8005：搬送に加え、工具・爪交換を含む段取り自動化を確認する。','段取り・工程接続'),
    }
    for cid,(priority,reason,group) in recs.items():
        if cid in index:
            x=index[cid];x['recommendation']=priority;x['recommend_reason']=reason;x['visit_group']=group
    # Never introduce a booth from editorial text: the booth fields always come from the master.
    for x in items:
        if x['recommend_reason']:
            # Older narrative booth numbers can differ; use verified master booth fields only.
            x['recommend_reason']=re.sub(r'^[ESW][A-Z]?\d{3,4}：','',x['recommend_reason'])
        x['check']=x.get('check') or '入力・判断・出力、人の準備と異常復帰、適用条件を確認する。'
