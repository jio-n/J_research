from pathlib import Path
import urllib.request,re,io,json
from pypdf import PdfReader
D=Path(__file__).parent
def get(u):return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
out=[]
for key,url,terms in [
 ('anca_pdf','https://machines.anca.com/Anca.CNC/media/Images/Brochures/MX7-ULTRA-EN-digital_4.pdf?ext=.pdf',['LaserUltra','MTC']),
 ('abtec2024','https://www.scoop-japan.com/kaigi/abtec/file/ABTEC2024_Program_final_0802.pdf',['A05','深層生成'])
]:
    try:
        b=get(url);(D/'_private'/f'{key}.pdf').write_bytes(b);rd=PdfReader(io.BytesIO(b));texts=[p.extract_text() or '' for p in rd.pages]
        (D/'_private'/f'{key}.txt').write_text('\n'.join(texts),encoding='utf8')
        windows=[dict(page=i+1,text=t) for i,t in enumerate(texts) if any(w in t for w in terms)]
        out.append(dict(key=key,url=url,pages=len(texts),relevant_pages=windows))
    except Exception as e:out.append(dict(key=key,url=url,error=str(e)))
html=get('https://www.camsups.co.jp/').decode('utf8')
links=re.findall(r'href="([^"]+)"',html)
cam=list(dict.fromkeys(u for u in links if 'jimtof' in u.lower()))
out.append(dict(key='cam_show_links',urls=cam))
(D/'_private/pdf_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
