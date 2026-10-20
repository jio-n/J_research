"""Build a review from curated hypotheses and existing evidence classifications.

No new semantic classification is inferred from keyword hits. Full exhibitor rows
are retained; only exact official detail URL matches establish year evidence.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv
import hashlib
import html
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/research/strategy_review_20261021'
OUTPUT = ROOT / 'outputs/JIMTOF2026_潮流と開発候補レビュー_20261021.html'


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def norm(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value)).casefold()


def write_json(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_csv(name, rows):
    with (BASE / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(k for row in rows for k in row)))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()})


content = read_json('data/research/strategy_review_20261021/review_content.json')
keywords = read_json('data/research/strategy_keywords_20261021/strategy_keywords.json')
classification = read_json('data/research/report_v0/matrix_classification.json')
directory = read_json('data/research/report_v0/technology_directory.json')
majors = read_json('data/research/macro_20261019/major_dossiers.json')
census = read_json('data/research/macro_20261019/census.json')
for year in ('2024', '2026'):
    assert hashlib.sha256((ROOT / f'data/exhibitors_{year}_with_details.csv').read_bytes()).hexdigest() == census[year]['sha256']
text_signals = [dict(theme=theme, matched_name_keys=census['matched_panel']['name_keys'],
                     wording_2024=counts['2024'], wording_2026=counts['2026'],
                     newly_mentioned=census['matched_panel']['transitions'][theme]['added_wording'],
                     no_longer_mentioned=census['matched_panel']['transitions'][theme]['removed_wording'],
                     note='両年度に本文がある同名パネル内の公開説明の明示件数。採用率・新機能登場・性能差ではない。')
                for theme, counts in census['matched_panel']['counts'].items()]
sources = keywords['sources'] + content['additional_sources']
source_index = {s['id']: s for s in sources}
directory_index = {r['card_id']: r for r in directory['entries']}
matrix = classification['records']
card_index = {r['card_id']: r for r in matrix}
jobs = dict(classification['jobs'])
roles = {r[0]: r[1] for r in classification['roles']}
foundations = {r[0]: r[1] for r in classification['foundations']}
depth_counts = Counter(r['depth'] for r in matrix)

# URL evidence and name association remain separate, particularly for 2024.
by_url = {year: defaultdict(set) for year in (2024, 2026)}
by_name = defaultdict(set)
for record in matrix:
    by_name[norm(record['company_key'])].add(record['card_id'])
    for year in (2024, 2026):
        for url in directory_index[record['card_id']][f'exhibitor_urls_{year}']:
            by_url[year][url].add(record['card_id'])

coverage = []
for year in (2024, 2026):
    with (ROOT / f'data/exhibitors_{year}_with_details.csv').open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            direct = sorted(by_url[year].get(row['detail_url'], set())) if row['detail_url'] else []
            related = sorted(by_name.get(norm(row['company_name']), set()))
            text = bool((row['exhibition_content'] + row['main_exhibits']).strip())
            state = '年度別の公式詳細URLと技術カードを照合' if direct else ('本文あり・技術カードとの年度別URL照合なし' if text else '本文なし・追加確認待ち')
            coverage.append(dict(year=year, exhibitor_record_id=row['exhibitor_record_id'], company_name=row['company_name'],
                                 company_name_key=norm(row['company_name']), booth=row['booth'], has_description=text,
                                 coverage_status=state, year_url_evidenced_card_ids=direct, company_related_card_ids=related,
                                 detail_url=row['detail_url'], source_url=row['source_url'], checked_date=row['checked_date'],
                                 note='同名企業の関連カードは当該年の出展・機能を証明しない。未配置は機能なしを意味しない。'))
coverage_summary = []
for year in (2024, 2026):
    rows = [r for r in coverage if r['year'] == year]
    coverage_summary.append(dict(year=year, listing_rows=len(rows), normalized_names=len({r['company_name_key'] for r in rows}),
                                 rows_with_description=sum(r['has_description'] for r in rows),
                                 rows_url_matched=sum(bool(r['year_url_evidenced_card_ids']) for r in rows),
                                 description_but_unmapped=sum(r['has_description'] and not r['year_url_evidenced_card_ids'] for r in rows),
                                 no_description_unmapped=sum(not r['has_description'] and not r['year_url_evidenced_card_ids'] for r in rows)))

links_by_card = defaultdict(lambda: {'hypotheses': [], 'interfaces': [], 'candidates': []})
for collection, key in [('hypotheses', 'hypotheses'), ('interfaces', 'interfaces'), ('candidates', 'candidates')]:
    for item in content[collection]:
        for card_id in item['cards']:
            links_by_card[card_id][key].append(item['id'])

technology = []
for record in matrix:
    original = directory_index[record['card_id']]
    technology.append({k: record[k] for k in ['card_id', 'company', 'company_key', 'item', 'booths', 'target', 'human_boundary',
                                             'depth', 'exhibition_status', 'product_stage', 'evidence_ids', 'jobs', 'roles', 'methods', 'foundations']} |
                      dict(exhibitor_urls_2024=original['exhibitor_urls_2024'], exhibitor_urls_2026=original['exhibitor_urls_2026'],
                           source_urls=original['source_urls'], classification_basis=record['classification_basis'],
                           strategy_links=links_by_card[record['card_id']],
                           strategy_link_note='戦略への関連付けは分析。製品同士の接続実績・企業間の協業を意味しない。'))

major_rows = []
for major in majors:
    records = [r for r in technology if norm(r['company_key']) == norm(major['company'])]
    official = [r for r in coverage if r['year'] == 2026 and r['company_name_key'] == norm(major['company'])]
    major_rows.append(dict(company=major['company'], name=major['target'], booths=major['booths'],
                           card_ids=[r['card_id'] for r in records], example_items=[r['item'] for r in records[:3]],
                           status='既存技術カードあり' if records else ('2026公式説明あり・技術カード未整理' if major['text_2026'].strip() else '2026本文未取得・年度別の技術配置は保留'),
                           context_note=content['major_context_notes'].get(major['company'], ''),
                           description_present=bool(major['text_2026'].strip()),
                           official_record_ids=[r['exhibitor_record_id'] for r in official], official_urls=major['urls_2026'],
                           note='主要33社の確認用リスト。企業規模のランキングや全ての大企業を網羅する定義ではない。'))

# Resolve fieldwork targets through official rows; no guessed booth assignments.
for visit in content['visits']:
    matches = [r for r in coverage if r['year'] == 2026 and r['company_name_key'] == norm(visit['company'])]
    visit['booths'] = sorted({r['booth'] for r in matches if r['booth']})
    visit['official_urls'] = sorted({r['detail_url'] for r in matches if r['detail_url']})
    visit['additional_targets'] = [dict(card_id=cid, company=card_index[cid]['company'], booths=card_index[cid]['booths'],
                                       urls=directory_index[cid]['exhibitor_urls_2026']) for cid in visit.get('also_cards', [])]
    visit['certainty'] = '既存2026公式CSVのブース。現地・最新配置は未確認。質問中の戦略発表が当該ブースの展示であるとは限らない。'

matrix_cells = []
for job in jobs:
    for role in roles:
        matching = [r for r in technology if job in r['jobs'] and role in r['roles']]
        matrix_cells.append(dict(job=job, role=role, count=len(matching), card_ids=[r['card_id'] for r in matching]))

inputs = ['data/exhibitors_2024_with_details.csv', 'data/exhibitors_2026_with_details.csv',
          'data/research/report_v0/matrix_classification.json', 'data/research/report_v0/technology_directory.json',
          'data/research/macro_20261019/major_dossiers.json', 'data/research/macro_20261019/census.json',
          'data/research/strategy_keywords_20261021/strategy_keywords.json',
          'data/research/strategy_review_20261021/review_content.json']
provenance = dict(date=content['date'], input_files=[dict(path=p, bytes=(ROOT/p).stat().st_size, sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in inputs],
                  methodology=['既存の意味分類344件をそのまま再利用。キーワード一致による新規機能判定は行わない。',
                               '全出展者CSVを年度別に一行も除外せず保持。年度別URL完全一致と企業名の関連を別項目にする。',
                               '企業名キーはNFKC・空白除去・casefoldのみ。法人格除去・曖昧照合・推測による統合はしない。',
                               '記事40資料（既存34＋追加6）。複数ページの同じ記事は一資料。独立した40実証ではない。',
                               '戦略の因果、技術の配置、候補の差別化は調査者の分析。各リンクで根拠と未検証部分を明示。'],
                  counts=dict(coverage=coverage_summary, cards=len(technology), depth=dict(depth_counts), major_companies=len(major_rows),
                              sources=len(sources), hypotheses=len(content['hypotheses']), candidates=len(content['candidates']),
                              roles_unconfirmed=sum(not r['roles'] for r in technology), jobs_unconfirmed=sum(not r['jobs'] for r in technology)))

write_json('strategy_review.json', dict(**content, sources=sources, coverage_summary=coverage_summary, text_signals=text_signals, depth_counts=dict(depth_counts),
                                       jobs=jobs, roles=roles, foundations=foundations, technology=technology,
                                       major_companies=major_rows, matrix_cells=matrix_cells))
write_json('provenance.json', provenance)
write_csv('exhibitor_coverage_all_2024_2026.csv', coverage)
write_csv('technology_role_map.csv', technology)
write_csv('major_company_coverage.csv', major_rows)
write_csv('development_candidates.csv', content['candidates'])
write_csv('fieldwork_questions.csv', content['visits'])
write_csv('process_interfaces.csv', content['interfaces'])
write_csv('macro_wording_signals.csv', text_signals)
write_csv('hypothesis_evidence_links.csv', [dict(hypothesis_id=item['id'], title=item['title'], link_number=i+1,
                                               cause=link['cause'], effect=link['effect'], status=link['status'],
                                               source_ids=link['sources'], counter=item['counter'],
                                               counter_sources=item['counter_sources'], conditions=item['conditions'],
                                               boundary=item['boundary']) for item in content['hypotheses'] for i, link in enumerate(item['chain'])])
evidence = [dict(evidence_id=s['id'], publisher=s['publisher'], title=s['title'], url=s['url'], locator=s['locator'],
                 kind=s['kind'], checked_date=s['checked_date'], reading_scope=s['reading_scope']) for s in sources]
evidence += [dict(evidence_id=e['evidence_id'], publisher=e['publisher'], title=e['title'], url=e['url'], locator=e['locator'],
                  kind=e['evidence_type'], checked_date=e['checked_date'], reading_scope=e.get('retrieval_note', '既存台帳を参照')) for e in directory['evidence']]
write_csv('evidence_index.csv', evidence)

h = lambda value: html.escape(str(value), quote=True)


def source_links(ids):
    return ' '.join(f'<a class="ref" href="#source-{h(i)}">{h(i)}</a>' for i in ids)


def card_links(ids):
    return ' '.join(f'<a class="ref" href="#tech-{h(i)}">{h(i)} {h(card_index[i]["company"])}</a>' for i in ids)


def paras(values):
    return ''.join(f'<li>{h(value)}</li>' for value in values)


def url_links(urls, label='公式説明'):
    return ' '.join(f'<a href="{h(url)}" target="_blank" rel="noopener">{label}{i+1 if len(urls)>1 else ""} ↗</a>' for i, url in enumerate(urls))


parts = ['''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JIMTOF2026 潮流と開発候補レビュー</title><style>
:root{--ink:#172b3a;--muted:#526777;--blue:#145f79;--paper:#f4f6f7;--line:#d2dde2;--amber:#fff3da}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.8 'Yu Gothic','Meiryo',sans-serif}a{color:#075e89;text-underline-offset:3px}header{background:#133b4c;color:white;padding:48px max(24px,calc((100vw - 1200px)/2))}header p{max-width:1000px}h1{font-size:clamp(27px,3vw,42px);line-height:1.5;margin:10px 0}h2{font-size:26px;margin-top:0;border-bottom:3px solid #39768b;padding-bottom:10px}h3{font-size:21px;line-height:1.6;margin:0 0 12px}h4{margin:20px 0 6px}main{max-width:1260px;padding:30px;margin:auto}nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}nav a{color:white;border:1px solid #7298a7;border-radius:8px;padding:6px 12px;text-decoration:none}section{margin:0 0 44px;scroll-margin-top:20px}article,.panel{background:white;padding:25px;border:1px solid var(--line);border-radius:12px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.metric{background:white;border-top:4px solid #29778d;padding:18px;border-radius:10px}.metric strong{display:block;font-size:30px;color:var(--blue)}.muted,small{color:var(--muted)}.notice{background:var(--amber);padding:16px 20px;border-left:4px solid #b88324;border-radius:4px}.badge,.ref{display:inline-block;font-size:13px;padding:1px 8px;border-radius:5px;margin:2px;background:#e9f2f5}.chain{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:18px 0}.link{border:1px solid var(--line);padding:14px;border-radius:8px}.arrow{display:block;font-size:22px;color:var(--blue)}dl{display:grid;grid-template-columns:140px 1fr;margin:10px 0}dt{font-weight:bold;border-top:1px solid var(--line);padding:10px 0}dd{margin:0;border-top:1px solid var(--line);padding:10px 0 10px 16px}table{border-collapse:collapse;width:100%;background:white;font-size:14px}th,td{padding:12px;vertical-align:top;text-align:left;border:1px solid var(--line);overflow-wrap:anywhere}th{background:#e8eff2}caption{text-align:left;padding:10px 0}.scroll{overflow:auto}button,input,select{font:inherit}button{cursor:pointer;background:#e6f1f5;border:1px solid #9bb8c4;color:#124d64;border-radius:6px;padding:8px}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #b7770d;outline-offset:2px}.matrix button{width:100%;min-width:105px;background:#edf4f6}.matrix small{display:block;line-height:1.6}.matrix strong{font-size:24px}.filters{display:flex;flex-wrap:wrap;gap:12px;background:#e7eff2;padding:16px;border-radius:8px}.filters label{display:flex;flex-direction:column;font-size:14px}.filters input,.filters select{max-width:100%;padding:7px;border:1px solid #8aa2ae;border-radius:4px}.filters input{width:290px}summary{cursor:pointer;font-weight:bold}details{margin:12px 0}tr[hidden]{display:none!important}.tech-table td:first-child{width:25%}.tech-table td:nth-child(2){width:23%}.tech-table td:nth-child(3){width:38%}.tech-row{scroll-margin-top:20px}.source{font-size:14px}.source p{margin:5px 0}.pill{font-size:13px;font-weight:bold;color:#835700}footer{font-size:13px;color:var(--muted);padding:24px 0}.download a{display:inline-block;margin:5px 12px 5px 0}li{margin-bottom:7px}
@media(max-width:800px){main{padding:20px 14px}.grid,.chain{grid-template-columns:1fr}header{padding:28px 20px}article,.panel{padding:18px}dl{grid-template-columns:1fr}dd{padding:0 0 14px;border-top:0}dt{padding-bottom:2px}.tech-table{min-width:900px}.matrix{min-width:690px}}
@media print{body{background:white;font-size:10pt}header{background:white;color:var(--ink);padding:0}nav,.filters,.download{display:none}main{max-width:none;padding:0}article{break-inside:avoid;border-radius:0}h2{break-after:avoid}a{color:inherit}.scroll{overflow:visible}.tech-table{font-size:8pt}.chain{display:block}.link{margin-bottom:8px}.grid{display:block}.metric{display:inline-block;margin:5px;padding:8px}.metric strong{font-size:18pt}details>*{display:block}section{margin-bottom:24px}}
</style></head><body>''']
parts.append(f'<header><div>JIMTOF2026 · AI / 自動化 / AX・DX · {h(content["date"])}</div><h1>個の高度化を、つながる生産の価値へ</h1><p>{h(content["thesis"])}</p><p>{h(content["status"])}</p><nav><a href="#hypotheses">① 潮流と根拠</a><a href="#map">② 技術の役割</a><a href="#candidates">③ 開発候補</a><a href="#visits">現地で解く問い</a><a href="#coverage">調査範囲</a><a href="#sources">出典</a></nav></header><main>')
parts.append('<section id="overview"><div class="grid">')
for number, label in [('5', '潮流仮説：因果と成立条件'), ('344', '既存技術：工程と役割へ配置'), ('6', '開発候補：代替手段と棄却条件')]:
    parts.append(f'<div class="metric"><strong>{number}</strong>{label}</div>')
parts.append('</div><div class="notice"><b>今回の仮提言</b><p>自社に加工現象・計測・顧客接点の強みがあるなら、まずD1「使えるデータを作る」とD3「顧客現場へ適応・検証する」を組み合わせて確認する。CAMとの接点が強ければD2、計測・制御ならD4を優先する。自社能力と顧客の支払意思は未確認のため、現時点では条件付きの候補である。</p></div></section>')

parts.append('<section id="hypotheses"><h2>① 潮流仮説と根拠</h2><p>キーワードを、需要 → 技術・データ → 顧客成果の因果へ組み直す。下の各矢印は同じ確からしさではない。</p>')
for item in content['hypotheses']:
    parts.append(f'<article id="{item["id"]}"><h3>{item["id"]}　{h(item["title"])}</h3><p class="notice">{h(item["judgment"])}</p><div class="chain">')
    for link in item['chain']:
        parts.append(f'<div class="link"><span class="pill">{h(link["status"])}</span><p>{h(link["cause"])}<span class="arrow">↓</span>{h(link["effect"])}</p>{source_links(link["sources"])}</div>')
    parts.append(f'</div><dl><dt>反例・留保</dt><dd>{h(item["counter"])} {source_links(item["counter_sources"])}</dd><dt>成立条件</dt><dd>{h(item["conditions"])}</dd><dt>言い切れない範囲</dt><dd>{h(item["boundary"])}</dd><dt>開発への意味</dt><dd>{h(item["implication"])}</dd></dl><p>関連技術：{card_links(item["cards"])}</p><small>前段のキーワード：{h(" / ".join(item["keywords"]))}。戦略と技術の対応は本調査の分析。</small></article>')
parts.append('</section><section id="map"><h2>② 技術の位置づけ：工程 × 役割</h2><p>集める → 見極める → 案を作る → 実行する、を工程ごとに見る。学習・検証・安全などの横断基盤は別枠で絞り込める。実行には人の操作を含むカードがあり、無人化を意味しない。</p><div class="scroll"><table class="matrix"><caption>既存344カードの配置数。重複配置あり。市場規模・普及率・製品同士の接続実績ではない。数字を選ぶと技術一覧を絞り込む。</caption><thead><tr><th>工程</th>')
for role in roles.values():
    parts.append(f'<th>{h(role)}</th>')
parts.append('</tr></thead><tbody>')
for job, label in jobs.items():
    parts.append(f'<tr><th>{h(label)}</th>')
    for role in roles:
        cell = next(c for c in matrix_cells if c['job'] == job and c['role'] == role)
        examples = '・'.join(card_index[cid]['company'] for cid in cell['card_ids'][:2]) or '配置根拠なし'
        parts.append(f'<td><button type="button" data-cell-job="{job}" data-cell-role="{role}" aria-label="{h(label)}・{h(roles[role])}の{cell["count"]}件を表示"><strong>{cell["count"]}</strong><small>{h(examples)}</small></button></td>')
    parts.append('</tr>')
parts.append(f'</tbody></table></div><p class="muted">役割が未確定：{sum(not r["roles"] for r in technology)}件、工程が未確定：{sum(not r["jobs"] for r in technology)}件。空欄は確認待ち。件数の少なさだけで事業機会を判断しない。</p>')
parts.append('<h3>製品の間にある、確認すべき接点</h3><p>ここで挙げる製品は各モジュールの例。同じ接続構成として実装済みという意味ではない。開発余地は「どの接点で顧客が困るか」から検証する。</p>')
for interface in content['interfaces']:
    parts.append(f'<details class="panel" id="{interface["id"]}"><summary>{interface["id"]}　{h(interface["name"])} → <a href="#{interface["opportunity"]}">{interface["opportunity"]}</a></summary><dl><dt>受け渡すもの</dt><dd>{h(interface["transfer"])}</dd><dt>既存機能</dt><dd>{h(interface["observed"])}</dd><dt>未確認の接点</dt><dd>{h(interface["unknown"])}</dd></dl>{card_links(interface["cards"])}</details>')
parts.append('<h3 id="technologies">技術一覧：全344件</h3><p>概要の確認深度は混在する。一次分類のカードは、担当タスク・方式・人の残作業の追加確認が必要。基盤のみのカードは工程×役割の交差表に出ない場合があるが、下の一覧から参照できる。</p><div class="filters"><label>企業・製品・対象で検索<input id="search" type="search" placeholder="例：工具、DMG、計測"></label>')
for control, label, values in [('job', '工程', jobs), ('role', '役割', roles), ('foundation', '横断基盤', foundations), ('depth', '確認深度', {d:d for d in depth_counts})]:
    parts.append(f'<label>{label}<select id="{control}"><option value="">すべて</option>')
    for value, text in values.items():
        parts.append(f'<option value="{h(value)}">{h(text)}</option>')
    if control in ['job', 'role']:
        parts.append('<option value="unknown">未確定</option>')
    parts.append('</select></label>')
parts.append('<button id="reset" type="button">条件を解除</button></div><p id="result-count" aria-live="polite">344件表示</p><div class="scroll"><table class="tech-table"><thead><tr><th>企業・技術／ブース</th><th>工程・役割／基盤</th><th>対象・人の残作業・確実性</th><th>根拠</th></tr></thead><tbody>')
for record in technology:
    j = ' / '.join(jobs[x] for x in record['jobs']) or '工程未確定'
    r = ' / '.join(roles[x] for x in record['roles']) or '役割未確定'
    f = ' / '.join(foundations[x] for x in record['foundations'])
    urls = record['exhibitor_urls_2026'] or record['source_urls'][:2]
    parts.append(f'<tr id="tech-{record["card_id"]}" class="tech-row" data-job="{h(",".join(record["jobs"]))}" data-role="{h(",".join(record["roles"]))}" data-foundation="{h(",".join(record["foundations"]))}" data-depth="{h(record["depth"])}"><td><small>{record["card_id"]}</small><br><b>{h(record["company"])}</b><br>{h(record["item"][:180])}<br><small>ブース：{h(" / ".join(record["booths"])) or "未確認"}</small></td><td>{h(j)}<br><b>{h(r)}</b><br>{h(f)}<br><span class="badge">{h(record["depth"])}</span></td><td>{h(record["target"])}<br><small>{h(record["human_boundary"])}</small><br><small>{h(record["exhibition_status"])}／{h(record["product_stage"])}</small></td><td>{url_links(urls)}<details><summary>証拠ID</summary>{h(" / ".join(record["evidence_ids"]))}</details></td></tr>')
parts.append('</tbody></table></div><noscript><p>JavaScriptが無効のため、全件を表示しています。ブラウザのページ内検索を利用できます。</p></noscript></section>')

parts.append('<section id="candidates"><h2>③ 顧客向け開発候補と未確認事項</h2><p>順位は市場性の採点ではなく、自社能力を照合する順序の案。既存の代替手段に勝つ成果を示せなければ、独自開発を縮小・協業へ切り替える。</p>')
for item in content['candidates']:
    parts.append(f'<article id="{item["id"]}"><span class="badge">{h(item["priority"])}</span><h3>{item["id"]}　{h(item["name"])}</h3><p>{h(item["offer"])}</p><dl>')
    for key, label in [('customer','顧客'),('pain','困りごとの仮説'),('existing','既存の代替手段'),('differentiation','差別化を検証する点'),('own_fit','必要な自社能力'),('build','自ら担う'),('partner','他社と組む'),('ecosystem','外部基盤を使う'),('pilot','最小限の検証'),('metrics','測る成果と負担'),('economics','採算の確認'),('stop','棄却・縮小の条件')]:
        parts.append(f'<dt>{label}</dt><dd>{h(item[key])}</dd>')
    parts.append(f'</dl><p>戦略根拠：{source_links(item["sources"])}</p><p>既存技術：{card_links(item["cards"])}</p><p>現地質問：{" ".join(f"<a class=\"ref\" href=\"#{v}\">{v}</a>" for v in item["questions"])}</p></article>')
parts.append('<h3>データ取得・活用の戦略は、用途ごとに選ぶ</h3><div class="scroll"><table><thead><tr><th>経路</th><th>主な用途</th><th>得られること</th><th>成立条件</th></tr></thead><tbody>')
for row in content['data_strategy']:
    parts.append(f'<tr><th>{h(row["route"])}</th><td>{h(row["use"])}</td><td>{h(row["benefit"])}</td><td>{h(row["condition"])} {source_links(row["sources"])}</td></tr>')
parts.append('</tbody></table></div></section><section id="visits"><h2>現地で解く問い：回答が開発判断にどう効くか</h2><p>ブースは既存の2026公式CSVから照合。最新配置は訪問前に公式サイトで再確認する。戦略発表と当日の展示を区別して質問する。</p>')
for visit in content['visits']:
    more = ' / '.join(f'{x["company"]}（{"・".join(x["booths"])}）' for x in visit['additional_targets'])
    parts.append(f'<article id="{visit["id"]}"><span class="badge">{h(visit["priority"])}</span><h3>{visit["id"]}　{h(visit["target"])}</h3><p><b>{h(visit["company"])}：{h("・".join(visit["booths"])) or "要照合"}</b> {url_links(visit["official_urls"])}</p><p class="muted">{h(more)}</p><dl><dt>質問</dt><dd>{h(visit["question"])}</dd><dt>具体的に確認</dt><dd>{h(visit["request"])}</dd><dt>判断への使い方</dt><dd>{h(visit["decision"])}</dd></dl>{source_links(visit["sources"])}</article>')
parts.append('</section><section id="coverage"><h2>全体照合から見える変化と、情報不足</h2><h3>同じ社名の538件で、公開説明の変化を照合</h3><p>両年度に本文がある同名パネルで比較すると、AI・生成AI・フィジカルAIの明示は増える。一方、工場運用・データ連携の明示が一律に増えたわけではない。したがって、全体最適への方向は戦略・開発計画と技術の接点から評価し、文言の増加だけで業界全体の実装進展を断定しない。</p><div class="scroll"><table><thead><tr><th>公開説明の語群</th><th>2024</th><th>2026</th><th>明示が加わった</th><th>明示がなくなった</th></tr></thead><tbody>')
for row in text_signals:
    parts.append('<tr>' + ''.join(f'<td>{h(row[k])}</td>' for k in ['theme','wording_2024','wording_2026','newly_mentioned','no_longer_mentioned']) + '</tr>')
parts.append('</tbody></table></div><p class="muted">NFKC・空白除去・casefoldによる同名キー。法人格や社名変更の推測統合はしない。公開説明の明示数であり、導入率・新機能の登場数ではない。説明量・出展製品の選び方の年度差も残る。既存の集計規則と入力CSVのハッシュ一致を確認して再利用。</p><h3>全出展者リストを残した照合範囲</h3><div class="scroll"><table><caption>件数は企業数ではなく年度別リストの行数。同じ企業の別枠掲載を保持。</caption><thead><tr><th>年度</th><th>全掲載行</th><th>正規化社名</th><th>説明本文あり</th><th>技術との年度別URL照合あり</th><th>本文あり・照合なし</th><th>本文なし・照合なし</th></tr></thead><tbody>')
for row in coverage_summary:
    parts.append('<tr>' + ''.join(f'<td>{row[k]:,}</td>' for k in ['year','listing_rows','normalized_names','rows_with_description','rows_url_matched','description_but_unmapped','no_description_unmapped']) + '</tr>')
parts.append('</tbody></table></div><p>全2,427行を監査CSVに残し、年度別の公式詳細URLの完全一致と、社名が同じため関連する技術を別欄にした。本文あり・未配置は「関連技術なし」ではなく、台帳との照合又は精査が未完了という意味。</p><div class="grid">')
for depth, count in depth_counts.items():
    parts.append(f'<div class="metric"><strong>{count}</strong>{h(depth)}</div>')
parts.append('</div><h3>主要企業33社の確認状況</h3><p>大手は必ず確認対象に残す。AIの詳細が乏しい企業にも、工程集約・工具・計測などの役割がある。カード未整理の企業を機能なしとは扱わない。</p><div class="scroll"><table><thead><tr><th>企業／ブース</th><th>既存カードの例</th><th>確認状況／公式出展説明</th></tr></thead><tbody>')
for row in major_rows:
    parts.append(f'<tr><th>{h(row["company"])}<br><small>{h(" / ".join(row["booths"]))}</small></th><td>{card_links(row["card_ids"][:3]) or "技術カード未整理"}<br><small>{h(" / ".join(x[:55] for x in row["example_items"]))}</small>{h(row["context_note"])}</td><td>{h(row["status"])}<br>{url_links(row["official_urls"])}</td></tr>')
parts.append('</tbody></table></div><details class="panel"><summary>方法と解釈上の注意</summary><ul>' + paras(content['scope_notes']) + '</ul></details><div class="panel download"><h3>根拠・分類データ</h3>')
for filename, label in [('strategy_review.json','レビュー全体JSON'),('hypothesis_evidence_links.csv','潮流の因果・根拠CSV'),('exhibitor_coverage_all_2024_2026.csv','全出展者2,427行の照合CSV'),('macro_wording_signals.csv','同名パネルの文言比較CSV'),('technology_role_map.csv','技術344件の役割CSV'),('process_interfaces.csv','工程間の接点CSV'),('development_candidates.csv','開発候補CSV'),('fieldwork_questions.csv','現地質問CSV'),('major_company_coverage.csv','主要企業CSV'),('evidence_index.csv','出典索引CSV'),('provenance.json','入力ハッシュ・調査方法')]:
    parts.append(f'<a href="../data/research/strategy_review_20261021/{filename}">{label}</a>')
parts.append('</div></section><section id="sources"><h2>戦略・潮流の出典40資料</h2><p>既存34資料へ、既存ツール・参加窓口・少量データの反例など6資料を追加した。本文確認と検索抽出のみの資料を明示する。技術カードの根拠は各行のリンクと出典索引CSVから追える。</p>')
for source in sources:
    parts.append(f'<article class="source" id="source-{source["id"]}"><b>{source["id"]}　{h(source["publisher"])}｜{h(source["title"])}</b><p>{h(source["published_date"])} · {h(source["kind"])} · 確認 {h(source["checked_date"])}</p><p>{h(source["context"])}</p><small>該当箇所：{h(source["locator"])}<br>確認範囲：{h(source["reading_scope"])}</small><p>{url_links([source["url"]]+source.get("extra_urls", []),"原文")}</p></article>')
parts.append('</section><section id="next"><h2>レビュー後に決めること</h2><ol>' + paras(content['next_decisions']) + '</ol></section><footer>2026-10-21時点の公開情報と既存台帳による調査。公開発表・展示予定・実装実績を区別。外部記事の全文は再配布せず、要旨と出典を保存。</footer></main>')
parts.append('''<script>
const controls={search:document.getElementById('search'),job:document.getElementById('job'),role:document.getElementById('role'),foundation:document.getElementById('foundation'),depth:document.getElementById('depth')};
const rows=[...document.querySelectorAll('.tech-row')];
const fold=s=>s.normalize('NFKC').toLocaleLowerCase();
const matches=(value,list)=>!value||(value==='unknown'?!list:list.split(',').includes(value));
function filter(){const term=fold(controls.search.value.trim());let count=0;for(const row of rows){const ok=(!term||fold(row.textContent).includes(term))&&matches(controls.job.value,row.dataset.job)&&matches(controls.role.value,row.dataset.role)&&matches(controls.foundation.value,row.dataset.foundation)&&(!controls.depth.value||controls.depth.value===row.dataset.depth);row.hidden=!ok;if(ok)count++;}document.getElementById('result-count').textContent=count+'件表示 / 全'+rows.length+'件（重複配置あり）';}
Object.values(controls).forEach(c=>c.addEventListener(c.tagName==='INPUT'?'input':'change',filter));
function reset(){Object.values(controls).forEach(c=>c.value='');filter();}
document.getElementById('reset').addEventListener('click',reset);
document.querySelectorAll('[data-cell-job]').forEach(button=>button.addEventListener('click',()=>{reset();controls.job.value=button.dataset.cellJob;controls.role.value=button.dataset.cellRole;filter();document.getElementById('technologies').scrollIntoView({behavior:'smooth'});}));
function revealHash(){const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const target=document.getElementById(id);if(target?.classList.contains('tech-row')){reset();target.scrollIntoView();}}
addEventListener('hashchange',revealHash);filter();revealHash();
</script></body></html>''')
OUTPUT.write_text(''.join(parts), encoding='utf-8')
print(json.dumps(provenance['counts'], ensure_ascii=False, indent=2))
print(str(OUTPUT))
