"""Render the manually curated quotation ledger. Standard library only."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/research/quotation_evidence_20261022'
OUTPUT = ROOT / 'outputs/JIMTOF2026_原文エビデンス集_20261022.html'
ledger = json.loads((DATA / 'quotes.json').read_text(encoding='utf-8'))
taxonomy = json.loads((DATA / 'task_taxonomy.json').read_text(encoding='utf-8'))
tasks = {t['id']: t['name'] for t in taxonomy['tasks']}
quotes = ledger['quotes']

intro = '''# 光る表現を原文で確かめる：46の短い抜粋

2026年10月22日。S01～S40の全40資料を各1か所、定義・追加調査の6資料を各1か所掲載した原文集。各資料を読み直して代表的な文・句を選び、連続する原文と照合した。これは重要文を全て抽出し終えた状態ではなく、要約・解釈を原文に辿って点検するための第一版である。

**引用ブロックが原文**。それ以外の文脈・用途・注意は調査者の整理。取材発言、企業発表、記者の説明、見出しを区別し、短く切り出した文の範囲を明記する。文中の離れた箇所をつないだ合成引用はしていない。英語は英語のまま載せ、要約を原文の翻訳として扱わない。

44件は取得した原文テキストとの照合、S28・S29の2件は前回精読時のPDF画像との照合。10月21日の取得資料を再利用し、必要箇所は10月22日に追加取得・再確認した。本文キャッシュ・PDF画像全体は公開対象外。原典が変更・削除された場合は、掲載位置と確認日も参照する。

使い方：[作業定義・タスク・展示の確認方法](02_physical_ai_and_tasks.md)／[別セッションへの指示文](03_parallel_research_prompts.md)／[機械可読の原文台帳](quotes.json)。

S37は連携窓口の根拠であり、技術潮流の証拠ではない。将来計画と実現済みの能力、契約方式と収益効果も混同しない。
'''
md = [intro]
articles = []
for q in quotes:
    labels = [f"{tid} {tasks[tid]}" for tid in q['task_ids']]
    tag_text = '／'.join(labels) or '連携窓口（タスク割当なし）'
    md.append(f'''\n<a id="{q['quote_id'].lower()}"></a>
## {q['quote_id']}｜{q['source_id']}｜{q['use_for']}

> {q['excerpt_original']}

- **誰の言葉か**：{q['attribution']}
- **出典・位置**：[{q['title']}]({q['source_url']})／{q['publisher']}／公表日：{q['published_date']}／{q['locator']}
- **文脈〔要約〕**：{q['context_paraphrase']}
- **根拠として使う論点**：{q['use_for']}
- **この一節からは言えないこと**：{q['not_evidence_for']}
- **関連タスク**：{tag_text}
- **照合**：{q['verification']}／{q['verified_date']}
''')
    esc = lambda key: html.escape(q[key])
    search = ' '.join(str(q[k]) for k in ('quote_id', 'source_id', 'title', 'publisher', 'excerpt_original', 'attribution', 'context_paraphrase', 'use_for', 'not_evidence_for')) + ' ' + tag_text
    articles.append(f'''<article id="{q['quote_id'].lower()}" data-tasks="{' '.join(q['task_ids'])}" data-search="{html.escape(search.lower(), quote=True)}">
<h2><a class="qid" href="#{q['quote_id'].lower()}">{esc('quote_id')} · {esc('source_id')}</a> {esc('use_for')}</h2>
<blockquote>{esc('excerpt_original')}</blockquote>
<p class="speaker">{esc('attribution')}</p>
<p class="source"><a href="{html.escape(q['source_url'], quote=True)}" target="_blank" rel="noopener noreferrer">{esc('title')}</a><br>{esc('publisher')} · 公表日：{esc('published_date')} · {esc('locator')}</p>
<p class="tags">{html.escape(tag_text)}</p>
<details><summary>文脈と、根拠として使える範囲</summary><dl><dt>前後の文脈〔要約〕</dt><dd>{esc('context_paraphrase')}</dd><dt>この一節からは言えないこと</dt><dd>{esc('not_evidence_for')}</dd><dt>原文照合</dt><dd>{esc('verification')}／{esc('verified_date')}</dd></dl></details>
</article>''')

(DATA / '01_verbatim_evidence.md').write_text('\n'.join(md), encoding='utf-8', newline='\n')
options = ''.join(f'<option value="{tid}">{tid} {html.escape(name)}</option>' for tid, name in tasks.items())
page = '''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JIMTOF2026 原文エビデンス集</title>
<style>
:root{color-scheme:light;--ink:#193247;--muted:#506779;--line:#cbd7df;--accent:#08636f}*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:17px/1.85 "Yu Gothic",Meiryo,sans-serif}main{max-width:1080px;margin:auto;padding:40px 32px 80px}h1{font-size:32px;line-height:1.5;margin:12px 0 18px}h2{font-size:19px;line-height:1.6;margin:0 0 18px}a{color:var(--accent);text-underline-offset:3px}p{margin:12px 0}.eyebrow{font-size:14px;letter-spacing:.1em}.lead{font-size:19px}.note,.source,.tags{font-size:14px;color:var(--muted)}nav{margin:24px 0}nav a{display:inline-block;margin-right:18px}.filters{border-top:2px solid var(--ink);border-bottom:1px solid var(--line);padding:18px 0;margin:28px 0 0;display:flex;align-items:end;gap:16px;flex-wrap:wrap}.filters label{display:grid;gap:5px;font-size:14px}.filters input,.filters select,.filters button{font:inherit;padding:9px;border:1px solid #8ba1af;border-radius:3px;background:white;color:var(--ink);max-width:100%}.filters input{width:330px}.filters button{cursor:pointer}#count{font-size:14px}article{padding:32px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}blockquote{font-size:23px;line-height:1.8;font-weight:600;border-left:4px solid var(--accent);padding:0 0 0 20px;margin:18px 0;overflow-wrap:anywhere}.speaker{font-size:16px}.qid{font-size:14px;font-weight:400;margin-right:12px}.tags{margin-top:18px}details{font-size:15px;margin-top:16px}summary{cursor:pointer;color:var(--accent)}dl{margin:16px 0 0}dt{font-weight:bold}dd{margin:4px 0 14px}article[hidden]{display:none}footer{font-size:14px;margin-top:28px;color:var(--muted)}@media(max-width:600px){main{padding:24px 18px 60px}h1{font-size:26px}blockquote{font-size:20px}.filters label{width:100%}.filters input,.filters select{width:100%}}@media print{.filters{display:none}details{display:block}article{break-inside:avoid}main{padding:0}blockquote{font-size:17px}body{font-size:12px}h1{font-size:24px}}
</style><main><header><p class="eyebrow">JIMTOF2026 · 原文から確かめる · 2026.10.22</p><h1>光る表現を、原文で確かめる。</h1>
<p class="lead">元の40資料すべてと追加6資料から、短い原文を46か所。<br>誰が、どこで述べたか。何の根拠に使えるか。</p>
<details><summary>原文の扱い・照合方法</summary><p>太字の引用部分が原文です。文脈・用途・留意点は調査者の整理として分けました。代表的な文・句の第一版であり、全重要文の抽出を完了したものではありません。</p>
<p class="note">44件を原文テキストで、2件をPDF画像で照合。10月21日の取得資料を再利用し、必要箇所を10月22日に追加確認しました。S37は連携窓口の情報です。技術性能・潮流の根拠とは区別します。</p></details>
<nav><a href="../data/research/quotation_evidence_20261022/02_physical_ai_and_tasks.md">作業定義・タスク・展示の確認方法</a><a href="../RESEARCH_START.md">別セッションへの入口</a><a href="../data/research/quotation_evidence_20261022/quotes.json">原文台帳JSON</a></nav></header>
<form class="filters" onsubmit="return false"><label>原文・企業・論点を検索<input id="search" type="search" placeholder="例：判断、データ、ファナック"></label><label>顧客タスクで絞る<select id="task"><option value="">すべてのタスク</option>__OPTIONS__</select></label><button type="button" id="reset">解除</button><span id="count" role="status" aria-live="polite"></span></form>
<div id="entries">__ARTICLES__</div><p id="empty" hidden>条件に合う抜粋はありません。</p><footer>発表・研究・商品・展示予定と現地確認を区別しています。長い前後関係は各原典へ。HTML単体で検索できます。補足資料への相対リンクはリポジトリのフォルダ構成を保持した場合に使えます。</footer></main>
<script>
const entries=Array.from(document.querySelectorAll('article'));
const query=document.querySelector('#search'),task=document.querySelector('#task');
function filter(){const terms=query.value.trim().toLowerCase().split(/\\s+/).filter(Boolean);let count=0;for(const entry of entries){const ok=terms.every(t=>entry.dataset.search.includes(t))&&(!task.value||entry.dataset.tasks.split(' ').includes(task.value));entry.hidden=!ok;if(ok)count++}document.querySelector('#count').textContent=count+' / '+entries.length+' 件';document.querySelector('#empty').hidden=count>0}
query.addEventListener('input',filter);task.addEventListener('change',filter);document.querySelector('#reset').addEventListener('click',()=>{query.value='';task.value='';filter()});filter();
</script></html>'''
OUTPUT.write_text(page.replace('__OPTIONS__', options).replace('__ARTICLES__', '\n'.join(articles)), encoding='utf-8', newline='\n')
print(f'Rendered {len(quotes)} excerpts to Markdown and HTML')
