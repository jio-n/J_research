import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from './_private/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const D=path.dirname(fileURLToPath(import.meta.url)),R=path.resolve(D,'../../..'),O=path.join(R,'outputs',path.basename(D));
const data=JSON.parse(await fs.readFile(path.join(D,'research.json'),'utf8'));
const wb=Workbook.create(),font='Yu Gothic UI',tags=['AI','フィジカルAI','自律化','自動化'];
const qa=path.join(D,'_private','qa');await fs.mkdir(qa,{recursive:true});
const col=n=>{let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
const starts={},layouts=[];
const widthOf=s=>[...String(s??'')].reduce((a,c)=>a+(c.charCodeAt(0)>255?1.85:1),0);
function make(name,title,note,headers,rows,widths,freeze=2){
 const sh=wb.worksheets.add(name);sh.showGridLines=false;
 const last=rows.length+6,end=col(headers.length);
 const body=sh.getRange(`A1:${end}${last}`);
 body.format={font:{name:font,size:11,color:'#263747'},verticalAlignment:'top',wrapText:true};
 sh.getRange('A2').values=[[title]];sh.getRange('A2').format={font:{name:font,size:16,bold:true,color:'#18334D'},wrapText:false,rowHeight:29};
 sh.getRange('A3').values=[[note]];sh.getRange('A3').format={font:{name:font,size:10,color:'#536574'},wrapText:false,rowHeight:21};
 sh.getRange(`A6:${end}${last}`).values=[headers,...rows];
 const table=sh.tables.add(`A6:${end}${last}`,true,'VisitTable'+wb.worksheets.items.length);table.showFilterButton=true;table.style='TableStyleLight9';
 sh.getRange(`A6:${end}6`).format={fill:'#234C70',font:{name:font,size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:37,verticalAlignment:'center',horizontalAlignment:'center',borders:{insideVertical:{style:'thin',color:'#FFFFFF'}}};
 widths.forEach((w,i)=>sh.getRange(`${col(i+1)}1:${col(i+1)}${last}`).format.columnWidth=w);
 rows.forEach((row,i)=>{
   const lines=Math.max(...row.map((v,j)=>String(v??'').split('\n').reduce((a,s)=>a+Math.max(1,Math.ceil(widthOf(s)/Math.max(5,widths[j]-2))),0)));
   sh.getRange(`A${i+7}:${end}${i+7}`).format.rowHeight=Math.max(name==='訪問計画'?58:29,Math.min(395,lines*15+9));
 });
 sh.freezePanes.freezeRows(6);sh.freezePanes.freezeColumns(freeze);
 layouts.push({sheet:name,rows:rows.length,columns:headers.length,last});
 return sh;
}

const techRows=[];
for(const x of data.items){
 starts[x.id]=techRows.length+7;
 const a=x.visit_analysis;
 const facets=[
  ['対象タスク・顧客課題',x.task+'。顧客課題：'+x.need],['入力・取得データ',x.input],['実現方式・AIの担当',x.method],['出力・実機への接続',x.output],
  ['人の準備・判断・操作',x.human],['技術的な注目点・参考要素〈分析〉',a.reference_value],['新規性と評価の限界',x.novelty_note],
  ['優先理由〈分析〉',a.priority_reason],['現地質問〈分析〉',a.questions.map((q,i)=>`${i+1}. ${q}`).join('\n')],
  ['関連展示の確認対象',a.related],['提供段階・展示根拠',x.stage+'\n'+x.exhibit+'。'+x.exhibit_note],['適用条件・未確認',x.limits],
  ...tags.map(t=>[t+'の該当理由',x.tags[t].status+'：'+x.tags[t].reason]),
  ['確認深度・今回の確認',x.depth+'\n'+a.analysis_basis+'\n今回原典：'+(x.fresh_review_ids.join('、')||'今回は再取得せず既存確認を継承')],
  ['ホール・小間の根拠',x.booths.join('／')+'。'+x.booth_priority_note]
 ];
 for(const [label,value] of facets)techRows.push([x.id,x.company,x.item,label,value,x.source_ids.join('、')]);
}
const tierLabels={A:'A 最優先',B:'B 重点比較',C:'C 補完',D:'D 周辺・標準自動化'};
const headers=['推奨順位','訪問優先度','訪問判断','企業名','ホール','ブース番号','見る展示・アイテム','AI','フィジカルAI','自律化','自動化','関心テーマ','展示技術の概要','優先する理由〈分析〉','技術的な注目点・参考要素〈分析〉','現地での質問〈分析〉','展示確度','関連技術の展示確認対象','関連展示の確認結果','訪問順','自分の優先度','自分が気になる理由','訪問後メモ','候補ID・技術詳細へ','代表の根拠URL','技術確認の深度'];
const rows=data.items.map(x=>{
 const a=x.visit_analysis;
 const primary=x.fresh_review_ids.length?x.sources.find(s=>s.source_id===x.fresh_review_ids[0]).url:x.source_urls.find(u=>!u.includes('jimtof.org')&&!u.includes('/2024/'))||x.source_urls.find(u=>!u.includes('/2024/'))||x.source_urls[0];
 const booth=['FT-M01','FT-M02'].includes(x.id)?'S4005':x.booths.join('／');
 const halls=['FT-M01','FT-M02'].includes(x.id)?'南4ホール':x.halls.join('／');
 return [x.suggested_rank,tierLabels[a.tier],'未選定',x.company,halls,booth,x.item,...tags.map(t=>x.tags[t].status),a.themes.join('／')||'所定動作・構成要素',x.overview,a.priority_reason,a.reference_value,a.questions.map((q,i)=>`${i+1}. ${q}`).join('\n'),x.exhibit,a.related,'未確認',null,null,null,null,x.id,primary,x.depth+'。'+a.analysis_basis];
});
const main=make('訪問計画','JIMTOF2026 訪問先選定', '全390候補。四タグは重複可。黄色＝入力欄。優先度は技術上の比較価値、展示確度はQ列。候補IDから詳細へ移動できます。',headers,rows,[9,18,14,29,15,16,44,17,19,17,17,41,68,62,65,78,28,70,24,10,16,60,72,20,80,60],4);
const last=rows.length+6;
main.tabColor='#234C70';
for(const c of ['C','S','T','U','V','W'])main.getRange(`${c}7:${c}${last}`).format.fill='#FFF1CC';
main.getRange(`C7:C${last}`).dataValidation={rule:{type:'list',values:['未選定','訪問予定','保留','見送り','訪問済み']}};
main.getRange(`S7:S${last}`).dataValidation={rule:{type:'list',values:['未確認','実機あり','動画・パネル','説明のみ','展示なし','要問い合わせ']}};
main.getRange(`U7:U${last}`).dataValidation={rule:{type:'list',values:['最優先','高','中','低']}};
main.getRange(`T7:T${last}`).dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:999}};
main.getRange(`A7:A${last}`).format.numberFormat='0';main.getRange(`T7:T${last}`).format.numberFormat='0';
main.getRange('A4').values=[['訪問予定']];main.getRange('B4').formulas=[[`=COUNTIFS(C7:C${last},"訪問予定")`]];
main.getRange('C4').values=[['全候補']];main.getRange('D4').formulas=[[`=COUNTA(X7:X${last})`]];
main.getRange('E4').values=[['最優先']];main.getRange('F4').formulas=[[`=COUNTIFS(B7:B${last},"A 最優先")`]];
main.getRange('G4').values=[['調査基準 2026-10-23']];main.getRange('A4:G4').format.font={name:font,size:11,bold:true,color:'#234C70'};
main.getRange('G4').format.wrapText=false;
main.getRange(`B7:B${last}`).conditionalFormats.add('containsText',{text:'A 最優先',format:{fill:'#DCEAF4',font:{bold:true,color:'#123D60'}}});
main.getRange(`C7:C${last}`).conditionalFormats.add('containsText',{text:'訪問予定',format:{fill:'#DDF0E4',font:{bold:true,color:'#1E6140'}}});
main.getRange(`Q7:Q${last}`).conditionalFormats.add('containsText',{text:'未確認',format:{fill:'#FFF4DA',font:{color:'#865B0E'}}});

