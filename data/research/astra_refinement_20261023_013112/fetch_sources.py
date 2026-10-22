from pathlib import Path
import json, urllib.request, urllib.parse, hashlib, concurrent.futures, sys, io, re
from html.parser import HTMLParser
from pypdf import PdfReader
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.text=[];self.links=[];self.skip=0;self.anchor=None;self.title=[];self.intitle=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ['script','style','noscript','svg']:self.skip+=1
  if t=='title':self.intitle=True
  if t=='a' and a.get('href'):self.anchor=[a['href'],'']
 def handle_endtag(self,t):
  if t in ['script','style','noscript','svg'] and self.skip:self.skip-=1
  if t=='title':self.intitle=False
  if t=='a' and self.anchor:self.links.append(self.anchor);self.anchor=None
  if t in ['p','div','section','li','h1','h2','h3','h4','tr']:self.text.append('\n')
 def handle_data(self,s):
  if not self.skip:
   self.text.append(s)
   if self.anchor:self.anchor[1]+=s
   if self.intitle:self.title.append(s)
D=Path(__file__).parent; R=D.parents[2]; P=D/'_private'; P.mkdir(exist_ok=True)
base=json.loads((R/'data/research/four_tag_20261022/research.json').read_text(encoding='utf8'))
urls=set()
for x in base['items']:
 if x['recommendation'] in ['優先訪問','比較訪問','事前確認'] or x['tags']['AI']['status'] in ['呼称・用途記載','関連基盤'] or x['tags']['フィジカルAI']['status']!='—':
  urls.update(u for u in x['source_urls'] if 'jimtof.org/' not in u)
  if x['tags']['AI']['status']=='呼称・用途記載':urls.update(x['company_sites'])
urls.update(['https://www.cgsys.co.jp/jp/cam-tool/function_features.html','https://www.cgsys.co.jp/jp/products/event_ct.html','https://www.tm-robot.com/ja/product/ai-vision','https://www.fanuc.co.jp/ja/profile/pr/newsrelease/2026/news20260930.html','https://www.dmgmori.co.jp/corporate/news/2026/20260706_geniac.html','https://www.abejainc.com/news/20261016/2','https://www.aist.go.jp/aist_j/news/pr20260702.html','https://www.aist.go.jp/aist_j/press_release/pr2022/pr20220117/pr20220117.html','https://unit.aist.go.jp/cmt-ri/research-topics/digital-manufacturing.htm'])
if len(sys.argv)>1:urls=set(json.loads(Path(sys.argv[1]).read_text(encoding='utf8')))
def get(u):
 key=hashlib.sha256(u.encode()).hexdigest()[:20]; dest=P/(key+'.txt'); meta={'url':u,'cache':key,'checked':'2026-10-23','semantic_review':False}
 if dest.exists():return {**meta,'status':'cached','characters':len(dest.read_text(encoding='utf8'))}
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=22) as r:b=r.read();typ=r.headers.get('Content-Type','');meta['resolved_url']=r.url
  if 'pdf' in typ or u.endswith('.pdf'):
   body='\n'.join(f'PAGE {i+1}\n'+(p.extract_text() or '') for i,p in enumerate(PdfReader(io.BytesIO(b)).pages));title='PDF';links=[]
  else:
   enc=re.search(br'charset\s*=\s*["\x27]?([A-Za-z0-9_-]+)',b[:10000],re.I)
   enc=enc[1].decode() if enc else 'utf-8';p=Page();p.feed(b.decode(enc,errors='replace'));title=''.join(p.title)
   links=[{'label':s.strip(),'url':urllib.parse.urljoin(u,v)} for v,s in p.links]
   body='\n'.join(t.strip() for t in ''.join(p.text).splitlines() if t.strip())
  dest.write_text(body,encoding='utf8');meta.update(status='retrieved',title=title,characters=len(body),links=links)
 except Exception as e:meta.update(status='failed',error=str(e))
 (P/(key+'.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
 return {k:v for k,v in meta.items() if k!='links'}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:res=list(ex.map(get,sorted(urls)))
log=D/('retrieval_log.json' if len(sys.argv)==1 else 'additional_retrieval_log.json')
log.write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'attempted':len(res),'success':sum(x['status']!='failed' for x in res)}))
