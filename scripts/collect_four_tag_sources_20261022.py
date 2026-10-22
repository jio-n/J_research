"""Collect public company pages linked by the saved JIMTOF exhibitor records.

Full pages stay in .build. The public log records retrieval, not semantic verification.
"""
import argparse
import concurrent.futures
import csv
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT/'.build/four_tag_20261022'
PUBLIC = ROOT/'data/research/four_tag_20261022'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.text=[]; self.skip=0; self.title=[]; self.in_title=False; self.anchor=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style','noscript','svg'): self.skip+=1
        if tag=='title': self.in_title=True
        if tag=='a' and a.get('href'): self.anchor=[a['href'],'']
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript','svg') and self.skip: self.skip-=1
        if tag=='title': self.in_title=False
        if tag=='a' and self.anchor: self.links.append(self.anchor);self.anchor=None
        if tag in ('p','div','section','li','h1','h2','h3','h4','br','tr'): self.text.append('\n')
    def handle_data(self,data):
        if not self.skip:
            self.text.append(data)
            if self.anchor: self.anchor[1]+=data
            if self.in_title:self.title.append(data)

def parse(text):
    p=Page();p.feed(text)
    p.clean='\n'.join(s.strip() for s in re.split(r'\n+', ''.join(p.text)) if s.strip())
    return p

def write_json(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def fetch(job):
    u=job['url']; key=hashlib.sha256(u.encode()).hexdigest()[:20]
    meta=PRIVATE/'pages'/f'{key}.json'; raw=PRIVATE/'pages'/f'{key}.html'
    if meta.exists(): return json.loads(meta.read_text(encoding='utf-8'))
    result={**job,'checked_date':'2026-10-22','cache_key':key,'status':'未取得'}
    try:
        req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; JIMTOFResearch/1.0)'})
        with urllib.request.urlopen(req,timeout=18) as response:
            b=response.read(3_000_000); content_type=response.headers.get('Content-Type','')
            result.update(http_status=response.status,final_url=response.url,content_type=content_type)
            if 'pdf' in content_type:
                result.update(status='PDF取得・本文未解析',bytes=len(b));raw.with_suffix('.pdf').write_bytes(b)
                write_json(meta,result);return result
            enc=response.headers.get_content_charset()
            if not enc:
                m=re.search(br'charset\s*=\s*["\']?([A-Za-z0-9_-]+)',b[:10000],re.I)
                enc=m[1].decode('ascii') if m else 'utf-8'
        try:t=b.decode(enc,errors='replace')
        except LookupError:t=b.decode('utf-8',errors='replace')
        raw.write_text(t,encoding='utf-8',newline='\n'); p=parse(t)
        raw.with_suffix('.txt').write_text(p.clean,encoding='utf-8',newline='\n')
        result.update(status='本文取得',title=''.join(p.title).strip(),characters=len(p.clean),sha256=hashlib.sha256(b).hexdigest())
        links=[]
        for url,label in p.links:
            absolute=urllib.parse.urljoin(result['final_url'],url)
            if absolute.startswith(('https://','http://')) and not re.search(r'facebook|twitter|youtube|linkedin|instagram|mailto:',absolute,re.I):
                links.append({'url':absolute,'label':re.sub(r'\s+',' ',label).strip()[:140]})
        result['links']=list({x['url']:x for x in links}.values())
    except Exception as e: result.update(status='取得不能',error=str(e)[:240])
    write_json(meta,result)
    return result

def seeds():
    rows=list(csv.DictReader((ROOT/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig',newline='')))
    old=json.loads((ROOT/'data/research/technology_atlas_v1/candidate_screening.json').read_text(encoding='utf-8'))
    known={r['record_id'] for r in old}
    terms=r'フィジカル|エージェント|(?<![A-Za-z])AI(?![A-Za-z])|人工知能|自律|自立|自動(?!車)|無人|ロボット|robot|automation|autonom|認識|適応制御|予知|フィードバック|スケジュー|CAM|デジタルツイン|自動補正'
    jobs={}; mappings=[]
    for r in rows:
        text=r['exhibition_content']+'\n'+r['main_exhibits']
        flag=r['exhibitor_record_id'] in known or bool(re.search(terms,text,re.I))
        links=[]; cache=ROOT/r['detail_cache_path'] if r['detail_cache_path'] else None
        if cache and cache.exists():
            t=cache.read_text(encoding='utf-8')
            contact=re.search(r'<div class="details-contact">([\s\S]*?)</ul>',t)
            if contact:
                for u in re.findall(r'<a[^>]+href="([^"]+)"',contact[1]):
                    if u.startswith(('http://','https://')):links.append(html.unescape(u))
        mappings.append({'record_id':r['exhibitor_record_id'],'company':r['company_name'],'booth':r['booth'],'screen_hit':flag,'company_urls':links})
        if flag:
            for u in links:
                j=jobs.setdefault(u,{'url':u,'kind':'出展ページに記載された企業サイト','companies':[]})
                if r['company_name'] not in j['companies']:j['companies'].append(r['company_name'])
    write_json(PUBLIC/'company_links.json',mappings)
    return list(jobs.values())

def run(jobs):
    results=[]; start=time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for i,result in enumerate(pool.map(fetch,jobs),1):
            results.append(result)
            if i%40==0:print(f'{i}/{len(jobs)} retrieved, {round(time.time()-start)} seconds',flush=True)
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['home','linked'],default='home');args=parser.parse_args()
    PRIVATE.mkdir(parents=True,exist_ok=True);(PRIVATE/'pages').mkdir(exist_ok=True)
    if args.phase=='home':jobs=seeds()
    else:
        home=json.loads((PRIVATE/'home_results.json').read_text(encoding='utf-8'))
        jobs={}
        for p in home:
            if p['status']!='本文取得':continue
            links=p.get('links',[]); host=urllib.parse.urlsplit(p['final_url']).hostname
            scored=[]
            for link in links:
                u,label=link['url'],link['label'];score=0
                if urllib.parse.urlsplit(u).hostname!=host or u==p['final_url']:continue
                if re.search(r'jimtof.?2026|JIMTOF2026',u+' '+label,re.I):score+=100
                if re.search(r'フィジカル|生成AI|エージェント|(?<![A-Za-z])AI(?![A-Za-z])|physical.?ai|artificial|machine.learning',u+' '+label,re.I):score+=60
                if re.search(r'ロボット|自動化|自律|robot|automat|product|solution|製品|ソリューション',u+' '+label,re.I):score+=15
                if re.search(r'privacy|recruit|採用|contact|問い合わせ',u+' '+label,re.I):score-=100
                if score>0:scored.append((score,u,label))
            for score,u,label in sorted(scored,reverse=True)[:2]:
                jobs.setdefault(u,{'url':u,'kind':'企業サイトの製品・出展関連リンク','companies':p['companies'],'parent_url':p['final_url'],'link_label':label})
        jobs=list(jobs.values())
    result=run(jobs);write_json(PRIVATE/f'{args.phase}_results.json',result)
    public=[{k:v for k,v in p.items() if k!='links'} for p in result]
    write_json(PUBLIC/f'{args.phase}_retrieval_log.json',public)
    print(json.dumps({'phase':args.phase,'pages':len(result),'body_success':sum(r['status']=='本文取得' for r in result)},ensure_ascii=False))
