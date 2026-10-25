$ErrorActionPreference='Stop'
$root='C:\Users\paulr\resarch\JIMTOF2026_Research'
$out=Join-Path $root 'outputs\integrated_review_20261026_013801'
$checks=[System.Collections.Generic.List[string]]::new()
$excel=New-Object -ComObject Excel.Application
$excel.Visible=$false
$excel.DisplayAlerts=$false
try {
 $book=$excel.Workbooks.Open((Join-Path $out 'JIMTOF2026_訪問先一覧_コメント統合・企業別閲覧.xlsx'),0,$false)
 try {
  $sheet=$book.Worksheets.Item('自動化・自律化50社');$table=$sheet.ListObjects.Item(1)
  $table.Range.AutoFilter(4,'訪問候補') | Out-Null
  $count=$excel.WorksheetFunction.Subtotal(103,$sheet.Range('A2:A60'))
  if($count -ne 1){throw "Visit filter count: $count"}
  $table.AutoFilter.ShowAllData();$checks.Add('訪問候補フィルタ：TPRの1行を抽出')
  $view=$book.Worksheets.Item('閲覧_AI・フィジカルAI')
  if(-not $view.Range('A2:A3').MergeCells){throw 'FANUC name not merged'}
  if(-not $view.Range('B2:B3').MergeCells){throw 'FANUC booth not merged'}
  $checks.Add('FANUC企業名・ブース縦結合をExcelで確認')
  $book.Save()
 } finally {$book.Close($false)}
 $book=$excel.Workbooks.Open((Join-Path $out 'JIMTOF2026_未掲載候補一覧_別冊.xlsx'),0,$false)
 try {
  $sheet=$book.Worksheets.Item('未掲載候補');$table=$sheet.ListObjects.Item(1)
  $table.Range.AutoFilter(3,'優先照会') | Out-Null
  $count=$excel.WorksheetFunction.Subtotal(103,$sheet.Range('A2:A302'))
  if($count -ne 9){throw "Candidate filter count: $count"}
  $table.AutoFilter.ShowAllData();$checks.Add('未掲載候補の優先照会フィルタ：9行を抽出')
  $sheet.Range('Q2').Value2='保留';$sheet.Range('R2').Value2=1;$sheet.Range('S2').Value2='入力検証'
  if($sheet.Range('Q2').Value2 -ne '保留' -or $sheet.Range('S2').Value2 -ne '入力検証'){throw 'Input failed'}
  $sheet.Range('Q2:S2').ClearContents();$checks.Add('訪問判断・優先度・当日メモの編集と初期空欄への復元')
  $book.Save()
 } finally {$book.Close($false)}
 foreach($file in Get-ChildItem -LiteralPath $out -Filter '*.xlsx'){
  $book=$excel.Workbooks.Open($file.FullName,0,$true)
  $checks.Add("通常モードで保存後再オープン：$($file.Name)／$($book.Worksheets.Count)シート")
  $book.Close($false)
 }
 [pscustomobject]@{engine=$excel.Version;checks=$checks.ToArray()} | ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 (Join-Path $root 'data\research\integrated_review_20261026_013801\native_excel_verification.json')
 $checks
} finally {$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
