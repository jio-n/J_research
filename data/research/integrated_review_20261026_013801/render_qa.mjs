import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,FileBlob}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),O=path.resolve(D,'../../../outputs',path.basename(D)),qa=path.join(D,'_private/qa');await fs.mkdir(qa,{recursive:true});const log=[];
for(const plan of ['visit_plan.json','additional_workbook_plan.json']){
 const p=JSON.parse(await fs.readFile(path.join(D,'_private',plan+'.final.json'),'utf8')),wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(O,p.fileName)));
 for(const [i,s]of p.sheets.entries()){
  const range=s.kind==='notes'?'A1:B5':s.kind==='details'?'C1:H3':s.kind==='candidates'?'A1:H4':s.kind==='sources'?'A1:F4':s.kind==='audit'?'A1:F4':s.kind==='excluded'?'A1:F4':s.name==='閲覧_自動化・自律化'?'A1:F6':'A1:F4';
  const blob=await wb.render({sheetName:s.name,range,scale:1,format:'png'}),file=`${plan.startsWith('visit')?'visit':'extra'}-${i+1}.png`;await fs.writeFile(path.join(qa,file),new Uint8Array(await blob.arrayBuffer()));log.push({sheet:s.name,range,file});
 }
 if(plan.startsWith('visit')){const s=p.sheets[1],r=s.values.findIndex(x=>x[0].includes('TPR'))+2,range=`D${r}:I${r}`;const b=await wb.render({sheetName:s.name,range,scale:1,format:'png'});await fs.writeFile(path.join(qa,'TPR-detail.png'),new Uint8Array(await b.arrayBuffer()));log.push({sheet:s.name,range,file:'TPR-detail.png'});}
}
await fs.writeFile(path.join(D,'render_verification.json'),JSON.stringify({representative_saved_workbook_ranges:log},null,2));console.log(JSON.stringify(log));process.exit(0);
