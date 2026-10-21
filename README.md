# JIMTOF2026 調査資料

AI・自動化・AX／DXを中心に、公式出展者情報、企業公式発表、公開記事を整理した事前調査です。2024年との比較、マクロ動向、大手企業を含む注目展示、訪問候補を収録しています。

公開スナップショット：2026年10月19日。出展者CSVの収集基準日は2026年10月16日。レポートの追加Web確認は2026年10月19日です。

## 40資料の精読と追加調査（2026年10月21日）

記事の個別分析を省いて分類・要約へ進んだ点を見直し、元の40資料へ戻って、具体的な表現、技術・データ・事業の関係、次に調べる問いを記録しました。物理モデルの作成・校正、熟練者の判断の記録、継続サービスの価値、工場全体の計画と実行を、追加の一次資料11件まで追っています。

- [S01～S40の個別精読ノート](data/research/deep_reading_20261021/01_source_readings.md)
- [論点から追った追加調査](data/research/deep_reading_20261021/02_followup_investigations.md)
- [出典・確認範囲・修正点](data/research/deep_reading_20261021/source_coverage.json)

研究を深めるためのノートです。大きなPDFは確認した章・頁を明記し、計画・実証・製品の説明と分析を区別しています。既存HTML・Word・PowerPointは、この精読結果を反映した改訂版にはまだ置き換えていません。原文キャッシュやPDF画像は再配布していません。

## 視察前の説明用PowerPoint（2026年10月21日）

[PowerPointをダウンロード](outputs/strategy_briefing_20261021/JIMTOF2026_事前調査報告_主張3枚と補足17枚_r2.pptx)。**主張3枚＋根拠・比較の補足17枚、合計20枚**です。冒頭は、工程間の判断・実行へ広がる競争、使えるデータと顧客適応・検証という開発候補、協業と顧客成果による開発範囲の判断を伝えます。後半には主要3社の戦略比較、少量データの開発例、技術の役割、主要33社、訪問時の問いを収録しました。

展示会前の公開情報に基づく報告です。現地観察や顧客導入を確認した報告とは区別し、開発提案は仮説として明示しています。出典URL・該当箇所・確認範囲は各スライドのノートへ記載しています。比較表17点とグラフ1点は編集可能です。

- [短い要約テキスト](outputs/JIMTOF2026_戦略レビュー要約_20261021.txt)
- [スライド構成](data/research/strategy_briefing_20261021/slide_index.json) / [スライド本文と出典ノート](data/research/strategy_briefing_20261021/slide_content.json)
- [入力と成果物の対応・ハッシュ](data/research/strategy_briefing_20261021/presentation_basis.json) / [生成スクリプト](scripts/build_strategy_briefing_20261021.mjs)

## 潮流・技術の役割・開発候補のレビュー（2026年10月21日）

[レビューHTML](outputs/JIMTOF2026_潮流と開発候補レビュー_20261021.html) に、5つの潮流仮説、既存344技術の工程×役割マップ、6つの顧客向け開発候補、判断につながる現地質問をまとめました。既存34資料へ6資料を加え、因果の根拠・反例・成立条件を区別しています。全出展者2,427行を照合範囲に残し、技術台帳への配置状況と情報不足を分けました。主要33社の確認表も含みます。

- [潮流の因果と根拠CSV](data/research/strategy_review_20261021/hypothesis_evidence_links.csv)
- [技術の役割CSV](data/research/strategy_review_20261021/technology_role_map.csv) / [工程間の接点CSV](data/research/strategy_review_20261021/process_interfaces.csv)
- [開発候補CSV](data/research/strategy_review_20261021/development_candidates.csv) / [現地質問CSV](data/research/strategy_review_20261021/fieldwork_questions.csv)
- [全出展者の照合CSV](data/research/strategy_review_20261021/exhibitor_coverage_all_2024_2026.csv) / [同名538件の文言比較](data/research/strategy_review_20261021/macro_wording_signals.csv)
- [レビュー全体JSON](data/research/strategy_review_20261021/strategy_review.json) / [出典索引](data/research/strategy_review_20261021/evidence_index.csv) / [入力ハッシュ・方法](data/research/strategy_review_20261021/provenance.json) / [検証記録](data/research/strategy_review_20261021/validation.json)

