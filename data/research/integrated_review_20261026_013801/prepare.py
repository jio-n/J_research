import pathlib,json,csv,re,unicodedata,zipfile,xml.etree.ElementTree as E,collections,hashlib,posixpath,copy
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];OUT=R/'outputs'/D.name
def read(s):return json.loads((R/s).read_text(encoding='utf-8-sig'))
def save(name,x): (D/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def key(s):
 s=unicodedata.normalize('NFKC',s).casefold();s=re.sub(r'\([^)]*\)','',s)
 return re.sub(r'[\s.,・/&-]','',s.replace('株式会社','').replace('有限会社',''))
def boothkey(s):
 m=re.search(r'[A-Z]+\d+',s or '');return m[0] if m else s
M='http://schemas.openxmlformats.org/spreadsheetml/2006/main';REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships';ns={'m':M}
source='outputs/overlap_column_20261025_172348/JIMTOF2026_調査企業一覧_C列重複管理付き.xlsx'
headers=['企業名','ブース','他シートとの重複','優先','注目アイテム','タグ','着眼点','補足：当日聞くこと','追加技術資料']
source_hash=hashlib.sha256((R/source).read_bytes()).hexdigest();canonical=[];alllinks=[]
with zipfile.ZipFile(R/source) as z:
 styles=E.fromstring(z.read('xl/styles.xml'));xfs=list(styles.find('m:cellXfs',ns));fills=list(styles.find('m:fills',ns))
 def explicit_fill(cell):
  xf=xfs[int(cell.attrib.get('s',0))];f=fills[int(xf.attrib.get('fillId',0))]
  fg=f.find('m:patternFill/m:fgColor',ns)
  if fg is None:return None
  rgb=fg.attrib.get('rgb','')[-6:]
  return '#'+rgb if len(rgb)==6 and rgb.upper() not in ['FFFFFF','000000'] else None
 ss=[''.join(t.text or '' for t in s.findall('m:t',ns)+s.findall('m:r/m:t',ns)) for s in E.fromstring(z.read('xl/sharedStrings.xml'))]
 for i,name in enumerate(['AI・フィジカルAI','自動化・自律化50社'],1):
  root=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));rows=[];heights=[];highlights=[]
  def val(c):
   if c is None:return None
   if c.attrib.get('t')=='inlineStr':return ''.join(t.text or '' for t in c.findall('m:is/m:t',ns)+c.findall('m:is/m:r/m:t',ns))
   v=c.find('m:v',ns)
   return None if v is None else (ss[int(v.text)] if c.attrib.get('t')=='s' else v.text)
  for r in root.findall('m:sheetData/m:row',ns):
   rn=int(r.attrib['r'])
   if rn==1:continue
   cells={c.attrib['r'][:1]:c for c in r};rows.append([val(cells.get(c)) for c in 'ABCDEFGHI']);heights.append(float(r.attrib.get('ht',30)))
   for c in r:
    color=explicit_fill(c)
    if color:highlights.append(dict(cell=c.attrib['r'],color=color))
  rels={x.attrib['Id']:x.attrib for x in E.fromstring(z.read(f'xl/worksheets/_rels/sheet{i}.xml.rels'))}
  for h in root.findall('m:hyperlinks/m:hyperlink',ns):
   target=rels[h.attrib['{'+REL+'}id']]['Target'];alllinks.append(dict(sheet=name,cell=h.attrib['ref'],url=target,tip=h.attrib.get('tooltip','')))
  canonical.append(dict(name=name,headers=headers,values=rows,source_values=copy.deepcopy(rows),source_heights=heights,highlights=highlights))
assert [len(x['values']) for x in canonical]==[32,59]
changes=[];comments=read('data/research/'+D.name+'/user_comments.json')
wta=read('data/research/overlap_column_20261025_172348/pending_user_comments.json')['comments'][0]
comments.append(dict(company='Wintech Automation Co., Ltd',priority=wta['priority'],item=None,focus=wta['user_focus'],questions=wta['suggested_questions'],tags=None))
def setlink(sheet,cell,url,tip=''):
 alllinks[:]=[l for l in alllinks if not(l['sheet']==sheet and l['cell']==cell)]
 alllinks.append(dict(sheet=sheet,cell=cell,url=url,tip=tip))
