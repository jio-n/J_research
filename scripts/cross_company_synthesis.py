"""Source-linked analytical views of the 33 priority cards; no new acquisition."""
import html,re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
FUNCTIONS=['基盤・入力整備','判定・表示','提案・生成','ソフト実行','実機動作']

# These are comparison families, not claims about a shared algorithm or product integration.
METHODS=[
 ('M01','対話・コード／業務生成','自然言語・設計文脈・業務履歴 → 回答、コード、見積案。Operationsはコマンド実行も説明。','要求・スケッチ・原価等を人が用意。EPLANは人が意思決定、匠フォースは確認・修正・承認。CoAgentは専門家が制御権を保持。','生成案の採否と実機への適用は別の仕事。EPLANの自動操作は将来構想、CoAgentは製品発表・投入時期要問合せ。','PLC支援は2023に存在。2026はI/O・HMI・運用対象を具体化。匠フォースのエージェントは2026/7発表、2024展示比較は不能。',['FC011','FC012','FC013','FC017','FC062']),
 ('M02','履歴を使う工程／寿命予測','ProPlanAIは過去ジョブから工程予測。アナライザーは摩耗履歴・経験知から寿命と交換時期を提案。','履歴と対象条件の整合を確認。最終NC採否・工具交換の承認者は公開資料で未確定。','工程予測と寿命予測は対象・学習データが異なる。いずれも提案から実機実行までの一体自動化は確認できない。','Hexagonは2025.2→2026.1で旋削等の商用範囲を拡張。寿命推定研究は2023に存在し、2026は製品・用途を具体化。',['FC018','FC040']),
 ('M03','物理・加工ルール型CAM生成','形状・工具／ホルダ・材種・保持・機械・方向等 → 加工性評価、編集可能な工程・経路案。','人が制約を入力し、案を編集・並べ替え・検証してポスト処理。加工開始は別工程。','履歴学習型と入力依存性が違う。CloudNCは顧客のMastercamデータで学習しないと明記。3軸・3+2軸ミル中心、通信が必要。','Mastercam対応は2024/7/25に提供発表済み。SolidCAMは2025 SP4対応を説明。2026の初発明とはしない。',['AC131','FC020']),
 ('M04','画像・時系列の認識／診断','良品との差、工具画像、設備電流・振動、図面OCR、時系列予測など。入力と教師・基準が製品ごとに異なる。','HACARUSは人が良否を追加ラベル、Fact BaseはOCR結果を人が確認・補正。停止・出荷・交換判断は多くが未記載。','検知・表示・予測と、機械停止・排出・修理は区別。Kowaは別体プロセッサが必要。SOFIXの予測と搬送実行の直結は未確認。','Moriの摩耗判定・Muratec診断は2024から継続。ZEROは2025/7に追加学習を搭載し販売開始。2026初登場と一括しない。',['FC036','FC039','AC225','FC063','AC195','FC030']),
 ('M05','認識から動作・加工補正','切粉状況→除去、小部品画像→ピック、刃先測定→ホーニング補正、3D形状→加工軌道。別資料には車輪型ロボットの物流試験。','GH5は人が目標幅・角度を設定。動作許可・失敗検知・再試行・停止復帰の権限は他の例を含め未公開部分が多い。','AIの担当が明確な例と、AI明示のみ・学習方式未確認の例を併置。TAKISAWAは参考出品、HMNDはドイツの別実証でJIMTOF同一機体未確認。','TR-20Wは2024搬入出→2026切粉除去を追加記載。カネテックの2D＋磁気ピックは既存でAI記載追加。GH5の資料は2025/10、2026初登場とは断定しない。',['FC049','AC051','AC085','AC146','AC098']),
 ('M06','幾何・機械モデルでの検証','実行NC・工具・治具・制御ロジックを用いるVericut、仮想SINUMERIK ONEによるToknの仮想加工・訓練。','人がモデル・実機・工具・NCの版を合わせ、結果を受けて修正・採否を決める。','AI生成案と独立した比較対象。シミュレーションがあるだけで実機の正しさやAI搭載を保証しない。','Toknの事例はCompletion 2024。Vericutの既存検証と2026固有の機能追加を分ける。',['FC021','AC098']),
 ('M07','AI実装のデータ／モデル基盤','ML Creatorの学習・評価／ONNX、OPC UA情報モデルとMCP連携計画、TRINIXのCAD・物理属性／SimReady生成。','データ・目的・情報モデル・物理条件を用意し、出力の正しさと公開権限を確認。','モデル・データ生成は作業実行とは別層。MCPは提供計画、SimReadyは実機精度未確認。3方式の相互接続は未確認。','ML CreatorのONNX等は2024資料に存在。OPC UAは既存でAI接続計画を追加。TRINIXの2024同名原典はなく差分不能。',['FC014','FC024','AC273']),
 ('M08','ルール・寸法・機構による自動化','在庫ルール、上位指令、寸法パラメータ、AMR搬送、ナットランナー・ばね等の機構。各方式の学習AIは未確認。','WinToolは購買要求を管理者承認後ERPへ送信。FNSは人が投入・スケジューリング。MMKは人が寸法入力、イマオは治具・指を設計。','多くを自動実行してもAI自律判断の証拠にはならない。AMRの配車最適化、統合制御の再計画は未確認。','MMKのCAPTO交換・イマオ同系列治具は2024にも存在。2026は後付け・構成・供給方法や搬送対象の具体化を比較。Fleeterミニ工場は2025にも告知。',['AC295','AC039','AC214','AC186','FC042','FC043','FC030']),
 ('M09','人の遠隔対応を支援','通常自動運転で障害物停止 → 人がX-Area Remoteに切替え、映像を見て回避。','運行担当者が遠隔介入。2026/7の屋外実証はセーフティドライバー搭乗。','AI支援型という呼称と、AI自身が障害を回避・復帰することは分ける。通信断・再開許可は未確認。','2024同名展示比較は不能。2026/7実証で屋外物流の人による例外対応を具体確認。',['FC031']),
 ('M10','判断方式未公開の助言・監視','ToolDiscoveryは選択3項目から条件の目安、ALFREDは濃度・pHのリアルタイム監視。','条件を採用する判断、警報後の補給・液交換や校正は公開資料では未特定。','条件助言はAI明示・算定内訳不明。ALFREDのAI判断・自動補給は未確認。2社とも補足技術資料未確認。','2社とも2024同名原典がなく個別比較不能。新規技術・自律制御の証拠として使わない。',['AC136','AC234']),
]
METHOD_EVIDENCE={
 'M01':['EDP-03','EAT-N03','EAT-N04','EAT-N05','EAT-N06','EDP-05'],
 'M02':['EOV-W02','EOV-W08','EOV-V024-2024-1','EOV-V024-2026-1'],
 'M03':['EDP-07','EDP-08','EDP-09','EDP-10'],
 'M04':['EDP-14','EDP-15','EDP-12','EDP-13','EDP-33','EDP-11','EDP-21','EDP-22','EOV-V024-2024-1','EEX-EXH-2024-b0a94c1cd407ea8a'],
 'M05':['EAT-N01','EAT-N02','EDP-01','EDP-02','EEX-WTED','EDP-17','EEX-EXH-2026-30b70a74241de123'],
 'M06':['EDP-16','EDP-20'],
 'M07':['EDP-04','EOV-W01','EDP-06','EEX-WNDOT'],
 'M08':['EDP-18','EDP-19','EDP-25','EDP-26','EDP-27','EDP-28','EDP-29','EDP-30','EDP-31','EDP-32','EDP-22','EDP-23'],
 'M09':['EDP-24'],
 'M10':['EEX-EXH-2026-d383a51fea03ae6e','EEX-EXH-2026-1fb607fd5307c2fa'],
}

