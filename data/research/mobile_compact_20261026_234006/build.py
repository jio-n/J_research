import pathlib,json,re,unicodedata,hashlib
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name;B=R/'data/research/visit_update_20261026_225824';p=json.loads((B/'final_plan.json').read_text(encoding='utf8'));route=json.loads((B/'route_plan.json').read_text(encoding='utf8'))
def key(s):return re.sub(r'[\s.,・/&-]','',re.sub(r'\([^)]*\)','',unicodedata.normalize('NFKC',s).casefold()).replace('株式会社','').replace('有限会社',''))
rs=next(s for s in p['sheets'] if s['kind']=='route');companies=[]
for row,color in zip(rs['values'],rs['row_colors']):
 company=row[2];booth=re.search(r'[EWS]\d+',row[3])[0];items=[];seen=set()
 for sh in p['sheets']:
  if sh['kind']!='search':continue
  for ri,v in enumerate(sh['values'],2):
   if key(v[0])!=key(company) or re.search(r'[EWS]\d+',v[1])[0]!=booth:continue
   ident=tuple(v[4:9])
   if ident in seen:continue
   seen.add(ident);links={l['cell'][0]:l['url'] for l in p['links'] if l['sheet']==sh['name'] and int(re.search(r'\d+',l['cell'])[0])==ri};items.append({'name':v[4] or '注目アイテム未指定','tags':v[5] or '', 'focus':v[6] or '', 'questions':v[7] or '', 'url':links.get('E',''),'extraLabel':v[8] or '', 'extraUrl':links.get('I',''),'companyUrl':links.get('A','')})
 companies.append({'id':booth+'-'+hashlib.sha256(key(company).encode()).hexdigest()[:10],'company':company,'shortName':company.replace('株式会社','').replace('有限会社',''),'booth':row[3],'hall':row[4],'area':row[0],'priority':color,'order':row[1],'routeNote':row[7],'map':row[8],'items':items})
data={'version':'20261026-compact1','companies':companies,'areas':[{'id':a['area'][0],'name':a['area'][2:],'move':a['move'],'core':a['core'],'cut':a['cut']} for a in route['areas']]}
(D/'app_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
template=(D/'template.html').read_text(encoding='utf8');page=template.replace('__APP_DATA__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c'));(O/'index.html').write_text(page,encoding='utf8');print(json.dumps({'companies':len(companies),'items':sum(len(x['items']) for x in companies)},ensure_ascii=False))
