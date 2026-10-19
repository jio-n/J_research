import fs from 'node:fs/promises';
import path from 'node:path';
import {constants} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from 'file:///C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const root=path.resolve('.'),work=path.join(root,'.build/technical_report/slides'),pub=path.join(root,'.build/technical_report/publish');
await fs.mkdir(work,{recursive:true});await fs.mkdir(pub,{recursive:true});
const d=JSON.parse(await fs.readFile('.build/technical_report/report_content.json','utf8'));
const refs=new Map(d.references.map(r=>[r.id,r]));
const skill='C:/Users/paulr/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.11052/skills/presentations';
const python='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES='C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const ink='#18354C',blue='#225B92',muted='#64778A',line='#D4DEE7',pale='#EEF3F8';
const deck=Presentation.create({slideSize:{width:1920,height:1080}}),native=[];
function wrap(t,max){return String(t).split('\n').map(s=>{let n=0,out='';for(const c of s){const w=/[\u0020-\u007e]/.test(c)?.52:1;if(n+w>max&&!/[。、）」]/.test(c)){out+='\n';n=0}out+=c;n+=w}return out}).join('\n')}
function txt(s,name,t,x,y,w,h,size=30,bold=false,color=ink,uri){const a=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=uri?[[{run:t,link:{uri,isExternal:true}}]]:t;a.text.style={fontSize:size,bold,typeface:'Noto Sans JP',color,insets:0,autoFit:'none',wrap:'none',verticalAlignment:'top'};return a}
function base(title,context){const s=deck.slides.add();s.background.fill='#FFFFFF';txt(s,'title',title,80,48,1760,90,45,true);txt(s,'context',wrap(context,75),82,151,1756,72,26,false,muted);return s}
function finish(s,ids,limit,additionalIds=[]){txt(s,'limit',wrap(limit,83),82,1007,1685,52,20,false,muted);txt(s,'page',String(deck.slides.items.length).padStart(2,'0'),1793,1015,48,28,20,false,muted);
 let x=82;for(const id of ids){const r=refs.get(id),e=r.evidence.find(e=>String(e.year)==='2026'&&e.url.includes('jimtof.org/'))||r.evidence[0];txt(s,'source-'+id,id,x,963,95,30,20,false,blue,e.url);x+=105}
 s.speakerNotes.text=[...new Set([...ids,...additionalIds])].map(id=>{const r=refs.get(id);return `${id} ${r.title}\n${r.card_ids.join(', ')}\n`+r.evidence.map(e=>`${e.evidence_id}\n${e.title}\n${e.url}\n該当箇所 ${e.locator}\n確認日 ${e.checked_date}\n種類 ${e.evidence_type}`).join('\n\n')}).join('\n\n')+'\n\n公式記載はメーカー説明。横断解釈は分析。開発提案と将来像は未検証の仮説。';}
function table(s,values,widths,heights,font=29,top=250){const t=s.tables.add({rows:values.length,columns:values[0].length,left:80,top,width:1760,height:heights.reduce((a,b)=>a+b,0),columnWidths:widths,values});t.borders.assign({fill:line,width:1,style:'solid'});for(let r=0;r<values.length;r++){t.rows[r].height=heights[r];for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?'#244B63':r%2?pale:'#FFFFFF';cell.text.style={fontSize:r===0?font+1:font,bold:r===0||c===0,typeface:'Noto Sans JP',color:r===0?'#FFFFFF':ink,insets:12,wrap:'square',autoFit:'none',verticalAlignment:'top'};}}native.push(deck.slides.items.length);return t}

