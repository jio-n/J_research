import pathlib,json,html,collections
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name;data=json.loads((R/'data/research/visits_csv_update_20261027_093945/app_data.json').read_text(encoding='utf8'));by={x['shortName']:x for x in data['companies']};H=html.escape
events=[];minute=600
def add(duration,kind,title,note='',company=None):
 global minute
 e={'start':minute,'end':minute+duration,'duration':duration,'kind':kind,'title':title,'note':note}
 if company:e['company']=by[company]
 events.append(e);minute+=duration
def visit(name,duration,note):add(duration,'visit',name,note,name)
visit('ヤマザキマザック',20,'工程設計・生産計画エージェントの担当範囲と、人の承認を確認。構想と現在動くMAZATROL DXを分ける。全製品説明には広げない。')
add(5,'move','東1内を移動','マザックからCAMSUPSへ。途中の緑・青には立ち寄らない。')
visit('CAMSUPS',20,'Cam Agent Betaの個別実演の有無を最初に確認。入力→工程・工具・条件→工具経路と検証のどこを自動生成するかに絞る。実演・担当者が不在なら5分で資料取得して先へ。')
visit('クオリカ',10,'緑の短時間枠。KOM-MICSの2024年からの変化、負荷一定化の条件算出とNCへの戻し方だけ聞く。移動を含む10分の上限。遅れたら最初に省略。')
add(5,'move','東1→東2','C＆Gシステムズへ。')
visit('C＆Gシステムズ',20,'AI切削条件算出のロジック、共同研究、顧客条件の学習・適用外判定を優先。CAM全般の説明より条件決定の中身を聞く。')
visit('ベッコフオートメーション',10,'緑の短時間枠。外部センサ→解析→CNC補正の周期・組込範囲に絞る。CoAgentの一般説明は今日は省略。Hexagonへ替えるならこの10分枠との入替にする。')
add(5,'move','東2→東3','シーメンスへ。')
visit('シーメンス',10,'Eigenと人型ロボットの個別展示・実演を先に照会。見られる対象とAIの担当だけ確認。構想紹介だけなら5分で切り上げ、後日の資料確認へ回す。')
visit('オークマ',15,'OSP-AIの2024年からの差と、検出後に退避・再開・条件変更のどこまで自動化するか。OSP-P500の総合説明は短く。')
add(15,'move','東3→東8','DMGへ。棟間の通路移動枠。所要は仮置きで、途中の他ブースは省略。')
visit('DMG森精機',25,'GENIAC／製造データ基盤・物理モデルと、実際の製品の境界を重点確認。サービス／Condition Agentは実機データとの接続・制御への戻し方を一問ずつ。')
add(10,'move','東8→東7','TPRのある東7へ戻る。')
visit('TPR大阪精密機械',10,'緑の短時間枠。歯車測定から何の補正値を算出し、加工機へどう返すか。人の承認、再測定、補正上限だけ聞く。遅延時は省略可能。')
add(5,'move','東7内を移動','ハイデンハインへ。')
visit('ハイデンハイン',15,'VT122＋VTC 6.0の実演機種、摩耗・欠損の診断範囲、検知結果を工具交換・運転継続へつなぐ部分を確認。総合製品説明は省略。')
add(5,'move','東7内を移動','ナガセへ。')
visit('ナガセインテグレックス',25,'生成AI画像変換とCNN砥面判定の役割、従来との変化、研究と製品実装を分けて聞く。推定からドレス判断・実行へつながる範囲を重点確認。')
add(20,'break','昼食・休憩','東7付近で行列に並ばない軽食を想定。売店・席・店の場所を確認した予約ではない。')
add(25,'transfer','東7→南2','公式全体図の無料巡回バスを候補に、待ち・乗車・入場を含む25分枠。運行は当日確認。待ちだけで10分を超えそうなら案内で移動方法を確認し、南の開始遅れを把握する。')
visit('ファナック',25,'最初の2分でAI溶接エージェントの展示有無を確認。あれば図面→条件・動作生成と人の修正範囲を優先。なければ現場適応・日立連携の説明を短時間で取得し、無理に25分使わない。')
visit('三菱電機',25,'ヒューマノイド×CNCのタスク生成・割当・実行の実演を最優先。未登録作業、失敗時の復帰、AIと教示の境界を聞く。実演待ちで枠を超えない。')
add(10,'move','南2・1F→南3・4F','エスカレーター等の階移動。南1の青候補へは寄らない。')
visit('たけびし',10,'MCP AdapterでAIへ渡せるデータ、AIから設備へ操作を返せる範囲、承認・権限境界を一問ずつ。製品全体の説明へ広げない。')
add(5,'move','南3内を移動','モリマシナリーへ。')
visit('モリマシナリー',15,'工具摩耗の判定対象、必要データ、根拠表示、2024年からの変更を確認。寿命予測と単なる画像判定を分ける。')
add(10,'move','南3→南4・同じ4F','Phoxterへ。途中の緑・青は後回し。')
visit('Phoxter',20,'黄色のAI＋ルール検査を15分の主題にする。良品学習・寸法ルール・ロボット撮像の担当範囲を確認。残り5分だけ保守チャットボットへ。遅れたらチャット部分を省く。')
add(15,'buffer','遅延吸収・余ればNdotlight','基本は予備枠。16:35までにPhoxterを出られ、移動を含め16:50までに終えられる場合だけNdotlightを最大10分。遅れていれば追加しない。')
add(10,'exit','記録・退出','16:50で追加商談を打ち切り、音声メモの企業名・写真の対応を確認して退出へ。17:00終了。駅到着時刻の保証ではない。')
assert minute==1020
planned={e['company']['id'] for e in events if e.get('company')};yellow={x['id'] for x in data['companies'] if x['priority']=='黄色'};assert yellow<=planned and len(planned)==16
optional=by['Ndotlight Co., Ltd.']['id'];dispositions=[]
special={'日本クリンゲルンベルグ':'歯車の閉ループ比較は今日はTPRへ集約。双方の詳説を回らず、追加質問を後日にする。','Hexagon Manufacturing Intelligence':'有力だが3テーマで時間を使う。今日はC＆G／CAMSUPSを優先。見たい場合はベッコフ10分枠と入替。','東京エレクトロンデバイス':'経路自動生成は有力だが、東7は黄色3社とTPRを優先。TPR10分枠との入替は可。','匠技研工業':'見積・図面検索は今回は後順位。南3の黄色2社を削らずに加えない。','三菱商事テクノス':'エージェント連携の比較は三菱電機へ集約。南3ではたけびし・モリを先に確保。','ミロクリエ':'保全チャット比較はDMG／Phoxterへ寄せ、今日は独立した説明時間を取らない。','興和オプトロニクス':'画像判定・工具状態の比較はナガセ／モリ／Phoxterを先に。','ツールディスカバリー':'緑だが西への独立移動が必要。条件算出はC＆Gを優先して西の移動を省く。','シマダマシンツール':'実機連携は有力だが、今日は黄色のCNC・ロボット連携を優先。','伊藤忠マシンテクノス':'具体展示の確認から始まる候補。黄色の実演・方式確認の時間を先に守る。','牧野フライス製作所':'今回見るアイテムが未指定のため、大型ブースを漫然と回る時間を割かない。','ソフィックス':'全体自律化の比較は有力だが、独立の説明時間が必要。今日は黄色の連携実演を優先。','シチズンマシナリー':'南2で近いが優先色は未指定。ファナック・三菱電機が早く終わった場合の5分照会まで。'}
for c in data['companies']:
 if c['id'] in planned:
  e=next(e for e in events if e.get('company',{}).get('id')==c['id']);status='本日予定';why=f"{e['duration']}分。"+e['note']
 elif c['id']==optional:status='余裕時のみ';why='16:35以降の予備枠が残った場合だけ。移動込み16:50終了を守る。'
 else:
  status='今日は見送る';why=special.get(c['shortName']) or ('青は黄色13社と緑の短時間枠を守るため原則省略。' if c['priority']=='青系' else '優先色未指定のため今回は固定枠を設けない。行く判断自体は保持し、次回・別日候補に残す。' if c['priority']=='未指定' else '黄色を優先し、同エリアでも今日は独立した訪問枠を設けない。')
 dispositions.append({'company':c,'status':status,'why':why})
