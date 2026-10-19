"""Join cached official detail text to all listing rows without dropping missing rows."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def export_year(year):
    master = json.loads((ROOT/'data'/f'exhibitors_{year}.json').read_text(encoding='utf-8'))
    detail_path = ROOT/'data'/f'exhibitor_details_{year}.json'
    details = json.loads(detail_path.read_text(encoding='utf-8')) if detail_path.exists() else []
    by_id = {r['exhibitor_record_id']:r for r in details}
    rows = []
    for original in master:
        row = dict(original)
        detail = by_id.get(row['exhibitor_record_id'])
        row['exhibition_content'] = detail.get('exhibition_introduction','') if detail else ''
        row['main_exhibits'] = detail.get('main_exhibits','') if detail else ''
        row['detail_retrieval_status'] = detail['parse_status'] if detail else '詳細未取得' if row['detail_url'] else '公式一覧に詳細URLなし'
        row['detail_checked_date'] = detail.get('checked_date','') if detail else ''
        row['detail_evidence_locator'] = detail.get('evidence_locator','') if detail else ''
        row['detail_cache_path'] = detail.get('cache_path','') if detail else ''
        if detail:
            row['exhibition_status'] = f'{year}公式カタログの出展者説明取得済み' if row['exhibition_content'] or row['main_exhibits'] else f'{year}公式詳細取得済み・説明記載なし'
            if year==2026:
                row['exhibition_status'] += '・展示予定（現地未確認）'
            missing = row['missing_fields'].split(';')
            if row['exhibition_content']:
                missing = [f for f in missing if f!='展示内容']
            missing = [f for f in missing if f!='詳細本文']
            row['missing_fields'] = ';'.join(missing)
        rows.append(row)
    out = ROOT/'data'/f'exhibitors_{year}_with_details'
    tmp = out.with_suffix('.csv.tmp')
    with tmp.open('w',encoding='utf-8-sig',newline='') as stream:
        front = ['year','company_name','booth','exhibition_content','main_exhibits','detail_retrieval_status','detail_url','detail_checked_date']
        writer = csv.DictWriter(stream,fieldnames=front+[k for k in rows[0] if k not in front])
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(out.with_suffix('.csv'))
    summary = dict(year=year,total_listing_rows=len(rows),detail_records=len(details),rows_with_introduction=sum(bool(r['exhibition_content']) for r in rows),rows_with_main_exhibits=sum(bool(r['main_exhibits']) for r in rows),rows_not_retrieved=sum(r['detail_retrieval_status']=='詳細未取得' for r in rows),rows_without_detail_url=sum(not bool(r['detail_url']) for r in rows),csv=str(out.with_suffix('.csv').relative_to(ROOT)))
    assert len(rows)==len(master)
    assert len({r['exhibitor_record_id'] for r in rows})==len(rows)
    with out.with_suffix('.csv').open(encoding='utf-8-sig',newline='') as stream:
        assert len(list(csv.DictReader(stream)))==len(master)
    return summary

def export_all():
    summary = {str(y):export_year(y) for y in (2024,2026)}
    temp = ROOT/'checkpoints/enriched_masters.json.tmp'
    temp.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    temp.replace(ROOT/'checkpoints/enriched_masters.json')
    return summary

if __name__=='__main__':
    print(json.dumps(export_all(),ensure_ascii=False,indent=2))
