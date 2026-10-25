import pathlib,json,re,unicodedata,hashlib,csv,zipfile,xml.etree.ElementTree as E
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
p=json.loads((R/'data/research/curated_links_20261024_204215/link_plan.json').read_text(encoding='utf-8'))
source='outputs/curated_links_20261024_204215/JIMTOF2026_調査企業一覧_追加技術資料付き.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(R/source) as z:
    ss=[''.join(t.text or '' for t in s.findall('m:t',ns)+s.findall('m:r/m:t',ns)) for s in E.fromstring(z.read('xl/sharedStrings.xml'))]
    for i,items in enumerate([p['ai'],p['automation']],1):
        root=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
        for r,item in enumerate(items,2):
            values=[]
            for col in 'ABCDEFGH':
                cell=root.find(f"m:sheetData/m:row[@r='{r}']/m:c[@r='{col}{r}']",ns)
                v=cell.find('m:v',ns) if cell is not None else None
                if cell is not None and cell.attrib.get('t')=='inlineStr':value=''.join(cell.find('m:is',ns).itertext())
                elif v is None:value=None
                elif cell.attrib.get('t')=='s':value=ss[int(v.text)]
                else:value=v.text
                values.append(value)
            item['values']=values
def key(name):
    s=unicodedata.normalize('NFKC',name).casefold()
    s=re.sub(r'\([^)]*\)','',s)
    s=s.replace('株式会社','').replace('有限会社','')
    return re.sub(r'[\s.,・]','',s)
ai={key(x['values'][0]) for x in p['ai']};auto={key(x['values'][0]) for x in p['automation']}
shared=ai & auto
audit=[];sheets=[];copied=[]
headers=p['headers'][:2]+['他シートとの重複']+p['headers'][2:]
expanded=[]
for oldrow,item in enumerate(p['automation'],2):
    matches=[(r,x) for r,x in enumerate(p['ai'],2) if key(x['values'][0])==key(item['values'][0])]
    same=[x for x in matches if re.match(r'[A-Z]+\d+',x[1]['values'][1])[0]==re.match(r'[A-Z]+\d+',item['values'][1])[0]]
    if not same:
        expanded.append(dict(**item,origin_sheet='自動化・自律化50社',origin_row=oldrow))
    for r,x in matches:
        expanded.append(dict(**x,origin_sheet='AI・フィジカルAI',origin_row=r))
        copied.append(dict(company=x['values'][0],item=x['values'][3],from_row=r,original_candidate_booth=item['values'][1],copied_booth=x['values'][1]))
aiitems=[dict(**x,origin_sheet='AI・フィジカルAI',origin_row=r) for r,x in enumerate(p['ai'],2)]
for name,items,other in [('AI・フィジカルAI',aiitems,'自動化・自律化50社'),('自動化・自律化50社',expanded,'AI・フィジカルAI')]:
    values=[]
    origins=[]
    for i,item in enumerate(items,2):
        v=item['values'];match=key(v[0]) in shared
        label=other+'と重複あり' if match else '重複なし'
        values.append(v[:2]+[label]+v[2:])
        origins.append(dict(sheet=item['origin_sheet'],row=item['origin_row']))
        audit.append(dict(sheet=name,row=i,company=v[0],booth=v[1],canonical_key=key(v[0]),overlap=match,label=label))
    sheets.append(dict(name=name,headers=headers,values=values,origins=origins,overlap_rows=sum(x['overlap'] for x in audit if x['sheet']==name)))
links=[]
for sheet in sheets:
    for newrow,origin in enumerate(sheet['origins'],2):
        for old in p['links']:
            if old['sheet']!=origin['sheet'] or int(old['cell'][1:])!=origin['row']:continue
            l=old.copy();c=l['cell'][0]
            l['source_sheet']=old['sheet'];l['source_cell']=old['cell']
            if c>='C':c=chr(ord(c)+1)
            l['cell']=c+str(newrow);l['sheet']=sheet['name'];links.append(l)
plan=dict(source_workbook=source,source_sha256=hashlib.sha256((R/source).read_bytes()).hexdigest(),headers=headers,sheets=sheets,links=links,copied_records=copied,shared_company_count=len(shared),shared_company_keys=sorted(shared),policy='企業単位の照合。法人格・英字句読点・空白・括弧の補足表記を正規化し完全一致。同一ブースを重複根拠にしない。重複企業の記入済みAIアイテムレコードを自動化側へそのまま転記。別ブースの元候補は保持。')
(D/'link_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with (D/'overlap_audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(audit[0]));w.writeheader();w.writerows(audit)
pending=dict(status='最終統合待ち。今回のExcelではユーザー着眼点・優先度を変更しない。',comments=[dict(company='Wintech Automation Co., Ltd',item='HGM-DX 自動両面研削システム',priority='相対的に低め。他候補との比較後に決定',user_focus='加工対象は工具であり、直接ワークを加工する自律制御への関心を優先したい。厚み・刃先高さの測定に基づく補正は比較的単純な印象。より高度な加工制御を行う候補があれば、そちらを優先する。',suggested_questions='厚み・刃先高さの補正以外に、加工状態に応じて条件を変更する制御はあるか。',distinction='単純との評価はユーザーの印象。技術的に単純だと確認した事実ではない。質問はコメントに基づくAI整理案。')])
(D/'pending_user_comments.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'shared_companies':len(shared),'overlap_rows':[(x['name'],x['overlap_rows']) for x in sheets]},ensure_ascii=False))
