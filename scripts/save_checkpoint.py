"""Save a compact, restartable first-delivery checkpoint."""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda file:json.loads((root/file).read_text(encoding='utf-8'))
masters=read('checkpoints/exhibitors.json')
details=read('checkpoints/exhibitor_details.json')
overview_path=root/'data/research/overview_v0/coverage.json'
overview=read('data/research/overview_v0/coverage.json') if overview_path.exists() else None
overview_complete=bool(overview and (root/'outputs/JIMTOF2026_事前共有_v0_全体俯瞰.pptx').exists())
status={
    'saved_at':datetime.now(timezone(timedelta(hours=9))).isoformat(),
    'canonical_spec':'JIMTOF2026_Codex_Project_Spec_v0.md',
    'canonical_spec_sha256':hashlib.sha256((root/'JIMTOF2026_Codex_Project_Spec_v0.md').read_bytes()).hexdigest(),
    'latest_presentation':'outputs/JIMTOF2026_事前共有_v0_r1.pptx',
    'presentation_status':'本編1枚・指定4項目の初期例示版（重点3社のみ）。業界全体の事前共有版は未完成。PPTX再読込・画像確認済み。PowerPointアプリでの開封は未確認',
    'listing':{year:{'rows':r['listing_rows'],'unique_names_whitespace_normalized':r['unique_company_names_exact_whitespace_normalized'],'groups':len(r['group_counts']),'missing_booth':r['missing_booth']} for year,r in masters['years'].items()},
    'official_announced_totals_reconciled':False,
    'detail_enrichment':{year:{'retrieved':r['cumulative_detail_records'],'linked_rows_remaining':r['all_master_linked_rows_remaining'],'rows_without_detail_url':r['master_rows_without_detail_links']} for year,r in details['years'].items()},
    'research':{'companies':3,'evidence':len(read('data/research/evidence_v0.json')),'claims':len(read('data/research/claims_v0.json')),'technology_items':len(read('data/research/technology_items_v0.json')),'research_themes':2,'scope':'重点3社の初期仮説。業界全体の横断分析と訪問先の選別は未完了'},
    'poc':{'html':'tools/iphone-poc/index.html','master_import':'data/exhibitors_2026.csv','candidate_import':'data/research/poc_candidates_v0.json','status':'実装と最小コード整合性確認のみ。iPhone実機・file://起動・保存・復元・写真音声・ZIP実機確認は未実施'},
    'remaining':[f"詳細リンク付き残り{sum(r['all_master_linked_rows_remaining'] for r in details['years'].values())}行。リンクなし{sum(r['master_rows_without_detail_links'] for r in details['years'].values())}行の企業公式資料調査",'共同・内部出展の親出展社同定。名称一致823候補の法人確認','公式公表総数と一覧の定義差照合','AX/DX候補の全母集団スクリーニング、年度差分の技術比較、仮説の裏付け','iPhone実機確認。サーバー化の方針変更は行っていない'],
    'reading_csvs':['data/exhibitors_2024_with_details.csv','data/exhibitors_2026_with_details.csv'],
    'next_command':details['next_all_details_command']+' --limit 100' if any(r['all_master_linked_rows_remaining'] for r in details['years'].values()) else "& 'C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/export_enriched_masters.py",
    'next_after_acquisition':'取得詳細からAX/DX候補を抽出し、公式資料で方式・制約・実用化実績を確認。既存PPTの6Claimと研究テーマ2件を更新する',
    'note':'一覧マスターは取得時点の原データとして保持。重点詳細・分析は別ファイル。取得済みキャッシュを再利用し、未取得を完了扱いにしない'
}
if overview_complete:
    status['latest_presentation']='outputs/JIMTOF2026_事前共有_v0_全体俯瞰.pptx'
    status['presentation_status']='事前共有PowerPoint v0完成（本編1枚・指定4項目）。最終PPTX再読込・全スライド画像確認済み。現地性能・実績検証と事前レビューは未実施。'
    status['research']=overview['semantic_review']
    status['research']['scope']='全2427掲載行を一次抽出。重点42社を横断整理、33社の両年説明を比較。候補345行は機械抽出であり採用率ではない。'
    status['supporting_report']='outputs/JIMTOF2026_v0_根拠と横断比較.html'
    status['comparison_csv']='data/research/overview_v0/company_comparison.csv'
    status['remaining']=['詳細URLなし619行の企業公式資料調査、原典説明不足・名称変更候補の補完','共同・内部出展の親出展社同定、公式公表総数との定義別照合','事前レビューで研究仮説・訪問先を確定。現地で適用限界・定量効果・受注／採用・市場規模根拠を確認','iPhone実機検証は未実施。']
    status['next_after_acquisition']='事前レビューと現地調査準備。優先13社の質問は data/research/overview_v0/visit_priority.csv。'
