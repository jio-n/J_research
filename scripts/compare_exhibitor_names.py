"""Conservative cross-year name candidates and list-to-cache row-count validation."""
import csv
import json
from collections import defaultdict
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
def key(name):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', name)).casefold()

data = {year:json.loads((ROOT/'data'/f'exhibitors_{year}.json').read_text(encoding='utf-8')) for year in (2024,2026)}
validation = {}
for year, rows in data.items():
    groupchecks = []
    for path in sorted((ROOT/'sources').glob(f'{year}_list_*.html')):
        group = path.stem.split('_')[-1]
        markup = path.read_text(encoding='utf-8')
        raw_count = len(re.findall(r'<div class="col-md-10 col-sm-10">',markup))
        parsed_count = sum(r['list_group']==group for r in rows)
        groupchecks.append(dict(group=group, raw_company_cells=raw_count, master_rows=parsed_count, matches=raw_count==parsed_count))
    ids = [r['exhibitor_record_id'] for r in rows]
    duplicate_pairs = defaultdict(list)
    for row in rows:
        duplicate_pairs[(key(row['company_name']),row['booth'])].append(row['exhibitor_record_id'])
    validation[str(year)] = dict(group_checks=groupchecks, total_rows=len(rows),
        all_group_counts_match=all(g['matches'] for g in groupchecks), unique_record_ids=len(set(ids))==len(ids),
        missing_company_name=sum(not r['company_name'] for r in rows),missing_booth=sum(not r['booth'] for r in rows),
        duplicate_name_booth_groups=[dict(normalized_name=n,booth=b,record_ids=values) for (n,b),values in duplicate_pairs.items() if len(values)>1])

indices = {}
for year, rows in data.items():
    indices[year] = defaultdict(list)
    for row in rows:
        indices[year][key(row['company_name'])].append(row)

matches = []
for normalized_name in sorted(set(indices[2024]) | set(indices[2026])):
    older, newer = indices[2024].get(normalized_name,[]),indices[2026].get(normalized_name,[])
    matches.append(dict(normalized_name=normalized_name,
        company_name_2024=' | '.join(sorted(set(r['company_name'] for r in older))),
        company_name_2026=' | '.join(sorted(set(r['company_name'] for r in newer))),
        presence='両年掲載・名称一致候補' if older and newer else '2024のみ掲載' if older else '2026のみ掲載',
        matching_method='NFKC・空白除去・casefold。法人同一性は未確認。',
        record_ids_2024=';'.join(r['exhibitor_record_id'] for r in older),
        record_ids_2026=';'.join(r['exhibitor_record_id'] for r in newer),
        booths_2024=';'.join(sorted(set(r['booth'] for r in older))),
        booths_2026=';'.join(sorted(set(r['booth'] for r in newer))),
        content_comparison='比較不能・両年展示内容未取得'))

(ROOT/'data'/'exhibitor_name_matches_2024_2026.json').write_text(json.dumps(matches,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'data'/'exhibitor_name_matches_2024_2026.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer = csv.DictWriter(stream,fieldnames=list(matches[0]))
    writer.writeheader()
    writer.writerows(matches)
validation['name_matching'] = {'both_year_name_candidates':sum(m['presence']=='両年掲載・名称一致候補' for m in matches),
    'only_2024':sum(m['presence']=='2024のみ掲載' for m in matches), 'only_2026':sum(m['presence']=='2026のみ掲載' for m in matches),
    'note':'名称一致のみ。社名変更・統合・表記揺れ未調査。出展内容差分は未取得のため比較不能。'}
(ROOT/'checkpoints'/'exhibitor_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(validation,ensure_ascii=False,indent=2))
