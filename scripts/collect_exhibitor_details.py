"""Resume public official detail-page enrichment separately from list masters."""
import argparse
import csv
import json
from pathlib import Path
import re
import urllib.robotparser
import html
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from collect_exhibitors import ROOT, STAMP, UA, fetch, text
from export_enriched_masters import export_all

def detail_text(markup):
    markup = re.sub(r'<br\s*/?>|</p>', '\n', markup, flags=re.I)
    markup = html.unescape(re.sub('<[^>]+>', ' ', markup))
    return '\n'.join(re.sub(r'[\t \xa0]+',' ',line).strip() for line in markup.splitlines() if line.strip())

def status_from_text(intro_text,exhibits_text):
    return '説明本文・主な出展物を保存済み' if intro_text and exhibits_text else '説明本文のみ掲載（主な出展物欄なし）' if intro_text else '主な出展物のみ掲載（説明本文なし）' if exhibits_text else '公式詳細に説明・出展物の記載なし'

def extract(markup):
    main = re.search(r'<main\b[^>]*>(.*?)</main>', markup, re.S)
    if not main:
        return {'parse_status':'本文未解析：main要素なし', 'exhibition_introduction':'', 'main_exhibits':''}
    content = main[1]
    introduction = re.search(r'<div class="col-md-8 mb-5">\s*<p[^>]*>(.*?)</p>',content,re.S)
    exhibits = re.search(r'<h3[^>]*>\s*主な出展物\s*</h3>\s*<p[^>]*>(.*?)</p>',content,re.S)
    intro_text = detail_text(introduction[1]) if introduction else ''
    exhibits_text = detail_text(exhibits[1]) if exhibits else ''
    status = status_from_text(intro_text,exhibits_text)
    return dict(parse_status=status,
                exhibition_introduction=intro_text,
                main_exhibits=exhibits_text,
                evidence_locator='main > div.container > div.row > div.col-md-8.mb-5; 見出し「主な出展物」と直後のp',
                evidence_type='公式カタログ掲載・出展者記述。2026は展示予定で現地実演未確認。')

def save_json(path,value):
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year',nargs='+',type=int,choices=[2024,2026],default=[2024,2026])
    parser.add_argument('--limit',type=int,default=None,help='Maximum uncaptured detail URLs this run, across selected years')
    parser.add_argument('--company',nargs='+',default=[],help='Company-name substrings; omitted means all detail links')
    args = parser.parse_args()
    robotpath = ROOT/'sources'/'robots.txt'
    robot = None
    if robotpath.exists():
        robot = urllib.robotparser.RobotFileParser()
        robot.parse(robotpath.read_text(encoding='utf-8').splitlines())
    report = {'checked_date':STAMP,'selected_years':args.year,'company_filters':args.company,
              'attempted_this_run':0,'retrieved_this_run':0,'failures':[], 'years':{},
              'original_list_masters_unchanged':True,
              'remaining_scope':'詳細URLなし行は対象外。全社の解釈・展示確度分類・親出展社の同定は別工程。'}
    stopped = False
    consecutive_failures = 0
    for year in args.year:
        master = json.loads((ROOT/'data'/f'exhibitors_{year}.json').read_text(encoding='utf-8'))
        out = ROOT/'data'/f'exhibitor_details_{year}'
        records = json.loads(out.with_suffix('.json').read_text(encoding='utf-8')) if out.with_suffix('.json').exists() else []
        for record in records:
            cache = ROOT/record['cache_path']
            if cache.exists():
                record.update(extract(cache.read_text(encoding='utf-8-sig')))
        save_json(out.with_suffix('.json'),records)
        done = {r['exhibitor_record_id'] for r in records}
        selected = [r for r in master if r['detail_url'] and (not args.company or any(n in r['company_name'] for n in args.company))]
        for row in selected:
            if row['exhibitor_record_id'] in done:
                continue
            if args.limit is not None and report['attempted_this_run'] >= args.limit:
                break
            report['attempted_this_run'] += 1
            try:
                if robot and not robot.can_fetch(UA,row['detail_url']):
                    raise RuntimeError('robots disallows '+row['detail_url'])
                cache = ROOT/'sources'/f'detail_{year}_{row["exhibitor_record_id"]}.html'
                markup = fetch(row['detail_url'],cache)
                result = {k:row[k] for k in ('exhibitor_record_id','year','company_name','booth','detail_url')}
                result.update(extract(markup))
                result.update(checked_date=STAMP,cache_path=str(cache.relative_to(ROOT)))
                records.append(result)
                done.add(row['exhibitor_record_id'])
                save_json(out.with_suffix('.json'),records)
                report['retrieved_this_run'] += 1
                consecutive_failures = 0
                if report['retrieved_this_run'] % 25 == 0:
                    export_all()
                print(year,row['company_name'],result['parse_status'],flush=True)
            except Exception as exc:
                consecutive_failures += 1
                report['failures'].append({'year':year,'company_name':row['company_name'],'url':row['detail_url'],'error':str(exc)})
                if 'restriction' in str(exc).lower() or 'robots disallows' in str(exc) or consecutive_failures>=3:
                    stopped = True
                    break
            finally:
                save_json(ROOT/'checkpoints'/'exhibitor_details.json',report)
        if records:
            with out.with_suffix('.csv').open('w',encoding='utf-8-sig',newline='') as stream:
                writer = csv.DictWriter(stream,fieldnames=sorted(set().union(*(r.keys() for r in records))))
                writer.writeheader()
                writer.writerows(records)
        report['years'][str(year)] = {'selected_detail_links':len(selected),'selected_remaining':sum(r['exhibitor_record_id'] not in done for r in selected),
            'cumulative_detail_records':len(records),'cumulative_main_exhibits_extracted':sum(bool(r['main_exhibits']) for r in records),
            'all_master_linked_rows_remaining':sum(bool(r['detail_url']) and r['exhibitor_record_id'] not in done for r in master),
            'master_rows_without_detail_links':sum(not bool(r['detail_url']) for r in master),
            'files':[str(out.with_suffix('.json').relative_to(ROOT)),str(out.with_suffix('.csv').relative_to(ROOT))]}
        if stopped:
            break
    report['stopped_on_access_restriction'] = stopped
    report['merged_masters'] = export_all()
    report['next_all_details_command'] = "& 'C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/collect_exhibitor_details.py --year 2024 2026"
    save_json(ROOT/'checkpoints'/'exhibitor_details.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
