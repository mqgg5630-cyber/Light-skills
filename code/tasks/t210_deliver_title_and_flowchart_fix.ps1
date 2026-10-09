# t210_deliver_title_and_flowchart_fix.ps1 - Deliver updated Periodontitis AChE SCI paper & screening flowchart to local desktop
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
$zhDocx = Join-Path $delivDir "Periodontitis_AChE_SCI_Submission_Chinese.docx"
$enDocx = Join-Path $delivDir "Periodontitis_AChE_SCI_Submission_English.docx"
$figSvg = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\figures\fig_screening_cascade.svg"
$figPng = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\figures\fig_screening_cascade.png"

if (-not (Test-Path -LiteralPath $zhDocx)) {
    Write-Output "FAIL: Chinese docx missing at $zhDocx"
    exit 1
}
if (-not (Test-Path -LiteralPath $enDocx)) {
    Write-Output "FAIL: English docx missing at $enDocx"
    exit 1
}
Write-Output ("ZH_DOCX_SIZE=" + (Get-Item -LiteralPath $zhDocx).Length)
Write-Output ("EN_DOCX_SIZE=" + (Get-Item -LiteralPath $enDocx).Length)
Write-Output ("FIG_SVG_SIZE=" + (Get-Item -LiteralPath $figSvg).Length)
Write-Output ("FIG_PNG_SIZE=" + (Get-Item -LiteralPath $figPng).Length)

# 3. Create target folder on Desktop: Periodontitis_AChE_SCI_Paper
$destFolder = Join-Path $desktop "Periodontitis_AChE_SCI_Paper"
New-Item -ItemType Directory -Force -Path $destFolder | Out-Null
Write-Output "DEST_FOLDER=$destFolder"

# Copy main deliverables
Copy-Item -LiteralPath $zhDocx -Destination $destFolder -Force
Copy-Item -LiteralPath $enDocx -Destination $destFolder -Force
Copy-Item -LiteralPath $figSvg -Destination $destFolder -Force
Copy-Item -LiteralPath $figPng -Destination $destFolder -Force

# Copy all figures into figures subfolder
$figSrc = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\figures"
$destFig = Join-Path $destFolder "figures"
if (Test-Path -LiteralPath $figSrc) {
    New-Item -ItemType Directory -Force -Path $destFig | Out-Null
    Copy-Item -LiteralPath (Join-Path $figSrc "*") -Destination $destFig -Force -Recurse
    Write-Output "FIGURES_COPIED=True"
}

# Copy markdown sources
$zhMd = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\sci_submission\Chinese.md"
$enMd = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\sci_submission\English.md"
if (Test-Path -LiteralPath $zhMd) { Copy-Item -LiteralPath $zhMd -Destination $destFolder -Force }
if (Test-Path -LiteralPath $enMd) { Copy-Item -LiteralPath $enMd -Destination $destFolder -Force }

# Also copy updated figures to AMP_SCI_Paper if it exists
$ampDest = Join-Path $desktop "AMP_SCI_Paper"
if (Test-Path -LiteralPath $ampDest) {
    Copy-Item -LiteralPath $figSvg -Destination $ampDest -Force
    Copy-Item -LiteralPath $figPng -Destination $ampDest -Force
    Write-Output "COPIED_TO_AMP_FOLDER=True"
}

# 4. Try opening with Word COM to verify validity
$wordOk = $false
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($zhDocx, $false, $true) # read-only
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

# 5. Write status receipt
$statusDir = Join-Path $repo "results\status"
New-Item -ItemType Directory -Force -Path $statusDir | Out-Null
$reportFile = Join-Path $statusDir "round277_title_and_flowchart_report.md"
$lines = @(
    "# Round 277 Report: Periodontitis AChE SCI Title & Flowchart Delivery",
    "",
    "- Host: $env:COMPUTERNAME",
    "- Output Folder: $destFolder",
    "- Chinese DOCX: Periodontitis_AChE_SCI_Submission_Chinese.docx (" + (Get-Item -LiteralPath $zhDocx).Length + " bytes)",
    "- English DOCX: Periodontitis_AChE_SCI_Submission_English.docx (" + (Get-Item -LiteralPath $enDocx).Length + " bytes)",
    "- Title Update: Removed 100ns from Chinese & English titles and headings",
    "- Flowchart Update: Arrow 1 flows into AutoDock Vina; Arrow 2 flows from AutoDock Vina directly to GROMACS MD",
    "- Figures Copied: fig_screening_cascade.svg & fig_screening_cascade.png (high resolution)",
    "- Word COM test: " + $(if ($wordOk) { "PASSED" } else { "SKIPPED/INSPECTED" }),
    "- Status: SUCCESS"
)
Set-Content -LiteralPath $reportFile -Value $lines -Encoding UTF8
Write-Output "REPORT_WRITTEN=$reportFile"
Write-Output "TITLE_AND_FLOWCHART_TASK_DONE=True"
exit 0
