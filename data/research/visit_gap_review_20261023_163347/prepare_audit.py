from pathlib import Path
from collections import Counter
import json,csv,re,hashlib,zipfile,xml.etree.ElementTree as E
D=Path(__file__).parent;R=D.parents[2];BASE=R/'data/research/visit_priorities_20261023_152722'
d=json.loads((BASE/'research.json').read_text(encoding='utf8'))
raw={x['exhibitor_record_id']:x for x in csv.DictReader((R/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig'))}
pat=re.compile(r'AI|人工知能|機械学習|深層|自律|自立|自動|最適化|最適制御|知能|解析|フィードバック|工程設計|監視|状態監視|異常|ロボット|スケジュ|デジタルツイン|シミュレーション|NC|CNC|数値制御|加工条件|生産管理|MES|センサ|画像認識',re.I)
machine=re.compile(r'研削盤|研磨機|加工機|工作機械|マシニング|放電|測定機|三次元|機上|精機|精密機械|計測|制御装置|制御機器|ソフトウェア|スケジューラ|システム開発|ITシステム|研削機')
queue=[]
for a in d['audit']:
    row=raw.get(a['record_id'],{}); text=row.get('exhibition_content','')+'\n'+row.get('main_exhibits','')
    if a['item_ids']:continue
    hits=list(dict.fromkeys(m.group() for m in pat.finditer(text)))
    cls='機能語・タスク語あり' if hits else '工作機械・計測・ソフト分野' if machine.search(text+' '+a['company']) else '説明なし・不足' if not text.strip() else '工具・材料・部材・一般説明'
    queue.append(dict(row_no=a['row_no'],record_id=a['record_id'],company=a['company'],booth=a['booth'],previous_status=a['status'],triage=cls,signals=hits,exhibition_content=row.get('exhibition_content',''),main_exhibits=row.get('main_exhibits',''),urls=a['company_urls'],listing_url=a['detail_url']))
(D/'unlinked_triage.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2),encoding='utf8')
with (D/'_private/triage_reading.txt').open('w',encoding='utf8') as f:
    for x in queue:
        if x['triage'] in ['機能語・タスク語あり','工作機械・計測・ソフト分野']:
            f.write(f"{x['row_no']} {x['company']} {x['booth']} [{','.join(x['signals'])}]\n出展物:{x['main_exhibits']}\n説明:{x['exhibition_content']}\n企業:{','.join(x['urls'])}\n\n")

# Preserve the latest saved personal inputs by stable ID, without opening or editing the original.
original=R/'outputs/visit_priorities_20261023_152722/JIMTOF2026_関心テーマ別_訪問計画.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(original) as z:
    shared=[''.join(t.text or '' for t in si.findall('.//m:t',ns)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)] if 'xl/sharedStrings.xml' in z.namelist() else []
    rows=E.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:sheetData/m:row',ns)
    user={}
    for row in rows:
        if int(row.get('r'))<7:continue
        vals={}
        for c in row.findall('m:c',ns):
            v=c.find('m:v',ns);t=c.get('t');text=shared[int(v.text)] if t=='s' and v is not None else ''.join(t.text or '' for t in c.findall('.//m:t',ns)) if t=='inlineStr' else v.text if v is not None else ''
            vals[re.sub(r'\d','',c.get('r'))]=text
        if vals.get('X'):user[vals['X']]={k:vals.get(k,'') for k in ['C','S','T','U','V','W']}
(D/'_private/personal_inputs.json').write_text(json.dumps(user,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(unlinked=len(queue),triage=dict(Counter(x['triage'] for x in queue)),personal_input_rows=len(user),nondefault_personal_rows=sum(x['C']!='未選定' or x['S']!='未確認' or any(x[k] for k in ['T','U','V','W']) for x in user.values())),ensure_ascii=False))

# Do not replace the edition's generators when refreshing the audit.