# card, family, function column, short company, task, status. Two cards have deliberately separated roles.
POSITIONS=[
 ('FC011','M01',2,'Beckhoff','要求→PLCコード案','製品発表'),('FC012','M01',2,'Beckhoff','要求・スケッチ→I/O・HMI案','製品発表'),('FC013','M01',3,'Beckhoff','データ診断・TwinCATコマンド','製品発表・権限未公開'),('FC017','M01',2,'EPLAN','回答・手順支援','自動操作は将来'),('FC062','M01',2,'匠技研工業','原価算定・見積書案','人が確認・修正・承認'),
 ('FC018','M02',2,'Hexagon','過去ジョブ→工程予測','旋削等へ商用範囲拡張'),('FC040','M02',2,'モリマシナリー','摩耗履歴→寿命・交換提案','自動交換は未確認'),
 ('AC131','M03',2,'タクテックス','CAM Assist／SolidCAM','人が編集・検証'),('FC020','M03',2,'JBM','CAM Assist／Mastercam','人が編集・検証'),
 ('FC036','M04',1,'HACARUS','良品学習＋追加ラベル→判定','人が追加学習'),('FC039','M04',1,'モリマシナリー','工具画像→欠け・摩耗判定','交換指令は未確認'),('AC225','M04',1,'ムラテックCCS','電流・振動→設備診断','レポート・点検提案'),('FC063','M04',1,'興和','RW＋別体解析→異常通知','自動停止は未確認'),('AC195','M04',1,'Fact Base','図面OCR→登録・検索','人が読取確認・補正'),('FC030','M04',2,'SOFIX／AI Forecast','時系列・画像の予測','Fleeterへの直結未確認'),
 ('FC049','M05',4,'TAKISAWA','TR-20W：主軸の切粉除去','参考出品'),('AC051','M05',4,'カネテック','磁気＋2D：小径ネジピック','AIの担当未公開'),('AC085','M05',4,'サイバーRC','GH5：測定→ホーニング補正','人が目標幅・角度設定'),('AC146','M05',4,'TED／E7073内','3D認識→面取り・皿もみ','学習AIの使用未確認'),('AC098','M05',4,'Siemens／HMND','車輪型：トートの取出・搬送','ドイツ別実証・展示機未同定'),
 ('FC021','M06',1,'CGTech','実行NC→干渉・残削り検証','AI搭載は未確認'),('AC098','M06',1,'Siemens／Tokn','仮想CNC加工・訓練','2024事例・HMNDと別'),
 ('FC014','M07',0,'Beckhoff','データ→学習・評価／ONNX','作業用途は別設定'),('FC024','M07',0,'たけびし','OPC UA情報モデル×MCP','Adapterは提供計画'),('AC273','M07',0,'NdotLight','CAD・物理属性→SimReady','実機の作業実行と別層'),
 ('AC295','M08',3,'WinTool','在庫ルール→購買要求／ERP','管理者承認後に転送'),('AC039','M08',3,'FNS','TM-2800：機器の統合指示','AI再計画は未確認'),('FC030','M08',3,'SOFIX／Fleeter','上位命令→AMR・アーム・PLC','予測AIの直結未確認'),('AC214','M08',4,'松本機械工業','寸法入力→段取り交換','学習AIは未確認'),('AC186','M08',4,'白山機工','AMRで切り屑回収','実演・模型／配車AI不明'),('FC042','M08',4,'イマオ','ナットランナーでクランプ','機構・AIは未確認'),('FC043','M08',4,'イマオ','ばね・ピンで指交換','機構・AIは未確認'),
 ('FC031','M09',4,'パナソニック','障害物停止→人が遠隔回避','動作主体は人'),('AC136','M10',2,'ToolDiscovery','工具・材種・方法→条件目安','AI算定内訳未公開'),('AC234','M10',1,'ユシロ','ALFRED：濃度・pH監視','AI・自動補給は未確認'),
]

