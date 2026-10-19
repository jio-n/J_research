"""Priority comparison and candidate disposition sections for the local atlas."""
import html,json
H=lambda value:html.escape(str(value),quote=True)

def roles_section(rows,defs,cards):
 by={c['card_id']:c for c in cards}
 parts=['<section id="ai-human"><h2>訪問優先28社：AIの判断・実行と、人が担う仕事</h2><p>33展示を同じ観点で比較しました。26社は企業・開発元の補足公式資料で照合。ツールディスカバリーとユシロALFREDは公式出展説明までで、補足の技術資料は未確認です。<b>公式</b>は資料の説明、<b>分析・推論</b>は調査者の解釈、<b>未記載</b>は公開資料では確認できなかった点です。</p><p class="note">AIが案を出すこと、ソフトがデータを書き込むこと、ロボットが実機を動かすことを分離しています。人の承認が未記載の場合、無承認で実行できるとは扱いません。国外の運用試験、製品説明、JIMTOFの展示予定も区別します。</p><div class="filters"><select id="roles-category" aria-label="AIと人の役割をカテゴリーで絞る"><option value="">全カテゴリー</option>'+''.join(f'<option value="{d["category_id"]}">{H(d["category"])}</option>' for d in defs)+'</select><input id="roles-query" aria-label="AIと人の役割を検索" placeholder="企業・展示・判断・承認・2024年の差分を検索"></div><p id="roles-count" class="muted"></p><div class="scroll"><table><thead><tr>'+''.join('<th>'+s+'</th>' for s in ['企業・展示・ブース','入力とAIの判断','機械・ソフトの実行','人の事前準備','人の承認・例外対応','2024からの差分','確認できていないこと・原典'])+'</tr></thead><tbody>']
 for r in rows:
  categories=[t['category_id'] for t in by[r['card_id']]['categories']]
  parts.append(f'<tr class="role-row" data-role-categories="{H(json.dumps(categories))}" data-search="{H(json.dumps(r,ensure_ascii=False))}"><td><strong class="priority-company">{H(r["company"])}</strong><p class="booth-label">{H("・".join(r["booths_2026"]))}</p><a href="#{r["card_id"]}">{H(r["item"])}</a><p class="small muted">{H(r["ai_scope"])}</p></td><td><b>入力</b><p>{H(r["ai_input"])}</p><b>判断・提案</b><p>{H(r["ai_judgment"])}</p></td><td>{H(r["execution"])}</td><td>{H(r["human_preparation"])}</td><td><b>承認</b><p>{H(r["human_approval"])}</p><b>例外対応</b><p>{H(r["human_exception"])}</p></td><td><b>2024の基準</b><p>{H(r["baseline_2024"])}</p><b>差分の扱い</b><p>{H(r["delta_interpretation"])}</p><span class="tag">{H(r["delta_type"])}</span></td><td>{H(r["limits"])}<p class="small">{H(r["source_status"])}</p>'+''.join(f'<a class="chip" href="#{eid}">{eid}</a>' for eid in r['evidence_ids'])+'</td></tr>')
 parts.append('</tbody></table></div><p><a href="../data/research/technology_atlas_v1/priority_deepening.csv">判断・実行・人の関与の比較CSV</a> ／ Excelは「カテゴリー別訪問優先」のS〜X列、「展示詳細」のV〜AB列に追加。従来の方式・出力・人の境界・年度比較も更新しています。</p></section>')
 return ''.join(parts)

ROLES_JS='''const rolesCategory=document.querySelector('#roles-category'),rolesQuery=document.querySelector('#roles-query');
function filterRoles(){const companies=new Set();let n=0;document.querySelectorAll('.role-row').forEach(r=>{r.hidden=!!((rolesCategory.value&&!JSON.parse(r.dataset.roleCategories).includes(rolesCategory.value))||!r.dataset.search.toLocaleLowerCase().includes(rolesQuery.value.toLocaleLowerCase()));if(!r.hidden){n++;companies.add(JSON.parse(r.dataset.search).company)}});document.querySelector('#roles-count').textContent=companies.size+'社・'+n+'展示の判断・実行・人の関与'}
rolesCategory.addEventListener('change',filterRoles);rolesQuery.addEventListener('input',filterRoles);filterRoles();
'''

