from pathlib import Path
from collections import Counter
import json,csv,re,html,hashlib,unicodedata
D=Path(__file__).parent;R=D.parents[2];O=R/'outputs'/D.name
old=R/'data/research/astra_refinement_20261023_013112'
d=json.loads((old/'research.json').read_text(encoding='utf8'))
src={r['exhibitor_record_id']:r for r in csv.DictReader((R/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig'))}
pat=re.compile(r'(?<![A-Za-z])AI(?![A-Za-z])|人工知能|機械学習|深層学習|自律|自立|自動補正|自動生成|最適化|ロボット|自動化|自動搬送',re.I)
judgments={
'株式会社Smart Craft':('候補追加','実績データを活かすAI機能を出展説明に明記。AI担当処理・提供段階は未特定として候補化。'),
'株式会社ケーエムケーワールド':('確認待ち','生産計画の最適化・管理機能は記載。自動計画・AI判断の有無を確認できず、四タグを推定しない。'),
'テクノダイナミックス株式会社':('周辺部材・参考','フィジカルAI向け減速機という用途表現。減速機自体がAI判断する記載ではない。部材の探索対象として残す。'),
'リタール株式会社':('確認待ち','電気設計から製造への接続事例。どの処理が自動化されるかの説明を追加確認したい。'),
'JFEエンジニアリング株式会社':('周辺技術・参考','DfAMのトポロジー最適化支援。製造実行のAI・自律動作や自動化範囲は今回の本文から特定できない。'),
}
queue=[]
for a in d['audit']:
 r=src.get(a['record_id'],{});t=r.get('exhibition_content','')+' '+r.get('main_exhibits','');hits=list(pat.finditer(t))
 if a['item_ids'] or not hits:continue
 status,reason=judgments.get(a['company'],('候補追加保留','該当語は用途・対象分野・一般的な最適化・相談サービス等の記載。本文から対象タスクのAI判断・状態対応・自動処理を特定できず、今回候補を追加しない。技術の不存在とは断定しない。'))
 queue.append(dict(row_no=a['row_no'],record_id=a['record_id'],company=a['company'],booth=a['booth'],old_status=a['status'],decision=status,reason=reason,url=a['detail_url'],signals=list(dict.fromkeys(h.group() for h in hits)),excerpts=[t[max(0,h.start()-40):h.end()+85] for h in hits[:3]]))
a=next(a for a in d['audit'] if a['company']=='株式会社Smart Craft');r=src[a['record_id']]
tags={t:dict(status='—',reason='該当機能を公開説明から特定できない。') for t in ['AI','フィジカルAI','自律化','自動化']}
tags['AI']=dict(status='呼称・用途記載',reason='出展者説明に「蓄積した実績データを活かすAI機能」と記載。分析対象は生産性・不良率・リードタイム。AI方式、具体的な入出力、自動意思決定は未確認。')
x=dict(id='VP001',legacy_ids=[],company=a['company'],listing_ids=[a['record_id']],booths=[a['booth']],item='Smart Craft MES／実績データ活用・AI機能',task='工程・品質・在庫データの一元化と分析支援',need='進捗や検査記録を人に聞く負担、紙・Excelの分断と二重入力',input='タブレットから入力する作業実績・不良、検査記録・写真・測定値、在庫・ロット情報',method='クラウドMES、ダッシュボード、API連携。実績データ活用AIとの記載あり。AIアルゴリズム・学習条件・推論の具体処理は未確認',output='作業指示の配信、進捗・負荷の可視化、検査記録・在庫の管理。AI固有の出力は要確認',human='工程・帳票・検査項目の設定、作業実績や不良・検査値の入力。AI結果の承認・修正方法は要確認',limits='AIは呼称・用途記載として候補化。自動スケジューリングや実機制御を認定しない',exhibit_note='保存済み公式出展説明にMESデモとAI機能を記載。AIの個別デモ範囲、提供済みか開発計画かは未確認。今回ライブ再取得は失敗',stage='MESデモ予定／AI個別機能の段階は未確認',sources=[dict(source_id='VP-S01',publisher=a['company'],title='JIMTOF2026公式出展者説明（保存済み）',url=a['detail_url'],locator='主な出展物 > データ活用／AI',checked_date=r['detail_checked_date'],usage='既存保存本文を2026-10-23に再読。ライブ再取得未完了')],tags=tags,depth='保存済み公式出展説明を再読（製品技術資料未照合）',exhibit='企業・MES展示予定／AI個別実演未確認',advance='AI方式・提供段階未確認',check='AIが具体的に何を入力し何を出すか。単なる集計との違い、異常要因分析・推奨・再計画の範囲、必要データ量、人の承認、実機への接続を確認',recommendation='事前確認',recommend_reason='工程・品質・在庫データ接続の比較対象。AIの具体機能は事前に問い合わせたい',source_urls=[a['detail_url']],source_ids=['VP-S01'],task_ids=['P10','P11'],task_categories=['生産計画・運用','データ・シミュレーション基盤'],refinement_review='今回：保存済み公式本文を再読',physical_ai_class='物理動作へのAI接続未確認',novelty_note='新規性・性能の独立検証なし',taxonomy_basis='工程・品質・在庫の接続と分析支援に対応付け')
d['items'].append(x);a['status']='候補あり（新版追加）';a['item_ids']=['VP001'];a['reason']='保存済み公式説明のAI機能記載を再読して追加。具体方式は未確認。'
for x in d['items']:
 # This is a transparent re-edit of existing evidence, not new technical claims.
 x['overview']='対象は'+x['task']+'。'+x['method']+'。出力は'+x['output']+'。'
 x['explanation_basis']='既存のタスク・方式・出力欄を読みやすく再編集。新たな性能認定ではない。'
d['coverage_review']=dict(scanned_rows=len(d['audit']),original_rows_without_description=sum(not a['description_available'] for a in d['audit']),signal_rows=len(queue),added=1,queue=queue,method='保存済み2026年全出展者説明を関連語で横断走査し、未対応27件の周辺文脈を再読。無語の見落とし、説明未掲載、更新後の追加情報は網羅できない。',live_check='公式ページ3件はWeb取得ツールで到達できず。今回の追加判定は保存済み公式説明に限定。')
d['previous_edition_stats']=d['stats'].copy()
d['stats']['candidate_items']=len(d['items'])
norm=lambda s:re.sub(r'[\s・･,，.．()（）]','',unicodedata.normalize('NFKC',s)).replace('株式会社','').replace('合同会社','').lower()
d['stats']['candidate_companies']=len(set(norm(x['company']) for x in d['items']))
d['stats']['linked_master_rows']=sum(bool(a['item_ids']) for a in d['audit'])
d['stats']['audit_status']=dict(Counter(a['status'] for a in d['audit']))
d['stats']['recommendations']=sum(x['recommendation']!='通常候補' for x in d['items'])
d['stats']['tag_counts']={t:dict(Counter(x['tags'][t]['status'] for x in d['items'] if x['tags'][t]['status']!='—')) for t in tags}
d['stats']['depth_counts']=dict(Counter(x['depth'] for x in d['items']))
d['planner_version']=D.name
(D/'research.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
(D/'coverage_review.json').write_text(json.dumps(d['coverage_review'],ensure_ascii=False,indent=2),encoding='utf8')
with (D/'coverage_review.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['row_no','company','booth','old_status','decision','reason','url','signals','excerpts'],extrasaction='ignore');w.writeheader();w.writerows(queue)
template=(D/'template.html').read_text(encoding='utf8')
serialized=json.dumps(d,ensure_ascii=False).replace('<','\\u003c')
(O/'visits.html').write_text(template.replace('__DATA__',serialized).replace('__SEED__','{}'),encoding='utf8')
assert len(d['items'])==390 and len(queue)==27
print(json.dumps(dict(items=len(d['items']),coverage_flags=len(queue),output=str(O)),ensure_ascii=False))
