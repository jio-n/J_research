import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {SpreadsheetFile,FileBlob} from './_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const file=path.join(R,'outputs',path.basename(D),'JIMTOF2026_関心テーマ別_訪問計画.xlsx');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const views=[['訪問計画','A2:G9','final_identity'],['訪問計画','M6:P9','final_technology'],['訪問計画','Q6:W9','final_inputs'],['技術詳細','A6:E14','final_detail'],['出典','A6:F9','final_sources'],['使い方','A2:C12','final_guide']];
for(const [sheetName,range,name]of views){
 const img=await wb.render({sheetName,range,scale:1.2,format:'png'});
 await fs.writeFile(path.join(D,'_private/qa',name+'.png'),new Uint8Array(await img.arrayBuffer()));
}
console.log(JSON.stringify({saved_workbook_rendered:true,views:views.map(v=>({sheet:v[0],range:v[1]}))}));
process.exit(0);
