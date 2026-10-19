"""Materialize the initial, evidence-linked research deliverables (no network)."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'research'

def save(name, rows):
    (OUT / (name + '.json')).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    if rows:
        with (OUT / (name + '.csv')).open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(k for row in rows for k in row)))
            writer.writeheader()
            writer.writerows({k: json.dumps(v,ensure_ascii=False) if isinstance(v,list) and any(isinstance(x,dict) for x in v) else ';'.join(v) if isinstance(v,list) else v for k,v in r.items()} for r in rows)

evidence = json.loads((OUT / 'evidence_v0.json').read_text(encoding='utf-8'))
claims = json.loads((OUT / 'claims_v0.json').read_text(encoding='utf-8'))
save('evidence_v0', evidence)
save('claims_v0', claims)
items = [
    dict(item_id='T001', company='オークマ株式会社', title='AI加工診断', customer_need='工具損傷・ワーク不良と過早交換を減らす', mechanism='CNC制御情報から異常度を算出し閾値超過時に工具退避', evidence_ids=['E002'], certainty='既存技術確認。2026個別展示未確認', baseline_2024='この台帳では2024当時の機能を未確定', plan_2026='AIコーナーの展示予告はE004で確認。個別診断機能の展示は要確認', difference='比較不能', constraint='ドリル加工対象、一部特別仕様。加工条件変更に対する誤検知・見逃しは未確認'),
    dict(item_id='T002', company='オークマ株式会社', title='smarTwinCELLの復帰ガイダンス', customer_need='異常除去後に作業者が迷わず生産再開したい', mechanism='デジタルツインで準備し、異常除去後に再起動手順を提示', evidence_ids=['E007'], certainty='2024展示説明確認。2026同機能展示未確認', baseline_2024='事前準備と再起動手順ガイダンスを案内', plan_2026='自動化とAIの展示予告のみ確認', difference='比較不能。自動復帰とは解釈しない', constraint='復帰条件の検証、手動介入、安全の責任分担が不明'),
    dict(item_id='T003', company='ファナック株式会社', title='FANUC Smart Digital Twin', customer_need='試削と現場段取りを減らす', mechanism='機械特性を含むサーボモデルで動作・時間・加工面品位を事前検証', evidence_ids=['E001', 'E003'], certainty='2024展示予告・既存製品確認。2026個別展示未確認', baseline_2024='サーボモデルによる加工前シミュレーションを案内', plan_2026='本調査時点で2026個別機能展示は未確認', difference='比較不能。2026新機能と混同しない', constraint='工具・材料・熱のモデル化範囲、予測誤差と校正工数は未確認'),
    dict(item_id='T004', company='ファナック株式会社', title='実工場で学ぶフィジカルAI共同実証', customer_need='品種変更の段取り替え・ピッキングの人手依存を減らす', mechanism='日立のAIとファナックのロボット・AIを実工場で検証し継続学習', evidence_ids=['E006'], certainty='2026年9月の共同実証計画発表。JIMTOF展示未確認', baseline_2024='AIによるバラ積み取出しをE001で案内', plan_2026='共同実証計画。2027年度からの展開を目指す', difference='発表上の対象がピッキング等から段取り替え・現場ルール適応へ広がる。実装性能の改善は未実証', constraint='学習データ量、未知形状成功率、タクト、品質、採用実績は未確認'),
    dict(item_id='T005', company='ヤマザキマザック株式会社', title='工程集約とAI・デジタル・自動化の融合展示', customer_need='工程間のムダと技能依存の削減', mechanism='最新INTEGREXとAI・デジタル・自動化ソリューションを展示予告', evidence_ids=['E005'], certainty='2026展示予告確認（テーマ単位）', baseline_2024='企業出展のみ確認。個別技術未調査', plan_2026='工程集約とAI等の融合を展示予定', difference='比較不能。具体方式未確認', constraint='AIの役割、既存製品との機能差、対応機種と利用制約は未確認')
]
items[2].update(certainty='2024・2026公式カタログに製品名掲載。機能差は未確認',plan_2026='Smart Digital Twinを主な出展物に掲載（E012）',evidence_ids=['E001','E003','E009','E012'])
items[4].update(baseline_2024='CNCマザトロールを中心に機械・ソフト・サービスの複合提案（E010）',evidence_ids=['E005','E010','E013'])
items.append(dict(item_id='T006', company='ファナック株式会社', title='フィジカルAI CNC／生成AIロボット駆動', customer_need='知的作業の自動化と現場の生産性向上', mechanism='オープンプラットフォームを利用した生成AIロボット駆動等を予告。モデル構成と制御接続は未確認', evidence_ids=['E009','E012'], certainty='2026公式カタログに展示予定記載。実演未確認', baseline_2024='AI高速バラ積み、ZDT、デジタルツインを掲載', plan_2026='フィジカルAI CNCとオープンプラットフォーム事例を掲載', difference='出展記述上の対象拡張。成功率・自律化度・性能向上は比較不能', constraint='自然言語指示の制御権限、未知条件判定、停止条件、再現性と商用実績は未確認'))
save('technology_items_v0', items)
themes = [
    dict(theme_id='R001', claim_id='C005', status='研究テーマ仮説・要現地確認', what='加工セルの異常後復帰支援', why='検知・退避だけでは残る停止後の判断と再準備の負担を減らす', method='制御時系列異常検知＋原因候補推定＋設備状態機械／制約付き手順生成。実行前に人が承認', conventional='単独の閾値監視と固定手順ガイダンスを比較対象にする', experiment='工具異常、把持失敗、非常停止後の代表事例で手順妥当性と再開時間を比較', metrics='復帰所要時間、誤指示率、人の介入回数、未知異常の棄却率', barrier='故障ラベル不足、状態観測不足、機種間差、復帰許可条件の設計', evidence_ids=['E002', 'E007'], adoption='未確認', market_size='未算定。顧客工程数と停止損失の実測が必要'),
    dict(theme_id='R002', claim_id='C006', status='研究テーマ仮説・要現地確認', what='品種変更時の少量データ適応', why='再教示と試行の負担を抑えて多品種生産を成立させる', method='ツイン事前検証＋視覚認識＋実機少量データで適応。接触作業は力覚の必要性を検証', conventional='固定教示と品種ごとの再設定を比較対象にする', experiment='類似部品群の形状・配置・把持条件を変更し、未学習部品で必要教示数とタクトを比較', metrics='再設定時間、必要データ数、成功率、タクト、品質不良率', barrier='仮想と実機の差、未知条件検出、学習の再現性、追加センサと統合費', evidence_ids=['E001', 'E003', 'E006'], adoption='共同実証計画の発表のみ。量産採用実績は未確認', market_size='未算定。対象工程・品種変更頻度と顧客数の根拠が必要')
]
save('research_themes_v0', themes)
common = ['顧客が最も困る工程と現在の対処は何か', '開発理由と方式の選択理由、実現の要所技術は何か', '適用範囲、制約、導入時の追加作業と費用は何か', '推定市場規模と対象工程・企業数・単価など算定根拠は何か', '受注・引き合い・PoC・採用件数を実績と見通しに分けて教えてほしい', '2024年と比べて製品機能・方式・対応範囲・実用化状況はどう変わったか', '今後の開発方向と実用化を妨げる課題は何か']
specific = {
    'オークマ株式会社': ['診断対象の工具・材料・加工法と、条件変更時の再学習は必要か', '誤検知率・見逃し率と、退避後の再開に必要な人手はどれだけか', 'smarTwinCELLの復帰ガイダンスと2026展示機能の差は何か'],
    'ファナック株式会社': ['サーボモデルに含む機械特性と、工具・材料・熱の扱いは何か', '実測に対する時間・面品位の予測誤差と校正工数はどれだけか', '共同実証の対象・学習データ量・未知形状の成功率と、今回の展示との関係は何か'],
    'ヤマザキマザック株式会社': ['2026のAI展示では何を入力し、どの判断をAIが担うか', '従来機能との違い、対応機種とデータ連携の制約は何か', '顧客導入で段取り時間・技能依存がどれだけ減ったか']
}
masters = {year: json.loads((ROOT/'data'/f'exhibitors_{year}.json').read_text(encoding='utf-8')) for year in (2024,2026)}
visits=[]
for company, qs in specific.items():
    record = next(r for r in masters[2026] if r['company_name'] == company)
    visits.append(dict(company_name=company, year=2026, booth=record['booth'], exhibitor_record_id=record['exhibitor_record_id'], priority='暫定A（3社内での重点、全社比較未了）', reason='R001/R002の方式・限界・成熟度を確認', questions=common+qs, visit_status='未訪問', confirmation='出展社一覧確認。個別技術の展示確度はtechnology_items_v0参照'))
save('field_questions_v0', visits)
save('poc_candidates_v0', [dict(year=2026, name=v['company_name'], booth=v['booth'], candidates=[dict(name=i['title'], overview=i['customer_need'], reason='研究テーマ仮説R001/R002の方式・制約・実用性を確認', questions='／'.join(specific[v['company_name']]), detail=i['mechanism']+'。展示確度：'+i['certainty']+'。制約：'+i['constraint'], difference=i['difference'], source='; '.join(next(e['url'] for e in evidence if e['evidence_id']==eid) for eid in i['evidence_ids'])) for i in items if i['company']==v['company_name']]) for v in visits])
save('slide_mapping_v0', [dict(slide=1, claim_id=c['claim_id'], evidence_ids=c['evidence_ids']) for c in claims])
assert all(set(c['evidence_ids']) <= {e['evidence_id'] for e in evidence} for c in claims)
assert len({c['claim_id'] for c in claims}) == len(claims)
print(f'{len(evidence)} evidence, {len(claims)} claims, {len(items)} items, {len(themes)} themes, {len(visits)} visit candidates')
