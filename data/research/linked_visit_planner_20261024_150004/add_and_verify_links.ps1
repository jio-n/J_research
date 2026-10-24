$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$p=Get-Content (Join-Path $PSScriptRoot 'link_plan.json') -Raw -Encoding utf8|ConvertFrom-Json
$file=Join-Path $root ('outputs/'+(Split-Path $PSScriptRoot -Leaf)+'/JIMTOF2026_ユーザー選定_調査企業一覧_リンク付き.xlsx')
$excel=$null;$book=$null;$src=$null
try{
 $excel=New-Object -ComObject Excel.Application;$excel.Visible=$false;$excel.DisplayAlerts=$false;$excel.AutomationSecurity=3
 $src=$excel.Workbooks.Open((Join-Path $root $p.source_workbook),0,$true)
 $book=$excel.Workbooks.Open($file,0,$false)
 foreach($l in $p.links){
  $sh=$book.Worksheets.Item($l.sheet);$c=$sh.Range($l.cell)
  $tip=($l.kind+'：'+$l.locator);if($tip.Length -gt 240){$tip=$tip.Substring(0,240)}
  [void]$sh.Hyperlinks.Add($c,$l.url,'',$tip)
  $c.Font.Name='Yu Gothic UI';$c.Font.Size=11;$c.Font.Color=12611589;$c.Font.Underline=2
 }
 $styles=0;$values=0
 for($n=1;$n -le 2;$n++){
  $a=$src.Worksheets.Item($n);$b=$book.Worksheets.Item($n)
  $last=if($n -eq 1){33}else{51}
  if($a.Name -ne $b.Name -or $b.ListObjects.Count -ne 1 -or $b.ListObjects.Item(1).ListRows.Count -ne $last-1){throw 'Sheet/table mismatch'}
  for($r=1;$r -le $last;$r++){
   # Preserve all original row heights and column widths, including multi-line questions.
   if([Math]::Abs($a.Rows.Item($r).RowHeight-$b.Rows.Item($r).RowHeight) -gt 0.1){throw "Row height changed $n/$r"}
   for($c=1;$c -le 7;$c++){
    $av=$a.Cells.Item($r,$c).Value2;$bv=$b.Cells.Item($r,$c).Value2
    if($n -eq 1 -and $r -eq 33 -and $c -eq 1){$av='株式会社ナベル'}
    if($av -cne $bv){throw "Value changed $n/$r/$c"};$values++
    if($a.Cells.Item($r,$c).Interior.Color -ne $b.Cells.Item($r,$c).Interior.Color){throw "Fill changed $n/$r/$c"};$styles++
   }
  }
  for($c=1;$c -le 7;$c++){if([Math]::Abs($a.Columns.Item($c).ColumnWidth-$b.Columns.Item($c).ColumnWidth) -gt 0.1){throw 'Width changed'}}
  # Existing pane settings are preserved by the import. Do not reset unrelated window properties.
 }
 $sh=$book.Worksheets.Item(1);[void]$sh.ListObjects.Item(1).Range.AutoFilter(1,'ファナック株式会社')
 $visible=0;for($r=2;$r -le 33;$r++){if(-not $sh.Rows.Item($r).Hidden){$visible++}}
 if($visible -ne 2){throw 'Filter failed'};$sh.ShowAllData()
 $sh.Activate();$book.Save();$book.Close($false);$book=$null
 $book=$excel.Workbooks.Open($file,0,$true)
 foreach($l in $p.links){
  $c=$book.Worksheets.Item($l.sheet).Range($l.cell)
  if($c.Hyperlinks.Count -ne 1 -or $c.Hyperlinks.Item(1).Address -cne $l.url){throw ('Saved hyperlink mismatch '+$l.id+'/'+$l.cell)}
 }
 $summary=@{native_engine='Microsoft Excel '+$excel.Version;company_links=82;technical_links=96;saved_hyperlinks_verified=$p.links.Count;cells_compared=$values;fills_compared=$styles;data_changes='Only A33 company transcription correction: 株式会社ベル -> 株式会社ナベル';filter_company_visible=2;original_heights_widths_preserved=$true;two_sheets_seven_columns=$true;verified_at=(Get-Date -Format s)}
 $summary|ConvertTo-Json -Depth 5|Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'native_verification.json')
 $summary|ConvertTo-Json -Compress
}finally{
 if($null -ne $book){$book.Close($false)};if($null -ne $src){$src.Close($false)}
 if($null -ne $excel){$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
}