YEARS=[
 ('Y01','開発支援の対象を具体化','2023のTwinCAT ChatはPLCコード作成等。ML Creatorは2024資料で学習・評価・ONNX。','CoAgentでI/O・HMI・運用診断とコマンドを説明。製品発表段階。','AI開発支援の初登場ではない。2024展示の同条件比較、販売版と操作権限は未確認。',['FC011','FC012','FC013','FC014'],['EDP-03','EDP-04','EAT-N03','EAT-N04','EAT-N05']),
 ('Y02','CAMは学習源と加工範囲で分岐','CAM Assist／Mastercamは2024/7/25に提供発表。SolidCAMの2024展示はiMachining等。','SolidCAM 2025 SP4対応。ProPlanAIは2025.2導入説明→2026.1で旋削・複合・スイス型を商用拡張。','ProPlanAIの2024同名資料なし。国内供給・会場版は要確認。履歴予測と物理・加工ルール型を分ける。',['FC018','FC020','AC131'],['EDP-10','EDP-09','EDP-07','EDP-08','EOV-W02']),
 ('Y03','既存の判定に人の調整・予測を追加','Moriの摩耗判定・Muratecの診断は2024に存在。寿命推定研究は2023発表。','ZEROは2025/7/9販売開始、良否ラベルの追加学習。2026はMoriアナライザーの寿命・交換提案を具体掲載。','診断→自動修理／交換とは確認できない。追加学習の更新採否・実運用性能は別途確認。',['FC036','FC039','FC040','AC225'],['EDP-14','EDP-15','EDP-12','EOV-W08','EDP-13']),
 ('Y04','物理作業と導入構成を拡張','TR-20Wは搬入出。磁気＋2Dピック、MMKのCAPTO交換、イマオ同系列治具は2024に存在。','TR-20Wは切粉除去を参考出品。MMKはAdv後付け・単体販売、FNSは工程間統合、白山はAMR回収を説明。','既存機構をAI新技術としない。カネテックのAI担当、再計画・失敗復帰、実演範囲は未確認。',['FC049','AC051','AC214','FC042','AC039','AC186'],['EAT-N01','EAT-N02','EDP-01','EDP-27','EDP-28','EDP-32','EDP-25','EDP-29']),
 ('Y05','接続基盤にAI利用の層を追加','2024のたけびしはOPC UA情報モデル・多ベンダー接続。','2026はOPC UA×MCP Adapterの提供計画。NdotLightはCAD・物理属性からSimReadyを説明。','MCP計画を実装済みとしない。TRINIXは2024個別比較不能。データ生成→実機作業の一体実装も未確認。',['FC024','AC273'],['EDP-06','EEX-WNDOT']),
 ('Y06','別の実証と比較不能を残す','Toknの仮想CNC訓練はCompletion 2024。Panasonic等は2024同名資料不足。','SiemensのHMND物流試験は2026/4ドイツの別実証。Panasonicは2026/7に人の遠隔回避を具体確認。','ToknからHMNDへの進化・接続は未確認。海外事例とJIMTOF展示機を同一視しない。人の介入を自律復帰としない。',['AC098','FC031','FC063','AC136','AC234','AC195','AC146','FC062'],['EDP-16','EDP-17','EDP-24','EDP-33','EDP-05','EEX-WTED']),
]

