import fs from 'node:fs/promises';
import path from 'node:path';
import {constants} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile, FileBlob} from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const root=path.resolve('.');
const work=path.join(root,'.build/strategy_briefing_20261021');
const outdir=path.join(root,'outputs/strategy_briefing_20261021');
const datadir=path.join(root,'data/research/strategy_briefing_20261021');
await fs.mkdir(work,{recursive:true});await fs.mkdir(outdir,{recursive:true});await fs.mkdir(datadir,{recursive:true});
const skill='C:/Users/paulr/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.11052/skills/presentations';
const python='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const review=JSON.parse(await fs.readFile(path.join(root,'data/research/strategy_review_20261021/strategy_review.json'),'utf8'));
const directory=JSON.parse(await fs.readFile(path.join(root,'data/research/report_v0/technology_directory.json'),'utf8'));
const sources=new Map(review.sources.map(s=>[s.id,s]));
const cards=new Map(review.technology.map(c=>[c.card_id,c]));
const evidence=new Map(directory.evidence.map(e=>[e.evidence_id,e]));
const font='Noto Sans JP';
const fontPolicy={basis:'design',families:[font]};
const ink='#183C4D',teal='#167789',muted='#596C77',line='#CFDADF',warm='#A76B23';
const deck=Presentation.create({slideSize:{width:1920,height:1080}});
const tableSlides=[],chartSlides=[],slideIndex=[];

function wrap(text,width){return String(text).split('\n').map(s=>{let n=0,out='';for(const c of s){const w=/[\u0020-\u007e]/.test(c)?0.53:1;if(n+w>width&&!/[、。）」]/.test(c)){out+='\n';n=0;}out+=c;n+=w;}return out;}).join('\n');}
function text(s,name,value,x,y,w,h,size=32,bold=false,color=ink,uri){
 const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=uri?[[{run:value,link:{uri,isExternal:true}}]]:value;
 t.text.style={fontSize:size,bold,typeface:font,color,insets:0,autoFit:'none',wrap:'none',verticalAlignment:'top'};
 return t;
}
function base(title,context){
 const s=deck.slides.add();s.background.fill='#FFFFFF';
 text(s,'heading',title,86,54,1748,120,46,true);
 text(s,'context',wrap(context,76),88,180,1740,95,27,false,muted);
 slideIndex.push({number:deck.slides.items.length,section:deck.slides.items.length<=3?'主張':'補足',title,context,source_ids:[],card_ids:[]});
 return s;
}
function finish(s,ids=[],cids=[],caveat='',extraNotes=''){
 const n=deck.slides.items.length;slideIndex[n-1].source_ids=ids;slideIndex[n-1].card_ids=cids;slideIndex[n-1].caveat=caveat;
 let x=88;
 for(const id of ids){const src=sources.get(id);if(!src)throw new Error('Missing source '+id);text(s,'ref-'+id,id,x,960,80,30,20,false,teal,src.url);x+=86;}
 text(s,'disclosure',wrap(caveat,83),88,1004,1640,63,20,false,muted);
 text(s,'page',String(n).padStart(2,'0'),1780,1012,60,34,22,false,muted);
 const sourceNotes=ids.map(id=>{const s=sources.get(id);return `${id} ${s.publisher}\n${s.title}\n発表 ${s.published_date}\n${s.url}\n該当箇所 ${s.locator}\n確認範囲 ${s.reading_scope}\n確認日 ${s.checked_date}`;});
 const seen=new Set();
 for(const cid of cids){const c=cards.get(cid);if(!c)throw new Error('Missing card '+cid);sourceNotes.push(`${cid} ${c.company} ${c.item}\nブース ${c.booths.join(', ')}\n確認深度 ${c.depth}\n人の残作業 ${c.human_boundary}\n段階 ${c.exhibition_status} / ${c.product_stage}`);for(const eid of c.evidence_ids){if(seen.has(eid))continue;seen.add(eid);const e=evidence.get(eid);if(!e)throw new Error('Missing evidence '+eid);sourceNotes.push(`${eid} ${e.publisher}\n${e.title}\n${e.url}\n該当箇所 ${e.locator}\n確認日 ${e.checked_date}\n${e.evidence_type}`);}}
 s.speakerNotes.text=`JIMTOF2026 事前調査 2026年10月21日\n現地調査・顧客実証は未実施。公開発表、展示予定、分析仮説を区別。\n\n${sourceNotes.join('\n\n')}\n\n${extraNotes}\n\n留保 ${caveat}`;
}
function table(s,values,widths,heights,fontSize=29,top=280){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:86,top,width:1748,height:heights.reduce((a,b)=>a+b,0),columnWidths:widths,values});
 t.borders.assign({fill:line,width:1,style:'solid'});
 for(let r=0;r<values.length;r++){t.rows[r].height=heights[r];for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?ink:(r%2===0?'#F3F6F7':'#FFFFFF');cell.text.style={fontSize,bold:r===0||c===0,typeface:font,color:r===0?'#FFFFFF':ink,insets:12,autoFit:'none',wrap:'square',verticalAlignment:'top'};}}
 tableSlides.push(deck.slides.items.length);return t;
}
function statement(s,label,body,y,{labelWidth=390,size=34}={}){text(s,'label-'+y,label,88,y,labelWidth,70,size,true,teal);text(s,'body-'+y,wrap(body,Math.floor((1715-labelWidth)/size)),105+labelWidth,y,1715-labelWidth,155,size);}

