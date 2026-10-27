import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const dir=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(dir,'../../..');
const out=path.join(root,'outputs',path.basename(dir));
await fs.mkdir(out,{recursive:true});
await fs.mkdir(path.join(dir,'_private'),{recursive:true});
const prior=JSON.parse(await fs.readFile(path.join(root,'data/research/visits_csv_update_20261027_093945/app_data.json'),'utf8'));
const specs=[
 ['H001','ファナック株式会社','S2001','南2ホール／1F',1,'音声メモ欄'],
 ['H002','三菱電機株式会社','S2003','南2ホール／1F',1,'音声メモ欄'],
 ['H003','シチズンマシナリー','S2002','南2ホール／1F',1,'投稿末尾の独立メモ。ブース・エリアは事前台帳で補完し、メモ本文の記載とは区別'],
 ['H004','モリマシナリー株式会社','S3048','南3ホール／4F',2,'音声メモ欄'],
 ['H005','ヤマザキマザック株式会社','E1001','東1ホール／1F',3,'音声メモ欄'],
 ['H006','オークマ株式会社','E3028','東3ホール／1F',3,'音声メモ欄'],
 ['H007','DMG森精機株式会社','E8005','東8ホール／1F',4,'音声メモ欄'],
 ['U001','未確定','','',2,'投稿末尾の途中文。表記から企業やブースを推定せず、訪問社数から除外']
];
const records=[];
for(const [id,company,booth,area,batch,mapping] of specs){
 let raw=await fs.readFile(path.join(dir,'raw',id+'.txt'),'utf8');
 raw=raw.replace(/\r\n/g,'\n').replace(/\n$/,'');
 const base=prior.companies.find(c=>c.booth===booth);
 if(booth && !base) throw Error('Booth missing from prior list: '+booth);
 records.push({id,company,booth,area,batch,mapping,status:id.startsWith('H')?'訪問実績':'帰属未確定',raw,sha256:crypto.createHash('sha256').update(raw).digest('hex'),source:'本チャットで本人が分割投稿した当日メモ',sourceCompany:base?.company??'',companyUrl:base?.items?.[0]?.companyUrl??''});
}
const data={version:'20261027_175238',visitDate:'2026-10-27',uploadComplete:true,receivedBatches:4,visitedCompanies:7,unassignedMemos:1,policy:'メモ本文は要約・言換え・誤字修正・事実確認による改変をしない。元の改行を保持。抽出境界の空白行とファイル末尾改行は本文に含めない。事前の展示情報・質問・空欄は当日メモへ混ぜない。',records};
await fs.writeFile(path.join(dir,'hearing_records.json'),JSON.stringify(data,null,2),'utf8');

let md='# JIMTOF2026 当日ヒアリングメモ（原文）\n\n';
md+='メモのある7社を訪問実績として抽出。4回の投稿を受領し、企業・ブースが未確定の途中文1件も別枠で収録した。\n\n';
md+='以下のコードブロック内は本人のメモ原文。誤字・表記揺れ・推測・感想・途中の文を修正していない。事前の展示情報と質問、音声メモ欄が空の企業は収録していない。見出しと索引は整理用に追加した。発言・技術仕様の裏付け確認や分析は未実施。\n\n';
md+='|記録ID|企業|ブース|エリア|受領回|\n|---|---|---|---|---|\n';
for(const r of records.filter(r=>r.status==='訪問実績')) md+=`|${r.id}|${r.company}|${r.booth}${r.id==='H003'?'（事前台帳補完）':''}|${r.area}|第${r.batch}回|\n`;
for(const r of records){
 md+=`\n## ${r.id} ${r.company}${r.booth?'｜'+r.booth:''}\n\n`;
 md+=`受領：第${r.batch}回。${r.mapping}。\n\n`;
 md+='```text\n'+r.raw+'\n```\n';
}
await fs.writeFile(path.join(out,'JIMTOF2026_当日ヒアリング原文.md'),md,'utf8');

const wb=Workbook.create();
const index=wb.worksheets.add('訪問実績');
const notes=wb.worksheets.add('メモ原文');
for(const sh of[index,notes]){sh.showGridLines=false;sh.tabColor='#24445C';}
index.getRange('A2').values=[['JIMTOF2026 当日ヒアリング記録']];
index.getRange('A3').values=[['メモあり7社。帰属未確定1件は訪問実績に含めない。']];
index.getRange('A4').values=[['原文は要約・誤字修正なし。事前の展示情報・質問は当日の記録から除外。']];
const ih=['記録ID','企業名','ブース','エリア','受領回','原文行数','原文シート行','紐付け補足'];
index.getRange('A6:H6').values=[ih];
notes.getRange('A2').values=[['当日の音声メモ 原文']];
notes.getRange('A3').values=[['F列を原文行番号順に改行で連結すると全文を復元できる。空白行も保持。']];
notes.getRange('A4').values=[['出典：本人の本チャット投稿（全4回）。企業・ブース・状態・行番号は整理用の付加情報。']];
notes.getRange('A6:F6').values=[['記録ID','企業名','ブース','状態','原文行番号','メモ原文（要約・修正なし）']];
const nrows=[];const locations={};
for(const r of records){
 const start=nrows.length+7;
 for(const [i,line] of r.raw.split('\n').entries()) nrows.push([r.id,r.company,r.booth||'未確定',r.status,i+1,line]);
 locations[r.id]={start,end:nrows.length+6};
}
notes.getRange(`A7:F${nrows.length+6}`).values=nrows;
const visited=records.filter(r=>r.status==='訪問実績');
const irows=visited.map(r=>[r.id,r.company,r.booth,r.area,r.batch,r.raw.split('\n').length,`${locations[r.id].start}〜${locations[r.id].end}行`,r.id==='H003'?'ブース・エリアは事前台帳補完':'本人の企業・ブース見出しに紐付け']);
index.getRange('A7:H13').values=irows;
index.getRange('A16').values=[['帰属未確定のメモ（訪問社数から除外）']];
index.getRange('A17:C17').values=[['記録ID','原文','取扱い']];
index.getRange('A18:C18').values=[['U001',records.at(-1).raw,'企業・ブースを推定しない']];
index.getRange('A21').values=[['空欄の企業は当日未訪問として抽出対象外。予定一覧そのものは変更していない。']];

