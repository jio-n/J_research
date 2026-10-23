$ErrorActionPreference='Stop'
$research=Get-Content -Raw -Encoding utf8 (Join-Path $PSScriptRoot 'research.json') | ConvertFrom-Json
$layout=Get-Content -Raw -Encoding utf8 (Join-Path $PSScriptRoot 'workbook_layout.json') | ConvertFrom-Json
$root=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$file=Join-Path $root ('outputs/'+(Split-Path $PSScriptRoot -Leaf)+'/JIMTOF2026_関心テーマ別_訪問計画.xlsx')
$excel=$null;$book=$null
function VisibleCount($sh,$last){$n=0;for($r=7;$r -le $last;$r++){if(-not $sh.Rows.Item($r).Hidden){$n++}};return $n}
function SortTable($table,$sh,$column,$last){$table.Sort.SortFields.Clear();[void]$table.Sort.SortFields.Add($sh.Range("${column}7:${column}${last}"),0,1);$table.Sort.Header=1;$table.Sort.Apply()}
try{
 $excel=New-Object -ComObject Excel.Application
 $excel.Visible=$false;$excel.DisplayAlerts=$false;$excel.AskToUpdateLinks=$false;$excel.AutomationSecurity=3
 $book=$excel.Workbooks.Open($file,0,$false)
 $main=$book.Worksheets.Item('訪問計画');$detail=$book.Worksheets.Item('技術詳細');$source=$book.Worksheets.Item('出典')
 $last=$research.items.Count+6;$table=$main.ListObjects.Item(1)
 if($book.Worksheets.Count -ne 4 -or $table.ListRows.Count -ne 390){throw 'Sheet or candidate count mismatch'}
 $counts=[ordered]@{}
 foreach($pair in @(@('AI',8),@('フィジカルAI',9),@('自律化',10),@('自動化',11))){
  [void]$table.Range.AutoFilter([int]$pair[1],'<>—')
  $n=VisibleCount $main $last
  $expected=@($research.items | Where-Object {$_.tags.($pair[0]).status -ne '—'}).Count
  if($n -ne $expected){throw "Tag filter mismatch: $($pair[0]) $n/$expected"}
  $counts[$pair[0]]=$n;$main.ShowAllData()
 }
 [void]$table.Range.AutoFilter(8,'<>—');[void]$table.Range.AutoFilter(9,'<>—')
 $overlap=VisibleCount $main $last
 $expectedOverlap=@($research.items | Where-Object {$_.tags.AI.status -ne '—' -and $_.tags.'フィジカルAI'.status -ne '—'}).Count
 if($overlap -ne $expectedOverlap){throw 'AND tag overlap filter failed'};$main.ShowAllData()
 [void]$table.Range.AutoFilter(2,'A 最優先');$priorityCount=VisibleCount $main $last
 if($priorityCount -ne 19){throw 'Priority filter failed'};$main.ShowAllData()

 # Native hyperlinks are added because the authoring library does not calculate HYPERLINK.
 for($i=0;$i -lt $research.items.Count;$i++){
  $x=$research.items[$i];$r=$i+7;$id=[string]$x.id
  if([string]$main.Cells.Item($r,24).Value2 -ne $id){throw 'Record order mismatch'}
  $target=[int]$layout.technicalStarts.$id
  [void]$main.Hyperlinks.Add($main.Cells.Item($r,24),'',"'技術詳細'!A$target",'技術詳細を開く',$id)
  [void]$detail.Hyperlinks.Add($detail.Cells.Item($target,1),'',"'訪問計画'!A1",'訪問計画の先頭へ戻る',$id)
  $url=[string]$main.Cells.Item($r,25).Value2
  if($url -match '^https?://'){[void]$main.Hyperlinks.Add($main.Cells.Item($r,25),$url)}
 }
 for($r=7;$r -le $source.ListObjects.Item(1).ListRows.Count+6;$r++){
  $url=[string]$source.Cells.Item($r,4).Value2
  if($url -match '^https?://'){[void]$source.Hyperlinks.Add($source.Cells.Item($r,4),$url)}
 }
 $excel.CalculateFullRebuild()
 if($main.Cells.Item(4,2).Value2 -ne 0 -or $main.Cells.Item(4,4).Value2 -ne 390){throw 'Initial formula count wrong'}
 $idBefore=[string]$main.Cells.Item(7,24).Value2
 $main.Cells.Item(7,3).Value2='訪問予定';$main.Cells.Item(7,20).Value2=1
 $main.Cells.Item(7,21).Value2='最優先';$main.Cells.Item(7,22).Value2='検証用の個人関心';$main.Cells.Item(7,23).Value2='検証用の訪問記録';$main.Cells.Item(7,19).Value2='説明のみ'
 $excel.CalculateFullRebuild();if($main.Cells.Item(4,2).Value2 -ne 1){throw 'Native recalculation failed'}
 foreach($c in @(3,19,21)){if($main.Cells.Item(7,$c).Validation.Type -ne 3){throw 'Dropdown missing'}}
 $main.Cells.Item(7,20).Value2=0;if($main.Cells.Item(7,20).Validation.Value){throw 'Visit order accepted zero'}
 $main.Cells.Item(7,20).Value2=1
 SortTable $table $main 'D' $last
 $rFound=0;for($r=7;$r -le $last;$r++){if([string]$main.Cells.Item($r,24).Value2 -eq $idBefore){$rFound=$r;break}}
 if($rFound -eq 0 -or $main.Cells.Item($rFound,22).Value2 -ne '検証用の個人関心' -or $main.Cells.Item($rFound,23).Value2 -ne '検証用の訪問記録'){throw 'Input separated from ID after sort'}
 if($main.Cells.Item($rFound,3).Value2 -ne '訪問予定' -or $main.Cells.Item($rFound,20).Value2 -ne 1){throw 'Visit state separated after sort'}
 SortTable $table $main 'A' $last
 if([string]$main.Cells.Item(7,24).Value2 -ne $idBefore){throw 'Sort restoration failed'}
 $main.Cells.Item(7,3).Value2='未選定';$main.Cells.Item(7,19).Value2='未確認';$main.Range('T7:W7').ClearContents()
 $excel.CalculateFullRebuild();if($main.Cells.Item(4,2).Value2 -ne 0){throw 'Input restoration failed'}
 $main.Cells.Item(7,24).Hyperlinks.Item(1).Follow()
 if($excel.ActiveSheet.Name -ne '技術詳細'){throw 'Detail navigation failed'}
 $detail.Cells.Item([int]$layout.technicalStarts.$idBefore,1).Hyperlinks.Item(1).Follow()
 if($excel.ActiveSheet.Name -ne '訪問計画'){throw 'Return navigation failed'}

 $rowCaps=@();$nativeSheets=@()
 foreach($sh in $book.Worksheets){
  # Only the new workbook is formatted. Native autofit is needed for Japanese wrap metrics.
  $lastRow=$sh.UsedRange.Rows.Count
  $sh.ListObjects.Item(1).TableStyle='TableStyleLight9'
  $sh.Range("A7:A$lastRow").EntireRow.AutoFit()
  $min=if($sh.Name -eq '訪問計画'){58}else{29}
  for($r=7;$r -le $lastRow;$r++){
   if($sh.Rows.Item($r).RowHeight -lt $min){$sh.Rows.Item($r).RowHeight=$min}
   if($sh.Rows.Item($r).RowHeight -ge 409){$rowCaps+=@($sh.Name+':'+$r)}
  }
  $sh.Activate();$excel.ActiveWindow.DisplayGridlines=$false;$excel.ActiveWindow.Zoom=90
  $excel.ActiveWindow.FreezePanes=$false;$excel.ActiveWindow.SplitRow=6;$excel.ActiveWindow.SplitColumn=if($sh.Name -eq '訪問計画'){4}elseif($sh.Name -eq '技術詳細'){2}else{1};$excel.ActiveWindow.FreezePanes=$true
  $sh.Range('A1').Select();$excel.ActiveWindow.ScrollRow=1;$excel.ActiveWindow.ScrollColumn=1
  $nativeSheets+=@([ordered]@{name=$sh.Name;table_rows=$sh.ListObjects.Item(1).ListRows.Count;frozen_rows=$excel.ActiveWindow.SplitRow;frozen_columns=$excel.ActiveWindow.SplitColumn})
 }
 if($rowCaps.Count -gt 0){throw ('Rows hit Excel maximum height: '+($rowCaps -join ','))}
 $main.Activate();$main.Range('A1').Select()
 $excel.CalculateFullRebuild();$book.Save()
 $summary=[ordered]@{engine='Excel '+$excel.Version;sheets=$nativeSheets;candidate_rows=390;tag_filters=$counts;AI_and_PhysicalAI=$overlap;priority_A=$priorityCount;recalculation='0 to 1 to 0';input_fields='visit state, order, own priority, personal reason, after-visit memo, related exhibit status';sort_identity='passed and restored';dropdowns='passed';order_zero_rejected=$true;detail_and_return_links='passed';source_links=$source.Hyperlinks.Count;main_links=$main.Hyperlinks.Count;maximum_height_rows=$rowCaps;inputs_restored=$true;verified_at=(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')}
 $summary|ConvertTo-Json -Depth 6|Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'native_verification.json')
 $summary|ConvertTo-Json -Depth 6 -Compress
}finally{
 if($null -ne $book){$book.Close($false);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($book)}
 if($null -ne $excel){$excel.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel)}
}
