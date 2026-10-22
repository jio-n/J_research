from pathlib import Path
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent;name=D.name
s=(R/'scripts/build_four_tag_workbook_20261022.mjs').read_text(encoding='utf8')
s=s.replace("path.dirname(fileURLToPath(import.meta.url)),'..'","path.dirname(fileURLToPath(import.meta.url)),'../../..'")
s=s.replace('data/research/four_tag_20261022/research.json',f'data/research/{name}/research.json').replace('outputs/four_tag_20261022',f'outputs/{name}').replace('.build/four_tag_20261022/workbook_qa',f'data/research/{name}/_private/workbook_qa')
s=s.replace('JIMTOF2026_訪問先選定_四タグと技術詳細_20261022.xlsx','visit_selection.xlsx')
s=s.replace('x.exhibit,x.task,x.method','x.exhibit,x.task_categories.join("／"),x.method')
s=s.replace('x.check,x.depth,\'\',','x.check,x.refinement_review+"／"+x.depth,\'\',')
s=s.replace("['対象タスク','task']","['対象タスク','task']")
s=s.replace("['新規性・適応能力','advance']","['新規性・適応能力','novelty_note']")
s=s.replace("methodRows.push(['資料探索の取得ログ'", "methodRows.push(['前版の資料探索ログ'")
s=s.replace("今回の確認深度は候補ごとに記載。","今回の原典照合は32候補・戦略等36資料。今回の確認深度は候補ごとに記載。")
s=s.replace("const srcRows=", "methodRows.push(['今回の版','387候補から総称1件を統合し、3機能を追加して389候補。全1,146掲載行は保持。','今回照合32候補。その他の候補は前版の確認深度を保持。']);\nconst srcRows=")
(D/'build_workbook.mjs').write_text(s,encoding='utf8')
p=(R/'scripts/finalize_four_tag_workbook_20261022.ps1').read_text(encoding='utf8')
p=p.replace("param([string]$Workspace = (Split-Path -Parent $PSScriptRoot))", "param([string]$Workspace = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path)")
p=p.replace('data/research/four_tag_20261022/research.json',f'data/research/{name}/research.json').replace('outputs/four_tag_20261022/JIMTOF2026_訪問先選定_四タグと技術詳細_20261022.xlsx',f'outputs/{name}/visit_selection.xlsx').replace('.build/four_tag_20261022/workbook_qa/native_verification.json',f'data/research/{name}/_private/workbook_qa/native_verification.json')
p=p.replace('    # Keep the opening view', '''    # Verify native filtering, dropdown input, hyperlink target, and restoration.
    $table = $selection.ListObjects.Item(1)
    [void]$table.Range.AutoFilter(11, '優先訪問')
    $visible = 0
    for ($r=6; $r -le $data.items.Count+5; $r++) { if (-not $selection.Rows.Item($r).Hidden) { $visible++ } }
    $expected = @($data.items | Where-Object { $_.recommendation -eq '優先訪問' }).Count
    if ($visible -ne $expected) { throw 'Native filter mismatch' }
    $selection.ShowAllData()
    if ($selection.Cells.Item(6,1).Validation.Type -ne 3) { throw 'Visit dropdown missing' }
    $selection.Cells.Item(6,2).Value2 = '高'
    $selection.Cells.Item(6,18).Value2 = '動作確認テスト'
    if ($selection.Cells.Item(6,18).Value2 -ne '動作確認テスト') { throw 'Notes entry failed' }
    $selection.Cells.Item(6,2).ClearContents()
    $selection.Cells.Item(6,18).ClearContents()
    $firstLink = $selection.Cells.Item(6,3).Hyperlinks.Item(1)
    $firstLink.Follow()
    if ($excel.ActiveSheet.Name -ne '技術詳細') { throw 'Internal hyperlink navigation failed' }
    # Keep the opening view''')
p=p.replace('source_links=$sources.Hyperlinks.Count;', 'source_links=$sources.Hyperlinks.Count; native_filter_visible=$visible; filter_expected=$expected; dropdown_and_notes="passed-restored"; hyperlink_navigation="passed";')
(D/'finalize_workbook.ps1').write_text(p,encoding='utf8')
print('New local builders prepared')
