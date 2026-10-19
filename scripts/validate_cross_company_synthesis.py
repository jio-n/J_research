"""Bounded checks for evidence references, map coverage and research traceability."""
import hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/research/technology_atlas_v1'
read=lambda name:json.loads((DATA/(name+'.json')).read_text(encoding='utf-8'))
cards={r['card_id']:r for r in read('fact_cards')}
ev={r['evidence_id']:r for r in read('evidence_ledger')}
deep=read('priority_deepening');methods=read('method_comparison');positions=read('technology_method_positions')
years=read('year_change_patterns');issues=read('common_issues');themes=read('research_candidates')
assert [len(x) for x in [deep,methods,positions,years,issues,themes]]==[33,10,35,6,5,5]
assert {p['card_id'] for p in positions}=={r['card_id'] for r in deep}
assert len({cards[p['card_id']]['company'] for p in positions})==28
assert {m['method_id'] for m in methods}=={p['method_id'] for p in positions}
assert {cid for m in methods for cid in m['card_ids']}=={r['card_id'] for r in deep}
assert len({p['position_id'] for p in positions})==35
for dataset in [methods,positions,years,issues,themes]:
 for r in dataset:
  assert set(r['card_ids'])<=cards.keys() and set(r['evidence_ids'])<=ev.keys()
  assert set(r['evidence_ids'])<={eid for cid in r['card_ids'] for eid in cards[cid]['evidence_ids']}
  assert r['source_urls']==[ev[e]['url'] for e in r['evidence_ids']]
  assert r['source_locators']==[f"{e}: {ev[e]['locator']}" for e in r['evidence_ids']]
  assert r['analysis_date']=='2026-10-18' and r['source_checked_date']=='2026-10-16' and r['supplement_checked_date']=='2026-10-18'
for r in themes:
 issue=next(i for i in issues if i['issue_id']==r['issue_id'])
 assert set(r['card_ids'])<=set(issue['card_ids'])
 assert all(r[k] for k in ['customer_problem','technical_approach','experiment','metrics','adoption_condition','stage'])
 assert '未採否' in r['stage']
assert len([p for p in positions if p['card_id']=='AC098'])==2
assert len([p for p in positions if p['card_id']=='FC030'])==2
assert '人' in next(p for p in positions if p['card_id']=='FC031')['status']
assert '学習AIの使用未確認' in next(p for p in positions if p['card_id']=='AC146')['status']
assert '参考出品' in next(p for p in positions if p['card_id']=='FC049')['status']
assert '将来' in next(p for p in positions if p['card_id']=='FC017')['status']
assert '2024/7/25' in years[1]['baseline'] and '2025' in years[2]['current']
questions=read('open_questions');aliases=read('company_alias_confirmations')
assert len(questions)==12 and len({r['question_id'] for r in questions})==12
for r in questions:
 assert set(r['card_ids'])<=cards.keys() and set(r['evidence_ids'])<=ev.keys()
 assert r['source_urls']==[ev[e]['url'] for e in r['evidence_ids']]
 assert all(r[k] for k in ['question','requested_evidence','experiment_gate','unresolved'])
assert len(aliases)==1 and aliases[0]['effective_date']=='2025-04-01'
assert 'リモート監視' in cards['AC234']['baseline_2024'] and '同一名称の2024詳細なし' not in cards['AC234']['baseline_2024']
assert '2025' in cards['FC012']['delta_interpretation'] and '公式2025' in cards['FC012']['deepening']['human_approval']
assert sum(e.startswith('ERF-') for e in ev)==13
assert all(t['decision'] and t['experiment_gate'] and t['assessment_date']=='2026-10-18' for t in themes)
html=(ROOT/'outputs/JIMTOF2026_技術整理と全体マップ_v1.html').read_text(encoding='utf-8')
assert html.count('class="research-theme"')==5
assert all(f'id="{r["theme_id"]}"' in html for r in themes)
assert all(f'id="{r["issue_id"]}"' in html for r in issues)
for name,expected in [('JIMTOF2026_方式別比較マップ_v1',35),('JIMTOF2026_年度変化比較図_v1',0)]:
 path=ROOT/'outputs'/f'{name}.svg';svg=ET.parse(path).getroot()
 links=[e.get('href') for e in svg.iter() if e.tag.endswith('}a')]
 assert len(links)==expected
 for href in links:
  filename,cid=href.split('#');assert (path.parent/filename).exists() and cid in cards
 with Image.open(path.with_suffix('.png')) as image:
  assert image.size==(int(svg.get('width')),int(svg.get('height')))
cp=ROOT/'checkpoints/technology_atlas_v1.json';checkpoint=json.loads(cp.read_text(encoding='utf-8'))
result=dict(status='passed',**read('coverage')['cross_company_synthesis'],checks=['28社33カードを35配置に漏れなく対応','別機能・海外別実証の分離','全分析行のカードID・根拠ID・原典URL・該当箇所','研究候補→共通論点→事実カード→原典の対応','比較図SVGリンク・PNG寸法','社名変更の公式根拠と2024監視・補給の照合','研究判断5件・質問12件の根拠・開始条件','事実・分析・研究仮説と未確認の区別'],followup=read('coverage')['remaining_followup'],source_basis='基礎613出典を保持し、10/18の再確認・既存原典再読を含む公式根拠13件を追補。台帳626件。全原ページを再取得した件数ではない。',html_browser_interaction='file://自動観察はポリシー制限のため未検証',sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'outputs/JIMTOF2026_方式別比較マップ_v1.svg',ROOT/'outputs/JIMTOF2026_年度変化比較図_v1.svg',DATA/'research_candidates.csv']})
out=ROOT/'checkpoints/cross_company_synthesis_v1.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
checkpoint['cross_company_synthesis_validation']=str(out.relative_to(ROOT));cp.write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
