"""Build a standalone Japanese research report from curated evidence and analysis."""
from pathlib import Path
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/research/evidence_report_20261022'
QUOTES = ROOT / 'data/research/quotation_evidence_20261022'
OUTPUT = ROOT / 'outputs/JIMTOF2026_原文から読む技術潮流_事前調査レポート_20261022.html'
content = json.loads((DATA/'report_content.json').read_text(encoding='utf-8'))
quotes = json.loads((QUOTES/'quotes.json').read_text(encoding='utf-8'))['quotes']
tasks = json.loads((QUOTES/'task_taxonomy.json').read_text(encoding='utf-8'))['tasks']
coverage = json.loads((ROOT/'data/research/deep_reading_20261021/source_coverage.json').read_text(encoding='utf-8'))
additional = {s['id']:s for s in coverage['additional_sources']}
major = json.loads((ROOT/'data/research/macro_20261019/major_dossiers.json').read_text(encoding='utf-8'))
qmap = {q['quote_id']:q for q in quotes}
used = set()
E = html.escape

def refs(ids):
    return '<span class="refs">' + ''.join(f'<a href="#{sid.lower()}" class="ref" title="根拠へ移動">{sid}</a>' for sid in ids) + '</span>'

def quote(qid):
    assert qid not in used, qid
    used.add(qid)
    q = qmap[qid]
    return f'''<figure class="evidence" id="{qid.lower()}" data-tasks="{' '.join(q['task_ids'])}">
<figcaption><span class="quote-label">原文</span> {E(qid)} / {E(q['source_id'])} · {E(q['use_for'])}</figcaption>
<blockquote>{E(q['excerpt_original'])}</blockquote>
<p class="attribution">{E(q['attribution'])}</p>
<p class="source"><a href="{E(q['source_url'],quote=True)}" target="_blank" rel="noopener noreferrer">{E(q['title'])} ↗</a><br>{E(q['published_date'])} · {E(q['locator'])}</p>
<details><summary>文脈・根拠として使える範囲</summary><p><b>文脈〔要約〕</b>　{E(q['context_paraphrase'])}</p><p><b>この一節からは言えないこと</b>　{E(q['not_evidence_for'])}</p><p class="small">{E(q['verification'])} · {E(q['verified_date'])}</p></details></figure>'''

def table(headers, rows, cls=''):
    head=''.join(f'<th scope="col">{E(h)}</th>' for h in headers)
    body=''.join('<tr>'+''.join(f'<td>{cell}</td>' for cell in row)+'</tr>' for row in rows)
    return f'<div class="table-scroll"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

parts=[]
def add(text): parts.append(text)