技術分類は確認深度が異なり、詳細比較57件・個別タスク整理33件・出展説明の一次分類254件です。分類の空欄は技術や企業の不在を意味しません。自社能力・顧客の支払意思は未確認のため、開発候補は条件付きの分析仮説です。これは最終レポートの再編集前に議論するレビュー版で、既存Word・PowerPointの内容を今回の仮説で上書きしていません。

HTMLはダウンロードして開いてください。単一HTMLで検索・絞り込みを使えます。CSVへの相対リンクも使う場合はリポジトリのフォルダ構成を保持してください。構造・参照関係・検索と28マスの絞り込みを検証済み。ブラウザ描画による外観確認は未実施です。

再生成：`python scripts/compile_strategy_review_20261021.py`（標準ライブラリ）。内容は `review_content.json`、既存の技術分類、キーワード台帳、両年度の出展者CSVを入力にします。検証記録は再生成時に自動更新されません。

## 戦略・潮流のキーワード追加調査（2026年10月21日）

[キーワード探索HTML](outputs/JIMTOF2026_戦略キーワード探索_20261021.html) に、顧客ニーズ、現象に基づくデータ取得、顧客固有モデル、工程間連携、継続サービス等の28語群と出典を整理しました。[機械可読データ](data/research/strategy_keywords_20261021/strategy_keywords.json) と [出典台帳](data/research/strategy_keywords_20261021/sources.json) も保存しています。34資料のうち29資料は本文の該当節または公表要旨、5資料は検索結果の本文抽出のみの確認です。複数ページの同一インタビューは1資料として数えています。開発提言を確定する前の探索資料であり、全出展者集計に代わる母集団調査ではありません。

## 最初に読む資料

- [HTML：検索・絞り込みを使い、マクロ動向から企業・ブースを探す](outputs/AI_AX_DX_20261019/JIMTOF2026_AI_AX_DX_%E8%AA%BF%E6%9F%BB%E3%82%AC%E3%82%A4%E3%83%89.html)
- [Word：章立てで調査方法、動向、企業比較、訪問計画を読む](outputs/AI_AX_DX_20261019/JIMTOF2026_AI_AX_DX_%E8%AA%BF%E6%9F%BB%E5%A0%B1%E5%91%8A%E6%9B%B8.docx)
- [PowerPoint：視察前の説明と優先順位の共有に使う](outputs/AI_AX_DX_20261019/JIMTOF2026_AI_AX_DX_%E8%A6%96%E5%AF%9F%E3%83%96%E3%83%AA%E3%83%BC%E3%83%95%E3%82%A3%E3%83%B3%E3%82%B0.pptx)

3形式は用途に合わせて編集しており、同じ本文の単純な変換ではありません。大手を含む33社の比較、優先訪問19件、回遊案を含みます。

## その他のローカル成果物

元のファイル名・フォルダ構成を保持しています。`v0`、`r1`などは過去版として残しています。内容や調査範囲が異なるため、すべてを同一時点・同一深度の分析とは扱わないでください。

