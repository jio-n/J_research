"""Check row preservation and complete screenshot-example text after collection."""
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
report={}
for year in (2024,2026):
    master=json.loads((ROOT/'data'/f'exhibitors_{year}.json').read_text(encoding='utf-8'))
    with (ROOT/'data'/f'exhibitors_{year}_with_details.csv').open(encoding='utf-8-sig',newline='') as stream:
        rows=list(csv.DictReader(stream))
    original={r['exhibitor_record_id']:r for r in master}
    assert len(rows)==len(master)
    assert {r['exhibitor_record_id'] for r in rows}==set(original)
    assert all(r['company_name']==original[r['exhibitor_record_id']]['company_name'] and r['booth']==original[r['exhibitor_record_id']]['booth'] for r in rows)
    assert all(r['detail_retrieval_status'] for r in rows)
    report[str(year)]={'listing_rows':len(rows),'rows_with_description':sum(bool(r['exhibition_content']) for r in rows),'rows_with_main_exhibits':sum(bool(r['main_exhibits']) for r in rows),'listing_rows_preserved':True,'name_booth_preserved':True,'maximum_description_chars':max(len(r['exhibition_content']) for r in rows)}
    if year==2026:
        dmg=next(r for r in rows if r['company_name']=='DMG森精機株式会社')
        assert all(term in dmg['exhibition_content'] for term in ['AIエージェント','AMR 1000','MATRIS WPH 210','第21回切削加工ドリームコンテスト'])
        assert all(term in dmg['main_exhibits'] for term in ['INH 63 FD','Automation Cube ONE'])
        assert '\n' in dmg['exhibition_content']
        report['screenshot_example']={'company':'DMG森精機株式会社','booth':dmg['booth'],'description_chars':len(dmg['exhibition_content']),'main_exhibits_chars':len(dmg['main_exhibits']),'screenshot_key_content_preserved':True,'paragraph_breaks_preserved':True}
(ROOT/'checkpoints/detail_csv_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
