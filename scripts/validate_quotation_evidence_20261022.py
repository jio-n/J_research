"""Check coverage, quote preservation, task references and local links.

This validates the published ledger, not a fresh retrieval of source pages.
Original-text/PDF-image checks were performed during curation on 2026-10-22.
"""
from pathlib import Path
from collections import Counter
import hashlib
import html
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/research/quotation_evidence_20261022'
quotes = json.loads((DATA / 'quotes.json').read_text(encoding='utf-8'))['quotes']
tasks = json.loads((DATA / 'task_taxonomy.json').read_text(encoding='utf-8'))['tasks']
task_ids = {t['id'] for t in tasks}
assert task_ids == {f'T{i:02}' for i in range(1, 15)}
assert [q['quote_id'] for q in quotes] == [f'Q{i:02}' for i in range(1, 47)]
assert {q['source_id'] for q in quotes[:40]} == {f'S{i:02}' for i in range(1, 41)}
assert len({q['source_id'] for q in quotes}) == 46
assert len({q['source_url'] for q in quotes}) == 46
md = (DATA / '01_verbatim_evidence.md').read_text(encoding='utf-8')
page_path = ROOT / 'outputs/JIMTOF2026_原文エビデンス集_20261022.html'
page = page_path.read_text(encoding='utf-8')
blocks = [html.unescape(b) for b in re.findall(r'<blockquote>(.*?)</blockquote>', page, re.S)]
assert blocks == [q['excerpt_original'] for q in quotes]
assert re.findall(r'^> (.*)$', md, re.M) == blocks
assert page.count('<article ') == 46
assert page.count('<option value="T') == 14
assert all(set(q['task_ids']) <= task_ids for q in quotes)
for q in quotes:
    for key in ['attribution', 'locator', 'context_paraphrase', 'not_evidence_for', 'verification']:
        assert q[key], (q['quote_id'], key)
    assert q['source_url'].startswith('https://')
    assert f'id="{q["quote_id"].lower()}"' in page
    if not re.search('[\u3040-\u9fff]', q['excerpt_original']):
        assert len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", q['excerpt_original'])) <= 25

checked_links = 0
documents = [ROOT/'AGENTS.md', ROOT/'RESEARCH_START.md', *DATA.glob('*.md')]
for path in documents:
    text = path.read_text(encoding='utf-8')
    assert '\ufffd' not in text
    assert not re.search(r'turn\d+(?:view|search)|TODO|TBD|lorem', text, re.I)
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if link.startswith(('https://', 'http://', '#')):
            continue
        target = path.parent / unquote(link.split('#')[0])
        assert target.exists(), (str(path), link)
        checked_links += 1
for link in re.findall(r'href="([^"]+)"', page):
    if not link.startswith(('https://', '#')):
        assert (page_path.parent / link).exists(), link
        checked_links += 1
template = json.loads((DATA/'exhibit_assessment_template.json').read_text(encoding='utf-8'))
assert not any(template['evidence_checks'].values())
counts = dict(Counter(q['verification'] for q in quotes))
result = {'date':'2026-10-22','quotes':len(quotes),'original_sources':40,'additional_quote_sources':6,'task_categories':14,'curation_verification_modes':counts,'automated_checks':['原資料ID40件の網羅','原文46抜粋のMarkdown・HTML一致','タスク参照・ID重複','ローカルリンクの存在','空の展示評価票'],'local_links_checked':checked_links,'scope':'構造と参照の検証。原典の原文照合は編集時に別途実施。ブラウザでの動作確認結果はこの検証に含まない。','sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [DATA/'quotes.json',DATA/'task_taxonomy.json',DATA/'01_verbatim_evidence.md',DATA/'02_physical_ai_and_tasks.md',page_path]}}
(DATA/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
