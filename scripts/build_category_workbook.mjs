import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import { Workbook, SpreadsheetFile } from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const root=path.resolve('.');
const data=path.join(root,'data/research/technology_atlas_v1');
const read=async name=>JSON.parse(await fs.readFile(path.join(data,name+'.json'),'utf8'));
const [cards,rows,defs,evidence,priorities,audit,coverage]=await Promise.all(['fact_cards','category_index','category_definitions','evidence_ledger','category_visit_priorities','candidate_screening','coverage'].map(read));
const [methods,positions,years,issues,themes]=await Promise.all(['method_comparison','technology_method_positions','year_change_patterns','common_issues','research_candidates'].map(read));
const questions=await read('open_questions');
const ev=new Map(evidence.map(e=>[e.evidence_id,e]));
const wb=Workbook.create();
const trendSheet=wb.worksheets.add('技術動向・年度比較');
const reportSheet=wb.worksheets.add('報告用比較・提言');
const taskMap=wb.worksheets.add('仕事から見る技術全体マップ');
const directorySheet=wb.worksheets.add('技術別企業・年度比較');
const synthesis=wb.worksheets.add('横断比較・技術マップ');
const research=wb.worksheets.add('共通課題・研究候補');
const visits=wb.worksheets.add('カテゴリー別訪問優先');
const index=wb.worksheets.add('カテゴリー索引');
const details=wb.worksheets.add('展示詳細');
const definitions=wb.worksheets.add('カテゴリー定義');
const screening=wb.worksheets.add('候補仕分け');
const work=path.join(root,'.build/category_index');
await fs.mkdir(work,{recursive:true});
const col=n=>{let s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26)}return s};
function layout(sheet,title,context,headers,body,widths,rowHeight,tableName){
 const last=body.length+6,lastCol=col(headers.length);
 sheet.showGridLines=false;
 sheet.getRange(`A2:${lastCol}${last}`).format.font={name:'Meiryo',size:11,color:'#203746'};
 sheet.getRange('A2').values=[[title]];
 sheet.getRange('A2').format.font={name:'Meiryo',size:16,bold:true,color:'#173C55'};
 sheet.getRange('A2').format.wrapText=false;
 sheet.getRange('A2').format.rowHeight=30;
 sheet.getRange('A3').values=[[context]];
 sheet.getRange('A4').values=[['2026年は展示予定。基礎原典10/16・追補10/18（全件再取得ではない）。詳細・制約はカードと原典を参照。']];
 sheet.getRange(`A3:${lastCol}4`).format.font={name:'Meiryo',size:10,color:'#526B7A'};
 sheet.getRange(`A3:${lastCol}4`).format.wrapText=false;
 sheet.getRange(`A3:${lastCol}4`).format.rowHeight=22;
 sheet.getRange(`A6:${lastCol}${last}`).values=[headers,...body];
 sheet.getRange(`A6:${lastCol}${last}`).format.wrapText=true;
 sheet.getRange(`A7:${lastCol}${last}`).format.verticalAlignment='top';
 sheet.getRange(`A7:${lastCol}${last}`).format.rowHeight=rowHeight;
 const table=sheet.tables.add(`A6:${lastCol}${last}`,true,tableName);
 table.style='TableStyleLight9';
 table.showFilterButton=true;
 sheet.getRange(`A6:${lastCol}6`).format={fill:'#244B63',font:{name:'Meiryo',size:11,bold:true,color:'#FFFFFF'},rowHeight:34,horizontalAlignment:'center',verticalAlignment:'center',wrapText:true};
 widths.forEach((w,i)=>sheet.getRange(`${col(i+1)}2:${col(i+1)}${last}`).format.columnWidth=w);
 sheet.freezePanes.freezeRows(6);
 sheet.freezePanes.freezeColumns(sheet===index?3:sheet===details?3:1);
 return last;
}
function section(sheet,row,title,headers,body,rowHeight,name){
 const end=row+body.length,lastCol=col(headers.length);
 sheet.getRange(`A${row-2}`).values=[[title]];
 sheet.getRange(`A${row-2}`).format.font={name:'Meiryo',size:15,bold:true,color:'#173C55'};
 sheet.getRange(`A${row-2}`).format.rowHeight=30;
 sheet.getRange(`A${row}:${lastCol}${end}`).values=[headers,...body];
 sheet.getRange(`A${row}:${lastCol}${end}`).format={font:{name:'Meiryo',size:11,color:'#203746'},wrapText:true,verticalAlignment:'top'};
 sheet.getRange(`A${row+1}:${lastCol}${end}`).format.rowHeight=rowHeight;
 const t=sheet.tables.add(`A${row}:${lastCol}${end}`,true,name);t.style='TableStyleLight9';t.showFilterButton=true;
 sheet.getRange(`A${row}:${lastCol}${row}`).format={fill:'#244B63',font:{name:'Meiryo',size:11,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
}
const functions=['基盤・入力整備','判定・表示','提案・生成','ソフト実行','実機動作'];
layout(synthesis,'28社の横断比較：方式 × 任せる仕事','28社・33カード／10方式・35配置。別事例・別機能を分離。横軸は自律性・性能の順位ではありません。',
 ['技術方式',...functions],methods.map(m=>[m.method_id+' '+m.method,...functions.map(f=>positions.filter(p=>p.method_id===m.method_id&&p.function===f).map(p=>`${p.company} ${p.card_id}\n${p.task}\n【${p.status}】`).join('\n\n')||'今回の配置なし')]),[38,44,44,44,44,44],305,'TechnologyMethodMap');
synthesis.getRange('A4').values=[['整理・追補2026-10-18／基礎原典10/16・追補10/18。下に方式比較・年度比較。根拠IDとURLは「展示詳細」S/T列。']];
synthesis.getRange('A7:A16').format.font={name:'Meiryo',size:12,bold:true,color:'#173C55'};
methods.forEach((m,i)=>{
 const n=Math.max(...functions.map(f=>positions.filter(p=>p.method_id===m.method_id&&p.function===f).length));
 synthesis.getRange(`A${i+7}:F${i+7}`).format.rowHeight=Math.max(60,n*54);
 synthesis.getRange(`A${i+7}`).format.fill='#E8F0F5';
 functions.forEach((f,j)=>synthesis.getRange(`${col(j+2)}${i+7}`).format.fill=positions.some(p=>p.method_id===m.method_id&&p.function===f)?(j===4?'#EEF5ED':'#EDF7F7'):'#F5F7FA');
});
synthesis.getRange('G2:H43').format.columnWidth=36;
section(synthesis,22,'方式ごとの違い：AIの担当と人の仕事',
 ['方式','入力→判断・出力','人が担う部分','方式間の違い・制約','年度変化','カードID','根拠ID','主張の種類'],
 methods.map(m=>[m.method_id+' '+m.method,m.mechanism,m.human_boundary,m.comparison,m.year_change,m.card_ids.join(' / '),m.evidence_ids.join(' / '),m.statement_type]),130,'CrossMethodComparison');
section(synthesis,37,'2024以前からの変化：継続・対象拡張・比較不能',
 ['パターン','2024以前','2025–2026','解釈・未確定','カードID','根拠ID','確認日・整理日','主張の種類'],
 years.map(r=>[r.change_id+' '+r.pattern,r.baseline,r.current,r.interpretation,r.card_ids.join(' / '),r.evidence_ids.join(' / '),'基礎10/16・追補／整理10/18',r.statement_type]),110,'YearChangePatterns');
synthesis.tabColor='#117A83';
layout(research,'共通課題から研究開発候補へ','共通論点5件→研究候補5件。事実・分析・未検証仮説を区別。既存製品の不足や優位性を証明したものではありません。',
 ['共通論点','確認した事実','横断して考える点〈分析〉','限界・既存機能','カードID','根拠ID','研究候補'],
 issues.map((r,i)=>[r.issue_id+' '+r.issue,r.observed_facts,r.shared_issue,r.limits,r.card_ids.join(' / '),r.evidence_ids.join(' / '),themes[i].theme_id+' '+themes[i].theme]),[38,56,56,56,30,38,42],100,'CommonIssues');
research.getRange('A4').values=[['10/18追補：29行から候補の扱い、39行から現地確認12件。根拠ID→「展示詳細」S/T列。実験・採用決定は未実施。']];
research.getRange('H2:J22').format.columnWidth=38;
section(research,17,'研究開発候補：仮説・比較実験・見送り条件',
 ['候補／共通論点','顧客課題〈仮説〉','技術的な取り組み案','比較対象・限定実験','測る指標','採用条件・見送り条件','カードID','根拠ID','段階','主張の種類'],
 themes.map(r=>[r.theme_id+' '+r.theme+'\n'+r.issue_id,r.customer_problem,r.technical_approach,r.experiment,r.metrics,r.adoption_condition,r.card_ids.join(' / '),r.evidence_ids.join(' / '),r.stage,r.statement_type]),120,'ResearchCandidates');
section(research,29,'10/18追補：既存機能との重複と候補の扱い',
 ['候補／現時点の扱い','確認した既存機能','残る研究仮説','最初に確認すること','検証開始の条件','研究の開始・見送り判断','根拠カード','根拠ID','判定日','判定の範囲'],
 themes.map(r=>[r.theme_id+' '+r.decision,r.existing_capabilities,r.remaining_hypothesis,r.check_first,r.experiment_gate,r.adoption_condition,r.card_ids.join(' / '),r.evidence_ids.join(' / '),r.assessment_date,r.assessment_status]),160,'ResearchAssessment');
section(research,39,'未確認12論点：企業・ブース・質問・見たい証拠',
 ['論点／訪問先','現時点で確認した事実','現地・技術担当への質問','見たい証拠','研究に進む条件','現地まで保留する点','カードID','根拠ID','状態','追補日'],
 questions.map(r=>[r.question_id+' '+r.title+'\n'+r.companies.join(' / ')+'\n'+r.booths_2026.join(' / '),r.known_facts,r.question,r.requested_evidence,r.experiment_gate,r.unresolved,r.card_ids.join(' / '),r.evidence_ids.join(' / '),r.status,r.checked_date]),160,'OpenQuestions');
research.tabColor='#117A83';
const body=rows.map(r=>[r.category,r.subcategory,r.company,r.item,r.booths_2026.join(' / '),r.classification_basis,r.relation_scope,r.card_id,r.classification_reason,r.evidence_ids.join('\n'),r.source_urls.join('\n')]);
const roleFields=['ai_judgment','execution','human_preparation','human_approval','human_exception','limits'];
const roleHeaders=['AIの判断・提案','実行・出力','人の事前準備','人の承認','人の例外対応','制約・公開資料の不足'];
const visitBody=priorities.map(r=>[r.category,r.category_order,r.priority,r.company,r.booths_2026.join(' / '),r.exhibits,r.why_visit,r.baseline_2024,r.observation_2026,r.delta_type,r.comparison_interpretation,r.on_site_check,r.exhibition_status,r.product_stage,r.card_ids.join('\n'),r.card_ids[0],r.evidence_ids.join('\n'),r.evidence_ids.map(id=>`${id}: ${ev.get(id).url}`).join('\n'),...roleFields.map(k=>r[k])]);
const lastVisit=layout(visits,'カテゴリー別：どこから見に行くか',`${priorities.length}件・${coverage.visit_priorities.companies}社の訪問順案。カテゴリー内の順番。性能・普及率のランキングではありません。`,
 ['カテゴリー','順番','位置づけ','企業名','2026ブース','具体展示','優先する理由','2024の基準点','2026の記載','比較判定','差分の読み方','現地で確かめること','展示確度','提供段階','参照カード全件','詳細へ（先頭カード）','根拠ID','原典URL',...roleHeaders],visitBody,[26,8,20,30,15,46,58,58,58,30,58,65,48,48,18,20,35,75,58,58,55,58,58,65],145,'CategoryVisitPriorities');
visits.getRange('A4').values=[['AI・人の関与はS〜X列。基礎10/16、追補10/18。2社の追加仕様は保留、ユシロの旧社名2024原典を追加照合。']];
visits.freezePanes.freezeColumns(4);
visits.getRange(`D7:D${lastVisit}`).format.font={name:'Meiryo',size:11,bold:true,color:'#173C55'};
visits.getRange(`P7:P${lastVisit}`).format.font={name:'Meiryo',size:11,color:'#006F85',underline:'single'};
const lastIndex=layout(index,'JIMTOF2026 カテゴリー別出展索引',`${coverage.category_index.companies}名称キー・${cards.length}カード／追加候補を9カテゴリーで一次整理。重複・周辺部品を含み、精査深度は展示詳細を参照。`,
 ['カテゴリー','細分類','企業名','展示アイテム','2026ブース','分類根拠','関連範囲','詳細へ','分類理由','根拠ID','原典URL'],body,[25,30,30,45,15,25,43,15,65,35,65],84,'CategoryIndex');
index.tabColor='#244B63';
index.getRange(`H7:H${lastIndex}`).format.font={name:'Meiryo',size:11,color:'#006F85',underline:'single'};
const detailBody=cards.map(c=>[c.card_id,c.company,c.item,c.booths_2026.join(' / '),c.categories.map(t=>t.category).join('\n'),c.task,c.deployment,c.system_configuration,c.input,c.mechanism,c.output,c.human_boundary,c.baseline_2024,c.observation_2026,c.delta_type,c.exhibition_status,c.product_stage,c.unresolved,c.evidence_ids.join('\n'),c.evidence_ids.map(id=>`${id}: ${ev.get(id).url}`).join('\n'),c.review_depth,...['ai_scope',...roleFields].map(k=>c.deepening?.[k]??null)]);
layout(details,'展示アイテムの詳細','カードIDで索引と対応。システムの構成にはソフトウェアのみの構成も含みます。',
 ['カードID','企業名','展示アイテム','2026ブース','カテゴリー','担当タスク','実装先','システムの構成','入力','方式（原典要旨）','何を助けるか','人・権限の境界','2024の基準点','2026の記載','比較判定','展示確度','提供段階','未確認事項','根拠ID','原典URL','整理深度','AIの位置づけ',...roleHeaders],detailBody,[14,30,45,15,28,28,42,58,48,58,50,58,58,58,30,50,50,65,35,80,45,35,58,58,55,58,58,65],170,'ExhibitionDetails');
details.getRange('A4').values=[['訪問優先28社・33展示はV〜AB列で詳細化。空欄は今回の深掘り対象外。公式・分析・未記載を分離。2026年は展示予定。']];
details.getRange(`B7:B${cards.length+6}`).format.font={name:'Meiryo',size:11,bold:true,color:'#173C55'};
layout(definitions,'カテゴリーの定義','カテゴリーは重複可。メーカーの呼称と調査者の分類を索引で区別しています。',
 ['カテゴリー','分類する対象','分類上の境界','展示アイテム数'],defs.map(d=>[d.category,d.definition,d.boundary,null]),[30,75,75,22],52,'CategoryDefinitions');
defs.forEach((d,i)=>definitions.getRange(`D${i+7}`).formulas=[[`=COUNTIF('カテゴリー索引'!$A$7:$A$${lastIndex},A${i+7})`]]);
definitions.getRange(`D7:D${defs.length+6}`).setNumberFormat('0');
layout(screening,'関連候補345掲載の仕分け履歴','追加重点19掲載＝両年原典比較13掲載（同名12＋公式社名変更照合1）、2024未照合6掲載。一次分類265・対象外32・保留1。',
 ['企業名','2026ブース','判定','判定理由','カードID','2026原典URL','掲載ID','名称キー'],audit.map(r=>[r.company,r.booth,r.disposition,r.reason,r.card_ids.join('\n'),r.url,r.record_id,r.normalized_name]),[30,15,35,75,23,70,40,40],65,'CandidateScreening');
const report=JSON.parse(await fs.readFile(path.join(root,'data/research/report_v0/report.json'),'utf8'));
const catalog=report.catalog;
const catalogEvidence=new Map(catalog.evidence.map(e=>[e.evidence_id,e]));
const domainNames=new Map([...report.domains.map(x=>[x.id,x.short]),['D0','分類保留']]);
const directoryRows=catalog.topics.flatMap(t=>catalog.entries.filter(c=>c.topic_ids.includes(t.topic_id)).map(c=>[domainNames.get(t.domain_id),t.title,c.company,c.item,c.booths.join(' / '),c.target,c.technology,c.need,c.baseline_2024,c.observation_2026,c.year_change,c.year_status,c.depth,c.related_note,c.human_boundary,c.exhibition_status+'\n'+c.product_stage,c.card_id,c.exhibitor_urls_2026.join('\n'),c.exhibitor_urls_2024.join('\n'),c.evidence_ids.map(id=>`${id}: ${catalogEvidence.get(id).url}\n該当箇所: ${catalogEvidence.get(id).locator}`).join('\n')]));
layout(directorySheet,'技術別に企業・展示を探し、2024／2026年を対照する',`${catalog.scope.directory_rows}カード／${catalog.scope.company_name_keys}企業名キー。テーマ重複を含む${directoryRows.length}対応行。AI見積の直接事例と図面管理等の関連用途を区別。`,
 ['分野','対象の仕事・技術テーマ','企業名','製品・展示','2026ブース','対象の仕事〈用途整理〉','使う技術・公式説明の要約または抜粋','減らしたい負担〈分析〉','2024年の説明・基準点','2026年の説明・展示予定','差分の読み方〈分析〉','比較段階','整理の深さ','関連用途の境界','人の役割・未確認','展示確度・段階','カードID','2026公式出展ページURL','2024公式出展ページURL','根拠ID・URL・該当箇所'],
 directoryRows,[23,34,31,52,15,52,70,65,70,70,65,32,26,50,58,56,16,75,75,100],155,'TaskCompanyYearDirectory');
directorySheet.getRange('A4').values=[['10/19分類整理。57事例の詳細比較と一次分類を区別。両年原典があっても機能差未判定の場合あり。2024未掲載を新規発明としない。']];
directorySheet.freezePanes.freezeColumns(3);
directorySheet.getRange(`C7:C${directoryRows.length+6}`).format.font={name:'Meiryo',size:11,bold:true,color:'#173C55'};
directorySheet.getRange(`R7:S${directoryRows.length+6}`).format.font={name:'Meiryo',size:11,color:'#006F85',underline:'single'};
directoryRows.forEach((r,i)=>{for(const [j,year] of [[17,2026],[18,2024]])if(r[j])directorySheet.getRange(`${col(j+1)}${i+7}`).values=[[`JIMTOF${year} 出展ページ`]]});
layout(taskMap,'仕事とニーズから見る技術全体マップ','対象の仕事、減らしたい負担、使う技術、関連企業を同じ対応表から集計。1社・1展示が複数のテーマに関係する場合があります。',
 ['分野','対象の仕事・技術テーマ','減らしたい負担〈分析〉','使われる技術・解決の手段','関連企業名キー数','カード数','企業・該当カード','テーマID'],catalog.topics.map(t=>[domainNames.get(t.domain_id),t.title,t.problem,t.technology,t.company_count,t.row_count,catalog.entries.filter(c=>c.topic_ids.includes(t.topic_id)).map(c=>`${c.company} ${c.card_id}`).join(' / '),t.topic_id]),[23,36,67,75,16,12,110,14],145,'TaskTechnologyMap');
taskMap.getRange('A4').values=[['25技術テーマ＋分類保留。全344カードを表示対象に含む。個別企業の年度・出典は隣の「技術別企業・年度比較」で確認。市場シェアではありません。']];
taskMap.getRange('E7:F32').setNumberFormat('#,##0');
catalog.topics.forEach((t,i)=>taskMap.getRange(`A${i+7}:H${i+7}`).format.rowHeight=Math.min(400,Math.max(145,Math.ceil(catalog.entries.filter(c=>c.topic_ids.includes(t.topic_id)).map(c=>`${c.company} ${c.card_id}`).join(' / ').length/45)*16+25)));
taskMap.tabColor='#225B92';directorySheet.tabColor='#225B92';
const reportEv=new Map(report.evidence.map(e=>[e.evidence_id,e]));
const reportCases=report.topics.flatMap(t=>t.cases.map(c=>[t.title,c.company,c.item,c.booth,c.target,c.need,c.official_mechanism,c.ai_status,c.human_boundary,c.year_change,c.case_id,c.evidence_ids.join('\n'),c.evidence_ids.map(id=>`${id}: ${reportEv.get(id).url}\n該当箇所: ${reportEv.get(id).locator}`).join('\n')]));
layout(reportSheet,'報告v0：対象の仕事から企業・技術を比べる',`${reportCases.length}事例行。顧客ニーズは分析、技術は公式説明の要約。元の28社の比較より対象を広げています。原典はM列。`,
 ['技術・用途','企業名','製品・展示','2026ブース','対象の仕事','減らしたい負担〈分析〉','使う技術・担当する仕事〈公式説明〉','AIの位置づけ','人の関与・未確認','2024からの変化','事例ID','根拠ID','原典URL・該当箇所'],reportCases,[32,30,43,16,45,55,62,40,60,60,16,38,100],160,'ReportCaseComparison');
reportSheet.getRange('A4').values=[['説明本文取得988/820行。詳細URLなし619行は内容未取得。2026は展示予定。製品資料のみの事例は搭載未確認と表示。']];
reportSheet.getRange(`B7:B${reportCases.length+6}`).format.font={name:'Meiryo',size:11,bold:true,color:'#173C55'};
section(reportSheet,reportCases.length+14,'以前の研究候補：大テーマの下位課題として保存〈仮説〉',
 ['個別課題','関連する開発の大テーマ','残る仮説','確認した既存機能','取り組み案','着手・見送り条件','評価指標','現時点の扱い','根拠テーマ'],
 report.micro_research.map(r=>[r.name,report.research.filter(m=>m.child_ids.includes(r.id)).map(m=>m.name).join('\n'),r.hypothesis,r.existing,r.approach,r.decision,r.metrics,r.priority,r.basis.join(' / ')]),170,'ReportResearchSubtasks');
layout(trendSheet,'技術動向：現場の困りごとから、2024年との変化を読む','公式説明を横断した分析。製品名より先に対象の仕事・ニーズ・技術を示す。未掲載を新技術の誕生とは扱わない。',
 ['分野','現場の困りごと〈分析〉','使う技術と狙い〈分析〉','2024年以前にもあったこと','2025–2026年に具体化したこと','変化の読み方〈分析〉','比較の限界','根拠となる仕事・事例'],
 report.domains.map(r=>[r.name,r.need,r.technology+'\n'+r.value,r.past,r.now,r.change,r.limits,r.topics.map(id=>{const t=report.topics.find(t=>t.topic_id===id);return t.title+'\n'+t.cases.map(c=>c.case_id).join(' / ')}).join('\n\n')]),[30,58,60,62,65,62,62,100],145,'TopicYearComparison');
trendSheet.getRange('A4').values=[['6分野の比較と57事例の根拠は同じテーマで対応。市場の需要量・競合の空白・性能優位は未検証。']];
section(trendSheet,20,'技術動向から考える、4つの開発の大テーマ〈分析・未検証仮説〉',
 ['開発の大テーマ','解決するニーズ','確認した展示・開発の広がり','狙う立ち位置','何を・どの技術で開発するか','開発余地の仮説','既存技術・着手の考え方','評価指標','根拠となる仕事'],
 report.research.map(r=>[r.name,r.need,r.signal,r.position,r.approach,r.hypothesis,r.existing+'\n'+r.decision,r.metrics,r.basis.map(id=>report.topics.find(t=>t.topic_id===id).title).join('\n')]),175,'MacroResearchDirections');
trendSheet.getRange('I2:I24').format.columnWidth=65;
trendSheet.tabColor='#173C55';
reportSheet.tabColor='#173C55';
research.getRange('A4').values=[['以下は28社深掘り時点の個別課題。開発の大テーマは先頭「技術動向・年度比較」、企業事例は「報告用比較・提言」を参照。']];
wb.recalculate();
const countValues=definitions.getRange(`D7:D${defs.length+6}`).values.flat();
if(countValues.some((n,i)=>n!==defs[i].item_count))throw new Error(`Category count mismatch: ${JSON.stringify(countValues)}`);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:2000});
await fs.writeFile(path.join(work,'formula_scan.json'),JSON.stringify(errors,null,2));
const sample=await wb.inspect({kind:'table',range:'共通課題・研究候補!A29:E31',include:'values,formulas',tableMaxRows:3,tableMaxCols:5,maxChars:1700});
console.log(sample.ndjson);
for(const [sheetName,range,file] of [['技術別企業・年度比較','R6:S9','catalog_links']]){
 const blob=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(work,file+'.png'),new Uint8Array(await blob.arrayBuffer()));
}
// The renderer cannot calculate HYPERLINK. Render its friendly labels above;
// preserve Excel's native formula and supply only the missing cached label below.
rows.forEach((r,i)=>index.getRange(`H${i+7}`).formulas=[[`=HYPERLINK("#'展示詳細'!A"&MATCH("${r.card_id}",'展示詳細'!$A$1:$A$${cards.length+6},0),"${r.card_id}")`]]);
priorities.forEach((r,i)=>visits.getRange(`P${i+7}`).formulas=[[`=HYPERLINK("#'展示詳細'!A"&MATCH("${r.card_ids[0]}",'展示詳細'!$A$1:$A$${cards.length+6},0),"${r.card_ids[0]}")`]]);
directoryRows.forEach((r,i)=>{for(const [j,year] of [[17,2026],[18,2024]])if(r[j])directorySheet.getRange(`${col(j+1)}${i+7}`).formulas=[[`=HYPERLINK("${r[j].split('\n')[0]}","JIMTOF${year} 出展ページ")`]]});
wb.recalculate();
const output=path.join(root,'outputs/JIMTOF2026_カテゴリー別出展索引_v1.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(output);
execFileSync('C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',['scripts/finalize_category_workbook.py',output],{stdio:'inherit'});
await fs.rename(output+'.inspect.ndjson',path.join(work,'workbook.inspect.ndjson'));
await fs.writeFile(path.join(root,'checkpoints/category_workbook_v1.json'),JSON.stringify({status:'exported',output,categories:defs.length,associations:rows.length,companies:new Set(rows.map(r=>r.company)).size,cards:cards.length,calculated_category_counts:countValues,preview_directory:work,native_excel_open:'未確認'},null,2));
console.log(JSON.stringify({output,associations:rows.length,categories:defs.length,cards:cards.length}));
