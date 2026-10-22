"""Validate the report's quotation integrity and navigation; does not refetch sources."""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/research/evidence_report_20261022'
path=ROOT/'outputs/JIMTOF2026_原文から読む技術潮流_事前調査レポート_20261022.html'
page=path.read_text(encoding='utf-8')
quotes=json.loads((ROOT/'data/research/quotation_evidence_20261022/quotes.json').read_text(encoding='utf-8'))['quotes']
figures=re.findall(r'<figure class="evidence" id="(q\d+)".*?</figure>',page,re.S)
assert len(figures)==46 and len(set(figures))==46
for q in quotes:
    block=re.search(r'<figure class="evidence" id="'+q['quote_id'].lower()+r'".*?</figure>',page,re.S).group(0)
    original=html.unescape(re.search(r'<blockquote>(.*?)</blockquote>',block,re.S).group(1))
    assert original==q['excerpt_original'],q['quote_id']
    assert html.escape(q['source_url'],quote=True) in block
    assert html.escape(q['attribution']) in block
    assert html.escape(q['locator']) in block
    assert html.escape(q['not_evidence_for']) in block
ids=re.findall(r'\bid="([^"]+)"',page)
assert len(ids)==len(set(ids)),[x for x in ids if ids.count(x)>1]
links=re.findall(r'href="#([^"]+)"',page)
assert all(link in ids for link in links),set(links)-set(ids)
assert len(re.findall(r'class="index-link"',page))==46
assert len(re.findall(r'id="theme-',page))==6
assert len(re.findall(r'id="task-t',page))==14
assert len(re.findall(r'id="a\d\d"',page))==11
major_table=re.search(r'<table class="major-table">.*?</table>',page,re.S).group(0)
assert major_table.count('<tr>')==34
assert len(re.findall(r'<blockquote>',page))==46
assert not re.search(r'__(?:CSS|JS)__|\ufffd|turn\d+(?:view|search)|TODO|TBD|lorem',page,re.I)
assert not re.search(r'<script\b[^>]*\bsrc=|<link\b[^>]*\bhref=',page,re.I)
assert b'\r\n' not in path.read_bytes()
result={'date':'2026-10-22','html':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'quote_count':46,'quote_integrity':'全46抜粋をJSON正本と比較し一致。各1回掲載。話者・出典URL・掲載位置・注意を保持。','internal_anchor_count':len(links),'internal_navigation':'リンク先IDの存在とID重複なしを確認。','themes':6,'task_categories':14,'followups':11,'major_company_rows':33,'offline_reading':'外部スクリプト・スタイル依存なし。原典リンクの閲覧は通信が必要。','scope':'構造・原文・参照関係の検証。ブラウザ確認はbrowser_validation.jsonに別記。'}
(DATA/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