ISSUES=[
 ('I01','提案を採用可能な結果へ変える検証','CAMは生成後に人が編集・検証。PLCは専門家が制御権を保持。匠フォースは人が確認・修正・承認。','工具・保持・機械・版・業務前提が変わる時の整合確認が共通する作業〈分析〉。自動承認が必要と決めつけない。','CAMの既存加工性評価やNCシミュレーションはすでに存在。各社の未検出制約と修正負担は未測定。',['FC018','FC020','AC131','FC021','FC011','FC062'],['EOV-W02','EDP-09','EDP-08','EDP-20','EAT-N05','EDP-05']),
 ('I02','データの意味と操作権限をつなぐ','OPC UAは値・状態・属性・関係を構造化。CoAgentはコマンド実行を説明。WinToolは管理者承認後にERP送信。Panasonicは停止後に人が遠隔回避。','読取り・提案・書込み・実機動作を分ける権限と、状態／版の整合が連携時の論点〈分析〉。','人の承認を備える製品はある。許可コマンド・二重実行・停止復帰の公開情報不足は、製品に機能がない証拠ではない。',['FC024','FC013','AC295','FC062','FC031'],['EDP-06','EAT-N04','EAT-N05','EDP-18','EDP-05','EDP-24']),
 ('I03','動作の成否と例外時の引継ぎ','切粉除去・ピック・面取り・ホーニングで認識から動作へ進む。Panasonicは障害物停止後に人が遠隔回避。','認識の不確かさ、作業完了、再試行限界、人への引継ぎ、再開条件をタスクごとに定める必要性〈研究仮説〉。','GH5の目標設定、Panasonicの人の介入は確認済み。その他の失敗処理は公開資料不足で、現場不具合を確認したわけではない。',['FC049','AC051','AC085','AC146','FC031','AC098'],['EAT-N01','EDP-01','EDP-02','EEX-WTED','EDP-24','EDP-17']),
 ('I04','条件変化に応じた判定の更新と採否','HACARUSは見逃し／過検出に人が追加ラベル。Moriは工具画像、Muratecは新品基準と信号、Kowaは耐環境撮像と別体AI。','対象・照明・工具・材種・機械状態の変化ごとに、誤判定と人の修正工数を分けて評価する論点〈分析〉。','ZEROの追加学習は既存機能。自動更新・版の差戻し・条件別の性能保証は今回の公開資料では未確認。',['FC036','FC039','FC040','AC225','FC063'],['EDP-14','EDP-15','EDP-12','EOV-W08','EDP-13','EDP-33']),
 ('I05','生成・仮想モデルと実機条件を照合','TRINIXは物理属性・関節等を生成。HMND事例はIsaac Sim/Labで学習。Vericutは実行NCと機械モデルで検証。','見た目の形状だけでなく質量・摩擦・関節・制御設定等の由来と誤差を管理する論点〈分析〉。','別企業の実装済み接続とは確認していない。各社の属性検証や実機誤差評価の実装範囲は追加確認が必要。',['AC273','AC098','FC021'],['EEX-WNDOT','EDP-17','EDP-20']),
]

