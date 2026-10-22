import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile,FileBlob} from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const root=path.resolve('.'),rev=process.argv[2]||'r1';
if(!/^r\d+$/.test(rev))throw Error('Revision must be r1, r2, ...');
const skill='C:/Users/paulr/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22135/skills/presentations';
const python='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {finalizePresentation,resolvePresentationFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const data=path.join(root,'data/research/technical_guide_20261022');
const work=path.join(root,'.build/technical_guide_20261022',rev);
const out=path.join(root,'outputs/technical_guide_20261022');
await fs.mkdir(work,{recursive:true});await fs.mkdir(out,{recursive:true});
const g=JSON.parse(await fs.readFile(path.join(data,'content.json'),'utf8'));
const quotes=JSON.parse(await fs.readFile(path.join(root,'data/research/quotation_evidence_20261022/quotes.json'),'utf8')).quotes;
const qm=new Map(quotes.map(q=>[q.quote_id,q]));
const font=resolvePresentationFont({fontFamily:'Yu Gothic UI',availableFonts:['Yu Gothic UI']});
const deck=Presentation.create({slideSize:{width:1920,height:1080}});
const ink='#193647',teal='#087B81',muted='#536774',line='#CFDBDF';
const owners=[],index=[],fit=[];

function units(text){return [...text].reduce((sum,c)=>sum+(/[\u0020-\u007e]/.test(c)?0.53:1),0);}
// Wrap at phrase punctuation or word boundaries, avoiding Japanese punctuation orphans.
function wrap(text,max){
 return String(text).split('\n').map(p=>{
  const chars=[...p],lines=[];let start=0;
  while(start<chars.length){
   let end=start,used=0,lastBreak=-1;
   while(end<chars.length&&used+units(chars[end])<=max){
    used+=units(chars[end]);end++;
    if(/[ 、。・／）]/.test(chars[end-1]))lastBreak=end;
   }
   if(end===chars.length){lines.push(chars.slice(start).join(''));break;}
   if(lastBreak>start+Math.max(3,Math.floor((end-start)*0.62)))end=lastBreak;
   while(end<chars.length&&/[、。，．）]/.test(chars[end]))end++;
   if(end===start)end++;
   lines.push(chars.slice(start,end).join('').trim());start=end;
  }
  return lines.join('\n');
 }).join('\n');
}
function text(s,name,value,x,y,w,h,size=29,{bold=false,color=ink,link}={}){
 const sh=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=link?[[{run:value,link:{uri:link,isExternal:true}}]]:value;
 sh.text.style={fontSize:size,typeface:font,bold,color,insets:0,autoFit:'none',wrap:'square',lineSpacing:1.12,verticalAlignment:'top'};
 return sh;
}
function table(s,headers,rows,widths,heights,size=28,top=285){
 const vals=[headers,...rows].map((r,ri)=>r.map((v,ci)=>{
  const t=wrap(v,(widths[ci]-26)/size);
  const need=t.split('\n').length*size*1.19+22;
  if(need>heights[ri]+3)fit.push({slide:deck.slides.items.length,row:ri,col:ci,need,available:heights[ri],text:t});
  return String(v);
 }));
 const t=s.tables.add({rows:vals.length,columns:headers.length,left:86,top,width:1748,height:heights.reduce((a,b)=>a+b,0),columnWidths:widths,values:vals});
 t.borders.assign({fill:line,width:1,style:'solid'});
 for(let r=0;r<vals.length;r++){
  t.rows[r].height=heights[r];
  for(let c=0;c<headers.length;c++){
   const ce=t.getCell(r,c);ce.fill=r===0?ink:(r%2===0?'#F0F5F5':'#FFFFFF');
   ce.text.style={fontSize:size,typeface:font,bold:r===0||c===0,color:r===0?'#FFFFFF':ink,insets:11,autoFit:'none',wrap:'square',lineSpacing:1.12,verticalAlignment:'top'};
  }
 }
 owners.push(deck.slides.items.length);
}
function start(title,context){
 const s=deck.slides.add();s.background.fill='#FFFFFF';
 text(s,'heading',title,86,52,1748,86,46,{bold:true});
 text(s,'context',context,88,160,1738,84,29,{color:muted});
 return s;
}
function sourceText(qid){
 const q=qm.get(qid);return `${qid} ${q.attribution}\n${q.publisher} ${q.title} ${q.published_date}\n${q.source_url}\n掲載位置 ${q.locator}\n原文抜粋 ${q.excerpt_original}\n文脈の要約 ${q.context_paraphrase}\n留保 ${q.not_evidence_for}`;
}
function finish(s,title,{section='補足',refs=[],rows=[],note='',extra=[]}={}){
 const n=deck.slides.items.length;
 const body=['公開資料による事前調査。現地未確認。2026年10月22日。',note,
  ...refs.map(sourceText),...rows.flatMap(r=>[`${r.card_id} ${r.company} ${r.product} ブース ${r.booth}\n${r.status}\n${r.description}\n現地確認 ${r.check}`,...r.sources.map(e=>`${e.id} ${e.title}\n${e.url}\n掲載位置 ${e.locator}`)]),...extra];
 s.speakerNotes.text=body.join('\n\n');
 text(s,'footer',note||'出典URL・掲載位置はスピーカーノートに記載。2026年10月22日時点の事前調査。',88,1001,1590,49,20,{color:muted});
 text(s,'page',String(n).padStart(2,'0')+' / 22',1740,1001,100,35,21,{color:muted});
 index.push({number:n,section,title,card_ids:rows.map(r=>r.card_id),quote_ids:refs});
}