// Main message 1. No separate cover: these three slides form the briefing.
{
 const s=base('JIMTOF2026 事前調査報告','2026年10月21日時点の公開情報に基づく見立て。展示会・顧客現場での実態は未確認。');
 text(s,'thesis','競争の範囲は、個々の機械から\n工程をつなぐ判断と実行へ広がる',88,300,1730,190,64,true);
 statement(s,'全体最適','設計・加工・計測・計画の情報をつなぎ、工程間の待ちや調整を減らす。',550);
 statement(s,'変化への対応','品種変更・段取り・例外に残る人の判断を、AIと自動化の対象にする。',710);
 finish(s,['S01','S04','S06','S11','S19'],[],'個々の加工・固定自動化の高度化も続く。工場全体の自律運用が既に普及したという結論ではない。');
}
// Main message 2. Conditional recommendation with a concrete customer outcome.
{
 const s=base('顧客向け開発の焦点は、使えるデータと現場への適応','加工現象・計測の知見と顧客接点がある場合、データ取得支援とモデルの適応・検証を組み合わせる。');
 table(s,[['顧客が困ること','提供するサービスの案','独自性を検証する点'],['データを集めても\n開発に使えない','現象から測定項目・同期・正解を設計\n条件・工具・品質が揃ったデータを提供','特定加工の理解に基づき\n開発の手戻りを減らせるか'],['一台で使えたモデルが\n別設備で安定しない','設備差を評価し、追加取得・適応を支援\n更新後の評価と復帰まで設計','少ない現場調整で\n使える範囲を広げられるか']],[470,755,523],[85,215,215],34,310);
 text(s,'proposal','データ量の競争に加え、工程の理解と顧客成果で差を作る',88,875,1720,60,37,true,teal);
 finish(s,['S01','S03','S31','S35','S38','S39','S40'],[],'開発候補は分析仮説。自社能力・顧客の支払意思・既存サービスとの差は未確認。');
}
// Main message 3. The commercial logic and immediate decision standard.
{
 const s=base('既存基盤との協業を使い、顧客成果から開発範囲を決める','継続サービスの成立には、精度向上に加えて、導入・データ作成・現場対応の費用まで確認する必要がある。');
 statement(s,'自ら担う部分','加工現象、判断理由、品質との対応、顧客での適用条件を蓄積する。',320,{size:35});
 statement(s,'他社と組む部分','センサー、CNC、CAM、学習・実行環境、外部データ基盤を活用する。',510,{size:35});
 statement(s,'開発を続ける条件','既存製品だけの運用と比べ、顧客の準備・不良・停止の負担が費用を含めて減る。',700,{size:35});
 finish(s,['S02','S05','S16','S26','S27','S36'],[],'AI精度向上から継続課金の収益性向上までの因果は未検証。外部データの利用・参加条件も個別確認が必要。');
}
// Appendix 1. Full census and uneven research depth.
{
 const s=base('補足1　調査の範囲と確認深度','全出展者を照合範囲に残し、戦略資料と技術台帳を組み合わせる。深掘りした企業だけを母集団にはしない。');
 table(s,[['調査の層','対象','読み取れることと限界'],['全出展者CSV','2024年 1,281掲載行\n2026年 1,146掲載行','説明の有無と台帳との照合状況を管理\n全行の詳細技術を確認済みとはしない'],['同名パネル','両年度に本文がある538名称キー','公開説明の語群を同じ範囲で比較\n導入率・性能向上・新機能数は示さない'],['技術の位置づけ','344カード、主要企業33社の確認表','詳細比較57、個別タスク33、一次分類254\n役割未確定92、工程未確定39'],['戦略・潮流の根拠','既存34資料と追加6資料','公式発表、取材、公的研究、論評を区別\n同じ発表の引用を独立した実証と数えない']],[400,560,788],[75,145,145,145,145],30,280);
 finish(s,[],[],'出典：年度別公式CSV、既存技術台帳、戦略レビュー。集計規則・入力ハッシュと全行監査CSVをGitHubに収録。',
 '入力 data/exhibitors_2024_with_details.csv / data/exhibitors_2026_with_details.csv\n集計 data/research/macro_20261019/census.json\n技術 data/research/report_v0/matrix_classification.json\n最新レビュー data/research/strategy_review_20261021/strategy_review.json\nhttps://github.com/jio-n/J_research');
}
// Appendix 2. Native chart; exact counts, no adoption inference.
{
 const s=base('補足2　公開説明ではAIの明示が増える','両年度に本文がある同名538件。工場運用・データ連携など、全ての語群が増えたわけではない。');
 const selected=review.text_signals.filter(r=>['AI明示','生成AIとエージェント','フィジカルAI明示','自動化と省人化','設計製造のデジタル化','工場運用とデータ連携','状態監視と補正','自律の明示'].includes(r.theme));
 const chart=s.charts.add('bar',{position:{left:95,top:295,width:1725,height:620},categories:selected.map(r=>r.theme),series:[{name:'2024年',values:selected.map(r=>r.wording_2024),fill:'#91AAB5'},{name:'2026年',values:selected.map(r=>r.wording_2026),fill:teal}],barOptions:{direction:'bar',grouping:'clustered',gapWidth:70},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:25}},dataLabels:{showValue:true,position:'outEnd',textStyle:{fontSize:24}},xAxis:{textStyle:{fontSize:25}},yAxis:{textStyle:{fontSize:23},min:0,max:220},chartFill:'#FFFFFF',chartLine:{fill:'none',width:0},plotAreaLine:{fill:'none',width:0}});
 const {applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
 applyPresentationChartFont(chart,{fontFamily:font});chartSlides.push(deck.slides.items.length);
 finish(s,[],[],'単位：名称キーの明示件数。重複分類あり。語の追加・削除には説明量・展示対象の差も含む。採用率ではない。',
 '元データ data/research/strategy_review_20261021/macro_wording_signals.csv\n規則 data/research/macro_20261019/census.json\n'+selected.map(r=>`${r.theme}: 2024=${r.wording_2024}, 2026=${r.wording_2026}`).join('\n'));
}
// Appendix 3. Manufacturer strategies, not assumed exhibition implementations.
{
 const s=base('補足3　主要3社は、データと現場適応へ異なる入口を持つ','戦略発表・取材内容の比較。各社の計画を、JIMTOFの展示機能・販売機能・顧客導入実績と混同しない。');
 table(s,[['企業','開発の入口と狙い','データと適応','現時点での留保'],['DMG森精機','設備・工程・品質を使う\n製造フィジカルAI基盤','複数企業・設備の実運用データ\n現象を捉える取得と構造化','約100社・1,000台・100TBは整備計画\n外部利用の条件は要確認 [S02,S03]'],['ヤマザキマザック','工程設計・計画のエージェント\nロボット学習環境','加工意図と人の修正を使う\n基盤モデルと顧客固有モデル','取材時点でPoC、提供形態は未確定\n自社開発範囲・利用権を確認 [S04,S05]'],['ファナック・日立','変化するピッキング・段取り等\n現場固有ルールへの対応','日立の工場をカスタマーゼロに\n実機で認識・タクト・品質を検証','共同実証から2027年度の展開を計画\n実証先は日立の工場 [S06,S07]']],[285,460,485,518],[80,190,190,190],29,285);
 finish(s,['S02','S03','S04','S05','S06','S07'],[],'基盤モデルという表現だけで、モデル構造の独占保有やゼロからの学習を断定しない。');
}
// Appendix 4. Corroboration beyond the three machine tool manufacturers.
{
 const s=base('補足4　工程間連携は、研究機関・制御・ITにも共通する論点','工作機械メーカーだけでなく、データの意味、計画と実績、仮想と実機を接続する動きから方向を読む。');
 table(s,[['主体','公開情報の焦点','全体像における役割','確認が残る点'],['産総研','現象に基づく取得、構造化\n製造データの循環 [S01,S39]','現象理解・データ・AI開発と\n実機テストベッドの接続','参加・提供条件\n個別の利用可能データ'],['Siemens','デジタルツインと産業AI\n設計と運用の接続 [S11,S12]','仮想検証と実績をつなぎ\n生産の調整に使う構想','既設設備との接続\n顧客での効果と操作範囲'],['NEC・オムロン','業務をまたぐエージェント\nITとOTの意味の統合 [S10,S33]','計画・現場・業務の情報を\n判断に使える状態へ整理','試作と販売機能の区別\n権限と顧客別の設定負担'],['オークマ・牧野','工程集約、供給自動化\nライン設計・保守との組合せ','機械と自動化を組み合わせ\n安定して生産する仕組み','他社機の対応範囲\n全体を調整する責任']],[300,505,500,443],[75,145,145,145,145],29,280);
 finish(s,['S01','S10','S11','S12','S22','S33','S39'],['FC008','FC046'],'戦略・研究構想と個別製品の実装は異なる。固定自動化や工程集約も全体像を支える既存の手段。');
}
// Appendix 5. Physical AI cases and conventional comparators.
{
 const s=base('補足5　フィジカルAIは、変化する作業の適用条件で比べる','認識から動作、完了確認、失敗後の復帰まで、どこを技術が担うかを確認する。');
 table(s,[['残る作業','公開されている例','現地で確かめたい条件'],['主軸の切粉処理','TAKISAWA TR-20W\n絡まりの認識・判断と除去 [FC049]','参考出品。油・切粉状態の変化、\n完了判定・再試行・人への引継ぎ'],['不定形ワークの面取り','東京エレクトロンデバイス\n3D形状から作業軌道を生成 [AC146]','加工条件・干渉・品質の確認範囲\n形状変更時の再設定とタクト'],['移設・配置変更後の復帰','中村留 RoboSync\nマーカーから相対位置を補正 [FC048]','位置復旧と作業の自律判断を区別\n許容誤差と人に残る調整'],['段取りと付帯作業の機構','イマオの締結・爪交換、工具機構等\n機械的な保持・交換 [FC042,FC043]','固定機構で十分な範囲との比較\n必要な認識・学習を絞る']],[410,650,688],[75,145,145,145,145],30,280);
 finish(s,['S06','S07','S23'],['FC049','AC146','FC048','FC042','FC043'],'自律・教示不要という名称だけで汎用性を判断しない。各社の公開説明・展示予定であり、現地未確認。');
}
// Appendix 6. Key qualification to a simplistic big-data strategy.
{
 const s=base('補足6　必要なデータ量は、開発するモデルと用途で変わる','広い汎用性を狙う基盤モデル、限定工程のモデル化、顧客設備への適応、導入評価を分けて考える。');
 table(s,[['開発の目的','データの使い方','公開例と解釈'],['多様な現場を扱う基盤','複数企業・設備から実運用を収集\n条件・品質・設備を構造化','DMG森精機の大規模整備計画 [S02]\n計画規模を収集済みとは扱わない'],['加工誤差をリアルタイム補正','高頻度信号から必要情報を抽出\nコンパクトな物理モデルへ反映','三菱電機のエッジツイン研究 [S31]\n取得・モデル・制御を一体で設計'],['限定工程の条件を決める','限定条件の少数実験から\n入出力モデルと条件探索を構成','産総研のスピニング加工研究 [S38]\n切削や全工場への一般化はしない'],['実機差を補正し劣化を推定','既知の物理モデルに\n追加データで補正を加える','三菱電機の物理モデル組込みAI [S40]\n用途・適用条件の限定が前提']],[425,670,653],[75,145,145,145,145],29,280);
 finish(s,['S02','S03','S31','S38','S39','S40'],[],'共通するのは、目的に合う信号・条件・正解が必要という点。全ての開発に巨大な独自データ基盤を前提としない。');
}
// Appendix 7. Tacit knowledge and adaptation already have competitors.
{
 const s=base('補足7　暗黙知の活用は、理由と結果の記録までが論点','修正された最終データだけでは、変更理由・一時的な制約・誤操作を区別できない場合がある。');
 table(s,[['知識・モデルの扱い','既存機能・構想','差別化を検証する接点'],['過去工程の再利用','ProPlanAIは過去ジョブと形状から工程を予測\nカスタムCAMという選択肢もある [S14,S15]','どの条件で使える知識か\n既存CAMで残る修正は何か'],['顧客ごとの適応','マザックは加工意図と人の修正を使う\n顧客固有モデルを構想 [S05]','修正理由と品質結果の紐付け\n学習に採用する条件と権利'],['モデル作成と評価','Beckhoffはデータ・ラベル・学習・評価・出力の\nワークフローを提供 [S35]','汎用ツールに加え、工程ごとの\n評価項目と現場差を扱えるか'],['運用中の改善','更新のための学習と、毎回の実行判断を区別\n版・評価・復帰の管理が必要 [S21]','別設備への適応工数\n更新後の回帰と適用範囲']],[400,795,553],[75,145,145,145,145],29,280);
 finish(s,['S05','S14','S15','S21','S35'],['FC018','FC020','FC014'],'過去ジョブ学習やモデル評価を市場の空白とみなさない。独自価値は特定工程の成果で確認する。');
}
// Appendix 8. Full existing role matrix, native table.
{
 const s=base('補足8　工程と役割で見る既存344技術の位置づけ','件数は既存台帳のカード数。工程・役割は重複配置があり、分類深度も異なる。');
 const values=[['工程','集めて見せる','状態を見極める','案・手順を作る','作業・調整を行う']];
 for(const [job,label] of Object.entries(review.jobs)){values.push([label,...Object.keys(review.roles).map(role=>String(review.matrix_cells.find(c=>c.job===job&&c.role===role).count))]);}
 table(s,values,[540,302,302,302,302],[80,...Array(7).fill(82)],30,280);
 finish(s,[],[],'市場規模・普及率ではない。未配置は不在を意味しない。学習・接続等の横断基盤は交差表に出ない場合がある。',
 '元データ data/research/strategy_review_20261021/technology_role_map.csv\n分類 data/research/report_v0/matrix_classification.json\n役割未確定92、工程未確定39。実行には人の操作を含むカードがあり、無人化を意味しない。');
}
// Appendix 9. Interfaces, not an unsupported connected product architecture.
{
 const s=base('補足9　開発余地は、モジュール間に残る仕事から検証する','同じマップに並べた製品が接続済みという意味ではない。次の接点で顧客の負担と既存対応範囲を確認する。');
 const rows=[
 ['工程案と加工検証','設備・工具・保持の制約、採用した工程案','修正理由と検証結果が次の提案へ返るか','D2'],
 ['信号と現象モデル','時刻・加工区間・条件・工具・品質の対応','同期・欠損・校正・正解を誰が保証するか','D1'],
 ['計測と加工判断','寸法・摩耗・負荷と品質・時間・費用の制約','診断の矛盾や不確実性をどう扱うか','D4'],
 ['停止と再計画・復帰','設備・仕掛・工具・人員と再開条件','承認・実行権限と結果確認までつながるか','D5'],
 ['人の修正と学習','元の案、変更理由、採否、最終結果','入力負担と誤修正・秘匿ノウハウの扱い','D2'],
 ['別設備へのモデル展開','適用条件・モデル版・評価データ','必要な追加取得と再調整の費用','D3'],
 ['認識と完了・復帰','作業状態・軌道・工具・完了と介入','未経験状態での失敗と復帰時間','D6']];
 table(s,[['接点','受け渡す情報','未確認事項','候補'],...rows],[365,650,615,118],[70,...Array(7).fill(86)],26,280);
 finish(s,[],['FC018','FC020','FC033','FC040','FC025','FC013','FC027','FC049','AC146'],'接点の整理は分析。開発余地・市場の空白・既存製品の機能不足を実証したものではない。');
}
// Appendix 10. All six candidate concepts.
{
 const s=base('補足10　顧客向け開発候補の比較','自社能力と顧客の困りごとを照合するための候補。モデル保有やAIの採用自体を目的にしない。');
 table(s,[['候補','顧客へ返す成果','既存手段との比較','必要な接点'],
 ['D1 データ取得・品質保証','現象と品質が対応するデータ\n開発の手戻りを減らす','計測・収集ツールだけで\n解けない作業があるか','加工現象・計測\n実機と品質データ'],
 ['D2 工程知識の再利用','修正理由と適用条件を残し\n準備・初品手戻りを減らす','過去ジョブ学習やCAM設定\nとの追加効果','工程知識・CAM\n履歴と利用権'],
 ['D3 顧客適応・導入検証','設備差への適応を支援し\n更新後も使える範囲を示す','既存の学習・評価だけで\n足りるか','工程理解・評価\n複数設備の検証'],
 ['D4 工程の統合判断','品質・工具・時間を踏まえ\n続行・変更・交換を支援','既存補正と監視の組合せ\nとの総合成果','計測・工具・制御\n品質責任の合意'],
 ['D5 例外業務の運用支援','停止・不足から代替案と\n復帰確認までの負担を減らす','既存MES・計画系の設定\nとの違い','業務設計・API\n顧客工場の権限'],
 ['D6 変動する付帯作業','切粉等の作業を完了確認と\n復帰まで含めて自律化','固定機構・既存認識方式\nとの教示・介入の差','作業・工具の知見\nロボットSI・実験']],[380,520,480,368],[70,...Array(6).fill(102)],27,280);
 finish(s,[],['FC015','AC175','FC018','FC014','FC033','FC027','FC049'],'D1とD3は加工現象・計測に強みがある場合の優先案。自社能力・需要・支払意思は未確認。');
}
// Appendix 11. Build/partner/join choices by purpose.
{
 const s=base('補足11　データ取得・活用の組合せ','自社取得、共同取得、外部基盤、既存モデルの利用を、開発目的に応じて選ぶ。');
 table(s,[['経路','向く用途','自社で持つ役割','事前に確認すること'],
 ['自社で取得','現象モデル、品質との対応\n限定工程の適応・評価','測定条件と正解を揃える\n工程知識と評価方法','実機・計測・データ利用権\n自社条件だけへの偏り'],
 ['顧客・装置メーカーと\n共同取得','実運用、希少な異常\n設備差、人の修正','顧客課題と現場条件の整理\n取得・評価と便益の還元','取得負担・試験と停止\n所有・学習利用の合意'],
 ['外部基盤・研究連携','一般的な学習・比較\n共同研究と技術検証','目的と必要項目を示す\n顧客固有データを補完','提供時期・項目・商用利用\n参加とデータ権利は別'],
 ['既存・物理モデルを利用','限定工程の予測・補正\n少量データでの適応','適用範囲と設備差の評価\n更新・復帰の手順','入出力・ライセンス\n顧客環境での独立評価']],[400,455,455,438],[75,145,145,145,145],29,280);
 finish(s,['S01','S02','S31','S35','S37','S38','S40'],[],'MOCOの入会窓口は確認。入会で製造AX・GENIACデータの利用権を得られるとは確認していない。');
}
// Appendix 12. Financial causality is an explicit hypothesis.
{
 const s=base('補足12　継続サービスの価値と採算を分けて確認する','運用データを改善に返す仕組みはある。利益率の向上まで成立するかは、顧客成果と提供費用の両面で評価する。');
 table(s,[['事業のつながり','根拠・位置づけ','追加確認が必要な条件'],
 ['運用・保守データを蓄積','MROの経験を診断や開発へ返す説明\nDMG森精機の取材・統合報告 [S24,S25,S29]','学習に使える内容と権利\n異常・介入の記録品質'],
 ['診断・支援・更新を継続提供','Condition Agent、デジタルサービス\n学習ツールの継続課金例 [S26,S28,S36]','利用が続く理由と契約範囲\n顧客別の対応負担'],
 ['顧客の成果を改善','準備・不良・停止・工具等の負担削減\n候補サービスで検証する分析仮説','現行運用と同じ条件で比較\n入力・調整・監視の残作業'],
 ['提供側の採算が成立','利益率向上は今回の資料で未実証\nMRO等の開示とAI単体を区別 [S27]','取得・注釈・推論・現場対応費\n導入部分の再利用性と継続率']],[400,800,548],[75,145,145,145,145],29,280);
 finish(s,['S20','S24','S25','S26','S27','S28','S29','S36'],[],'売上・利益の予測値は置いていない。自社導入は、顧客向けサービスのデータ取得・運用費検証にも使える。');
}
// Appendix 13. Fieldwork questions have specific effects on development decisions.
{
 const s=base('補足13　訪問先と、開発判断につながる確認事項','ブースは既存2026公式CSVから照合。直前の配置と当日の展示内容は公式案内で再確認する。');
 const rows=[
 ['DMG森精機 E8005','データの参加・提供条件、計画と実績\n品質との対応、商用・学習利用の権利','D1・D3の取得戦略'],
 ['マザック E1001\nHexagon E2013 / E7035','加工意図と修正理由、顧客適応\n既存CAMに残る準備・変更作業','D2の補完価値と協業の接点'],
 ['ファナック S2001\nTAKISAWA E3013 / TED E7073','設備・対象変更時の適応、完了判定\n失敗・人の介入・復帰とタクト','D3・D6の実用範囲'],
 ['Beckhoff E2028\n三菱電機 S2003 / キスラー S4031','必要な信号・同期・ラベル・モデル評価\n既存ツールが扱う範囲と追加負担','D1・D3の重複と差別化'],
 ['レニショー E7089\nブルーム E7077 / モリマシナリー S3048','補正・工具寿命・計測の連携\n異常値、競合する判断、品質責任','D4の追加価値と必要な権限'],
 ['たけびし S3015 / CEC E2006\nものレボ S3018 / FNS E2034','状態と制約の意味、計画変更と実行\n停止後の結果確認、個別設定工数','D5の再利用部分と個別SI']];
 // Additional booth numbers are resolved from cards instead of guessed labels.
 const replaceBooths=[['FC034','ブルーム'],['FC027','ものレボ']];
 for(const [cid,label] of replaceBooths){const c=cards.get(cid);for(const row of rows)row[0]=row[0].replace(new RegExp(label+' [A-Z][0-9]+'),label+' '+c.booths.join(' / '));}
 table(s,[['訪問先','具体的な問い','回答の使い道'],...rows],[655,740,353],[75,...Array(6).fill(96)],26,280);
 finish(s,['S02','S05','S06','S35'],['FC018','FC020','FC034','FC040','FC027','FC024','FC025','AC039','AC175','AC146'],'質問中の戦略が全て当該ブースで展示されるとは限らない。公式説明、担当者説明、実演観察を区別して記録する。');
}