- [JIMTOF2026_v0_根拠と横断比較.html](outputs/JIMTOF2026_v0_%E6%A0%B9%E6%8B%A0%E3%81%A8%E6%A8%AA%E6%96%AD%E6%AF%94%E8%BC%83.html)
- [JIMTOF2026_カテゴリー別出展索引_v1.xlsx](outputs/JIMTOF2026_%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA%E3%83%BC%E5%88%A5%E5%87%BA%E5%B1%95%E7%B4%A2%E5%BC%95_v1.xlsx)
- [JIMTOF2026_事前共有_v0.pptx](outputs/JIMTOF2026_%E4%BA%8B%E5%89%8D%E5%85%B1%E6%9C%89_v0.pptx)
- [JIMTOF2026_事前共有_v0_r1.pptx](outputs/JIMTOF2026_%E4%BA%8B%E5%89%8D%E5%85%B1%E6%9C%89_v0_r1.pptx)
- [JIMTOF2026_事前共有_v0_全体俯瞰.pptx](outputs/JIMTOF2026_%E4%BA%8B%E5%89%8D%E5%85%B1%E6%9C%89_v0_%E5%85%A8%E4%BD%93%E4%BF%AF%E7%9E%B0.pptx)
- [JIMTOF2026_技術別補足と分野別まとめ_v0.pptx](outputs/JIMTOF2026_%E6%8A%80%E8%A1%93%E5%88%A5%E8%A3%9C%E8%B6%B3%E3%81%A8%E5%88%86%E9%87%8E%E5%88%A5%E3%81%BE%E3%81%A8%E3%82%81_v0.pptx)
- [JIMTOF2026_技術動向レポート_20261019.docx](outputs/JIMTOF2026_%E6%8A%80%E8%A1%93%E5%8B%95%E5%90%91%E3%83%AC%E3%83%9D%E3%83%BC%E3%83%88_20261019.docx)
- [JIMTOF2026_技術動向レポート_20261019.html](outputs/JIMTOF2026_%E6%8A%80%E8%A1%93%E5%8B%95%E5%90%91%E3%83%AC%E3%83%9D%E3%83%BC%E3%83%88_20261019.html)
- [JIMTOF2026_技術動向レポート_20261019.pptx](outputs/JIMTOF2026_%E6%8A%80%E8%A1%93%E5%8B%95%E5%90%91%E3%83%AC%E3%83%9D%E3%83%BC%E3%83%88_20261019.pptx)
- [JIMTOF2026_技術整理と全体マップ_v1.html](outputs/JIMTOF2026_%E6%8A%80%E8%A1%93%E6%95%B4%E7%90%86%E3%81%A8%E5%85%A8%E4%BD%93%E3%83%9E%E3%83%83%E3%83%97_v1.html)

図版のPNG・SVGも `outputs/` に保存しています。HTMLはダウンロードしてブラウザで開いてください。GitHub上のファイル表示ではHTMLの操作画面は実行されません。Word、PowerPoint、Excelはファイルをダウンロードして利用できます。

## 調査の土台となるCSV

| データ | 内容 |
|---|---|
| [2024年・説明付き全掲載CSV](data/exhibitors_2024_with_details.csv) | 1,281掲載行。企業名、ブース、説明、原典URL、取得状況 |
| [2026年・説明付き全掲載CSV](data/exhibitors_2026_with_details.csv) | 1,146掲載行。同じ列構成で比較可能 |
| [2024年一覧](data/exhibitors_2024.csv) / [2026年一覧](data/exhibitors_2026.csv) | 公式一覧からの掲載行。共同・内部出展の記号を保持 |
| [2024年詳細](data/exhibitor_details_2024.csv) / [2026年詳細](data/exhibitor_details_2026.csv) | 説明・主な出展物の取得結果 |
| [両年の名称対応候補](data/exhibitor_name_matches_2024_2026.csv) | 名称の正規化による照合。法人同一性の確定ではない |
| [収集時の説明](data/EXHIBITOR_MASTER_README.md) | 列の意味、取得範囲、履歴。過去時点の記述も含む |

CSVはUTF-8 BOM付きです。説明文のセルには改行が含まれるため、行数はCSVパーサーで数えてください。Excelではセルの折り返し表示が便利です。

## マクロ集計と出典をたどる

- [全件集計・分類規則・入力ハッシュ](data/research/macro_20261019/census.json)
- [全名称キーの分類監査CSV](data/research/macro_20261019/census_audit.csv)
- [AI表記86件の文脈確認CSV](data/research/macro_20261019/ai_context_review.csv)
- [レポートの編集データ・出典](data/research/macro_20261019/report_content.json)
- [技術別の出典台帳](data/research/technology_atlas_v1/evidence_ledger.csv)
- [技術・企業の比較カード](data/research/technology_atlas_v1/fact_cards.csv)
- [タスク別の年度比較](data/research/technology_atlas_v1/task_comparison_2024_2026.csv)

