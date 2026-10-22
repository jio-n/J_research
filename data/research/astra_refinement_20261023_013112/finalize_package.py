from pathlib import Path
import json,csv,hashlib,zipfile,xml.etree.ElementTree as ET,re,html,shutil
D=Path(__file__).parent;R=D.parents[2];O=R/'outputs'/D.name;P=D/'_private'
J=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
S=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=J(D/'original_file_hashes.json');changed=[p for p,sha in old.items() if not (R/p).exists() or S(R/p)!=sha]
assert not changed,('Pre-existing files changed',changed)
d=J(D/'research.json');g=J(D/'report_content.json');e=J(D/'evidence_review.json');baseline=J(R/'data/research/four_tag_20261022/research.json')
ids={x['id'] for x in d['items']};tags=['AI','フィジカルAI','自律化','自動化'];assert len(ids)==len(d['items'])==389
assert len(d['audit'])==1146;assert len(d['majors'])==33
for a,b in zip(d['audit'],baseline['audit']):assert all(a[k]==b[k] for k in ['row_no','record_id','company','booth','description_available','detail_url'])
for a in d['audit']:assert set(a['item_ids'])<=ids
for m in d['majors']:assert set(m['item_ids'])<=ids
for x in d['items']:
 assert set(x['tags'])==set(tags)
 assert all(x[k] for k in ['input','method','output','human','limits','exhibit','check','task_ids'])
 assert x['tag_names']==[t for t in tags if x['tags'][t]['status']!='—']
 assert x['source_urls'] and all(u.startswith(('https://','http://')) for u in x['source_urls'])
for f,n in [('candidate_items.csv',389),('tag_reasons.csv',1556),('all_exhibitor_audit.csv',1146),('recommended_visits.csv',39)]:
 with (D/f).open(encoding='utf-8-sig',newline='') as inp:assert len(list(csv.DictReader(inp)))==n
assert len(g['slides'])==28 and sum(s['section']=='メイン' for s in g['slides'])==3
assert all(set(s['ids'])<=ids for s in g['slides'])
known={v['source_id'] for v in e}|{q['quote_id'] for q in J(D/'original_quotes_reference.json')['quotes']}
assert all(set(s['refs'])<=known for s in g['slides'])
# Keep only final deliverables in outputs, preserving drafts privately in this new edition.
if (O/'report-r3.pptx').exists():
 if (O/'report.pptx').exists():
  assert not (P/'report-r1.pptx').exists();(O/'report.pptx').rename(P/'report-r1.pptx')
 if (O/'report-r2.pptx').exists():
  assert not (P/'report-r2.pptx').exists();(O/'report-r2.pptx').rename(P/'report-r2.pptx')
 (O/'report-r3.pptx').rename(O/'report.pptx')
assert S(O/'report.pptx')==J(P/'presentation_qa/validation-r3.json')['finalSha256']
native=J(D/'powerpoint_native_verification.json');assert native['slides']==28 and not native['cell_overflow_findings']
xls=J(P/'workbook_qa/native_verification.json');assert xls['candidate_rows']==389 and xls['master_rows']==1146 and xls['internal_links']==389
ht=J(D/'html_verification.json');assert not ht['errors'] and len(ht['checks'])>=32
expected=['index.html','report.html','report.pptx','technology_map.html','technology_map.svg','visits.html','visit_selection.xlsx','handover.html']
assert all((O/f).exists() for f in expected)
# Verify internal file and item references without making claims about external URL reachability.
links=0
for name in ['index.html','report.html','technology_map.html','visits.html','handover.html','technology_map.svg']:
 text=(O/name).read_text(encoding='utf8')
 for match in re.findall(r'href="([^"<>]+)"',text):
  url=html.unescape(match)
  if url.startswith(('https:','http:','#')) or any(c in url for c in ['{','+']):continue
  if '.html' in url or url.endswith(('.pptx','.xlsx','.svg')):
   fn=url.split('#')[0];assert (O/fn).exists(),(name,url);links+=1
   if '#item=' in url:assert url.split('#item=')[1] in ids
