const dataNode=document.querySelector('#memo-data');
const memos=dataNode?JSON.parse(dataNode.textContent):[];
const byId=new Map(memos.map(m=>[m.id,m]));
const visible=()=>[...document.querySelectorAll('details.record')].filter(e=>!e.hidden);
document.querySelectorAll('[data-expand]').forEach(b=>b.onclick=()=>document.querySelectorAll('details').forEach(d=>{if(!d.hidden)d.open=true}));
document.querySelectorAll('[data-collapse]').forEach(b=>b.onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=false));
function revealHash(){if(location.hash){const t=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(t){for(let p=t;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;setTimeout(()=>t.scrollIntoView({block:'start'}),60)}}}
window.addEventListener('hashchange',revealHash);revealHash();
document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)d.querySelectorAll('img[data-src]').forEach(im=>{im.src=im.dataset.src;delete im.dataset.src})}));
let timer;
function notice(text){let e=document.querySelector('#toast');if(!e){e=document.createElement('div');e.id='toast';e.setAttribute('role','status');document.body.append(e)}e.textContent=text;e.hidden=false;clearTimeout(timer);timer=setTimeout(()=>e.hidden=true,2600)}
async function copyText(text){try{if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(text);else{const e=document.createElement('textarea');e.value=text;e.style.position='fixed';e.style.opacity='0';document.body.append(e);e.select();const ok=document.execCommand('copy');e.remove();if(!ok)throw new Error('copy failed')}notice('原文をコピーしました')}catch{notice('コピーできませんでした。TXTを開いて選択してください。')}}
document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>copyText(byId.get(b.dataset.copy).raw));
const q=document.querySelector('#query'),kind=document.querySelector('#kind');
function filter(){if(!q)return;const terms=q.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);let n=0;for(const e of document.querySelectorAll('details.record')){const m=byId.get(e.id);const hay=(m.id+' '+m.company+' '+(m.booth||'')+' '+m.raw).toLocaleLowerCase();const show=(!kind.value||m.type===kind.value)&&terms.every(t=>hay.includes(t));e.hidden=!show;if(show)n++}document.querySelector('#count').textContent=n+'／'+memos.length+'記録';document.querySelector('#empty').hidden=!!n;document.querySelector('#copy-all').disabled=!n}
if(q){q.addEventListener('input',filter);kind.addEventListener('change',filter);document.querySelector('#copy-all').onclick=()=>copyText(visible().map(e=>{const m=byId.get(e.id);return m.id+'｜'+m.company+'\n\n'+m.raw}).join('\n\n━━━━━━━━━━━━━━━━\n\n'))}