atlas_checkpoint=root/'checkpoints/technology_atlas_v1.json'
atlas_validation=root/'checkpoints/technology_atlas_v1_validation.json'
if atlas_checkpoint.exists() and atlas_validation.exists():
    atlas=read('checkpoints/technology_atlas_v1.json')
    validation=read('checkpoints/technology_atlas_v1_validation.json')
    if validation['status']=='passed':
        status['current_phase']='工程・具体タスク別の技術整理、事実カード、全体マップを作成。ユーザー合意により最終1枚への集約は後工程。'
        status['presentation_status']='過去の本編1枚はユーザーから具体性・大局観の不足を指摘済み。現行の最終版として扱わず、技術マップを基に再編集する。'
        status['previous_research']=status['research']
        status['research']={k:atlas[k] for k in ['reviewed_company_keys','fact_cards','task_categories','evidence_records','cards_by_delta','explicit_label_scan','card_comparison_scope']}
        status['research']['research_themes_status']='以前の3テーマは暫定へ戻す。技術配置と未解決部分の比較後に再選定。'
        status['supporting_report']='outputs/JIMTOF2026_技術整理と全体マップ_v1.html'
        status['technology_map']='outputs/JIMTOF2026_技術全体マップ_v1.svg'
        status['fact_cards_csv']='data/research/technology_atlas_v1/fact_cards.csv'
        status['comparison_csv']='data/research/technology_atlas_v1/task_comparison_2024_2026.csv'
        status['research_checkpoint']='checkpoints/technology_atlas_v1.json'
        status['remaining']=atlas['remaining']+['iPhone実機検証は未実施。']
        status['next_command']="& 'C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/validate_technology_atlas.py"
        status['next_after_acquisition']=atlas['next_action']
        if 'category_index' in atlas:
            status['research']['category_index']={k:atlas['category_index'][k] for k in ['categories','associations','companies','items','scope']}
            status['category_csv']='data/research/technology_atlas_v1/category_index.csv'
        if 'category_workbook_path' in atlas:
            status['category_workbook']=atlas['category_workbook_path']
            status['category_validation']=atlas['category_validation']
        if 'candidate_screening' in atlas:
            status['research']['candidate_screening']=atlas['candidate_screening']
            status['research']['visit_priorities']=atlas['visit_priorities']
            status['candidate_screening_csv']='data/research/technology_atlas_v1/candidate_screening.csv'
            status['category_visit_priorities_csv']='data/research/technology_atlas_v1/category_visit_priorities.csv'
            status['current_phase']='関連候補345掲載の一次仕分けと9カテゴリーの訪問優先37件・28社を保存。最終1枚への集約は未着手。'
        if 'priority_deepening' in atlas:
            status['research']['priority_deepening']=atlas['priority_deepening']
            status['priority_deepening_csv']='data/research/technology_atlas_v1/priority_deepening.csv'
            status['current_phase']='訪問優先28社・33展示のAIの判断・実行・人の関与・年度差分を深掘り。ExcelとHTMLを同一パスへ反映。1枚集約は未着手。'
        if 'cross_company_synthesis' in atlas:
            status['research']['cross_company_synthesis']=atlas['cross_company_synthesis']
            status['research']['research_themes_status']='研究候補5件を根拠・限定実験・評価指標・採否条件付きで保存。未採否の仮説。'
            status['current_phase']='28社・33カードを10方式・35配置、年度変化6パターン、共通課題5件・研究候補5件に横断整理。同じExcelとHTMLを更新。1枚集約は未着手。'
            status['method_map']='outputs/JIMTOF2026_方式別比較マップ_v1.svg'
            status['year_change_figure']='outputs/JIMTOF2026_年度変化比較図_v1.svg'
            status['research_candidates_csv']='data/research/technology_atlas_v1/research_candidates.csv'
        if 'remaining_followup' in atlas:
            status['research']['remaining_followup']=atlas['remaining_followup']
            status['current_phase']='10/18追補：根拠13件・10カード更新、社名変更1社を照合。研究候補5件の扱いと現地確認12論点を同じExcel・HTMLに保存。1枚集約は未着手。'
            status['open_questions_csv']='data/research/technology_atlas_v1/open_questions.csv'
            status['company_alias_confirmations']='data/research/technology_atlas_v1/company_alias_confirmations.csv'
(root/'checkpoints/status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(status,ensure_ascii=False,indent=2))
