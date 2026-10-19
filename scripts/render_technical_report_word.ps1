$ErrorActionPreference = 'Stop'
$taskRoot = (Get-Location).Path
$docPath = Join-Path $taskRoot 'outputs\JIMTOF2026_技術動向レポート_20261019.docx'
$pdfPath = Join-Path $taskRoot '.build\technical_report\docx_render\report.pdf'
$wordApp = $null
$reportDoc = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordApp.AutomationSecurity = 3
    $reportDoc = $wordApp.Documents.Open($docPath, $false, $true, $false)
    $reportDoc.Repaginate()
    $null = $reportDoc.Fields.Update()
    $pageCount = $reportDoc.ComputeStatistics(2)
    $reportDoc.ExportAsFixedFormat($pdfPath, 17)
    [PSCustomObject]@{renderer='Microsoft Word';pages=$pageCount;pdf=$pdfPath} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot '.build\technical_report\docx_render\render.json') -Encoding UTF8
    Write-Output "Word PDF saved. Pages: $pageCount"
} finally {
    if ($null -ne $reportDoc) { $reportDoc.Close(0) }
    if ($null -ne $wordApp) { $wordApp.Quit(0) }
}
