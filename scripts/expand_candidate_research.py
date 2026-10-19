"""Extend the reviewed topic index to the complete, frozen 2026 candidate set."""
import hashlib,json,re,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
norm=lambda s:re.sub(r'\s+','',unicodedata.normalize('NFKC',s)).casefold()
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))

# Numbers refer to the 298 source records outside the original 47 catalogue records.
# Assignments were reviewed from the source-located descriptions; no keyword score.
MEMBERS={
 'C01':[19,51,85,159,273],
 'C02':[],
 'C03':[95,131,136,194,195,273],
 'C04':[7,51,79,85,107,178,204,210,225,252,271],
 'C05':[18,24,31,47,53,55,61,74,76,78,82,95,98,99,101,104,111,117,119,121,131,133,148,172,176,190,194,195,206,215,220,228,240,258,273,279,282,284,286,295,297],
 'C06':[3,7,14,19,25,26,37,38,39,41,42,54,60,62,63,70,71,74,95,98,100,103,104,106,109,112,115,124,129,131,138,148,153,154,156,166,172,175,176,180,183,185,186,190,195,204,206,207,210,211,215,216,217,220,224,225,226,227,231,232,234,235,236,240,244,245,246,250,252,256,265,271,273,279,282,287,288,295,297],
 'C07':[1,2,5,6,9,10,11,12,13,15,16,17,21,22,23,24,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,54,56,57,58,59,60,63,64,65,66,67,68,69,72,73,75,76,77,81,83,85,86,88,89,90,91,93,94,95,96,97,98,100,101,102,103,105,106,107,108,110,111,112,113,114,115,116,117,118,119,120,122,123,125,126,127,129,130,131,132,133,134,137,138,139,140,141,142,143,145,146,148,149,150,151,152,153,154,155,156,157,158,159,160,162,163,164,165,167,168,169,170,171,172,173,174,175,177,178,179,181,182,183,184,185,186,187,188,189,190,191,192,193,194,197,198,199,201,203,204,205,208,209,210,212,213,214,216,217,218,219,220,221,222,223,224,227,229,230,232,233,234,235,236,238,241,242,243,244,245,246,247,248,249,250,251,252,254,256,257,260,262,264,265,268,269,271,272,273,275,276,277,278,279,280,282,284,287,288,289,291,292,293,295,297,298],
 'C08':[39,90,146,186,245,265,273,287],
 'C09':[2,7,8,14,62,65,71,72,79,104,145,175,182,185,208,210,222,227,240,250,271,273,286,288],
}
EXCLUDED={
 20:'配管・流量最適化の説明。AI・DX・自動運用の具体機能は今回の記述では確認できない。',
 35:'CAMは内視鏡の型番。CAD/CAMやAI展示を示す一致ではない。',
 44:'DXはキャビネットの型番。透明窓による見える化をデジタルDXと扱わない。',
 80:'社内のCAD/CAM設備と受託精密加工の説明。DXソフト展示ではない。',
 84:'汎用旋盤の条件調整・教育用途。最適化の語だけでAI等に分類しない。',
 87:'AIロボット等はベアリングの供給先分野。AI作業の展示ではない。',
 92:'CAMはカム式自動旋盤の型番。CAD/CAMの展示ではない。',
 128:'省人化は切削油剤の訴求。自動化システム・データ機能の説明なし。',
 135:'加工会社の検索・連携サービス。AI・DX・自動化の具体展示は記述不足。',
 144:'砥石と研削相談の説明。自動化相談の語だけで自動システムと扱わない。',
 147:'砥石・チャック寸法の最適化等の機械仕様。AI・DXの最適化ではない。',
 161:'見積は加工受託の受付窓口。AI見積システムではない。',
 196:'エンコーダの光学測定技術改良。最適化の語だけでAI・DXに分類しない。',
 200:'切削工具・加工法の最適化提案。個別のAI・DX・自動化装置は未特定。',
 202:'ロボットマシニングは切削油剤の採用用途。ロボットシステム展示ではない。',
 237:'MESは微細工具測定器の製品名。製造実行システムと扱わない。',
 239:'手動クイックチェンジの省力化。自動爪交換・自律判断の記述なし。',
 253:'自社のCAD/CAM利用と工具製造設備を紹介。CAD/CAM製品の展示ではない。',
 255:'ロボットは軸受の供給先用途。認識・制御・自動化機能の実装説明なし。',
 259:'ロボット減速機部品の加工用途。ロボットによる作業とは区別。',
 261:'AIはセミナーの翻訳対応。製造のAI展示とは分ける。',
 263:'コーティング性能の最適化。データ駆動・AI方式の説明なし。',
 266:'AM造形・設計支援の総論。自動化やデータ連携の具体機能は未特定。',
 267:'製品最適化と社内設備の紹介。AI・DX応用の具体記述なし。',
 270:'重研削・省力化とサンプル展示。自動システムの具体記述なし。',
 274:'ロボット関節はブローチの加工対象。AIロボットの展示ではない。',
 281:'バイス等の標準・特注製造。候補抽出語から自動機能を確認できない。',
 283:'工具の寿命・切粉処理の改善。認識・データ連携・自動動作は未特定。',
 285:'自動化装置は砥石の加工対象分野。自動化システムの展示ではない。',
 290:'測定顕微鏡の校正・補正。自動補正制御やAI工具診断とは別。',
 294:'AIサーバーはステンレス材料の供給先用途。製造AIの実装ではない。',
 296:'社名のROBOTとロボット向け軸受。ロボット作業の展示と扱わない。',
}
PERIPHERAL={2,13,14,17,27,30,33,37,40,50,57,64,65,66,67,72,75,81,83,105,108,113,122,132,137,141,145,157,158,165,168,169,173,182,185,187,192,201,203,205,208,222,227,233,241,242,243,249,250,254,262,269,275,278,293}

