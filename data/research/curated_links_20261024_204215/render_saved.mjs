import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,FileBlob}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(R,'outputs',path.basename(D),'JIMTOF2026_調査企業一覧_追加技術資料付き.xlsx')));
wb.recalculate();
for(const[sheetName,range,n]of [['AI・フィジカルAI','F1:H5','comments_and_sources'],['AI・フィジカルAI','F23:H25','control_sources'],['AI・フィジカルAI','A1:E4','company_and_items'],['自動化・自律化50社','A1:H6','automation']]){
 const b=await wb.render({sheetName,range,scale:1.1,format:'png'});await fs.writeFile(path.join(D,'_private',n+'.png'),new Uint8Array(await b.arrayBuffer()));
}
console.log('Rendered 4 views of final saved workbook.');process.exit(0);