THEMES=[
 ('T01','生成CAMの制約整合検証と修正フィードバック','I01','生成時間を短縮しても、段取り条件との照合や修正が残る可能性。','部品・工具／ホルダ・保持・機械・版を揃え、工程案→実行NCの検証結果と人の修正理由を対応付ける。顧客データを外部モデル学習へ送る設計は前提にしない。','3軸・3+2軸の限定部品群。手作業CAM／既存CAM Assist／履歴予測を同条件で比較し、未登録工具や保持条件変更を含める。','承認可能NCまでの総時間、修正工数、制約違反と見逃し、条件変更時の再作業。','既存CAM・検証製品だけで同等に解決できるなら連携・運用改善を優先。生成速度だけ改善し総工数が減らなければ採用しない。',['FC018','FC020','AC131','FC021'],['EOV-W02','EDP-09','EDP-10','EDP-07','EDP-08','EDP-20']),
 ('T02','設備エージェントの権限付き実行と停止復帰','I02','診断や提案を設備・業務システムの操作に移す際、許可と状態整合を保つ必要がある。','型付きコマンド、実行前条件、読書き許可、プレビュー・人の承認、実行ID・履歴、失敗時の停止／引継ぎを組み合わせる。差戻せない操作は事前検証と停止手順を設ける。','模擬PLCと業務データの限定命令。現行手動操作／承認付きワークフローと比較し、通信断・重複指令・古い状態を注入。','未許可実行の発生、二重実行、承認負担、失敗の検出率、停止からの復帰時間。','既存製品の権限・例外制御が要件を満たせば実装の再発明を避ける。必要な実行APIが公開されない場合は読取り・提案支援に範囲を絞る。',['FC024','FC013','AC295','FC062','FC031'],['EDP-06','EAT-N04','EAT-N05','EDP-18','EDP-05','EDP-24']),
 ('T03','切粉除去・部品ピックの失敗検知と限定再試行','I03','未知の切粉状態・複数個把持等で、作業完了や人への引継ぎを判断する負担が残る可能性。','画像と動作／接触の情報で成功・不確実・失敗を分け、作業ごとの力・接触制約内で限定再試行。上限で停止し、人が確認して再開する。','切粉除去と小部品ピックを別実験にする。現行固定手順／形状認識型を比較し、絡まり・空振り・二個取り等を段階的に変える。','完了判定の見逃し／誤完了、介入回数、復帰時間、連続運転時間。平均成功率だけで判断しない。','メーカーの既存機能と適用条件を先に確認。失敗判定の改善が接触リスク・復帰負担を増やすなら範囲を縮小する。',['FC049','AC051','AC085','AC146','FC031'],['EAT-N01','EAT-N02','EDP-01','EDP-02','EEX-WTED','EDP-24']),
 ('T04','条件変化を検出する検査AIの更新採否判定','I04','人の追加学習を使いつつ、条件別の見逃し・過検出を悪化させず更新したい。','撮像・工具・材種等の条件を記録し、変化検出→人のラベル→独立評価→更新承認・版管理をつなぐ。工程ごとに出荷判定や停止判断は別途設定。','良品のみの学習／追加学習／ルール判定を比較。工具・照明等を一条件ずつ変え、学習に使わない評価群を確保。','条件別の見逃し・過検出、追加データ量、ラベル工数、更新作業、不要停止コスト。','ZERO等の既存機能で満たせるかを確認。単一精度指標の向上だけで、条件別悪化や更新負担を隠す提案は採用しない。',['FC036','FC039','FC040','AC225','FC063'],['EDP-14','EDP-15','EDP-12','EOV-W08','EDP-13','EDP-33']),
 ('T05','SimReady物理属性の検証と実機誤差評価','I05','生成データを学習・検証に使う前に、どの物理条件が実機との差を生むか見極めたい。','質量・重心・摩擦・関節の由来、単位、推定／実測、誤差範囲を保持し、物理整合チェック→仮想試験→実機の限定動作で比較する。','単純形状の把持・配置などに範囲を限定。生成属性／実測属性／従来手作業モデルを比較。ToknのNC訓練と物流ロボット学習は別に扱う。','物理属性の誤差、動作結果の仮想／実機差、検証工数、修正した属性と誤差改善の対応。','既存SimReady検証機能で十分なら追加開発を減らす。外観品質だけ改善し、実機差・検証工数が改善しなければ採用しない。',['AC273','AC098','FC021'],['EEX-WNDOT','EDP-17','EDP-20']),
]

