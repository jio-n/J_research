"""Reparse already fetched HTML only; never request the network."""
import argparse
import json
from collect_exhibitor_details import ROOT, extract, save_json, status_from_text
from export_enriched_masters import export_all

parser=argparse.ArgumentParser()
parser.add_argument('--year',nargs='+',type=int,choices=[2024,2026],default=[2024,2026])
parser.add_argument('--status-only',action='store_true',help='Keep stored text and refresh only its missing-field classification')
args=parser.parse_args()
for year in args.year:
    path=ROOT/'data'/f'exhibitor_details_{year}.json'
    records=json.loads(path.read_text(encoding='utf-8'))
    for record in records:
        if args.status_only:
            if not record['parse_status'].startswith('本文未解析'):
                record['parse_status']=status_from_text(record['exhibition_introduction'],record['main_exhibits'])
        else:
            record.update(extract((ROOT/record['cache_path']).read_text(encoding='utf-8-sig')))
    save_json(path,records)
print(json.dumps(export_all(),ensure_ascii=False,indent=2))
