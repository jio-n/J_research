import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {chromium} from '../visit_update_20261026_225824/_private/node_modules/playwright/index.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(dir,'../../..'),out=path.join(root,'outputs',path.basename(dir));
const md=await fs.readFile(path.join(out,'JIMTOF2026_現地ヒアリングと事前仮説の照合.md'),'utf8'),raw=JSON.parse(await fs.readFile(path.join(root,'data/research/hearing_raw_20261027_175238/hearing_records.json'),'utf8'));
const checks=[];function ok(v,m){if(!v)throw Error(m);checks.push(m)}
ok(md.includes('2024年にも示されていた'),'2024年に構想が存在したことを区別');
ok(md.includes('紐付いたデータを作りやすい'),'データセット完成を断定しない');
ok(md.includes('排他的な選択肢ではなく'),'知識表現・参照・接続を別軸で整理');
const quotes=md.split(/\r?\n/).filter(l=>l.startsWith('> ')).map(l=>l.slice(2));
ok(quotes.length===8,'7社の原文抜粋8行');for(const q of quotes)ok(raw.records.some(r=>r.raw.includes(q)),'原文抜粋を文字単位で照合');
const manifest=JSON.parse(await fs.readFile(path.join(dir,'input_manifest.json'),'utf8'));for(const x of manifest.inputs)ok(crypto.createHash('sha256').update(await fs.readFile(path.join(root,x.path))).digest('hex')===x.sha256,'入力資料を改変していない：'+x.path);
const hs=JSON.parse(await fs.readFile(path.join(dir,'hypothesis_assessment.json'),'utf8')).hypotheses;
ok(hs.length===9,'9論点の仮説照合');ok(hs.every(h=>h.evidenceIds.length>0&&h.evidenceIds.every(id=>raw.records.some(r=>r.id===id&&r.status==='訪問実績'))),'仮説の根拠IDは訪問7社に限定');
const server=http.createServer(async(req,res)=>{const rel=decodeURIComponent((req.url||'/').split('?')[0]);const file=path.resolve(root,'.'+rel);if(!file.startsWith(root+path.sep)){res.statusCode=403;res.end();return}try{const data=await fs.readFile(file);res.setHeader('Content-Type',file.endsWith('.html')?'text/html;charset=utf-8':'text/plain;charset=utf-8');res.end(data)}catch{res.statusCode=404;res.end('not found')}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:'+server.address().port+'/outputs/'+path.basename(dir)+'/analysis.html');
ok(await page.locator('.chapter').count()===7,'7章の開閉構成');
await page.screenshot({path:path.join(dir,'_private/mobile_top.png')});
await page.locator('#section-2 > summary').click();ok(await page.locator('#section-2 table tbody tr').count()===9,'9論点の比較表を開ける');
for(const w of[320,390,430,1200]){await page.setViewportSize({width:w,height:844});ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'外側の横はみ出しなし：'+w)}
await page.setViewportSize({width:390,height:844});
await page.locator('#section-2 a[href="#H005"]').first().click();
ok(await page.locator('#section-7').getAttribute('open')!==null,'根拠リンクで閉じた章を自動展開');
await page.waitForFunction(()=>{const y=document.getElementById('H005').getBoundingClientRect().top;return y>=-1&&y<200});
ok(await page.getByRole('heading',{name:'H005 ヤマザキマザック｜E1001',exact:true}).isVisible(),'対応する企業の根拠へ移動');
await page.screenshot({path:path.join(dir,'_private/mobile_evidence.png')});
for(const name of ['JIMTOF2026_当日ヒアリング原文.md']){const response=await page.request.get('http://127.0.0.1:'+server.address().port+'/outputs/hearing_raw_20261027_175238/'+encodeURIComponent(name));ok(response.status()===200,'原文全文へのリンク先あり')}
ok(errors.length===0,'ブラウザーエラーなし');
await browser.close();await new Promise(r=>server.close(r));
await fs.writeFile(path.join(dir,'verification.json'),JSON.stringify({checks,count:checks.length,errors,rawSourcesUnchanged:true,nativeIPhoneTest:false},null,2),'utf8');
console.log(JSON.stringify({checks:checks.length,errors}));