def build_synthesis(cards,evidence):
 byid={c['card_id']:c for c in cards};ev=evidence if isinstance(evidence,dict) else {e['evidence_id']:e for e in evidence}
 def base(ids,eids=None):
  eids=eids or list(dict.fromkeys(e for cid in ids for e in byid[cid]['evidence_ids']))
  assert set(ids)<=byid.keys() and set(eids)<=ev.keys()
  return dict(card_ids=ids,evidence_ids=eids,source_urls=[ev[e]['url'] for e in eids],source_locators=[f"{e}: {ev[e]['locator']}" for e in eids],analysis_date='2026-10-17',source_checked_date='2026-10-16')
 methods=[dict(method_id=i,method=n,mechanism=m,human_boundary=h,comparison=c,year_change=y,statement_type='調査者の横断整理。機能記述は紐付けた原典要旨。',**base(ids,METHOD_EVIDENCE[i])) for i,n,m,h,c,y,ids in METHODS]
 positions=[]
 for n,(cid,mid,col,company,task,status) in enumerate(POSITIONS,1):
  c=byid[cid];positions.append(dict(position_id=f'P{n:02}',card_id=cid,method_id=mid,function=FUNCTIONS[col],function_index=col,company=company,official_company=c['company'],task=task,status=status,booths_2026=c['booths_2026'],**base([cid])))
 years=[dict(change_id=i,pattern=n,baseline=b,current=c,interpretation=u,statement_type='複数事例の変化パターン〈分析〉。一様な進化や初発明年は示さない。',**base(ids,eids)) for i,n,b,c,u,ids,eids in YEARS]
 issues=[dict(issue_id=i,issue=n,observed_facts=f,shared_issue=a,limits=l,statement_type='事実に基づく共通論点〈調査者分析〉。業界全体の未解決を証明しない。',**base(ids,eids)) for i,n,f,a,l,ids,eids in ISSUES]
 themes=[dict(theme_id=i,theme=n,issue_id=issue,customer_problem=p,technical_approach=a,experiment=e,metrics=m,adoption_condition=ad,stage='研究開発候補・未採否・効果未検証',statement_type='研究仮説。既存製品の不足や優位性を確認したものではない。',**base(ids,eids)) for i,n,issue,p,a,e,m,ad,ids,eids in THEMES]
 coverage=dict(analysis_date='2026-10-17',source_checked_date='2026-10-16',companies=len({byid[p['card_id']]['company'] for p in positions}),cards=len({p['card_id'] for p in positions}),positions=len(positions),method_families=len(methods),year_patterns=len(years),common_issues=len(issues),research_candidates=len(themes),scope='訪問優先28社・33カード。SOFIXの予測／搬送、SiemensのTokn／海外物流試験を分けた35配置。市場全体の比率・性能順位ではない。',remaining=['未公開の承認権限・失敗検知・再試行・復帰条件は確認待ち。公開情報不足を製品の欠陥としない。','ToolDiscoveryとユシロALFREDの補足技術資料、2024同名原典不足は継続残件。','研究候補は既存機能との重複確認・現地質問・小規模実験を経て選定する。最終1枚への集約は未着手。'])
 return dict(method_comparison=methods,technology_method_positions=positions,year_change_patterns=years,common_issues=issues,research_candidates=themes),coverage


class Drawing:
 """Write the same simple primitives to SVG and a static PNG preview."""
 def __init__(self,w,h,title):
  self.w,self.h=w,h;self.image=Image.new('RGB',(w,h),'white');self.draw=ImageDraw.Draw(self.image)
  self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}"><style>text{{font-family:Meiryo,sans-serif}}a:hover rect{{stroke:#c58b22;stroke-width:2}}</style>']
 def font(self,size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('meiryob.ttc' if bold else 'meiryo.ttc'),size)
 def rect(self,x,y,w,h,fill,stroke=None):
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
  self.draw.rounded_rectangle((x,y,x+w,y+h),radius=3,fill=fill,outline=stroke)
 def text(self,x,y,text,size=16,bold=False,color='#203b50'):
  f=self.font(size,bold);assert x+self.draw.textlength(text,font=f)<=self.w-10,text
  self.svg.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{color}">{html.escape(text)}</text>')
  self.draw.text((x,y),text,font=f,fill=color,anchor='ls')
 def lines(self,text,width,size):
  f=self.font(size);out=[]
  for para in text.split('\n'):
   line=''
   for token in re.findall(r'[A-Za-z0-9][A-Za-z0-9./+–-]*|.',para):
    if line and self.draw.textlength(line+token,font=f)>width:out.append(line.rstrip());line=token.lstrip()
    else:line+=token
   out.append(line)
  return out
 def paragraph(self,x,y,text,width,size=16,gap=25):
  for line in self.lines(text,width,size):self.text(x,y,line,size);y+=gap
  return y
 def save(self,stem):
  self.svg.append('</svg>');s=''.join(self.svg)
  (ROOT/'outputs'/f'{stem}.svg').write_text(s.replace('href="#','href="JIMTOF2026_技術整理と全体マップ_v1.html#'),encoding='utf-8');self.image.save(ROOT/'outputs'/f'{stem}.png')
  return s


