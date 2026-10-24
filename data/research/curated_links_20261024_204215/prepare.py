import json, pathlib, hashlib, csv
D = pathlib.Path(__file__).resolve().parent
R = D.parents[2]
p = json.loads((R/'data/research/linked_visit_planner_20261024_150004/link_plan.json').read_text(encoding='utf-8-sig'))
p['source_workbook'] = 'outputs/linked_visit_planner_20261024_150004/JIMTOF2026_ユーザー選定_調査企業一覧_リンク付き.xlsx'
p['source_sha256'] = hashlib.sha256((R/p['source_workbook']).read_bytes()).hexdigest()
p['links'] = [x for x in p['links'] if x['cell'].startswith(('A','D'))]
rows = [
 (4, 'SimReady：アセット検証と実行時検証の分担', 'https://docs.omniverse.nvidia.com/simready/latest/simready-faq.html', 'NVIDIA', 'How Do I Validate My Composed Scene…／Would Schemas Allow…', '個別アセットの構造・属性等を静的検証し、組合せたシーンの接続や挙動はシミュレータ実行で確認する。', 'TRINIXの生成物を検証する際の比較基準。TRINIXが全項目を自動生成・検証できる証拠ではない。'),
 (5, 'Fuzzy Studio：軌道生成・干渉確認と実機制御', 'https://www.linkage-japan.co.jp/simulator', 'リンケージ', 'Fuzzy Studioの特徴／Fuzzy RTOS', 'ノーコードでセル設計・軌道生成・リーチと衝突の確認。Fuzzy RTOSによる実機制御と周辺機器連携を説明。', '関連する製品の仕組み。統合システム全体のAI担当範囲や当日の組合せは未確定。'),
 (6, 'HS4200：4主軸の並列加工・着脱と走行ロボット', 'https://smd.co.jp/lineup/hs4200/', 'シマダマシンツール', '4主軸2NC／ローディングロボット', '加工中に別主軸で着脱できる構成と、機械上部のレールを走行するローディングロボットを説明。', 'ハード構成の説明。フィジカルAIが何を認識・判断するかはこのページだけでは確認できない。'),
 (10, '画像による教示位置補正（自然言語教示との比較）', 'https://www.mamezou.com/services/embedded/pdc_teachcorrection', '豆蔵', 'ロボットのティーチング自動補正／補正の方法', '基準画像との位置差を検出し教示位置を補正。Z方向、XY方向の補正や、補正と溶接を繰り返す方法を説明。', '従来型の画像補正を比較する参考資料。同じAIティーチング製品や今回展示の実装方式と断定しない。'),
 (12, 'TwinCAT CNC：独自モジュールとオンライン補正', 'https://www.beckhoff.com/de-de/unternehmen/presse/twincat-3-cnc-mit-neuen-funktionen-und-technologiepaketen-2024-09.html', 'Beckhoff', 'TF5262 CNC Online Adaption／2024-09-10', 'TcCOMで独自の補間処理を組込み可能。工具変形に応じた経路補正、工具径補正、送り補正を説明。', '独語資料。オンライン補正の開放性の根拠であり、生成AIや学習制御を標準搭載する証拠ではない。'),
 (13, 'CoAgent Operations：稼働データによる故障解析', 'https://www.beckhoff.com/en-en/products/automation/twincat/tfxxxx-twincat-3-functions/tf1xxx-system/tf1700.html', 'Beckhoff', 'TF1700 TwinCAT 3 CoAgent Operations／Product status', '機械・工程の現在データ、ログ、システムメッセージから診断を支援。独自文書の追加やTwinCATコマンド操作も説明。', 'D列のEngineering用TE1700とは別の運用向けTF1700。製品発表段階で発売時期は問い合わせ。展示未確認。'),
 (23, '歯車のClosed Loop・DDQM・工程データ連携', 'https://klingelnberg.com/jp/ニュース/見本市/イベント情報/jimtof-2026', 'Klingelnberg', 'QBG／DDQM／Smart Tracing／Smart Factory／JIMTOF 2026でお会いしましょう', '測定値の加工へのフィードバック、工程横断の品質データ利用、サーボトレース解析を説明。', 'メーカーの展示特設。バーチャルマシン・シミュレーションによる紹介と明記。各機能が実機で連続実演されるとは限らない。'),
 (25, '関連制御技術：加工ナビM-iの振動測定→回転数補正', 'https://www.okuma.co.jp/solution_technology/process/', 'オークマ', 'ミーリング加工用加工条件探索機能／加工ナビM-i', '内蔵センサでびびり振動を測定し、適切な主軸回転速度を算出して指令を自動変更。M-g系は候補提示後のワンタッチ変更。', 'OSP-P500と併せて質問する関連制御技術。P500全機種の標準装備や今回の展示を示すものではない。AI利用もこの資料だけでは不明。'),
 (32, 'Materials Enrich：短繊維樹脂の疲労曲線予測例', 'https://nexus.hexagon.com/community/public/nexus-materials-connect-enrich/b/nexus-materials-news-announcements/posts/can-i-predict-fatigue-curves-for-short-fiber-reinforced-plastics-absolutely', 'Hexagon／Bernard Alsteens', 'Can I predict fatigue curves for short fiber reinforced plastics? Absolutely!／2025-07-29', '引張曲線と1本のS-N曲線を基に、温度・繊維含有率・荷重角度等を変えた疲労曲線を予測しCAEへ渡す例。', '短繊維強化樹脂の事例。金属材料への適用やあらゆる条件での精度保証を示さない。展示未確認。'),
 (33, 'Techman AI Vision：画像認識・位置決めとモデル学習', 'https://www.tm-robot.com/ja/product/ai-vision', 'Techman Robot', 'AI Vision／AI+ Trainer／AI+ AOI Edge', '画像による位置決め・寸法・外観検査、TMflowとの統合、モデルの学習・配備を説明。', 'ナベルが扱う協働ロボットの技術資料。VLAや動作生成の搭載を示すものではない。今回の構成は現地確認。'),
]
extra=[]
for row,label,url,publisher,locator,summary,limit in rows:
    extra.append(dict(id=f'P{row-1:02}',sheet='AI・フィジカルAI',cell=f'H{row}',text=label,url=url,kind='追加技術資料',publisher=publisher,locator=locator,reviewed_summary=summary,scope_note=limit,checked_date='2026-10-24',evidence_type='原典本文の要約（原文引用ではない）'))
