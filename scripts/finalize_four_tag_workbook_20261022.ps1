param([string]$Workspace = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$data = Get-Content -LiteralPath (Join-Path $Workspace 'data/research/four_tag_20261022/research.json') -Raw -Encoding utf8 | ConvertFrom-Json
$file = Join-Path $Workspace 'outputs/four_tag_20261022/JIMTOF2026_訪問先選定_四タグと技術詳細_20261022.xlsx'
$excel = $null
$book = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.AutomationSecurity = 3
    $book = $excel.Workbooks.Open($file, 0, $false)
    $selection = $book.Worksheets.Item('訪問選定')
    if ($book.Worksheets.Count -ne 7) { throw 'Worksheet count mismatch' }
    if ($selection.ListObjects.Item(1).ListRows.Count -ne $data.items.Count) { throw 'Candidate row count mismatch' }
    if ($book.Worksheets.Item('全出展者').ListObjects.Item(1).ListRows.Count -ne 1146) { throw 'Master row count mismatch' }
    if ($selection.Cells.Item(3,4).Value2 -ne $data.items.Count) { throw 'Summary count mismatch' }
    $selection.Cells.Item(6,1).Value2 = '訪問予定'
    $excel.CalculateFullRebuild()
    if ($selection.Cells.Item(3,2).Value2 -ne 1) { throw 'Visit count did not recalculate' }
    $selection.Cells.Item(6,1).Value2 = '未選定'
    $excel.CalculateFullRebuild()
    if ($selection.Cells.Item(3,2).Value2 -ne 0) { throw 'Restored visit count mismatch' }
    # Artifact Tool does not implement HYPERLINK calculation. Add native links without formulas.
    for ($i=0; $i -lt $data.items.Count; $i++) {
        $row = $i+6
        $target = [int]$selection.Cells.Item($row,21).Value2
        $id = [string]$data.items[$i].id
        if ($selection.Cells.Item($row,3).Value2 -ne $id) { throw "Record order mismatch: $id" }
        [void]$selection.Hyperlinks.Add($selection.Cells.Item($row,3), '', "'技術詳細'!A$target", '技術詳細を開く', $id)
    }
    $sources = $book.Worksheets.Item('出典')
    for ($row=6; $row -le $sources.ListObjects.Item(1).ListRows.Count+5; $row++) {
        $url = [string]$sources.Cells.Item($row,4).Value2
        if ($url -match '^https?://') { [void]$sources.Hyperlinks.Add($sources.Cells.Item($row,4), $url) }
    }
    # Keep the opening view on the selection sheet and the first records.
    $selection.Activate()
    $selection.Range('A1').Select()
    $excel.CalculateFullRebuild()
    $book.Save()
    $summary = [ordered]@{ native_excel_version=$excel.Version; worksheets=$book.Worksheets.Count; candidate_rows=$data.items.Count; master_rows=1146; visit_count_restored=$selection.Cells.Item(3,2).Value2; internal_links=$selection.Hyperlinks.Count; source_links=$sources.Hyperlinks.Count; verified_at=(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss') }
    $summary | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $Workspace '.build/four_tag_20261022/workbook_qa/native_verification.json') -Encoding utf8
    $summary | ConvertTo-Json -Compress
} finally {
    if ($null -ne $book) { $book.Close($false); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($book) }
    if ($null -ne $excel) { $excel.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel) }
}