validation={
 'date':'2026-10-23','pre_existing_files':{'checked':len(old),'unchanged':len(old),'modified':[]},
 'data':{'candidate_items':389,'companies':344,'master_rows':1146,'major_companies':33,'tag_reason_rows':1556,'recommendations':39,'reviewed_items':32,'reviewed_sources':36,'unique_ids':True,'original_master_identity_and_booths_preserved':True,'csv_json_counts_match':True,'task_and_source_references_valid':True},
 'html':{'browser':ht['engine'],'method':ht['mode'],'checks':ht['checks'],'script_errors':ht['errors'],'internal_links_checked':links,'visual_review':'全5ページの代表範囲、候補詳細、スマートフォン幅、技術配置図を目視。'},
 'powerpoint':{'slides':28,'main':3,'appendix':25,'native_tables':28,'minimum_body_font_px':min(x['font_size_px'] for x in J(D/'presentation_layout.json')),'package_and_geometry':'pass','native_application':native,'visual_review':'全28枚を個別に描画・目視。英単語・数字の途中改行を調整。','final_sha256':S(O/'report.pptx')},
 'excel':{**xls,'technical_detail_rows':3890,'tag_reason_rows':1556,'visual_review':'全7シートの代表範囲を描画・目視。全セルの目視ではない。','formula_test':'訪問予定0→1→0。入力を復元して保存。','external_url_scope':'677リンクの設定を確認。全URLのライブ到達確認は実施していない。'},
 'limits':['現地実演・性能・成功率・失敗復帰は未検証。','389候補すべてを今回再精読したわけではない。','PowerPointの表は編集可能。HTML・Excel・PowerPointの本文は用途別編集で、同文複製ではない。']}
(D/'validation_summary.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
qa='<ul><li>PowerPoint：28枚を個別描画・目視。PowerPoint 16.0で読み取り、28の編集可能な表と表内文字の収まりを検証。はみ出し検出0。</li><li>HTML：独立したEdgeで検索・四タグAND/OR・展示確度・推奨・確認深度・詳細・CSV・地図リンク等32項目を確認。スクリプトエラー0。スマートフォン幅の横はみ出しを修正。</li><li>Excel：7シートを描画。Excel 16.0で389候補・1,146元行、フィルタ、入力、再計算0→1→0、389内部リンク・677出典リンクを確認。入力は初期値に復元。</li><li>元の266ファイルのSHA-256を照合し、変更なし。新版のCSV・JSON・候補ID・タグ件数の整合を検証。</li></ul><p>現地実演・技術性能、全外部URLのライブ到達、全Excelセルの目視は未実施。検証の詳細は新規データフォルダのvalidation_summary.jsonに記録。</p>'
p=O/'handover.html';s=p.read_text(encoding='utf8');s=s.replace('検証完了後の記録を本欄へ反映します。',qa);p.write_text(s,encoding='utf8')
skip={'input_inventory.txt','inspect_inputs.py','read_cached.py','original_file_hashes.json','manifest.json'}
files=[O/f for f in expected]+[p for p in D.iterdir() if p.is_file() and p.name not in skip and p.suffix in ['.json','.csv','.py','.mjs','.ps1','.md']]
manifest={'edition':D.name,'date':'2026-10-23','repository':'https://github.com/jio-n/J_research','file_count':len(files),'files':[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':S(p)} for p in files],'excluded':'_private（取得全文・プレビュー・途中版・ランタイム参照）、入力の全量ダンプ、原本ハッシュ一覧。manifest自身のハッシュは含めない。'}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'outputs':expected,'publication_files':len(files)+1,'originals_unchanged':len(old),'html_checks':len(ht['checks'])},ensure_ascii=False))
