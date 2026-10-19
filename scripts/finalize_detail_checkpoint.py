"""Separate console-display warnings from retrieval failures using persisted records."""
import json
from collect_exhibitor_details import ROOT, save_json
from export_enriched_masters import export_all

path=ROOT/'checkpoints/exhibitor_details.json'
report=json.loads(path.read_text(encoding='utf-8'))
raw_path=ROOT/'checkpoints/exhibitor_details_collection_run.json'
if not raw_path.exists():
    save_json(raw_path,report)
warnings=[]
failures=[]
for failure in report.get('failures',[]):
    records=json.loads((ROOT/'data'/f"exhibitor_details_{failure['year']}.json").read_text(encoding='utf-8'))
    if "codec can't encode" in failure['error'] and any(r['detail_url']==failure['url'] for r in records):
        warnings.append(dict(failure,impact='Console print failed after data was saved. UTF-8 CSV/JSON and HTML are present.'))
    else:
        failures.append(failure)
report['console_display_warnings']=warnings
report['failures']=failures
report['merged_masters']=export_all()
report['csv_scope']='全掲載行を保持した説明本文・主な出展物付きCSV。未掲載と未取得を区別。'
save_json(path,report)
print(json.dumps(report['merged_masters'],ensure_ascii=False,indent=2))
