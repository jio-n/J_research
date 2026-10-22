import fs from 'node:fs/promises';
import path from 'node:path';
import {constants} from 'node:fs';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const root=path.resolve('.');
const revision=process.argv[2]||'r1';
if(!/^r\d+$/.test(revision))throw Error('Expected revision r1, r2, ...');
const work=path.join(root,'.build/evidence_briefing_20261022',revision);
const datadir=path.join(root,'data/research/evidence_briefing_20261022');
const outdir=path.join(root,'outputs/evidence_briefing_20261022');
const skill='C:/Users/paulr/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22135/skills/presentations';
const python='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation,resolvePresentationFont,applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
await fs.mkdir(work,{recursive:true});await fs.mkdir(outdir,{recursive:true});
const read=async name=>JSON.parse(await fs.readFile(path.join(root,name),'utf8'));
const content=await read('data/research/evidence_briefing_20261022/slide_content.json');
const ledger=await read('data/research/quotation_evidence_20261022/quotes.json');
const coverage=await read('data/research/deep_reading_20261021/source_coverage.json');
const quotes=new Map(ledger.quotes.map(q=>[q.quote_id,q]));
const extra=new Map(coverage.additional_sources.map(s=>[s.id,s]));
const quotePages=new Map();
for(const s of content.slides)for(const qid of s.quote_ids||[])quotePages.set(qid,s.number);
const font=resolvePresentationFont({fontFamily:'Noto Sans JP'});
const fontPolicy={basis:'design',families:[font]};
const ink='#183C4D',teal='#117D83',muted='#536C78',line='#CEDBDC',warm='#926620';
const deck=Presentation.create({slideSize:{width:1920,height:1080}});
const tableOwners=[],chartOwners=[],index=[],fitIssues=[];

function wrap(value,width){
 return String(value).split('\n').map(p=>{let used=0,result='';for(const ch of p){const units=/[\u0020-\u007e]/.test(ch)?0.53:1;if(used+units>width){result+='\n';used=0;}result+=ch;used+=units;}return result;}).join('\n');
}
function textbox(s,name,value,x,y,w,h,size=30,{bold=false,color=ink,uri,wrapText=true}={}){
 const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=uri?[[{run:value,link:{uri,isExternal:true}}]]:value;
 t.text.style={fontSize:size,typeface:font,bold,color,insets:0,autoFit:'none',wrap:wrapText?'square':'none',lineSpacing:1.08,verticalAlignment:'top'};
 return t;
}
function nativeTable(s,values,widths,heights,size,top=270){
 const inset=size<=25?8:11;
 const formatted=values.map((row,r)=>row.map((value,c)=>{
   const text=wrap(value,(widths[c]-2*inset-6)/size);
   const required=text.split('\n').length*size*1.2+2*inset;
   if(required>heights[r]+2)fitIssues.push({slide:deck.slides.items.length,row:r,column:c,required,available:heights[r],text});
   return text;
 }));
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:86,top,width:1748,height:heights.reduce((a,b)=>a+b,0),columnWidths:widths,values:formatted});
 t.borders.assign({fill:line,width:1,style:'solid'});
 for(let r=0;r<values.length;r++){
  t.rows[r].height=heights[r];
  for(let c=0;c<values[0].length;c++){
   const cell=t.getCell(r,c);cell.fill=r===0?ink:(r%2===0?'#F0F5F3':'#FFFFFF');
   cell.text.style={fontSize:size,typeface:font,bold:r===0||c===0,color:r===0?'#FFFFFF':ink,insets:inset,autoFit:'none',wrap:'none',lineSpacing:1.08,verticalAlignment:'top'};
  }
 }
 tableOwners.push(deck.slides.items.length);
 return t;
}
function sourceNotes(ids){
 return ids.map(id=>{
  if(quotes.has(id)){
   const q=quotes.get(id);
   return `${id} / ${q.source_id}\n${q.attribution}\n${q.publisher} ${q.title}\n公表日 ${q.published_date}\n${q.source_url}\n掲載位置 ${q.locator}\n文脈の要約 ${q.context_paraphrase}\n根拠にする論点 ${q.use_for}\nこの一節からは言えないこと ${q.not_evidence_for}\n確認 ${q.verified_date} ${q.verification}`;
  }
  const a=extra.get(id);if(!a)throw Error('Missing source '+id);
  return `${id} ${a.title}\n${a.url}\n確認範囲 ${id==='A10'?'製造関連の印刷頁7～9、13～21。採択計画。':a.reading_scope}\n確認日 2026-10-21`;
 }).join('\n\n');
}
function finish(s,d){
 let x=88;
 for(const id of d.refs){
  const url=quotes.has(id)?quotes.get(id).source_url:extra.get(id).url;
  const page=quotePages.get(id);
  textbox(s,'ref-'+id,page?`${id} p.${page}`:id,x,961,135,31,20,{color:teal,uri:url,wrapText:false});x+=143;
 }
 textbox(s,'disclosure',wrap(d.caveat,78),88,1003,1620,63,21,{color:muted,wrapText:false});
 textbox(s,'page',String(d.number).padStart(2,'0')+' / 40',1745,1005,100,35,21,{color:muted,wrapText:false});
 const local=(d.local_sources||[]).map(p=>`${p}\nhttps://github.com/jio-n/J_research/blob/main/${p}`).join('\n\n');
 const booth=(d.booth_sources||[]).map(b=>`${b.company}\nブース ${b.booth}\n${b.url||'詳細URL未保存。主要33社台帳の保存情報から確認。'}\n出展説明の収集基準日 2026-10-16`).join('\n\n');
 const quantitative=d.signals?d.signals.map(x=>`${x.theme}: 2024年 ${x.wording_2024}件、2026年 ${x.wording_2026}件`).join('\n'):'';
 s.speakerNotes.text=`JIMTOF2026 事前調査 2026年10月22日\n公開資料に基づく整理。現地未確認。本文の要約・分析と、引用欄の原文を区別。\n\n${sourceNotes(d.refs)}\n\n${booth}\n\n${local}\n\n${quantitative}\n\n留保 ${d.caveat}`;
 index.push({number:d.number,section:d.section,title:d.title,kind:d.kind,source_ids:d.refs,quote_ids:d.quote_ids||[]});
}

