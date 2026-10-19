"""Task directory, company year comparisons and a map from the same memberships."""
import html,json
from report_matrix import prepare as prepare_matrix, build as build_matrix, STYLE as MATRIX_STYLE, script as matrix_script
H=lambda s:html.escape(str(s))
STYLE='''
.directory-grid,.year-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;align-items:start}
.directory-view main,.directory-view .bar,.directory-view nav{max-width:2200px}
.directory-view main{padding-left:24px;padding-right:24px}
.directory-grid{gap:20px}
.directory-grid .company-head h3{overflow-wrap:anywhere}
.directory-grid .company-head{border-left:6px solid #225b92}.directory-grid .company-head h3{font-size:25px}
.directory-grid .target{font-size:20px}.catalog-links{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.catalog-links a,.company-chips a{font-size:13px;padding:5px 9px;border:1px solid #b9ccdf;border-radius:4px;background:#f5f9ff;text-decoration:none}
.company-chips{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0}.company-chips a{background:white}
.catalog-note{padding:14px 18px;background:#fff4df;color:#77551d;border-left:4px solid #c69238;margin:14px 0}
.catalog-detail{margin-top:18px;padding-top:12px;border-top:1px solid #dce3ec}.catalog-detail p{font-size:14px}
.pager{display:flex;gap:16px;align-items:center;margin:25px 0}.pager button{background:white;border:1px solid #b9ccdf;border-radius:4px;color:#225b92;padding:8px 18px}.pager button:disabled{opacity:.35;cursor:default}
.year-grid{grid-template-columns:1fr}.year-pair{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:18px 0}.year-pair>div{background:#f3f6fa;padding:20px;border-top:4px solid #90a7be}.year-pair>div+div{background:#eef5fc;border-color:#225b92}.year-pair h3{font-size:19px}.year-pair p{font-size:15px}
.map-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;align-items:start}.map-grid .map-card{border-top-width:6px}.map-flow{display:grid;grid-template-columns:1fr 1fr;gap:15px}.map-flow>p{background:#f3f6fa;padding:13px;font-size:15px;margin-bottom:0}.map-flow b{display:block;color:#225b92;font-size:12px}.coverage{padding:18px 23px;background:#e8f0f8;margin-bottom:24px}.empty-state{padding:25px;background:white;border:1px solid #c6d4e2}
@media(min-width:1200px){.directory-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(min-width:1800px){.directory-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:900px){.map-grid{grid-template-columns:1fr}}
@media(max-width:700px){.directory-grid,.year-pair,.map-flow{grid-template-columns:1fr}.directory-view main{padding-left:16px;padding-right:16px}}
'''
STYLE+=MATRIX_STYLE

