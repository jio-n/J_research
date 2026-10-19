"""Reproducible catalogue census. Counts describe wording, not adoption."""
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/research/macro_20261019'
OUT.mkdir(parents=True, exist_ok=True)
RULES = {
    'AI明示': r'(?<![a-z])ai(?![a-z])|人工知能|機械学習|深層学習|生成ai|machine learning|deep learning',
    '生成AIとエージェント': r'生成ai|エージェント|大規模言語|\bllm\b|generative ai|coagent|copilot|chatgpt',
    'フィジカルAI明示': r'フィジカル\s*ai|physical\s*ai',
    '自動化と省人化': r'自動化|省人|省力|無人|ロボット|ハンドリング|自動搬送|自動計測|自動測定|自動検査|automation|robot|unmanned',
    '設計製造のデジタル化': r'デジタルツイン|シミュレ|自動プログラ|(?<![a-z])(?:cad|cam)(?![a-z])|工程設計|工程計画|見積|digital twin|simulation',
    '工場運用とデータ連携': r'(?<![a-z])(?:dx|ax|iot|mes|aps|opc)(?![a-z])|データ連携|データ活用|稼働監視|稼働管理|工程管理|生産管理|工具管理|デジタル化|smart factory',
    '状態監視と補正': r'機上計測|加工監視|状態監視|異常検|予知|予兆|予防保全|適応制御|補正|インプロセス|in.process|condition monitoring',
    '自律の明示': r'自律|autonomous',
}
MAJORS = ['DMG森精機','ヤマザキマザック','オークマ','牧野フライス製作所','ファナック','三菱電機','シーメンス','ジェイテクト','ニデックマシンツール','ニデックオーケーケー','ソディック','アマダ','ブラザー工業','松浦機械製作所','シチズンマシナリー','スター精密','ツガミ','オーエスジー','三菱マテリアル','京セラ','タンガロイ','ミツトヨ','東京精密','レニショー','ハイデンハイン','ベッコフオートメーション','Hexagon Manufacturing Intelligence','住友電気工業','中村留精密工業','FUJI','TAKISAWA','オートデスク','ニコン']

def norm(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s)).casefold()

def short(s):
    return norm(s).replace('株式会社', '').replace('合同会社', '')

data = {}
all_records = []
summary = {'basis': '全掲載行を処理し、NFKC・空白除去・casefoldの名称キーで集約。法人単位の完全名寄せではない。', 'rules': RULES}
for year in [2024, 2026]:
    f = ROOT / f'data/exhibitors_{year}_with_details.csv'
    rows = list(csv.DictReader(f.open(encoding='utf-8-sig', newline='')))
    groups = {}
    for row in rows:
        k = norm(row['company_name'])
        g = groups.setdefault(k, {'key': k, 'company': row['company_name'], 'rows': [], 'texts': [], 'urls': [], 'booths': []})
        g['rows'].append(row['exhibitor_record_id'])
        for value in [row['exhibition_content'], row['main_exhibits']]:
            if value.strip() and value not in g['texts']:
                g['texts'].append(value)
        if row['detail_url'] and row['detail_url'] not in g['urls']:
            g['urls'].append(row['detail_url'])
        if row['booth'] not in g['booths']:
            g['booths'].append(row['booth'])
    for g in groups.values():
        g['text'] = '\n'.join(g['texts'])
        t = unicodedata.normalize('NFKC', g['text']).lower()
        g['tags'] = [label for label, pattern in RULES.items() if re.search(pattern, t)]
        g['hits'] = {label: list(dict.fromkeys(m.group() for m in re.finditer(pattern, t))) for label, pattern in RULES.items() if re.search(pattern, t)}
        all_records.append({'year': year, **g})
    data[year] = groups
    usable = [g for g in groups.values() if g['text']]
    summary[str(year)] = {
        'input': str(f.relative_to(ROOT)), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
        'listing_rows': len(rows), 'name_keys': len(groups), 'text_name_keys': len(usable),
        'text_coverage_pct': round(100 * len(usable) / len(groups), 1),
        'no_text_name_keys': len(groups) - len(usable),
        'theme_counts': {label: sum(label in g['tags'] for g in usable) for label in RULES},
        'theme_rates': {label: round(100 * sum(label in g['tags'] for g in usable) / len(usable), 1) for label in RULES},
    }

panel_keys = sorted(k for k in set(data[2024]) & set(data[2026]) if data[2024][k]['text'] and data[2026][k]['text'])
summary['matched_panel'] = {'name_keys': len(panel_keys), 'counts': {}, 'transitions': {}}
for tag in RULES:
    summary['matched_panel']['counts'][tag] = {str(y): sum(tag in data[y][k]['tags'] for k in panel_keys) for y in [2024,2026]}
    summary['matched_panel']['transitions'][tag] = {
        'both': sum(tag in data[2024][k]['tags'] and tag in data[2026][k]['tags'] for k in panel_keys),
        'added_wording': sum(tag not in data[2024][k]['tags'] and tag in data[2026][k]['tags'] for k in panel_keys),
        'removed_wording': sum(tag in data[2024][k]['tags'] and tag not in data[2026][k]['tags'] for k in panel_keys),
    }
summary['cooccurrence_2026'] = {tag: sum('AI明示' in g['tags'] and tag in g['tags'] for g in data[2026].values()) for tag in RULES if tag != 'AI明示'}
summary['notes'] = ['語の明示件数は採用率・市場シェア・成熟度ではない。分類は重複。', '同名パネルにも説明量・製品選択の年度差がある。語の追加は新機能登場を意味しない。', '情報欠損を陰性として扱わない。社名変更は本パネルに自動追加しない。']

majors = []
for target in MAJORS:
    matches = [g for g in data[2026].values() if short(g['company']) == short(target)]
    if not matches:
        matches = [g for g in data[2026].values() if short(target) in short(g['company'])]
    for g in matches:
        old = data[2024].get(g['key'])
        majors.append({'target': target, 'company': g['company'], 'booths': g['booths'], 'tags': g['tags'], 'text_2026': g['text'], 'text_2024': old['text'] if old else '', 'urls_2026': g['urls'], 'urls_2024': old['urls'] if old else [], 'key': g['key']})

(OUT/'census.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT/'corpus.json').write_text(json.dumps(all_records, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT/'major_dossiers.json').write_text(json.dumps(majors, ensure_ascii=False, indent=2), encoding='utf-8')
with (OUT/'census_audit.csv').open('w', encoding='utf-8-sig', newline='') as f:
    cols = ['year','company','booths','text_available',*RULES,'source_urls','record_ids']
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for g in all_records:
        w.writerow({'year':g['year'],'company':g['company'],'booths':';'.join(g['booths']),'text_available':bool(g['text']),**{k:k in g['tags'] for k in RULES},'source_urls':';'.join(g['urls']),'record_ids':';'.join(g['rows'])})
print(json.dumps(summary, ensure_ascii=False, indent=2))
print('Major dossiers:',len(majors))