for(const d of content.slides){
 const s=deck.slides.add();s.background.fill='#FFFFFF';
 textbox(s,'heading',d.title,86,54,1748,112,46,{bold:true});
 textbox(s,'context',d.context,88,178,1740,70,27,{color:muted});
 if(d.kind==='table'){
  if(d.lead)textbox(s,'main-thesis',d.lead,88,278,1730,146,51,{bold:true,color:teal});
  nativeTable(s,[d.headers,...d.rows],d.widths,d.heights,d.size,d.top||270);
 }else if(d.kind==='definition'){
  textbox(s,'definition-label','本調査の作業定義',88,273,1700,37,29,{bold:true,color:teal});
  textbox(s,'working-definition',wrap(d.definition,49),88,326,1740,185,33,{bold:true,wrapText:false});
  nativeTable(s,[d.headers,...d.rows],[430,1318],[65,80,80,80,80],28,539);
 }else if(d.kind==='chart'){
  const chart=s.charts.add('bar',{
   position:{left:92,top:282,width:1732,height:639},categories:d.signals.map(r=>r.theme),
   series:[{name:'2024年',values:d.signals.map(r=>r.wording_2024),fill:'#91ABB5'},{name:'2026年',values:d.signals.map(r=>r.wording_2026),fill:teal}],
   barOptions:{direction:'bar',grouping:'clustered',gapWidth:70},hasLegend:true,
   legend:{position:'bottom',textStyle:{fontSize:25}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:24}},
   xAxis:{textStyle:{fontSize:25}},yAxis:{textStyle:{fontSize:24},min:0,max:220},
   chartFill:'#FFFFFF',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}
  });
  applyPresentationChartFont(chart,{fontFamily:font});chartOwners.push(d.number);
 }else if(d.kind==='quotes'){
  for(let i=0;i<d.quote_ids.length;i++){
   const q=quotes.get(d.quote_ids[i]),y=258+i*173;
   textbox(s,'qid-'+q.quote_id,q.quote_id+'\n'+q.source_id,88,y,120,75,27,{bold:true,color:teal,uri:q.source_url,wrapText:false});
   textbox(s,'verbatim-'+q.quote_id,q.excerpt_original,240,y-1,1592,78,32,{bold:true});
   textbox(s,'attribution-'+q.quote_id,q.attribution+'　'+q.published_date,240,y+78,1592,30,21,{color:muted});
   textbox(s,'context-'+q.quote_id,'文脈〔要約〕：'+q.context_paraphrase,240,y+108,1592,29,22);
   textbox(s,'boundary-'+q.quote_id,'留保：'+q.not_evidence_for,240,y+139,1592,28,20,{color:warm});
  }
 }else throw Error('Unknown slide kind '+d.kind);
 finish(s,d);
}
if(deck.slides.items.length!==40)throw Error('Unexpected slide count');
await fs.writeFile(path.join(work,'text-fit-preflight.json'),JSON.stringify(fitIssues,null,2)+'\n');
if(fitIssues.length)throw Error('Text-fit estimates failed: '+JSON.stringify(fitIssues.slice(0,5)));
const draft=path.join(work,'candidate.pptx');
await(await PresentationFile.exportPptx(deck)).save(draft);
console.log('Draft exported: 40 slides, '+tableOwners.length+' native tables, 1 native chart');
const finalPath=path.join(outdir,`JIMTOF2026_AI技術動向_主張3枚と補足37枚_20261022_${revision}.pptx`);
try{
 await finalizePresentation({workspaceDir:root,candidatePath:draft,finalPath,pythonExecutable:python,
  integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],
  explicitTotalSlideCount:40,requiredNativeTableOwnerSlides:tableOwners,requiredNativeChartOwnerSlides:chartOwners,
  materializeLiteralChartWorkbooks:true,fontPolicy,verifyArtifactToolImport:true,receiptPath:path.join(work,'validation.json')});
}catch(error){
 // A denied hard-link publication occurs only after the finalizer's checks.
 if(error.code!=='EPERM'||error.syscall!=='link'||error.dest!==finalPath)throw error;
 await fs.copyFile(draft,finalPath,constants.COPYFILE_EXCL);
 await fs.writeFile(path.join(work,'publication-fallback.json'),JSON.stringify({reason:'Hard-link publication denied after checks; preserved candidate bytes by exclusive copy.',sha256:createHash('sha256').update(await fs.readFile(finalPath)).digest('hex')},null,2)+'\n');
}
const finalDeck=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<finalDeck.slides.items.length;i++){
 const png=await finalDeck.export({slide:finalDeck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(work,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered',i+1,'/',finalDeck.slides.items.length);
}
await fs.writeFile(path.join(datadir,'slide_index.json'),JSON.stringify({date:content.date,main_slides:3,appendix_slides:37,slides:index},null,2)+'\n');
const inputs=['data/research/evidence_briefing_20261022/slide_content.json','data/research/evidence_report_20261022/report_content.json','data/research/quotation_evidence_20261022/quotes.json','data/research/deep_reading_20261021/source_coverage.json','data/research/macro_20261019/major_dossiers.json','data/research/strategy_review_20261021/strategy_review.json'];
const hashes={};for(const name of inputs)hashes[name]=createHash('sha256').update(await fs.readFile(path.join(root,name))).digest('hex');
await fs.writeFile(path.join(datadir,'presentation_basis.json'),JSON.stringify({date:content.date,stage:'視察前の公開情報',source_report:content.source_report,main_slides:3,appendix_slides:37,original_excerpts:46,major_companies:33,task_categories:14,inputs:hashes,output:{path:path.relative(root,finalPath).replaceAll('\\','/'),sha256:createHash('sha256').update(await fs.readFile(finalPath)).digest('hex')},native_table_slides:tableOwners,native_chart_slides:chartOwners},null,2)+'\n');
console.log(JSON.stringify({finalPath,slides:40,nativeTables:tableOwners.length,nativeCharts:chartOwners.length}));
