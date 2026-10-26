import pathlib,json
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];OLD=R/'data/research/candidate_picker_20261026_235118';O=R/'outputs'/D.name
t=(OLD/'picker_template.html').read_text(encoding='utf8')
def replace(old,new):
 global t
 assert old in t,old[:90]
 t=t.replace(old,new,1)
replace('</style>','.candidate{grid-template-columns:76px minmax(0,1fr)}.decisions{display:grid;grid-template-columns:30px 42px;align-items:start;padding:5px 2px;background:#f0f4f7}.decision{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:48px;font-size:11px;white-space:nowrap;gap:3px;cursor:pointer}.decision input{width:19px;height:19px;margin:0}.candidate.chosen .decisions{background:#e4f0e8}.candidate.rejected{border-left:4px solid #b47970}.candidate.rejected>details>summary{background:#f1eeee}.decision-title{font-size:12px;color:#607986;margin-top:3px}#exportScope{width:100%;padding:9px;border:1px solid #a9c2d0;border-radius:4px;background:white;font:inherit}.export-scope-label{display:block;font-size:14px;margin:8px 0 3px}</style>')
replace('<option value="selected">選択したもの</option><option value="unselected">未選択</option>','<option value="selected">行く</option><option value="rejected">行かない</option><option value="undecided">未判断</option><option value="remaining">行かないを除く</option>')
replace('☑＝訪問候補に採用。行をタップして内容・質問を展開','行く／行かないは片方だけ。両方空欄＝未判断')
replace('チェックは採用候補の選択で、訪問済みとは別です。選択とメモはこのブラウザ内に自動保存。','行く／行かない／未判断を保存します。訪問済みとは別です。判断とメモはこのブラウザ内に自動保存。')
replace('<h2>選択した候補を書き出す</h2><p id="selectionCount"></p>','<h2>候補の判断を書き出す</h2><p id="selectionCount"></p><label class="export-scope-label" for="exportScope">出力対象</label><select id="exportScope"><option value="go">行くのみ</option><option value="remaining">行かないを除く（行く＋未判断）</option><option value="no">行かないのみ</option><option value="all">全件・判断履歴</option></select>')
replace('選択したものだけ表示','行くのみ表示')
replace('選択一覧HTMLを保存','指定対象の一覧HTMLを保存')
replace('選択一覧CSVを保存（Excel用）','指定対象のCSVを保存（Excel用）')
replace('訪問HTML統合用JSONを保存','指定対象の統合用JSONを保存')
replace('全候補＋選択状態のHTMLを保存','全候補＋判断状態のHTMLを保存')
replace('JSONは候補ID・元Excel行・詳細・根拠リンク・自分のメモを含みます。','JSONは行く／行かない／未判断、候補ID・元Excel行・詳細・根拠リンク・自分のメモを含みます。')
replace("const e={selected:x.selected===true,note:","const decision=['go','no','pending'].includes(x.decision)?x.decision:(x.selected===true?'go':'pending');const e={decision,selected:decision==='go',note:")
start=t.index('function selected()');end=t.index('function detail(x)')
t=t[:start]+'''function decision(id){return state[id]?.decision||'pending'}
function selected(){return data.items.filter(x=>decision(x.id)==='go')}
function exportItems(){const scope=document.getElementById('exportScope').value;return data.items.filter(x=>scope==='all'||(scope==='remaining'?decision(x.id)!=='no':decision(x.id)===scope))}
function decisionLabel(id){return {go:'行く',no:'行かない',pending:'未判断'}[decision(id)]}
function counts(){const go=selected().length,no=data.items.filter(x=>decision(x.id)==='no').length,pending=data.items.length-go-no;document.getElementById('selectedBtn').textContent='行く'+go;document.getElementById('selectionCount').textContent='行く '+go+'件／行かない '+no+'件／未判断 '+pending+'件';}
function update(id,patch){const old={decision:'pending',selected:false,note:'',...state[id]};state[id]={...old,...patch,updatedAt:new Date().toISOString()};state[id].selected=state[id].decision==='go';save();counts();const n=document.getElementById('candidate-'+id);if(n){n.classList.toggle('chosen',decision(id)==='go');n.classList.toggle('rejected',decision(id)==='no');for(const cb of n.querySelectorAll('.decisions input'))cb.checked=cb.dataset.decision===decision(id);}}
''' + t[end:]
replace("(mode.value!=='selected'||state[x.id]?.selected)&&(mode.value!=='unselected'||!state[x.id]?.selected)","(mode.value!=='selected'||decision(x.id)==='go')&&(mode.value!=='rejected'||decision(x.id)==='no')&&(mode.value!=='undecided'||decision(x.id)==='pending')&&(mode.value!=='remaining'||decision(x.id)!=='no')")
replace("if(mode.value==='selected')content.append(el('p','selected-summary','選択済み '+selected().length+'件。チェックを外すと採用候補から外れます。'));","if(mode.value==='selected')content.append(el('p','selected-summary','行く '+selected().length+'件'));if(mode.value==='remaining')content.append(el('p','selected-summary','行かないを除いた候補。未判断は行くと確定していません。'));")
start=t.index("row.classList.toggle('chosen',state[x.id]?.selected===true);");end=t.index("const det=el('details','candidate-detail');",start)
t=t[:start]+'''row.classList.toggle('chosen',decision(x.id)==='go');row.classList.toggle('rejected',decision(x.id)==='no');const controls=el('div','decisions');for(const[value,text]of[['go','行く'],['no','行かない']]){const label=el('label','decision'),cb=el('input','');cb.type='checkbox';cb.dataset.decision=value;cb.checked=decision(x.id)===value;cb.setAttribute('aria-label',x.company+' '+x.item+' '+text);cb.addEventListener('change',()=>{update(x.id,{decision:cb.checked?value:'pending'});if(mode.value!=='all')render()});label.append(cb,document.createTextNode(text));controls.append(label);}''' +t[end:]
replace('row.append(label,det);','row.append(controls,det);')
start=t.index('function requireSelection()');end=t.index('function exportHtml(',start)
t=t[:start]+'''function requireSelection(){if(exportItems().length)return true;document.getElementById('exportStatus').textContent='この出力対象に該当する候補はありません。出力対象を変更してください。';return false}
''' +t[end:]
replace('items=onlySelected?selected():data.items','items=onlySelected?exportItems():data.items')
replace("root.querySelector('.top strong').textContent='選択済み候補';root.querySelector('footer').textContent='採用チェックを付けた候補のみを収録した保存版。元Excelの行番号と候補IDを保持しています。';","root.querySelector('.top strong').textContent='出力した候補';root.querySelector('footer').textContent='指定した出力対象の候補を収録。行く／行かない／未判断、元Excelの行番号と候補IDを保持しています。';")
replace("schema:'jimtof2026-selected-candidates/v1'","schema:'jimtof2026-selected-candidates/v2',filterScope:document.getElementById('exportScope').value")
replace("items:selected().map(x=>({...x,selection:state[x.id]}))","items:exportItems().map(x=>({...x,selection:{decision:decision(x.id),selected:decision(x.id)==='go',note:state[x.id]?.note||'',updatedAt:state[x.id]?.updatedAt||''}}))")
replace("'技術URL','出展者URL'","'技術URL','出展者URL','訪問判断'")
replace('for(const x of selected())rows.push','for(const x of exportItems())rows.push')
replace("state[x.id]?.note||'',x.url,x.companyUrl]","state[x.id]?.note||'',x.url,x.companyUrl,decisionLabel(x.id)]")
replace("(onlySelected?'選択候補':'候補選定バックアップ')","(onlySelected?'候補判断一覧':'候補判断バックアップ')")
replace("'JIMTOF2026_選択候補_'","'JIMTOF2026_候補判断_'")
(D/'template.html').write_text(t,encoding='utf8');data=json.loads((OLD/'picker_data.json').read_text(encoding='utf8'));(O/'candidates.html').write_text(t.replace('__PICKER_DATA__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c')),encoding='utf8');print('Built three-state candidate selector; legacy key preserved')
