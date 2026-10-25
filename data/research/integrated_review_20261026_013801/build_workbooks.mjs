import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,Workbook}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..'),OUT=path.join(R,'outputs',path.basename(D));
const jobs=[['visit_plan.json','JIMTOF2026_訪問先一覧_コメント統合・企業別閲覧.xlsx'],['additional_workbook_plan.json','JIMTOF2026_未掲載候補一覧_別冊.xlsx']];
const col=n=>{let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s};
const font={name:'Yu Gothic UI',size:11,color:'#243342'};
function widths(s){
 if(['search','view'].includes(s.kind))return[30,16,30,17,49,28,64,77,56];
 if(s.kind==='candidates')return[31,17,15,47,17,18,18,18,28,65,64,52,45,76,42,64,18,17,45,48,18];
 if(s.kind==='details')return[18,31,45,56,57,68,59,58,72,38,55,82,48,72,45];
 if(s.kind==='excluded')return[34,18,30,55,75,50];
 if(s.kind==='audit')return[18,33,18,50,30,50,50];
 if(s.kind==='sources')return[18,32,47,85,38,60,23,34];
 return[28,105];
}
function lines(value,width){return String(value??'').split('\n').reduce((n,t)=>n+Math.max(1,Math.ceil([...t].reduce((k,c)=>k+(c.charCodeAt(0)>255?2:1),0)/(width-2))),0)}
for(const[planName,fileName]of jobs){
 if(process.argv[2]&&process.argv[2]!==planName)continue;
 const p=JSON.parse(await fs.readFile(path.join(D,planName),'utf8')),wb=Workbook.create();
 if(planName==='additional_workbook_plan.json'){
  const detail=p.sheets.find(s=>s.kind==='details'),extra=JSON.parse(await fs.readFile(path.join(D,'additional_candidates.json'),'utf8'));
  const sourceRows=[];
  for(const x of extra.items.filter(x=>!x.user_excluded)){
   const seen=new Set();for(const src of x.sources??[]){if(!src.url)continue;const id=src.url+'|'+(src.locator??'');if(seen.has(id))continue;seen.add(id);
    sourceRows.push([x.id,x.company,src.title??'原典',src.url,src.publisher??'未記載',src.locator??'位置未記載',src.checked_date??x.as_of??'未記載',x.current_review]);
   }
  }
  detail.values.forEach(v=>v[13]='根拠台帳をIDで絞り込み');
  p.sheets.splice(p.sheets.length-1,0,{name:'根拠台帳',headers:['ID','企業名','資料名','原典URL','発行者','掲載位置','過去の確認日','今回の確認範囲'],values:sourceRows,kind:'sources',merges:[]});
  sourceRows.forEach((v,i)=>p.links.push({sheet:'根拠台帳',cell:`C${i+2}`,url:v[3],tip:v[4]+'｜'+v[5]}));
 }
 const renders=[];
 for(const [si,s]of p.sheets.entries()){
  const sh=wb.worksheets.add(s.name),last=s.values.length+1,lastCol=col(s.headers.length-1),w=widths(s);
  const all=sh.getRange(`A1:${lastCol}${last}`);all.values=[s.headers,...s.values];all.format.font=font;all.format.wrapText=true;all.format.verticalAlignment='top';
  all.format.borders={preset:'all',style:'thin',color:'#DCE4EB'};
  const header=sh.getRange(`A1:${lastCol}1`);header.format.fill='#E6EEF4';header.format.font={...font,bold:true,color:'#17374D'};header.format.rowHeight=32;header.format.verticalAlignment='center';
  for(let c=0;c<s.headers.length;c++)sh.getRange(`${col(c)}1:${col(c)}${last}`).format.columnWidth=w[c]??48;
  for(let i=0;i<s.values.length;i++){
   const n=Math.max(...s.values[i].map((v,c)=>lines(v,w[c]??48)));
   sh.getRange(`A${i+2}:${lastCol}${i+2}`).format.rowHeight=Math.min(390,Math.max(s.kind==='notes'?42:32,n*15+10));
  }
  sh.freezePanes.freezeRows(1);sh.freezePanes.freezeColumns(s.kind==='notes'?1:2);
  if(s.kind!=='view'&&s.kind!=='notes'&&s.values.length){const t=sh.tables.add(`A1:${lastCol}${last}`,true,'IRTable'+(si+1));t.style='TableStyleLight9';t.showFilterButton=true;}
  if(s.kind==='candidates')sh.getRange(`Q2:S${last}`).format.fill='#FFF6DA';
  if(s.kind==='excluded')sh.getRange(`F2:F${last}`).format.fill='#FFF6DA';
  if(['search','view'].includes(s.kind)){
   for(let i=0;i<s.values.length;i++){
    if(s.values[i][3]==='訪問候補')sh.getRange(`D${i+2}`).format.fill='#DDEFE6';
   }
  }
  for(const h of s.highlights??[])sh.getRange(h.cell).format.fill=h.color;
  for(const range of s.merges??[]){sh.mergeCells(range);sh.getRange(range).format.verticalAlignment='center';}
  for(const l of p.links.filter(l=>l.sheet===s.name))sh.getRange(l.cell).format.font={...font,color:'#0563C1',underline:'single'};
 }
 wb.recalculate();
 const check=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:1000});
 await fs.writeFile(path.join(D,'_private',planName+'.errors.ndjson'),check.ndjson);
 await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(OUT,fileName));
 await fs.writeFile(path.join(D,'_private',planName+'.final.json'),JSON.stringify({...p,fileName},null,2));
 console.log(JSON.stringify({fileName,sheets:p.sheets.map(s=>({name:s.name,rows:s.values.length,merges:(s.merges??[]).length}))}));
}
process.exit(0);