for comment in comments:
 hits=0
 for sh in canonical:
  for r,v in enumerate(sh['values'],2):
   if key(v[0])!=key(comment['company']):continue
   hits+=1;before=copy.deepcopy(v)
   v[3]=comment['priority'];v[6]=comment['focus'];v[7]=comment['questions']
   if comment.get('item'):v[4]=comment['item']
   if comment.get('tags'):v[5]=comment['tags']
   if comment.get('url'):setlink(sh['name'],f'E{r}',comment['url'],'企業・製品の説明。展示の確認範囲は技術資料・照合記録を参照。')
   if comment.get('extra_url'):
    v[8]=comment['extra_label'];setlink(sh['name'],f'I{r}',comment['extra_url'],'注目アイテムとは別の技術資料。関連方式と今回の実演を区別。')
   changes.append(dict(sheet=sh['name'],row=r,company=v[0],before=before,after=copy.deepcopy(v),origin='ユーザー発言の整理。質問はAIによる整理案。'))
 assert hits>0,comment['company']
# Useful new research belongs to the technical-reference column, not to user-authored focus text.
for sh in canonical:
 for r,v in enumerate(sh['values'],2):
  if key(v[0])==key('三菱電機'):
   assert v[8] is None
   v[8]='関連研究：CNC上のエッジDTで加工誤差を実時間補正（展示未確認）'
   setlink(sh['name'],f'I{r}','https://www.mitsubishielectric.co.jp/ja/pr/2026/0325/','構造変形由来の誤差補正研究。ヒューマノイド連携とは別技術。今回の展示は未確認。')
selected={key(v[0]) for sh in canonical for v in sh['values']};assert len(selected)==59
visit_sheets=[]
for sh in canonical:
 visit_sheets.append(dict(name=sh['name'],headers=headers,values=sh['values'],kind='search',merges=[],origin_sheet=sh['name'],highlights=sh['highlights']))
for sh in canonical:
 name='閲覧_AI・フィジカルAI' if sh['name'].startswith('AI') else '閲覧_自動化・自律化'
 groups=collections.OrderedDict()
 for r,v in enumerate(sh['values'],2):groups.setdefault((key(v[0]),boothkey(v[1])),[]).append((r,v))
 rows=[];merges=[];highlights=[]
 for group in groups.values():
  start=len(rows)+2
  for r,v in group:
   nr=len(rows)+2;rows.append(copy.deepcopy(v))
   highlights.extend(dict(cell=h['cell'][0]+str(nr),color=h['color']) for h in sh['highlights'] if int(h['cell'][1:])==r)
   for l in list(alllinks):
    if l['sheet']==sh['name'] and int(l['cell'][1:])==r:
     if l['cell'][0]=='A' and nr!=start:continue
     alllinks.append(dict(l,sheet=name,cell=l['cell'][0]+str(nr)))
  end=len(rows)+1
  if end>start:
   merges.extend([f'A{start}:A{end}',f'B{start}:B{end}'])
   for rr in range(start+1,end+1):rows[rr-2][0]=None;rows[rr-2][1]=None
 visit_sheets.append(dict(name=name,headers=headers,values=rows,kind='view',merges=merges,origin_sheet=sh['name'],highlights=highlights))
