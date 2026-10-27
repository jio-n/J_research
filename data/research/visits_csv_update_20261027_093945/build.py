import pathlib,csv,json,re,unicodedata,hashlib,copy
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name
source=pathlib.Path(r'C:\Users\paulr\.codex\codex-remote-attachments\01a16758-475a-7f73-add3-8ae91c534e09\F24CF043-92FF-47B7-8DC6-3DCAC6246AE2\1-JIMTOF2026_候補判断_20261027_003751.csv')
rows=list(csv.DictReader(source.open(encoding='utf-8-sig',newline='')));old=json.loads((R/'data/research/mobile_compact_20261026_234006/app_data.json').read_text(encoding='utf8'));data=copy.deepcopy(old);data['version']='20261027-csv-update1';companies=data['companies'];old_ids={x['id'] for x in companies}
def key(s):return re.sub(r'[\s.,・/&-]','',re.sub(r'\([^)]*\)','',unicodedata.normalize('NFKC',s).casefold()).replace('株式会社','').replace('有限会社',''))
def booth(s):return re.search(r'[EWS]\d+',s)[0]
lookup={(key(x['company']),booth(x['booth'])):x for x in companies};exhibitors=list(csv.DictReader((R/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig')));sources=json.loads((R/'data/research/visit_update_20261026_225824/map_sources.json').read_text(encoding='utf8'))['pdfs']
def priority(memo):
 m=re.search(r'黄色|緑|青色|青',memo)
 return {'黄色':'黄色','緑':'緑','青色':'青系','青':'青系'}[m[0]] if m else '未指定'
def rank(p):return {'黄色':0,'緑':1,'青系':2,'未指定':3}[p]
changes=[];new=[];ignored=[];duplicate=[]
for r in rows:
 if r['訪問判断'].strip()!='行く':ignored.append(r);continue
 code=booth(r['ブース']);k=(key(r['企業名']),code);pr=priority(r.get('採用理由・メモ',''));c=lookup.get(k);existing=bool(c)
 if not c:
  hall=int(code[1]);letter=code[0];area=('B' if hall in [7,8] else 'A') if letter=='E' else ('C' if hall in [1,2] else 'D') if letter=='S' else 'E';mp=('E7-8' if area=='B' else 'E1-3' if area=='A' else 'S1-2' if area=='C' else 'S3-4' if area=='D' else 'W3-4' if hall in [3,4] else 'W1-2');floor='4F' if letter in 'SW' and hall in [3,4] else '1F'
  c={'id':code+'-'+hashlib.sha256(key(r['企業名']).encode()).hexdigest()[:10],'company':r['企業名'],'shortName':r['企業名'].replace('株式会社','').replace('有限会社',''),'booth':r['ブース'],'hall':{'E':'東','S':'南','W':'西'}[letter]+str(hall)+'ホール／'+floor,'area':area,'priority':pr,'order':'CSV追加'+('・優先度未指定' if pr=='未指定' else ''),'routeNote':'今回のCSVで訪問予定に追加。ブース位置・実演時刻に合わせて既存の巡回順へ組み込む。','map':sources[mp],'items':[],'newCompany':True}
  # Place additions next to the closest existing booth in that hall; do not reorder old entries.
  same=[(i,x) for i,x in enumerate(companies) if booth(x['booth'])[:2]==code[:2]]
  if same:
   i,near=min(same,key=lambda ix:abs(int(booth(ix[1]['booth'])[1:])-int(code[1:])));pos=i+(int(code[1:])>=int(booth(near['booth'])[1:]))
  else:
   samearea=[i for i,x in enumerate(companies) if x['area']==area];pos=(samearea[0] if samearea else len(companies))
  companies.insert(pos,c);lookup[k]=c;new.append(c['company'])
 company_url=r.get('出展者URL','').strip()
 if not company_url:
  ex=next((x for x in exhibitors if key(x['company_name'])==key(c['company'])),None)
  if ex:company_url=ex.get('detail_url') or ex.get('booth_url') or ''
 item={'name':r['注目アイテム'],'tags':'／'.join(t for t in ['AI','フィジカルAI','自律化','自動化'] if r.get(t,'—') not in ['','—']),'focus':r.get('採用理由・メモ',''),'questions':r.get('現地で聞くこと',''),'url':r.get('技術URL',''),'extraLabel':'','extraUrl':'','companyUrl':company_url,'candidateId':r['候補ID'],'sourceExcelRow':int(r['元Excel行']),'task':r.get('対象タスク',''),'method':r.get('方式',''),'exhibit':r.get('展示確度',''),'researchReason':r.get('注目理由',''),'priority':pr,'importedFromCsv':True}
 if item['candidateId']=='FC061':item['reviewNote']='本人が見たい対象は「類似図面検索」。CSVの注目アイテムはTECHS系の実績・購買連携で、製品・展示との対応は要確認。'
 if item['candidateId']=='AC112':item['reviewNote']='本人メモは「ヒューマノイド」。台帳は人型ロボット用部品を含む加工用途で、人型ロボット自体の展示を確認した記録ではない。'
 if any(i.get('candidateId')==item['candidateId'] or i['name']==item['name'] for i in c['items']):duplicate.append(r);continue
 c['items'].append(item)
 if rank(pr)<rank(c['priority']):c['priority']=pr
 changes.append({'company':c['company'],'companyId':c['id'],'existing_company':existing,'candidateId':item['candidateId'],'item':item['name'],'priority_from_memo':pr,'company_priority':c['priority'],'user_memo':item['focus']})
assert len(companies)==45 and len(new)==11 and len(changes)==13 and len({c['id'] for c in companies})==45
for prior in old['companies']:
 current=next(c for c in companies if c['id']==prior['id'])
 assert all(i in current['items'] for i in prior['items'])
 assert current['id']==prior['id']
counts={p:sum(c['priority']==p for c in companies) for p in ['黄色','緑','青系','未指定']};data['priorityCounts']=counts;data['csvImport']={'acceptedItems':len(changes),'newCompanies':len(new),'sourceFile':source.name,'importedAt':'2026-10-27'}
(D/'app_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');(D/'intake.csv').write_bytes(source.read_bytes());(D/'import_log.json').write_text(json.dumps({'sourceFile':source.name,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'inputRows':len(rows),'acceptedItems':len(changes),'ignoredRows':ignored,'duplicates':duplicate,'newCompanies':new,'companyCount':45,'itemCount':sum(len(c['items']) for c in companies),'priorityCounts':counts,'changes':changes},ensure_ascii=False,indent=2),encoding='utf8')
t=(R/'data/research/candidate_picker_20261026_235118/visit_template.html').read_text(encoding='utf8')
def replace(a,b):
 global t
 assert a in t,a[:80];t=t.replace(a,b,1)
replace('全34社','全45社');replace('<option value="memo">','<option value="unset">優先度未指定</option><option value="memo">');replace("(filter.value!=='yg'||x.priority!=='青系')","(filter.value!=='yg'||['黄色','緑'].includes(x.priority))&&(filter.value!=='unset'||x.priority==='未指定')")
replace("list.length+' / 34社　黄11・緑14・青9'","list.length+' / '+data.companies.length+'社　黄13・緑17・青12・未指定3'");replace("{'黄色':'yellow','緑':'green','青系':'blue'}[x.priority]","{'黄色':'yellow','緑':'green','青系':'blue','未指定':'unset'}[x.priority]")
replace("itemEl.append(title);if(item.tags)","itemEl.append(title);if(item.importedFromCsv)itemEl.append(el('div','tags','CSV追加／このアイテム：'+({'黄色':'黄','緑':'緑','青系':'青','未指定':'優先度未指定'}[item.priority])));if(item.tags)")
replace("itemEl.append(block('着眼点・既存コメント',item.focus),block('当日聞くこと',item.questions));","if(item.method)itemEl.append(block('方式・担当機能',item.method));if(item.exhibit)itemEl.append(block('展示確度',item.exhibit));itemEl.append(block('着眼点・既存コメント',item.focus),block('当日聞くこと',item.questions));if(item.reviewNote)itemEl.append(block('展示との対応・要確認',item.reviewNote));")
replace("x.company,x.booth,x.priority,item.name","x.company,x.booth,item.priority||x.priority,item.name")
replace('黄色11社を先に確保','黄色13社を先に確保');replace('東1→東2を通過→東3→東8→東7→南2→南3。','東1→東2→東3→東8→東7→南2→南3→南4。')
replace('HTMLには34社の資料','HTMLには45社の資料');replace('</style>','.stop.unset{border-left-color:#a5adb3}.stop.unset>summary{background:#f5f5f5}.status{flex-wrap:wrap}.stop.unset .name:after{content:"（優先未指定）";font-size:11px;color:#687984}</style>')
(D/'visit_template.html').write_text(t,encoding='utf8');(O/'index.html').write_text(t.replace('__APP_DATA__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c')),encoding='utf8')
print(json.dumps({'companies':45,'items':sum(len(c['items']) for c in companies),'new_companies':len(new),'added_items':len(changes),'priorities':counts},ensure_ascii=False))