primary={x['url'].rstrip('/') for x in p['links'] if x['cell'].startswith('D')}
assert not any(x['url'].rstrip('/') in primary for x in extra)
assert len({x['url'].rstrip('/') for x in extra})==len(extra)
p['links']+=extra
p['additional_sources']=extra
p['headers'].append('追加技術資料')
p['ai'][-1]['values'][0]='株式会社ナベル'
labels={x['id']:x['text'] for x in extra}
for item in p['ai']:
    item['values'].append(labels.get(item['id']))
for item in p['automation']:
    item['values'].append(None)
p['changes']=[{'change':'F・G列のリンク64件を削除し、黒文字・下線なしに変更。本文・質問は保持。'},{'change':'H列追加技術資料を両シートに追加。本文精読済みの別資料10件のみ採用。自動化50社のH列は空欄。'}]
p['policy']='既存2シート・行順・A:Gの値・優先・着眼点・質問を保持。A/Dのリンク114件は変更しない。HはDとURL重複なしの追加資料に限定。関連方式・比較資料・開発段階はリンクの説明に注記。'
(D/'link_plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
with (D/'additional_sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(extra[0]));w.writeheader();w.writerows(extra)
print(json.dumps({'kept_links':len(p['links'])-len(extra),'additional_links':len(extra),'source_sha256':p['source_sha256']}))
