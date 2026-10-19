# 公式出展社マスター（確認日 2026-10-16）

## 説明本文付きCSV（現在の閲覧用）

`exhibitors_2024_with_details.csv` と `exhibitors_2026_with_details.csv` を参照する。従来の一覧行をすべて保持し、公式出展社詳細の説明を結合している。取得中は25件ごとに更新する。最新件数は `checkpoints/enriched_masters.json`。

2026-10-16 最終保存：詳細URL付きは2024年988/988行、2026年820/820行を取得。説明本文は943件／768件、「主な出展物」は887件／753件。全掲載1,281行／1,146行を保持。詳細URLなし293行／326行は別調査の残件。本文の原典未掲載は取得漏れと区別している。DMG森精機E8005の添付例にある技術・製品説明と段落改行の保持を確認。

- `exhibition_content`：出展社詳細の展示・技術の説明本文。要約で置き換えず、段落改行を保持。
- `main_exhibits`：「主な出展物」欄の本文。
- `detail_retrieval_status`：保存済み／原典に記載なし／未取得／詳細URLなしの区別。
- `detail_url`、`detail_checked_date`、`detail_evidence_locator`：原典URL、確認日、原典該当箇所。
- `detail_cache_path`：内部調査用の取得HTML。

UTF-8 BOM付きCSVで、改行を含むセルはCSV引用符で保存。Excel等では「折り返して全体を表示」を使うと読みやすい。空欄を「展示なし」「技術なし」と解釈しない。2026は出展者の展示予定の説明であり、実演済み・性能検証済みを意味しない。

以下の数値は初回の一覧収集時点の記録で、詳細の追加取得とは分けて保持する。

| 指標 | 2024 | 2026 |
|---|---:|---:|
| 全11区分の掲載行 | 1,281 | 1,146 |
| 企業名の空白除去による重複除去数 | 1,243 | 1,132 |
| 詳細URLあり | 988 | 820 |
| 詳細URLなし | 293 | 326 |
| 共同出展者記号 (*) | 163 | 129 |
| 内部出展者記号 (**) | 63 | 48 |
| 企業名・ブース欠損 | 0 | 0 |
| 展示内容本文取得 | 0 | 0 |

掲載行数と、企業名の重複除去数、主催者発表の出展者総数は別指標。全11区分（ア〜ワ、海外A-Z）を取得したが、展示内容の全件調査まで完了したことは意味しない。2024はAM Area表示の行も含む。

`exhibitors_2024.csv/json` と `exhibitors_2026.csv/json` は掲載行を削除せず保存。共同・内部出展は原典の記号を保存したが、親出展社を隣接順・同一ブースから推測せず未同定とした。詳細URLなしは原典リストにリンクがないことを表す。

`exhibitor_name_matches_2024_2026.csv/json` はNFKC、空白除去、casefoldだけで生成した候補。両年名称一致823、2024のみ419、2026のみ308。法人同一性、社名変更、表記揺れは未検証。各年の上表とこの名寄せ集計では正規化方法が異なる。展示内容は未取得につき比較不能とした。

検証は `checkpoints/exhibitor_validation.json` に保存。全22区分のHTML企業セル数とマスター行数は一致。原典の同名・同ブース候補重複は2024が2組、2026が1組あり、削除せず記録。

原ページキャッシュは `sources/2024_list_*.html`、`sources/2026_list_*.html`。公式利用条件も各年保存。robots.txtは404。キャッシュは内部調査用で、原典の文章・写真・画像の無断転載を許可するものではない。

## 再開

取得済みリストはキャッシュを再解析する。アクセス制限を検出した場合は止まり、同一URLの取得リトライ上限は2回。

```powershell
& 'C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/collect_exhibitors.py
& 'C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/compare_exhibitor_names.py
```

次工程はAX/DX候補の両年詳細URL・企業公式展示ページの取得、展示確度の分類、展示内容差分。公式発表総数との定義差を含めた照合、親出展社の明示関係確認も残る。

## 重点3社の詳細取得チェックポイント

追加取得：オークマ、ファナック、ヤマザキマザックの両年6詳細。`exhibitor_details_2024.csv/json`、`exhibitor_details_2026.csv/json` に各3件を保存。既存一覧マスターは上書きしていない。全6件で「主な出展物」の本文を抽出、取得失敗0。2026は公式掲載の展示予定であり、現地実演・性能・実用化の確認を意味しない。

この別マスターは `scripts/collect_exhibitor_details.py` で再開可能。キャッシュ済みHTMLは再取得しない。次のコマンドは残る詳細リンク付き1,802行（2024:985、2026:817）を対象とする。詳細リンクなし619行（2024:293、2026:326）は対象外のため、別途企業公式情報を調査する。

```powershell
& 'C:/Users/paulr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/collect_exhibitor_details.py --year 2024 2026
```

必要に応じて `--limit 50` で今回の未取得行処理数を制限できる。取得状況は `checkpoints/exhibitor_details.json` に逐次保存。`--company オークマ ファナック ヤマザキマザック` で対象企業を絞れる。
