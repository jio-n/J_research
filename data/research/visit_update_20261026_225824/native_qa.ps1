$ErrorActionPreference='Stop'
$root='C:\Users\paulr\resarch\JIMTOF2026_Research';$file=Join-Path $root 'outputs\visit_update_20261026_225824\JIMTOF2026_訪問先一覧_更新版_優先色と巡回順.xlsx'
$excel=New-Object -ComObject Excel.Application;$excel.Visible=$false;$excel.DisplayAlerts=$false
try {
 $book=$excel.Workbooks.Open($file,0,$false)
 try {
  if($book.Worksheets.Count -ne 8){throw 'Sheet count'}
  $ai=$book.Worksheets.Item('AI・フィジカルAI');if($ai.Range('E2').Interior.Color -ne 65535){throw 'Yellow fill'}
  $sh=$book.Worksheets.Item('エリア別巡回順');$t=$sh.ListObjects.Item(1);$t.Range.AutoFilter(6,'最優先') | Out-Null
  $n=$excel.WorksheetFunction.Subtotal(103,$sh.Range('C2:C35'));if($n -ne 11){throw "Yellow count $n"};$t.AutoFilter.ShowAllData()
  $sh.Range('J2').Value2='入力検証';if($sh.Range('J2').Value2 -ne '入力検証'){throw 'Input failed'};$sh.Range('J2').ClearContents()
  $view=$book.Worksheets.Item('閲覧_AI・フィジカルAI');if(-not $view.Range('A2:A3').MergeCells){throw 'Merge lost'}
  $book.Save()
 } finally {$book.Close($false)}
 $book=$excel.Workbooks.Open($file,0,$true);$book.Close($false)
 [pscustomobject]@{engine=$excel.Version;checks=@('8シートの通常オープン','黄色の行背景を確認','巡回表で最優先11社のフィルタ','メモ入力と空欄への復元','企業名の縦結合','保存後の再オープン')} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $root 'data\research\visit_update_20261026_225824\native_verification.json')
 'Native Excel checks passed'
} finally {$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
