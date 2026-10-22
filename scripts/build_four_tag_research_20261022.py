"""Compile item-level reviews and a traceable audit of the complete saved 2026 list.

Keyword screening only discovers records. Tag overrides and function notes are
researcher judgments. Retrieval logs never imply semantic verification.
"""
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/research/four_tag_20261022'
DATE = '2026-10-22'
TAGS = ['AI','フィジカルAI','自律化','自動化']

def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def norm(s): return re.sub(r'[\s・･,，.．()（）]','',unicodedata.normalize('NFKC',s)).replace('株式会社','').replace('合同会社','').lower()
def csvout(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

ROWS=list(csv.DictReader((ROOT/'data/exhibitors_2026_with_details.csv').open(encoding='utf-8-sig',newline='')))
BYID={r['exhibitor_record_id']:r for r in ROWS}
BYNAME=defaultdict(list)
for r in ROWS: BYNAME[norm(r['company_name'])].append(r)
FACTS=read('data/research/technology_atlas_v1/fact_cards.json')
DIRECTORY=read('data/research/report_v0/technology_directory.json')['entries']
DIR={x['card_id']:x for x in DIRECTORY}
DEEP={x['card_id']:x for x in read('data/research/technology_atlas_v1/priority_deepening.json')}
CASES={x['card_id']:x for x in read('data/research/report_v0/case_comparison.json')}
for x in CASES.values():
    if x.get('full_record',{}).get('deepening'): DEEP[x['card_id']]=x['full_record']['deepening']
EVIDENCE={x['evidence_id']:x for x in read('data/research/report_v0/evidence_ledger.json')}
REVIEWS={r['legacy_id']:r for r in csv.DictReader((OUT/'item_reviews.tsv').open(encoding='utf-8'),delimiter='\t')}
LINKS={r['record_id']:r for r in read('data/research/four_tag_20261022/company_links.json')}
ITEMS=[]
EXCLUDED={
 'FC026':'MESの一元管理・API連携は確認できるが、四タグに該当する個別の自動判断・実行機能を特定できない。',
 'FC066':'遠隔保守の支援は確認できるが、AI推論・自動診断・自動復旧の具体機能が不明。',
 'FC069':'減速機の用途にフィジカルAIを掲げるが、部品自体に知覚・判断・動作生成機能はない。',
 'AC018':'Automation Studioは回路設計・シミュレーション。製品名だけでは四タグの自動処理機能を特定できない。',
 'AC053':'FEM・CFD解析サービスとミスト捕集。AI推論・自動工程の具体記載なし。',
 'AC065':'ケーブル保護材。ロボットへの利用だけで作業自動化機能とは数えない。',
 'AC070':'生産情報の一元管理が中心。自動計画・AI・自律実行の具体機能は未確認。',
 'AC071':'無線振動センサのデータ基盤。AI診断・閉ループ実行機能は未確認。',
 'AC099':'受託積層造形・加工サンプル。今回の対象となる個別のAI・自動化機能は未確認。',
 'AC104':'標準工具データの提供基盤。データ連携だけでAI・自律判断とは数えない。',
 'AC106':'樹脂加工とIoT可視化。個別の自動判断・自動作業の説明が不足。',
 'AC121':'CTの可視化・解析。自動欠陥判定・自動搬送・AI方式の記載は未確認。',
 'AC166':'焦点確認・CAD位置合わせの操作支援。自動測定・自動補正の記載は未確認。',
 'AC168':'ロボット用減速機。利用先がロボットであることだけでは四タグの機能としない。',
 'AC180':'生産管理・コンサルティング。今回の四タグの具体的機能を特定できない。',
 'AC182':'ケーブル・保護管。ロボット向けの用途説明のみ。',
 'AC203':'クーラントポンプ・モータ。自動化に貢献するとの総論に対し個別の自動機能が不明。',
 'AC208':'配線の結束・保護材。展示品に自動結束装置の記載は確認できない。',
 'AC240':'制御盤・ITラック等の基盤。個別のAI処理・自動加工機能は未確認。',
 'AC258':'歯車設計・加工シミュレーション。AI・自動工程生成の具体機能は未確認。',
 'AC286':'3D SDK・形状変換基盤。今回の四タグの完成機能・AI学習機能は未確認。',
 'SUB001':'GibbsCAM2026の展示は確認できるが、今回確認した資料では自動化・AIの個別機能を特定できない。',
 'RPT005':'RBYは遠隔操作・教示の参考展示。自律実行・AI生成の機能を確認できない。計測ロボットは別候補AC148で扱う。',
}

# These sets reflect item-level source review, not inheritance of the old C01–C09 labels.
AI_FUNCTION=set('FC004 FC011 FC012 FC013 FC014 FC017 FC018 FC020 FC028 FC030 FC036 FC037 FC038 FC039 FC040 FC049 FC058 FC059 FC062 FC063 AC051 AC085 AC107 AC131 AC178 AC195 AC204 AC210 AC225 AC273'.split())
AI_LABEL=set('FC003 FC005 FC006 FC009 FC023 FC031 FC051 FC052 FC064 AC022 AC095 AC136 AC154 AC159 AC194 AC231 AC252'.split())
AI_SUPPORT=set('FC024 FC025 FC068 AC008 AC019'.split())
PA_FUNCTION=set('FC049 AC051 AC085'.split())
PA_LABEL=set('FC005 FC006 FC051 AC159'.split())
PA_SUPPORT=set('AC019 AC273'.split())
AUTO_LIMITED=set('FC033 FC034 FC054 RPT002 RPT006 RPT007 AC026 AC036 AC052 AC054 AC097 AC109 AC115 AC146 AC153 AC176 AC209 AC214 AC230 AC244 AC257 AC276 AC289'.split())
AUTO_MOBILE=set('FC001 FC031 AC039 AC041 AC090 AC186 AC287'.split())
COMPONENT=set('FC042 FC043 FC044 FC045 FC068 AC002 AC008 AC016 AC017 AC027 AC030 AC033 AC037 AC050 AC057 AC063 AC066 AC067 AC072 AC075 AC079 AC081 AC083 AC097 AC105 AC113 AC122 AC127 AC137 AC140 AC145 AC157 AC158 AC181 AC183 AC184 AC185 AC187 AC192 AC201 AC222 AC227 AC233 AC243 AC249 AC254 AC257 AC278 AC293'.split())
NO_AUTOMATION=set('FC003 FC004 FC009 FC017 FC025 FC052 FC058 FC062 FC064 AC019 AC022 AC136 AC231'.split())

def src(eid):
    e=EVIDENCE.get(eid,{})
    return {'source_id':eid,'publisher':e.get('publisher',''),'title':e.get('title',eid),'url':e.get('url',''),'locator':e.get('locator','該当製品・機能説明'),'checked_date':e.get('checked_date','2026-10-16'),'usage':'技術・出展根拠（既存調査）'}

def refs_for(x):
    refs=[src(e) for e in x.get('evidence_ids',[]) if EVIDENCE.get(e,{}).get('url')]
    for s in x.get('source_locations',[]):
        if s.get('url') and s['url'] not in [r['url'] for r in refs]:refs.append({'source_id':s.get('evidence_id',''),'title':'既存調査の一次資料','url':s['url'],'locator':s.get('locator',''),'checked_date':x.get('checked_date','2026-10-16'),'usage':'技術・出展根拠（既存調査）'})
    return refs

def listing_for(x):
    ids=[]
    if x.get('candidate_record_id') in BYID:ids.append(x['candidate_record_id'])
    for s in x.get('source_locations',[]):
        for r in ROWS:
            if r['detail_url'] and r['detail_url']==s.get('url') and r['exhibitor_record_id'] not in ids:ids.append(r['exhibitor_record_id'])
    for name in [x.get('company',''),DIR.get(x.get('card_id'),{}).get('company_key','')]:
        for r in BYNAME.get(norm(name),[]):
            if r['exhibitor_record_id'] not in ids:ids.append(r['exhibitor_record_id'])
    return ids

def task_for(text):
    rules=[('保全・異常診断',r'保全|診断|目詰|安全|消火|故障|潤滑|監視|停止'),('生産計画・運用',r'スケジュ|生産計画|MES|配車|見積|図面|購買|在庫|工具管理|キャビネット|floow'),('工程設計・プログラム生成',r'CAM|プログラ|工程設計|経路生成|ツイン|仮想|シミュレ|PLC|HMI|Copilot|CoAgent'),('検査・計測・補正',r'測定|計測|検査|画像|定寸|オフセット|センサ|校正|プリセット'),('周辺作業・環境管理',r'切粉|切り屑|切りくず|クーラント|洗浄|希釈|混合|液|フィルタ|ドレン|ミスト'),('工具・治具・段取り交換',r'工具交換|砥石交換|クランプ|チャック|把持|ハンド|治具|ATC|固定|ジョー|コレット'),('搬送・供給・工程接続',r'搬送|供給|パレット|ストッカ|AMR|ローダ|ATP|ロボット|自動ライン'),('加工・仕上げ制御',r'加工|研削|研磨|肉盛|溶接|面取り|転造|曲げ|成形|ねじ|バリ')]
    for name,pat in rules:
        if re.search(pat,text,re.I):return name
    return '装置・ソフトの自動処理'

NEEDS={
 '保全・異常診断':'故障・異常時の発見遅れ、停止時間と保全担当者の負担を減らす。',
 '生産計画・運用':'計画変更・情報探索・在庫管理に伴う手作業と属人性を減らす。',
 '工程設計・プログラム生成':'多品種の工程・制御プログラム準備時間と熟練者への依存を減らす。',
 '検査・計測・補正':'検査工数と判定のばらつきを抑え、加工・工具の品質を安定させる。',
 '周辺作業・環境管理':'切粉・液・清掃等の周辺作業による人手介入・チョコ停を減らす。',
 '工具・治具・段取り交換':'品種変更・工具摩耗に伴う交換と位置合わせの手作業を減らす。',
 '搬送・供給・工程接続':'ワーク受渡し・物流の人手と設備の供給待ち時間を減らす。',
 '加工・仕上げ制御':'加工・仕上げを連続化し、作業者の負担と品質のばらつきを減らす。',
 '装置・ソフトの自動処理':'定型操作の手作業を減らす。具体的な対象業務は現地で確認する。'}

def settag(x,t,status,reason):x['tags'][t]={'status':status,'reason':reason}
def build_old(x):
    cid=x['card_id'];d=DIR.get(cid,{}); rev=REVIEWS.get(cid);deep=DEEP.get(cid)
    item=rev['item'] if rev else x['item']
    method=rev['function_note'] if rev else x.get('mechanism',d.get('technology',''))
    xx={'id':cid,'legacy_ids':[cid],'company':x['company'],'listing_ids':listing_for(x),'booths':x.get('booths_2026',d.get('booths',[])),
        'item':item,'task':x.get('task',''),'need':x.get('customer_need',''),'method':method,'input':x.get('input',''),'output':x.get('output',''),
        'human':x.get('human_boundary',d.get('human_boundary','')),'limits':x.get('unresolved',''),'exhibit_note':x.get('exhibition_status',d.get('exhibition_status','')),
        'stage':x.get('product_stage',d.get('product_stage','')),'sources':refs_for(x),'tags':{t:{'status':'—','reason':'今回確認した資料では、このタグの個別機能を裏付けない。'} for t in TAGS},
        'depth':'公式出展説明の機能整理','new_review':False,'as_of':DATE,'baseline':d.get('year_change',x.get('delta_interpretation',''))}
    if rev:
        xx['task']=task_for(item+' '+method);xx['need']=NEEDS[xx['task']]
        xx['input']='詳細な入力仕様・取得信号は今回の出展説明では未特定。'
        xx['output']=method
        xx['human']='教示・段取り条件、運転開始、停止後の復帰を誰が行うかは未確認。'
        xx['limits']='個別モデル・設定条件・適用限界・人の残作業を未確認として残す。'
    if cid.startswith('FC'):xx['depth']='個別タスク・入出力整理'
    if deep:
        xx.update(input=deep.get('ai_input',xx['input']),method=deep.get('ai_judgment',xx['method']),output=deep.get('execution',xx['output']),human='／'.join(deep.get(k,'未確認') for k in ['human_preparation','human_approval','human_exception']),limits=deep.get('limits',xx['limits']),depth='企業・開発元の技術資料まで照合')
    # Directory comparison data for RPT006/007 has inherited unrelated fields. Use their source mechanism only.
    if cid in ['RPT006','RPT007']:
        xx.update(task=d['target'],need=NEEDS['検査・計測・補正'],input='RPT006'==cid and '温度・回転等の状態と加工後の測定結果。' or '加工中の振動情報。',method=d['technology'],output=d['target'],human=d['human_boundary'],limits='同機能・版の2026展示搭載は未確認。',depth='企業公式製品資料まで照合')
    if cid in AI_FUNCTION:settag(xx,'AI','機能記載',xx['method'])
    if cid in AI_LABEL:settag(xx,'AI','呼称・用途記載','AIの利用を訴求するが、対象モデル・学習方法・判断範囲の具体化が不足。'+xx['method'])
    if cid in AI_SUPPORT:settag(xx,'AI','関連基盤','AIへデータ・実行環境を供給する役割。単体でAI推論を実装するという意味ではない。'+xx['method'])
    if cid in PA_FUNCTION:settag(xx,'フィジカルAI','機能記載','AIによる認識・判断を物理的な作業へ接続する。'+xx['method'])
    if cid in PA_LABEL:settag(xx,'フィジカルAI','呼称・用途記載','生成AI・フィジカルAIを用いる制御を紹介。個別タスクの適応範囲は未確認。'+xx['method'])
    if cid in PA_SUPPORT:settag(xx,'フィジカルAI','関連基盤','学習データやロボット制御を支える開発基盤。実機の自律作業とは分ける。'+xx['method'])
    if cid in AUTO_LIMITED and cid not in ['AC097','AC244']:settag(xx,'自律化','限定機能','計測値・制約に応じた補正・計画変更を行う限定タスク。工場全体の完全自律性とは異なる。'+xx['method'])
    if cid in AUTO_MOBILE:settag(xx,'自律化','用途記載','AMR等の自律搬送を含むが、経路選択・障害物・再計画の担当範囲は要確認。'+xx['method'])
    if cid not in NO_AUTOMATION:
        settag(xx,'自動化','構成要素' if cid in COMPONENT else '機能記載',xx['method'])
    xx['exhibit']='展示未確認' if re.search('個別JIMTOF展示未確認|展示搭載は未確認|同機能の展示',xx['exhibit_note']) else '出展説明に掲載'
    if cid=='FC041':xx['exhibit']='動画・資料予定'
    if cid=='FC049':xx['exhibit']='参考出展予定';xx['stage']='参考出品・現地実証前'
    if xx['tags']['フィジカルAI']['status']=='関連基盤':xx['advance']='フィジカルAIの開発基盤'
    elif cid in PA_FUNCTION:xx['advance']='AI認識・物理動作の接続／方式の詳細は未公開'
    elif cid in PA_LABEL:xx['advance']='呼称・計画／適応能力は要確認'
    elif cid in AUTO_LIMITED:xx['advance']='計測フィードバック・最適化（AIとは別）'
    else:xx['advance']='個別技術の新規性・一般化能力は未評価'
    xx['check']=f"{xx['item']}の対象品種・変更条件は何か。{xx['task']}で人が設定する内容、異常時の停止・復帰、他工程との接続仕様を確認する。"
    xx['recommendation']='通常候補';xx['recommend_reason']='';xx['visit_group']=''
    for field in ['input','output','human','limits']:
        if not xx[field]:xx[field]='今回の資料では具体仕様を未確認。'
    return xx

for x in FACTS:
    if x['card_id'] not in EXCLUDED: ITEMS.append(build_old(x))
for d in DIRECTORY:
    if d['card_id'] not in {x['card_id'] for x in FACTS} and d['card_id'] not in EXCLUDED:
        fake=CASES.get(d['card_id'],{}).get('full_record',{})
        fake={**d,**fake,'card_id':d['card_id'],'company':d['company'],'item':d['item'],'booths_2026':d['booths'],'mechanism':d['technology'],'task':d['target'],'customer_need':d['need'],'source_locations':[{'url':u,'evidence_id':''} for u in d['source_urls']]}
        ITEMS.append(build_old(fake))

# Merge exact repeated items of the same company; preserve group distributors as separate visit choices.
MERGE={'AC082':'RPT001','AC115':'RPT002','AC217':'AC216'}
for old,new in MERGE.items():
    a=next(x for x in ITEMS if x['id']==old);b=next(x for x in ITEMS if x['id']==new)
    for field in ['listing_ids','booths','legacy_ids']:b[field]=list(dict.fromkeys(b[field]+a[field]))
    b['sources']+= [s for s in a['sources'] if s['url'] not in {z['url'] for z in b['sources']}]
    ITEMS.remove(a)

for rr in csv.DictReader((OUT/'additional_listing_reviews.tsv').open(encoding='utf-8'),delimiter='\t'):
    r=ROWS[int(rr['row_index'])];cid='N'+rr['row_index'].zfill(4)
    fake={'card_id':cid,'company':r['company_name'],'item':rr['item'],'booths_2026':[r['booth']],'task':task_for(rr['item']+' '+rr['function_note']),'customer_need':'','mechanism':rr['function_note'],'input':'詳細な入力仕様・取得信号は今回の出展説明では未特定。','output':rr['function_note'],'human_boundary':'段取り設定・停止復帰と自動化範囲の境界は要確認。','exhibition_status':'公式出展説明に機能を記載。現地未確認。','product_stage':'出展説明掲載・提供段階は個別確認','candidate_record_id':r['exhibitor_record_id'],'source_locations':[{'url':r['detail_url'],'evidence_id':'LIST-'+r['exhibitor_record_id'],'locator':'公式出展紹介・主な出展物'}]}
    x=build_old(fake);x['need']=NEEDS[x['task']];x['new_review']=True
    for t in TAGS:x['tags'][t]={'status':'機能記載','reason':rr['function_note']} if t in rr['tags'].split(',') else {'status':'—','reason':'今回確認した出展説明では当該機能を裏付けない。'}
    if int(rr['row_index']) in [176,180,703,790,915,933,936,1043]:x['tags']['自動化']['status']='構成要素'
    if x['tags']['自律化']['status']!='—':x['tags']['自律化']['status']='限定機能';x['advance']='計測フィードバック（AI方式の説明なし）'
    ITEMS.append(x)

# New, source-reviewed products and updates are maintained separately from the full-list screening.
from four_tag_curated_20261022 import enrich
enrich(ITEMS,ROWS,DATE,TAGS)

for x in ITEMS:
    x['listing_ids']=list(dict.fromkeys(x['listing_ids']))
    if not x['listing_ids']:
        x['listing_ids']=[r['exhibitor_record_id'] for r in ROWS if norm(r['company_name'])==norm(x['company'])]
    x['booths']=list(dict.fromkeys(x['booths']))
    x['company_sites']=list(dict.fromkeys(u for rid in x['listing_ids'] for u in LINKS.get(rid,{}).get('company_urls',[])))
    x['source_ids']=[s['source_id'] for s in x['sources']]
    x['source_urls']=list(dict.fromkeys(s['url'] for s in x['sources'] if s.get('url')))
    x['tag_names']=[t for t in TAGS if x['tags'][t]['status']!='—']
    non_reasons={'AI':'このアイテムで学習モデル・生成AIが担当する具体的な入力・推論を今回確認できない。','フィジカルAI':'AIの判断を物理作業の手順・動作・制御の生成または変更へ接続する説明を今回確認できない。','自律化':'状態変化に対する判断・補正・再計画をシステム側が行う説明を今回確認できない。所定動作の自動実行とは分ける。','自動化':'自動処理・作業の範囲を特定できない。AI支援・情報提示だけから自動実行を推定しない。'}
    for t in TAGS:
        if x['tags'][t]['status']=='—':x['tags'][t]['reason']=non_reasons[t]
    assert x['tag_names'],x['id']
    assert x['listing_ids'],('Not linked to master',x['id'],x['company'])
    assert x['source_urls'],x['id']

screened=read('data/research/technology_atlas_v1/candidate_screening.json')
OLDSCREEN={x['record_id']:x for x in screened}
EXCLUDED_ROWS={}
for x in FACTS:
    if x['card_id'] in EXCLUDED:
        for rid in listing_for(x):EXCLUDED_ROWS[rid]=EXCLUDED[x['card_id']]
itemmap=defaultdict(list)
for x in ITEMS:
    for rid in x['listing_ids']:itemmap[rid].append(x)

audit=[]
for i,r in enumerate(ROWS):
    rid=r['exhibitor_record_id'];text=r['exhibition_content']+'\n'+r['main_exhibits'];related=itemmap[rid]
    if related: status='候補あり';reason='／'.join(f"{x['id']}：{x['item']}" for x in related)
    elif not text.strip():status='情報不足';reason='元の公式一覧に出展紹介・主な出展物の本文がない。非該当とは判定しない。企業サイトでの個別確認が必要。'
    elif rid in EXCLUDED_ROWS:status='対象外（機能未特定）';reason=EXCLUDED_ROWS[rid]
    elif rid in OLDSCREEN:status='対象外（既存判定照合）';reason=OLDSCREEN[rid].get('reason','四タグの具体的機能を確認できない。')
    else:
        status='未抽出（公開説明ベース）'
        if re.search('自動車|ロボット|AI|半導体',text,re.I):reason='用途・需要先の記載と、製品が持つAI・自動作業機能を区別。今回の公開説明から具体的な対象機能を抽出できない。'
        else:reason='今回保存された公開説明と機能語の再走査では対象機能を特定できない。企業の全製品が非該当という意味ではない。'
    # An official event page can give a reason to monitor a major company even without an eligible named item.
    if rid not in itemmap and norm(r['company_name'])==norm('株式会社不二越'):
        reason+=' 10/19公式発表はE3009の新型歯車加工機・自動化を予告するが、ロボット実演・AI機能の型式は未特定。'
    audit.append({'row_no':i+1,'record_id':rid,'company':r['company_name'],'booth':r['booth'],'status':status,'reason':reason,'item_ids':[x['id'] for x in related],
                  'tag_names':list(dict.fromkeys(t for x in related for t in x['tag_names'])),'detail_url':r['detail_url'],'company_urls':LINKS.get(rid,{}).get('company_urls',[]),'original_checked_date':r['detail_checked_date'] or r['checked_date'],'description_available':bool(text.strip())})

ITEMS.sort(key=lambda x:({'優先訪問':0,'比較訪問':1,'事前確認':2,'通常候補':3}.get(x['recommendation'],4),norm(x['company']),x['id']))
stats={'master_rows':len(ROWS),'master_companies':len({norm(x['company_name']) for x in ROWS}),'description_rows':sum(bool((r['exhibition_content']+r['main_exhibits']).strip()) for r in ROWS),'candidate_items':len(ITEMS),'candidate_companies':len({norm(x['company']) for x in ITEMS}),'linked_master_rows':sum(x['status']=='候補あり' for x in audit),'audit_status':dict(Counter(x['status'] for x in audit)),'tag_counts':{t:dict(Counter(x['tags'][t]['status'] for x in ITEMS if x['tags'][t]['status']!='—')) for t in TAGS},'depth_counts':dict(Counter(x['depth'] for x in ITEMS))}
logs=[]
for f in ['home_retrieval_log.json','linked_retrieval_log.json','extra_retrieval_log.json']:logs+=read('data/research/four_tag_20261022/'+f)
stats['retrieval_unique_urls']=len({x['url'] for x in logs});stats['retrieval_body_success_unique']=len({x['url'] for x in logs if x['status']=='本文取得'})
definitions=[
 {'tag':'AI','definition':'機械学習・生成AI等による認識、推定、生成、判断支援。単なる数式・ルール・画像処理をAIと推定しない。','boundary':'AIを使う完成機能／メーカー呼称／学習・データ基盤を別表示。'},
 {'tag':'フィジカルAI','definition':'AIが現実の状態や作業指示を認識・解釈し、作業手順・動作・制御を生成または変更して物理作業へ接続する技術。','boundary':'調査上の作業定義。固定設置でも該当しうる。VLA等の新規性、可変条件、人承認、安全性は別に検証。'},
 {'tag':'自律化','definition':'状態・計測・制約を受けて、限定タスクの判断・補正・再計画をシステム側で行うもの。','boundary':'AMR搬送・閉ループ補正を含む。人承認付きの判断支援、呼称のみ、工場全体の完全自律化と区別。'},
 {'tag':'自動化','definition':'所定の作業・処理・搬送・計測・交換を機械やソフトで行うもの。','boundary':'従来型自動化も含む。自動動作を直接構成するハンド・クランプ等は構成要素として表示。単にロボットに使う材料・軸受・配線材は除外。'}]
limitations=[
 '視察前の事前調査。展示予定は公開資料の記載であり、当日の実機・稼働・性能の確認ではない。',
 '母集団は保存済み2026年公式一覧1,146掲載行。出展説明は主に10月16日取得、追加の企業資料は10月22日確認。主催者の最新一覧との差分を完全保証するものではない。',
 '同じ会社の複数小間・共同出展を残す。掲載行数、企業数、アイテム数は異なる。代理店とメーカーの同一製品も別の訪問候補として残る。',
 '全件の機能探索と、重点候補の企業技術資料照合を区別した。企業サイトの取得ログは取得の記録であり、全ページの精読済みを意味しない。',
 '全候補に個別機能メモと四タグの理由を持たせたが、方式・入力・学習・例外復帰まで確認できた候補と出展説明に留まる候補では調査深度が異なる。',
 '「未抽出」「情報不足」は非該当の断定ではない。一般的なCNC運動、単なるDX可視化・シミュレーション、ロボット用材料だけでは機能を推定しない。',
 '顧客ニーズ・訪問推奨・技術分類・確認質問は調査者の分析。性能値・省人工数・市場採用率を独立に実証したものではない。',
 '四タグは重複可。タグ集計には呼称・計画・関連基盤も含み、技術採用率・先端技術の普及率を表さない。']
majors=[]
for m in read('data/research/macro_20261019/major_dossiers.json'):
    rr=[r for r in audit if norm(r['company'])==norm(m['company'])]
    ids=list(dict.fromkeys(cid for r in rr for cid in r['item_ids']))
    majors.append({'company':m['company'],'booths':m['booths'],'item_ids':ids,'status':'候補あり' if ids else '対象機能の追加確認が必要','note':'個別候補の四タグ・展示確度を参照。' if ids else '主要企業として確認対象に残す。型式・AI／自動化機能を推定して候補化しない。','urls':[r['detail_url'] for r in rr if r['detail_url']]})
result={'title':'JIMTOF2026 四タグ別・訪問候補総覧','as_of':DATE,'stats':stats,'definitions':definitions,'limitations':limitations,'items':ITEMS,'audit':audit,'majors':majors}
write(OUT/'research.json',result)
csvout('candidate_items.csv',[{'item_id':x['id'],'company':x['company'],'item':x['item'],'booths':' / '.join(x['booths']),**{t:x['tags'][t]['status'] for t in TAGS},'task':x['task'],'need_analysis':x['need'],'method':x['method'],'input':x['input'],'output':x['output'],'human_boundary':x['human'],'limits':x['limits'],'exhibition_certainty':x['exhibit'],'exhibition_note':x['exhibit_note'],'advancement':x['advance'],'research_depth':x['depth'],'recommendation':x['recommendation'],'recommend_reason':x['recommend_reason'],'visit_check':x['check'],'master_record_ids':' / '.join(x['listing_ids']),'source_urls':'\n'.join(x['source_urls'])} for x in ITEMS])
csvout('tag_reasons.csv',[{'item_id':x['id'],'company':x['company'],'item':x['item'],'tag':t,'status':x['tags'][t]['status'],'reason':x['tags'][t]['reason'],'source_urls':'\n'.join(x['source_urls'])} for x in ITEMS for t in TAGS])
csvout('recommended_visits.csv',[{'item_id':x['id'],'company':x['company'],'booths':' / '.join(x['booths']),'item':x['item'],'visit_group':x['visit_group'],'recommendation':x['recommendation'],'recommend_reason':x['recommend_reason'],'exhibition_certainty':x['exhibit'],'check_at_booth':x['check'],'source_urls':'\n'.join(x['source_urls'])} for x in ITEMS if x['recommendation']!='通常候補'])
csvout('all_exhibitor_audit.csv',[{**x,'item_ids':' / '.join(x['item_ids']),'tag_names':' / '.join(x['tag_names']),'company_urls':' / '.join(x['company_urls'])} for x in audit])
print(json.dumps(stats,ensure_ascii=False,indent=2))
