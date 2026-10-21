from pathlib import Path
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'data/research/deep_reading_20261021'
original=json.loads((ROOT/'data/research/strategy_review_20261021/strategy_review.json').read_text(encoding='utf-8'))['sources']
first=(DEST/'01_source_readings.md').read_text(encoding='utf-8')
second=(DEST/'02_followup_investigations.md').read_text(encoding='utf-8')
ids=re.findall(r'^## (S\d\d) ',first,re.M)
assert ids==[f'S{i:02}' for i in range(1,41)],ids
extra=re.findall(r'^### (A\d\d) ',second,re.M)
assert len(extra)==11 and len(set(extra))==11,extra
assert set(extra)=={f'A{i:02}' for i in range(1,12)}
assert not re.search(r'turn\d+(?:view|search)|TODO|TBD|lorem',first+second,re.I)
for doc in [first,second]:
 assert '\ufffd' not in doc
 for line in doc.splitlines():assert line==line.rstrip(),line

coverage=[]
for source in original:
 sid=source['id']
 block=re.search(r'^## '+sid+r' .*?(?=^## S\d\d |\Z)',first,re.S|re.M).group(0)
 scope=block.splitlines()[2]
 coverage.append({'id':sid,'title':source['title'],'url':source['url'],'reading_scope':scope,'note_file':'01_source_readings.md','analysis_status':'原文の記述と派生する分析・追加の問いを記録。製品化や自社適合性の判断は未確定。'})

additional=[]
for aid in sorted(extra):
 block=re.search(r'^### '+aid+r' (.*?)(?=^### |^## |\Z)',second,re.S|re.M).group(0)
 url=re.search(r'\]\((https://[^)]+)\)',block).group(1)
 additional.append({'id':aid,'title':block.splitlines()[0][4:],'url':url,'reading_scope':'リンク先の公開本文を確認。A10は製造関連の該当頁。','note_file':'02_followup_investigations.md'})

registry={'date':'2026-10-21','status':'精読・追加調査の研究ノート。レポート・スライドの改訂版ではない。','original_sources':coverage,'additional_sources':additional,'corrections':[{'source':'S06','point':'共同提携のCustomer Zeroは日立の製造現場。'},{'source':'S09','point':'工場全体の計画最適化の記述は富士通側の発表A08に帰属させる。ファナック側の単独発表だけに全範囲を帰属させない。'},{'source':'S27','point':'MRO等の事業成長と、AI機能単独・サブスクリプション単独の収益を区別する。'},{'source':'S28,S29','point':'大型PDFは該当章・頁の確認範囲を明記。全編精読とは主張しない。'},{'source':'S31','point':'最大50%の低減は検証機の加振機試験の結果であり、全切削条件の実績へ拡張しない。'}],'private_cache':'.build/deep_reading_20261021。原文キャッシュとPDF画像は調査用であり公開成果物には含めない。'}
(DEST/'source_coverage.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

result={'original_source_count':len(ids),'additional_primary_source_count':len(extra),'notes':[{'file':p.name,'characters':len(p.read_text(encoding='utf-8')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in DEST.glob('*.md')],'checks':['S01-S40各1件','A01-A11各1件','出典URLと精読範囲を記録','本文と分析・未解決の問いを区別','ツール内部参照・仮置き文字列なし','文字化け・行末空白なし']}
(ROOT/'.build/deep_reading_20261021/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