make('技術詳細','各アイテムの技術・四タグの理由','候補IDで絞り込み。原典の説明と、調査者による優先理由・質問を分けています。実機性能・失敗復帰は現地未検証です。',['候補ID','企業名','アイテム','観点','詳細','根拠資料ID'],techRows,[17,29,44,38,112,75],2);

const sources=new Map();
for(const x of data.items)for(const s of x.sources){
 const key=s.url;
 if(!sources.has(key))sources.set(key,{...s,ids:[],items:[]});
 const src=sources.get(key);
 if(!src.ids.includes(s.source_id))src.ids.push(s.source_id);
 if(!src.items.includes(x.id))src.items.push(x.id);
 if(s.source_id.startsWith('VP-R'))Object.assign(src,{...s,ids:src.ids,items:src.items});
}
const asDate=s=>/^\d{4}-\d{2}-\d{2}$/.test(s||'')?Date.parse(s+'T00:00:00Z')/86400000+25569:s||'未記録';
const srcRows=[...sources.values()].map(s=>[s.ids.join('、'),s.publisher||'既存資料',s.title||'製品・出展情報',s.url,s.locator||'該当製品の説明',asDate(s.checked_date),s.usage||'既存調査を継承',s.items.join('、')]);
const sourceSheet=make('出典','出典・掲載位置・確認範囲','短い文脈要約と掲載位置を保持。確認日は原典ごとに異なります。全URLのライブ到達を確認した意味ではありません。',['資料ID','発行者','資料名','根拠URL','掲載位置','確認日','確認範囲・要約','対応候補ID'],srcRows,[65,28,65,95,85,17,112,85],1);
sourceSheet.getRange(`F7:F${srcRows.length+6}`).format.numberFormat='yyyy-mm-dd';