// Appendix 14–16. All 33 majors, including sparse evidence.
const majorFocus={
 'DMG森精機':'工程集約、AMR、ワーク・パレット供給、運用支援',
 'ヤマザキマザック':'複合加工と自動化、AI活用。工程案・顧客適応を確認',
 'オークマ':'機内ロボット、供給、熱変位制御と加工支援',
 '牧野フライス製作所':'パレット供給、MAS、ライン設計・保守の組合せ',
 'ファナック':'CNC・ロボット・ツイン。生成AIと物理作業の範囲',
 '三菱電機':'CNCの監視・省人化、保守、計画と加工データ',
 'シーメンス':'CAD/CAM、工程内品質、工作機械ツイン',
 'ジェイテクト':'研削・加工ソリューションと省人化の構成',
 'ニデックマシンツール':'歯車加工・工程集約、デジタルツインの説明',
 'ニデックオーケーケー':'加工機とローダ等による自動化の構成',
 'ソディック':'放電・加工と自動化。具体的な連携範囲を確認',
 'アマダ':'レーザ・研削・プレスと周辺工程の自動化',
 'ブラザー工業':'工具搭載数・5軸と複合加工による段取り負担低減',
 '松浦機械製作所':'多パレット・MiOS、加工データと供給の連携',
 'シチズンマシナリー':'自動旋盤と付帯作業・供給の省人化',
 'スター精密':'自動旋盤と周辺工程。条件変更時の作業を確認',
 'ツガミ':'精密自動旋盤と供給・自動化への対応',
 'オーエスジー':'切削工具と加工課題へのソリューション',
 '三菱マテリアル':'工具・材種・加工ソリューション、超硬リサイクル',
 '京セラ':'工具と加工ソリューション。安定加工・段取りを確認',
 'タンガロイ':'工具の多機能化と加工の効率・安定化',
 'ミツトヨ':'自動測定、測定プログラムと工程データ',
 '東京精密':'2026本文未取得。自動測定・品質データ接続を確認',
 'レニショー':'計測結果と工具オフセットのフィードバック',
 'ハイデンハイン':'工具計測・摩耗診断とCNCへの接点',
 'ベッコフオートメーション':'制御設計・運用のAI支援、信号取得とモデル作成',
 'Hexagon Manufacturing Intelligence':'工程予測、CAM、計測と品質ソフトウェア',
 '住友電気工業':'工具寿命・安定加工、工程集約と段取り低減',
 '中村留精密工業':'供給自動化と配置変更後の位置復旧',
 'FUJI':'加工と周辺工程の自動化。人の残作業を確認',
 'TAKISAWA':'切粉処理の参考出品、認識・除去・復帰',
 'オートデスク':'CAD/CAMとPLM・AI支援の連携範囲',
 'ニコン':'画像・CT等の計測とロボットビジョン'
};
for(let page=0;page<3;page++){
 const group=review.major_companies.slice(page*11,page*11+11);
 const s=base(`補足${14+page}　主要企業の確認表 ${page+1}/3`,'33社を確認対象に保持。表の役割は公開説明の要旨と分析であり、AI使用・接続実績を一律に認定しない。');
 const rows=group.map(m=>[wrap(m.name,20),m.booths.join(' / '),wrap(majorFocus[m.name],37),m.card_ids.length?'カードあり':'詳細追加確認']);
 table(s,[['企業','ブース','見る技術と役割','台帳の状況'],...rows],[520,250,760,218],[65,...Array(11).fill(57)],24,280);
 const notes=group.map(m=>`${m.company}\n${majorFocus[m.name]}\n2026公式CSV行 ${m.official_record_ids.join(', ')}\n${m.official_urls.join('\n')}\n${m.context_note||''}`).join('\n\n');
 finish(s,[],group.flatMap(m=>m.card_ids.slice(0,2)),'ブースは既存公式CSV。カードの深度は混在。本文不足・カード未整理を、出展や技術の不在とは扱わない。',notes);
}
// Appendix 17. Evidence quality and the remaining decisions.
{
 const s=base('補足17　現地確認後に更新する判断','事前の見立てを、展示の実態と顧客の困りごとで検証し、開発・協業・既存製品活用の範囲を絞る。');
 table(s,[['判断の軸','今回わかっていること','現地・顧客で追加する根拠'],
 ['方向性','データ・顧客適応・工程連携へ向かう\n複数の計画と既存技術がある','展示と販売の違い、実用条件\n実顧客への導入と継続運用'],
 ['独自性','D1〜D6の補完価値を仮説化\n既存の代替手段も併記','既存機能で残る負担の具体例\n追加開発で改善できる成果'],
 ['自社適合性','必要な工程理解・計測・連携等を整理\n具体的な自社能力は未確認','得意工程、顧客接点、実機\nデータ・API・評価へのアクセス'],
 ['事業性','継続提供の例はある\n採算向上の因果は未実証','支払意思、導入・運用の費用\n再利用部分と顧客別の対応量']],[370,710,668],[75,145,145,145,145],30,280);
 finish(s,['S01','S06','S14','S21','S27'],[],'根拠は各スライドのノートとリンクに記載。公開情報・現地説明・実演・顧客実績を分けて追記する。',
 '参照元の全体台帳 https://github.com/jio-n/J_research/tree/main/data/research/strategy_review_20261021\nレビューHTML outputs/JIMTOF2026_潮流と開発候補レビュー_20261021.html\n40資料には検索抽出のみの資料を含む。確認範囲は戦略レビューの各sourceレコードを参照。');
}

