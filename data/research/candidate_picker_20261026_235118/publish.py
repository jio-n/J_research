import pathlib,json,subprocess,os,urllib.request
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name;repo='jio-n/J_research';branch='codex/jimtof-mobile-site'
r=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,env=dict(os.environ,GIT_TERMINAL_PROMPT='0'),timeout=30);creds=dict(x.split('=',1) for x in r.stdout.splitlines() if '=' in x);token=creds.get('password');assert token
def api(path,method='GET',body=None):
 req=urllib.request.Request('https://api.github.com/repos/'+repo+path,method=method,data=None if body is None else json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'JIMTOF-candidate-picker'})
 with urllib.request.urlopen(req,timeout=45) as response:return json.load(response)
pages=api('/pages');assert pages['source']['branch']==branch;ref=api('/git/ref/heads/'+branch);parent=ref['object']['sha'];old=api('/git/commits/'+parent);tree=[]
for name,seed in [('index.html','memoSeed'),('candidates.html','selectionSeed')]:
 text=(O/name).read_text(encoding='utf8');assert 'id="'+seed+'">{}</script>' in text,'Only blank initial data may be published';tree.append({'path':name,'mode':'100644','type':'blob','content':text})
t=api('/git/trees','POST',{'base_tree':old['tree']['sha'],'tree':tree});commit=api('/git/commits','POST',{'message':'Add row90+ candidate selector and direct visited checkboxes','tree':t['sha'],'parents':[parent]});api('/git/refs/heads/'+branch,'PATCH',{'sha':commit['sha'],'force':False})
result={'url':pages['html_url'],'picker_url':pages['html_url']+'candidates.html','commit':commit['sha'],'published_files':['index.html','candidates.html'],'private_notes_uploaded':False};(D/'publication.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result))