nav=[('overview','01','まず見える方向性'),('companies','02','主要3社の戦略'),('definition','03','フィジカルAIの基準'),('themes','04','六つの深掘り論点'),('tasks','05','顧客タスクへの配置'),('followups','06','追加11資料の成果'),('visits','07','会場で確かめる問い'),('development','08','顧客向け開発候補'),('evidence-index','09','原文46件の索引'),('appendix','10','補足原文と主要33社')]
navigation=''.join(f'<a href="#{sid}"><span>{num}</span>{name}</a>' for sid,num,name in nav)
add(f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(content['title'])}｜JIMTOF2026</title><style>__CSS__</style></head><body>
<a class="skip" href="#main">本文へ移動</a><aside><p class="brand">JIMTOF<span>2026</span></p><p class="nav-sub">AI・自動化・AX／DX<br>視察前の根拠と論点</p><nav aria-label="目次">{navigation}</nav><button id="print" type="button">印刷 / PDF保存</button><p class="nav-date">整理基準 2026.10.22</p></aside><main id="main">
<header class="hero"><p class="eyebrow">EVIDENCE &amp; TECHNOLOGY OUTLOOK</p><h1>{E(content['title'])}</h1><p class="subtitle">{E(content['subtitle'])}</p><p class="hero-scope">公開資料に基づく事前調査。現地実演を確認した報告ではありません。</p><div class="hero-stats"><span><b>40</b> 元資料の精読</span><span><b>46</b> 原文の短い抜粋</span><span><b>11</b> 追加調査資料</span><span><b>14</b> 顧客タスク分類</span></div></header>
<section id="overview"><p class="section-num">01 / INDUSTRY DIRECTION</p><h2>複数の資料をつなぐと、どの方向が見えるか</h2><p class="lead">個々の機械・ロボットを動かす自動化に、工程設計、条件出し、変更への対応、工程間の調整が加わりつつある。局所の判断を高度化する開発と、その判断を工場全体で使えるようにする開発を、両方見る。</p><p class="scope-note">以下は企業方針・研究・製品説明を比較した分析。業界全体での普及率や、全工程が自律化済みという実績を示すものではない。</p>''')
for i,(title,body,rids) in enumerate(content['takeaways'],1):
    add(f'<div class="thesis"><span class="thesis-number">{i:02}</span><div><h3>{E(title)}</h3><p>{E(body)} {refs(rids)}</p></div></div>')
add('''<figure class="strategy-flow"><figcaption>資料から整理した開発・事業のつながり〔調査仮説〕</figcaption><ol><li><b>現場を捉える</b><span>現象・状況・意図<br>品質・判断・結果</span></li><li><b>判断を作る</b><span>物理モデル・学習<br>経験の再利用・検証</span></li><li><b>仕事を変える</b><span>条件・動作・計画<br>人の承認と実行</span></li><li><b>価値を届ける</b><span>品質・納期・停止損失<br>継続支援と改善</span></li></ol><p>利用結果を次のデータ・モデル・設計へ戻す。各矢印の成立条件を確かめることが調査の中心になる。</p></figure></section>''')

add('<section id="companies"><p class="section-num">02 / STRATEGY COMPARISON</p><h2>主要3社は、異なる資産から同じ課題へ近づく</h2><p>データ基盤、熟練知、実証工場という言葉を、各社が持ち寄る資産と顧客の仕事へ結び直す。共同開発の発表と、会場で見られる製品・実演は照合して判断する。</p>')
for company in content['companies']:
    add(f'<article class="company"><p class="company-name">{E(company["name"])}</p><h3>{E(company["headline"])}</h3><p>{E(company["body"])}</p>')
    add(quote(company['quote']))
    add(f'<p><span class="analysis-label">読み取り</span> {E(company["analysis"])} {refs(company["refs"])}</p><p class="stage"><b>公表段階</b>　{E(company["stage"])}</p></article>')
task_names={t['id']:t['name'] for t in tasks}
add(table(['企業','主に扱う仕事','持ち寄る資産','次に確かめること'],[[E(c['name']),E('／'.join(task_names[tid] for tid in c['tasks'].split('・')))+f'<br><span class="small">{E(c["tasks"])}</span>',E(c['assets']),E(c['question'])] for c in content['companies']]))
add('<p class="scope-note">ファナック／日立の共同提携で先行適用の場になるのは、日立グループの工場。共同実証での改善と、その後の顧客展開を分けて読む。</p></section>')

add('''<section id="definition"><p class="section-num">03 / PHYSICAL AI</p><h2>「フィジカルAIで何があったか」を報告するための基準</h2><p>メーカーの呼称を記録した上で、今回重視する能力を明示する。正式な業界共通定義を決めるのではなく、展示を比較できる作業定義を置く。</p><div class="quote-grid">''')
for qid in ['Q07','Q09','Q21','Q41']:add(quote(qid))
add('''</div><div class="definition"><span class="analysis-label">本調査の作業定義</span><p>センサ等で物理世界の状態を捉え、学習モデルを含むAIが状態・目的に応じて判断や動作を選び、その結果を物理世界で実行する仕組み。そのうち、<strong>条件の変化や不確実性への対応能力を具体的に確認できるもの</strong>を重点的に紹介する。</p></div><p>これは上の資料を組み合わせた調査者の整理。ファナックの発言そのものや一般規格とは区別する。VLA、基盤モデル、世界モデル、模倣学習等は確認する技術項目であり、全てを必須条件にはしない。動作の選び直しと、その場の再学習も別である。</p>''')
add(table(['仮想例〔実際の展示確認ではない〕','どう整理するか','聞くべきこと'],[
 ['同じワークを撮像し、登録済み経路の位置を補正','従来型の自動化でも成立。AIの使用と新規性は別途確認。','認識方式、経路の生成方式、従来製品との差。'],
 ['固定アームでも、姿勢・滑りで把持や再試行を変える','固定設置・同種ワークでも適応能力の候補。','AIが変える判断、失敗検知と復帰、試験条件・介入率。'],
 ['音声で登録済み作業メニューを呼び出す','指示入力の改善。新しい作業への汎化は未確認。','言い換え理解と、新しい動作・手順の生成を分ける。'],
 ['新しい形状や指示に、再教示を抑えて対応する','汎化を主張する候補として比較条件を確認。','初めての範囲、学習データ、調整時間、人の介入。'],
 ['加工信号から推定し、条件を実行中に変える','加工における適応的な判断・実行として調べる。','物理モデルとAIの分担、安定性、適用範囲。']]))
add('''<h3>報告する四つの欄を分ける</h3><ol class="check-list"><li><b>メーカー呼称</b>：原文と発言者を記録。</li><li><b>方式と適応範囲</b>：入力、AIの判断、変える動作、対応する変化。</li><li><b>実機検証</b>：比較条件、成功率・介入率、時間・品質、適用外。</li><li><b>現地確認</b>：実際に見た条件と結果。説明を聞いた範囲も区別。</li></ol><p class="scope-note">四欄を足し合わせて総合点にはしない。「呼称あり／方式は資料記載／比較条件は未確認」のように報告する。フィジカルAIかどうかと、2024年以前から何が進歩したかを別々に評価する。</p></section>''')

add('<section id="themes"><p class="section-num">04 / SIX RESEARCH QUESTIONS</p><h2>原文から、一段深い開発の問いへ</h2><p>各論点を、資料の読み取り、原文、顧客向け開発への示唆、未解決の問いの順に示す。提言は自社の能力・顧客需要を照合する前の候補として扱う。</p>')
for theme in content['themes']:
    add(f'<article class="theme" id="theme-{theme["id"]}"><p class="theme-number">論点 {theme["number"]} <span>{E(theme["tasks"])}</span></p><h3>{E(theme["title"])}</h3>')
    for paragraph,rids in theme['paragraphs']:add(f'<p>{E(paragraph)} {refs(rids)}</p>')
    add('<div class="quote-grid">')
    for qid in theme['quotes']:add(quote(qid))
    add(f'</div><div class="implication"><h4>顧客向け開発への示唆〔仮説〕</h4><p>{E(theme["implication"])}</p></div><p class="question"><b>次に確かめる問い</b><br>{E(theme["question"])}</p></article>')
add('</section>')

add('''<section id="tasks"><p class="section-num">05 / CUSTOMER TASKS</p><h2>技術の名前から、顧客が任せたい仕事へ置き直す</h2><p>工程設計、条件出し、加工中の補正などを縦軸に、技術方式、判断・実行の範囲、データ、成熟度を比較する。AI・エージェント・デジタルツインは手段の軸に置く。</p><div class="process-groups">''')
for title,ids in [('計画・準備',['T01','T02','T03','T04']),('段取り・実行',['T05','T06','T07','T08']),('測定・改善',['T09','T10','T11']),('横断して支える・つなぐ',['T12','T13','T14'])]:
    add(f'<div><h3>{title}</h3><ul>'+''.join(f'<li><a href="#task-{tid.lower()}">{E(next(t["name"] for t in tasks if t["id"]==tid))}</a></li>' for tid in ids)+'</ul></div>')
add('</div>')
rows=[]
for t in tasks:
    rids=[q['quote_id'] for q in quotes if t['id'] in q['task_ids']]
    rows.append([f'<span id="task-{t["id"].lower()}" class="anchor"></span><b>{E(t["id"])}</b><br>{E(t["name"])}<br><span class="small">{E(t["type"])}</span>', E(t['typical_input'])+'<br>↓<br>'+E(t['typical_output']), refs(rids)])
add(table(['タスク','代表的な入力 → 出力','関連する原文'],rows,'tasks-table'))
add('<p class="scope-note">入力・出力は比較の目安であり、全製品の仕様ではない。今回タグを付けたのは46抜粋。既存344技術の全面再分類は未実施。「自律加工」は総称のため、自動化した判断範囲を付記する。</p></section>')

add('<section id="followups"><p class="section-num">06 / FOLLOW-UP FINDINGS</p><h2>追加11資料で、どこまで具体化できたか</h2><p>40資料から生じた問いを、先行サービス・研究・仕様・契約まで追った成果。追加6抜粋のうち5資料はこの11資料と重複し、NVIDIA教材1資料を別途追加している。件数を足し合わせて新規資料数にはしない。</p>')
rows=[]
for sid,finding,meaning,scope in content['followups']:
    s=additional[sid]
    rows.append([f'<span id="{sid.lower()}" class="anchor"></span><b>{sid}</b><br><a href="{E(s["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{E(s["title"][4:])} ↗</a>',f'<b>{E(finding)}</b><br>{E(meaning)}',E(scope)])
add(table(['追加資料・原典','得られた内容と意味','確認範囲・段階'],rows))
add('</section>')

add('<section id="visits"><p class="section-num">07 / ON-SITE QUESTIONS</p><h2>問いから選ぶ、会場での確認先</h2><p>以下は調査の問いと訪問先を対応させた例。主要33社は付録にも一覧化している。ブース情報は保存済みの2026公式出展情報に基づき、収集基準日は10月16日。提携先・研究所が、そのままJIMTOFに出展しているとは扱わない。</p>')
visit_indices=[0,1,4,5,2,6,3,26,25,21]
rows=[]
for i in visit_indices:
    c=major[i]
    rows.append([E(c['target']),E(' / '.join(c['booths'])),E(content['major_questions'][i])+f'<br><a href="{E(c["urls_2026"][0],quote=True)}" target="_blank" rel="noopener noreferrer">公式出展情報 ↗</a>'])
for name,booth,role,question,url in content['special_booths']:
    rows.append([E(name),E(booth),f'<b>{E(role)}</b><br>{E(question)}<br><a href="{E(url,quote=True)}" target="_blank" rel="noopener noreferrer">公式出展情報 ↗</a>'])
add(table(['確認先','ブース〔保存情報〕','聞くこと'],rows))
add('''<div class="question"><b>どのブースでも共通して聞く五つ</b><ol><li>どの仕事で、どの判断・動作を自動化するか。</li><li>何が変わると対応を変えられるか。人が残る作業は何か。</li><li>データ・物理モデル・AI・既存制御をどう分担するか。</li><li>従来方式との比較条件と、時間・品質・介入の結果は何か。</li><li>前後工程へ何を渡し、利用結果を次の改善へどう戻すか。</li></ol></div><p class="scope-note">研究発表にある機能が出展実機へ入っているかを現地で照合する。製品の紹介と共同開発のロードマップを分けて記録する。</p></section>''')

add('<section id="development"><p class="section-num">08 / DEVELOPMENT OPTIONS</p><h2>顧客に嬉しいサービスへ、どこから入るか</h2><p>主軸は顧客の判断・作業を改善するサービスの開発。自社での導入は、顧客向けの適用・評価・データを得る場として位置付けられる。以下は優先順位の確定ではなく、自社能力と顧客需要を照合するための候補である。</p>')
rows=[]
for name,customer,deliverable,existing,condition,rids in content['development']:
    rows.append([f'<b>{E(name)}</b><br>{refs(rids.split("・"))}',E(customer),E(deliverable),E(existing)+'<br><b>着手前の確認：</b>'+E(condition)])
add(table(['開発候補と根拠','困っている顧客の仕事','提供するもの','既存との違い・成立条件'],rows))
add('''<div class="decision"><h3>「差別化の穴」は、現時点では候補</h3><p>まず既存ベンダーの適用範囲と顧客の未充足需要を調べる。新しい名称のモデルを所有することだけでなく、取得しにくい現象、判断理由、品質との対応、顧客条件への適応、効果を検証する手順を持つことが独自性になり得る。</p><p>顧客が支払う改善、既存基盤に任せる部分、自社が得意な部分、運用とデータ利用の条件を揃えてから開発範囲を決める。</p></div></section>''')

add('''<section id="evidence-index"><p class="section-num">09 / VERBATIM INDEX</p><h2>原文46件を、企業・論点・タスクから探す</h2><p>引用は本資料内に各1回掲載。Q番号を押すと該当箇所へ移動する。原文は引用枠、文脈と分析はその外側に分けた。</p><form class="filters" onsubmit="return false"><label>原文・企業・論点<input id="evidence-search" type="search" placeholder="例：データ、判断、ファナック"></label><label>関連タスク<select id="evidence-task"><option value="">すべて</option>''')
add(''.join(f'<option value="{t["id"]}">{t["id"]} {E(t["name"])}</option>' for t in tasks))
add('</select></label><button id="filter-reset" type="button">解除</button><output id="evidence-count" aria-live="polite"></output></form>')
rows=[]
for q in quotes:
    rows.append([f'<a href="#{q["quote_id"].lower()}" class="index-link" data-quote="{q["quote_id"].lower()}" data-tasks="{" ".join(q["task_ids"])}">{q["quote_id"]} / {q["source_id"]}</a>',E(q['attribution']),E(q['use_for'])])
add(table(['原文へ','誰の言葉か','根拠にする論点'],rows,'index-table'))
add('<p id="no-evidence" hidden>条件に合う原文はありません。</p></section>')

add('<section id="appendix"><p class="section-num">10 / APPENDIX &amp; METHOD</p><h2>補足原文・主要企業・調査の範囲</h2><h3>本論を支える補足の原文</h3><p>接続の意味、反復作業と学習の使い分け、計測、学習の実装、継続サービス等。S37は連携窓口の情報であり、技術潮流の証拠とは区別する。</p><details class="appendix-details" id="other-quotes"><summary>補足の原文18件を開く</summary><div class="quote-grid">')
for q in quotes:
    if q['quote_id'] not in used:add(quote(q['quote_id']))
assert len(used)==46
add('</div></details><details class="appendix-details" id="major-companies"><summary>主要33社のブース・確認する問い</summary><p>保存した公式出展情報を土台にした確認リスト。問いは調査者の提案であり、各社がAIを搭載済みという認定ではない。</p>')
rows=[]
for c,question in zip(major,content['major_questions']):
    url=c['urls_2026'][0] if c['urls_2026'] else None
    link=f'<a href="{E(url,quote=True)}" target="_blank" rel="noopener noreferrer">{E(c["target"])} ↗</a>' if url else E(c['target'])
    rows.append([link,E(' / '.join(c['booths'])),E(question)])
add(table(['主要企業','ブース〔保存情報〕','確認する問い'],rows,'major-table'))
add('''</details><h3>どこまで調べ、何がまだ残るか</h3><p>本資料はS01～S40の精読、そこから追った追加11資料、定義用のNVIDIA教材を土台に再編集した。原文の短い抜粋は46件。44件を取得した本文テキスト、2件をPDF画像で照合している。10月21日の取得資料を再利用し、必要箇所を10月22日に追加確認した。引用は各資料の代表的な一節で、重要文を全て抽出し終えたものではない。</p><p>マクロ探索の土台には2024年・2026年の出展者2,427掲載行と、両年に説明文がある同名538件の比較がある。行数はユニーク企業数ではなく、文言比較は業界全体の技術採用率でもない。既存344技術は詳細比較57件、個別タスク整理33件、出展説明からの一次分類254件で確認深度が異なる。</p><p>研究の成果を全加工条件へ一般化せず、発表・研究実証・商品・展示予定・現地確認を区別した。AI単独の収益寄与、各社技術間の完成済み連携、自社の実装能力・顧客の支払意思には未確認点が残る。</p><h3>元データと、追加調査へ引き継ぐ入口</h3><p>原文台帳、個別精読、追加調査のノート、タスク分類は、下記のリポジトリへ保存している。別の調査は入口資料から既存成果と未解決の問いを読み、五つの切り口の担当別指示を使って深掘りできる。</p><ul class="resource-links">
<li><a href="https://github.com/jio-n/J_research/blob/main/RESEARCH_START.md">調査の入口・既存成果物の所在</a></li>
<li><a href="https://github.com/jio-n/J_research/tree/main/data/research/quotation_evidence_20261022">原文台帳・作業定義・14タスク・展示評価票・並行調査指示文</a></li>
<li><a href="https://github.com/jio-n/J_research/tree/main/data/research/deep_reading_20261021">40資料の個別精読と追加11資料のノート</a></li>
<li><a href="https://github.com/jio-n/J_research/blob/main/data/research/strategy_review_20261021/exhibitor_coverage_all_2024_2026.csv">両年の全出展者照合CSV</a></li>
</ul></section><footer><p>JIMTOF2026 事前調査資料 · 整理基準 2026年10月22日</p><p>原文・掲載位置と、資料に基づく要約・分析・仮説を分けて記録。原典の本文全体は再配布していない。<br>このHTMLは単体で閲覧・検索できる。原典やリポジトリを開く場合はインターネット接続が必要。</p><a href="#main">先頭へ戻る ↑</a></footer></main><div id="jump-status" role="status" aria-live="polite" class="sr-only"></div><script>__JS__</script></body></html>''')

CSS='''
:root{--navy:#183b50;--ink:#203e4d;--muted:#58707c;--teal:#087f85;--paper:#f8f7f2;--rule:#d4dfdf;--gold:#a96d15;--wash:#edf5f3;--nav:244px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.9 "Yu Gothic",Meiryo,sans-serif}a{color:#096a77;text-underline-offset:3px}a:hover{color:#a15f08}button,input,select{font:inherit}button{cursor:pointer}aside{position:fixed;inset:0 auto 0 0;width:var(--nav);background:var(--navy);color:#e7f0f0;padding:30px 23px;overflow-y:auto}.brand{font-size:24px;letter-spacing:.08em;margin:0}.brand span{color:#7cdbce;margin-left:5px}.nav-sub{font-size:13px;line-height:1.9;margin:12px 0 26px;color:#c3d8dd}nav{display:grid;gap:3px}nav a{color:#e7f0f0;text-decoration:none;font-size:13px;padding:10px 2px;border-bottom:1px solid #ffffff19}nav a span{color:#89cfc9;margin-right:10px;font-size:11px}nav a:hover,nav a.active{color:#b8f4e5}#print{margin-top:26px;border:1px solid #9ab9c1;border-radius:3px;background:transparent;color:white;font-size:12px;padding:8px 12px}.nav-date{font-size:11px;color:#adc7ce;margin-top:16px}main{margin-left:var(--nav)}.hero,section,footer{padding:46px max(32px,calc((100% - 1040px)/2))}.hero{background:#eaf1ed;border-bottom:1px solid #c9d9d5;padding-top:60px;padding-bottom:42px}.eyebrow,.section-num{font-size:11px;font-weight:700;letter-spacing:.14em;color:var(--teal);margin:0 0 16px}h1{font-size:clamp(30px,3.1vw,45px);line-height:1.5;letter-spacing:.025em;max-width:960px;margin:12px 0 20px}h2{font-size:29px;line-height:1.6;margin:4px 0 24px}h3{font-size:23px;line-height:1.6;margin:18px 0}h4{font-size:16px;margin:0 0 8px}.subtitle{font-size:19px;max-width:800px}.hero-scope{font-size:13px;color:var(--muted)}.hero-stats{display:flex;gap:26px;flex-wrap:wrap;margin-top:28px;font-size:12px}.hero-stats span{display:grid;gap:0}.hero-stats b{font-size:32px;line-height:1.5;font-weight:500;color:var(--navy)}section{border-bottom:1px solid var(--rule);scroll-margin-top:20px}p{margin:15px 0}.lead{font-size:20px;line-height:2}.scope-note{font-size:13px;color:var(--muted);padding-left:14px;border-left:2px solid #a8bbbf}.thesis{display:grid;grid-template-columns:42px 1fr;gap:15px;padding:22px 0;border-bottom:1px solid var(--rule)}.thesis-number{color:var(--teal);font-size:23px;margin-top:16px}.thesis h3{font-size:20px;margin:12px 0}.thesis p{margin:8px 0}.refs{display:inline;white-space:normal}.ref{display:inline-block;font-size:11px;line-height:1.8;padding:0 5px;margin:0 2px 2px;border:1px solid #b8cccf;border-radius:2px;text-decoration:none;vertical-align:baseline}.strategy-flow{margin:34px 0 8px;padding:22px;background:var(--navy);color:#e8f1ef}.strategy-flow figcaption{font-size:13px;margin-bottom:20px}.strategy-flow ol{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:0;padding:0}.strategy-flow li{position:relative;border-top:2px solid #74cec0;padding-top:12px}.strategy-flow li:not(:last-child):after{content:'→';position:absolute;right:-12px;top:8px;color:#81d6c9}.strategy-flow b{display:block;font-size:16px}.strategy-flow span{display:block;font-size:12px;line-height:1.8;color:#c7dcdf;margin-top:7px}.strategy-flow p{font-size:12px;margin-bottom:0;color:#c7dcdf}.company{padding:24px 0 30px;border-bottom:1px solid var(--rule)}.company-name{color:var(--teal);font-weight:bold;font-size:14px;margin-bottom:10px}.company h3{margin-top:5px}.analysis-label{font-size:12px;font-weight:bold;color:#86601f;letter-spacing:.04em}.stage{font-size:13px;color:var(--muted)}.evidence{padding:19px 21px;background:white;border-left:3px solid var(--teal);margin:22px 0;scroll-margin-top:26px;overflow-wrap:anywhere}.evidence figcaption{font-size:12px;color:var(--muted);line-height:1.7}.quote-label{font-size:10px;color:white;background:var(--teal);padding:2px 5px;margin-right:7px}.evidence blockquote{font-size:21px;line-height:1.85;font-weight:600;margin:16px 0;color:#163c4e}.attribution{font-size:14px;margin:8px 0}.source{font-size:12px;color:var(--muted);line-height:1.9;margin:9px 0}.evidence details{font-size:13px;border-top:1px solid var(--rule);padding-top:10px;margin-top:12px}.evidence summary{cursor:pointer;font-size:12px;color:var(--teal)}.evidence details p{margin:10px 0}.small{font-size:12px;color:var(--muted)}.quote-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 22px}.definition,.decision{margin:26px 0;background:#e4efea;padding:24px;border-top:3px solid var(--teal)}.definition p{font-size:20px;font-weight:600;line-height:2;margin:12px 0}.table-scroll{overflow-x:auto;margin:25px 0;width:100%;border-top:2px solid var(--navy)}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.85;text-align:left;min-width:650px}th{background:#e9efed;font-size:12px;color:var(--navy)}th,td{padding:14px 13px;border-bottom:1px solid var(--rule);vertical-align:top}th:first-child,td:first-child{padding-left:10px}tbody tr:nth-child(even){background:#ffffff78}.theme{padding:32px 0 38px;border-top:1px solid var(--rule);margin-top:30px;scroll-margin-top:20px}.theme-number{font-size:14px;font-weight:bold;color:var(--teal)}.theme-number span{display:block;font-size:12px;font-weight:400;color:var(--muted);margin-top:4px}.theme h3{font-size:25px}.implication{border-top:2px solid #b49453;background:#f1ede1;padding:20px 23px;margin-top:20px}.implication p{font-size:15px;line-height:2;margin:8px 0 0}.question{border-left:3px solid #b49453;padding:10px 18px;margin:24px 0;color:#66522d;font-size:15px;line-height:2}.process-groups{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin:26px 0}.process-groups div{border-top:2px solid var(--teal)}.process-groups h3{font-size:15px}.process-groups ul{list-style:none;padding:0;font-size:13px}.process-groups li{margin:8px 0}.tasks-table td:first-child{width:26%}.tasks-table td:nth-child(2){width:36%}.check-list{font-size:15px;line-height:2.1}.filters{display:flex;gap:15px;align-items:end;flex-wrap:wrap;background:#eaf0ec;padding:18px}.filters label{display:grid;gap:6px;font-size:12px}.filters input,.filters select,.filters button{padding:9px;border:1px solid #96afb6;background:white;border-radius:3px;color:var(--ink);font-size:14px;max-width:100%}.filters input{width:260px}.filters select{max-width:320px}.filters output{font-size:12px;padding-bottom:9px}.index-table{min-width:550px}.index-table tr[hidden]{display:none}.index-table td:first-child{white-space:nowrap}.index-table td:nth-child(2){width:47%}.appendix-details{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin:25px 0;padding:15px 0}.appendix-details>summary{font-size:16px;font-weight:bold;cursor:pointer;color:var(--teal)}.resource-links{font-size:14px;line-height:2.2;padding-left:20px}.anchor{scroll-margin-top:30px}footer{font-size:12px;color:var(--muted);background:#eaf0ed}.skip{position:absolute;top:-100px;left:20px;background:white;padding:12px;z-index:20}.skip:focus{top:10px}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.evidence:target{box-shadow:0 0 0 3px #b49453}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #bb822f;outline-offset:4px}
@media(max-width:1100px){:root{--nav:205px}aside{padding:24px 16px}.hero,section,footer{padding-left:28px;padding-right:28px}.quote-grid{grid-template-columns:1fr}.hero-stats{gap:20px}.strategy-flow ol{grid-template-columns:repeat(2,1fr)}.strategy-flow li:nth-child(2):after{content:''}.process-groups{grid-template-columns:repeat(2,1fr)}}
@media(max-width:760px){aside{position:sticky;top:0;z-index:10;width:auto;padding:10px 15px;background:#183b50f5;backdrop-filter:blur(8px);overflow:hidden}.brand,.nav-sub,.nav-date,#print{display:none}nav{display:flex;overflow-x:auto;gap:17px}nav a{flex-shrink:0;font-size:11px;padding:4px 0;border:0}nav a span{margin-right:5px;font-size:10px}main{margin-left:0}.hero,section,footer{padding:32px 20px}.hero{padding-top:35px}h1{font-size:29px}h2{font-size:24px}h3,.theme h3{font-size:21px}body{font-size:16px;line-height:2}.lead{font-size:18px}.subtitle{font-size:16px}.hero-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.hero-stats b{font-size:28px}.thesis{grid-template-columns:30px 1fr;gap:9px}.thesis-number{font-size:18px}.thesis h3{font-size:18px}.strategy-flow{padding:19px 16px}.strategy-flow li:not(:last-child):after{content:''}.strategy-flow b{font-size:14px}.quote-grid{gap:0}.evidence{padding:17px 16px}.evidence blockquote{font-size:19px}.evidence,.anchor,section,.theme{scroll-margin-top:72px}.definition{padding:19px}.definition p{font-size:18px}.filters{padding:15px}.filters label{width:100%}.filters input,.filters select{width:100%;max-width:100%}.question{padding-left:13px}.implication{padding:18px}.table-scroll{margin:20px 0}.process-groups{gap:16px}.process-groups h3{font-size:14px}.index-table{font-size:12px;min-width:490px}th,td{padding:12px 10px}.source{font-size:11px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{@page{size:A4;margin:15mm 13mm}html{scroll-behavior:auto}body{background:white;font-size:10pt;line-height:1.7}aside,.filters,#no-evidence,.skip{display:none}main{margin:0}.hero,section,footer{padding:8mm 0;background:white}h1{font-size:25pt}h2{font-size:19pt;break-after:avoid}h3,.theme h3{font-size:15pt;break-after:avoid}.lead{font-size:12pt}.hero-stats b{font-size:22pt}.hero{border-top:3px solid var(--navy)}section{break-before:page}.evidence{padding:4mm;background:#f5f8f6;break-inside:avoid;border:1px solid #a6bfbd;border-left:3px solid var(--teal);margin:4mm 0}.evidence blockquote{font-size:12pt}.evidence figcaption,.source,.attribution{font-size:8pt}.quote-grid{grid-template-columns:1fr}.table-scroll{overflow:visible}table{min-width:0!important;font-size:8pt;table-layout:fixed}thead{display:table-header-group}tr{break-inside:avoid}th,td{padding:2mm;overflow-wrap:anywhere}.thesis{break-inside:avoid}.thesis h3{font-size:13pt}.strategy-flow{background:#edf4f1;color:var(--ink);padding:5mm;break-inside:avoid}.strategy-flow span,.strategy-flow p{color:var(--ink)}.strategy-flow ol{grid-template-columns:repeat(4,1fr)}.strategy-flow b{font-size:10pt}.strategy-flow span,.strategy-flow p{font-size:8pt}.definition p{font-size:12pt}.process-groups{grid-template-columns:repeat(4,1fr)}.process-groups h3{font-size:10pt}.process-groups ul{font-size:8pt}.implication,.question,.definition,.decision{break-inside:avoid}.theme{padding-top:5mm}.ref{font-size:7pt}.appendix-details>summary{font-size:11pt}.small,.scope-note{font-size:8pt}.index-table tr[hidden]{display:table-row}footer{font-size:8pt}.resource-links{font-size:9pt}}
'''
JS='''
const rows=Array.from(document.querySelectorAll('.index-table tbody tr'));
const search=document.querySelector('#evidence-search'),task=document.querySelector('#evidence-task');
function filterEvidence(){const words=search.value.trim().toLowerCase().split(/\\s+/).filter(Boolean);let count=0;for(const row of rows){const link=row.querySelector('[data-quote]');const figure=document.getElementById(link.dataset.quote);const text=(row.textContent+' '+figure.textContent).toLowerCase();const show=words.every(w=>text.includes(w))&&(!task.value||link.dataset.tasks.split(' ').includes(task.value));row.hidden=!show;if(show)count++}document.querySelector('#evidence-count').textContent=count+' / '+rows.length+' 件';document.querySelector('#no-evidence').hidden=count>0}
search.addEventListener('input',filterEvidence);task.addEventListener('change',filterEvidence);document.querySelector('#filter-reset').addEventListener('click',()=>{search.value='';task.value='';filterEvidence()});filterEvidence();
function revealTarget(hash){const target=document.getElementById(decodeURIComponent(hash.slice(1)));if(!target)return;let parent=target.parentElement;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement}requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));if(target.classList.contains('evidence'))document.querySelector('#jump-status').textContent=target.id.toUpperCase()+' の原文へ移動しました'}
document.addEventListener('click',event=>{const link=event.target.closest('a[href^="#"]');if(link&&link.hash){event.preventDefault();history.pushState(null,'',link.hash);revealTarget(link.hash)}});window.addEventListener('hashchange',()=>revealTarget(location.hash));if(location.hash)revealTarget(location.hash);
document.querySelector('#print').addEventListener('click',()=>window.print());
let printState=[];window.addEventListener('beforeprint',()=>{printState=Array.from(document.querySelectorAll('details')).map(d=>[d,d.open]);for(const [d] of printState)d.open=true});window.addEventListener('afterprint',()=>{for(const [d,state] of printState)d.open=state});
const navLinks=Array.from(document.querySelectorAll('nav a'));const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){for(const link of navLinks)link.classList.toggle('active',link.hash==='#'+entry.target.id)}}},{rootMargin:'-10% 0px -70% 0px'});for(const section of document.querySelectorAll('main>section'))observer.observe(section);
'''
page=''.join(parts).replace('__CSS__',CSS).replace('__JS__',JS)
OUTPUT.write_text(page,encoding='utf-8',newline='\n')
inputs=[DATA/'report_content.json',QUOTES/'quotes.json',QUOTES/'task_taxonomy.json',ROOT/'data/research/deep_reading_20261021/source_coverage.json',ROOT/'data/research/macro_20261019/major_dossiers.json']
provenance={'date':'2026-10-22','purpose':'既存の原文・精読・追加調査を、単体で読めるHTMLレポートへ再編集。新規のWeb調査ではない。','quote_count':len(quotes),'quote_placements':len(used),'additional_followup_count':len(additional),'major_company_count':len(major),'tasks':len(tasks),'inputs':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'output':{'path':OUTPUT.relative_to(ROOT).as_posix(),'bytes':OUTPUT.stat().st_size,'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest()},'scope':'原文は各1回。引用・文脈要約・分析・開発仮説を区別。現地確認前。'}
(DATA/'provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'html':str(OUTPUT),'quotes':len(used),'bytes':OUTPUT.stat().st_size},ensure_ascii=False))
