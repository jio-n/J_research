import json,pathlib,zipfile,xml.etree.ElementTree as E,hashlib,re,unicodedata
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name
N={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','p':'http://schemas.openxmlformats.org/package/2006/relationships'}
def col(i):
 s=''
 while i:i,k=divmod(i-1,26);s=chr(65+k)+s
 return s
checks=[];whitespace=[]
for plan in ['visit_plan.json','additional_workbook_plan.json']:
 p=json.loads((D/'_private'/(plan+'.final.json')).read_text(encoding='utf-8'));summary=[]
 with zipfile.ZipFile(O/p['fileName']) as z:
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   for si in E.fromstring(z.read('xl/sharedStrings.xml')):
    for ph in si.findall('.//s:rPh',N):si.remove(ph)
    strings.append(''.join(si.itertext()))
  for i,s in enumerate(p['sheets'],1):
   root=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));cells={}
   for c in root.findall('.//s:sheetData/s:row/s:c',N):
    v=c.find('s:v',N);t=c.get('t');value=v.text if v is not None else ''
    if t=='s':value=strings[int(value)]
    elif t=='inlineStr':value=''.join(c.find('s:is',N).itertext())
    assert t!='e',(s['name'],c.get('r'),value)
    cells[c.get('r')]=value or ''
   for ri,row in enumerate([s['headers']]+s['values'],1):
    for ci,val in enumerate(row,1):
     actual=cells.get(col(ci)+str(ri),'');expected=str(val) if val is not None else ''
     if actual!=expected and actual.rstrip()==expected.rstrip():whitespace.append({'sheet':s['name'],'cell':col(ci)+str(ri),'change':'Excel保存時の末尾空白正規化'})
     else:assert actual==expected,(s['name'],col(ci)+str(ri),actual[:80],expected[:80])
   merges=[m.get('ref') for m in root.findall('s:mergeCells/s:mergeCell',N)]
   assert set(merges)==set(s.get('merges',[]))
   pane=root.find('s:sheetViews/s:sheetView/s:pane',N)
   assert pane is not None and float(pane.get('ySplit','0'))==1
   assert float(pane.get('xSplit','0'))==(1 if s['kind']=='notes' else 2)
   links=root.findall('s:hyperlinks/s:hyperlink',N);expectedlinks={x['cell']:x['url'] for x in p['links'] if x['sheet']==s['name']}
   relpart=f'xl/worksheets/_rels/sheet{i}.xml.rels';rels={}
   if relpart in z.namelist():rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read(relpart))}
   actual={h.get('ref'):rels[h.get('{'+N['r']+'}id')]+('#'+h.get('location') if h.get('location') else '') for h in links}
   assert actual==expectedlinks,(s['name'],'links')
   if s['kind'] in ['search','view']:assert not any(c.startswith(('G','H')) for c in actual)
   tables=root.findall('s:tableParts/s:tablePart',N)
   assert len(tables)==(0 if s['kind'] in ['view','notes'] else 1)
   summary.append({'sheet':s['name'],'data_rows':len(s['values']),'value_cells_checked':sum(map(len,[s['headers']]+s['values'])),'merges':len(merges),'links':len(links),'panes_verified':True,'table_filter':bool(tables)})
 checks.append({'file':p['fileName'],'sheets':summary})
stats=json.loads((D/'stats.json').read_text());source=R/'outputs/overlap_column_20261025_172348/JIMTOF2026_調査企業一覧_C列重複管理付き.xlsx'
assert hashlib.sha256(source.read_bytes()).hexdigest()==stats['original_file_sha256']
p=json.loads((D/'_private/additional_workbook_plan.json.final.json').read_text(encoding='utf-8'));main=p['sheets'][0]
def key(s):
 s=re.sub(r'\([^)]*\)','',unicodedata.normalize('NFKC',s).casefold())
 return re.sub(r'[\s.,・/&-]','',s.replace('株式会社','').replace('有限会社',''))
assert len(main['values'])==301 and len({key(r[0]) for r in main['values']})==283
assert sum(r[2]=='優先照会' for r in main['values'])==9
assert all(not any(r[16:19]) for r in main['values'])
result={'xml_value_link_merge_filter_pane_checks':checks,'source_unchanged':True,'candidate_counts_verified':True,'input_columns_initially_blank':True,'native_trailing_whitespace_normalization':whitespace}
(D/'workbook_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
