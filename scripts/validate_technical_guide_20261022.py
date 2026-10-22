"""Audit cross-format completeness and traceability, without modifying artifacts."""
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT/'data/research/technical_guide_20261022'
g = json.loads((folder/'content.json').read_text(encoding='utf-8'))
basis = json.loads((folder/'presentation_basis.json').read_text(encoding='utf-8'))
original = json.loads((ROOT/'data/research/report_v0/technology_directory.json').read_text(encoding='utf-8'))
quotes = {q['quote_id']: q for q in json.loads((ROOT/'data/research/quotation_evidence_20261022/quotes.json').read_text(encoding='utf-8'))['quotes']}
majors = json.loads((ROOT/'data/research/macro_20261019/major_dossiers.json').read_text(encoding='utf-8'))
assert len(g['categories']) == 11
assert [m['company'] for m in g['majors']] == [m['target'] for m in majors]
assert len(g['majors']) == 33
rows = [r for c in g['categories'] for r in c['rows']]
assert len(rows) == 33
assert len({r['card_id'] for r in rows}) == 33
for r in rows:
    assert all(r[k] for k in ['company','product','booth','task','method','description','status','check','sources'])
    assert all(urlsplit(s['url']).scheme == 'https' for s in r['sources'])

class InspectHTML(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.scripts=[]; self.current=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a': self.links.append(a.get('href',''))
        if tag == 'script': self.current={'attrs':a,'text':''}
    def handle_data(self, data):
        if self.current is not None: self.current['text']+=data
    def handle_endtag(self, tag):
        if tag=='script' and self.current is not None:
            self.scripts.append(self.current); self.current=None

html_path=ROOT/'outputs/technical_guide_20261022/JIMTOF2026_技術動向と視察ガイド_20261022.html'
html=html_path.read_text(encoding='utf-8')
parser=InspectHTML(); parser.feed(html)
assert len(parser.ids)==len(set(parser.ids))
atlas=json.loads(next(s['text'] for s in parser.scripts if s['attrs'].get('id')=='atlas-data'))
assert len(atlas)==344 and {a['card_id'] for a in atlas}=={a['card_id'] for a in original['entries']}
for link in parser.links:
    if link.startswith('#'): assert link[1:] in parser.ids
    elif not urlsplit(link).scheme:
        assert (html_path.parent/unquote(link.split('#')[0])).resolve().is_file(), link
for qids in [a[1] for a in g['evidence_groups']]:
    for qid in qids: assert quotes[qid]['excerpt_original'] in html

pptx=ROOT/basis['output']['path']
assert hashlib.sha256(pptx.read_bytes()).hexdigest()==basis['output']['sha256']
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(pptx) as z:
    assert z.testzip() is None
    slides=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda n:int(re.search(r'(\d+)\.xml',n)[1]))
    assert len(slides)==22
    table_count=0
    for i,name in enumerate(slides,1):
        xml=ET.fromstring(z.read(name))
        texts='\n'.join(t.text or '' for t in xml.findall('.//a:t',ns))
        assert texts and f'{i:02d} / 22' in texts
        table_count+=len(xml.findall('.//a:tbl',ns))
        note=z.read(f'ppt/notesSlides/notesSlide{i}.xml').decode('utf-8')
        assert '事前調査' in note
        if 4<=i<=14:
            for r in g['categories'][i-4]['rows']:
                assert r['product'] in texts and r['booth'] in texts
                for s in r['sources']: assert s['url'].replace('&','&amp;') in note
    assert table_count==20
print(json.dumps({'slides':22,'native_tables':20,'categories':11,'comparison_rows':33,'major_companies':33,'atlas_entries':344,'source_traceability':'passed','html_local_links':'passed','sha256':basis['output']['sha256']},ensure_ascii=False))