def priority_section(rows,defs):
 parts=['<section id="priorities"><h2>カテゴリー別：どこから見に行くか</h2><p>9カテゴリー・37件の訪問順案（企業はカテゴリー間で重複）。具体的な作業、2024との比較、異なる方式を見比べる価値、未確認点を現地で解消できるかを重視しました。性能・普及率のランキングではありません。カテゴリー内の番号順にご覧ください。</p><div class="filters" id="priority-results"><select id="priority-category" aria-label="訪問優先リストのカテゴリー"><option value="">全カテゴリー</option>'+''.join(f'<option value="{d["category_id"]}">{H(d["category"])}</option>' for d in defs)+'</select></div><p id="priority-count" class="muted"></p><div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['カテゴリー・順番','企業・ブース・展示','先に見る理由','2024 → 2026','差分の読み方・提供段階','現地で確かめること'])+'</tr></thead><tbody>']
 for r in rows:
  links=''.join(f'<a class="chip" href="#{cid}">{cid}：詳細カード</a>' for cid in r['card_ids'])
  parts.append(f'<tr class="priority-row" data-priority-category="{r["category_id"]}" id="{r["priority_id"]}"><td>{H(r["category"])}<br><strong>{r["category_order"]} · {H(r["priority"])}</strong></td><td><strong class="priority-company">{H(r["company"])}</strong><p class="booth-label">{H("・".join(r["booths_2026"]))}</p>{H(r["exhibits"])}{links}</td><td>{H(r["why_visit"])}</td><td><b>2024</b><p>{H(r["baseline_2024"])}</p><b>2026</b><p>{H(r["observation_2026"])}</p></td><td><b>{H(r["delta_type"])}</b><p>{H(r["comparison_interpretation"])}</p><span class="small muted">{H(r["product_stage"])}<br>{H(r["exhibition_status"])}</span></td><td>{H(r["on_site_check"])}</td></tr>')
 parts.append('</tbody></table></div><p><a href="JIMTOF2026_カテゴリー別出展索引_v1.xlsx">Excelの訪問優先シート</a> ／ <a href="../data/research/technology_atlas_v1/category_visit_priorities.csv">訪問優先CSV</a></p></section>')
 return ''.join(parts)

def screening_section(rows):
 parts=['<section id="screening"><h2>関連候補345掲載の仕分け履歴</h2><p>2026の凍結候補集合（342名称キー）を一次仕分け。従来の重点47掲載に加え、残り298掲載から265掲載へカテゴリーを追加。32掲載は語の一致・供給先用途等で対象外、1掲載は具体機能不足で保留。55掲載の周辺部品・機構は、完成システムのAI機能と分けています。追加の年度全文照合は19掲載で実施し、それ以外の機能差は未判定です。</p><details><summary>全掲載の判定・理由・原典を開く</summary><div class="filters"><input id="screening-query" aria-label="候補仕分けを検索" placeholder="企業・判定・ブースを検索"></div><div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in ['企業','2026ブース','判定','理由','カード・原典'])+'</tr></thead><tbody>']
 for r in rows:
  parts.append(f'<tr class="screening-row" data-search="{H(json.dumps(r,ensure_ascii=False))}"><td>{H(r["company"])}</td><td>{H(r["booth"])}</td><td>{H(r["disposition"])}</td><td>{H(r["reason"])}</td><td>'+''.join(f'<a class="chip" href="#{cid}">{cid}</a>' for cid in r['card_ids'])+f'<a href="{H(r["url"])}" target="_blank" rel="noopener">2026原典</a></td></tr>')
 parts.append('</tbody></table></div></details><p><a href="../data/research/technology_atlas_v1/candidate_screening.csv">仕分け履歴CSV</a>（Excelにも候補仕分けシートあり）</p></section>')
 return ''.join(parts).replace('追加の年度全文照合は19掲載で実施し、それ以外の機能差は未判定です。','追加19掲載を重点整理。両年原典比較13掲載（同名12＋公式社名変更照合1）、未照合6掲載。それ以外の機能差は未判定です。')

PRIORITY_JS='''const priorityCategory=document.querySelector('#priority-category');
function filterPriorities(){let n=0;document.querySelectorAll('.priority-row').forEach(r=>{r.hidden=!!(priorityCategory.value&&r.dataset.priorityCategory!==priorityCategory.value);if(!r.hidden)n++});document.querySelector('#priority-count').textContent=n+'件の訪問順案を表示（企業はカテゴリー間で重複）'}
priorityCategory.addEventListener('change',filterPriorities);filterPriorities();
document.querySelector('#screening-query').addEventListener('input',e=>document.querySelectorAll('.screening-row').forEach(r=>r.hidden=!r.dataset.search.toLocaleLowerCase().includes(e.target.value.toLocaleLowerCase())));
'''
