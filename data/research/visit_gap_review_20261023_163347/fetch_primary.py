from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,re,sys
D=Path(__file__).parent
class Text(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.out=[]
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,t):
        if not self.skip and t.strip():self.out.append(t.strip())
def fetch(v):
    key,url,terms=v
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=35) as r:b=r.read();charset=r.headers.get_content_charset() or 'utf-8'
        s=b.decode(charset,errors='replace');p=Text();p.feed(s);t='\n'.join(p.out)
        (D/'_private'/f'{key}.txt').write_text(t,encoding='utf8')
        windows=[]
        for term in terms:
            i=t.find(term);windows.append(dict(term=term,found=i>=0,text=t[max(0,i-100):i+2600] if i>=0 else t[-1500:]))
        return dict(key=key,url=url,characters=len(t),windows=windows)
    except Exception as e:return dict(key=key,url=url,error=str(e))
jobs=[
 ('imec','https://www.jmtba-imec.jp/',['川下','生成AI']),
 ('citizen','https://cmj.citizen.co.jp/jimtof2026/alkapply.html',['AI','出展サービス一覧']),
 ('accretech','https://www.accretech.com/jp/product/measuring/event/20261026_jimtof.html',['JIMTOF 2026','出展内容']),
 ('vericut','https://vericut.com/ja-jp/products/ai',['Vericut Intelligence','AI']),
 ('nagase','https://nagase-i.jp/product/product_33.html',['特長']),
 ('anca','https://machines.anca.com/Products/Machines/MX7-ULTRA',['LaserUltra','MTC']),
]
if len(sys.argv)>1:jobs=json.loads(Path(sys.argv[1]).read_text(encoding='utf8'))
results=list(ThreadPoolExecutor(max_workers=6).map(fetch,jobs))
(D/'_private'/('fetch_results_'+(Path(sys.argv[1]).stem if len(sys.argv)>1 else 'initial')+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([dict(key=x['key'],url=x['url'],characters=x.get('characters'),error=x.get('error')) for x in results],ensure_ascii=False,indent=2))
