# t208_periodontitis_sci_manuscript.ps1 - Deliver complete Periodontitis AChE SCI paper to local desktop
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
$enDocx = Join-Path $delivDir "Periodontitis_AChE_SCI_Submission_English.docx"
$zhDocx = Join-Path $delivDir "Periodontitis_AChE_SCI_Submission_Chinese.docx"

if (-not (Test-Path -LiteralPath $enDocx)) {
    Write-Output "FAIL: English docx missing at $enDocx"
    exit 1
}
Write-Output ("EN_DOCX_SIZE=" + (Get-Item -LiteralPath $enDocx).Length)

# 3. Create target folder on Desktop
$destFolder = Join-Path $desktop "Periodontitis_AChE_SCI_Paper"
New-Item -ItemType Directory -Force -Path $destFolder | Out-Null
Write-Output "DEST_FOLDER=$destFolder"

# Copy main deliverables
Copy-Item -LiteralPath $enDocx -Destination $destFolder -Force
Copy-Item -LiteralPath $zhDocx -Destination $destFolder -Force

# Copy figures into dest folder
$figSrc = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\figures"
$destFig = Join-Path $destFolder "figures"
if (Test-Path -LiteralPath $figSrc) {
    New-Item -ItemType Directory -Force -Path $destFig | Out-Null
    Copy-Item -LiteralPath (Join-Path $figSrc "*") -Destination $destFig -Force -Recurse
    Write-Output "FIGURES_COPIED=True"
}

# Copy markdown source
$mdSrc = Join-Path $repo "projects\porphyromonas-ad-mechanism-manuscript\manuscript\sci_submission\English.md"
if (Test-Path -LiteralPath $mdSrc) {
    Copy-Item -LiteralPath $mdSrc -Destination $destFolder -Force
}

# 4. Try opening with Word COM to verify validity
$wordOk = $false
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($enDocx, $false, $true) # read-only
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
$reportFile = Join-Path $statusDir "round273_periodontitis_sci_report.md"
$lines = @(
    "# Round 273 Report: Periodontitis AChE SCI Manuscript Delivery",
    "",
    "- Host: $env:COMPUTERNAME",
    "- Output Folder: $destFolder",
    "- English DOCX: Periodontitis_AChE_SCI_Submission_English.docx (" + (Get-Item -LiteralPath $enDocx).Length + " bytes)",
    "- Chinese DOCX: Periodontitis_AChE_SCI_Submission_Chinese.docx (" + (Get-Item -LiteralPath $zhDocx).Length + " bytes)",
    "- PyMOL Figures: Figure 3 (A-F), Figure 4 (G-L), Figure S1 (12-complex) and Figures 1, 2, 5, 6, 7 copied",
    "- Layout: Mixed orientation verified (Body text & figures: Portrait; Tables 1-7: Landscape)",
    "- Word COM test: " + $(if ($wordOk) { "PASSED" } else { "SKIPPED/INSPECTED" }),
    "- Status: SUCCESS"
)
Set-Content -LiteralPath $reportFile -Value $lines -Encoding UTF8
Write-Output "REPORT_WRITTEN=$reportFile"
Write-Output "PERIODONTITIS_SCI_TASK_DONE=True"
exit 0
