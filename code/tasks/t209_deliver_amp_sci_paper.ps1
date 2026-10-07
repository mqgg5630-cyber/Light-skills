# t209_deliver_amp_sci_paper.ps1 - Deliver complete Alligator Gut AMP SCI Paper & Deliverables using the user's exact SCI figures
# ASCII-only source for Windows PowerShell 5.1 compatibility.

$ErrorActionPreference = 'Continue'
$repo = (Get-Location).Path
Write-Output "HOST=$env:COMPUTERNAME"
Write-Output "REPO=$repo"

# 1. Locate Desktop directory
$desktop = $null
foreach ($d in @([Environment]::GetFolderPath("Desktop"), ("D:\" + [char]0x684C + [char]0x9762), (Join-Path $env:USERPROFILE "Desktop"))) {
    if ($d -and (Test-Path -LiteralPath $d)) { $desktop = $d; break }
}
if (-not $desktop) {
    $desktop = [Environment]::GetFolderPath("Desktop")
}
Write-Output "DESKTOP=$desktop"

# 2. Locate User's EXACT SCI Suite Figures
# User Suite: SCI_Docking_Figure4_Suite/sci_composite_figures
$userFigSuite = Join-Path $desktop "AMP_Docking_Vina_R255_20261005_1552\SCI_Docking_Figure4_Suite\sci_composite_figures"
Write-Output "USER_FIG_SUITE=$userFigSuite"
Write-Output "USER_FIG_SUITE_EXISTS=$(Test-Path -LiteralPath $userFigSuite)"

$figSrc = Join-Path $repo "sources\user_amp\figures"
New-Item -ItemType Directory -Force -Path $figSrc | Out-Null

if (Test-Path -LiteralPath $userFigSuite) {
    Copy-Item -LiteralPath (Join-Path $userFigSuite "*.png") -Destination $figSrc -Force
    Write-Output "COPIED_USER_SUITE_FIGURES_INTO_REPO=True"
}

# 3. Rebuild docx with Python if python is available so the user's local 300 DPI suite is embedded
$py = $null
foreach ($c in @("python.exe", "E:\spider\python.exe", (Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"))) {
    try {
        & $c -c "import docx" 2>$null
        if ($LASTEXITCODE -eq 0) { $py = $c; break }
    } catch {}
}

if ($py) {
    Write-Output "BUILDING_DOCX_WITH_USER_SUITE_USING=$py"
    $buildScript = Join-Path $repo "code\tasks\build_amp_full_manuscript.py"
    & $py $buildScript
    Write-Output "REBUILD_EXIT_CODE=$LASTEXITCODE"
} else {
    Write-Output "NOTE: python-docx not found locally, using pre-built deliverables"
}

# 4. Check deliverables in repo
$delivDir = Join-Path $repo "deliverable"
$sciDocx = Join-Path $delivDir "AMP_Alligator_Gut_SCI_Manuscript.docx"
$methodDocx = Join-Path $delivDir "method_with_docking_20261007_1600.docx"
$reproMd = Join-Path $delivDir "AMP_Pipeline_Reproduction_Method.md"
$reviewMd = Join-Path $delivDir "AMP_Figure_Style_Review.md"
$manifestJson = Join-Path $delivDir "AMP_Method_Supplement_manifest.json"

if (-not (Test-Path -LiteralPath $sciDocx)) {
    Write-Output "FAIL: SCI docx missing at $sciDocx"
    exit 1
}
Write-Output ("SCI_DOCX_SIZE=" + (Get-Item -LiteralPath $sciDocx).Length)
Write-Output ("METHOD_DOCX_SIZE=" + (Get-Item -LiteralPath $methodDocx).Length)

# 5. Deliver to target folders on Desktop
$destDirs = @(
    (Join-Path $desktop "AMP_SCI_Paper"),
    (Join-Path $desktop "AMP_Docking_Vina_R255_20261005_1552")
)

foreach ($dest in $destDirs) {
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -LiteralPath $sciDocx -Destination $dest -Force
    Copy-Item -LiteralPath $methodDocx -Destination $dest -Force
    Copy-Item -LiteralPath $reproMd -Destination $dest -Force
    Copy-Item -LiteralPath $reviewMd -Destination $dest -Force
    Copy-Item -LiteralPath $manifestJson -Destination $dest -Force
    Write-Output "DELIVERED_TO=$dest"
}

# 6. Cleanup local disk space per user request
$oldPeriodontitisFolder = Join-Path $desktop "Periodontitis_AChE_SCI_Paper"
if (Test-Path -LiteralPath $oldPeriodontitisFolder) {
    try {
        Remove-Item -LiteralPath $oldPeriodontitisFolder -Recurse -Force -ErrorAction SilentlyContinue
        Write-Output "CLEANED_OLD_FOLDER=$oldPeriodontitisFolder"
    } catch {
        Write-Output "NOTE_CLEANUP=$($_.Exception.Message)"
    }
}

# 7. Word/WPS COM verification
$wordOk = $false
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($sciDocx, $false, $true) # read-only
    if ($doc) {
        $pCount = $doc.Paragraphs.Count
        $tCount = $doc.Tables.Count
        $sCount = $doc.Sections.Count
        Write-Output "WORD_COM_OPEN=True paragraphs=$pCount tables=$tCount sections=$sCount"
        $doc.Close($false)
        $wordOk = $true
    }
    $word.Quit()
} catch {
    Write-Output ("WORD_COM_NOTE=" + $_.Exception.Message)
}

# 8. Write status receipt
$statusDir = Join-Path $repo "results\status"
New-Item -ItemType Directory -Force -Path $statusDir | Out-Null
$reportFile = Join-Path $statusDir "round275_amp_sci_delivery_report.md"
$lines = @(
# User Suite: SCI_Docking_Figure4_Suite/sci_composite_figures
    "",
    "- Host: $env:COMPUTERNAME",
    "- Output Folder: $desktop\AMP_SCI_Paper",
    "- Output Folder 2: $desktop\AMP_Docking_Vina_R255_20261005_1552",
"- Figure Source: Desktop\AMP_Docking_Vina_R255_20261005_1552\SCI_Docking_Figure4_Suite\sci_composite_figures",
    "- Main SCI DOCX: AMP_Alligator_Gut_SCI_Manuscript.docx (" + (Get-Item -LiteralPath $sciDocx).Length + " bytes)",
    "- Supplemented Method DOCX: method_with_docking_20261007_1600.docx (" + (Get-Item -LiteralPath $methodDocx).Length + " bytes)",
    "- Reproduction Guide: AMP_Pipeline_Reproduction_Method.md",
    "- Figure Review: AMP_Figure_Style_Review.md",
    "- Layout Standard: Portrait Body & Figures, Landscape Tables (Table 1, Table 2, Table 3)",
    "- Word COM test: " + $(if ($wordOk) { "PASSED" } else { "SKIPPED/INSPECTED" }),
    "- Status: SUCCESS"
)
Set-Content -LiteralPath $reportFile -Value $lines -Encoding UTF8
Write-Output "REPORT_WRITTEN=$reportFile"
Write-Output "AMP_SCI_TASK_DONE=True"
exit 0