// 01 Opening conclusion rather than a separate ornamental cover.
{
 const s=base('JIMTOF2026 技術動向','2026年10月19日　公開公式資料による事前調査');
 txt(s,'lead','人手が残る準備・判断・付帯作業へ\nAIと自動化の対象が広がる',82,285,1730,170,64,true);
 const lines=[['生産準備','図面・加工履歴・要求から、見積や工程・コードの案を作る。'],['加工と検査','負荷・寸法・工具状態を捉え、調整や交換の判断を助ける。'],['物理作業と運用','搬送に加え、切粉処理、段取り、トラブル時の対処を支援する。']];
 lines.forEach(([label,body],i)=>{const y=520+i*115;txt(s,'label-'+i,label,84,y,350,47,32,true,blue);txt(s,'body-'+i,wrap(body,45),450,y,1355,80,32)});
 finish(s,['S01','S08','S12','S16','S05'],'上段は横断分析。2026年は展示予定。344候補カードと57詳細比較事例は調査の深さが異なる。');
}
// 02 Requested role matrix, native and editable.
{
 const s=base('どの仕事を どこまで技術が担うか','仕事と担当する役割の代表配置。複数の役割に現れる製品があり、自律性・成熟度の順位ではありません。');
 const matrix=structuredClone(d.matrix);matrix[3][2]='ProPlanAI\nCAMAssist\n工程と経路案\n[S02,S03]';matrix[4][0]='作業・調整';
 table(s,matrix,[185,225,225,225,225,225,225,225],[85,156,156,156,156],23,235);
 finish(s,['S01','S04','S07','S09','S12','S16','S20','S28'],'配置は分析。参考出品と人の遠隔操作を区別。代表例なしは企業・技術・需要の不在を意味しない。',d.matrix.flat().join(' ').match(/S\d{2}/g));
}
// 03 Three preparation tasks share a need, but not the same input or output.
{
 const s=base('生産準備では 案づくりの対象が異なる','経験に頼る準備を減らすというニーズに対し、図面検索、工程予測、経路生成が使われています。');
 table(s,[['対象の仕事','使う情報','AIが助ける部分','人が確かめること'],['見積を作る\n匠フォース [S01]','図面、類似案件、原価','材料費・加工費等から\n見積書案を作る','計算の根拠、修正、\n承認と社外への送信'],['工程を考える\nProPlanAI [S02]','形状特徴、過去ジョブ','新部品の加工工程を\n予測する','データの準備、工程の採用、\n最終NCへの反映'],['加工経路を作る\nCAMAssist [S03]','工具、材料、機械等の条件','加工戦略・工具経路・\n条件の案を作る','前提の設定、案の調整、\n加工検証']],[350,420,490,500],[80,180,180,180],30,255);
 txt(s,'insight','比較するのは、生成時間だけでなく\n修正量と初品までの手戻り。',85,895,1680,65,27,true,blue);
 finish(s,['S01','S02','S03'],'AI CAMは2024以前にも存在。過去ジョブを使う工程予測と、経路・条件案の生成は役割を分ける。');
}
// 04 An agent's installation location matters.
{
 const s=base('AIエージェントは 設計と運用で役割が違う','何を参照し、どんな出力を作り、実機の操作にどこまでつながるかを分けて比較します。');
 table(s,[['実装先','支援する仕事','出力の例','人と実行権限'],['制御開発環境\nCoAgent Engineering [S04]','PLC、I/O構成、HMIの設計','コード案、構成案、画面案','専門家が確認・承認。\n実機起動等の権限は未確認。'],['電気設計環境\nEplan Copilot [S06]','文脈に合う情報と\n操作手順を探す','回答、推奨、手順','人が意思決定。\n設計変更の自動採用は未確認。'],['設備の運用支援\nCoAgent Operations [S05]','機械データと文書から原因・対処を検討','原因仮説、対処案','専門家が制御権を保持。\n提供時期・書込範囲等は要確認。']],[390,450,430,490],[80,195,195,195],29,255);
 finish(s,['S04','S05','S06'],'PLCコード支援は2023、I/O・HMIは2025にも公式説明あり。製品発表を完全自律運転の実績としない。');
}
// 05 Timing is the simplest explanation of the competing control approaches.
{
 const s=base('加工の最適化は 判断する時点と入力が異なる','同じ能率・品質の課題でも、事前予測、加工中の適応制御、測定後の補正は異なる方式です。');
 table(s,[['いつ','入力と方式','何を変えるか','代表例と確認事項'],['加工前','切削物理、材料・工具、\n力・動力の制約','NCの送りを最適化','Vericut Force [S07]\nモデルと限界条件を準備。'],['加工中','実測した主軸負荷に応じる\n適応制御','その場で送り速度を調整','ACM [S08]\n負荷限界・停止復帰は要確認。'],['寸法計測後','計測結果のフィードバック','工具オフセット等を更新','Renishaw Central＋IPC [S09]\n補正上限・異常値処理を確認。'],['工具刃先の計測と加工','機内3D画像とAI補正','幅・角度を狙い値へ近づける','サイバーRC GH5 [S10]\n方式詳細・過研磨時の対処は未公開。']],[240,500,475,545],[75,155,155,155,155],29,245);
 finish(s,['S07','S08','S09','S10'],'Force・ACM・Centralは2024にも掲載。各方式を一律に学習AIとは扱わない。');
}
// 06 Diagnosis and the next operational decision are not interchangeable.
{
 const s=base('検査の判定から 交換・保全の判断支援へ','観測した状態をどう行動へ結び付けるかが焦点。ただし、交換や停止の自動実行まで同じ範囲ではありません。');
 table(s,[['対象','認識・判断すること','支援する次の仕事','残る確認'],['製品の外観','良品との差で異常を検出\nHACARUS Check ZERO [S11]','人の良否注釈で判定を追加調整','画像・注釈の準備、\n更新モデル採用と出荷判定'],['工具の刃先','欠け・摩耗をAI判定\nツールコラージュ [S12]','摩耗記録から寿命・交換時期を提案\nアナライザー [S12]','対象工具と加工条件、\n継続使用・交換の決定者'],['工具の画像','VTC 6.0のAI摩耗診断\nハイデンハイン [S13]','工具の点検・使用判断を支援','判定閾値と自動交換への接続'],['設備の電流・振動','新品状態との差から劣化を診断\nムラテックCCS [S14]','点検や部品交換の判断を支援','誤警報、最終判断、\n異なる設備への適用範囲']],[250,525,540,445],[75,155,155,155,155],28,245);
 finish(s,['S11','S12','S13','S14','S15'],'AI摩耗判定・設備診断は2024にも存在。ZERO追加学習は2025、工具寿命には以前の研究発表もある。');
}
// 07 Concrete physical tasks, with conventional mechanisms as comparators.
{
 const s=base('フィジカルAIは 対象作業と機構から評価する','搬送の先に残る切粉処理・面取り・段取りを、認識と動作、または機構によって省力化する提案です。');
 table(s,[['残る仕事','企業と展示','使う技術・構成','提供段階と人の関わり'],['切粉の絡まりを除く','TAKISAWA TR-20W [S16]','絡まりの認識・判断と\n主軸の切粉除去','参考出品。失敗検出・\n再試行・引継ぎは未確認。'],['不定形ワークの\n面取り','東京エレクトロンデバイス [S17]','3Dスキャンから\n加工軌道を生成','条件設定・干渉確認・\n品質承認の範囲を確認。'],['小径ねじ等を拾う','カネテック [S18]','カメラ、協働ロボット、\n磁気ピンセット','AIを明記。具体的な\n判断箇所は未公開。'],['ブラシ摩耗に追従','XEBEC CPS [S19]','突出し量を自動調整する\n工具機構とロボット','機構による自動化。\nAI使用は未確認。']],[300,465,510,485],[75,155,155,155,155],29,245);
 finish(s,['S16','S17','S18','S19','S20','S21','S29'],'爪交換・位置復旧も対照技術。人型機体の遠隔操作・教示を、自律作業の実証とは扱わない。');
}
// 08 The enabling layer is connected to the actual work.
{
 const s=base('データと仮想環境は 用途に結び付けて評価する','つながること、学習モデルを作れること、仮想で試せることと、現場で任せられることは別の条件です。');
 table(s,[['基盤','具体例','何の準備を減らすか','確認する限界'],['機器情報の意味づけ','たけびし OPC UA連携 [S23]','設備データをエージェントへ渡す','公開データとメソッド、\n書込権限は未確認。'],['学習モデルの作成','TwinCAT ML Creator [S22]','学習・モデル選択・ONNX出力','人が目的・データ・注釈を準備。\n実機採用基準を確認。'],['加工の仮想検証','FANUC Smart Digital Twin [S24]\nシーメンス工作機械ツイン [S25]','加工前の挙動・工程を確認する','モデルと実機の一致、\n検証対象外の事象を確認。'],['物理学習用のデータ','NdotLight TRINIX [S26]','CADから形状・物理属性等を生成','属性の正しさや自己修正の収束、\n実機との誤差は未確認。']],[300,535,465,460],[75,155,155,155,155],28,245);
 finish(s,['S22','S23','S24','S25','S26'],'基盤単体で自律化を示すものではない。海外の人型実証とJIMTOFの展示は同一システムと確認していない。');
}
// 09 A second matrix compares ways of solving the same work.
{
 const s=base('技術方式の違いと 人に残る仕事','方式ごとの比較。AIという呼称より、方式が使う入力と出力、設定・承認・例外対応を確認します。');
 table(s,[['方式','得意とする支援','代表例','人に残る仕事'],['生成AI・エージェント','文脈を使う回答・コード・\n対処案の生成','CoAgent、Eplan Copilot\n匠フォース [S01,S04–S06]','前提の指定、案の確認・修正、\n実行や設計変更の承認'],['画像・3D認識','外観・摩耗の検出、\n形状からの作業位置・軌道','HACARUS、モリマシナリー\n東京ED [S11,S12,S17]','撮像・注釈、条件設定、\n誤判定や加工品質の確認'],['学習による予測・診断','過去の状態・履歴から\n工程や寿命・劣化を推定','ProPlanAI、寿命推定\nムラテックCCS [S02,S12,S14]','データ準備、適用範囲の確認、\n継続使用・保全の決定'],['シミュレーション・物理最適化','事前検証、切削負荷等の\n予測とNC最適化','Vericut、Force\n工作機械ツイン [S07,S24]','モデルと制約の設定、\n実機との差の評価'],['機構・規則による自動化','送り調整、補正、交換、\n在庫・購買処理','ACM、IPC、MMK、WinTool\n[S08,S09,S20,S27]','閾値・設定、承認、\n対象変更と異常時の対処']],[330,500,475,455],[70,125,125,125,125,125],27,250);
 finish(s,['S01','S04','S07','S12','S17','S27'],'方式分類は分析。全製品の内部アルゴリズムを確認したものではない。複数方式の併用もある。',['S02','S05','S06','S08','S09','S11','S14','S20','S24']);
}
// 10 Macro year comparison is a reading, not a list of product releases.
{
 const s=base('2024年からの変化は 支援する仕事の広がりにある','公開記載を横断した分析。新発明、既存技術の継続、用途・構成の拡張を区別します。');
 const cols=[['以前からある技術','CAM支援とPLCコード支援\n負荷適応と計測フィードバック\nAI摩耗診断と段取り自動化','2024以前にも存在するため、\n2026初の方式とは言えない。'],['具体化する対象','見積や工程案、I/OとHMI\n摩耗から交換時期の提案\n切粉処理と変動する付帯作業','対象作業と構成の広がりを、\n個別の公式資料で確かめる。'],['比較が残る部分','変更後の再設定と適用限界\n人の介入と失敗後の復帰\n提供段階と顧客での稼働','説明の具体化を、性能向上や\n普及の証明とは扱わない。']];
 cols.forEach(([title,body,meaning],i)=>{const x=82+i*602;txt(s,'h-'+i,title,x,285,550,65,38,true,blue);txt(s,'body-'+i,wrap(body,17),x,400,540,290,32);txt(s,'meaning-'+i,wrap(meaning,18),x,730,540,150,30,true)});
 finish(s,['S03','S04','S08','S11','S12','S16','S30'],'2024資料がない事例は比較不能。追加学習は2025、PLC支援は2023等の発表も参照している。',['S01','S02','S05','S06','S07','S09','S13','S14','S17','S20','S21']);
}
// 11 Strategic proposals retain concrete technical targets.
{
 const s=base('研究開発は 四つの仕事を候補にする','公開情報からの開発仮説。市場の空白、自社の適合性、性能優位を実証した提案ではありません。');
 table(s,[['候補領域','顧客の負担','何を開発するか','比べる効果'],['加工知識を扱う\n生産準備AI','多品種の見積・工程検討を\n毎回熟練者が組み立てる','図面・履歴・設備制約を使う工程案を\n既存CAMと検証へつなぐ','総準備時間、修正量、\n初品の手戻り'],['品質と工具状態を使う\n自律加工','条件、工具交換、品質を\n人が経験から結び付ける','切削予測・信号・工具画像・寸法を使い\n継続・条件変更・交換を支援','品質・工具利用量\n加工時間・再調整時間'],['付帯作業を担う\nフィジカルAI','切粉処理やバリ取り、\n品種変更時の教示が残る','作業を絞り、認識・工具機構・動作・\n完了判断を組み合わせる','完了率、教示時間、\n介入回数、タクト'],['変化に対応する\n工場運用AI','停止・不足のたびに情報を集め\n代替案と指示を組み直す','設備・工具・進捗と過去対処から\n案と担当作業を示す','状況確認・再計画の時間、\n実行できた提案、停止時間']],[330,470,560,400],[75,155,155,155,155],28,245);
 finish(s,['S01','S02','S04','S09','S12','S16','S17','S23','S27'],'既存製品の適用・連携との比較を先に行う。各領域で部品群・加工法・作業・例外業務を限定する。',['S03','S05','S07','S08','S10','S11','S13','S14','S15','S18','S19','S20','S21','S28']);
}
// 12 Close with evidence to collect, not a generic conclusion slide.
{
 const s=base('現地では 適用条件と人の残作業を確認する','展示の説明から、実際に使える範囲と開発の必要性を判断するための論点。');
 const left=[['入力と変更','同じ対象で、工具・材料・形状が変わった時の\n再設定と生成案の修正を確認する。'],['判断と実行','どの判断をAIが行い、誰が承認し、\nどの操作まで実行できるかを確認する。'],['失敗と品質','見逃し・過検出、作業未完了、測定不能の時に、\nどう止まり、誰が復帰させるかを確認する。']];
 left.forEach(([label,body],i)=>{const y=285+i*205;txt(s,'l-'+i,label,83,y,780,52,35,true,blue);txt(s,'lb-'+i,wrap(body,28),83,y+70,820,115,29)});
 txt(s,'right-title','技術の説明に加えて聞くこと',1010,286,820,60,36,true,blue);
 txt(s,'right-body',wrap('対象顧客、導入工数、価格、\n有償導入・PoC・受注・引き合い。\n市場規模は対象と算定根拠を確認する。',26),1010,390,790,190,31);
 txt(s,'decision',wrap('現地確認後の判断\n既存製品で解ける範囲と、\n追加の研究を要する範囲を分ける。',25),1010,695,790,180,34,true);
 finish(s,['S04','S08','S10','S11','S16','S26','S27'],'公式記載、現地での説明・実演、顧客での稼働、将来構想を区別して記録する。原典URLは各スライドのノートへ。');
}

for(let i=0;i<deck.slides.items.length;i++){
 const png=await deck.export({slide:deck.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(work,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
const draft=path.join(work,'candidate.pptx'),validated=path.join(pub,'technical-report-'+Date.now()+'.pptx');
await(await PresentationFile.exportPptx(deck)).save(draft);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
try{await finalizePresentation({workspaceDir:root,candidatePath:draft,finalPath:validated,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-heading-fit',...native.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:12,requiredNativeTableOwnerSlides:native,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Noto Sans JP']},verifyArtifactToolImport:true,receiptPath:path.join(work,'validation.json')});}
catch(e){if(e.code!=='EPERM'||e.syscall!=='link'||e.dest!==validated)throw e;await fs.copyFile(draft,validated,constants.COPYFILE_EXCL);}
const output=path.join(root,'outputs/JIMTOF2026_技術動向レポート_20261019.pptx');await fs.copyFile(validated,output);
console.log(JSON.stringify({output,slides:deck.slides.items.length,native_tables:native}));
