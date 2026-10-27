import pathlib,json,subprocess,os,urllib.request
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2];O=R/'outputs'/D.name
repo='jio-n/J_research';branch='codex/jimtof-mobile-site';target='analysis-20261027.html'
r=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,env=dict(os.environ,GIT_TERMINAL_PROMPT='0'),timeout=30)
token=dict(x.split('=',1) for x in r.stdout.splitlines() if '=' in x).get('password');assert token
def api(p,method='GET',body=None):
    req=urllib.request.Request('https://api.github.com/repos/'+repo+p,method=method,data=None if body is None else json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'JIMTOF-hearing-analysis'})
    with urllib.request.urlopen(req,timeout=45) as response:return json.load(response)
pages=api('/pages');assert pages['source']['branch']==branch
parent=api('/git/ref/heads/'+branch)['object']['sha'];old=api('/git/commits/'+parent)
tree=api('/git/trees/'+old['tree']['sha']);assert not any(x['path']==target for x in tree['tree']),'Public target already exists'
tree=api('/git/trees','POST',{'base_tree':old['tree']['sha'],'tree':[{'path':target,'mode':'100644','type':'blob','content':(O/'analysis.html').read_text(encoding='utf8')}]})
commit=api('/git/commits','POST',{'message':'Add onsite hearing and hypothesis analysis','tree':tree['sha'],'parents':[parent]})
api('/git/refs/heads/'+branch,'PATCH',{'sha':commit['sha'],'force':False})
v={'url':pages['html_url']+target,'commit':commit['sha'],'existingPagesUnchanged':True}
(D/'publication.json').write_text(json.dumps(v,indent=2),encoding='utf8');print(json.dumps(v))