def draw_figures(data):
 positions=data['technology_method_positions'];methods=data['method_comparison'];years=data['year_change_patterns']
 widths=[max(sum(p['method_id']==m['method_id'] and p['function_index']==col for p in positions) for col in range(5)) for m in methods]
 heights=[max(82,n*64+12) for n in widths];w=1930
 d=Drawing(w,190+sum(heights)+72,'28社の技術方式と任せる仕事の比較マップ')
 d.text(25,39,'28社・33カード｜技術方式 × 任せる仕事',28,True)
 d.text(25,70,'35配置：SOFIXの予測と搬送、SiemensのToknと海外物流試験を分離。セル内をクリックすると事実カードへ。',17)
 d.text(25,99,'横軸は機能の種類。自律性・性能・成熟度の順位ではない。実機動作には人の遠隔操作・AI未確認の自動化も含む。',16)
 d.rect(20,119,280,48,'#244b63');d.text(32,149,'方式／比較の単位',18,True,'#ffffff')
 for col,name in enumerate(FUNCTIONS):d.rect(310+col*320,119,310,48,'#244b63');d.text(321+col*320,149,name,18,True,'#ffffff')
 y=177
 for m,rh in zip(methods,heights):
  d.rect(20,y,280,rh-6,'#e8f0f5');d.text(31,y+26,m['method_id'],16,True)
  d.paragraph(31,y+53,m['method'],255,18,26)
  for col in range(5):
   x=310+col*320;d.rect(x,y,310,rh-6,'#f1f6f8' if col<4 else '#f0f5ef')
   ps=[p for p in positions if p['method_id']==m['method_id'] and p['function_index']==col]
   for k,p in enumerate(ps):
    sy=y+6+k*64;d.svg.append(f'<a href="#{p["card_id"]}">');d.rect(x+5,sy,300,59,'#ffffff','#b8ccd5')
    d.text(x+12,sy+17,p['company']+'  '+p['card_id'],14,True)
    d.text(x+12,sy+36,p['task'],14)
    d.text(x+12,sy+52,p['status'],12,False,'#785a20');d.svg.append('</a>')
  y+=rh
 d.text(25,y+22,'配置は確認できた主な出力先。空欄は技術の不存在を示さない。各製品の提供段階・AIの内訳はカードを参照。',16)
 d.text(25,y+49,'横断整理・追補：2026-10-18 ／ 基礎原典：10/16・補足：10/18 ／ 現地実演・性能は未検証。',15)
 method_svg=d.save('JIMTOF2026_方式別比較マップ_v1')
 # Three equal evidence lanes preserve the discontinuities and missing baselines.
 rh=205;d=Drawing(1930,190+len(years)*rh+65,'2024以前と2025年から2026年の変化パターン')
 d.text(25,39,'2024以前 → 2025–2026｜何が変わり、何が未確定か',28,True)
 d.text(25,74,'出展説明と企業公式リリースの確認範囲。技術の初発明年や業界全体の一様な進化を表す図ではない。',17)
 for x,width,label in [(20,250,'変化パターン'),(280,520,'2024以前に確認'),(810,550,'2025–2026に確認'),(1370,540,'解釈・未確定')]:d.rect(x,101,width,48,'#244b63');d.text(x+12,132,label,18,True,'#ffffff')
 y=161
 for r in years:
  d.rect(20,y,250,rh-10,'#e8f0f5');d.text(32,y+27,r['change_id'],16,True);d.paragraph(32,y+57,r['pattern'],225,19,29)
  for x,width,k,fill in [(280,520,'baseline','#f1f6f8'),(810,550,'current','#edf7f4'),(1370,540,'interpretation','#fff5df')]:
   d.rect(x,y,width,rh-10,fill);end=d.paragraph(x+12,y+29,r[k],width-24,18,28);assert end<y+rh-8,(r['change_id'],k,end)
  y+=rh
 d.text(25,y+22,'根拠ID・比較対象の全カードは同じHTMLの年度比較表とExcel「横断比較・技術マップ」に収録。',16)
 d.text(25,y+48,'研究候補は未採否の仮説。公開情報の不足は、各製品に機能がないことや現場の不具合を意味しない。',15)
 year_svg=d.save('JIMTOF2026_年度変化比較図_v1')
 return method_svg,year_svg


