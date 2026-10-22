import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(D,'../../..'),O=path.join(root,'outputs',path.basename(D)),work=path.join(D,'_private/presentation_qa');
const skill='C:/Users/paulr/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11618/skills/presentations';
const python='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const read=async p=>JSON.parse(await fs.readFile(path.join(D,p),'utf8'));
const g=await read('report_content.json'),d=await read('research.json'),ev=await read('evidence_review.json'),quotes=(await read('original_quotes_reference.json')).quotes;
const items=new Map(d.items.map(x=>[x.id,x])),sources=new Map(ev.map(x=>[x.source_id,x])),qm=new Map(quotes.map(x=>[x.quote_id,x]));
await fs.mkdir(work,{recursive:true});
const font='Yu Gothic UI',ink='#17374A',muted='#516978',teal='#0B7B7C',deck=Presentation.create({slideSize:{width:1920,height:1080}}),owners=[],layout=[];
function text(s,name,v,x,y,w,h,size,bold=false,color=ink){const q=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});q.text=v;q.text.style={fontSize:size,typeface:font,bold,color,insets:0,wrap:'square',autoFit:'none',lineSpacing:1.12,verticalAlignment:'top'};return q;}
function units(s){return [...s].reduce((a,c)=>a+(/[\u0020-\u007e]/.test(c)?.59:1),0)}
function wrap(s,max){return String(s).split('\n').map(p=>{let line='',u=0,out=[];for(const token of (p.match(/[A-Za-z0-9][A-Za-z0-9_&.+/\-]*|./gu)||[])){let v=units(token);if(u+v>max&&line&&!/^[、。）」]/.test(token)){out.push(line.trim());line='';u=0;}line+=token;u+=v;}if(line)out.push(line.trim());return out.join('\n')}).join('\n')}
function lines(s,max){return String(s).split('\n').reduce((a,p)=>a+Math.max(1,Math.ceil(units(p)/max)),0)}
function sourceText(id){if(sources.has(id)){let s=sources.get(id);return `${id} ${s.publisher}｜${s.title}\n発行 ${s.published_date} 確認 ${s.checked_date}\n${s.url}\n掲載位置 ${s.locator}\n確認方式 ${s.verification}\n原文 ${s.short_quote||'引用なし'}\n文脈要約 ${s.context_summary}\n留保 ${s.not_evidence_for}`}let q=qm.get(id);return q?`${id} ${q.attribution}\n${q.title} ${q.published_date}\n${q.source_url}\n掲載位置 ${q.locator}\n原文 ${q.excerpt_original}\n文脈 ${q.context_paraphrase}\n留保 ${q.not_evidence_for}\n前版確認 ${q.verified_date} を継承`:id;}
for(let i=0;i<g.slides.length;i++){
 const c=g.slides[i],s=deck.slides.add();s.background.fill='#FFFFFF';
 text(s,'section',c.section==='メイン'?'JIMTOF2026｜技術動向・訪問調査':'JIMTOF2026｜補足資料',86,31,1748,27,19,false,teal);
 text(s,'heading',c.title,86,82,1748,72,44,true);
 text(s,'context',c.context,88,171,1740,79,28,false,muted);
 const widths=c.widths||[440,640,668],raw=[c.headers,...c.rows];let size=28,heights,vals;
 while(true){vals=raw.map((r,ri)=>r.map((v,j)=>wrap(v,(widths[j]-38)/(ri?size:size-1))));heights=vals.map((r,ri)=>Math.max(ri?73:58,...r.map((v,j)=>v.split('\n').length*(ri?size:size-1)*1.22+27)));if(heights.reduce((a,b)=>a+b,0)<=690||size<=23)break;size--;}
 const total=heights.reduce((a,b)=>a+b,0);if(total>703)throw Error('Content needs editing on slide '+(i+1)+': '+total);
 const spare=(698-total)/c.rows.length;heights=heights.map((h,n)=>n?h+spare:h);
 const t=s.tables.add({rows:vals.length,columns:c.headers.length,left:86,top:272,width:1748,height:heights.reduce((a,b)=>a+b,0),columnWidths:widths,values:vals});
 t.borders.assign({fill:'#CCDCE2',width:1,style:'solid'});
 for(let r=0;r<vals.length;r++){t.rows[r].height=heights[r];for(let j=0;j<c.headers.length;j++){const ce=t.getCell(r,j);ce.fill=r===0?ink:(r%2===0?'#F0F5F6':'#FFFFFF');ce.text.style={fontSize:r===0?size-1:size,typeface:font,bold:r===0||j===0,color:r===0?'#FFFFFF':ink,insets:11,autoFit:'none',wrap:'square',lineSpacing:1.10,verticalAlignment:'top'};}}
 owners.push(i+1);layout.push({slide:i+1,title:c.title,font_size_px:size,row_heights:heights});
 text(s,'footer',c.note||'公開情報の事前分析｜現地未確認｜出典URL・掲載位置・留保はスピーカーノートに記載',88,992,1600,57,19,false,muted);
 text(s,'page',`${String(i+1).padStart(2,'0')} / ${g.slides.length}`,1740,1001,110,35,21,false,muted);
 s.speakerNotes.text=['視察前資料／2026-10-23。主張・顧客課題・推奨理由は調査者の分析。メーカーの記載と性能の独立実証を区別。',c.note,...c.refs.map(sourceText),...c.ids.map(id=>{let x=items.get(id);return `${x.id} ${x.company} ${x.item}\n小間 ${x.booths.join('/')}\n展示 ${x.exhibit} ${x.exhibit_note}\n入力 ${x.input}\n方式 ${x.method}\n出力 ${x.output}\n人 ${x.human}\n限界 ${x.limits}\n現地 ${x.check}\n確認 ${x.refinement_review}\n`+x.sources.map(e=>`${e.source_id} ${e.publisher} ${e.title}\n${e.url}\n掲載位置 ${e.locator}\n確認 ${e.checked_date}`).join('\n\n')})].join('\n\n');
}
const candidate=path.join(work,'candidate-r3.pptx'),finalPath=path.join(O,'report-r3.pptx');
await(await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit',...owners.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:g.slides.length,requiredNativeTableOwnerSlides:owners,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(work,'validation-r3.json')});
await fs.writeFile(path.join(D,'presentation_layout.json'),JSON.stringify(layout,null,2));
const finalDeck=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<finalDeck.slides.items.length;i++){const png=await finalDeck.export({slide:finalDeck.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(work,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));}
console.log(JSON.stringify({output:finalPath,slides:g.slides.length,main:3,nativeTables:owners.length,minimumFont:Math.min(...layout.map(x=>x.font_size_px))}));process.exit(0);
