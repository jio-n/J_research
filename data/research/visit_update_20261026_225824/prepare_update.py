import json,pathlib,re,unicodedata,copy,collections,zipfile,xml.etree.ElementTree as E,hashlib,csv
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def key(s):return re.sub(r'[\s.,・/&-]','',re.sub(r'\([^)]*\)','',unicodedata.normalize('NFKC',s).casefold()).replace('株式会社','').replace('有限会社',''))
intake=read('data/research/visit_selection_intake_20261026/intake_summary.json');records={key(x['company']):x for x in intake['company_records']}
base=read('data/research/integrated_review_20261026_013801/visit_plan.json');candidates=read('data/research/integrated_review_20261026_013801/additional_candidates.json')['items'];byid={x['id']:x for x in candidates}
original=R/'outputs/integrated_review_20261026_013801/JIMTOF2026_訪問先一覧_コメント統合・企業別閲覧.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};RN='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
canonical=copy.deepcopy(base['sheets'][:2]);oldlinks=[]
with zipfile.ZipFile(original) as z:
 ss=[''.join(t.text or '' for t in s.findall('m:t',ns)+s.findall('m:r/m:t',ns)) for s in E.fromstring(z.read('xl/sharedStrings.xml'))]
 for n,s in enumerate(canonical,1):
  s['values']=[]
  for row in E.fromstring(z.read(f'xl/worksheets/sheet{n}.xml')).findall('m:sheetData/m:row',ns)[1:]:
   v=[None]*9
   for c in row:
    idx=ord(c.get('r')[0])-65
    if idx>8:continue
    val=c.find('m:v',ns)
    if val is not None:v[idx]=ss[int(val.text)] if c.get('t')=='s' else val.text
   s['values'].append(v)
  rels={t.get('Id'):t.get('Target') for t in E.fromstring(z.read(f'xl/worksheets/_rels/sheet{n}.xml.rels'))}
  for h in E.fromstring(z.read(f'xl/worksheets/sheet{n}.xml')).findall('m:hyperlinks/m:hyperlink',ns):oldlinks.append({'sheet':s['name'],'cell':h.get('ref'),'url':rels[h.get('{'+RN+'}id')]+('#'+h.get('location') if h.get('location') else ''),'tip':h.get('tooltip','')})
headers=canonical[0]['headers'];sheets=[];links=[];lineage=[];excluded=[];unreviewed=[];exlinks=[];unlinks=[]
def transfer(oldname,oldrow,newname,newrow):
 for l in oldlinks:
  if l['sheet']==oldname and int(re.search(r'\d+',l['cell'])[0])==oldrow:links.append(dict(l,sheet=newname,cell=re.sub(r'\d+',str(newrow),l['cell'])))
def color_for(rec,sheet):
 if rec['color_conflict']:return '緑' if sheet.startswith('AI') else '青系'
 return rec['resolved_color']
for s in canonical:
 new=dict(name=s['name'],headers=headers,values=[],kind='search',merges=[],row_colors=[])
 for ri,v in enumerate(s['values'],2):
  rec=records.get(key(v[0]));active=rec and rec['include_in_final_visit_list']
  if active:
   nr=len(new['values'])+2;new['values'].append(v);new['row_colors'].append(color_for(rec,s['name']));transfer(s['name'],ri,s['name'],nr);lineage.append({'sheet':s['name'],'row':nr,'source_row':ri,'source_sheet':s['name'],'new':False,'values_preserved':True})
  else:
   target=excluded if rec else unreviewed;name='訪問しない_履歴' if rec else '未精査_元一覧';nr=len(target)+2;target.append(v+[s['name'],'本人判断・色なし' if rec else '写真未受領・未精査']);transfer(s['name'],ri,name,nr)
 sheets.append(new)
