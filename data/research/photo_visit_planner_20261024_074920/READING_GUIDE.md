# 写真からのユーザー選定一覧（2026-10-24）

成果物：`outputs/photo_visit_planner_20261024_074920/JIMTOF2026_ユーザー選定_調査企業一覧.xlsx`

写真のユーザーコメントを保持する転記作業。過去の調査分析を混ぜず、技術・展示・ブースの訂正や新規質問生成は行わない。既存成果物は変更せず、新規2ディレクトリのみ追加。

- `transcription.json`：7列の値と写真番号。AI32アイテム・21社、自動化50社。
- `ai_physical_ai.csv` / `automation_50.csv`：Excelと同じ列順。
- `unreadable.json`：判読できない4セルの位置・写真番号。
- `transcribe.py`：目視による転記内容・重複整理。
- `build_workbook.mjs`：Artifact Toolによる新規Excel作成。
- `finalize_and_verify.ps1`：Excelの折り返し・固定表示・フィルタと入力検証。
- `verify_package.py`：保存XLSXの588セルと構造化データを照合。
- `render_saved.mjs`：保存XLSXを再読込し7範囲を画像化。
- `*_verification.json`：実施した検証結果。
- `manifest.json`：公開ファイルのSHA-256。

元画像はユーザー添付。AI側の添付IDはEF52C7EA-AF24-4E37-BE81-73F369795A57（写真1〜10）、自動化側は4A5BE852-0E67-4B29-B649-A94BDF48C7F9（訂正版写真1〜5）。写真間の重複を統合した。青字のリンク先URLは不可視のため推測しない。原文の空白・改行・箇条書き体裁は整理した。

`_private/`は元写真の拡大画像・操作試験コピー・依存ライブラリ接続を含むローカル検証領域。GitHubへ公開しない。再生成はユーザー環境のNode/PythonとArtifact Tool、Microsoft Excelが必要。
