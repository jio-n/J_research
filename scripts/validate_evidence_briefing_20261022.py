"""Check delivered slide text, native evidence and source traceability."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/research/evidence_briefing_20261022'
basis=json.loads((DATA/'presentation_basis.json').read_text(encoding='utf-8'))
content=json.loads((DATA/'slide_content.json').read_text(encoding='utf-8'))
quotes=json.loads((ROOT/'data/research/quotation_evidence_20261022/quotes.json').read_text(encoding='utf-8'))['quotes']
major=json.loads((ROOT/'data/research/macro_20261019/major_dossiers.json').read_text(encoding='utf-8'))
path=ROOT/basis['output']['path']
assert hashlib.sha256(path.read_bytes()).hexdigest()==basis['output']['sha256']
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
normalize=lambda s:re.sub(r'\s+','',s)
all_text=[]
actual_quotes={}
table_count=0
with ZipFile(path) as z:
    names=z.namelist()
    slide_names=[n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
    assert len(slide_names)==40
    for d in content['slides']:
        n=d['number']
        root=ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'))
        paragraphs=[''.join(t.text or '' for t in p.findall('.//a:t',ns)) for p in root.findall('.//a:p',ns)]
        text='\n'.join(paragraphs)
        all_text.append(text)
        assert normalize(d['title']) in normalize(text),(n,'title')
        assert normalize(d['caveat']) in normalize(text),(n,'caveat')
        notes=ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{n}.xml'))
        notes_text='\n'.join(t.text or '' for t in notes.findall('.//a:t',ns))
        for sid in d['refs']:
            assert sid in notes_text,(n,sid)
        if d['kind'] in {'table','definition'}:
            tables=root.findall('.//a:tbl',ns)
            assert len(tables)==1,n
            table_count+=1
            cells=tables[0].findall('.//a:tc',ns)
            expected=d['headers']+[cell for row in d['rows'] for cell in row]
            actual=[''.join(t.text or '' for t in cell.findall('.//a:t',ns)) for cell in cells]
            assert len(actual)==len(expected)
            assert [normalize(s) for s in actual]==[normalize(s) for s in expected],(n,'table text')
        for shape in root.findall('.//p:sp',ns):
            prop=shape.find('p:nvSpPr/p:cNvPr',ns)
            name=prop.get('name','') if prop is not None else ''
            if name.startswith('verbatim-'):
                qid=name.removeprefix('verbatim-')
                assert qid not in actual_quotes,qid
                actual_quotes[qid]=''.join(t.text or '' for t in shape.findall('.//a:t',ns))
    assert table_count==27
    assert len(actual_quotes)==46
    for q in quotes:assert actual_quotes[q['quote_id']]==q['excerpt_original'],q['quote_id']
    full=normalize('\n'.join(all_text))
    for c in major:assert normalize(c['target']) in full,c['target']
    for i in range(1,15):assert f'T{i:02}' in full
    chart_names=[n for n in names if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)]
    assert len(chart_names)==1
    chart=ET.fromstring(z.read(chart_names[0]))
    series=chart.findall('.//c:ser',ns)
    signals=next(d['signals'] for d in content['slides'] if d['kind']=='chart')
    assert len(series)==2
    for ser,year in zip(series,['2024','2026']):
        values=[float(t.text) for t in ser.findall('.//c:val//c:pt/c:v',ns)]
        assert values==[r['wording_'+year] for r in signals],(year,values)
    assert any(n.startswith('ppt/embeddings/') and n.endswith('.xlsx') for n in names)
assert [s['section'] for s in content['slides'][:3]]==['メイン']*3
assert all(s['section']=='補足' for s in content['slides'][3:])
result={'slides':40,'main':3,'appendix':37,'verbatim_excerpts_exact':46,'major_companies':33,'task_categories':14,'native_tables':27,'native_charts':1,'embedded_chart_workbook':True,'table_text':'all cells match authored content after whitespace normalization','sources':'reference IDs present in relevant slide notes','sha256':basis['output']['sha256']}
out=ROOT/'.build/evidence_briefing_20261022/content_validation.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