budget=collections.Counter()
for e in events:budget['黄色訪問' if e.get('company',{}).get('priority')=='黄色' else '緑訪問' if e.get('company') else '移動' if e['kind'] in ['move','transfer'] else e['kind']]+=e['duration']
plan={'date':'2026-10-27','start':'10:00','end':'17:00','assumption':'入場を済ませ、10:00に東1ホールのマザック付近から開始。入口未指定。受付から開始するなら緑枠を削って吸収。','events':events,'dispositions':dispositions,'budget':dict(budget),'delay_rules':[{'minutes':10,'text':'クオリカ10分を省略。'},{'minutes':20,'text':'クオリカとベッコフの計20分を省略。'},{'minutes':30,'text':'緑3社（クオリカ・ベッコフ・TPR）計30分を省略。'},{'minutes':45,'text':'緑3社を省略し、シーメンス10→5分、ハイデンハイン15→10分、たけびし10→5分で計45分を回収。'},{'minutes':60,'text':'45分案に加え、マザック20→10分、モリ15→10分。説明の延長より資料取得を選ぶ。南の三菱電機・Phoxter枠を守る。'}],'gates':['12:15 東8のDMG開始','14:35 南2到着','15:25 南2を切り上げて4Fへ','16:15 南4のPhoxter開始','16:50 新しい商談を始めず退出へ'],'sources':{'index':'https://www.jimtof.org/jp/exhi_search_booth.html','site':'https://jimtof.org/files/site_map_jp.pdf','checked':'2026-10-27'},'limits':['全45社の訪問を前提にしない','移動時間は計画用の仮置きで実測値ではない','個別の実演時刻・待ち時間・担当者在席は未確認','今日見送るは調査対象外や本人の行かない判断へ変更した意味ではない']}
(D/'schedule.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
def clock(m):return f'{m//60:02d}:{m%60:02d}'
def row(e,i):
 c=e.get('company');kind='yellow' if c and c['priority']=='黄色' else 'green' if c else e['kind'];sub=(c['booth']+' ／ '+c['hall']+' ／ '+str(e['duration'])+'分') if c else str(e['duration'])+'分';body='<p>'+H(e['note'])+'</p>'
 if c:
  body+='<p><a href="'+H(c['map'])+'" target="_blank" rel="noopener">公式小間図 ↗</a>　<a href="https://jio-n.github.io/J_research/#stop-'+c['id']+'">訪問一覧・メモ ↗</a></p>'
 return f'<details class="slot {kind}" id="slot-{i}" data-start="{e["start"]}" data-end="{e["end"]}"><summary><span class="time">{clock(e["start"])}<small>–{clock(e["end"])}</small></span><span class="title">{H(e["title"])}<small>{H(sub)}</small></span><span class="arrow">›</span></summary><div class="detail">{body}</div></details>'
agenda=''.join(row(e,i) for i,e in enumerate(events));skipped=''
for status in ['余裕時のみ','今日は見送る']:
 group=[x for x in dispositions if x['status']==status];skipped+=f'<details class="group"><summary>{status}（{len(group)}社）</summary>'
 for x in group:
  c=x['company'];label={'黄色':'黄','緑':'緑','青系':'青','未指定':'優先未指定'}[c['priority']];skipped+=f'<details class="skip-company"><summary>{H(c["shortName"])} <small>{H(c["booth"])}・{label}</small></summary><p>{H(x["why"])}</p></details>'
 skipped+='</details>'
styles='''*{box-sizing:border-box}body{margin:0;background:#f3f6f7;color:#243b48;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Yu Gothic UI",Meiryo,sans-serif;overflow-wrap:anywhere}header{position:sticky;top:0;z-index:10;padding:7px 9px;background:white;border-bottom:1px solid #bdcdd6}.heading{display:flex;justify-content:space-between;align-items:center;gap:5px}h1{font-size:17px;margin:0}.heading a{font-size:13px}a{color:#075f8e}header p{font-size:12px;margin:3px 0;color:#567381}.tools{display:flex;gap:6px;margin-top:5px}.tools button,.tools select{min-height:36px;border:1px solid #afc7d3;background:#f0f6f8;border-radius:4px;padding:5px 7px;color:#214f66;font:inherit;font-size:14px}.tools select{flex:1;min-width:0}main{max-width:850px;margin:auto;padding:6px 8px 25px}.intro{font-size:14px;margin:7px 3px}.intro p{margin:5px 0}.slot{border:1px solid #cedde4;border-top:0;border-left:5px solid #ccd8df;background:white;scroll-margin-top:125px}.slot:first-child{border-top:1px solid #cedde4}.slot.yellow{border-left-color:#d6ba00}.slot.green{border-left-color:#78a65b}.slot.yellow>summary{background:#fffbe5}.slot.green>summary{background:#f3f9ef}.slot.move>summary,.slot.transfer>summary{background:#edf2f6}.slot.break>summary,.slot.buffer>summary,.slot.exit>summary{background:#f6f4ef}.slot>summary{display:grid;grid-template-columns:58px minmax(0,1fr) 10px;gap:7px;align-items:center;padding:7px 8px;min-height:54px;list-style:none;cursor:pointer}.slot>summary::-webkit-details-marker{display:none}.time{font-size:15px;font-weight:650;line-height:1.3}.time small{display:block;font-size:12px;font-weight:400;color:#607888}.title{font-size:15px;font-weight:550;min-width:0}.title small{display:block;font-weight:400;color:#607888;font-size:12px;line-height:1.5}.arrow{color:#557789}.detail{font-size:15px;padding:0 12px 9px}.detail p{margin:9px 0}.now{outline:2px solid #187da2;outline-offset:-2px}.now .title:before{content:'今の枠 ';font-size:12px;color:#08719b}.group{margin-top:10px;padding:0 8px;background:white;border:1px solid #cedde4;border-radius:5px}.group>summary{font-size:15px;font-weight:600;min-height:45px;padding:10px 0;cursor:pointer}.group p{font-size:14px;margin:8px 0}.skip-company{border-top:1px solid #dae4e9}.skip-company>summary{font-size:14px;min-height:44px;padding:8px 0;cursor:pointer}.skip-company small{color:#627d8b}.warning{border-left:3px solid #c98f28;padding-left:10px}.delay{padding:8px 10px;margin:7px 0;background:#fff5df;border:1px solid #d8c59c;border-radius:4px;font-size:14px}#clock{font-variant-numeric:tabular-nums}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;border-bottom:1px solid #d7e1e7;padding:7px}footer{max-width:850px;margin:auto;padding:5px 12px 22px;color:#617988;font-size:12px}@media(min-width:850px){header{padding-left:max(9px,calc((100% - 832px)/2));padding-right:max(9px,calc((100% - 832px)/2))}}'''
rows=''.join(f'<tr><th>{H(k)}</th><td>{v}分</td></tr>' for k,v in [('黄色の訪問',budget['黄色訪問']),('緑の短時間枠',budget['緑訪問']),('移動・階移動・バス待ち',budget['移動']),('昼食・休憩',budget['break']),('遅延吸収',budget['buffer']),('記録・退出',budget['exit'])])
page='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>今日のJIMTOF｜10:00–17:00</title><style>__STYLE__</style></head><body><header><div class="heading"><h1>今日の予定　10:00–17:00</h1><a href="https://jio-n.github.io/J_research/">45社一覧</a></div><p>10/27｜黄色13社＋緑3社。全45社を詰め込まない。</p><div class="tools"><button id="nowBtn" type="button">今の枠へ</button><select id="delay" aria-label="遅延時の省略"><option value="0">遅れたらここで省略案</option><option value="10">10分遅れ</option><option value="20">20分遅れ</option><option value="30">30分遅れ</option><option value="45">45分遅れ</option><option value="60">60分遅れ</option></select></div><p id="clock" aria-live="polite"></p></header><main><div class="intro"><p><strong>基本16社、余裕があればNdotlightを1社追加。</strong>青・西展示棟・優先度未指定は今日は原則見送ります。</p><p class="warning">10:00に東1・マザック付近で開始する前提。受付からなら緑枠を削って吸収。実演・担当者が不在なら長く待たず資料を取得して次へ。</p></div><div id="delayAdvice" class="delay" hidden></div><section id="agenda" aria-label="タイムテーブル">__AGENDA__</section><details class="group"><summary>時間を守るチェックポイント</summary><p>12:15 DMG開始 → 14:35 南2着 → 15:25 南2切上げ → 16:15 南4・Phoxter開始 → 16:50 新しい商談を始めず退出。</p><p>午後の黄色を守るため、午前の緑や一般説明を延ばしません。展示がない黄色に予定時間いっぱい滞在する必要もありません。</p><p>混雑が長い場合は担当者・資料・後日連絡先を確保。実演時刻に合わせた予約は未確認です。</p></details>__SKIPPED__<details class="group"><summary>420分の内訳・前提・出典</summary><table>__BUDGET__<tr><th>合計</th><td>420分</td></tr></table><p>黄色でも8社は20〜25分、3社は15分、2社は10分。緑3社は各10分。移動・待ち・各社滞在は計画上の割当であり実測値ではありません。ブース内の質問は一つの主題に絞ります。</p><p>南3・4は4F。東7→南2は公式会場図の巡回バスを候補にしています。運行・乗り場・待ち時間は当日確認。駅への到着時間は含みません。</p><p>今日見送るという提案で、45社の訪問候補一覧や本人の行く／行かない判断は変更していません。</p><p><a href="https://www.jimtof.org/jp/exhi_search_booth.html">公式小間割図</a> ／ <a href="https://jimtof.org/files/site_map_jp.pdf">公式全体図・移動案内</a></p></details></main><footer>2026-10-27作成。開始地点・実演時刻未指定のため東1開始の案。最短経路の保証ではありません。時刻は日本時間。訪問済みの記録・音声メモは45社一覧へ。</footer><script type="application/json" id="scheduleData">__DATA__</script><script>
'use strict';const data=JSON.parse(document.getElementById('scheduleData').textContent);function currentMinute(){const p=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Tokyo',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date()),v=Object.fromEntries(p.map(x=>[x.type,x.value]));return {date:v.year+'-'+v.month+'-'+v.day,minute:Number(v.hour)*60+Number(v.minute),time:v.hour+':'+v.minute}}function tick(){const n=currentMinute();document.querySelectorAll('.now').forEach(x=>x.classList.remove('now'));if(n.date!==data.date){document.getElementById('clock').textContent='10/27の予定表です';return}const i=data.events.findIndex(e=>e.start<=n.minute&&n.minute<e.end);if(i>=0){document.getElementById('slot-'+i).classList.add('now');document.getElementById('clock').textContent='日本時間 '+n.time+'｜'+data.events[i].title}else document.getElementById('clock').textContent='日本時間 '+n.time+(n.minute<600?'｜10:00開始':'｜本日の予定終了');}document.getElementById('nowBtn').onclick=()=>{tick();(document.querySelector('.now')||document.getElementById('agenda')).scrollIntoView({block:'start',behavior:'smooth'})};document.getElementById('delay').onchange=e=>{const box=document.getElementById('delayAdvice'),rule=data.delay_rules.find(x=>x.minutes===Number(e.target.value));box.hidden=!rule;box.textContent=rule?rule.minutes+'分遅れ：'+rule.text:'';};tick();setInterval(tick,30000);
</script></body></html>'''
page=page.replace('__STYLE__',styles).replace('__AGENDA__',agenda).replace('__SKIPPED__',skipped).replace('__BUDGET__',rows).replace('__DATA__',json.dumps(plan,ensure_ascii=False).replace('<','\\u003c'));(O/'schedule.html').write_text(page,encoding='utf8');print(json.dumps({'events':len(events),'minutes':sum(e['duration'] for e in events),'companies':len(planned),'yellow':len(yellow),'budget':dict(budget),'skip':sum(d['status']=='今日は見送る' for d in dispositions)},ensure_ascii=False))
