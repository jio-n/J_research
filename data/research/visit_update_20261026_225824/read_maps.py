import urllib.request,pathlib,json,pdfplumber
from urllib.parse import quote
D=pathlib.Path(__file__).resolve().parent;P=D/'_private'
urls={k:'https://www.jimtof.org/files/map/JIMTOF2026_小間割'+v+'.pdf' for k,v in [('E1-3','E1-3'),('E7-8','E7-8'),('S1-2','S1-2'),('S3-4','S3-4'),('W1-2','w1-2'),('W3-4','w3-4')]}
urls['site']='https://jimtof.org/files/site_map_jp.pdf'
for name,url in urls.items():
 f=P/(name+'.pdf');f.write_bytes(urllib.request.urlopen(quote(url,safe=':/%'),timeout=45).read())
 with pdfplumber.open(f) as doc:
  pg=doc.pages[0];pg.to_image(resolution=135).save(P/(name+'.png'));(P/(name+'.text.json')).write_text(json.dumps(pg.extract_words(),ensure_ascii=False),encoding='utf8');print(name,pg.width,pg.height,flush=True)
(D/'map_sources.json').write_text(json.dumps({'checked':'2026-10-26','index':'https://www.jimtof.org/jp/exhi_search_booth.html','pdfs':urls},ensure_ascii=False,indent=2),encoding='utf8')
