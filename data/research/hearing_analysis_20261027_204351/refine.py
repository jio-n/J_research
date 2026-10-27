import pathlib,json
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];old=R/'data/research/hearing_analysis_20261027_201005';O=R/'outputs'/D.name;O.mkdir(exist_ok=False)
name='JIMTOF2026_現地ヒアリングと事前仮説の照合.md'
s=(R/'outputs'/old.name/name).read_text(encoding='utf8')
def replace_once(a,b):
    global s
    assert s.count(a)==1,a[:80]
    s=s.replace(a,b)
replace_once('2026年10月27日・追補反映版。対象は、本人のメモがある7社、10月21〜23日の事前調査、判断知識についての本人追補R001。原文メモと前版は変更せず、本資料を別版として作成した。','2026年10月27日・2024年比較／業務データ循環の追補反映版。対象は、本人のメモがある7社、事前調査、本人追補R001・R002、今回追加確認した2024年の一次資料。原文メモと前版は変更せず、本資料を別版として作成した。')
replace_once('**製造業務の判断と実行を接続する方向性は強まった。ただし、今回の現地メモから最も具体的に見える進展は、生成AIが製造知識・現在の設備状態・既存の解析ツールを使い、加工準備、原因分析、改善提案、設定操作へつなぐ構成である。工場全体の自律運営や、切削中の品質を継続的に保証する自律加工が完成したとは言えない。**','**2024年にも示されていた生成AIによる製造支援の構想が、2026年には機械・CAD/CAMのUI、実データ参照、解析・シミュレーションや設定操作へ具体化している。判断知識と専門ツールを使って業務を支援し、その過程を文脈付きのデータとして残せることに、目の前の省力化と次の改善をつなぐ価値がある。**\n\n今回の現地メモは、工場全体の自律運営や切削中の継続的な品質保証の完成までは示さない。また、2024年に設備データ連携の構想がなかったとも言えない。世代差は、生成AIが既存の製造技術を利用する適用範囲・組込み・具体性の前進として評価する。')
replace_once('更新すべきなのは、①接続の実装手段、②知識の扱いが性能を左右する具体的な問題、③商用化を制約する費用・速度・責任、④同じAIエージェントでも異なる顧客業務、の4点である。','更新すべきなのは、①2024年の構想からの実装進展、②知識を使う判断と専門ツールへの接続、③業務を使う過程で文脈付きデータを生成する価値、④商用化を制約する費用・速度・責任、⑤同じAIエージェントでも異なる顧客業務、の5点である。')
replace_once('## 4. 各社の位置付けと到達範囲',(D/'sections.md').read_text(encoding='utf8')+'\n## 4. 各社の位置付けと到達範囲')
replace_once('|実測と加工モデルを結ぶ検証基盤|','|課題解決過程の文脈保存・評価|依頼・対象ID・観測・判断知識・ツール入力出力・人の修正・実行結果→案件単位の記録と評価→再利用可能な事例・改良対象|R002の業務利用を通じたデータ生成という仮説。対話だけでなく、計測・解析・実機結果を紐付ける。各社での完成は未確認。|実行結果まで紐付いた案件率、追跡・再現可能性、専門家の評価工数、知識改訂への利用件数。|\n|実測と加工モデルを結ぶ検証基盤|')
replace_once('### 現地メモの短い原文抜粋','### 本人追補R002と2024年比較の追加根拠\n\nR002は、2024年との比較、製品内へのエージェント統合、課題解決過程のデータ蓄積、専門ツールと自然言語UXについての本人追補。[追補原文](https://github.com/jio-n/J_research/blob/main/data/research/hearing_analysis_20261027_204351/R002.txt)は別保存し、既存7社のメモへ合成していない。企業名のない横断観察を、新たな個別ブースの訪問実績として数えない。\n\n- W08：三菱電機・関口俊一氏「生成AI利活用におけるガバナンス・ELSIリスク対応に向けて」、2025-01-24、印刷頁8。大阪大学ELSIセンター公開の企業講演資料。2026-10-27に本文とページ画像を確認。JIMTOF2024のトラブルシューティングアプリと、装置データ利用・継続学習の構想を確認。社内文書RAGの記載とは別項目。\n- W09：三菱電機JIMTOF2024公式出展ページ。2026-10-27本文確認。NC MachiningAID、シミュレーション・監視・DXの存在を確認。生成AIアプリの具体的方式はこのページから確定しない。\n- W10：MCP 2025-06-18版Server Features。2026-10-27本文確認。Prompts・Resources・Toolsの区分を確認。ファナック独自のナレッジ登録方式を証明するものではない。\n\n### 現地メモの短い原文抜粋')
(O/name).write_text(s,encoding='utf8',newline='\n')
extra=" ['W08','https://elsi.osaka-u.ac.jp/system/wp-content/uploads/2025/02/2_MitsubishiSekiguchi_ELSIForum2024_forWEB.pdf','本文・印刷頁8の画像確認','2025-01-24企業講演資料。JIMTOF2024の事例'],\n ['W09','https://www.mitsubishielectric.co.jp/fa/events-seminars/exhibitions/2024/jimtof2024/index.html','本文確認','2024年のCNC・DX説明'],\n ['W10','https://modelcontextprotocol.io/specification/2025-06-18/server','本文確認','Prompts・Resources・Tools'],\n"
for fn in ['build.mjs','verify.mjs','publish.py']:
    v=(old/fn).read_text(encoding='utf8')
    if fn=='build.mjs':
        v=v.replace("const inputs=[","const inputs=['data/research/hearing_analysis_20261027_204351/R002.txt','data/research/hearing_analysis_20261027_204351/sections.md',",1)
        v=v.replace('const urls=[\n','const urls=[\n'+extra,1)
    if fn=='publish.py':v=v.replace("target='analysis-20261027-r2.html'","target='analysis-20261027-r3.html'")
    (D/fn).write_text(v,encoding='utf8',newline='\n')