def build(d):
 matrix=prepare_matrix(d);d['_matrix_view']=matrix
 cat=d['catalog'];entries=cat['entries'];topics=cat['topics'];s=cat['scope'];ev={e['evidence_id']:e for e in cat['evidence']};bytopic={t['topic_id']:t for t in topics}
 domains={x['id']:x['short'] for x in d['domains']};domains['D0']='分類保留'
 def links(c,y=None):
  p=[]
  for year in ([y] if y else [2026,2024]):
   urls=c['exhibitor_urls_'+str(year)]
   p += [f'<a href="{H(u)}" target="_blank" rel="noopener">JIMTOF{year} 出展ページ'+(f' {n+1}' if len(urls)>1 else '')+' ↗</a>' for n,u in enumerate(urls)]
   if not urls and y:p.append(f'<span class="meta">{year}出展ページの比較資料なし</span>')
  if not y and not c['exhibitor_urls_2026']:p.append('<span class="meta">2026展示の個別記載は未確認。公式製品資料による補足。</span>')
  return '<div class="catalog-links">'+''.join(p)+'</div>'
 def provenance(c):
  return '<details class="catalog-detail"><summary>公式資料・該当箇所・確認事項</summary>'+''.join(f'<p><a href="{H(ev[i]["url"])}" target="_blank" rel="noopener">{H(ev[i]["title"])} ↗</a><br><span class="meta">{H(i)}　確認 {H(ev[i]["checked_date"])}<br>{H(ev[i]["locator"])}</span></p>' for i in c['evidence_ids'])+f'<p>{H(c["exhibition_status"])} ／ {H(c["product_stage"])}</p><p class="meta">{H(c["classification"])}</p></details>'
 def heading(c):
  item=c['item'];short=item if len(item)<110 else item[:107]+'…'
  return f'<div class="company-head"><span class="badge">{H(c["depth"])}</span><h3>{H(c["company"])}</h3><div class="product" title="{H(item)}">{H(short)}</div><span class="booth">ブース {H(" / ".join(c["booths"])) or "未確認"}</span></div>'
 def attrs(c):
  return f'data-topics="{H(" ".join(c["topic_ids"]))}" data-domains="{H(" ".join(c["domain_ids"]))}" data-company="{H(c["company_key"])}" data-id="{c["card_id"]}" data-search="{H(" ".join([c["card_id"],c["company"],c["item"],c["target"],c["technology"]," ".join(c["booths"])]).lower())}"'
 def companycard(c):
  tech=c['technology'];raw=tech.startswith('原典抜粋：');brief=tech.removeprefix('原典抜粋：')
  if raw and len(brief)>210:brief=brief[:210]+'…'
  target=c['target'] if len(c['target'])<110 else ' ／ '.join(bytopic[i]['title'] for i in c['topic_ids'][:3])
  return f'<article class="company-card directory-card" {attrs(c)}>{heading(c)}<div class="company-body"><div class="field-label">対象の仕事〈用途整理〉</div><p class="target">{H(target)}</p><div class="field"><div class="field-label">使う技術・展示内容 <span class="badge">公式説明の抜粋・要約</span></div><p>{H(brief)}</p></div>'+ (f'<p class="catalog-note">{H(c["related_note"])}</p>' if c['related_note'] else '')+f'<p class="meta small">{H(c["exhibition_status"])}</p>'+links(c)+f'<a class="small" href="#years/{c["card_id"]}">この企業・技術の2024／2026年を対照する →</a><details class="catalog-detail"><summary>解決したい負担・人の役割・年度差を見る</summary><p><span class="badge analysis">ニーズの分析</span>{H(c["need"])}</p><p><b>人の役割・未確認</b><br>{H(c["human_boundary"])}</p><p><b>年度差</b><br>{H(c["year_change"])}</p><p><b>展示名</b><br>{H(c["item"])}</p><p><b>技術説明</b><br>{H(tech)}</p></details>'+provenance(c)+'</div></article>'
 options='<option value="ALL">全テーマ</option>'+''.join(f'<option value="{t["topic_id"]}">{H(t["title"])}（{t["company_count"]}社・{t["row_count"]}カード）</option>' for t in topics)
 def pager(kind):return f'<div class="pager"><button type="button" id="{kind}-prev">前へ</button><span id="{kind}-page"></span><button type="button" id="{kind}-next">次へ</button></div>'
 directory=f'<section data-panel="cases" hidden><h1>技術から企業・展示を探す</h1><p class="lead">代表例の件数で絞らず、取得済みの関連候補を並べています。分野・技術を選び、企業のパネルから公式出展ページへ進めます。</p><div class="coverage">{s["directory_rows"]}カード／{s["company_name_keys"]}企業名キー。うち{len(s["pending_card_ids"])}カードは用途分類を保留。複数テーマへの重複と、同一企業の別展示・別掲載を含みます。<br><span class="small">詳細比較57事例と、出展説明の一次分類では調査の深さが異なります。AI機能と周辺のDX・自動化を同じものとは扱いません。</span></div><div class="toolbar"><select id="catalog-domain" aria-label="分野"><option value="ALL">全分野</option>'+''.join(f'<option value="{k}">{H(v)}</option>' for k,v in domains.items())+f'</select><select id="topic-choice" aria-label="技術テーマ">{options}</select><input id="case-search" placeholder="選択中の分野・テーマから企業・技術・ブースを検索" aria-label="企業・技術検索"></div><div class="topic-intro" id="catalog-intro"></div><p id="case-count" class="meta" aria-live="polite"></p><div class="directory-grid">'+''.join(companycard(c) for c in entries)+'</div><p id="catalog-empty" class="empty-state" hidden>該当する候補がありません。分野・テーマ・検索語を変更してください。</p>'+pager('catalog')+'<p class="small"><a href="../data/research/report_v0/technology_directory.csv">全対応行のCSV</a> ／ <a href="../data/research/report_v0/case_comparison.csv">詳細比較57事例のCSV</a></p></section>'
 # Every map count and company chip is derived from the directory above.
 maps='<section data-panel="map" hidden><h1>仕事から見る、技術全体マップ</h1><p class="lead">何を対象に、どの技術で負担を減らすか。その仕事に関連する企業を、同じ索引につないでいます。</p><p class="meta">ニーズと用途の分類は分析。企業の関連づけは保存済み公式説明に基づきます。全業界の市場地図・シェアではありません。AX／DX・自動化・自律化は複数の仕事にまたがります。</p>'+build_matrix(matrix,H)+'<div data-matrix-mode="cards" hidden><div class="pills">'+''.join(f'<a href="#map/cards/{k}" data-map-choice="{k}">{H(v)}</a>' for k,v in {'ALL':'全分野',**domains}.items())+'</div><div class="map-grid">'
 for t in topics:
  rows=[c for c in entries if t['topic_id'] in c['topic_ids']];companies={}
  for c in rows:companies.setdefault(c['company_key'],c)
  chips=''.join(f'<a href="#years/{c["card_id"]}">{H(c["company"])}</a>' for c in companies.values())
  maps+=f'<article class="map-card" data-map-domain="{t["domain_id"]}"><p class="meta">{H(domains[t["domain_id"]])}　{t["company_count"]}社・{t["row_count"]}カード</p><h2>{H(t["title"])}</h2><div class="map-flow"><p><b>対象の仕事・減らしたい負担〈分析〉</b>{H(t["problem"])}</p><p><b>使われる技術・解決の手段</b>{H(t["technology"])}</p></div><details><summary>関連する{t["company_count"]}社を表示</summary><div class="company-chips">{chips}</div><p class="small">企業名は当該企業の最初の該当カードへ。複数の展示は下の一覧から確認できます。</p></details><a class="more" href="#cases/{t["topic_id"]}">このテーマの企業・展示をすべて見る →</a></article>'
 maps+='</div></div></section>'
 names={}
 for c in entries:names.setdefault(c['company_key'],c['company'])
 years=f'<section data-panel="years" hidden><h1>企業・技術ごとの2024／2026年比較</h1><p class="lead">同じ企業の説明を並べ、何が変わったか、何がまだ判断できないかを分けて読みます。</p><p class="catalog-note">両年の出展説明があるだけでは、同じ製品の性能向上を確認したことにはなりません。2024年に記載がないことを、新発明の根拠にはしません。一次分類のカードは機能差の判定を保留しています。</p><div class="toolbar"><select id="year-company" aria-label="企業"><option value="ALL">全企業</option>'+''.join(f'<option value="{H(k)}">{H(v)}</option>' for k,v in sorted(names.items(),key=lambda x:x[1]))+'</select><select id="year-status" aria-label="比較の深さ"><option value="ALL">すべての比較段階</option>'+''.join(f'<option>{H(x)}</option>' for x in dict.fromkeys(c['year_status'] for c in entries))+'</select><input id="year-search" placeholder="企業・技術・カードIDを検索" aria-label="年度比較を検索"></div><p id="year-count" class="meta" aria-live="polite"></p><div class="year-grid">'
 for c in entries:
  years+=f'<article class="company-card year-card" {attrs(c)} data-status="{H(c["year_status"])}">{heading(c)}<div class="company-body"><p class="target">{H(c["target"])}</p><span class="badge">{H(c["year_status"])}</span><div class="year-pair"><div><h3>2024年の説明・基準点</h3><p>{H(c["baseline_2024"])}</p>{links(c,2024)}</div><div><h3>2026年の説明・展示予定</h3><p>{H(c["observation_2026"])}</p>{links(c,2026)}</div></div><div class="field"><div class="field-label">差分の読み方・比較の限界 <span class="badge analysis">比較分析</span></div><p>{H(c["year_change"])}</p></div><p class="small">関連テーマ：'+ ' ／ '.join(f'<a href="#cases/{i}">{H(bytopic[i]["title"])}</a>' for i in c['topic_ids'])+'</p>'+provenance(c)+'</div></article>'
 years+='</div><p id="year-empty" class="empty-state" hidden>該当する比較カードがありません。条件を変更してください。</p>'+pager('year')+'</section>'
 return directory,maps,years

