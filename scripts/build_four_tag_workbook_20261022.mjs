process.on('uncaughtException',e=>{console.error(String(e.stack||e).split('\n').map(s=>s.slice(0,500)).join('\n'));process.exit(1);});
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath,pathToFileURL} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const moduleDir=process.env.ARTIFACT_NODE_MODULES||path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const {Workbook,SpreadsheetFile}=await import(pathToFileURL(path.join(moduleDir,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const data=JSON.parse(await fs.readFile(path.join(root,'data/research/four_tag_20261022/research.json'),'utf8'));
const out=path.join(root,'outputs/four_tag_20261022'),qa=path.join(root,'.build/four_tag_20261022/workbook_qa');
await fs.mkdir(out,{recursive:true});await fs.mkdir(qa,{recursive:true});
const wb=Workbook.create(),font='Yu Gothic UI',tags=['AI','フィジカルAI','自律化','自動化'];
const col=n=>{let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const cellText=v=>String(v??'');
const quote=s=>String(s).replace(/"/g,'""');
const dateValue=s=>/^\d{4}-\d{2}-\d{2}$/.test(s||'')?Date.parse(s+'T00:00:00Z')/86400000+25569:s;

function make(name,title,note,headers,rows,widths){
 const sh=wb.worksheets.add(name);sh.showGridLines=false;
 const end=col(headers.length),last=rows.length+5;
 sh.getRange(`A1:${end}${last}`).format={font:{name:font,size:10,color:'#17334B'},verticalAlignment:'top',wrapText:true};
 sh.getRange('A1').values=[[title]];sh.getRange('A1').format.font={name:font,size:16,bold:true,color:'#153F60'};sh.getRange(`A1:${end}1`).format.rowHeight=30;
 sh.getRange('A2').values=[[note]];sh.getRange('A1:A2').format.wrapText=false;sh.getRange(`A2:${end}2`).format.rowHeight=22;sh.getRange(`A2:${end}2`).format.font={name:font,size:10,color:'#546B7A'};
 sh.getRange(`A5:${end}${last}`).values=[headers,...rows];
 const table=sh.tables.add(`A5:${end}${last}`,true,'ResearchTable_'+wb.worksheets.items.length);table.showFilterButton=true;
 sh.getRange(`A5:${end}5`).format={fill:'#174D77',font:{name:font,size:10,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:34,verticalAlignment:'center',horizontalAlignment:'center'};
 widths.forEach((w,i)=>sh.getRange(`${col(i+1)}1:${col(i+1)}${last}`).format.columnWidth=w);
 rows.forEach((r,i)=>{
  let lines=Math.max(...r.map((v,j)=>String(v??'').split('\n').reduce((n,t)=>n+Math.max(1,Math.ceil([...t].reduce((sum,c)=>sum+(c.charCodeAt(0)>255?1.8:1),0)/Math.max(5,widths[j]-2))),0)));
  sh.getRange(`A${i+6}:${end}${i+6}`).format.rowHeight=Math.max(name==='訪問選定'?42:26,Math.min(380,lines*14+8));
 });
 sh.freezePanes.freezeRows(5);sh.freezePanes.freezeColumns(name==='訪問選定'?4:2);
 return sh;
}

const sourceMap=new Map();
for(const x of data.items)for(const s of x.sources){
 let v=sourceMap.get(s.url);if(!v){v={...s,aliases:[],items:[]};sourceMap.set(s.url,v);}
 if(s.source_id&&!v.aliases.includes(s.source_id))v.aliases.push(s.source_id);
 if(!v.items.includes(x.id))v.items.push(x.id);
 if(s.short_quote)v.short_quote=s.short_quote;
}
const techRows=[],techStarts=new Map();
const aspects=[['対象タスク','task'],['顧客ニーズ〈分析〉','need'],['入力・取得データ','input'],['技術・判断の仕組み','method'],['出力・実行','output'],['人の準備・承認・例外','human'],['新規性・適応能力','advance'],['出展の根拠・提供段階','exhibit_note'],['未確認・適用限界','limits'],['現地の確認事項〈分析〉','check']];
for(const x of data.items){techStarts.set(x.id,techRows.length+6);for(const [label,key]of aspects)techRows.push([x.id,x.company,x.item,label,key==='exhibit_note'?`${x.exhibit}／${x.exhibit_note}\n提供段階：${x.stage}`:cellText(x[key]),x.depth,x.source_ids.join(' / ')]);}
const headers=['訪問判断','自分優先','候補ID','企業','小間','アイテム','AI','フィジカルAI','自律化','自動化','おすすめ','展示確度','対象タスク','実現方式','おすすめ理由〈分析〉','現地の確認事項〈分析〉','確認深度','当日メモ','個別展示の補足','代表の出典URL','技術詳細の行','根拠資料ID'];
const mainRows=data.items.map(x=>['未選定','',x.id,x.company,x.booths.join(' / '),x.item,...tags.map(t=>x.tags[t].status),x.recommendation,x.exhibit,x.task,x.method,x.recommend_reason,x.check,x.depth,'',x.exhibit_note,x.source_urls.find(u=>!u.includes('/2024/'))||x.source_urls[0],'',x.source_ids.join(' / ')]);
const main=make('訪問選定','JIMTOF2026｜訪問先の選定',`全${data.stats.master_rows.toLocaleString()}掲載行から${data.items.length}アイテム。A・B・R列が入力欄。G～J列の四タグ、L列の展示確度で絞り込みます。`,headers,mainRows,[15,12,13,29,13,43,16,18,17,17,14,23,31,70,65,80,33,65,70,72,14,70]);
const last=data.items.length+5;
main.getRange(`A6:B${last}`).format.fill='#FFF4D8';main.getRange(`R6:R${last}`).format.fill='#FFF4D8';
main.getRange(`A6:A${last}`).dataValidation={rule:{type:'list',values:['未選定','訪問予定','保留','見送り','訪問済み']}};
main.getRange(`B6:B${last}`).dataValidation={rule:{type:'list',values:['高','中','低']}};
main.getRange('A3').values=[['訪問予定']];main.getRange('B3').formulas=[[`=COUNTIFS(A6:A${last},"訪問予定")`]];
main.getRange('C3').values=[['候補件数']];main.getRange('D3').formulas=[[`=COUNTA(C6:C${last})`]];
main.getRange('E3').values=[['調査日']];main.getRange('F3').values=[[Date.parse(data.as_of+'T00:00:00Z')/86400000+25569]];main.getRange('F3').format.numberFormat='yyyy-mm-dd';
main.getRange('A3:F3').format.font={name:font,size:11,bold:true,color:'#174D77'};
main.getRange(`A6:A${last}`).conditionalFormats.add('containsText',{text:'訪問予定',format:{fill:'#D5EEE2',font:{color:'#075D44',bold:true}}});

make('技術詳細','候補ごとの技術詳細・確認事項','同じ候補IDで10観点を整理。IDで絞り込むと、入力→判断→出力、人の残作業、展示確度を一続きで確認できます。',['候補ID','企業','アイテム','観点','詳細メモ','確認深度','根拠資料ID'],techRows,[14,29,43,27,112,35,75]);
const tagRows=data.items.flatMap(x=>tags.map(t=>[x.id,x.company,x.item,t,x.tags[t].status,x.tags[t].reason,x.source_ids.join(' / ')]));
make('タグ根拠','四タグの付与・非付与理由','四タグは重複可。「—」も残し、名称だけでAI・自律性を推定しない理由を追跡します。',['候補ID','企業','アイテム','タグ','状態','該当・非該当の理由〈分類・分析〉','根拠資料ID'],tagRows,[14,29,43,19,23,112,75]);
const auditRows=data.audit.map(x=>[x.row_no,x.record_id,x.company,x.booth,x.status,x.reason,x.item_ids.join(' / '),x.tag_names.join(' / '),x.description_available?'あり':'なし',x.detail_url,x.company_urls.join('\n'),dateValue(x.original_checked_date)]);
const auditSheet=make('全出展者','全出展者からの抽出・判定記録','元の1,146掲載行を保持。情報不足・未抽出を非該当と混同しないでください。同一企業の複数小間も残しています。',['元の行番号','掲載ID','企業','小間','判定','判定理由・対応アイテム','候補ID','付与タグ','元説明本文','公式出展URL','元ページ記載の企業URL','元資料確認日'],auditRows,[13,36,32,13,31,118,65,40,15,78,65,18]);
auditSheet.getRange(`L6:L${auditRows.length+5}`).format.numberFormat='yyyy-mm-dd';
const majorRows=data.majors.map(x=>[x.company,x.booths.join(' / '),x.status,x.item_ids.join(' / '),x.note,x.urls.join('\n')]);
make('主要33社','主要企業の照合','大手の見落とし防止用。企業が出展していても、特定のAI機能の展示予定までは確認できない場合があります。',['企業','小間','確認状態','対応する候補ID','メモ','元の公式出展URL'],majorRows,[34,20,35,95,88,90]);
const methodRows=data.definitions.map(x=>[x.tag,x.definition,x.boundary]);
methodRows.push(['状態の読み方','機能記載＝メーカー資料に担当機能の説明あり。性能を独立に実証した意味ではない。','呼称・用途記載／関連基盤／構成要素／限定機能／人承認付き／—を区別。']);
data.limitations.forEach((s,i)=>methodRows.push(['調査範囲・限界 '+(i+1),s,'']));
for(const [t,c]of Object.entries(data.stats.tag_counts))methodRows.push([t+'集計',Object.entries(c).map(([a,b])=>`${a} ${b}件`).join(' / '),'重複可。呼称・基盤を含むため、実装数・普及率ではない。']);
methodRows.push(['資料探索の取得ログ',`${data.stats.retrieval_unique_urls} URLの取得を試行、${data.stats.retrieval_body_success_unique} URLで本文取得。`,'取得は精読や技術検証の完了を意味しない。今回の確認深度は候補ごとに記載。']);
make('分類・範囲','分類定義と調査範囲','四タグと技術の先端性は別軸。顧客ニーズ・推奨理由・確認事項は調査者の分析です。',['項目','定義・説明','境界・注意点'],methodRows,[30,110,90]);
const srcRows=[...sourceMap.values()].map(s=>[s.aliases.join(' / '),s.publisher||'既存台帳の出典',s.title,s.url,s.locator||'該当製品説明',dateValue(s.checked_date||'未記録'),s.short_quote||'',s.items.join(' / '),s.usage||'既存調査の出典']);
const sourceSheet=make('出典','原典・掲載位置・短い原文抜粋','URLで重複排除した出典一覧。全文転載はせず、掲載位置と必要な短い原文だけを残しています。確認日は出典単位で異なります。',['資料ID（別名含む）','発行者','資料名','原典URL','掲載位置','確認日','短い原文抜粋','対応する候補ID','資料の扱い'],srcRows,[56,27,63,95,80,18,65,85,45]);
sourceSheet.getRange(`F6:F${srcRows.length+5}`).format.numberFormat='yyyy-mm-dd';
main.getRange(`U6:U${last}`).values=data.items.map(x=>[techStarts.get(x.id)]);

// Recalculate, change one authorized input, verify the dependent count, then restore.
wb.recalculate();
const inspection=[];
inspection.push((await wb.inspect({kind:'table',range:'訪問選定!A3:F3',include:'values,formulas',tableMaxRows:1,tableMaxCols:6,maxChars:3000})).ndjson);
if(main.getRange('B3').values[0][0]!==0||main.getRange('D3').values[0][0]!==data.items.length)throw new Error('Initial summary count mismatch');
main.getRange('A6').values=[['訪問予定']];wb.recalculate();
inspection.push((await wb.inspect({kind:'table',range:'訪問選定!A3:B3',include:'values,formulas',tableMaxRows:1,tableMaxCols:2,maxChars:2000})).ndjson);
if(main.getRange('B3').values[0][0]!==1)throw new Error('Visit input did not update count');
main.getRange('A6').values=[['未選定']];wb.recalculate();
inspection.push((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A',options:{useRegex:true,maxResults:30},maxChars:5000})).ndjson);
await fs.writeFile(path.join(qa,'inspection.json'),JSON.stringify(inspection,null,2));
for(const sh of wb.worksheets.items){
 const range=({'訪問選定':'A1:L9','技術詳細':'A1:F12','タグ根拠':'A1:F10','全出展者':'A1:F9','主要33社':'A1:E9','分類・範囲':'A1:C9','出典':'A1:F8'})[sh.name];
 const img=await wb.render({sheetName:sh.name,range,scale:1.2,format:'png'});
 await fs.writeFile(path.join(qa,sh.name+'.png'),new Uint8Array(await img.arrayBuffer()));
}
// Final recalculation after verification and restoration; export only the restored state.
wb.recalculate();
const filename='JIMTOF2026_訪問先選定_四タグと技術詳細_20261022.xlsx';
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,filename));
await fs.writeFile(path.join(qa,'build_summary.json'),JSON.stringify({filename,items:data.items.length,masterRows:data.audit.length,sheets:wb.worksheets.items.map(x=>x.name),sources:srcRows.length,tagRows:tagRows.length,technicalRows:techRows.length},null,2));
console.log(JSON.stringify({output:path.join(out,filename),sheets:wb.worksheets.items.length,items:data.items.length}));
process.exit(0);