source={'id':'W08','publisher':'三菱電機（関口俊一氏、企業講演資料）','host':'大阪大学ELSIセンター','date':'2025-01-24','pagePrinted':8,'refersTo':'JIMTOF2024','url':'https://elsi.osaka-u.ac.jp/system/wp-content/uploads/2025/02/2_MitsubishiSekiguchi_ELSIForum2024_forWEB.pdf','checked':'2026-10-27','verification':'本文と該当ページ画像を確認','supports':['JIMTOF2024の生成AIトラブルシューティングアプリ','装置データを使う解析と利用を通じた学習の構想も当時の図に存在'],'doesNotEstablish':['JIMTOF2024アプリの方式がRAGだったこと','2024で全機能が実装済みだったこと','2026の導入率・普及率の定量比較']}
(D/'year_comparison_sources.json').write_text(json.dumps([source],ensure_ascii=False,indent=2),encoding='utf8')
(D/'change_log.json').write_text(json.dumps({'previous':old.name,'supplement':'R002.txt','changes':['2024年側の企業講演PDFと出展説明を確認。装置データ利用・学習の構想は既存と明記','世代差を生成AIの製品UI組込み・実データ参照・ツール利用の具体化として整理','課題解決の記録と検証結果を結ぶデータ生成・改善の二つの循環を追加','判断知識の渡し方の各社比較を更新','専門的な加工解析・モデル化の競争力と自然言語UXの役割を整理'],'unchanged':['7社の生メモ','前版','訪問実績数7社'],'externalSourceReview':'今回の追加確認はW08〜W10。W01〜W07の確認記録は前版の同日調査を継承。'},ensure_ascii=False,indent=2),encoding='utf8')
(D/'READING_GUIDE.md').write_text('# 2024年比較・業務データ循環の追補反映版\n\nHTMLとMarkdownはoutputs/hearing_analysis_20261027_204351/。本人追補R002を原文で保存し、前版の第1節・第3.8〜3.10節・開発候補・根拠を更新。以前の成果物と7社の生メモは変更していない。\n\n2024年側は三菱電機の企業講演資料（大阪大学ELSIセンター公開、2025-01-24、印刷頁8）を本文・画像で確認した。2024年にも装置データ利用と継続学習の将来像があるため、2026年に初めて登場したとしない。JIMTOFアプリをRAGと確定する資料ではない。2026年の本人観察との比較は、生成AIの適用・組込み・ツール利用の具体化についての定性的分析。\n\nデータ循環は価値の仮説で、紐付け・実測結果・評価を備えた学習用データセットが各社で完成したと断定していない。対話履歴は判断知識獲得の一手段という前版の整理も維持する。\n\nW08〜W10を今回追加確認し、前版の原典確認記録を継承。PDF全文・ページ画像は_privateに置きGitHubには含めない。\n',encoding='utf8')
print(str(O))
