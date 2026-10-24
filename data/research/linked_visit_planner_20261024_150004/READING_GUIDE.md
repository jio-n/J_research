# 調査企業一覧：リンク追加版

2026-10-24作成。既存の `photo_visit_planner_20261024_074920` のExcelを読み込み、新しい出力先へ別保存。

- 企業名リンク82件。JIMTOF2026の企業別URLを、社名とブースで照合。複数ブースのHexagonを区別。
- AI・フィジカルAIのD/F/G列に96件。具体的な製品説明・メーカー発表・技術マニュアルを優先し、詳細が未確定の行はJIMTOF公式出展説明へ案内。
- ナベルの前回転記誤読をAIシートA33だけ訂正。着眼点・質問・優先記号・展示未確認・判読不能表示を保持。
- Excelは通常のセルハイパーリンク。1セル内の複数単語へ異なるURLは設定していない。

`link_plan.json`：元の7列データ・リンク先・掲載位置・訂正理由。`link_index.csv`：全リンクの対応。
`link_checks.json`：88 URLのHTTP結果・タイトル・転送先。企業リンクは本文の社名を照合。技術リンクは製品名と該当説明を確認。
`native_verification.json`：Excel保存後の178リンクと588セル、行高・列幅・背景色・フィルタ検証。
`package_verification.json`：固定表示・元ファイルSHA-256保持等。
`prepare_links.py` / `check_links.py` / `edit_workbook.mjs` / `add_and_verify_links.ps1` / `render_saved.mjs`：追加・確認処理。

ProPlanAIのRelease Highlightsは通常取得が403だったため、同社Nexusの公開技術マニュアルへ変更し、全リンク先のHTTP 200を確認。リンク先は出展確度や未公開の性能を追加認定する根拠ではない。豆蔵の自然言語ティーチングは関連研究として示し、三菱商事テクノスの今回展示と断定しない。

書式確認画像・取得本文は `_private/` にローカル保管し、GitHubへ公開しない。元画像・Web全文は公開しない。旧版ExcelはSHA-256が不変であることを確認。
