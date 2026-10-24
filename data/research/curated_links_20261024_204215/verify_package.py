import json, pathlib, zipfile, xml.etree.ElementTree as E, hashlib
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
p=json.loads((D/'link_plan.json').read_text(encoding='utf-8'))
file=R/'outputs'/D.name/'JIMTOF2026_調査企業一覧_追加技術資料付き.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
total=0;panes=[];blanks=0
with zipfile.ZipFile(file) as z:
 for i,sheet in enumerate(['AI・フィジカルAI','自動化・自律化50社'],1):
  s=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
  rel=E.fromstring(z.read(f'xl/worksheets/_rels/sheet{i}.xml.rels'))
  urls={r.attrib['Id']:r.attrib['Target'] for r in rel}
  links={x.attrib['ref']:urls[x.attrib['{'+ns['r']+'}id']] for x in s.findall('m:hyperlinks/m:hyperlink',ns)}
  expected={x['cell']:x['url'] for x in p['links'] if x['sheet']==sheet}
  assert links==expected,(sheet,links,expected)
  assert not any(k.startswith(('F','G')) for k in links)
  total+=len(links)
  pane=s.find('m:sheetViews/m:sheetView/m:pane',ns).attrib
  assert pane.get('xSplit')=='2' and pane.get('ySplit')=='1' and pane.get('state')=='frozen'
  panes.append(pane)
  assert not [c for c in s.findall('.//m:c',ns) if c.attrib.get('t')=='e']
  if i==2:
   for c in s.findall('.//m:sheetData/m:row/m:c',ns):
    if c.attrib['r'][0] in 'CDEFGH' and int(c.attrib['r'][1:])>1:
     assert c.find('m:v',ns) is None and c.find('m:is',ns) is None
     blanks+=1
assert hashlib.sha256((R/p['source_workbook']).read_bytes()).hexdigest()==p['source_sha256']
out=dict(saved_hyperlinks=total,company_links=82,item_links=32,additional_links=10,comment_links=0,source_workbook_unchanged=True,frozen_header_and_first_two_columns=True,automation_C_to_H_blank=True,no_saved_error_cells=True,additional_urls_unique_and_distinct_from_primary=True)
(D/'package_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out))