{
 const title='JIMTOF2026 技術動向の要点';
 const s=start(title,'顧客課題は「技能依存」「品質変動」「多品種対応」「工程間の分断」。AI・自動化の適用を担当タスクで整理する。');
 table(s,['技術領域','顧客ニーズ','技術の方向','企業・製品例'],g.trends,[330,310,520,588],[61,153,153,153,153],28,259);
 text(s,'conclusion','全体最適化を目指す開発と、製品化・展示予定の個別機能を対応付けて調査する。',88,948,1740,45,29,{bold:true,color:teal});
 finish(s,title,{section:'メイン',refs:['Q02','Q05','Q06','Q11','Q14'],rows:g.categories.flatMap(c=>c.rows),note:'資料横断の分析。共同開発計画、既存製品、2026展示予定を含む。実演性能は現地未確認。'});
}
{
 const title='主要メーカーの開発対象と実現技術';
 const s=start(title,'工作機械・CNC・ソフトウェア各社の担当領域を比較。データ基盤と共同開発の計画は、展示機能と分けて示す。');
 table(s,['企業','ターゲット','公開製品・展示告知','共同開発・今後の方向'],g.company_strategy,[254,286,650,558],[60,128,137,128,128,128],27,254);
 finish(s,title,{section:'メイン',refs:['Q02','Q05','Q06','Q26','Q11'],extra:g.majors.filter(m=>['DMG森精機','ヤマザキマザック','ファナック','オークマ','シーメンス'].includes(m.company)).map(m=>m.company+' '+m.booth+'\n'+m.urls.join('\n')),note:'ファナック・日立の実証先は日立の工場。マザックの工程設計AIとDMGのGENIACは開発計画。'});
}
{
 const title='視察優先ブースと確認内容';
 const s=start(title,'調査目的への適合と、方式の違いを比較できる組合せを優先。各ブースで確認する対象を製品・機能まで指定する。');
 table(s,['調査テーマ','企業・製品・ブース','比較・確認内容'],g.priorities,[325,720,703],[59,95,95,95,95,95,95,95],27,254);
 finish(s,title,{section:'メイン',rows:g.categories.flatMap(c=>c.rows),note:'会場内の移動順は未設定。共同開発AIや個別製品の展示有無を含め、告知の範囲を現地確認する。'});
}
for(const c of g.categories){
 const title=c.id+' '+c.name;
 const s=start(title,'顧客ニーズ：'+c.need);
 table(s,['企業・製品・ブース','対象タスク・実現方式','技術内容','現地確認事項'],c.rows.map(r=>[
  r.company+'\n'+r.product+'\n'+r.booth,
  r.task+'。方式：'+r.method,
  r.description+'（'+r.status+'）',r.check]),[370,310,625,443],[63,194,194,194],28,270);
 text(s,'technical-distinction',c.distinction,88,934,1745,62,26,{bold:true,color:teal});
 finish(s,title,{rows:c.rows,note:'出展予定と製品資料を照合。個別展示未確認の機能は明示。製品版・性能・人の介入は現地確認。'});
}
{
 const title='フィジカルAIの調査・報告基準';
 const s=start(title,'作業定義：'+g.physical_ai.definition);
 table(s,['評価項目','確認・記録する内容'],g.physical_ai.criteria,[370,1378],[62,118,118,118,118],30,278);
 text(s,'definition-note',g.physical_ai.note,88,837,1735,112,29,{bold:true,color:teal});
 finish(s,title,{refs:['Q07','Q41'],note:'本調査の作業定義であり、業界統一規格ではない。TR-20W・3D形状認識加工・ファナックの違いはT06を参照。'});
}
for(const [title,qids] of g.evidence_groups){
 const s=start('原文根拠：'+title,'本文の解釈を確認するための短い原文抜粋。発言者・記事種別・文脈を併記する。全46抜粋は別添HTML原文集に収録。');
 for(let i=0;i<qids.length;i++){
  const q=qm.get(qids[i]),y=272+i*171;
  text(s,'quote-'+q.quote_id,'「'+q.excerpt_original+'」',88,y,1740,76,32,{bold:true});
  text(s,'attribution-'+q.quote_id,q.quote_id+'　'+q.attribution+'　'+q.published_date,88,y+72,1740,36,23,{color:muted,link:q.source_url});
  text(s,'meaning-'+q.quote_id,'文脈〔要約〕：'+q.context_paraphrase,88,y+113,1740,47,25);
 }
 finish(s,'原文根拠：'+title,{refs:qids,note:'原文の連続部分を抜粋。開発構想・研究方針の表明を、製品性能や展示での達成証明とは扱わない。'});
}
const groups=[g.majors.slice(0,9),g.majors.slice(9,17),g.majors.slice(17,25),g.majors.slice(25)];
for(let i=0;i<groups.length;i++){
 const title='主要33社の展示索引 '+(i+1)+' / 4';
 const s=start(title,'大手の展示を追加で確認する索引。AI機能が未確認の場合も、実際の加工・自動化・工具・計測の展示で位置付ける。');
 const rows=groups[i].map(m=>[(m.company==='ベッコフオートメーション'?'ベッコフ':m.company==='Hexagon Manufacturing Intelligence'?'Hexagon':m.company)+'　'+m.booth,m.exhibit,m.task,m.check]);
 table(s,['企業・ブース','展示品・ソリューション','対象タスク','確認事項'],rows,[320,440,320,668],[58,...rows.map(()=>i===0?79:80)],25,i===0?220:252);
 finish(s,title,{extra:groups[i].map(m=>m.company+' '+m.booth+'\n'+m.exhibit+'\n'+m.urls.join('\n')),note:'出展者の公開説明を要約。AI機能の未確認と、AIを使用しないという確認は区別。東京精密は展示内容未取得。'});
}
{
 const title='調査範囲と2024年比較';
 const s=start(title,'全出展者の照合と同名企業パネルをマクロ分析の土台とし、詳細な方式比較へ展開した。');
 table(s,['出展説明の用語群','2024年','2026年'],g.signals.slice(0,4).map(x=>[x.theme,String(x.wording_2024),String(x.wording_2026)]),[1048,350,350],[61,80,80,80,80],29,264);
 text(s,'scope','集計対象：両年に説明文がある同名538件。複数カテゴリの重複あり。\n技術索引344件、詳細比較57件、本編は方式差を比較する33行。主要企業33社を別途確認。',88,697,1740,116,30,{bold:true});
 text(s,'limits','文言の増加は、採用率・性能向上・新機能数を表さない。顧客ニーズは公開説明からの課題整理。\n説明文や詳細URLがない企業もあり、全社・全製品の技術を完全に分解した調査ではない。',88,841,1740,110,28,{color:muted});
 finish(s,title,{extra:['data/research/strategy_review_20261021/exhibitor_coverage_all_2024_2026.csv','data/research/strategy_review_20261021/macro_wording_signals.csv','data/research/report_v0/technology_directory.json','data/research/report_v0/case_comparison.json'],note:'2024・2026照合は2,427掲載行。候補索引全344件と出典リンクはHTML版に掲載。'});
}
if(deck.slides.items.length!==22)throw Error('Expected 22 slides, got '+deck.slides.items.length);
await fs.writeFile(path.join(work,'text-fit-preflight.json'),JSON.stringify(fit,null,2)+'\n');
if(fit.length)throw Error('Estimated text overflow: '+JSON.stringify(fit.slice(0,15)));
const candidate=path.join(work,'candidate.pptx');
await(await PresentationFile.exportPptx(deck)).save(candidate);
const finalPath=path.join(out,`JIMTOF2026_技術動向と視察ガイド_主篇3枚_補足19枚_20261022_${rev}.pptx`);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit',...owners.flatMap(n=>['--require-native-table-slide',String(n)])],
 explicitTotalSlideCount:22,requiredNativeTableOwnerSlides:owners,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(work,'validation.json')});
const finalDeck=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<finalDeck.slides.items.length;i++){
 const png=await finalDeck.export({slide:finalDeck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(work,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
const sha256=createHash('sha256').update(await fs.readFile(finalPath)).digest('hex');
await fs.writeFile(path.join(data,'presentation_basis.json'),JSON.stringify({date:g.date,main_slides:3,appendix_slides:19,technical_categories:11,comparison_rows:33,major_companies:33,atlas_entries:344,native_table_slides:owners,output:{path:path.relative(root,finalPath).replaceAll('\\','/'),sha256},slides:index},null,2)+'\n');
console.log(JSON.stringify({finalPath,slides:22,tables:owners.length,sha256}));