for(const [sh,lastCol,lastRow] of[[index,'H',21],[notes,'F',nrows.length+6]]){
 sh.getRange(`A1:${lastCol}${lastRow}`).format.font={name:'Arial',size:11,color:'#243746'};
 sh.getRange(`A1:${lastCol}${lastRow}`).format.verticalAlignment='center';
 sh.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#213F56'};
 sh.getRange('A2').format.rowHeight=26;
 sh.getRange(`A3:${lastCol}4`).format.font={name:'Arial',size:10,color:'#526573'};
 sh.getRange(`A6:${lastCol}6`).format={fill:'#28465B',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:29,horizontalAlignment:'center'};
 sh.freezePanes.freezeRows(6);
}
for(const [c,w] of[['A',12],['B',38],['C',12],['D',24],['E',10],['F',12],['G',18],['H',44]]) index.getRange(`${c}1:${c}21`).format.columnWidth=w;
index.getRange('A7:H13').format.rowHeight=32;
index.getRange('E7:F13').format.horizontalAlignment='right';
index.getRange('G7:G13').format.horizontalAlignment='center';
index.getRange('A16').format.font={name:'Arial',size:11,bold:true};
index.getRange('A17:C17').format={fill:'#E5ECF0',font:{name:'Arial',size:11,bold:true},rowHeight:25};
index.getRange('B18').format.wrapText=true;
index.getRange('A18:H18').format.rowHeight=44;
const table=index.tables.add('A6:H13',true,'VisitedCompanies');table.showFilterButton=true;
for(const [c,w] of[['A',11],['B',31],['C',11],['D',14],['E',12],['F',110]]) notes.getRange(`${c}1:${c}${nrows.length+6}`).format.columnWidth=w;
notes.getRange(`A7:F${nrows.length+6}`).format.verticalAlignment='top';
notes.getRange(`F7:F${nrows.length+6}`).format.wrapText=true;
for(const [i,row] of nrows.entries()){
 const line=row[5];
 const weight=[...line].reduce((n,c)=>n+(c.charCodeAt(0)>255?2:1),0);
 const height=line?Math.max(26,Math.ceil(weight/96)*19+8):22;
 notes.getRange(`A${i+7}:F${i+7}`).format.rowHeight=height;
 if(row[4]===1)notes.getRange(`A${i+7}:F${i+7}`).format.borders={top:{style:'medium',color:'#9DB0BD'}};
 if(row[3]==='帰属未確定')notes.getRange(`A${i+7}:E${i+7}`).format.fill='#FFF1D2';
}
const nt=notes.tables.add(`A6:F${nrows.length+6}`,true,'HearingLines');nt.showFilterButton=true;

wb.recalculate();
const inspection=await wb.inspect({kind:'table',range:'訪問実績!A6:H13',include:'values,formulas',tableMaxRows:8,tableMaxCols:8,maxChars:5000});
await fs.writeFile(path.join(dir,'_private/inspection.ndjson'),inspection.ndjson,'utf8');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:2000});
await fs.writeFile(path.join(dir,'_private/formula_scan.ndjson'),errors.ndjson,'utf8');
for(const [name,sheet,range] of[['index','訪問実績','A1:H21'],['raw','メモ原文','A6:F14'],['raw_dmg','メモ原文',`A${locations.H007.start}:F${locations.H007.start+6}`]]){
 const img=await wb.render({sheetName:sheet,range,scale:1,format:'png'});
 await fs.writeFile(path.join(dir,'_private',name+'.png'),new Uint8Array(await img.arrayBuffer()));
}
const x=await SpreadsheetFile.exportXlsx(wb);await x.save(path.join(out,'JIMTOF2026_当日ヒアリング原文.xlsx'));
await fs.writeFile(path.join(dir,'layout.json'),JSON.stringify({locations,lineRows:nrows.length,visitedCompanies:7,unassignedMemos:1},null,2),'utf8');
console.log(JSON.stringify({outputs:out,visited:7,unassigned:1,lineRows:nrows.length}));