if(deck.slides.items.length!==20)throw new Error('Unexpected slide count');
const draft=path.join(work,'candidate.pptx');
await(await PresentationFile.exportPptx(deck)).save(draft);
const finalPath=path.join(outdir,'JIMTOF2026_事前調査報告_主張3枚と補足17枚_r2.pptx');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
try{
 await finalizePresentation({workspaceDir:root,candidatePath:draft,finalPath,pythonExecutable:python,
  integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit',...tableSlides.flatMap(n=>['--require-native-table-slide',String(n)])],
  explicitTotalSlideCount:20,requiredNativeTableOwnerSlides:tableSlides,requiredNativeChartOwnerSlides:chartSlides,
  materializeLiteralChartWorkbooks:true,fontPolicy,verifyArtifactToolImport:true,receiptPath:path.join(work,'validation-r2.json')});
}catch(e){
 // This host can deny hard links after successful validation; preserve exact bytes.
 if(e.code!=='EPERM'||e.syscall!=='link'||e.dest!==finalPath)throw e;
 await fs.copyFile(draft,finalPath,constants.COPYFILE_EXCL);
}
// Reimport and render the final PPTX, including all appendix slides.
const finalDeck=await PresentationFile.importPptx(await FileBlob.load(finalPath));
for(let i=0;i<finalDeck.slides.items.length;i++){
 const png=await finalDeck.export({slide:finalDeck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(work,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 console.log('Rendered',i+1,'/',finalDeck.slides.items.length);
}
await fs.writeFile(path.join(datadir,'slide_index.json'),JSON.stringify({date:'2026-10-21',stage:'展示会前・現地未確認',main_slides:3,appendix_slides:17,slides:slideIndex},null,2)+'\n');
console.log(JSON.stringify({finalPath,slides:20,nativeTables:tableSlides,nativeCharts:chartSlides}));
