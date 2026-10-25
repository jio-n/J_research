import fs from'node:fs/promises';import path from'node:path';import{fileURLToPath}from'node:url';
import{SpreadsheetFile,FileBlob}from'./_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(R,'outputs',path.basename(D),'JIMTOF2026_調査企業一覧_C列重複管理付き.xlsx')));
wb.recalculate();
for(const[sheetName,range,n]of [['AI・フィジカルAI','A1:F6','ai_overlap'],['自動化・自律化50社','A1:E6','automation_overlap'],['AI・フィジカルAI','G20:I21','comments_and_sources'],['自動化・自律化50社','G2:I6','copied_comments']]){
 const b=await wb.render({sheetName,range,scale:1.2,format:'png'});await fs.writeFile(path.join(D,'_private',n+'.png'),new Uint8Array(await b.arrayBuffer()));
}
const check=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:10},maxChars:1000});
await fs.writeFile(path.join(D,'_private/error_scan.ndjson'),check.ndjson);console.log('Rendered both sheets and shifted comment/link columns.');process.exit(0);
