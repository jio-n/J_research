$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$p=Get-Content (Join-Path $PSScriptRoot 'link_plan.json') -Raw -Encoding utf8|ConvertFrom-Json
$file=Join-Path $root ('outputs/'+(Split-Path $PSScriptRoot -Leaf)+'/JIMTOF2026_調査企業一覧_追加技術資料付き.xlsx')
$excel=$null;$book=$null;$src=$null
try{
 $excel=New-Object -ComObject Excel.Application;$excel.Visible=$false;$excel.DisplayAlerts=$false;$excel.AutomationSecurity=3
 $src=$excel.Workbooks.Open((Join-Path $root $p.source_workbook),0,$true)
 $book=$excel.Workbooks.Open($file,0,$false)
 for($n=1;$n -le 2;$n++){
  $a=$src.Worksheets.Item($n);$b=$book.Worksheets.Item($n);$last=if($n -eq 1){33}else{51}
  $b.Hyperlinks.Delete()
  $b.Range("F2:G$last").Font.Color=0;$b.Range("F2:G$last").Font.Underline=-4142
  $a.Range('G1').Copy($b.Range('H1'));$b.Range('H1').Value2='追加技術資料'
  $b.Columns.Item(8).ColumnWidth=56
  $b.Range("H2:H$last").Font.Name='Yu Gothic UI';$b.Range("H2:H$last").Font.Size=11
  $b.Range("H2:H$last").WrapText=$true;$b.Range("H2:H$last").VerticalAlignment=-4160
  $b.ListObjects.Item(1).Resize($b.Range("A1:H$last"))
  for($r=1;$r -le $last;$r++){
   $b.Rows.Item($r).RowHeight=$a.Rows.Item($r).RowHeight
   for($c=1;$c -le 7;$c++){
    if($a.Cells.Item($r,$c).Interior.Color -ne $b.Cells.Item($r,$c).Interior.Color){$b.Cells.Item($r,$c).Interior.Color=$a.Cells.Item($r,$c).Interior.Color}
   }
  }
 }
 foreach($l in $p.links){
  $c=$book.Worksheets.Item($l.sheet).Range($l.cell)
  $tip=if($l.kind -eq '追加技術資料'){$l.publisher+'｜'+$l.reviewed_summary+' ※'+$l.scope_note}else{$l.kind+'：'+$l.locator}
  if($tip.Length -gt 250){$tip=$tip.Substring(0,250)}
  [void]$book.Worksheets.Item($l.sheet).Hyperlinks.Add($c,$l.url,'',$tip)
  $c.Font.Name='Yu Gothic UI';$c.Font.Size=11;$c.Font.Color=12611589;$c.Font.Underline=2
 }
 $values=0;$fills=0
 for($n=1;$n -le 2;$n++){
  $a=$src.Worksheets.Item($n);$b=$book.Worksheets.Item($n);$last=if($n -eq 1){33}else{51}
  if($b.ListObjects.Count -ne 1 -or $b.ListObjects.Item(1).Range.Columns.Count -ne 8 -or $b.ListObjects.Item(1).ListRows.Count -ne $last-1){throw 'Table size mismatch'}
  for($r=1;$r -le $last;$r++){
   if([Math]::Abs($a.Rows.Item($r).RowHeight-$b.Rows.Item($r).RowHeight) -gt 0.1){throw "Row height changed $n/$r"}
   for($c=1;$c -le 7;$c++){
    if($a.Cells.Item($r,$c).Value2 -cne $b.Cells.Item($r,$c).Value2){throw "Value changed $n/$r/$c"};$values++
    if($a.Cells.Item($r,$c).Interior.Color -ne $b.Cells.Item($r,$c).Interior.Color){throw "Fill changed $n/$r/$c"};$fills++
   }
  }
  for($c=1;$c -le 7;$c++){if([Math]::Abs($a.Columns.Item($c).ColumnWidth-$b.Columns.Item($c).ColumnWidth) -gt 0.1){throw 'Width changed'}}
 }
 $sh=$book.Worksheets.Item(1);[void]$sh.ListObjects.Item(1).Range.AutoFilter(8,'<>')
 $visible=0;for($r=2;$r -le 33;$r++){if(-not $sh.Rows.Item($r).Hidden){$visible++}}
 if($visible -ne 10){throw "Additional source filter failed $visible"};$sh.ShowAllData()
 [void]$sh.ListObjects.Item(1).Range.AutoFilter(1,'ファナック株式会社')
 $visible=0;for($r=2;$r -le 33;$r++){if(-not $sh.Rows.Item($r).Hidden){$visible++}}
 if($visible -ne 2){throw 'Company filter failed'};$sh.ShowAllData()
 $sh.Activate();$book.Save();$book.Close($false);$book=$null
 $book=$excel.Workbooks.Open($file,0,$true)
 foreach($l in $p.links){
  $c=$book.Worksheets.Item($l.sheet).Range($l.cell)
  if($c.Hyperlinks.Count -ne 1 -or $c.Hyperlinks.Item(1).Address -cne $l.url){throw ('Saved link mismatch '+$l.cell)}
  if($l.kind -eq '追加技術資料' -and $c.Value2 -cne $l.text){throw 'Label mismatch'}
 }
 for($n=1;$n -le 2;$n++){
  $sh=$book.Worksheets.Item($n);$last=if($n -eq 1){33}else{51}
  if($sh.Range("F2:G$last").Hyperlinks.Count -ne 0){throw 'Comment links remain'}
  for($r=2;$r -le $last;$r++){foreach($c in 6,7){if($sh.Cells.Item($r,$c).Font.Color -ne 0 -or $sh.Cells.Item($r,$c).Font.Underline -ne -4142){throw 'Comments not plain black'}}}
 }
 $summary=@{native_engine='Microsoft Excel '+$excel.Version;company_links=82;primary_item_links=32;additional_links=10;saved_hyperlinks_verified=$p.links.Count;comment_links=0;cells_compared=$values;fills_compared=$fills;original_heights_widths_preserved=$true;additional_source_filter_visible=10;company_filter_visible=2;two_sheets_eight_columns=$true;verified_at=(Get-Date -Format s)}
 $summary|ConvertTo-Json -Depth 5|Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'native_verification.json')
 $summary|ConvertTo-Json -Compress
}finally{
 if($null -ne $book){$book.Close($false)};if($null -ne $src){$src.Close($false)}
 if($null -ne $excel){$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
}
