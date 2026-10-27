import json, pathlib, zipfile, xml.etree.ElementTree as ET, re, hashlib
D=pathlib.Path(__file__).resolve().parent
O=D.parents[2]/'outputs'/D.name
data=json.loads((D/'hearing_records.json').read_text(encoding='utf8'))
records=data['records']; ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
with zipfile.ZipFile(O/'JIMTOF2026_当日ヒアリング原文.xlsx') as z:
    strings=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        strings=[''.join(t.text or '' for t in si.findall('.//s:t',ns)) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
    def sheet(number):
        xml=ET.fromstring(z.read(f'xl/worksheets/sheet{number}.xml'))
        cells={}
        for c in xml.findall('.//s:sheetData/s:row/s:c',ns):
            value=c.find('s:v',ns); t=c.get('t'); value=value.text if value is not None else ''
            if t=='s': value=strings[int(value)]
            elif t=='inlineStr': value=''.join(x.text or '' for x in c.findall('.//s:t',ns))
            cells[c.attrib['r']]=value or ''
        return xml,cells
    ix,ic=sheet(1); nx,nc=sheet(2)
    check([ic[f'A{i}'] for i in range(7,14)]==[r['id'] for r in records[:7]],'訪問実績はメモあり7社のみ')
    check(len({ic[f'C{i}'] for i in range(7,14)})==7,'7社のブース重複なし')
    check('U001' not in [ic[f'A{i}'] for i in range(7,14)],'未確定メモを訪問社数から除外')
    lines={r['id']:[] for r in records}
    for row in nx.findall('s:sheetData/s:row',ns):
        i=int(row.attrib['r'])
        rid=nc.get(f'A{i}')
        if rid in lines: lines[rid].append((int(nc[f'E{i}']),nc.get(f'F{i}','')))
    md=(O/'JIMTOF2026_当日ヒアリング原文.md').read_text(encoding='utf8')
    blocks=re.findall(r'```text\n(.*?)\n```',md,re.S)
    check(len(blocks)==8,'Markdownに7社と未確定1件の原文を収録')
    for i,r in enumerate(records):
        rows=sorted(lines[r['id']])
        check([p for p,t in rows]==list(range(1,len(rows)+1)),r['id']+' 原文行番号の欠落・重複なし')
        restored='\n'.join(t for p,t in rows)
        check(restored==r['raw']==blocks[i],r['id']+' Excel・Markdown・原文データの文字単位一致')
        check(hashlib.sha256(restored.encode()).hexdigest()==r['sha256'],r['id']+' 原文ハッシュ一致')
    for xml in (ix,nx):
        check(xml.find('.//s:pane',ns) is not None,'見出し固定の保存確認')
        check(not xml.findall('.//s:c[@t="e"]',ns),'Excelエラーセルなし')
    tabs=[ET.fromstring(z.read(n)) for n in z.namelist() if re.match(r'xl/tables/table\d+\.xml$',n)]
    check(len(tabs)==2 and all(t.find('s:autoFilter',ns) is not None for t in tabs),'両シートにフィルターを保存')
    check('事前台帳補完' in ic['H9'],'シチズンのブース補完を原文と区別')
result={'checks':checks,'count':len(checks),'visitedCompanies':7,'unassignedMemos':1,'originalTextUnchangedAcrossFormats':True,'visualReview':['訪問実績','メモ原文','DMGの長文箇所'],'nativeExcelApplicationTest':False,'sourceConversationExtraction':'当日メモ本文のみを転記。企業見出し・事前展示情報・質問・空欄は当日メモ本文に混在させていない。'}
(D/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'checks':len(checks),'visited':7,'unassigned':1},ensure_ascii=False))