# Deep comparisons: read both complete catalogue descriptions; dates here are
# exhibition years, not claims about invention or first commercial availability.
DEEP={
39:('TM-2800：AMR・ロボット・加工機の統合','2024はRK510のストッカー・2D位置補正・ハンド交換と加工機接続。','2026は高層ストッカーTM-2800を起点にAMR・ロボット・加工機を統合制御する提案。','セル内供給から工程間統合へ対象拡大を記載。再計画・未知例外対応は未確認。','搬送対象・構成の追加記載','投入・スケジューリング後の機器指示','既存設備の接続工数、品種切替、AMR遅延・加工機停止時の再計画と人への引継ぎは。'),
51:('マグネットピンセット：AI・2Dカメラ・協働ロボット','2024にも磁気ホルダ・2Dカメラ・協働ロボットによる小径ネジのバラ積みピッキング。','2026は同種構成にAIを明記し、小径ネジ・小部品のピッキングを説明。','ピッキング自体は継続。AI追加の実機機能・対応品種・性能差を確認する。','2024から継続・AIの記載を追加','2D画像・磁気制御・ロボットで小部品を拾う','AIが検出・把持点・重なり・再試行のどこを担うか。2024と同一ワークで比較できるか。'),
85:('GH5：工具の3D画像認識・AI補正ホーニング','2024はGM5の自動工具交換・研削とGri Star Honing2。','2026はGH5で機内3D画像解析・AI自動補正、測定・加工・検査の一体化を説明。','工具供給・加工の自動化に、画像を使う補正を追加記載。精度・条件差は未確認。','担当タスクの追加記載','工具を立体認識しホーニングを補正','何を計測し何の軸・条件をどこまで補正するか。教師データ、過補正抑止、測定不確かさは。'),
98:('Digital Thread：工作機械ツイン・工程内品質保証','2024もNX CAD/CAM/CMM、SINUMERIK ONE、Mcenter、CNC＋ロボット加工を展示予定。','2026はHeller Toknツイン、Renishaw Equator品質保証、ヒューマノイド特別展示を具体記載。','デジタル連携は既存。工程内品質保証との接続とヒューマノイドの担当タスクを確認。','2024から継続・構成を具体化','設計から加工・品質のデジタルスレッド','加工・計測のどの情報が往復するか。Equatorの結果で何を変えるか。ヒューマノイドは何の作業を行うか。'),
131:('CAM Assist for SolidCAM／SolidShop','2024はSolidCAM、iMachining、SolidProbeと実機・プローブ連携。','2026は形状からのAI CAM支援、生成AIセミナー、SolidShopによる設備接続を追加掲載。','計測・CAM支援に、AIプログラミングと稼働・生産管理を追加記載。','担当タスクの追加記載','形状→CAMプログラミング支援／設備の稼働情報','対応加工・機種・工具制約、人の修正とNC検証の範囲を他CAM AIと同一部品で比較する。'),
136:('切削加工条件カリキュレーター','同一名称の2024詳細なし。法人同一性を含む別名照合は未実施。','スマホで工具・被削材・加工方法を選び、AI最適化した切削条件の目安を出して共有する。','2024差分は比較不能。CAM内の工程生成と、条件目安の提示の違いを比較する。','2024個別比較不能','工具・被削材・加工方法→条件の目安','学習・算定根拠、適用材・工具範囲、機械剛性や突出しの扱い、推奨条件の検証方法は。'),
146:('3D形状認識・教示不要の面取り／皿もみ','同一名称の2024詳細なし。名称変更・他ブースの照合は未完了。','レーザースキャンで未教示の不定形ワークを認識し、加工軌道を生成して面取り・皿もみ等を行う予定。','2024差分は比較不能。AI使用を断定せず、認識から軌道生成・実行までを比較対象にする。','2024個別比較不能','レーザースキャン→形状認識→軌道生成→加工','未登録形状の許容範囲、取り残し・反り・誤認識、干渉検証、刃具摩耗と加工後検査の扱いは。'),
159:('TM Robot S-Type：ビジョン・AI内蔵協働ロボット','2024もTMロボットを掲載。主説明はカバー・クーラント等。','2026はS-Typeの内蔵カメラ・AIソフトを明記。EPSON LS8の供給・仕分け用途も掲載。','ロボット出展は継続。AIの具体タスク・機能差は未確定。','2024から継続・AIの記載を具体化','内蔵ビジョン・AIを備える協働ロボット','会場タスクとモデル・学習・教示・座標補正の担当、部品や照明が変わった際の再設定は。'),
186:('AMRによる切り屑自動回収','2024は高精度ろ過、スマートチップコンベヤ、複数機からのポンプバック集中処理。','2026はAMR切り屑回収、自由なレイアウトのコンベヤ、ろ過を実演・模型で紹介。','集中コンベヤ／配管とAMR回収を比較できる。AMRでの運搬対象・受渡しを確認。','搬送対象・構成の追加記載','切り屑の回収をAMRで結ぶ','容器交換・満杯検知・回収順序・切屑こぼれ・通路混雑と停止復帰は。実機と模型の範囲を確認。'),
195:('ズメーン：図面・関連文書管理とAI','同一名称の2024詳細なし。','図面を検索し、見積・検査書等を紐づけ管理。AIで登録から運用を支援との説明。','2024差分は比較不能。検索・関連付け・AI支援の担当範囲を具体化する。','2024個別比較不能','図面検索・見積／検査書の関連付け','AIがOCR・類似検索・登録のどこを助けるか。図面改訂、品番、権限、誤関連の修正は。'),
204:('OTRS+AI：作業動画の自動分節','2024にもOTRS10、OTRS+AI、Mobile OTRSを掲載。','2026は同系統の動画分析・自動分節を継続し、VPS NEXTアイトラッキングを追加記載。','動画分節AIを2026新登場とはしない。視線情報と作業分析の接続・差分を確認。','2024から継続・構成を追加記載','作業動画を分節し改善分析を助ける','分節境界の修正工数、作業者差・工具差、視線データと工程指標の結び付けは。'),
214:('Smart Terrace Adv／爪・CAPTO工具の交換','2024もSmart Terrace、爪交換、ケレ交換、測定ハンド、チャック本体交換の参考出品。','2026は既設機向けAdvを追加し、爪・CAPTO工具・ケレ交換等を具体展示。','段取り自動化自体は既存。後付け条件とCAPTO交換、構成・価格の差を確認。','2024から継続・構成を追加記載','既設機のワーク・爪・工具・ケレを交換','既設機の改造点、交換後の確認、品種データ・爪段取りの人手、段取り全体の残作業は。'),
225:('プライマリドクタサービス：稼働中データのAI診断','2024に容易に脱着できる機器で稼働中の重要部位データを取得し、AI診断・レポート・追加点検を説明。','2026も同名AIリモート診断を掲載。','方式は継続。新たな診断対象・対応機・分析内容は今回記述だけでは比較不能。','2024から継続','設備を止めずデータ取得・AI診断・点検提案','対象故障・必要信号・計測時間、診断専用NCとの違い、誤警報、報告後の保全判断と採用実績は。'),
234:('ALFRED：クーラント濃度・pH監視','同一名称の2024詳細なし。','濃度・pHをリアルタイム監視し、会場ではコントローラーと管理画面を展示予定。','2024差分は比較不能。監視と自動補給・濃度制御を区別する。','2024個別比較不能','クーラント状態を継続取得し可視化','センサ校正・汚れ・液種差・異常判定、補給装置連携の有無、記録と管理工数の実績は。'),
245:('Road to Automation：工具研削の自律性向上提案','同一名称の2024詳細なし。','研削高度化、接続、情報・教育・運用支援を含む6段階の自動化を提案。','2024差分は比較不能。自律性を高める具体製品・判断対象は記述不足。','2024個別比較不能','研削・接続・支援を段階的に提案','どの製品が測定・条件変更・再試行を担うか。通常自動化から自律性を高める具体機能は。'),
265:('boxcon：工具貸出・返却・在庫管理','2024もIoT・ロードセル・LED・ロック等とソフトによる工具在庫管理を説明。','2026はリアルタイム追跡・認証・履歴と自律製造対応を強調。','IoT工具管理は継続。自律製造向けという訴求を、自律判断機能の追加と混同しない。','2024から継続','工具貸出・返却・在庫を追跡','重量変化と品番・使用者の照合、誤返却、在庫補充の判断者、他システム連携と2024からの実装差は。'),
273:('TRINIX：CADから物理シミュレーション用データ生成','同一名称の2024詳細なし。','テキスト・画像・CADからNURBS形状、物理属性・関節・衝突メッシュを生成し、シミュレーション検証・自己修正を説明。','2024差分は比較不能。ロボット動作そのものと、学習・検証用データ生成の基盤を区別。','2024個別比較不能','生成→物理属性付与→検証・修正→USD等へ出力','推定質量・摩擦・関節の正解と検証基準、自己修正の停止条件、実機との誤差、VLAデータの内容は。'),
287:('協働ロボット・自律移動ロボットとツーリング','同一名称の2024詳細なし。日本語表記・旧名称との同一法人照合は未完了。','ロータリーマガジン付き協働ロボット、自律移動ロボット、ツーリングを掲載。','2024差分は比較不能。AMR・工具供給の接続と自律判断範囲は要確認。','2024個別比較不能','ロボット・AMR・ツーリングによる供給','自律走行以外の判断・設備連携、位置ずれ、品種切替・停止後の再開を確認。'),
295:('WinTool：工具情報と現物・工程資源の連携','2024も工具ライブラリ・CAM／NC・在庫・段取り・収納／プリセッター連携を説明。','2026は現物情報と生産資源・BOPへの対応、一貫性を強調。','工具情報の接続自体は継続。新しい接続先・同期・整合性の実装差を確認。','2024から継続','工具定義・在庫・現場ファイルをCAM等へ展開','工具組立・品番・所在・寿命情報のどこが正本か。CAM・実機・収納間の同期、改訂・差異検出は。'),
}

