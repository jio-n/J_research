import pathlib,json,subprocess,os,urllib.request,base64
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];repo='jio-n/J_research';branch='codex/jimtof-mobile-site'
r=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,env=dict(os.environ,GIT_TERMINAL_PROMPT='0'),timeout=30);token=dict(x.split('=',1) for x in r.stdout.splitlines() if '=' in x).get('password');assert token
def api(path,method='GET',body=None):
 req=urllib.request.Request('https://api.github.com/repos/'+repo+path,method=method,data=None if body is None else json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'JIMTOF-csv-visit-update'})
 with urllib.request.urlopen(req,timeout=45) as response:return json.load(response)
pages=api('/pages');assert pages['source']['branch']==branch;old=api('/contents/index.html?ref='+branch);text=(R/'outputs'/D.name/'index.html').read_bytes();assert b'id="memoSeed">{}</script>' in text
result=api('/contents/index.html','PUT',{'message':'Merge13 selected CSV items into45-company visit list','branch':branch,'sha':old['sha'],'content':base64.b64encode(text).decode()});out={'url':pages['html_url'],'commit':result['commit']['sha'],'companies':45,'items':59,'private_visit_memos_uploaded':False,'candidate_and_notes_pages_unchanged':True};(D/'publication.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out))
