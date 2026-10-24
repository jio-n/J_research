import fs from 'node:fs/promises';import path from 'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,FileBlob}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const p=JSON.parse(await fs.readFile(path.join(D,'link_plan.json'),'utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(R,p.source_workbook)));
for(const name of ['AI・フィジカルAI','自動化・自律化50社']){
 const s=wb.worksheets.getItem(name),last=name==='AI・フィジカルAI'?33:51;
 s.getRange('H1').values=[['追加技術資料']];
}
for(const l of p.additional_sources)wb.worksheets.getItem(l.sheet).getRange(l.cell).values=[[l.text]];
wb.recalculate();
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(R,'outputs',path.basename(D),'JIMTOF2026_調査企業一覧_追加技術資料付き.xlsx'));
console.log('Workbook authored; native link and table verification follows.');process.exit(0);