def synthesis_html(data,coverage,figures):
 H=lambda s:html.escape(str(s),quote=True)
 def cards(r):return ' '.join(f'<a class="tag" href="#{cid}">{cid}</a>' for cid in r['card_ids'])
 def sources(r):return '<details><summary>根拠・該当箇所</summary>'+''.join(f'<p><a href="#{e}">{e}</a> · <a href="{H(u)}" target="_blank" rel="noopener">公式原典</a><br>{H(loc)}</p>' for e,u,loc in zip(r['evidence_ids'],r['source_urls'],r['source_locators']))+'</details>'
 def table(headers,rows):return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+H(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
 out=['<section id="synthesis"><h2>28社を横断：方式・任せる範囲・年度変化</h2><p>横断整理・追補：2026-10-18 ／ 基礎原典：10/16・補足：10/18。訪問優先28社・33カードを10方式に整理し、同一カード内の別の仕事を分けて35配置にしました。</p><div class="guide"><div><h3>方式は一種類ではない</h3><p>履歴予測、物理・加工ルール型CAM、対話生成、画像・時系列判定、機構・ルール自動化を比較。AIの呼称だけでまとめません。</p></div><div><h3>提案から実行への境界を見る</h3><p>CAMの人による検証、匠フォースの承認、WinToolの管理者承認、Panasonicの遠隔介入を明示。未公開の権限・復帰条件は残します。</p></div><div><h3>新規・継続・比較不能を分ける</h3><p>2026は対象工程・導入構成の具体化が目立つ〈今回の対象内の分析〉。既存技術を2026の初登場と数えません。</p></div></div><p class="note">この地図の横軸は機能の種類です。自律性や性能の順位、メーカー間の接続、業界の普及率は表しません。2026年は展示予定。海外の別実証、製品発表、提供計画、参考出品を区別します。</p>']
 for svg,title,stem in [(figures[0],'技術方式と仕事の配置','JIMTOF2026_方式別比較マップ_v1'),(figures[1],'2024以前からの変化パターン','JIMTOF2026_年度変化比較図_v1')]:
  out.append(f'<h3>{title}</h3><p><a href="{stem}.svg">拡大SVG</a> ／ <a href="{stem}.png">画像PNG</a></p><div class="scroll">'+svg.replace('width="1930"','width="100%" style="min-width:1150px;height:auto"',1)+'</div>')
 out.append('<details><summary>10方式の比較：入力・判断／実行・人の仕事・年度差分・根拠</summary>'+table(['方式','何を入力し何をするか','人が担う部分','方式間の違い・制約','年度変化・カード・根拠'],[[f'<b>{r["method_id"]} {H(r["method"])}</b>',H(r['mechanism']),H(r['human_boundary']),H(r['comparison']),H(r['year_change'])+'<br>'+cards(r)+sources(r)] for r in data['method_comparison']])+'</details>')
 out.append('<details><summary>年度変化6パターンの根拠を開く</summary>'+table(['パターン','2024以前','2025–2026','解釈・未確認／根拠'],[[H(r['change_id']+' '+r['pattern']),H(r['baseline']),H(r['current']),H(r['interpretation'])+'<br>'+cards(r)+sources(r)] for r in data['year_change_patterns']])+'</details><p>下の工程マップは従来の代表例を工程から見る別の図です。今回の28社横断は上の方式別マップを参照してください。</p></section>')
 out.append('<section id="research-candidates"><h2>共通課題 → 研究開発テーマ候補</h2><p>原典で確認した機能 → 共通論点〈分析〉 → 研究候補〈未検証仮説〉を分けます。公開資料で不明なことを、その製品に機能がないことや業界全体の未解決課題とは扱いません。テーマの採否と1枚への集約は後工程です。</p>')
 out.append(table(['共通論点','確認した事実','横断して考える点〈分析〉','限界・既存機能／研究候補'],[[f'<b id="{r["issue_id"]}">{r["issue_id"]} {H(r["issue"])}</b>',H(r['observed_facts'])+'<br>'+cards(r),H(r['shared_issue']),H(r['limits'])+f'<p><a href="#T0{i+1}">研究候補 T0{i+1}へ</a></p>'+sources(r)] for i,r in enumerate(data['common_issues'])]))
 for r in data['research_candidates']:
  out.append(f'<article class="research-theme" id="{r["theme_id"]}" style="margin-top:24px;padding:22px;border:1px solid #bdced8;border-left:5px solid #117a83;scroll-margin-top:100px"><span class="id">{r["theme_id"]} · {H(r["stage"])}</span><h3>{H(r["theme"])}</h3><p><a href="#{r["issue_id"]}">共通論点 {r["issue_id"]}</a> ／ {cards(r)}</p><dl>'+''.join(f'<dt>{label}</dt><dd>{H(r[k])}</dd>' for k,label in [('customer_problem','顧客課題〈仮説〉'),('technical_approach','技術的な取り組み案'),('experiment','比較対象・限定実験'),('metrics','測る指標〈目標値は未設定〉'),('adoption_condition','採用条件・見送り条件')])+f'</dl><p class="small muted">{H(r["statement_type"])}</p>'+sources(r)+'</article>')
 out.append('<p class="export"><a href="../data/research/technology_atlas_v1/method_comparison.csv">方式比較CSV</a> ／ <a href="../data/research/technology_atlas_v1/technology_method_positions.csv">配置CSV</a> ／ <a href="../data/research/technology_atlas_v1/year_change_patterns.csv">変化パターンCSV</a> ／ <a href="../data/research/technology_atlas_v1/common_issues.csv">共通課題CSV</a> ／ <a href="../data/research/technology_atlas_v1/research_candidates.csv">研究候補CSV</a></p></section>')
 return ''.join(out)