const helpRows=[
 ['訪問候補を選ぶ','訪問計画は全390アイテムを1行1アイテムで保持。初期表示はA→B→C→Dの推奨順位。訪問判断を「訪問予定」にして絞り込みます。','入力はこのシートの黄色セルに集約。技術詳細は閲覧用。'],
 ['訪問順を決める','推奨順位は技術上の重要度です。訪問順はT列へ自分で入力し、列のフィルタで昇順に並べます。','滞在日・入口・商談時刻が未指定のため、移動経路の最適順は作っていません。'],
 ['個人の関心を残す','U列＝自分の優先度、V列＝自分が気になる理由、W列＝訪問後メモ。関連展示を確認したらS列も更新します。','表全体の並べ替えを使うと候補IDと入力内容が一緒に移動します。'],
 ['四タグ','H〜K列はAI、フィジカルAI、自律化、自動化の独立列。重複可。複数列を絞るとAND条件になります。','「—」は今回の根拠では該当機能を認定していない状態で、技術が存在しないとの断定ではありません。'],
 ['タグの状態','機能記載＝担当機能の説明あり。呼称・用途記載＝方式未確認。関連基盤＝開発・接続用。構成要素＝周辺部材。人承認付き・限定機能を区別。','機能記載は独立した性能実証を意味しません。詳細シートに四タグそれぞれの理由があります。'],
 ['関心テーマとタグ','関心テーマはAIエージェント、熟練者知識の形式化、フィジカルAI、自律走行、自律制御、全体最適。L列のテキストフィルタ「含む」で探せます。','テーマは確認したい観点。例えばフィジカルAIとの比較候補でも、証拠不足ならフィジカルAIタグは「—」のままです。'],
 ...Object.entries(data.priority_definitions).map(([k,v])=>['優先度 '+k,v,'絶対的な性能順位ではなく、今回の関心に基づく調査者の選定。展示未確認はQ列で別に管理。']),
 ['技術的新規性','方式の新しさ、任せられる判断、工程の接続範囲、変化への対応を分けて見ます。成熟した制御も比較基準として優先候補に入れています。','「AI搭載」「エージェント」の名称だけで最新方式・一般化能力・全体最適を認定しません。'],
 ['展示確度','企業の出展と個別製品の展示を分離。参考・コンセプト・他展示会の事例・販売予定は個別に記載。','ファナックの溶接・VLA・キッティング等はJIMTOFの個別展示未確認。事前照会または会場で確認。'],
 ['読み方','M列は対象タスク・方式・出力、N列は優先理由、O列は技術的な参考要素、P列は具体的な質問。入力・人の担当・限界はX列リンクの詳細に保持。','出典シートはURLで重複排除。候補の根拠資料IDから掲載位置と確認日を追えます。'],
 ['調査範囲',`前版390候補を継承し、${data.analysis_scope.curated_items}件に固有の技術的着眼点・質問を記述。今回原典15資料を確認し20候補の解釈に利用。`,'残りは既存の対象タスク・方式・出力から比較観点を整理。全390候補の新規精読ではありません。'],
 ['取得できなかった資料','Beckhoff旧ニュースは404、東京エレクトロンデバイスは保守ページ、DMG出展告知は502。取得不能を非展示・非該当と判定していません。','該当する既存の確認情報と日付を継承。'],
 ['数の読み方',`四タグはAI67、フィジカルAI15、自律化40、自動化380。複数タグの候補は${data.stats.overlapping_tag_items}件。`,'呼称・基盤・構成要素を含むため実装件数や普及率ではありません。'],
 ['更新の基準','本版は2026-10-23時点の公開資料と既存調査に基づく視察前資料。','成功率、未知条件、品質保証、安全検証、実際の展示内容は現地で確認します。']
];
make('使い方','訪問選定の操作・定義','優先度、四タグ、関心テーマは別の軸です。推奨理由・参考要素・質問は分析として記載しています。',['項目','操作・定義','条件・限界'],helpRows,[32,110,100],1);

