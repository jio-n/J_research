param([string]$Workspace = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path)
$ErrorActionPreference='Stop'
$qa=Join-Path $PSScriptRoot '_private/presentation_native'
New-Item -ItemType Directory -Path $qa -Force | Out-Null
$file=Join-Path $Workspace ('outputs/'+(Split-Path $PSScriptRoot -Leaf)+'/report-r3.pptx')
$app=$null;$deck=$null;$issues=@();$tables=0
try {
 $app=New-Object -ComObject PowerPoint.Application
 $deck=$app.Presentations.Open($file,$true,$false,$false)
 if($deck.Slides.Count -ne 28){throw 'Slide count mismatch'}
 foreach($s in $deck.Slides){
  foreach($shape in $s.Shapes){
   if($shape.HasTable -eq -1){
    $tables++
    for($r=1;$r -le $shape.Table.Rows.Count;$r++){
     for($c=1;$c -le $shape.Table.Columns.Count;$c++){
      $cell=$shape.Table.Cell($r,$c).Shape
      $tf=$cell.TextFrame2
      $need=$tf.TextRange.BoundHeight+$tf.MarginTop+$tf.MarginBottom
      if($need -gt $cell.Height+2){$issues += [ordered]@{slide=$s.SlideIndex;row=$r;column=$c;need=$need;height=$cell.Height;text=$tf.TextRange.Text}}
     }
    }
   }
  }
  $s.Export((Join-Path $qa ('slide-{0:d2}.png' -f $s.SlideIndex)),'PNG',1920,1080)
 }
 $result=[ordered]@{engine='PowerPoint '+$app.Version;slides=$deck.Slides.Count;native_tables=$tables;cell_overflow_findings=$issues;rendered_slides=28;saved_changes=$false}
 $result|ConvertTo-Json -Depth 8|Set-Content -Encoding utf8 -LiteralPath (Join-Path $PSScriptRoot 'powerpoint_native_verification.json')
 $result|ConvertTo-Json -Depth 8 -Compress
} finally {if($null -ne $deck){$deck.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)};if($null -ne $app){$app.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)}}
