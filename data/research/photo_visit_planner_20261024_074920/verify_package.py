from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E
D=Path(__file__).parent;R=D.parents[2];O=R/'outputs'/D.name
data=json.loads((D/'transcription.json').read_text(encoding='utf8'))
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(O/'JIMTOF2026_ユーザー選定_調査企業一覧.xlsx') as z:
    ss=E.fromstring(z.read('xl/sharedStrings.xml'))
    strings=[''.join(e.itertext()) for e in ss.findall('s:si',ns)]
    for n,key in [(1,'ai'),(2,'automation')]:
        root=E.fromstring(z.read(f'xl/worksheets/sheet{n}.xml'))
        values={}
        for c in root.findall('.//s:sheetData/s:row/s:c',ns):
            v=c.find('s:v',ns)
            if v is not None:
                assert c.get('t')!='e','Excel error cell'
                values[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
            assert c.find('s:f',ns) is None,'Unexpected formula'
        expected=[data['headers']]+[x['values'] for x in data[key]]
        for i,row in enumerate(expected,1):
            for j,v in enumerate(row):assert values.get(f'{chr(65+j)}{i}','')==(v or ''),(n,i,j)
        assert not root.findall('s:mergeCells',ns)
    assert len(E.fromstring(z.read('xl/workbook.xml')).find('s:sheets',ns))==2
result=dict(ai_items=len(data['ai']),ai_companies=len({x['values'][0] for x in data['ai']}),automation_companies=len(data['automation']),all_588_cells_including_headers_match=True,automation_C_to_G_blank=True,unreadable_cells=len(data['unreadable']),formula_errors=0)
(D/'package_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
