"""Supply native Excel hyperlink caches unsupported by the authoring renderer."""
import html,json,re,sys,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

p=Path(sys.argv[1]).resolve()
root=Path(__file__).resolve().parents[1]
assert p.parent==root/'outputs'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:files={n:z.read(n) for n in z.namelist()}
labels=[]
def patch(match):
 s=match.group(0)
 if 'HYPERLINK(' not in s:return s
 formula=ET.fromstring(s.replace('<x:c ','<x:c xmlns:x="'+ns['m']+'" ',1)).find('m:f',ns).text
 label=re.search(r',\s*"([^"]*)"\)\s*$',formula)
 assert label,formula
 label=label.group(1);labels.append(label)
 label=html.escape(label,quote=False)
 s=re.sub(r'\s+t="[^"]*"','',s,count=1)
 s=s.replace('<x:c ','<x:c t="str" ',1)
 s=re.sub(r'<x:v\b[^>]*>.*?</x:v>',f'<x:v>{label}</x:v>',s,flags=re.S)
 s=re.sub(r'<x:is\b[^>]*>.*?</x:is>','',s,flags=re.S)
 if '<x:v>' not in s:s=s.replace('</x:c>',f'<x:v>{label}</x:v></x:c>')
 return s
sheet_names=[n for n in files if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',n)]
for name in sheet_names:
 sheet=files[name].decode('utf-8')
 files[name]=re.sub(r'<x:c\b[^>]*>.*?</x:c>',patch,sheet,flags=re.S).encode('utf-8')
data=root/'data/research/technology_atlas_v1'
expected=sum(len(json.loads((data/(stem+'.json')).read_text(encoding='utf-8'))) for stem in ['category_index','category_visit_priorities'])
catalog_path=root/'data/research/report_v0/technology_directory.json'
if catalog_path.exists():
 catalog=json.loads(catalog_path.read_text('utf-8'))
 expected+=sum(len(c['topic_ids'])*(bool(c['exhibitor_urls_2026'])+bool(c['exhibitor_urls_2024'])) for c in catalog['entries'])
assert len(labels)==expected
# Retain native formulas, with recalculation in Excel after edits and sorts.
workbook=files['xl/workbook.xml'].decode('utf-8')
if '<x:calcPr' in workbook:workbook=re.sub(r'<x:calcPr\b[^>]*/>','<x:calcPr calcMode="auto" fullCalcOnLoad="1" forceFullCalc="1"/>',workbook)
else:workbook=workbook.replace('</x:workbook>','<x:calcPr calcMode="auto" fullCalcOnLoad="1" forceFullCalc="1"/></x:workbook>')
files['xl/workbook.xml']=workbook.encode('utf-8')
temp=p.with_suffix('.validated.xlsx')
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for name,contents in files.items():z.writestr(name,contents)
with zipfile.ZipFile(temp) as z:
 assert z.testzip() is None
 for name in z.namelist():
  if name.endswith('.xml'):ET.fromstring(z.read(name))
 links=[c for name in sheet_names for c in ET.fromstring(z.read(name)).findall('.//m:c',ns) if c.find('m:f',ns) is not None and 'HYPERLINK(' in c.find('m:f',ns).text]
 assert len(links)==expected
 assert [c.find('m:v',ns).text for c in links]==labels
temp.replace(p)
print(json.dumps({'native_hyperlink_formulas':len(labels),'cached_friendly_labels':'verified','xml_integrity':'passed'}))
