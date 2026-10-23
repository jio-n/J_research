from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E,hashlib,re,unicodedata
from collections import Counter
D=Path(__file__).parent;R=D.parents[2];O=R/'outputs'/D.name
d=json.loads((D/'research.json').read_text(encoding='utf8'));base=json.loads((R/d['base_file']).read_text(encoding='utf8'))
personal=json.loads((D/'_private/personal_inputs.json').read_text(encoding='utf8'))
items=d['items'];excluded=d['excluded_items'];bm={x['id']:x for x in base['items']};allitems=items+excluded
im={x['id']:x for x in allitems};assert len(im)==405 and len(items)==387 and len(excluded)==18
assert set(bm)<=set(im) and len(set(im)-set(bm))==15
assert all(im[k]['tags']==v['tags'] for k,v in bm.items())
assert all(im[k].get(field)==value for k,v in bm.items() for field,value in v.items() if field!='suggested_rank')
assert Counter(x['visit_analysis']['tier'] for x in items)==d['stats']['priority_counts']
assert len(d['user_exclusions']['companies'])==27
norm=lambda s:re.sub(r'[^a-z0-9一-龥ぁ-んァ-ヶー]','',unicodedata.normalize('NFKC',s).lower().replace('株式会社',''))
excluded_names={norm(e['company']) for e in d['user_exclusions']['companies']}
assert not any(norm(x['company']) in excluded_names for x in items)
assert all(x['source_ids'] and len(x['visit_analysis']['questions'])>=2 for x in allitems)
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
f=O/'JIMTOF2026_関心テーマ別_訪問計画.xlsx'
with zipfile.ZipFile(f) as z:
    shared=[''.join(t.text or '' for t in si.iterfind('.//m:t',ns)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)] if 'xl/sharedStrings.xml' in z.namelist() else []
    def cells(n):
        rt=E.fromstring(z.read(f'xl/worksheets/sheet{n}.xml'));cs={}
        for c in rt.findall('.//m:sheetData/m:row/m:c',ns):
            v=c.find('m:v',ns);typ=c.get('t');val=shared[int(v.text)] if typ=='s' and v is not None else ''.join(t.text or '' for t in c.findall('.//m:t',ns)) if typ=='inlineStr' else v.text if v is not None else ''
            cs[c.get('r')]=(val,typ,c.find('m:f',ns))
        return rt,cs
    root,main=cells(1)
    for r,x in enumerate(items,7):
        assert main[f'X{r}'][0]==x['id'] and main[f'D{r}'][0]==x['company']
        for c,t in zip('HIJK',['AI','フィジカルAI','自律化','自動化']):assert main[f'{c}{r}'][0]==x['tags'][t]['status']
        p=personal.get(x['id'],{})
        for c in ['C','S','T','U','V','W']:
            expected=p.get(c,'') or {'C':'未選定','S':'未確認'}.get(c,'')
            assert main.get(f'{c}{r}',('',None,None))[0]==expected,(x['id'],c)
        assert main[f'N{r}'][0]==x['visit_analysis']['priority_reason']
        assert main[f'P{r}'][0]=='\n'.join(str(i+1)+'. '+q for i,q in enumerate(x['visit_analysis']['questions']))
        assert main[f'Q{r}'][0]==x['exhibit']
    assert [float(main[c][0]) for c in ['B4','D4','F4']]==[0,387,21]
    _,ex=cells(3)
    for r,e in enumerate(d['user_exclusions']['companies'],7):
        assert ex[f'A{r}'][0]==e['company'] and ex[f'D{r}'][0]=='訪問対象外（ユーザー判断）'
        assert ex[f'B{r}'][0]==e['booth'] and ex[f'H{r}'][0]==('／'.join(e['item_ids']) or '既存候補なし')
    _,src=cells(4);assert src['F7'][1]!='s' and float(src['F7'][0])>40000
    _,tech=cells(2);assert sum(v[0].startswith('従来からの変化：') for k,v in tech.items() if k.startswith('D'))==4
    assert sum(v[0].startswith('担当比較：') for k,v in tech.items() if k.startswith('D'))==3
    links={};errors=[]
    for n in range(1,7):
        rt,cs=cells(n);errors.extend((n,c) for c,(v,t,ff) in cs.items() if t=='e');links[n]=len(rt.findall('.//m:hyperlinks/m:hyperlink',ns))
        assert rt.find('.//m:pane',ns).get('ySplit')=='6'
        assert all(float(r.get('ht','0'))<409 for r in rt.findall('.//m:row',ns))
    assert not errors and links[1]==774 and links[2]==387
    assert not any(n.startswith('xl/externalLinks/') for n in z.namelist())
result=dict(active_items=387,new_items=15,excluded_companies=27,excluded_items=18,base_items_retained_in_research=390,base_tags_unchanged=True,user_decision_not_technical_exclusion=True,original_inputs_preserved_by_id=True,nagase_role_comparison_rows=3,nagase_history_rows=4,tag_overlap=d['stats']['overlapping_tag_items'],formula_cache=[0,387,21],error_cells=errors,hyperlinks=links,source_dates_typed=True,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
(D/'package_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False))
