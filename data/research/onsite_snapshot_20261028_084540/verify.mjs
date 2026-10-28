import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import http from 'node:http';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=process.cwd(),folder='onsite_snapshot_20261028_084540',out=path.join(root,'outputs',folder),here=path.join(root,'data/research',folder);
fs.mkdirSync(path.join(here,'_private'),{recursive:true});
const checks=[];function ok(v,s){if(!v)throw Error(s);checks.push(s)}
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const manifest=JSON.parse(fs.readFileSync(path.join(out,'data/source_manifest.json')));
for(const x of manifest.sources){const src=fs.readFileSync(path.join(root,x.source));ok(sha(src)===(x.sha256||x.sourceSha256),'source unchanged: '+x.source);const dst=fs.readFileSync(path.join(out,x.copy));ok(sha(dst)===(x.sha256||x.copySha256),'copy matches: '+x.copy)}
const raw=JSON.parse(fs.readFileSync(path.join(out,'data/raw_memos.json')));
ok(raw.records.length===13,'13 raw records');ok(raw.records.filter(x=>/^H/.test(x.id)).length===7,'7 visited companies');ok(raw.records.find(x=>x.id==='U001').type==='未確定の断片','unassigned memo remains separate');
for(const r of raw.records)ok(fs.readFileSync(path.join(out,'raw',r.id+'.txt'),'utf8')===r.raw,'raw JSON matches TXT '+r.id);
const md=fs.readFileSync(path.join(out,'raw_memos.md'),'utf8');for(const r of raw.records)ok(md.includes(r.raw),'raw body in MD '+r.id);
const server=http.createServer((req,res)=>{const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);const file=path.resolve(out,'.'+name);if(!file.startsWith(out+path.sep)){res.statusCode=403;res.end();return}try{const b=fs.readFileSync(file);const ext=path.extname(file);res.setHeader('Content-Type',({'.html':'text/html;charset=utf-8','.css':'text/css;charset=utf-8','.js':'text/javascript;charset=utf-8','.jpg':'image/jpeg','.json':'application/json;charset=utf-8'})[ext]||'application/octet-stream');res.end(b)}catch{res.statusCode=404;res.end('Not found')}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(),errors=[],badLinks=[];
page.on('pageerror',e=>errors.push(e.message));
const origin='http://127.0.0.1:'+server.address().port+'/';
for(const f of ['index.html','raw_memos.html','notes.html','evidence.html']){
 await page.goto(origin+f);await page.locator('[data-expand]').first().click().catch(()=>{});
 for(const w of [320,390,430,1440]){await page.setViewportSize({width:w,height:844});ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),f+' no page overflow '+w)}
 const hrefs=await page.locator('a[href]').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
 for(const href of new Set(hrefs)){if(/^(https?:|mailto:|data:)/.test(href))continue;const u=new URL(href,origin+f);const disk=path.join(out,decodeURIComponent(u.pathname));if(!fs.existsSync(disk)){badLinks.push({f,href});continue}if(u.hash&&disk.endsWith('.html')){const text=fs.readFileSync(disk,'utf8');if(!text.includes('id="'+decodeURIComponent(u.hash.slice(1))+'"'))badLinks.push({f,href,reason:'missing anchor'})}}
 await page.setViewportSize({width:390,height:844});
 if(f==='index.html'){await page.locator('[data-collapse]').click();await page.locator('.toc-panel summary').click();await page.locator('.toc a[href="#s3"]').click();ok(await page.locator('#s3').evaluate(d=>d.open),'chapter anchor opens target');await page.screenshot({path:path.join(here,'_private/mobile_comparison.png')});await page.goto(origin+f);await page.screenshot({path:path.join(here,'_private/mobile_top.png')});}
 if(f==='raw_memos.html'){
  const q=page.locator('#query');await q.fill('Qwen');const expected=raw.records.filter(r=>(r.id+' '+r.company+' '+(r.booth||'')+' '+r.raw).toLowerCase().includes('qwen')).length;
  ok(await page.locator('details.record:visible').count()===expected,'keyword filtering');
  await page.locator('#kind').selectOption('写真補足原文');ok(await page.locator('details.record:visible').count()===1,'combined type and keyword filtering');
  if(!await page.locator('#P002').evaluate(d=>d.open))await page.locator('#P002 summary').click();await page.locator('[data-copy="P002"]').click();
  const normalize=s=>s.replace(/\r\n/g,'\n');ok(normalize(await page.evaluate(()=>navigator.clipboard.readText()))===normalize(raw.records.find(r=>r.id==='P002').raw),'single raw copy preserves body');
  await page.locator('#copy-all').click();ok((await page.evaluate(()=>navigator.clipboard.readText())).includes('Ornith'),'copy visible records');
  await q.fill('不存在CHECK987');ok(await page.locator('#empty').isVisible(),'no results feedback');ok(await page.locator('#copy-all').isDisabled(),'empty copy disabled');
  await q.fill('');await page.locator('#kind').selectOption('');ok(await page.locator('details.record:visible').count()===13,'reset filters restores all');
  await page.locator('[data-collapse]').click();await page.screenshot({path:path.join(here,'_private/mobile_raw.png')});
 }
 if(f==='evidence.html'){
  await page.locator('a[href="#FANUC-04"]').click();ok(await page.locator('#FANUC-04').evaluate(d=>d.open),'photo anchor opens image');
  await page.waitForFunction(()=>{const i=document.querySelector('#FANUC-04 img');return i.complete&&i.naturalWidth>0});ok(true,'photo loads');
 }
 if(f==='notes.html'){ok(await page.locator('.chapter').count()===4,'4 detailed working notes');const images=await page.locator('img').evaluateAll(es=>es.map(e=>e.getAttribute('src')));for(const src of images)ok(fs.existsSync(path.join(out,src)),'note image path exists '+src)}
}
ok(!badLinks.length,'all local HTML links and anchors exist');ok(!errors.length,'no browser page errors');
await page.setViewportSize({width:1440,height:960});await page.goto(origin+'index.html');await page.screenshot({path:path.join(here,'_private/desktop_top.png')});
await browser.close();
await new Promise(resolve=>server.close(resolve));
const result={status:'passed',checks:checks.length,checkDetails:checks,rawRecords:13,visitedCompanies:7,photoCopies:12,originalRawFileCopies:12,chatTranscribedRecords:1,allSourceHashesMatch:true,allRawBodiesMatch:true,brokenLocalLinks:badLinks,browserErrors:errors,viewports:[320,390,430,1440],browser:'Windows Edge headless, mobile viewport emulation',searchFilterCopyTested:true,chapterAndPhotoExpansionTested:true,nativeIPhoneTest:false,additionalWebResearch:false,exhibitPerformanceTesting:false,existingOutputsModified:false};
fs.writeFileSync(path.join(out,'data/verification.json'),JSON.stringify(result,null,2)+'\n');
fs.writeFileSync(path.join(here,'verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,brokenLocalLinks:badLinks,browserErrors:errors}));
