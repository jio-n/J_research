"""Add the six inspected official catalog records to the evidence ledger."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'data/research'
evidence=json.loads((out/'evidence_v0.json').read_text(encoding='utf-8'))
byid={e['evidence_id']:e for e in evidence}
number=8
for year in (2024,2026):
    for r in json.loads((root/'data'/f'exhibitor_details_{year}.json').read_text(encoding='utf-8')):
        eid=f'E{number:03}'
        number+=1
        byid[eid]=dict(evidence_id=eid,publisher=r['company_name']+'（JIMTOF公式カタログ）',title=f"{year}公式出展者詳細：{r['company_name']}",url=r['detail_url'],locator='出展紹介本文、見出し「主な出展物」の直後',checked_at=r['checked_date'],published_at=None,type='公式掲載のメーカー出展説明',summary={
            (2024,'オークマ株式会社'):'工程集約・知能化とARMROID、OMR20、smarTwinCELLを案内。',
            (2024,'ファナック株式会社'):'Smart Digital Twin、AI高速バラ積み、AIも用いるZDT、AIサーボモニタを案内。',
            (2024,'ヤマザキマザック株式会社'):'CNCマザトロールを中心に機械・ソフト・サービスの複合ソリューションを案内。',
            (2026,'オークマ株式会社'):'工程集約・自動化・AI知能化の融合、熱変位制御とAIによる品質・稼働率向上を予告。',
            (2026,'ファナック株式会社'):'フィジカルAI CNCと、生成AIロボット駆動を含むオープンプラットフォーム事例を予告。Smart Digital Twinも掲載。',
            (2026,'ヤマザキマザック株式会社'):'INTEGREXを中心に工程集約と自動化・デジタル・AIの融合を予告。'
        }[(year,r['company_name'])],exhibition_certainty=f'{year}公式カタログ記述確認'+('・展示予定' if year==2026 else ''),limitations='出展者の説明。実演内容・性能・商用成熟度は現地未確認。',cache_path=r['cache_path'])
(out/'evidence_v0.json').write_text(json.dumps(list(byid.values()),ensure_ascii=False,indent=2),encoding='utf-8')
claims=json.loads((out/'claims_v0.json').read_text(encoding='utf-8'))
for c in claims:
    if c['claim_id']=='C003':
        c.update(text='2024のAIバラ積み等に対し、2026公式カタログにはフィジカルAI CNCと生成AIロボット駆動の展示予告がある。別途、実工場の共同実証計画も発表された。',evidence_ids=['E009','E012','E006'],scope='展示記述の差は確認。性能差・自律化度・共同実証と展示の関係は未確認')
    if c['claim_id']=='C004':
        c['evidence_ids']=['E002','E006','E007','E012']
(out/'claims_v0.json').write_text(json.dumps(claims,ensure_ascii=False,indent=2),encoding='utf-8')