readme=[['用途','使い方'],['編集・検索','AI・フィジカルAI／自動化・自律化50社：1行1アイテム。ここで優先度・着眼点・質問を更新する。'],['企業別の閲覧','閲覧_で始まる2シート：企業名・同じブースを縦結合。右側はアイテム別。検索用の内容を同時点で複製した閲覧専用のスナップショット。編集は検索側で行い、再生成時に同期する。'],['今回の反映','16社のコメントと、Wintechの評価を統合。パスカルはユーザー確認済み。冒頭の企業未特定コメントは割当てず保留。'],['判断と事実','着眼点はユーザーの関心・評価。質問は発言からAIが整理。メーカーの仕組みと実演確認とは別。'],['リンク','企業名＝公式出展ページ。注目アイテム＝製品・技術資料。追加技術資料＝異なる補足資料。着眼点・質問は黒文字。'],['TPR','メーカー資料でGDE等の加工機へのフィードバックを確認。今回の閉ループ実演は未確認。'],['ブース差','HexagonのE2013とE7035は分けて保持。'],['書式','企業別閲覧にはセル結合があるため並べ替え・絞り込みは検索用シートで行う。'],['時点','2026-10-26／公開資料による視察準備。現地確認済みとはしない。']]
visit_sheets.append(dict(name='読み方',headers=readme[0],values=readme[1:],kind='notes',merges=[]))
save('visit_plan.json',dict(source_workbook=source,source_sha256=source_hash,sheets=visit_sheets,links=alllinks,current_companies=59,source_canonical_rows=91,changed_rows=len(changes),commented_companies=17))
save('comment_integration.json',changes)
items=read('data/research/'+D.name+'/_private/all_items.json');outside=read('data/research/'+D.name+'/_private/outside_raw.json')
exclusions=read('data/research/visit_gap_review_20261023_163347/user_visit_exclusions.json')
if isinstance(exclusions,dict):
 exclusions=exclusions.get('companies',exclusions.get('exclusions',exclusions.get('items',[])))