`data/research/` の各サブフォルダには、他の成果物の基礎データや過去の分析も保存しています。集計時点・母集団・分類規則が異なるデータは、件数を直接合算しないでください。

## 集計の読み方

任意の数十社を母集団にせず、両年の全2,427掲載行を処理しています。NFKC・空白除去・casefoldによる名称キーは2024年1,242、2026年1,131。説明文を利用できた名称キーは933、800で、両年に説明がある同名パネルは538です。

- 語の明示件数は、導入率、市場シェア、実装成熟度を示しません。分類は重複します。
- AI表記の文脈は別途確認しています。AI/AO入出力、加工先市場、翻訳などをそのままAI実装の証拠には扱いません。
- 説明欠損は技術の不在を意味しません。説明量・展示対象・社名表記の年度差が残ります。
- 2026年の出展説明は展示予定です。実演、性能、成功率、顧客導入を確認済みとはしません。
- 過去版の「空白除去だけ」の名称件数と、今回のNFKCを含む名称件数は定義が異なります。

## 再集計とファイル確認

Python標準ライブラリだけで、マクロ集計を再実行できます。

```sh
python scripts/analyze_macro_20261019.py
```

入力は両年の `exhibitors_*_with_details.csv`、出力は `data/research/macro_20261019/` です。集計結果・監査CSVなどを再生成するので、元のスナップショットを残す場合はコピー先で実行してください。

その他の `scripts/` は収集・各版の生成に使った作業ソースです。追加パッケージ、元ページのキャッシュ、フォント、専用ランタイムが必要なものがあり、このリポジトリだけで全成果物を一括再生成する環境は同梱していません。

[MANIFEST.csv](MANIFEST.csv) に掲載ファイルのサイズ・SHA-256・Git blob SHA-1・CSVデータ行数を記録しています。マニフェスト自身と、この公開用README・設定ファイルは対象外です。

公開時には全OfficeファイルのZIP構造を検査し、元ファイルとのハッシュ一致を確認しています。今回作成したAI／AX／DX版のWord・PowerPointは全ページの表示を確認済み。HTMLは検索処理を検証しましたが、ブラウザでの表示確認には環境上の制約がありました。他セッションで作成された過去成果物は今回再編集していません。

取得ページのHTMLキャッシュ、Officeのロックファイル、内部レンダリング、一時生成物、認証情報は掲載対象外です。データ内の `sources/` や `.build/` 参照はローカル調査時の追跡情報で、参照先ファイルを同梱しているとは限りません。公開原典はURLから確認してください。

## 出典・権利

原典はJIMTOF公式サイト、各社公式発表、公開記事です。出典URL・確認日・証拠箇所は各データとレポートに記録しています。企業名、製品名、原典の説明文・図版等の権利はそれぞれの権利者に帰属します。このリポジトリの公開は、第三者の原典について再利用許諾を付与するものではありません。

## 仕様書・調査チェックポイント・記録PoC

- [プロジェクト仕様書（正本）](JIMTOF2026_Codex_Project_Spec_v0.md)：目的、根拠の管理、現地調査、運用指針。後続のユーザー指示に基づく別編集レポートも掲載しています。
- [チェックポイント](checkpoints/)：取得・分析の各段階の件数、残件、成果物。日付付きの記録を参照し、`status.json` 単独を全成果物の最新状態とはみなさないでください。
- [iPhone記録HTMLのPoC](tools/iphone-poc/README.md)：ローカルHTMLの試作。保存・復元・録音などの実機確認状況は同READMEを参照してください。
- [原典キャッシュの一覧と扱い](sources/README.md)：手元に残した1,879ファイルの相対パス・サイズ・SHA-256。元ページの全文キャッシュは公開していません。原典URLはエビデンス台帳からたどれます。

`MANIFEST.csv` は先行公開分の一覧です。この節で追加した仕様書・チェックポイント・PoC・キャッシュ一覧は、同マニフェストの対象に含まれません。
