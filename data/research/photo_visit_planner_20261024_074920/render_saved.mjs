import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {SpreadsheetFile,FileBlob} from './_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(R,'outputs',path.basename(D),'JIMTOF2026_ユーザー選定_調査企業一覧.xlsx')));
const views=[['AI・フィジカルAI','A1:E5','identity'],['AI・フィジカルAI','F1:G5','comments'],['AI・フィジカルAI','F19:G20','unreadable'],['AI・フィジカルAI','D26:G26','long_questions'],['AI・フィジカルAI','A30:G33','last_items'],['自動化・自律化50社','A1:G7','automation'],['自動化・自律化50社','A46:G51','automation_last']];
for(const [sheetName,range,name]of views){const img=await wb.render({sheetName,range,scale:1.3,format:'png'});await fs.writeFile(path.join(D,'_private',name+'.png'),new Uint8Array(await img.arrayBuffer()));}
await fs.writeFile(path.join(D,'render_verification.json'),JSON.stringify({engine:'artifact-tool, reimport of final Excel file',views},null,2));
console.log(JSON.stringify({rendered:views.length}));process.exit(0);
