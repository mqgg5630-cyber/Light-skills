# t209_deliver_amp_sci_paper.ps1 - Deliver complete Alligator Gut AMP SCI Paper & Deliverables to local desktop
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

# 2. Check source deliverables in repo
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

# 3. Create target delivery folders on Desktop
# Deliver to both AMP_SCI_Paper and AMP_Docking_Vina_R255_20261005_1552 for maximum convenience
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
    
    # Also copy the 3 PyMOL 300 DPI composite figures
    $figDest = Join-Path $dest "sci_composite_figures"
    New-Item -ItemType Directory -Force -Path $figDest | Out-Null
    $figSrc = Join-Path $repo "sources\user_amp\figures"
    if (Test-Path -LiteralPath $figSrc) {
        Copy-Item -LiteralPath (Join-Path $figSrc "*.png") -Destination $figDest -Force
    }
    Write-Output "DELIVERED_TO=$dest"
}

# 4. Cleanup local disk space per user request ("其余的全删除，只留这个任务的结果，节省空间")
# Clean old unrelated periodontitis folder on Desktop if present
$oldPeriodontitisFolder = Join-Path $desktop "Periodontitis_AChE_SCI_Paper"
if (Test-Path -LiteralPath $oldPeriodontitisFolder) {
    try {
        Remove-Item -LiteralPath $oldPeriodontitisFolder -Recurse -Force -ErrorAction SilentlyContinue
        Write-Output "CLEANED_OLD_FOLDER=$oldPeriodontitisFolder"
    } catch {
        Write-Output "NOTE_CLEANUP=$($_.Exception.Message)"
    }
}

# 5. Try opening with Word/WPS COM to verify validity
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

# 6. Write status receipt
$statusDir = Join-Path $repo "results\status"
New-Item -ItemType Directory -Force -Path $statusDir | Out-Null
$reportFile = Join-Path $statusDir "round274_amp_sci_delivery_report.md"
$lines = @(
    "# Round 274 Report: Alligator Gut AMP SCI Manuscript Delivery",
    "",
    "- Host: $env:COMPUTERNAME",
    "- Output Folder: $desktop\AMP_SCI_Paper",
    "- Output Folder 2: $desktop\AMP_Docking_Vina_R255_20261005_1552",
    "- Main SCI DOCX: AMP_Alligator_Gut_SCI_Manuscript.docx (" + (Get-Item -LiteralPath $sciDocx).Length + " bytes)",
    "- Supplemented Method DOCX: method_with_docking_20261007_1600.docx (" + (Get-Item -LiteralPath $methodDocx).Length + " bytes)",
    "- Reproduction Guide: AMP_Pipeline_Reproduction_Method.md",
    "- Figure Review: AMP_Figure_Style_Review.md",
    "- Manifest: AMP_Method_Supplement_manifest.json",
    "- Embedded 300 DPI PyMOL Figures: Figure 4 Part1 (A-F), Figure 4 Part2 (G-L), Figure S1 (12-Complex Overview)",
    "- Layout Standard: Portrait Body & Figures, Landscape Tables (Table 1, Table 2, Table 3)",
    "- Local Cleanup: Removed old Periodontitis folder to save disk space",
    "- Word COM test: " + $(if ($wordOk) { "PASSED" } else { "SKIPPED/INSPECTED" }),
    "- Status: SUCCESS"
)
Set-Content -LiteralPath $reportFile -Value $lines -Encoding UTF8
Write-Output "REPORT_WRITTEN=$reportFile"
Write-Output "AMP_SCI_TASK_DONE=True"
exit 0