# Task, customer problem (analyst), deployment, and source-described inputs.
DETAILS={
 39:('設備間の供給・生産指示','ストッカー・搬送・加工機を別々に運用する負担','TM-2800を起点とするAMR・ロボット・加工機の統合','人による投入・スケジューリング情報。機器状態の取得範囲は未確認'),
 51:('小径ネジ・小部品のバラ積みピッキング','小さな部品を取り分けて供給する作業','2Dカメラ・磁気把持と協働ロボットのピッキングセル','2D画像と小径ネジ・小部品。AIの学習入力は未確認'),
 85:('工具の形状認識・ホーニング補正','工具の認識・補正と測定加工の分断','GH5の機内3D画像認識・ホーニング工程','工具の機内3D画像。補正対象の特徴量は要確認'),
 98:('設計・加工・工程内品質保証の連携','設計・加工・計測情報が分断する負担','CAD/CAM/CMM、CNC、工作機械ツインと工程内計測','設計・加工・計測データ。製品間の具体的データ項目は要確認'),
 131:('CAMプログラミング支援・設備情報接続','CAMの手作業と現場情報の分断','SolidCAM上のCAM Assist、設備接続のSolidShop','加工形状、設備情報。AIの具体的制約入力は要確認'),
 136:('切削条件の目安を算出・共有','工具・材種に合う条件を調べる負担','スマートフォンで利用する条件カリキュレーター','工具・被削材・加工方法の選択'),
 146:('不定形ワークの面取り・皿もみ・バリ取り','形状や穴位置ごとの図面準備・ロボット教示','ロボット加工セル。東京エンジニアリングE7073内','レーザースキャンによる不定形ワークの3D形状'),
 159:('協働ロボットのビジョン・AI利用（作業は要確認）','品種変化に対応するロボットの認識・設定負担','TM Robot S-Typeのカメラ・AIソフト。EPSON LS8は別製品','内蔵カメラ画像。AIの判定対象・学習手順は未確認'),
 186:('AMRによる切り屑回収','固定コンベヤ・配管による配置制約と切り屑回収','切り屑回収AMR・コンベヤ・ろ過。実演と模型を併用','切り屑。回収要求・満杯検知等の入力方式は未確認'),
 195:('図面検索・見積検査書の関連付け','図面と周辺文書の検索・登録の負担','図面管理ソフトウェア「ズメーン」','図面と見積・検査書等。AI処理の入力・出力は要確認'),
 204:('作業動画の自動分節・分析','作業を区切り分析する手作業','OTRS+AIの作業動画分析。VPS NEXTは視線計測の別構成','作業動画。視線データとの接続範囲は要確認'),
 214:('ワーク・爪・工具・ケレの交換','既設機の段取り替えと人手の残作業','Smart Terrace Adv等の工作機械向け段取りシステム','ワーク・爪・CAPTO工具・ケレ。品種情報・交換検証方式は要確認'),
 225:('稼働中の設備データ取得・AI診断','診断のための停止と保全原因調査の負担','重要部位の計測機器・AI分析・診断レポート／追加点検','稼働中の重要部位データ。信号種・計測条件は要確認'),
 234:('クーラントの濃度・pH監視','切削液の状態把握と記録の負担','ALFREDのコントローラーと管理画面','クーラントの濃度・pHデータ'),
 245:('工具研削の段階的な自動化支援','研削と接続・教育・運用支援の分断','Road to Automationの6段階の提案。個別実装先は未特定','個別機能の入力・判断対象は記述不足'),
 265:('工具の貸出・返却・在庫の追跡','工具の所在・使用者・在庫の照合負担','IoTセンサ等とboxcon管理ソフトウェア','工具の使用・返却・在庫情報。2024はロードセル等の構成を説明'),
 273:('ロボット学習・検証用3Dデータ生成','物理シミュレーション用データの作成・検証負担','TRINIXの生成・変換・シミュレーション検証ソフト','テキスト・画像・既存CAD。物理属性・関節等を付与'),
 287:('ロボット・AMRによる供給（具体作業は要確認）','加工設備への供給とツーリングの接続負担','ロータリーマガジン付き協働ロボット・AMR・ツーリング','搬送物・品種データ・位置検出方式は今回の記述では未特定'),
 295:('工具データと現物・工程資源の整合','工具情報・CAM・在庫・段取り間の不整合','WinToolとCAM/NC・収納・プリセッター等の連携','工具定義・在庫・工程資源情報。同期項目・頻度は要確認'),
}

