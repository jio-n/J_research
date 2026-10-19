"""Cache public official alphabetical lists; re-run to resume without re-fetching."""
import argparse
import csv
import hashlib
import html
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
import urllib.robotparser

ROOT = Path(__file__).resolve().parents[1]
STAMP = '2026-10-16'
HOST = 'https://www.jimtof.org'
UA = 'JIMTOFResearch/0.1 (public exhibitor-list research; sequential cached requests)'
for directory in ('sources', 'data', 'checkpoints'):
    (ROOT / directory).mkdir(exist_ok=True)

def fetch(url, target):
    if target.exists():
        return target.read_text(encoding='utf-8')
    time.sleep(1)
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as response:
                body = response.read()
            target.write_bytes(body)
            return body.decode('utf-8-sig')
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403, 429):
                raise RuntimeError(f'Access restriction {exc.code}; stop: {url}') from exc
            if attempt == 1:
                raise
            time.sleep(3)

def text(markup):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', markup))).strip()

def parse_page(markup, year, group, source):
    pairs = re.findall(r'<div class="col-md-2 col-sm-2(?: booth-col)?">(.*?)</div>\s*<div class="col-md-10 col-sm-10">(.*?)</div>', markup, re.S)
    if not pairs:
        raise ValueError(f'No list rows parsed: {source}')
    detailbase = re.search(r"window.open\('([^']+)'\s*\+\s*param", markup)
    records = []
    for booth_html, company_html in pairs:
        am_area = 'bg-AM' in company_html
        company_html_clean = re.sub(r'<span[^>]*>.*?</span>', '', company_html, flags=re.S)
        raw_name = text(company_html_clean)
        marker = '**' if '(**)' in raw_name else '*' if '(*)' in raw_name else ''
        name = re.sub(r'\s*\(\*{1,2}\)\s*$', '', raw_name).strip()
        companyid = re.search(r"CompanyDetails\('([^']+)'", company_html)
        detail = HOST + detailbase[1] + companyid[1] if companyid and detailbase else ''
        boothlink = re.search(r'href="([^"]+)"', booth_html)
        booth = text(booth_html)
        rowid = hashlib.sha256(f'{year}|{group}|{len(records)+1}|{raw_name}|{booth}'.encode()).hexdigest()[:16]
        records.append(dict(exhibitor_record_id=f'EXH-{year}-{rowid}', year=year, list_group=group,
                            company_name=name, company_name_as_listed=raw_name, booth=booth, am_area=am_area,
                            relationship_marker=marker, relationship_type={'*':'共同出展者','**':'内部出展者','':'記号なし'}[marker],
                            relationship_parent='', relationship_status='親出展社は未同定' if marker else '対象外',
                            detail_url=detail, booth_url=html.unescape(boothlink[1]) if boothlink else '',
                            exhibition_content='', exhibition_status='出展社一覧掲載のみ確認・展示内容未取得',
                            source_url=source, checked_date=STAMP,
                            missing_fields='展示内容;詳細本文;共同/内部出展の親会社' if marker else '展示内容;詳細本文'))
    return records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--years', nargs='+', type=int, default=[2024,2026])
    args = parser.parse_args()
    report = {'checked_date':STAMP, 'source':'JIMTOF official alphabetical catalog', 'years':{},
              'notes':['掲載行数・企業名重複除去数・公式発表出展者総数は別指標。',
                       '内部調査用キャッシュ。原典の文章・画像の無断転載はしない。',
                       '詳細ページと展示内容、親出展社の明示関係は次工程。']}
    robot_path = ROOT/'sources'/'robots.txt'
    try:
        if (ROOT/'sources'/'robots_status.json').exists() and not robot_path.exists():
            raise urllib.error.HTTPError(HOST+'/robots.txt',404,'cached 404',{},None)
        robots = fetch(HOST+'/robots.txt', robot_path)
        robot = urllib.robotparser.RobotFileParser()
        robot.parse(robots.splitlines())
        report['robots_status'] = 'retrieved'
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        robot = None
        report['robots_status'] = '404 Not Found; no robots directives published'
        (ROOT/'sources'/'robots_status.json').write_text(json.dumps({'url':HOST+'/robots.txt','status':404,'checked_date':STAMP}),encoding='utf-8')
    for year in args.years:
        prefix = '/2024' if year == 2024 else ''
        base = HOST+prefix+'/jp/exhi_search_pronoun'
        termsurl = HOST+prefix+'/jp/terms.html'
        terms = fetch(termsurl, ROOT/'sources'/f'{year}_terms.html')
        report.setdefault('terms',{})[str(year)] = {'url':termsurl,'cache':f'sources/{year}_terms.html',
            'summary':'保証制限・準拠法・文章画像写真の無断転載禁止。自動収集固有の禁止記載は確認されず。'}
        rows, groups, failures = [], {}, []
        for group in [str(n) for n in range(1,11)]+['oversea']:
            url = base+'?k='+group
            try:
                if robot and not robot.can_fetch(UA,url):
                    raise RuntimeError('robots disallows '+url)
                target = ROOT/'sources'/f'{year}_list_{group}.html'
                if group == '1' and not target.exists() and (ROOT/'sources'/f'{year}_initial.html').exists():
                    target.write_bytes((ROOT/'sources'/f'{year}_initial.html').read_bytes())
                markup = fetch(url,target)
                result = parse_page(markup,year,group,url)
                rows.extend(result)
                groups[group] = len(result)
                print(year, group, len(result), flush=True)
            except Exception as exc:
                failures.append({'group':group,'url':url,'error':str(exc)})
                print('FAILED',year,group,str(exc),flush=True)
                if 'restriction' in str(exc).lower() or 'robots disallows' in str(exc):
                    break
        out = ROOT/'data'/f'exhibitors_{year}'
        out.with_suffix('.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
        if rows:
            with out.with_suffix('.csv').open('w',encoding='utf-8-sig',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
        names = [re.sub(r'\s+','',r['company_name']) for r in rows]
        report['years'][str(year)] = {'listing_rows':len(rows),'unique_company_names_exact_whitespace_normalized':len(set(names)),
            'rows_with_detail_link':sum(bool(r['detail_url']) for r in rows),
            'rows_without_detail_link':sum(not bool(r['detail_url']) for r in rows),
            'joint_rows':sum(r['relationship_marker']=='*' for r in rows),
            'internal_rows':sum(r['relationship_marker']=='**' for r in rows),
            'missing_booth':sum(not r['booth'] for r in rows),'group_counts':groups,'failures':failures,
            'listing_coverage':'all 11 alphabetical groups retrieved' if len(groups)==11 else 'incomplete',
            'exhibition_content_retrieved':0,'official_announced_total':None,
            'remaining':'詳細本文・展示内容全件。詳細リンクなし行の企業公式資料。共同/内部出展の親会社。公式公表総数との別指標照合。',
            'files':[str(out.with_suffix('.csv').relative_to(ROOT)),str(out.with_suffix('.json').relative_to(ROOT))]}
        (ROOT/'checkpoints'/'exhibitors.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