save('_private/exclusions_shape.json',exclusions)
allrows=list(csv.DictReader((R/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig')));byid={r['exhibitor_record_id']:r for r in allrows}
# JSON exclusion fields vary across editions; the source CSV has a stable company-name column.
exrows=list(csv.DictReader((R/'data/research/visit_gap_review_20261023_163347/user_visit_exclusions.csv').open(encoding='utf-8-sig')))
companyfield=next(k for k in exrows[0] if 'company' in k or '企業' in k)
excluded={key(r[companyfield]) for r in exrows}
fresh=read('data/research/'+D.name+'/evidence_updates.json');fresh_byid={x['id']:x for x in fresh}
newmazak=dict(id='IR-MAZAK-AGENT',company='ヤマザキマザック株式会社',booths=['E1001'],listing_ids=[],item='ABEJA共同開発：工程設計・生産計画AIエージェント＋ロボット学習環境',task='工程設計・生産再計画・行動学習',need='熟練者の工程判断の継承と、特急注文・部材不足への対応',input='加工部品、工程知識、設備稼働、在庫、現場の運用データ',method='人の関与を前提に工程・スケジュールを提案するエージェントを開発し、データ収集・学習・実機検証の環境を構築。',output='工程案・生産計画案／ロボット行動学習の環境（開発計画）',human='知識・制約の提供、提案の評価・採否、学習と実機検証。',limits='モデル構成、提供時期、完成度、JIMTOF個別展示は未確認。',exhibit='企業出展確認・当該構想の展示未確認',exhibit_note='共同開発開始の発表。MAZATROL DXの既存機能と分ける。',stage='共同開発開始',tags={t:dict(status='構想・開発',reason='IR05の共同開発説明。実装済みではない。') for t in ['AI','フィジカルAI','自律化','自動化']},tag_names=['AI','フィジカルAI','自律化','自動化'],sources=[dict(url=fresh_byid['IR05']['url'],publisher='ABEJA',locator=fresh_byid['IR05']['locator'],title=fresh_byid['IR05']['title'],checked_date='2026-10-26')],depth='共同開発発表の本文を今回確認',_source='今回追加')
outside.append(newmazak);items.append(newmazak)
priority={
 'GR-N01':('優先照会','過去にユーザーが優先訪問を指定。生成AIによる観察画像変換とCNN判定の接続を比較できる。自動ドレス・実演は未確認。'),
 'GR-C01':('優先照会','最新のCAMエージェントが工程・工具・条件・経路・検証をどこまで実行するかを確認。Beta単体の会場実演は要確認。'),
 'IR-MAZAK-AGENT':('優先照会','最新AI・全体構想・熟練知・再計画の四関心を一度に照会できる。ただし共同開発段階であり展示は未確認。'),
 'FC033':('優先照会','ワークの測定偏差から複数工程・工具の補正へ返す統計的な閉ループ。単一寸法補正を越える割当・管理限界を比較する。'),
 'FC034':('優先照会','機上のワーク測定から工具別補正・位置補正・再加工へ接続。直接ワーク加工の品質維持に近い。'),
 'FT-M01':('優先照会','切削物理と制約から送り・切込み等を決める。条件算出と加工中の適応制御の境界を確かめる。'),
 'FT-M02':('優先照会','工程生成・ツイン・現物照合・衝突回避を接続する全体構成。SDKのため自社開発で使えるモジュールも確認。'),
 'AC146':('優先照会','3D実測形状から加工経路を作り、供給・加工へつなぐ。ワークの変化に対する経路生成の範囲を比較できる。AI方式は未確認。'),
 'GR-O01':('優先照会','パイプというワークの3D形状偏差を曲げ補正へ戻す。多点形状・反復補正の収束を比較できる。個別展示は要確認。'),
 'FC020':('比較照会','工具・保持・機械の条件を与えて加工戦略を生成するAI CAM。人の修正と物理ベースの条件選択を確認。'),
 'FT-SI01':('比較照会','プロジェクトを読みPLC/HMIの生成・試験・修正まで行う最新エージェント。加工制御そのものとは分けて比較。展示未確認。'),
 'FT-Z01':('比較照会','対話・工程知識を加工プログラムへ変換する既存製品。共同開発エージェントとの差を確認。'),
 'FT-J01':('比較照会','工程設計支援の実装を、LLMエージェント方式と比較する対象。'),
 'FT-J02':('比較照会','実際のワークへの教示・位置合わせを減らす技術。自動調整の対象と失敗時の復帰を確認。'),
 'FC038':('比較照会','工具形状・摩耗の認識を加工の継続判断へつなげられるか。画像解析だけか補正・交換までかを確認。'),
 'AC052':('比較照会','穴・砥石の測定からワーク研削補正へつながる候補。方式・展示範囲の情報が薄く、まず技術照会。'),
 'GR-A01':('参考','工具製造が対象。計測・振れ・温度の複合補償として参考になるが、ユーザーのワーク直接加工を優先。')}
updates={'FC033':('IR06',),'FT-M01':('IR07','IR08'),'FT-M02':('IR07',),'GR-C01':('IR09','IR10'),'FC034':('IR11',),'FT-SI01':('IR12',),'FC020':('IR13',),'GR-N01':('IR19',),'IR-MAZAK-AGENT':('IR05',)}
for x in outside:
 x['fresh_review_ids']=list(updates.get(x['id'],[]))
 if x['id']=='FT-M01':x['limits']+=' 今回再確認：物理モデルによる送り最適化であり、実機センサ入力による実時間閉ループの採用は未確認。'
 if x['id']=='FC033':x['method']='測定寸法の移動平均と標準偏差により補正値と管理限界を計算し、複数工程・工具のオフセットへ反映。補正上限で工具交換・停止につなぐ。'
 if x['id']=='FC034':x['method']='機上の測定値から工具別補正を計算。工具摩耗補償、NOK排出、最大5軸のワーク位置補正を説明。'
 if x['id']=='GR-I02':
  x['tags']['自律化']=dict(status='—',reason='生成AIによる操作支援は機械の自律動作と分ける。旧判定を今回訂正。')
  x['tag_names']=[t for t in x.get('tag_names',[]) if t!='自律化'];x['limits']+=' 今回分類訂正：Assistantによる操作支援自体を自律走行・自律加工と扱わない。'
 x['recommendation'],x['recommend_reason']=priority.get(x['id'],('参考',x.get('visit_analysis',{}).get('priority_reason') or '既存台帳で四タグのいずれかに該当。今回の四関心への寄与・方式・新規性は未再評価。'))
 # Human decisions override a researcher's recommendation.
 keys={key(x['company'])}|{key(byid[i]['company_name']) for i in x.get('listing_ids',[]) if i in byid}
 x['user_excluded']=bool(keys&excluded)
 x['history']='以前のユーザー判断：訪問対象外。関連性の否定ではない。' if x['user_excluded'] else ('以前ユーザーが優先指定／直近一覧では未掲載' if x['id']=='GR-N01' else '現在の59社一覧に未掲載')
 if x['user_excluded']:x['recommendation']='過去の対象外';x['recommend_reason']='ユーザーの訪問しない判断を優先。自動復帰しない。'
 x['current_review']='2026-10-26 原典の該当本文を再確認' if x['fresh_review_ids'] else '既存調査を継承。今回の原典再精読は未実施。'
 x['company_url']=next((byid[i]['detail_url'] for i in x.get('listing_ids',[]) if i in byid),'')
 if not x['company_url']:
  found=next((r for r in allrows if key(r['company_name'])==key(x['company'])),None)
  if found:x['company_url']=found['detail_url']
 x['main_url']=next((fresh_byid[i]['url'] for i in x['fresh_review_ids'] if i in fresh_byid),None) or next((s.get('url') for s in x.get('sources',[]) if s.get('url') and 'jimtof.org/2024' not in s['url'] and 'github.com' not in s['url']),x['company_url'])
 x['question_text']='\n'.join(x.get('visit_analysis',{}).get('questions',[])[:4]) or x.get('check') or '入力・判断対象・変更する量、人の準備、異常時の復帰、従来からの変化、今回の実演範囲を確認する。'
outside.sort(key=lambda x:({'優先照会':0,'比較照会':1,'参考':2,'過去の対象外':3}[x['recommendation']],x['company'],x['id']))
active=[x for x in outside if not x['user_excluded']];excluded_items=[x for x in outside if x['user_excluded']]
save('additional_candidates.json',dict(current_company_count=59,source_union_items=len(items),outside_items=len(outside),active_items=len(active),active_companies=len({key(x['company']) for x in active}),excluded_items=len(excluded_items),items=outside,exclusion_csv_source='data/research/visit_gap_review_20261023_163347/user_visit_exclusions.csv',scope='既存405アイテムと今回のマザック共同開発1件。全出展者の新規全面再調査ではない。'))
def tags(x):
 return [(x.get('tags',{}).get(t,{}) or {}).get('status') or ('既存判定' if t in x.get('tag_names',[]) else '—') for t in ['AI','フィジカルAI','自律化','自動化']]
def tagwhy(x):return '\n'.join(t+'：'+(x.get('tags',{}).get(t,{}) or {}).get('reason','未確認') for t in ['AI','フィジカルAI','自律化','自動化'])
ah=['企業名','ブース','推薦区分','注目アイテム','AI','フィジカルAI','自律化','自動化','対象タスク','実現方式・担当機能','注目理由','展示確度','ユーザー判断履歴','現地で聞くこと','追加技術資料','適用限界・留意点','訪問判断','自分の優先度','当日メモ','調査深度','ID']
ad=[];al=[]
for r,x in enumerate(active,2):
 more=next((s for s in x.get('sources',[]) if s.get('url') and s['url'] not in [x['main_url'],x['company_url']] and 'github.com' not in s['url'] and 'jimtof.org/2024' not in s['url']),None)
 ad.append([x['company'],'／'.join(x.get('booths',[])),x['recommendation'],x['item'],*tags(x),x.get('task'),x.get('method'),x['recommend_reason'],x.get('exhibit','未確認')+'／'+x.get('exhibit_note',''),x['history'],x['question_text'],more.get('title') or more.get('locator') or '別の技術資料' if more else None,x.get('limits'),None,None,None,x['current_review']+' '+x.get('depth',''),x['id']])
 for c,u in [('A',x['company_url']),('D',x['main_url'])]:
  if u:al.append(dict(sheet='未掲載候補',cell=f'{c}{r}',url=u,tip='アイテムの展示確度を別欄で確認。'))
 if more:al.append(dict(sheet='未掲載候補',cell=f'O{r}',url=more['url'],tip=more.get('locator','')[:240]))
detailh=['ID','企業名','アイテム','顧客課題','入力データ','実現方式','出力・変える量','人の担当','適用限界・未確認','実用段階','展示確度','四タグの根拠','技術分類','原典URL・位置・日付','今回の確認範囲']
details=[]
for x in active:
 sources='\n'.join((s.get('publisher','発行者未記載')+'｜'+s.get('url','')+'｜'+s.get('locator','位置未記載')+'｜確認 '+s.get('checked_date',x.get('as_of','未記載'))) for s in x.get('sources',[]) if s.get('url'))
 details.append([x['id'],x['company'],x['item'],x.get('need'),x.get('input'),x.get('method'),x.get('output'),x.get('human'),x.get('limits'),x.get('stage'),x.get('exhibit'),tagwhy(x),x.get('physical_ai_class','AI動作接続の個別評価は未確認'),sources,x['current_review']])
excluded_rows=[]
for r in exrows:
 if key(r[companyfield]) in selected:continue
 company=r[companyfield];related=[x for x in excluded_items if key(x['company'])==key(company)]
 excluded_rows.append([company,next((v for k,v in r.items() if 'booth' in k or 'ブース' in k),''),'過去のユーザー判断：訪問しない','関連性を否定するものではない。再推薦しない。','\n'.join(x['item'] for x in related) or '元候補台帳に対応アイテムなし',None])
coverage=[]
for x in items:
 keys={key(x['company'])}|{key(byid[i]['company_name']) for i in x.get('listing_ids',[]) if i in byid}
 status='現在の一覧に収録済み' if keys&selected else ('過去のユーザー対象外' if keys&excluded else '未掲載候補へ抽出')
 coverage.append([x['id'],x['company'],'／'.join(x.get('booths',[])),x['item'],status,x.get('_source','既存調査'),'／'.join(x.get('listing_ids',[]))])
notes=[['項目','説明'],['抽出対象',f"既存405アイテム＋今回のマザック共同開発1件。現在の一覧59社を企業単位で除外。未掲載{len(outside)}アイテムのうち、過去対象外{len(excluded_items)}アイテムを別管理。"],['全候補',f"未掲載候補は{len(active)}アイテム・{len({key(x['company']) for x in active})}社。推薦だけに絞らず保持。"],['四タグ','独立列・重複可。機能記載、呼称、構想、基盤を含む。件数を実装率・普及率として使わない。'],['最新技術','AIエージェント／フィジカルAI・全体構想、直接ワークの自律加工制御、熟練判断の形式知化、工程をまたぐ自動化・自律化を優先。'],['推薦と本人判断','推薦区分は調査者の分析。訪問判断・自分の優先度・当日メモは入力用。既存の訪問しない判断は過去の対象外に保持。'],['確認深度','原典本文まで再確認した候補と、過去の分類を引き継ぐ候補を分離。取得ログだけで技術確認済みと扱わない。'],['同一技術・別法人','HACARUSと日東商事など、別法人の出展は残す。同じ技術が現在の一覧にあっても追加訪問の必要性は利用者が判断。'],['母集団の限界','全出展者1146掲載行を土台にした既存候補台帳の差分抽出。説明不足や旧台帳の未抽出企業を網羅した新規全件調査ではない。'],['分類訂正','ifm moneo Assistantの自律化タグを取り下げ。生成AI操作支援と自律走行・加工動作を区別。'],['更新日','2026-10-26。現地性能・実演は未確認。']]
asheets=[dict(name='未掲載候補',headers=ah,values=ad,kind='candidates',merges=[]),dict(name='技術詳細',headers=detailh,values=details,kind='details',merges=[]),dict(name='過去の対象外',headers=['企業名','元ブース','ユーザー判断','留意点','元台帳の関連アイテム','再検討メモ'],values=excluded_rows,kind='excluded',merges=[]),dict(name='照合記録',headers=['ID','企業名','ブース','技術アイテム','今回の照合結果','元台帳','公式掲載ID'],values=coverage,kind='audit',merges=[]),dict(name='読み方',headers=notes[0],values=notes[1:],kind='notes',merges=[])]
save('additional_workbook_plan.json',dict(sheets=asheets,links=al))
with (D/'additional_candidates.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(ah);w.writerows(ad)
with (D/'screening_audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(asheets[3]['headers']);w.writerows(coverage)
stats=dict(current_companies=59,current_AI_rows=32,current_automation_rows=59,commented_companies=17,changed_rows=len(changes),source_union_items=len(items),outside_items=len(outside),additional_active_items=len(active),additional_active_companies=len({key(x['company']) for x in active}),excluded_items=len(excluded_items),past_excluded_companies=len(excluded_rows),priority_items=sum(x['recommendation']=='優先照会' for x in active),fresh_sources=len(fresh),original_file_sha256=source_hash)
save('stats.json',stats);print(json.dumps(stats,ensure_ascii=False))
