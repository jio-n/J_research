from pathlib import Path
import urllib.request,urllib.parse,json,re,html
from concurrent.futures import ThreadPoolExecutor
D=Path(__file__).parent;plan=json.loads((D/'link_plan.json').read_text(encoding='utf8'))
urls=sorted(set(x['url'] for x in plan['links']))
def fetch(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=20) as q:raw=q.read(2500000);status=q.status;final=q.url;ctype=q.headers.get('Content-Type','')
  text=raw.decode('utf8',errors='replace');titles=re.findall(r'<(?:title|h1)[^>]*>(.*?)</(?:title|h1)>',text,re.S|re.I)
  title=' / '.join(html.unescape(re.sub('<[^>]+>','',t)).strip() for t in titles)
  plain=html.unescape(re.sub('<[^>]+>',' ',re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',text,flags=re.S|re.I)))
  i=urls.index(url);(D/'_private'/f'url_{i:03}.txt').write_text(plain,encoding='utf8')
  return dict(url=url,status=status,final_url=final,content_type=ctype,title=title[:600],bytes_read=len(raw),text_file=f'_private/url_{i:03}.txt')
 except Exception as e:return dict(url=url,error=str(e))
result=list(ThreadPoolExecutor(12).map(fetch,urls));(D/'link_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'checked':len(result),'http_ok':sum(x.get('status')==200 for x in result),'issues':[x for x in result if x.get('status')!=200]},ensure_ascii=False))