wb.recalculate();
if(main.getRange('B4').values[0][0]!==0||main.getRange('D4').values[0][0]!==390||main.getRange('F4').values[0][0]!==19)throw Error('Initial count mismatch');
main.getRange('C7').values=[['訪問予定']];wb.recalculate();
if(main.getRange('B4').values[0][0]!==1)throw Error('Input does not recalculate');
main.getRange('C7').values=[['未選定']];wb.recalculate();
const checks=[];
checks.push((await wb.inspect({kind:'table',range:'訪問計画!A4:G4',include:'values,formulas',tableMaxRows:1,tableMaxCols:7,maxChars:2200})).ndjson);
checks.push((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},maxChars:2500})).ndjson);
await fs.writeFile(path.join(qa,'artifact_inspection.json'),JSON.stringify(checks,null,2));
// Every sheet and three parts of the wide planning table are rendered.
for(const [name,range,file]of [['訪問計画','A2:G9','plan_identity'],['訪問計画','H6:P9','plan_technology'],['訪問計画','Q6:Z9','plan_inputs'],['技術詳細','A2:E14','detail'],['出典','A2:F9','sources'],['使い方','A2:C12','guide']]){
 const img=await wb.render({sheetName:name,range,scale:1.2,format:'png'});
 await fs.writeFile(path.join(qa,file+'.png'),new Uint8Array(await img.arrayBuffer()));
}
wb.recalculate();
await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(O,'JIMTOF2026_関心テーマ別_訪問計画.xlsx'));
await fs.rename(path.join(O,'JIMTOF2026_関心テーマ別_訪問計画.xlsx.inspect.ndjson'),path.join(qa,'export_inspection.ndjson')).catch(e=>{if(e.code!=='ENOENT')throw e;});
await fs.writeFile(path.join(D,'workbook_layout.json'),JSON.stringify({sheets:layouts,technicalStarts:starts,sourceCount:sources.size,columns:headers},null,2));
console.log(JSON.stringify({items:data.items.length,sheets:layouts,sourceCount:sources.size}));
process.exit(0);
