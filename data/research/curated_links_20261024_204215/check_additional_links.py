import json,pathlib,urllib.request,urllib.parse,re,html
from concurrent.futures import ThreadPoolExecutor
D=pathlib.Path(__file__).resolve().parent
p=json.loads((D/'link_plan.json').read_text(encoding='utf-8'))
def fetch(l):
 try:
  u=urllib.parse.quote(l['url'],safe=':/?=&%#')
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:
   raw=r.read(2500000);status=r.status;final=r.url
  t=raw.decode('utf-8',errors='replace');titles=re.findall(r'<(?:title|h1)[^>]*>(.*?)</(?:title|h1)>',t,re.S|re.I)
  title=' / '.join(html.unescape(re.sub('<[^>]+>','',x)).strip() for x in titles)
  (D/'_private'/f"{l['id']}_additional.html").write_bytes(raw)
  return dict(cell=l['cell'],label=l['text'],url=l['url'],status=status,final_url=final,page_title=title[:600])
 except Exception as e:return dict(cell=l['cell'],url=l['url'],error=str(e))
out=list(ThreadPoolExecutor(10).map(fetch,p['additional_sources']))
(D/'additional_link_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checked':len(out),'http_200':sum(x.get('status')==200 for x in out),'issues':[x for x in out if x.get('status')!=200]},ensure_ascii=False))
