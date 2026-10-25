$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$p=Get-Content (Join-Path $PSScriptRoot 'link_plan.json') -Raw -Encoding utf8|ConvertFrom-Json
$file=Join-Path $root ('outputs/'+(Split-Path $PSScriptRoot -Leaf)+'/JIMTOF2026_調査企業一覧_C列重複管理付き.xlsx')
# Preserve the original native package; apply Artifact Tool-authored cell content to this copy.
Copy-Item -LiteralPath (Join-Path $root $p.source_workbook) -Destination $file -Force
$excel=$null;$book=$null;$src=$null;$auth=$null
try{
 $excel=New-Object -ComObject Excel.Application;$excel.Visible=$false;$excel.DisplayAlerts=$false;$excel.AutomationSecurity=3
 $src=$excel.Workbooks.Open((Join-Path $root $p.source_workbook),0,$true)
 $auth=$excel.Workbooks.Open((Join-Path $PSScriptRoot '_private/authored.xlsx'),0,$true)
 $book=$excel.Workbooks.Open($file,0,$false)
 for($n=1;$n -le 2;$n++){
  $b=$book.Worksheets.Item($n);$base=$src.Worksheets.Item($n);$s=$p.sheets[$n-1];$last=$s.values.Count+1
  [void]$b.Columns.Item(3).Insert(-4161)
  $b.Range("A1:I$last").Value2=$auth.Worksheets.Item($n).Range("A1:I$last").Value2
  if($b.ListObjects.Count -eq 0){
   $tbl=$b.ListObjects.Add(1,$b.Range("A1:I$last"),$null,1)
   $tbl.Name='PhotoTable'+$n;$tbl.TableStyle='TableStyleLight9'
  }else{$b.ListObjects.Item(1).Resize($b.Range("A1:I$last"))}
  for($c=1;$c -le 8;$c++){$nc=if($c -ge 3){$c+1}else{$c};$b.Columns.Item($nc).ColumnWidth=$base.Columns.Item($c).ColumnWidth}
  [void]$base.Range('A1:B1').Copy($b.Range('A1'))
  [void]$base.Range('C1:H1').Copy($b.Range('D1'))
  [void]$base.Range('B1').Copy($b.Range('C1'));$b.Range('C1').Value2='他シートとの重複'
  for($r=2;$r -le $last;$r++){
   $origin=$s.origins[$r-2];$a=$src.Worksheets.Item($origin.sheet);$sr=$origin.row
   [void]$a.Range("A${sr}:B${sr}").Copy($b.Range("A$r"))
   [void]$a.Range("C${sr}:H${sr}").Copy($b.Range("D$r"))
   $b.Rows.Item($r).RowHeight=$a.Rows.Item($sr).RowHeight
  }
  $b.Columns.Item(3).ColumnWidth=30
  $b.Range("C2:C$last").Font.Name='Yu Gothic UI';$b.Range("C2:C$last").Font.Size=11
  $b.Range("C2:C$last").Font.Color=0;$b.Range("C2:C$last").Font.Underline=-4142
  $b.Range("C2:C$last").WrapText=$true;$b.Range("C2:C$last").VerticalAlignment=-4160
  $b.Hyperlinks.Delete()
 }
 foreach($l in $p.links){
  $c=$book.Worksheets.Item($l.sheet).Range($l.cell);$old=$src.Worksheets.Item($l.source_sheet).Range($l.source_cell)
  if($old.Hyperlinks.Count -ne 1 -or $old.Hyperlinks.Item(1).Address -cne $l.url){throw 'Source link mismatch'}
  [void]$book.Worksheets.Item($l.sheet).Hyperlinks.Add($c,$l.url,'',$old.Hyperlinks.Item(1).ScreenTip)
  $c.Font.Color=12611589;$c.Font.Underline=2
 }
 $cells=0;$counts=@()
 for($n=1;$n -le 2;$n++){
  $b=$book.Worksheets.Item($n);$s=$p.sheets[$n-1];$last=$s.values.Count+1
  if($b.ListObjects.Item(1).Range.Columns.Count -ne 9 -or $b.ListObjects.Item(1).ListRows.Count -ne $last-1){throw 'Table mismatch'}
  for($c=1;$c -le 9;$c++){if($b.Cells.Item(1,$c).Value2 -cne $p.headers[$c-1]){throw 'Header mismatch'}}
  $savedValues=$b.Range("A2:I$last").Value2
  for($r=2;$r -le $last;$r++){
   $origin=$s.origins[$r-2];$a=$src.Worksheets.Item($origin.sheet);$sr=$origin.row
   for($c=1;$c -le 8;$c++){
    $nc=if($c -ge 3){$c+1}else{$c}
    if($savedValues.GetValue($r-1,$nc) -cne $s.values[$r-2][$nc-1]){throw "Value changed $n/$r/$c"};$cells++
   }
   if($savedValues.GetValue($r-1,3) -cne $s.values[$r-2][2]){throw 'Overlap tag mismatch'}
   if($origin.sheet -eq 'AI・フィジカルAI'){
    $colored=if($sr -eq 19){@(6)}elseif($sr -eq 20){@(7)}elseif($sr -eq 26){@(4,7)}else{@()}
    foreach($oldcol in $colored){$b.Cells.Item($r,$oldcol+1).Interior.Color=$a.Cells.Item($sr,$oldcol).Interior.Color}
   }
  }
  if($b.Range("G2:H$last").Hyperlinks.Count -ne 0){throw 'User comment links introduced'}
  [void]$b.ListObjects.Item(1).Range.AutoFilter(3,'*重複あり')
  $visible=$excel.WorksheetFunction.Subtotal(103,$b.Range("A2:A$last"))
  if($visible -ne $s.overlap_rows){throw 'Overlap filter mismatch'};$b.ShowAllData()
  $counts+=@{sheet=$b.Name;records=$s.values.Count;overlap_rows=$visible}
 }
 $book.Worksheets.Item(1).Activate();$book.Save();$book.Close($false);$book=$null
 $book=$excel.Workbooks.Open($file,0,$true)
 $total=$book.Worksheets.Item(1).Hyperlinks.Count+$book.Worksheets.Item(2).Hyperlinks.Count
 if($total -ne $p.links.Count){throw 'Saved link count mismatch'}
 $out=@{engine='Microsoft Excel '+$excel.Version;shared_companies=$p.shared_company_count;overlap_filters=$counts;record_cells_values_verified=$cells;hyperlink_count_verified=$total;copied_AI_records=$p.copied_records.Count;columns=9;source_records_unchanged=$true;pending_Wintech_comment_not_integrated=$true;verified_at=(Get-Date -Format s)}
 $out|ConvertTo-Json -Depth 5|Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'native_verification.json')
 $out|ConvertTo-Json -Compress -Depth 5
}finally{
 if($book){$book.Close($false)};if($auth){$auth.Close($false)};if($src){$src.Close($false)}
 if($excel){$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
}
