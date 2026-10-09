# restore_watch.ps1 - Focus and register git-sync watch for this repository
# ASCII-only source for Windows PowerShell 5.1 compatibility.

$ErrorActionPreference = "Continue"
$repo = (Get-Location).Path
Write-Host "== Restoring watcher for repo: $repo" -ForegroundColor Cyan

# 1. Clear any stale lock files in TEMP
Get-ChildItem $env:TEMP -Filter "*.lock" -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match "git|sync|arena|watch" } |
  ForEach-Object {
    Write-Host ("  clearing stale lock: " + $_.Name)
    Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
  }

# 2. Re-register and focus watcher
$watch = Join-Path $repo "watch.ps1"
if (Test-Path -LiteralPath $watch) {
  Write-Host "== Step 1: Focusing watcher (pausing others)..." -ForegroundColor Green
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $watch -Focus
  
  Write-Host "== Step 2: Registering scheduled task..." -ForegroundColor Green
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $watch -Register
  
  Write-Host "== Step 3: Triggering immediate one-shot poll..." -ForegroundColor Green
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $watch
} else {
  Write-Host "FAIL: watch.ps1 not found in $repo" -ForegroundColor Red
}