def expand_candidates(cards,evidence,category_rows,category_defs):
 candidate=[r for r in read('data/research/overview_v0/candidate_universe.json') if r['year']==2026]
 used={e.get('source_record_id') for e in evidence.values() if e['year']==2026}
 remaining=[r for r in candidate if r['record_id'] not in used]
 assert len(candidate)==345 and len(remaining)==298
 old=read('data/exhibitor_details_2024.json');old_by={}
 for d in old:old_by.setdefault(norm(d['company_name']),[]).append(d)
 cats={d['category_id']:d for d in category_defs};audit=[]
 existing_cards=list(cards)
 for r in candidate:
  if r['record_id'] not in used:continue
  ids=[c['card_id'] for c in existing_cards if any(evidence[e].get('source_record_id')==r['record_id'] for e in c['evidence_ids'])]
  audit.append(dict(record_id=r['record_id'],company=r['company_name'],normalized_name=r['normalized_name'],booth=r['booth'],disposition='既存の重点カードで分類済み',reason='既存69カードの対象掲載',card_ids=ids,url=r['detail_url']))
 for number,r in enumerate(remaining,1):
  category_ids=[cat for cat,ids in MEMBERS.items() if number in ids]
  if number in EXCLUDED:
   assert not category_ids,(number,category_ids)
  status='カテゴリー付与（周辺要素）' if number in PERIPHERAL else 'カテゴリー付与（一次整理）' if category_ids else '分類保留（具体機能不足）'
  reason=EXCLUDED.get(number,'原典の該当記述に基づく一次分類。個別製品の方式・年度差分の精査とは区別。' if category_ids else '具体的な自動化・データ利用の範囲を追加確認する。')
  if number in EXCLUDED:status='対象外（語の一致・用途等）'
  cid=f'AC{number:03}'
  audit.append(dict(record_id=r['record_id'],company=r['company_name'],normalized_name=r['normalized_name'],booth=r['booth'],disposition=status,reason=reason,card_ids=[cid] if category_ids else [],url=r['detail_url']))
  if not category_ids:continue
  matches=old_by.get(r['normalized_name'],[])
  ds=[(2026,r)]+[(2024,d) for d in matches]
  es=[];locs=[]
  for year,d in ds:
   rid=d.get('record_id',d.get('exhibitor_record_id'))
   eid='EEX-'+rid;es.append(eid)
   cache=d.get('cache_path','');url=d['detail_url']
   evidence[eid]=dict(evidence_id=eid,publisher=d.get('company_name',r['company_name']),year=year,title=f'JIMTOF{year}公式出展説明：{d["company_name"]} ({d["booth"]})',url=url,locator='出展紹介・主な出展物。追加カードの原典抜粋で検索',checked_date='2026-10-16',published_date='未記載',evidence_type='公式掲載の出展者記述・メーカー主張',exhibition_certainty='2026展示予定・現地未確認' if year==2026 else '2024当時の説明・実演事後確認ではない',source_record_id=rid,cache_path=cache,source_excerpt='原典キャッシュと年度別CSVに本文を保存')
   locs.append(dict(evidence_id=eid,url=url,locator=evidence[eid]['locator'],local_cache=cache))
  text=r['exhibition_content']+'\n'+r['main_exhibits']
  sentences=[s.strip() for s in re.split(r'(?<=[。!?])|\n',text) if s.strip()]
  keyword=r'AI|自律|エージェント|ロボット|自動|IoT|DX|CAM|CAD|工程管理|生産管理|監視|デジタル|補正|ツイン|simulation|automation'
  relevant=[s for s in sentences if re.search(keyword,s,re.I)]
  excerpt=' / '.join(relevant or sentences)[:220]
  title=re.split(r'\n',r['main_exhibits'].strip())[0].strip('・●■◆ >')[:75] if r['main_exhibits'].strip() else excerpt[:75]
  before=' / '.join(d['exhibition_introduction']+' '+d['main_exhibits'] for d in matches)
  deep=DEEP.get(number)
  before_text=deep[1] if deep else '2024原典抜粋：'+re.sub(r'\s+',' ',before)[:260] if matches else '同一正規化名称の2024詳細なし。新規出展・技術不存在とは判断しない。'
  after_text=deep[2] if deep else '2026原典抜粋：'+excerpt
  interpretation=deep[3] if deep else '原典記述の対照。個別機能の追加・性能差・初登場年は未判定。'
  diff=deep[4] if deep else '両年原典あり・機能差未判定' if matches else '2024個別比較不能'
  question=deep[6] if deep else 'どの作業を自動化・支援するか、入力と判断・操作の範囲、適用条件と人の残作業、2024からの機能差、採用・受注・効果の実測を確認する。'
  c=dict(card_id=cid,review_id='EXP-'+hashlib.sha1(r['normalized_name'].encode()).hexdigest()[:10],company=r['company_name'],item=deep[0] if deep else title,task_id='TASK99',phase='追加候補（出展説明単位）',task='出展説明の関連用途（個別タスクの分解は未完了）',customer_need='原典の課題記述を参照。定量的な顧客課題の追加確認が必要。',need_classification='追加候補の一次整理。重点比較対象は別に精査',deployment='出展説明に記載。実装位置の個別精査はカードの方式・未確認欄を参照',robot_form='原典の出展機器・ソフトウェアを参照',system_configuration=deep[5] if deep else '原典抜粋：'+excerpt,input='個別入力の追加確認が必要',mechanism='原典抜粋：'+excerpt,output=deep[5] if deep else excerpt,human_boundary='承認・例外対応・停止・復帰の境界は未確認',baseline_2024=before_text,observation_2026=after_text,delta_type=diff,delta_interpretation=interpretation,roles=['未特定'],product_stage='2026展示予定。既存製品・参考出展・構想等は原典で個別確認',exhibition_status='2026公式カタログ掲載・現地未確認',evidence_ids=es,booths_2026=[r['booth']],unresolved=question,adoption_and_market='採用・受注・市場規模未確認',checked_date='2026-10-16',source_locations=locs,company_need_context='',review_depth='両年全文を意味内容で比較した重点追加例' if deep else '出展説明の関連箇所に基づく一次分類',candidate_record_id=r['record_id'],categories=[])
  if number==273:c['exhibition_status']='2026のライブデモ・ロボット学習用データ展示を予告。実機ロボットの作業実演とは未確認'
  if number==186:c['exhibition_status']='2026は実演・模型を併用。AMR回収の実機／模型の範囲は要確認'
  if number==234:c['exhibition_status']='2026はコントローラーと管理画面の展示予定'
  if deep:
   c['review_depth']='2024・2026の原典全文を重点比較' if matches else '2026の原典全文を重点整理・2024同名原典なし'
   c['task'],c['customer_need'],c['deployment'],c['input']=DETAILS[number]
   c['mechanism']=deep[2]
  if number in [146,273]:
   wid='EEX-WTED' if number==146 else 'EEX-WNDOT'
   url='https://www.inrevium.com/news-event/event/p7331/' if number==146 else 'https://ndotlight.com/newsroom/ndotlight-proposes-a-new-3d-data-standard-for-the-physical-ai-era-with-trinix'
   note='東京エンジニアリングのブースE7073内。教示不要の面取り・皿もみ・バリ取りとビジョンローダー／アンローダーを予告。' if number==146 else '2026-05-13の企業公式説明。既存CAD等を関節・物理属性付きSimReadyデータへ変換する。実機ロボットの作業実演を示す情報ではない。'
   evidence[wid]=dict(evidence_id=wid,publisher=r['company_name'],year=2026,title='企業公式の展示告知' if number==146 else 'TRINIX：Physical AI向け3Dデータの企業公式説明',url=url,locator='展示会概要・出展製品／2026年5月13日の製品説明',checked_date='2026-10-16',published_date='未記載' if number==146 else '2026-05-13',evidence_type='企業公式説明・メーカー主張',exhibition_certainty='2026展示予定' if number==146 else '製品の方式説明。JIMTOFの実演範囲とは区別',source_excerpt=note,cache_path='',retrieval_note='webで確認し観察要旨を保存。ウェブ全文キャッシュではない。')
   c['evidence_ids'].append(wid);c['source_locations'].append(dict(evidence_id=wid,url=url,locator=evidence[wid]['locator']))
   if number==146:c['exhibition_status']='東京エンジニアリングE7073内で展示予定（企業公式告知で確認）'
  cards.append(c)
  for cat in category_ids:
   scope='周辺要素・実装部品。システム全体のAI／自動動作の確認ではない' if number in PERIPHERAL else '出展説明に基づく一次分類。方式・実装権限・提供段階は個別確認'
   if cat=='C01':scope='フィジカルAI関連の応用／基盤。メーカー呼称と内容分類を分ける。' if number in [51,85,159] else 'Physical AIの訴求／学習基盤。具体タスク・適用範囲はカード参照'
   if cat=='C08':scope={39:'工程間の統合制御。自律再計画・未知例外復帰は未確認',90:'AMRの限定走行。パレタイズとの協調判断は未確認',146:'形状認識から軌道生成・加工。AI利用・未知形状の限界は未確認',186:'AMRによる切り屑回収。容器受渡し・例外処理は未確認',245:'メーカーの自律性向上提案。個別判断・製品範囲未特定',265:'自律製造向け工具管理基盤。自律的な補充判断は未確認',273:'データ生成・検証の自己修正というメーカー説明。実機自律性とは別',287:'自律移動ロボットの掲載。走行以外の判断は未確認'}[number]
   basis='内容から分類（調査者・一次整理）'
   if cat=='C01' and number in [19,273]:basis='メーカー明示（Physical AI／公式製品説明）'
   er=[e for e in es if evidence[e]['year']==2026]
   row=dict(category_id=cat,category=cats[cat]['category'],subcategory='周辺部品・機構' if number in PERIPHERAL else deep[0] if deep else title,company=c['company'],item=c['item'],booths_2026=c['booths_2026'],classification_basis=basis,relation_scope=scope,classification_reason='2026の具体記述：'+excerpt,card_id=cid,exhibition_status=c['exhibition_status'],product_stage=c['product_stage'],output=c['output'],evidence_ids=er,source_urls=[r['detail_url']],checked_date='2026-10-16')
   category_rows.append(row)
   c['categories'].append({k:row[k] for k in ['category_id','category','subcategory','classification_basis','relation_scope']})
 category_rows.sort(key=lambda r:(r['category_id'],r['company'],r['card_id']))
 for d in category_defs:
  rs=[r for r in category_rows if r['category_id']==d['category_id']]
  d['item_count']=len(rs);d['company_count']=len({r['company'] for r in rs})
 assert len(audit)==345 and len({r['normalized_name'] for r in audit})==342
 return audit
