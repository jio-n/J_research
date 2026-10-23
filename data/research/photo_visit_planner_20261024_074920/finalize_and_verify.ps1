$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$file=Join-Path $root ('outputs/'+(Split-Path $PSScriptRoot -Leaf)+'/JIMTOF2026_ユーザー選定_調査企業一覧.xlsx')
$excel=$null;$book=$null;$test=$null
function CountVisible($sh,$last){$n=0;for($r=2;$r -le $last;$r++){if(-not $sh.Rows.Item($r).Hidden){$n++}};return $n}
try{
 $excel=New-Object -ComObject Excel.Application
 $excel.Visible=$false;$excel.DisplayAlerts=$false;$excel.AutomationSecurity=3
 $book=$excel.Workbooks.Open($file,0,$false)
 if($book.Worksheets.Count -ne 2){throw 'Sheet count mismatch'}
 $metrics=@()
 foreach($sh in $book.Worksheets){
  $last=$sh.ListObjects.Item(1).ListRows.Count+1
  $sh.ListObjects.Item(1).TableStyle='TableStyleLight9'
  $sh.Range("A2:G$last").EntireRow.AutoFit()
  $max=0
  for($r=2;$r -le $last;$r++){
   if($sh.Rows.Item($r).RowHeight -lt 36){$sh.Rows.Item($r).RowHeight=36}
   $max=[Math]::Max($max,$sh.Rows.Item($r).RowHeight)
  }
  if($max -ge 409){throw 'Row height reached Excel cap'}
  $sh.Activate();$excel.ActiveWindow.Zoom=85;$excel.ActiveWindow.DisplayGridlines=$false
  $excel.ActiveWindow.FreezePanes=$false;$excel.ActiveWindow.SplitRow=1;$excel.ActiveWindow.SplitColumn=2;$excel.ActiveWindow.FreezePanes=$true
  $sh.Range('A1').Select();$excel.ActiveWindow.ScrollRow=1;$excel.ActiveWindow.ScrollColumn=1
  $metrics+=@{sheet=$sh.Name;rows=$last-1;maximum_row_height=$max;frozen_rows=1;frozen_columns=2}
 }
 $book.Worksheets.Item(1).Activate();$book.Save();$book.Close($false);$book=$null
 $copy=Join-Path $PSScriptRoot '_private/operation_test.xlsx';Copy-Item -LiteralPath $file -Destination $copy
 $test=$excel.Workbooks.Open($copy,0,$false)
 $ai=$test.Worksheets.Item(1);$au=$test.Worksheets.Item(2)
 [void]$ai.ListObjects.Item(1).Range.AutoFilter(1,'ファナック株式会社')
 if((CountVisible $ai 33) -ne 2){throw 'Company filter failed'};$ai.ShowAllData()
 [void]$ai.ListObjects.Item(1).Range.AutoFilter(3,'★')
 $stars=CountVisible $ai 33
 if($stars -ne 4){throw "Priority filter failed: $stars"};$ai.ShowAllData()
 $au.Cells.Item(2,6).Value2='検証用の着眼点';$au.Cells.Item(2,7).Value2='検証用の質問'
 $sort=$au.ListObjects.Item(1).Sort;$sort.SortFields.Clear();[void]$sort.SortFields.Add($au.Range('A2:A51'),0,1);$sort.Header=1;$sort.Apply()
 $found=0
 for($r=2;$r -le 51;$r++){if($au.Cells.Item($r,1).Value2 -eq 'YKT株式会社'){$found=$r}}
 if($found -eq 0 -or $au.Cells.Item($found,2).Value2 -ne 'E2026' -or $au.Cells.Item($found,6).Value2 -ne '検証用の着眼点' -or $au.Cells.Item($found,7).Value2 -ne '検証用の質問'){throw 'Sort separated input from company'}
 $test.Close($false);$test=$null
 $result=@{engine='Microsoft Excel '+$excel.Version;metrics=$metrics;company_filter=2;star_filter=$stars;input_and_sort='passed on disposable copy; final file unaffected';checked_at=(Get-Date -Format s)}
 $result|ConvertTo-Json -Depth 6|Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'native_verification.json')
 $result|ConvertTo-Json -Depth 6 -Compress
}finally{
 if($null -ne $test){$test.Close($false)}
 if($null -ne $book){$book.Close($false)}
 if($null -ne $excel){$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
}
