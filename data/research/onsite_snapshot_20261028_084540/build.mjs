import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';

const root=process.cwd();
const stamp='20261028_084540';
const here=path.join(root,'data/research/onsite_snapshot_'+stamp);
const out=path.join(root,'outputs/onsite_snapshot_'+stamp);
const {marked}=await import(pathToFileURL('C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js'));
marked.setOptions({gfm:true,breaks:false});
if(fs.existsSync(out)) throw new Error('New output folder already exists');
for(const d of ['', 'raw','notes','data','evidence/photos','assets']) fs.mkdirSync(path.join(out,d),{recursive:true});
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rel=p=>path.relative(root,p).split(path.sep).join('/');
const write=(p,s)=>fs.writeFileSync(path.join(out,p),s,{encoding:'utf8',flag:'wx'});
const sources=[];
const mapping=new Map();
function copy(src,dst,role){
 const a=path.resolve(root,src),b=path.join(out,dst); fs.copyFileSync(a,b,fs.constants.COPYFILE_EXCL);
 const bytes=fs.readFileSync(a); if(hash(bytes)!==hash(fs.readFileSync(b))) throw new Error('Copy mismatch');
 sources.push({source:rel(a),copy:dst,role,sha256:hash(bytes),unchangedBytes:true});mapping.set(a,dst);return bytes.toString('utf8');
}
const old=JSON.parse(fs.readFileSync(path.join(root,'data/research/hearing_raw_20261027_175238/hearing_records.json'),'utf8'));
const records=old.records.map(r=>{
 const rawFile=`data/research/hearing_raw_20261027_175238/raw/${r.id}.txt`;
 const raw=copy(rawFile,`raw/${r.id}.txt`,r.id==='U001'?'企業未確定の断片':'現地ヒアリング原文');
 return {id:r.id,company:r.company,booth:r.booth,area:r.area,type:r.id==='U001'?'未確定の断片':'現地ヒアリング',status:r.id==='U001'?'訪問実績に含めない':r.status,source:rawFile,raw,sha256:hash(Buffer.from(raw)),url:r.companyUrl||null};
});
const un=old.unassigned||old.unassignedRecords||[];
if(!records.some(r=>r.id==='U001')) records.push({id:'U001',company:'企業未確定',booth:'未確定',area:'未確定',type:'未確定の断片',status:'訪問実績に含めない',source:'data/research/hearing_raw_20261027_175238/raw/U001.txt',raw:copy('data/research/hearing_raw_20261027_175238/raw/U001.txt','raw/U001.txt','企業未確定の原文断片')});
const add=[
 ['R001','判断知識・インターフェース','本人追補','data/research/hearing_analysis_20261027_201005/R001.txt'],
 ['R002','2024年比較・データ循環','本人追補','data/research/hearing_analysis_20261027_204351/R002.txt'],
 ['P001','DMG森精機・産総研の写真補足','写真補足原文','data/research/photo_review_20261028_000151/01_DMG森精機_本人補足原文.txt'],
 ['P002','FANUC フィジカルAI CNCの写真補足','写真補足原文','data/research/photo_review_20261028_080357_fanuc/本人補足原文.txt']
];
for(const [id,company,type,src] of add) records.push({id,company,type,status:'本人の説明・解釈を含む原文',source:src,raw:copy(src,`raw/${id}.txt`,type)});
const bertRaw='ちなみにこれはこれで残しておいていいけど、これもう書いてあることでそれだけの情報ならいらないという感じだったので、もう少し踏み込んだ感じで仮説とか想定とか定義につながるようなことも書きたいんだよね。っていうか、なんかそこで、ある意味だからそこでちょっと壁打ちしたいのが、あの、フィジカルAIってどういう定義、ここで言う。まあ、一般的にも。この製造データをいっぱい持っとくことによって、フィジカルAIの基本モデルって、もうある意味あれか。こうやって、ある意味BERTの製造版みたいなモデルを作ろうとしてるっていう意味なのかな。';
write('raw/R003.txt',bertRaw+'\n'); records.push({id:'R003',company:'製造版BERT仮説・定義についての問い',type:'本人追補',status:'本チャットの本人発言から転記',source:'本チャット：製造版BERTについての質問',raw:bertRaw+'\n'});
const photos=[];
for(const company of ['DMG','FANUC']) for(let i=1;i<=(company==='DMG'?2:10);i++){
 const name=`${company}_${String(i).padStart(2,'0')}.jpg`;
 const src=company==='DMG'?`data/research/photo_review_20261028_000151/photos/${name}`:`outputs/photo_review_20261028_080357_fanuc/photos/${name}`;
 copy(src,`evidence/photos/${name}`,'本人撮影写真・無加工');
 // Prior copies in the standalone discussion are the same photos.
 mapping.set(path.join(root,`outputs/discussion_notes_20261028_074731/photos/${name}`),`evidence/photos/${name}`);
 const labels=company==='DMG'?['製造データ・共通表現・特化型モデル（印刷頁6）','中立ハブ・AI-readyデータ基盤（印刷頁5）']:['全体構成：ツールとリソース','文字彫りの展示','加工面改善・仮想検証','加工面改善・事例DBの表示','加工面改善の全景','フィジカルAI CNCコンセプト','アラーム対応・自動復旧','全体構成の説明風景','全体構成の別角度','文字彫り：生成・検証・承認'];
 photos.push({id:`${company}-${String(i).padStart(2,'0')}`,company,title:labels[i-1],src:`evidence/photos/${name}`});
}
const noteSpecs=[
 ['discussion','追加議論の整理（FANUC写真受領前）','outputs/discussion_notes_20261028_074731/JIMTOF2026_追加議論まとめ_20261028.md','notes/discussion.md'],
 ['dmg','DMG森精機・産総研の写真読解','data/research/photo_review_20261028_000151/01_DMG森精機_検討メモ.md','notes/dmg.md'],
 ['bert','製造版BERT仮説とフィジカルAIの定義','data/research/photo_review_20261028_000151/02_製造版BERT仮説とフィジカルAI定義.md','notes/bert.md'],
 ['fanuc','FANUC フィジカルAI CNCの写真分析','outputs/photo_review_20261028_080357_fanuc/JIMTOF2026_FANUC_フィジカルAI_CNC_追加検討.md','notes/fanuc.md']
];
for(const [id,title,src,dst] of noteSpecs) mapping.set(path.join(root,src),dst);
mapping.set(path.join(root,'outputs/hearing_raw_20261027_175238/JIMTOF2026_当日ヒアリング原文.md'),'raw_memos.md');
mapping.set(path.join(root,'data/research/photo_review_20261028_080357_fanuc/manifest.json'),'data/source_manifest.json');
const notes=[];
for(const [id,title,src,dst] of noteSpecs){
 const p=path.join(root,src),original=fs.readFileSync(p,'utf8');
 const text=original.replace(/\]\(([^)]+)\)/g,(match,url)=>{
  if(/^(https?:|#)/.test(url))return match;
  const target=mapping.get(path.resolve(path.dirname(p),url));
  if(!target)throw new Error('Unmapped local source '+url);
  return ']('+path.posix.relative('notes',target)+')';
 });
 const head='> 集約版への複製。作成当時の検討経緯を残し、本文中の「未公開」「受領後にHTML化」等は当時の状態を示す。今回の公開状態はREADME参照。ローカルリンクのみ本フォルダ内へ付け替えた。\n\n';
 write(dst,head+text);sources.push({source:src,copy:dst,role:'分析・検討MDの複製',sourceSha256:hash(Buffer.from(original)),copySha256:hash(Buffer.from(head+text)),edits:'状態注記とローカルリンクの付替えのみ'});
 notes.push({id,title,path:dst,text:head+text});
}
const report=fs.readFileSync(path.join(here,'analysis.md'),'utf8');write('report.md',report);sources.push({source:rel(path.join(here,'analysis.md')),copy:'report.md',role:'今回編集した統合分析',sha256:hash(Buffer.from(report)),unchangedBytes:true});
for(const r of records)r.sha256=hash(Buffer.from(r.raw));
const recordData={snapshotDate:'2026-10-28',visitedCompanies:7,onsiteMemos:7,unassignedMemos:1,supplements:5,totalRecords:records.length,policy:'原文の誤字・表記差・改行は改変しない。見出し・分類・状態は本文外。原文内の推測を公式事実へ読み替えない。',records};
if(records.length!==13 || records.filter(r=>/^H/.test(r.id)).length!==7)throw new Error('Record count mismatch');
write('data/raw_memos.json',JSON.stringify(recordData,null,2)+'\n');
write('data/photos.json',JSON.stringify(photos,null,2)+'\n');
const rawIntro='# JIMTOF2026 生メモ集約\n\n2026年10月28日。現地7社＋企業未確定1件＋本人追補5件、計13記録。本文は要約・言換え・誤字修正せず保持。現地で聞いた内容、本人の感想・推測、後日の議論が含まれる。分類や見出しは原文の外側に追加した。\n\n';
write('raw_memos.md',rawIntro+records.map(r=>`## ${r.id}｜${r.company}${r.booth?'｜'+r.booth:''}\n\n種別：${r.type}／${r.status}\n\n\`\`\`\`text\n${r.raw}${r.raw.endsWith('\n')?'':'\n'}\`\`\`\`\n`).join('\n'));
write('raw_memos.txt','JIMTOF2026 生メモ集約｜2026-10-28\n本文は原文のまま。見出し・分類は管理用。\n\n'+records.map(r=>`━━━━━━━━━━━━━━━━\n${r.id}｜${r.company}${r.booth?'｜'+r.booth:''}\n種別：${r.type}\n\n${r.raw}`).join('\n\n'));
const css=fs.readFileSync(path.join(here,'style.css'),'utf8');write('assets/style.css',css);
const js=fs.readFileSync(path.join(here,'app.js'),'utf8');write('assets/app.js',js);
function render(md){return marked.parse(md).replace(/<table>/g,'<div class="table-scroll" tabindex="0" aria-label="比較表：左右にスクロール"><table>').replace(/<\/table>/g,'</table></div>').replace(/<img /g,'<img loading="lazy" ');}
function page(title,active,body,extra=''){
 const nav=[['index.html','分析','report'],['raw_memos.html','生メモ','raw'],['notes.html','詳細検討','notes'],['evidence.html','写真根拠','evidence']].map(([url,t,id])=>`<a href="${url}" ${active===id?'aria-current="page"':''}>${t}</a>`).join('');
 return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}｜JIMTOF2026</title><link rel="stylesheet" href="assets/style.css"><script defer src="assets/app.js"></script></head><body><header><div class="brand">JIMTOF2026 <span>現地調査・追加議論</span></div><nav aria-label="資料の切替">${nav}</nav></header><main>${body}</main><footer>2026.10.28 中間集約版 · 生メモ7社／写真12点 · <a href="README.md">読み方・ファイル一覧</a><br>写真の記載／現地説明／分析上の仮説を区別。追加資料の受領途中での保存版。</footer>${extra}</body></html>`;
}
const headings=[...report.matchAll(/^## (.+)$/gm)].map(m=>m[1]);
let sec=0;let html=render(report.replace(/^# .+\n/,'').replace(/^\s*2026年10月28日.*\n/,''));
html=html.replace(/<h2>([\s\S]*?)<\/h2>/g,(_,h)=>`${sec?'</section></details>':''}<details class="chapter" id="s${++sec}" ${sec===1?'open':''}><summary><h2>${h}</h2></summary><section class="chapter-body">`);
html+='</section></details>';
const flow='<figure class="workflow"><figcaption>課題解決の流れと、次の案件への循環</figcaption><ol>'+['要求・観測状態','判断知識・切分け','解析・仮想検証','人の承認','実機への適用','結果・事例を保存'].map(x=>'<li>'+x+'</li>').join('')+'</ol><p>↺ 評価済みの結果を、知識・モデル・ツールへ戻す段階は一部未確認。</p></figure>';
write('index.html',page('技術動向・仮説の照合','report',`<div class="eyebrow">2026.10.28／中間集約版</div><h1>AIが製造の判断と実行をつなぐ</h1><p class="lead">現地7社のヒアリングと、DMG森精機・FANUCの写真12点から、技術動向・各社の方式・仮説の支持と修正を整理。</p><div class="downloads"><a href="report.md" download>分析MD</a><a href="raw_memos.md" download>生メモMD</a><a href="raw_memos.txt" download>生メモTXT</a><a href="snapshot.zip" download>一式ZIP</a></div>${flow}<div class="toolbar"><button type="button" data-expand>全章を開く</button><button type="button" data-collapse>閉じる</button><span>章名をタップして展開</span></div><details class="toc-panel"><summary>目次（12章）</summary><div class="toc">${headings.map((h,i)=>`<a href="#s${i+1}">${esc(h)}</a>`).join('')}</div></details><article>${html}</article>`));
const rawBodies=records.map(r=>`<details class="record" id="${r.id}" data-kind="${esc(r.type)}" data-company="${esc(r.company)}"><summary><span class="record-id">${r.id}</span><strong>${esc(r.company)}</strong><span class="record-meta">${esc(r.booth||r.type)}</span></summary><div class="record-body"><div class="metadata">${esc(r.type)} · ${esc(r.status)}${r.area?' · '+esc(r.area):''}</div><div class="record-actions"><button type="button" data-copy="${r.id}">原文をコピー</button><a href="raw/${r.id}.txt" download>TXT</a></div><pre class="raw">${esc(r.raw)}</pre></div></details>`).join('');
write('raw_memos.html',page('生メモ全文','raw',`<div class="eyebrow">原文保存／13記録</div><h1>生メモ集約</h1><p>現地7社＋企業未確定1件＋本人追補5件。誤字・表記差を含め、要約せず掲載。原文中の推測や予定を、確定事項と読み替えない。</p><div class="searchbar"><label for="query">企業名・キーワードで検索</label><input id="query" type="search" placeholder="例：ファナック、判断、VAE" autocomplete="off"><label for="kind">記録の種類</label><select id="kind"><option value="">すべて</option>${[...new Set(records.map(r=>r.type))].map(t=>`<option>${esc(t)}</option>`).join('')}</select></div><div class="toolbar"><output id="count" aria-live="polite">13／13記録</output><button type="button" data-expand>表示分を開く</button><button type="button" data-collapse>閉じる</button><button type="button" id="copy-all">表示分をまとめてコピー</button></div><p id="empty" hidden>一致する記録はありません。</p>${rawBodies}<p class="downloads"><a href="raw_memos.md" download>全原文MD</a><a href="raw_memos.txt" download>全原文TXT</a><a href="data/raw_memos.json" download>JSON</a></p>`,`<script id="memo-data" type="application/json">${JSON.stringify(records).replace(/</g,'\\u003c')}</script>`));
const noteHTML=notes.map(n=>`<details class="chapter" id="${n.id}"><summary><h2>${esc(n.title)}</h2></summary><section class="chapter-body"><p class="downloads"><a href="${n.path}" download>この検討をMDで保存</a></p>${render(n.text).replace(/(href|src)="\.\.\//g,'$1="').replace(/href="(discussion|bert|dmg|fanuc)\.md"/g,'href="notes/$1.md')}</section></details>`).join('');
write('notes.html',page('詳細検討・議論の経緯','notes',`<div class="eyebrow">検討内容を保持</div><h1>詳細検討</h1><p>統合分析の背景となった4つの検討MD。作成当時の留保や解釈の変化も残しています。本文中の「未公開」等は当時の状態で、今回の公開状態はREADMEに記載。</p><div class="toolbar"><button data-expand>すべて開く</button><button data-collapse>閉じる</button></div>${noteHTML}`));
const ev=photos.map(p=>`<details class="record" id="${p.id}"><summary><span class="record-id">${p.id}</span><strong>${esc(p.title)}</strong></summary><div class="record-body"><a href="${p.src}" target="_blank" rel="noopener"><img data-src="${p.src}" alt="${esc(p.company+' '+p.title)}" width="2880" height="3840"></a><p><a href="${p.src}" target="_blank" rel="noopener">原寸写真を開く</a></p></div></details>`).join('');
write('evidence.html',page('写真根拠','evidence',`<div class="eyebrow">本人撮影／12点</div><h1>写真根拠</h1><p>DMG森精機2点、FANUC10点を無加工で保存。同じ展示の別角度写真を、別技術として数えていません。開いた写真だけを読み込みます。</p><div class="table-scroll"><table><thead><tr><th>根拠</th><th>重要な記載・位置</th><th>分析上の境界</th></tr></thead><tbody><tr><td><a href="#DMG-01">DMG・頁6</a></td><td>図②：共通の中間表現から特化型モデルへ。VAEの記載。</td><td>言語で対策・ツールを選ぶ能力までは示さない。</td></tr><tr><td><a href="#DMG-02">DMG・頁5</a></td><td>産総研の匿名化・構造化・権利処理とAI-ready基盤。</td><td>100社・1,000台は目標。</td></tr><tr><td><a href="#FANUC-01">FANUC・写真1</a></td><td>MCPサーバ内のツール、リソース（情報・知識）。</td><td>知識の内部形式は未確認。</td></tr><tr><td><a href="#FANUC-04">FANUC・写真4</a></td><td>上部：改善手順利用・仮想検証。下部UI：事例DB保存・次回参照。</td><td>実測結果の保存や、モデル再学習とは区別。</td></tr><tr><td><a href="#FANUC-07">FANUC・写真7</a></td><td>アラーム対応・自動復旧の見出し。</td><td>細部は一部判読不能。物理修理全般の自律化としない。</td></tr><tr><td><a href="#FANUC-10">FANUC・写真10</a></td><td>文字彫りプログラム生成・軌跡検証・確認と承認。</td><td>任意形状の工程設計へ一般化しない。</td></tr></tbody></table></div>${ev}`));
const readme=`# JIMTOF2026 現地調査・追加議論の集約\n\n2026-10-28 中間集約版。追加資料受領の途中で、本人の依頼によりここまでを別保存・公開する。既存成果物は変更しない。\n\n## 読み方\n\n- index.html：技術動向・各社比較・仮説の照合。スマホ向けの章開閉。\n- report.md：上記分析の編集可能なMarkdown。\n- raw_memos.html／raw_memos.md／raw_memos.txt：生メモ13記録。HTMLは検索・種類別絞込み・原文コピー。\n- notes.html／notes/：既存の詳細検討4本の複製。リンクと状態注記だけ調整。\n- evidence.html／evidence/photos/：本人撮影12点を無加工で保持。\n- data/raw_memos.json：現地7社、所属未確定1件、本人追補5件。\n- data/source_manifest.json：元のリポジトリ内パスと複製先・ハッシュ。\n- snapshot.zip：このフォルダの一式（ZIP自体と検証画像を除く）。\n\n## 原文の保持\n\nH001～H007、U001、R001～R002、P001～P002は保存済み原文をバイト単位で複製。R003は本チャットの本人発言「製造版BERTについての問い」を転記した。企業名・種類等の見出しは原文外の管理情報。生メモの誤字・表記差・推測・日程は修正しない。ファイル末尾の改行を含め、元ファイルの内容を保持する。\n\n## 確度\n\n写真のメーカー訴求、本人の現地説明、調査者の解釈は別の根拠。VAE／VLM、31Bモデル名の表記差、提供予定、事例DBとモデル再学習の違いは本文に明記。追加の広範なWeb再調査や、展示機の独立した性能試験は行っていない。\n\n## 検証\n\n最終結果は data/verification.json を参照。原文・写真の複製一致、ローカルリンク、スマホ・PC表示、検索・絞込み・展開・コピーを対象とする。実施済みの検証のみ記録する。\n`;
write('README.md',readme);
write('data/source_manifest.json',JSON.stringify({created:'2026-10-28',scope:'ここまでの中間集約・既存ファイル不変更',originalRecords:12,chatTranscribedRecords:1,photos:12,notes:4,sources},null,2)+'\n');
write('data/verification.json',JSON.stringify({status:'awaiting_browser_checks',rawCopies:12,photoCopies:12,copiesSha256Match:true,records:13,visitedCompanies:7,notes:4,additionalWebResearch:false,performanceTesting:false},null,2)+'\n');
console.log(JSON.stringify({out,records:records.length,photos:photos.length,notes:notes.length,sourceCopies:sources.length,reportChars:report.length}));
