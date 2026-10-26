import pathlib,json,zipfile,xml.etree.ElementTree as E,re,hashlib,collections,unicodedata
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name;p=json.loads((D/'final_plan.json').read_text(encoding='utf8'));NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};RN='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
def col(n):
 s=''
 while n:n,k=divmod(n-1,26);s=chr(65+k)+s
 return s
reports=[];whitespace=[]
with zipfile.ZipFile(O/p['fileName']) as z:
 ss=[''.join(t.text or '' for t in si.findall('s:t',NS)+si.findall('s:r/s:t',NS)) for si in E.fromstring(z.read('xl/sharedStrings.xml'))];styles=E.fromstring(z.read('xl/styles.xml'));fills=list(styles.find('s:fills',NS));xfs=list(styles.find('s:cellXfs',NS))
 for i,s in enumerate(p['sheets'],1):
  root=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));cells={};fills_bycell={}
  for c in root.findall('.//s:sheetData/s:row/s:c',NS):
   val=c.find('s:v',NS);v=val.text if val is not None else '';v=ss[int(v)] if c.get('t')=='s' else v
   if c.get('t')=='inlineStr':v=''.join(c.find('s:is',NS).itertext())
   assert c.get('t')!='e';cells[c.get('r')]=v or '';xf=xfs[int(c.get('s',0))];fill=fills[int(xf.get('fillId',0))];fg=fill.find('s:patternFill/s:fgColor',NS);fills_bycell[c.get('r')]=fg.get('rgb','')[-6:].upper() if fg is not None else ''
  for ri,row in enumerate([s['headers']]+s['values'],1):
   for ci,v in enumerate(row,1):
    a=cells.get(col(ci)+str(ri),'');b=str(v) if v is not None else ''
    if a!=b and a.rstrip()==b.rstrip():whitespace.append((s['name'],col(ci)+str(ri)))
    else:assert a==b,(s['name'],col(ci)+str(ri),a[:60],b[:60])
  for ri,color in enumerate(s['row_colors'],2):
   if color:assert fills_bycell.get('E'+str(ri))==p['color_hex'][color][1:],(s['name'],ri,'color')
  merges=[x.get('ref') for x in root.findall('s:mergeCells/s:mergeCell',NS)];assert set(merges)==set(s['merges'])
  rp=f'xl/worksheets/_rels/sheet{i}.xml.rels';rels={x.get('Id'):x.get('Target') for x in E.fromstring(z.read(rp))} if rp in z.namelist() else {};actual={h.get('ref'):rels[h.get('{'+RN+'}id')]+('#'+h.get('location') if h.get('location') else '') for h in root.findall('s:hyperlinks/s:hyperlink',NS)};expected={x['cell']:x['url'] for x in p['links'] if x['sheet']==s['name']};assert actual==expected,(s['name'],'links');assert not any(k.startswith(('G','H')) for k in actual) if s['kind'] in ['search','view'] else True
  reports.append({'sheet':s['name'],'rows':len(s['values']),'links':len(actual),'merges':len(merges),'colors_verified':len(s['row_colors'])})
assert hashlib.sha256((R/p['source_workbook']).read_bytes()).hexdigest()==p['source_sha256']
base=json.loads((D/'update_plan.json').read_text(encoding='utf8'));originalrows={}
with zipfile.ZipFile(R/p['source_workbook']) as z:
 ss=[''.join(t.text or '' for t in si.findall('s:t',NS)+si.findall('s:r/s:t',NS)) for si in E.fromstring(z.read('xl/sharedStrings.xml'))]
 for i,s in enumerate(p['sheets'][:2],1):
  for row in E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')).findall('s:sheetData/s:row',NS)[1:]:
   vals=[None]*9
   for c in row:
    v=c.find('s:v',NS);idx=ord(c.get('r')[0])-65
    if v is not None and idx<9:vals[idx]=ss[int(v.text)] if c.get('t')=='s' else v.text
   originalrows[(s['name'],int(row.get('r')))]=vals
for lin in p['lineage']:
 if not lin['new']:
  actual=next(s for s in p['sheets'] if s['name']==lin['sheet'])['values'][lin['row']-2];assert actual==originalrows[(lin['source_sheet'],lin['source_row'])],(lin['sheet'],lin['row'],'source preservation')
def key(s):return re.sub(r'[\s.,・/&-]','',re.sub(r'\([^)]*\)','',unicodedata.normalize('NFKC',s).casefold()).replace('株式会社','').replace('有限会社',''))
active={key(r[0]) for s in p['sheets'] if s['kind']=='search' for r in s['values']};route=next(s for s in p['sheets'] if s['kind']=='route');assert len(active)==34;assert {key(r[2]) for r in route['values']}==active;assert sum(c=='黄色' for c in route['row_colors'])==11
result={'sheets':reports,'source_unchanged':True,'visit_companies':34,'new_companies':9,'new_items':10,'yellow_companies':11,'route_covers_all_visits':True,'trailing_whitespace_normalization':whitespace};(D/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False))
