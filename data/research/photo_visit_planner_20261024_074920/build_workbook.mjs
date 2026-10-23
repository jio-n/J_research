import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from './_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..'),O=path.join(R,'outputs',path.basename(D));
const data=JSON.parse(await fs.readFile(path.join(D,'transcription.json'),'utf8'));
const wb=Workbook.create(),widths=[30,16,7,44,26,63,75];
for(const [name,items]of [['AI・フィジカルAI',data.ai],['自動化・自律化50社',data.automation]]){
 const sh=wb.worksheets.add(name),last=items.length+1;
 sh.showGridLines=false;
 sh.getRange(`A1:G${last}`).values=[data.headers,...items.map(x=>x.values)];
 sh.getRange(`A1:G${last}`).format={font:{name:'Yu Gothic UI',size:11,color:'#243342'},wrapText:true,verticalAlignment:'top'};
 const table=sh.tables.add(`A1:G${last}`,true,'PhotoTable'+wb.worksheets.items.length);
 table.style='TableStyleLight9';table.showFilterButton=true;
 sh.getRange('A1:G1').format={fill:'#E7EDF2',font:{name:'Yu Gothic UI',size:11,bold:true,color:'#20374A'},rowHeight:30,verticalAlignment:'center',horizontalAlignment:'center'};
 widths.forEach((v,i)=>sh.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${last}`).format.columnWidth=v);
 sh.getRange(`B2:C${last}`).format.horizontalAlignment='center';
 sh.getRange(`A2:G${last}`).format.rowHeight=name.startsWith('AI')?150:36;
 items.forEach((x,i)=>x.values.forEach((v,j)=>{if(String(v??'').includes('読めない'))sh.getRange(`${String.fromCharCode(65+j)}${i+2}`).format.fill='#FFF0C2';}));
 sh.freezePanes.freezeRows(1);sh.freezePanes.freezeColumns(2);
}
wb.recalculate();
await fs.mkdir(O,{recursive:true});
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(O,'JIMTOF2026_ユーザー選定_調査企業一覧.xlsx'));
console.log(JSON.stringify({sheets:2,ai_items:data.ai.length,automation:data.automation.length}));
process.exit(0);
