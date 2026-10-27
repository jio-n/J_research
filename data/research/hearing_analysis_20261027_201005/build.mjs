import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {marked} from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';
const dir=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(dir,'../../..'),out=path.join(root,'outputs',path.basename(dir));
const md=await fs.readFile(path.join(out,'JIMTOF2026_現地ヒアリングと事前仮説の照合.md'),'utf8');
const raw=JSON.parse(await fs.readFile(path.join(root,'data/research/hearing_raw_20261027_175238/hearing_records.json'),'utf8'));
const table=md.split('## 2. 事前仮説の判定')[1].split('## 3.')[0].split('\n').filter(l=>l.startsWith('|')).slice(2);
const hypotheses=table.map((line,i)=>{const cells=line.slice(1,-1).split('|').map(s=>s.trim());return {id:'T'+String(i+1).padStart(2,'0'),hypothesis:cells[0],assessment:cells[1],newEvidence:cells[2],limits:cells[3],evidenceIds:[...new Set([...line.matchAll(/\[H(\d{3})\]/g)].map(m=>'H'+m[1]))]};});
await fs.writeFile(path.join(dir,'hypothesis_assessment.json'),JSON.stringify({date:'2026-10-27',basis:'現地メモ7社と保存済み事前仮説の定性的照合。普及率・因果効果の統計推定ではない。',hypotheses},null,2),'utf8');
const inputs=['data/research/hearing_analysis_20261027_201005/R001.txt','AGENTS.md','RESEARCH_START.md','data/research/hearing_raw_20261027_175238/hearing_records.json','data/research/strategy_review_20261021/strategy_review.json','data/research/astra_refinement_20261023_013112/report_content.json','data/research/astra_refinement_20261023_013112/evidence_review.json','data/research/deep_reading_20261021/01_source_readings.md','data/research/quotation_evidence_20261022/02_physical_ai_and_tasks.md','data/research/quotation_evidence_20261022/01_verbatim_evidence.md'];
const sourceHashes=[];for(const p of inputs)sourceHashes.push({path:p,sha256:crypto.createHash('sha256').update(await fs.readFile(path.join(root,p))).digest('hex')});
await fs.writeFile(path.join(dir,'input_manifest.json'),JSON.stringify({inputs:sourceHashes,readingScope:'事前報告のthesis・主篇とanalysis、H1〜H5、精読ノートS01〜S09/S24〜S30、作業定義、現地7社全文を重点照合。40原典の全再精読を意味しない。',unassignedMemoExcluded:'U001',rawUnchanged:true},null,2),'utf8');
const urls=[
 ['W01','https://www.fanuc.co.jp/ja/product/cnc/physical-ai-cnc/','本文再確認','MCPとツイン・人の承認'],
 ['W02','https://www.abejainc.com/news/20261016/2','本文再確認','共同開発（1）〜（3）'],
 ['W03','https://www.aist.go.jp/aist_j/news/pr20260702.html','本文再確認','製造AX拠点の役割'],
 ['W04','https://www.mazak.com/jp-ja/technology/productivity/','本文再確認','MAZATROL DX'],
 ['W05','https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260930.html','本文再確認','日立工場での実証'],
 ['W06a','https://modelcontextprotocol.io/specification/2025-06-18/architecture','本文確認','Host・Client・Server'],
 ['W06b','https://modelcontextprotocol.io/specification/2025-06-18/server/tools','本文確認','ツールの発見・呼出し・確認'],
 ['W07','https://www.dmgmori.co.jp/corporate/news/2026/20260706_geniac.html','再取得失敗（502）','既存保存分析とW03を利用']
].map(([id,url,status,locator])=>({id,url,status,locator,checkedDate:'2026-10-27'}));
await fs.writeFile(path.join(dir,'source_checks.json'),JSON.stringify(urls,null,2),'utf8');
const htmlBody=marked.parse(md).replace(/href="\.\.\/([^"]+)"/g,(_,p)=>`href="https://github.com/jio-n/J_research/blob/main/outputs/${p}"`);
let n=0;const body=htmlBody.replace(/<h2>(.*?)<\/h2>/g,(_,t)=>`<h2 id="section-${++n}">${t}</h2>`);
const chunks=body.split(/(?=<h2 id="section-)/);
let content=chunks.shift();const navigation=[];
for(const chunk of chunks){const m=chunk.match(/^<h2 id="([^"]+)">(.*?)<\/h2>/);navigation.push(`<a href="#${m[1]}">${m[2]}</a>`);const open=m[1]==='section-1'?' open':'';content+=`<details class="chapter"${open} id="${m[1]}"><summary>${m[2]}</summary><div class="chapter-body">${chunk.slice(m[0].length)}</div></details>`;}
content=content.replace(/<table>/g,'<div class="table-wrap" tabindex="0"><table>').replace(/<\/table>/g,'</table></div>');
const css=`*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#253843;background:#f4f6f7;font:16px/1.8 -apple-system,BlinkMacSystemFont,"Yu Gothic UI",Meiryo,sans-serif;overflow-wrap:anywhere}header{background:#fff;border-bottom:1px solid #ccd7dd;padding:10px 12px}header div{max-width:1020px;margin:auto;display:flex;justify-content:space-between;gap:10px}a{color:#086b91}main{max-width:1050px;margin:auto;padding:12px}h1{font-size:24px;line-height:1.5;margin:10px 0}h3{font-size:18px;color:#234c65;margin:22px 0 9px}p{margin:10px 0}nav{font-size:14px;display:flex;gap:8px 14px;flex-wrap:wrap;margin:14px 0}.chapter{background:white;border:1px solid #cbd7df;border-radius:5px;margin:10px 0;scroll-margin-top:10px}.chapter>summary{cursor:pointer;font-weight:650;padding:10px 12px;font-size:17px}.chapter-body{padding:0 13px 13px}.chapter-body>p:first-child{margin-top:0}.table-wrap{overflow-x:auto;max-width:100%;margin:10px 0 16px}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.7;min-width:760px}th{text-align:left;background:#e7eef3;color:#233e50;font-weight:650}th,td{border-bottom:1px solid #d5e0e6;padding:8px;vertical-align:top}th:first-child,td:first-child{min-width:140px}td{min-width:165px}tbody tr:nth-child(even){background:#f7f9fa}blockquote{margin:10px 0;padding:4px 12px;border-left:3px solid #9cb5c6;background:#f5f8fa;font-size:15px}blockquote p{margin:5px 0}li{margin:7px 0}ul{padding-left:23px}footer{max-width:1020px;margin:auto;padding:16px 12px;color:#657985;font-size:13px}.scope{background:#eaf1f5;padding:9px 11px;margin:8px 0;font-size:14px}@media(max-width:520px){body{font-size:15px;line-height:1.85}main{padding:8px}h1{font-size:21px}.chapter>summary{font-size:16px;padding:9px}.chapter-body{padding:0 10px 10px}h3{font-size:17px}table{font-size:14px}nav{display:none}}`;
const script=`document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a)return;const id=decodeURIComponent(a.hash.slice(1)),el=document.getElementById(id);if(!el)return;e.preventDefault();for(let p=el;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;el.scrollIntoView({block:'start',behavior:'smooth'});history.replaceState(null,'','#'+id);});function revealHash(){if(!location.hash)return;const el=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(el){for(let p=el;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;el.scrollIntoView();}}revealHash();`;
const html=`<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>JIMTOF2026 現地ヒアリングと仮説の照合</title><style>${css}</style></head><body><header><div><strong>現地ヒアリングの技術分析</strong><a href="https://jio-n.github.io/J_research/">訪問一覧</a></div></header><main><p class="scope">7社のメモに基づく分析。原文は別保存。章をタップして展開、比較表は横スクロールできます。</p><nav>${navigation.join('')}</nav>${content}</main><footer>2026-10-27｜事前仮説と現地メモの照合版。モデル・価格・性能等はメモと公開情報の確認範囲を区別。</footer><script>${script}</script></body></html>`;
await fs.writeFile(path.join(out,'analysis.html'),html,'utf8');
await fs.mkdir(path.join(dir,'_private'),{recursive:true});
console.log(JSON.stringify({hypotheses:hypotheses.length,hearingCompanies:raw.visitedCompanies,htmlBytes:Buffer.byteLength(html),output:out}));