newcompanies=[];newitems=[]
for rec in records.values():
 if not(rec['new_company'] and rec['include_in_final_visit_list']):continue
 receipt=rec['receipts'][0];target=sheets[0] if receipt['batch_file']=='photo_002.json' else sheets[1];newcompanies.append(rec['company'])
 for i,ident in enumerate(receipt['source_candidate_ids']):
  x=byid[ident];v=[rec['company'],receipt['booth'],None,None,receipt['item_refs'][i], '／'.join(x.get('tag_names',[])),None,None,None];r=len(target['values'])+2;target['values'].append(v);target['row_colors'].append(rec['resolved_color'])
  u=x.get('company_url') or ('https://www.jimtof.org/map/jp/e1-3_booth/e1-3.html?no=E1053' if ident=='GR-C01' else None);main=x.get('main_url') or next((t['url'] for t in x.get('sources',[]) if t.get('url')),None)
  if u:links.append(dict(sheet=target['name'],cell=f'A{r}',url=u,tip='JIMTOF公式出展者ページ'))
  if main:links.append(dict(sheet=target['name'],cell=f'E{r}',url=main,tip='注目アイテムの既存調査根拠。展示・開発段階は本文の注記を参照。'))
  extra=next((t for t in x.get('sources',[]) if t.get('url') and t['url'] not in [u,main]),None)
  if extra:v[8]=extra.get('title') or '関連技術資料';links.append(dict(sheet=target['name'],cell=f'I{r}',url=extra['url'],tip=extra.get('locator','')))
  newitems.append({'company':rec['company'],'candidate_id':ident,'sheet':target['name'],'row':r,'item':v[4],'color':rec['resolved_color'],'user_focus_pending':True});lineage.append(dict(newitems[-1],new=True))
# New items are staged for later user comments. Existing item text, priorities and comments are unchanged.
for s in sheets:
 other={key(v[0]) for x in sheets if x is not s for v in x['values']}
 for row in s['values']:
  if row[2] is None:row[2]='他シートと重複あり' if key(row[0]) in other else '重複なし'
for s in list(sheets):
 name='閲覧_AI・フィジカルAI' if s['name'].startswith('AI') else '閲覧_自動化・自律化';view=dict(name=name,headers=headers,values=[],kind='view',merges=[],row_colors=[])
 groups=collections.OrderedDict()
 for ri,v in enumerate(s['values'],2):groups.setdefault((key(v[0]),v[1]),[]).append((ri,v))
 for group in groups.values():
  start=len(view['values'])+2
  for oldrow,v in group:
   nr=len(view['values'])+2;view['values'].append(copy.deepcopy(v));view['row_colors'].append(s['row_colors'][oldrow-2])
   for l in list(links):
    if l['sheet']==s['name'] and int(re.search(r'\d+',l['cell'])[0])==oldrow and not(l['cell'].startswith('A') and nr!=start):links.append(dict(l,sheet=name,cell=re.sub(r'\d+',str(nr),l['cell'])))
  end=len(view['values'])+1
  if end>start:
   view['merges'] += [f'A{start}:A{end}',f'B{start}:B{end}']
   for row in view['values'][start-1:end-1]:row[0]=row[1]=None
 sheets.append(view)
# Photograph 2's uncolored new firm belongs to the non-visit history, never the visit list.
for rec in records.values():
 if rec['new_company'] and not rec['include_in_final_visit_list']:
  rc=rec['receipts'][0];x=byid[rc['source_candidate_ids'][0]];nr=len(excluded)+2;excluded.append([rec['company'],rc['booth'],'重複なし',None,rc['item_refs'][0],'／'.join(x.get('tag_names',[])),None,None,None,'未掲載候補','本人判断・色なし'])
  if x.get('main_url'):links.append(dict(sheet='訪問しない_履歴',cell=f'E{nr}',url=x['main_url'],tip='参照用。訪問予定には含めない。'))
sheets += [dict(name='訪問しない_履歴',headers=headers+['元シート','管理判断'],values=excluded,kind='archive',merges=[],row_colors=[]),dict(name='未精査_元一覧',headers=headers+['元シート','管理判断'],values=unreviewed,kind='archive',merges=[],row_colors=[])]
plan=dict(fileName='JIMTOF2026_訪問先一覧_更新版_優先色と巡回順.xlsx',sheets=sheets,links=links,source_workbook=str(original.relative_to(R)),source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),new_companies=newcompanies,new_items=newitems,lineage=lineage,counts={'visit_companies':34,'new_companies':9,'excluded_companies':15,'unreviewed_original_companies':len({key(v[0]) for v in unreviewed})},color_hex={'黄色':'#FFFF00','緑':'#D9EAD3','青系':'#CFE2F3'})
(D/'update_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'counts':plan['counts'],'sheets':[(s['name'],len(s['values'])) for s in sheets],'new_items':len(newitems)},ensure_ascii=False))
