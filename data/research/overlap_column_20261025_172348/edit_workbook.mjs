import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,Workbook}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..'),p=JSON.parse(await fs.readFile(path.join(D,'link_plan.json'),'utf8'));
const wb=Workbook.create();
for(const s of p.sheets){
 const sh=wb.worksheets.add(s.name),last=s.values.length+1;
 sh.getRange(`A1:I${last}`).values=[s.headers,...s.values];
}
wb.recalculate();
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(D,'_private/authored.xlsx'));
console.log('C column inserted in two sheets.');process.exit(0);