JS='''
const directoryCards=[...document.querySelectorAll('.directory-card')],yearCards=[...document.querySelectorAll('.year-card')];
let catalogPage=0,yearPage=0;
function pageCards(rows,kind,page){const pages=Math.max(1,Math.ceil(rows.length/12));page=Math.max(0,Math.min(page,pages-1));rows.forEach((c,i)=>c.hidden=i<page*12||i>=(page+1)*12);document.getElementById(kind+'-prev').disabled=page===0;document.getElementById(kind+'-next').disabled=page===pages-1;document.getElementById(kind+'-page').textContent=(page+1)+' / '+pages+' ページ';return page}
function filterCases(reset=true){if(reset)catalogPage=0;const q=document.getElementById('case-search').value.toLocaleLowerCase(),tid=document.getElementById('topic-choice').value,did=document.getElementById('catalog-domain').value;directoryCards.forEach(c=>c.hidden=true);const rows=directoryCards.filter(c=>(tid==='ALL'||c.dataset.topics.split(' ').includes(tid))&&(did==='ALL'||c.dataset.domains.split(' ').includes(did))&&c.dataset.search.includes(q));catalogPage=pageCards(rows,'catalog',catalogPage);document.getElementById('case-count').textContent=new Set(rows.map(c=>c.dataset.company)).size+'社・'+rows.length+'カード（12件ずつ表示）';document.getElementById('catalog-empty').hidden=rows.length!==0;const t=catalogTopics.find(t=>t.topic_id===tid),intro=document.getElementById('catalog-intro');intro.replaceChildren();const title=document.createElement('h2'),need=document.createElement('p'),tech=document.createElement('p');title.textContent=t?t.title:'全テーマの関連候補';need.textContent=t?'減らしたい負担〈分析〉：'+t.problem:'個別の仕事はテーマを選ぶと確認できます。分類保留のカードも一覧に残しています。';tech.textContent=t?'手段：'+t.technology:'一次分類は、機能・適用範囲・人の関わりを深掘り済みという意味ではありません。';intro.append(title,need,tech)}
function filterYears(reset=true){if(reset)yearPage=0;const q=document.getElementById('year-search').value.toLocaleLowerCase(),co=document.getElementById('year-company').value,st=document.getElementById('year-status').value;yearCards.forEach(c=>c.hidden=true);const rows=yearCards.filter(c=>(co==='ALL'||c.dataset.company===co)&&(st==='ALL'||c.dataset.status===st)&&c.dataset.search.includes(q));yearPage=pageCards(rows,'year',yearPage);document.getElementById('year-count').textContent=new Set(rows.map(c=>c.dataset.company)).size+'社・'+rows.length+'比較カード';document.getElementById('year-empty').hidden=rows.length!==0}
document.getElementById('topic-choice').onchange=e=>{if(location.hash==='\x23cases/'+e.target.value)filterCases();else location.hash='cases/'+e.target.value};document.getElementById('case-search').oninput=()=>filterCases();document.getElementById('catalog-domain').onchange=()=>{const select=document.getElementById('topic-choice'),domain=document.getElementById('catalog-domain').value;[...select.options].forEach(o=>o.hidden=domain!=='ALL'&&o.value!=='ALL'&&!catalogTopics.some(t=>t.topic_id===o.value&&t.domain_id===domain));select.value='ALL';filterCases()};
['year-company','year-status'].forEach(id=>document.getElementById(id).onchange=()=>filterYears());document.getElementById('year-search').oninput=()=>filterYears();
['catalog','year'].forEach(kind=>['prev','next'].forEach(dir=>document.getElementById(kind+'-'+dir).onclick=()=>{if(kind==='catalog'){catalogPage+=dir==='next'?1:-1;filterCases(false)}else{yearPage+=dir==='next'?1:-1;filterYears(false)}window.scrollTo(0,0)}));
'''

def route_extension(d):
 payload=json.dumps([{k:t[k] for k in ['topic_id','title','problem','technology','domain_id']} for t in d['catalog']['topics']],ensure_ascii=False).replace('<','\\u003c')
 return 'const catalogTopics='+payload+';\n'+JS+'\n'+matrix_script(d['_matrix_view'])
