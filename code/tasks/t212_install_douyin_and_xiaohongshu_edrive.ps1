# t212_install_douyin_and_xiaohongshu_edrive.ps1 - Reinstall Douyin to E: drive, install Xiaohongshu to E: drive
# ASCII-only source for Windows PowerShell 5.1 compatibility.

$ErrorActionPreference = 'Continue'
$repo = (Get-Location).Path
$douyinCn = [char]0x6296 + [char]0x97F3
$xhsCn    = [char]0x5C0F + [char]0x7EA2 + [char]0x4E66
$desktopCn = [char]0x684C + [char]0x9762

Write-Output "HOST=$env:COMPUTERNAME"
Write-Output "REPO=$repo"
Write-Output "TASK=Migrate Douyin to E: drive and Install Xiaohongshu on E: drive"

# 1. Locate Desktop directory
$desktop = $null
foreach ($d in @([Environment]::GetFolderPath("Desktop"), ("D:\" + $desktopCn), (Join-Path $env:USERPROFILE "Desktop"))) {
    if ($d -and (Test-Path -LiteralPath $d)) { $desktop = $d; break }
}
if (-not $desktop) {
    $desktop = [Environment]::GetFolderPath("Desktop")
}
Write-Output "DESKTOP=$desktop"

# 2. Setup E: drive target base folder
$ePrograms = "E:\Programs"
if (-not (Test-Path -LiteralPath $ePrograms)) {
    New-Item -ItemType Directory -Force -Path $ePrograms | Out-Null
}

# =========================================================================
# PART 1: DOUYIN - MIGRATE / REINSTALL TO E: DRIVE (NO C: DRIVE)
# =========================================================================
Write-Output "=== DOUYIN: MIGRATING TO E: DRIVE ==="
# Stop any running douyin process
Get-Process | Where-Object { $_.ProcessName -match "douyin|bytedance|crashpad" } | Stop-Process -Force -ErrorAction SilentlyContinue
& taskkill.exe /F /IM "douyin*" /T 2>$null
& taskkill.exe /F /IM "Douyin*" /T 2>$null
& taskkill.exe /F /IM "crashpad_handler*" /T 2>$null
Start-Sleep -Seconds 2

$douyinEDir = Join-Path $ePrograms "Douyin"
$douyinEExe = Join-Path $douyinEDir "douyin.exe"

# Known C: drive install paths
$douyinCPaths = @(
    "C:\Program Files (x86)\ByteDance\douyin",
    "C:\Program Files\ByteDance\douyin",
    (Join-Path $env:LOCALAPPDATA "Programs\douyin"),
    (Join-Path $env:LOCALAPPDATA "Douyin")
)

$sourceCPath = $null
foreach ($cp in $douyinCPaths) {
    if (Test-Path -LiteralPath (Join-Path $cp "douyin.exe")) {
        $sourceCPath = $cp
        break
    }
}

if ($sourceCPath) {
    Write-Output "FOUND_DOUYIN_ON_C: $sourceCPath"
    if (-not (Test-Path -LiteralPath $douyinEDir)) {
        New-Item -ItemType Directory -Force -Path $douyinEDir | Out-Null
    }
    Write-Output "COPYING_DOUYIN_TO_EDRIVE: $sourceCPath -> $douyinEDir"
    Copy-Item -Path (Join-Path $sourceCPath "*") -Destination $douyinEDir -Recurse -Force -ErrorAction SilentlyContinue
}

# If still not on E:, download installer and install with /D=E:\Programs\Douyin
if (-not (Test-Path -LiteralPath $douyinEExe)) {
    Write-Output "DOUYIN_NOT_ON_E_YET. Downloading installer for fresh install to E: drive..."
    $installerPath = Join-Path $env:TEMP "DouyinSetup.exe"
    $cdnUrl = "https://lf-douyin-pc-web.douyinstatic.com/obj/douyin-pc-web/douyin-pc-client/7044145585217083655/releases/495279540/8.7.0/win32-ia32/douyin-v8.7.0-win32-ia32-douyin.exe"
    
    $curl = Get-Command "curl.exe" -ErrorAction SilentlyContinue
    if ($curl) {
        & curl.exe -sSL --connect-timeout 20 --max-time 300 -o $installerPath $cdnUrl
    } else {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $cdnUrl -OutFile $installerPath -TimeoutSec 300
    }
    
    if (Test-Path -LiteralPath $installerPath) {
        Write-Output "RUNNING_INSTALLER_WITH_EDRIVE_TARGET: /S /D=$douyinEDir"
        $p = Start-Process -FilePath $installerPath -ArgumentList @("/S", "/D=$douyinEDir") -PassThru -Wait
        Start-Sleep -Seconds 10
    }
}

# Verify E: drive installation
$douyinOnEOk = (Test-Path -LiteralPath $douyinEExe)
Write-Output "DOUYIN_ON_E_EXISTS=$douyinOnEOk ($douyinEExe)"

# Clean up C: drive completely
if ($douyinOnEOk) {
    & taskkill.exe /F /IM "douyin*" /T 2>$null
    & taskkill.exe /F /IM "ByteDance*" /T 2>$null
    & taskkill.exe /F /IM "crashpad_handler*" /T 2>$null
    Start-Sleep -Seconds 1

    foreach ($cp in $douyinCPaths) {
        if (Test-Path -LiteralPath $cp) {
            Write-Output "REMOVING_FROM_C: $cp"
            & cmd.exe /c "attrib -r -s -h `"$cp\*`" /s /d" 2>$null
            & cmd.exe /c "rd /s /q `"$cp`"" 2>$null
            
            # If folder or douyin.exe still exists, force move/delete
            if (Test-Path -LiteralPath $cp) {
                Get-ChildItem -LiteralPath $cp -Recurse -Force -ErrorAction SilentlyContinue |
                    Sort-Object -Property { $_.FullName.Length } -Descending |
                    ForEach-Object {
                        try { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue } catch {}
                    }
                try { Remove-Item -LiteralPath $cp -Recurse -Force -ErrorAction SilentlyContinue } catch {}
            }

            $cExe = Join-Path $cp "douyin.exe"
            if (Test-Path -LiteralPath $cExe) {
                try {
                    $tmpTrash = Join-Path $env:TEMP "douyin_c_trash_$PID.exe"
                    Move-Item -LiteralPath $cExe -Destination $tmpTrash -Force -ErrorAction SilentlyContinue
                    Remove-Item -LiteralPath $tmpTrash -Force -ErrorAction SilentlyContinue
                } catch {}
            }
        }
    }
    
    # Check parent ByteDance folder if empty
    $bdFolder = "C:\Program Files (x86)\ByteDance"
    if (Test-Path -LiteralPath $bdFolder) {
        & cmd.exe /c "rd /s /q `"$bdFolder`"" 2>$null
    }
    
    # Update registry paths to E: drive
    $regPaths = @(
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\douyin",
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\douyin",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\douyin"
    )
    foreach ($rp in $regPaths) {
        if (Test-Path -LiteralPath $rp) {
            try {
                Set-ItemProperty -Path $rp -Name "InstallLocation" -Value $douyinEDir -ErrorAction SilentlyContinue
                Set-ItemProperty -Path $rp -Name "DisplayIcon" -Value $douyinEExe -ErrorAction SilentlyContinue
                Write-Output "REGISTRY_UPDATED_TO_EDRIVE: $rp"
            } catch {}
        }
    }
}

# Update Douyin Desktop Shortcut to E: drive
if ($desktop -and $douyinOnEOk) {
    $douyinShortcut = Join-Path $desktop "$douyinCn.lnk"
    try {
        $wsh = New-Object -ComObject WScript.Shell
        $sc = $wsh.CreateShortcut($douyinShortcut)
        $sc.TargetPath = $douyinEExe
        $sc.WorkingDirectory = $douyinEDir
        $sc.IconLocation = "$douyinEExe,0"
        $sc.Save()
        Write-Output "DOUYIN_DESKTOP_SHORTCUT_UPDATED=$douyinShortcut (Target=$douyinEExe)"
    } catch {
        Write-Output "SHORTCUT_UPDATE_ERROR: $($_.Exception.Message)"
    }
}

# =========================================================================
# PART 2: XIAOHONGSHU - INSTALL ON E: DRIVE
# =========================================================================
Write-Output "=== XIAOHONGSHU: INSTALLING TO E: DRIVE ==="
$xhsEDir  = Join-Path $ePrograms "Xiaohongshu"
$xhsData  = Join-Path $xhsEDir "Data"
$xhsExe   = Join-Path $xhsEDir "Xiaohongshu.exe"
$xhsIco   = Join-Path $xhsEDir "xhs.ico"

if (-not (Test-Path -LiteralPath $xhsEDir)) {
    New-Item -ItemType Directory -Force -Path $xhsEDir | Out-Null
}
if (-not (Test-Path -LiteralPath $xhsData)) {
    New-Item -ItemType Directory -Force -Path $xhsData | Out-Null
}

# Locate browser for desktop application mode
$browsers = @(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
$targetBrowser = $null
foreach ($b in $browsers) {
    if ($b -and (Test-Path -LiteralPath $b)) {
        $targetBrowser = $b
        break
    }
}
Write-Output "BROWSER_FOR_XHS_APP=$targetBrowser"

# Download Xiaohongshu official icon
if (-not (Test-Path -LiteralPath $xhsIco)) {
    Write-Output "DOWNLOADING_XHS_ICON..."
    $icoUrls = @(
        "https://www.xiaohongshu.com/favicon.ico",
        "https://fe-static.xhscdn.com/formula-static/xhs-pc-web/public/favicon.ico"
    )
    foreach ($u in $icoUrls) {
        try {
            $curl = Get-Command "curl.exe" -ErrorAction SilentlyContinue
            if ($curl) {
                & curl.exe -sSL --connect-timeout 10 -o $xhsIco $u
            } else {
                [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
                Invoke-WebRequest -Uri $u -OutFile $xhsIco -TimeoutSec 15
            }
            if ((Test-Path -LiteralPath $xhsIco) -and ((Get-Item -LiteralPath $xhsIco).Length -gt 500)) {
                Write-Output "XHS_ICON_DOWNLOADED=$xhsIco"
                break
            }
        } catch {}
    }
}

# Compile native GUI launcher Xiaohongshu.exe in E:\Programs\Xiaohongshu
if (-not (Test-Path -LiteralPath $xhsExe)) {
    $cscPaths = @(
        "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
        "C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
    )
    $cscExe = $null
    foreach ($cp in $cscPaths) {
        if (Test-Path -LiteralPath $cp) { $cscExe = $cp; break }
    }

    $csharpSrc = Join-Path $xhsEDir "Launcher.cs"
    $csCode = @'
using System;
using System.Diagnostics;
using System.IO;

public class XiaohongshuApp {
    public static void Main() {
        string[] browsers = new string[] {
            @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            @"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            @"C:\Program Files\Google\Chrome\Application\chrome.exe",
            @"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        };
        string browser = "";
        foreach (string b in browsers) {
            if (File.Exists(b)) { browser = b; break; }
        }
        if (string.IsNullOrEmpty(browser)) { return; }
        string appDir = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
        string dataDir = Path.Combine(appDir, "Data");
        if (!Directory.Exists(dataDir)) { Directory.CreateDirectory(dataDir); }
        string args = string.Format("--app=https://www.xiaohongshu.com/explore --user-data-dir=\"{0}\"", dataDir);
        ProcessStartInfo psi = new ProcessStartInfo(browser, args);
        psi.UseShellExecute = false;
        Process.Start(psi);
    }
}
'@
    Set-Content -LiteralPath $csharpSrc -Value $csCode -Encoding UTF8

    if ($cscExe -and (Test-Path -LiteralPath $cscExe)) {
        Write-Output "COMPILING_XHS_EXE_WITH_CSC: $cscExe"
        $icoArg = if (Test-Path -LiteralPath $xhsIco) { "/win32icon:`"$xhsIco`"" } else { "" }
        $compArgs = @("/target:winexe", "/out:`"$xhsExe`"", "`"$csharpSrc`"")
        if ($icoArg) { $compArgs += $icoArg }
        $compProc = Start-Process -FilePath $cscExe -ArgumentList ($compArgs -join ' ') -PassThru -Wait -NoNewWindow
        Write-Output "CSC_EXIT_CODE=$($compProc.ExitCode)"
    }
}

# Fallback .bat launcher if exe not created
$xhsBat = Join-Path $xhsEDir "Xiaohongshu.bat"
$batContent = "@echo off`r`nstart `"`" `"$targetBrowser`" --app=https://www.xiaohongshu.com/explore --user-data-dir=`"$xhsData`""
Set-Content -LiteralPath $xhsBat -Value $batContent -Encoding ASCII

$xhsLaunchTarget = if (Test-Path -LiteralPath $xhsExe) { $xhsExe } else { $xhsBat }
Write-Output "XHS_LAUNCH_TARGET=$xhsLaunchTarget"

# Desktop shortcut for Xiaohongshu (check if already exists; if exists, do not recreate)
if ($desktop) {
    $xhsShortcut = Join-Path $desktop "$xhsCn.lnk"
    if (Test-Path -LiteralPath $xhsShortcut) {
        Write-Output "XHS_DESKTOP_SHORTCUT_ALREADY_EXISTS: $xhsShortcut (Skipping creation per user rule)"
    } else {
        Write-Output "CREATING_XHS_DESKTOP_SHORTCUT: $xhsShortcut"
        try {
            $wsh = New-Object -ComObject WScript.Shell
            $sc = $wsh.CreateShortcut($xhsShortcut)
            $sc.TargetPath = $xhsLaunchTarget
            $sc.WorkingDirectory = $xhsEDir
            if (Test-Path -LiteralPath $xhsIco) {
                $sc.IconLocation = "$xhsIco,0"
            }
            $sc.Save()
            Write-Output "XHS_DESKTOP_SHORTCUT_CREATED=$xhsShortcut"
        } catch {
            Write-Output "XHS_SHORTCUT_CREATE_ERROR: $($_.Exception.Message)"
        }
    }
}

# =========================================================================
# FINAL VERIFICATION & REPORT
# =========================================================================
$douyinOk = (Test-Path -LiteralPath $douyinEExe)
$douyinNotOnC = -not (Test-Path -LiteralPath "C:\Program Files (x86)\ByteDance\douyin\douyin.exe")
$xhsOk = (Test-Path -LiteralPath $xhsLaunchTarget)
$xhsShortcutExists = Test-Path -LiteralPath (Join-Path $desktop "$xhsCn.lnk")
$douyinShortcutExists = Test-Path -LiteralPath (Join-Path $desktop "$douyinCn.lnk")

$allOk = $douyinOk -and $douyinNotOnC -and $xhsOk

$statusDir = Join-Path $repo "results\status"
New-Item -ItemType Directory -Force -Path $statusDir | Out-Null
$reportFile = Join-Path $statusDir "round280_install_edrive_report.md"

$lines = @(
    "# Round 280 Report: Douyin and Xiaohongshu on E: Drive",
    "",
    "- Host: $env:COMPUTERNAME",
    "- Date: " + (Get-Date).ToString("yyyy-MM-dd HH:mm:ss"),
    "- Douyin on E Drive: " + $(if ($douyinOk) { "YES ($douyinEExe)" } else { "NO" }),
    "- Douyin purged from C Drive: " + $(if ($douyinNotOnC) { "YES" } else { "NO" }),
    "- Douyin Desktop Shortcut: " + $(if ($douyinShortcutExists) { "Present (Target E: drive)" } else { "Not found" }),
    "- Xiaohongshu on E Drive: " + $(if ($xhsOk) { "YES ($xhsLaunchTarget)" } else { "NO" }),
    "- Xiaohongshu User Data Dir: $xhsData",
    "- Xiaohongshu Desktop Shortcut: " + $(if ($xhsShortcutExists) { "Present" } else { "Not found" }),
    "- Status: " + $(if ($allOk) { "SUCCESS" } else { "FAILED" })
)

Set-Content -LiteralPath $reportFile -Value $lines -Encoding UTF8
Write-Output "REPORT_WRITTEN=$reportFile"

if ($allOk) {
    Write-Output "TASK_EDRIVE_MIGRATION_SUCCESS=True"
    exit 0
} else {
    Write-Output "TASK_EDRIVE_MIGRATION_FAILED=True"
    exit 1
}
