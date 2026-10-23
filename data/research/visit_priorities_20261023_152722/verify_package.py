from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E,hashlib
from collections import Counter
D=Path(__file__).parent;R=D.parents[2];O=R/'outputs'/D.name
d=json.loads((D/'research.json').read_text(encoding='utf8'))
base=json.loads((R/d['base_file']).read_text(encoding='utf8'))
items=d['items']; bm={x['id']:x for x in base['items']}
assert len(items)==390 and set(bm)=={x['id'] for x in items}
assert all(x['tags']==bm[x['id']]['tags'] for x in items)
assert Counter(x['visit_analysis']['tier'] for x in items)==dict(A=19,B=54,C=133,D=184)
assert all(x['source_ids'] and x['source_urls'] and len(x['visit_analysis']['questions'])>=2 for x in items)
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
f=O/'JIMTOF2026_関心テーマ別_訪問計画.xlsx'
with zipfile.ZipFile(f) as z:
    shared=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        shared=[''.join(t.text or '' for t in si.iterfind('.//m:t',ns)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
    def cells(sheet):
        root=E.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')); result={}
        for c in root.findall('.//m:sheetData/m:row/m:c',ns):
            v=c.find('m:v',ns);typ=c.get('t')
            val=shared[int(v.text)] if typ=='s' and v is not None else ''.join(t.text or '' for t in c.findall('.//m:t',ns)) if typ=='inlineStr' else v.text if v is not None else ''
            result[c.get('r')]=(val,typ,c.find('m:f',ns))
        return root,result
    root,main=cells(1)
    tags=['AI','フィジカルAI','自律化','自動化']
    for r,x in enumerate(items,7):
        assert main[f'X{r}'][0]==x['id'] and main[f'D{r}'][0]==x['company']
        for c,t in zip('HIJK',tags):assert main[f'{c}{r}'][0]==x['tags'][t]['status']
        assert main[f'C{r}'][0]=='未選定' and main[f'S{r}'][0]=='未確認'
        assert all(main.get(f'{c}{r}',('',None,None))[0]=='' for c in 'TUVW')
        assert main[f'N{r}'][0]==x['visit_analysis']['priority_reason']
        assert main[f'P{r}'][0].startswith('1. ')
        assert main[f'Q{r}'][0]==x['exhibit']
    assert [float(main[c][0]) for c in ['B4','D4','F4']]==[0,390,19]
    root3,src=cells(3)
    assert src['F7'][1]!='s' and float(src['F7'][0])>40000
    link_counts={}
    error_cells=[]
    for n in range(1,5):
        rt,cs=cells(n)
        error_cells.extend((n,c) for c,(v,t,fm) in cs.items() if t=='e')
        link_counts[n]=len(rt.findall('.//m:hyperlinks/m:hyperlink',ns))
        assert rt.find('.//m:pane',ns).get('ySplit')=='6'
        assert all(float(r.get('ht','0'))<409 for r in rt.findall('.//m:row',ns))
    assert not error_cells
    assert link_counts[1]==780 and link_counts[2]==390 and link_counts[3]==680
    assert not any(n.startswith('xl/externalLinks/') for n in z.namelist())
result=dict(candidate_items=390,independent_four_tags_unchanged=True,overlapping_tag_items=d['stats']['overlapping_tag_items'],priority_counts=d['stats']['priority_counts'],curated_items=d['analysis_scope']['curated_items'],fresh_sources=15,fresh_items=20,input_cells_blank_and_defaults_restored=True,native_formula_cache=[0,390,19],source_date_typed=True,hyperlinks=link_counts,formula_errors=error_cells,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
(D/'package_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
