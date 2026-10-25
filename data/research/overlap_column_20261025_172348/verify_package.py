import pathlib,json,zipfile,xml.etree.ElementTree as E,hashlib,posixpath
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
p=json.loads((D/'link_plan.json').read_text(encoding='utf-8'));out=R/'outputs'/D.name/'JIMTOF2026_調査企業一覧_C列重複管理付き.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def strings(z):
 return [''.join(t.text or '' for t in x.findall('m:t',ns)+x.findall('m:r/m:t',ns)) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
def value(cell,ss):
 if cell is None:return None
 if cell.attrib.get('t')=='inlineStr':return ''.join(cell.find('m:is',ns).itertext())
 v=cell.find('m:v',ns)
 if v is None:return None
 return ss[int(v.text)] if cell.attrib.get('t')=='s' else v.text
with zipfile.ZipFile(out) as z,zipfile.ZipFile(R/p['source_workbook']) as src:
 ss=strings(z);original_ss=strings(src)
 originals={name:E.fromstring(src.read(f'xl/worksheets/sheet{i}.xml')) for i,name in enumerate(['AI・フィジカルAI','自動化・自律化50社'],1)}
 checked=0
 for i,sheet in enumerate(p['sheets'],1):
  root=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
  rows={int(r.attrib['r']):r for r in root.findall('m:sheetData/m:row',ns)}
  for row,origin in enumerate(sheet['origins'],2):
   old=originals[origin['sheet']].find(f"m:sheetData/m:row[@r='{origin['row']}']",ns)
   oldcells={c.attrib['r'][:1]:c for c in old};newcells={c.attrib['r'][:1]:c for c in rows[row]}
   for col in 'ABCDEFGH':
    newcol=chr(ord(col)+1) if col>='C' else col
    assert value(oldcells.get(col),original_ss)==value(newcells.get(newcol),ss),(sheet['name'],row,col)
    checked+=1
   assert abs(float(old.attrib.get('ht','15'))-float(rows[row].attrib.get('ht','15')))<0.1
   assert value(newcells.get('C'),ss)==sheet['values'][row-2][2]
  rels=E.fromstring(z.read(f'xl/worksheets/_rels/sheet{i}.xml.rels'));targets={x.attrib['Id']:x.attrib['Target'] for x in rels}
  links={x.attrib['ref']:targets[x.attrib['{'+ns['r']+'}id']] for x in root.findall('m:hyperlinks/m:hyperlink',ns)}
  assert links=={x['cell']:x['url'] for x in p['links'] if x['sheet']==sheet['name']}
  assert not any(x.startswith(('C','G','H')) for x in links)
  part=root.find('m:tableParts/m:tablePart',ns)
  table=E.fromstring(z.read(posixpath.normpath('xl/worksheets/'+targets[part.attrib['{'+ns['r']+'}id']])))
  assert table.attrib['ref']==f"A1:I{len(sheet['values'])+1}"
  assert [x.attrib['name'] for x in table.find('m:tableColumns',ns)]==p['headers']
  pane=root.find('m:sheetViews/m:sheetView/m:pane',ns).attrib
  assert pane.get('xSplit')=='2' and pane.get('ySplit')=='1' and pane.get('state')=='frozen'
  assert not [x for x in root.findall('.//m:c',ns) if x.attrib.get('t')=='e']
assert hashlib.sha256((R/p['source_workbook']).read_bytes()).hexdigest()==p['source_sha256']
result=dict(source_unchanged=True,shared_company_count=p['shared_company_count'],copied_AI_records=len(p['copied_records']),record_cells_compared_to_source=checked,source_row_heights_preserved=True,tables_and_headers_correct=True,hyperlinks_preserved=len(p['links']),comment_and_management_columns_without_links=True,frozen_header_and_company_booth_columns=True,no_error_cells=True)
(D/'package_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
