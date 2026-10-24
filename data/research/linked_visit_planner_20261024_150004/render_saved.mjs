import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,FileBlob}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(R,'outputs',path.basename(D),'JIMTOF2026_ユーザー選定_調査企業一覧_リンク付き.xlsx')));
wb.recalculate();
const views=[['AI・フィジカルAI','A1:E4','ai_names'],['AI・フィジカルAI','F1:G3','ai_technology'],['AI・フィジカルAI','A32:G33','corrected_name'],['自動化・自律化50社','A1:G7','automation']];
for(const[sheetName,range,n]of views){const b=await wb.render({sheetName,range,scale:1.2,format:'png'});await fs.writeFile(path.join(D,'_private',n+'.png'),new Uint8Array(await b.arrayBuffer()));}
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:1200});
await fs.writeFile(path.join(D,'_private/final_error_scan.ndjson'),errors.ndjson);
console.log(JSON.stringify({saved_file_rendered:views.length}));process.exit(0);
