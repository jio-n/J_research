import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {SpreadsheetFile,FileBlob} from './_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..');
const file=path.join(R,'outputs',path.basename(D),'JIMTOF2026_関心テーマ別_訪問計画.xlsx');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const views=[['訪問計画','A2:G9','final_identity'],['訪問計画','H6:P7','final_nagase'],['訪問計画','Q6:W9','final_inputs'],['技術詳細','A24:E31','final_history'],['訪問除外記録','A2:G10','final_exclusions'],['訪問除外記録','H6:M10','final_exclusion_context'],['出典','A6:F9','final_sources'],['抽出再点検','A2:H10','final_gap_review'],['使い方','A2:C12','final_guide']];
views.push(['訪問計画','P6:P7','final_questions'],['訪問除外記録','A21:C26','final_booth_suffixes']);
for(const [sheetName,range,name]of views){
 const img=await wb.render({sheetName,range,scale:1.2,format:'png'});
 await fs.writeFile(path.join(D,'_private/qa',name+'.png'),new Uint8Array(await img.arrayBuffer()));
}
console.log(JSON.stringify({saved_workbook_rendered:true,views:views.map(v=>({sheet:v[0],range:v[1]}))}));
process.exit(0);
