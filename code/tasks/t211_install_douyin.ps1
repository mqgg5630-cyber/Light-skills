# t211_install_douyin.ps1 - Automated installation of Douyin (TikTok PC client) on Windows
# ASCII-only source for Windows PowerShell 5.1 compatibility.

$ErrorActionPreference = 'Continue'
$repo = (Get-Location).Path
$douyinCn = [char]0x6296 + [char]0x97F3
$desktopCn = [char]0x684C + [char]0x9762

Write-Output "HOST=$env:COMPUTERNAME"
Write-Output "REPO=$repo"
Write-Output "TASK=Install Douyin ($douyinCn)"

# 1. Locate Desktop directory
$desktop = $null
foreach ($d in @([Environment]::GetFolderPath("Desktop"), ("D:\" + $desktopCn), (Join-Path $env:USERPROFILE "Desktop"))) {
    if ($d -and (Test-Path -LiteralPath $d)) { $desktop = $d; break }
}
if (-not $desktop) {
    $desktop = [Environment]::GetFolderPath("Desktop")
}
Write-Output "DESKTOP=$desktop"

# Function to search for installed Douyin
function Find-Douyin {
    # A. Check registry uninstall entries
    $regPaths = @(
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    foreach ($rp in $regPaths) {
        try {
            $items = Get-ItemProperty -Path $rp -ErrorAction SilentlyContinue
            foreach ($it in $items) {
                $dn = [string]$it.DisplayName
                if ($dn -match "Douyin" -or $dn -match $douyinCn) {
                    $loc = [string]$it.InstallLocation
                    $displayIcon = [string]$it.DisplayIcon
                    $ver = [string]$it.DisplayVersion
                    Write-Output "FOUND_IN_REGISTRY: $dn version=$ver loc=$loc icon=$displayIcon"
                    return @{
                        Name = $dn
                        Version = $ver
                        Location = $loc
                        Icon = $displayIcon
                        Method = "Registry"
                    }
                }
            }
        } catch {}
    }

    # B. Check known executable file paths
    $possibleExes = @(
        (Join-Path $env:LOCALAPPDATA "Programs\douyin\douyin.exe"),
        (Join-Path $env:LOCALAPPDATA "Douyin\douyin.exe"),
        (Join-Path $env:ProgramFiles "Douyin\douyin.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Douyin\douyin.exe"),
        (Join-Path $env:APPDATA "Douyin\douyin.exe")
    )
    foreach ($pe in $possibleExes) {
        if ($pe -and (Test-Path -LiteralPath $pe)) {
            Write-Output "FOUND_EXE: $pe"
            return @{
                Name = "Douyin"
                Version = (Get-Item -LiteralPath $pe).VersionInfo.ProductVersion
                Location = (Split-Path -Parent $pe)
                Icon = $pe
                Method = "Path"
            }
        }
    }

    # C. Check desktop and start menu shortcuts
    $shortcutDirs = @(
        $desktop,
        (Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"),
        (Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs")
    )
    foreach ($sd in $shortcutDirs) {
        if ($sd -and (Test-Path -LiteralPath $sd)) {
            $links = Get-ChildItem -LiteralPath $sd -Filter "*.lnk" -Recurse -ErrorAction SilentlyContinue
            foreach ($lk in $links) {
                if ($lk.Name -match "Douyin" -or $lk.Name -match $douyinCn) {
                    Write-Output "FOUND_SHORTCUT: $($lk.FullName)"
                    return @{
                        Name = "Douyin"
                        Version = "Shortcut"
                        Location = $lk.FullName
                        Icon = $lk.FullName
                        Method = "Shortcut"
                    }
                }
            }
        }
    }

    return $null
}

# 2. Check if already installed
$info = Find-Douyin
$alreadyInstalled = $false
if ($info) {
    Write-Output "DOUYIN_ALREADY_INSTALLED=True"
    $alreadyInstalled = $true
} else {
    Write-Output "DOUYIN_NOT_INSTALLED_YET=True. Proceeding with installation..."

    # 3. Strategy A: Try winget first
    $wingetExe = $null
    try {
        $w = Get-Command "winget.exe" -ErrorAction SilentlyContinue
        if ($w) { $wingetExe = $w.Source }
    } catch {}

    $installedViaWinget = $false
    if ($wingetExe) {
        Write-Output "TRYING_WINGET: $wingetExe"
        try {
            $argsA = @("install", "--id", "ByteDance.Douyin", "--exact", "--silent", "--accept-package-agreements", "--accept-source-agreements")
            Write-Output "RUNNING: winget $($argsA -join ' ')"
            $p = Start-Process -FilePath $wingetExe -ArgumentList $argsA -NoNewWindow -PassThru -Wait
            Write-Output "WINGET_EXIT_CODE=$($p.ExitCode)"
            if ($p.ExitCode -eq 0) {
                $installedViaWinget = $true
            }
        } catch {
            Write-Output "WINGET_ERROR=$($_.Exception.Message)"
        }

        # Check if installed via winget
        $info = Find-Douyin
        if ($info) {
            $installedViaWinget = $true
        }
    }

    # 4. Strategy B: Direct official CDN installer download + silent install
    if (-not $info) {
        Write-Output "WINGET_NOT_COMPLETED. Trying Strategy B: Direct CDN Download..."
        $cdnUrls = @(
            "https://lf-douyin-pc-web.douyinstatic.com/obj/douyin-pc-web/douyin-pc-client/7044145585217083655/releases/495279540/8.7.0/win32-ia32/douyin-v8.7.0-win32-ia32-douyin.exe",
            "https://www.douyin.com/download/pc/obj/douyin-pc-client/douyin-pc-client.exe",
            "https://lf3-static.bytednsdoc.com/obj/eden-cn/aphqeh7nuvhnulpq/douyin_pc/DouyinSetup.exe"
        )

        $installerPath = Join-Path $env:TEMP "DouyinSetup.exe"
        $downloaded = $false

        foreach ($url in $cdnUrls) {
            Write-Output "TRYING_DOWNLOAD_URL: $url"
            try {
                if (Test-Path -LiteralPath $installerPath) {
                    Remove-Item -LiteralPath $installerPath -Force -ErrorAction SilentlyContinue
                }
                # Try curl first
                $curl = Get-Command "curl.exe" -ErrorAction SilentlyContinue
                if ($curl) {
                    Write-Output "USING_CURL: $url"
                    & curl.exe -sSL --connect-timeout 20 --max-time 300 -o $installerPath $url
                    if (Test-Path -LiteralPath $installerPath) {
                        $len = (Get-Item -LiteralPath $installerPath).Length
                        Write-Output "DOWNLOADED_BYTES=$len"
                        if ($len -gt 5000000) { $downloaded = $true; break }
                    }
                }
                # Fallback to Invoke-WebRequest
                if (-not $downloaded) {
                    Write-Output "USING_INVOKE_WEBREQUEST: $url"
                    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
                    Invoke-WebRequest -Uri $url -OutFile $installerPath -TimeoutSec 300
                    if (Test-Path -LiteralPath $installerPath) {
                        $len = (Get-Item -LiteralPath $installerPath).Length
                        Write-Output "DOWNLOADED_BYTES=$len"
                        if ($len -gt 5000000) { $downloaded = $true; break }
                    }
                }
            } catch {
                Write-Output "DOWNLOAD_FAILED_FOR_URL: $($_.Exception.Message)"
            }
        }

        if ($downloaded -and (Test-Path -LiteralPath $installerPath)) {
            Write-Output "INSTALLER_READY_AT: $installerPath ($((Get-Item -LiteralPath $installerPath).Length) bytes)"
            Write-Output "LAUNCHING_SILENT_INSTALL: /S"
            try {
                $instProc = Start-Process -FilePath $installerPath -ArgumentList "/S" -PassThru -Wait
                Write-Output "INSTALLER_PROCESS_FINISHED. ExitCode=$($instProc.ExitCode)"
            } catch {
                Write-Output "INSTALL_PROCESS_ERROR=$($_.Exception.Message)"
            }

            # Wait up to 60 seconds for background extraction to finish
            for ($wait = 1; $wait -le 12; $wait++) {
                Start-Sleep -Seconds 5
                $info = Find-Douyin
                if ($info) {
                    Write-Output "DOUYIN_DETECTED_AFTER_INSTALL_WAIT: $($info.Name) ($($info.Method))"
                    break
                }
            }
        } else {
            Write-Output "FAIL: Could not download installer from CDN"
        }
    }
}

# 5. Ensure Desktop Shortcut exists
if ($desktop) {
    $desktopShortcut = Join-Path $desktop "$douyinCn.lnk"
    if (-not (Test-Path -LiteralPath $desktopShortcut)) {
        # Search Start Menu for Douyin shortcut to copy to desktop
        $startMenuPrograms = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
        $srcShortcut = $null
        if (Test-Path -LiteralPath $startMenuPrograms) {
            $cand = Get-ChildItem -LiteralPath $startMenuPrograms -Filter "*.lnk" -Recurse | Where-Object { $_.Name -match "Douyin" -or $_.Name -match $douyinCn } | Select-Object -First 1
            if ($cand) { $srcShortcut = $cand.FullName }
        }
        if (-not $srcShortcut) {
            $commonPrograms = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs"
            if (Test-Path -LiteralPath $commonPrograms) {
                $cand = Get-ChildItem -LiteralPath $commonPrograms -Filter "*.lnk" -Recurse | Where-Object { $_.Name -match "Douyin" -or $_.Name -match $douyinCn } | Select-Object -First 1
                if ($cand) { $srcShortcut = $cand.FullName }
            }
        }
        if ($srcShortcut -and (Test-Path -LiteralPath $srcShortcut)) {
            Copy-Item -LiteralPath $srcShortcut -Destination $desktopShortcut -Force
            Write-Output "DESKTOP_SHORTCUT_COPIED=$desktopShortcut"
        } elseif ($info -and $info.Icon -and (Test-Path -LiteralPath $info.Icon)) {
            try {
                $wsh = New-Object -ComObject WScript.Shell
                $sc = $wsh.CreateShortcut($desktopShortcut)
                $sc.TargetPath = $info.Icon
                $sc.Save()
                Write-Output "DESKTOP_SHORTCUT_CREATED=$desktopShortcut"
            } catch {
                Write-Output "SHORTCUT_CREATE_NOTE=$($_.Exception.Message)"
            }
        }
    } else {
        Write-Output "DESKTOP_SHORTCUT_EXISTS=$desktopShortcut"
    }
}

# 6. Final verification & Report
$finalInfo = Find-Douyin
$statusDir = Join-Path $repo "results\status"
New-Item -ItemType Directory -Force -Path $statusDir | Out-Null
$reportFile = Join-Path $statusDir "round278_install_douyin_report.md"

$installedOk = ($null -ne $finalInfo)
$lines = @(
    "# Round 278 Report: Douyin ($douyinCn) PC Installation",
    "",
    "- Host: $env:COMPUTERNAME",
    "- Date: " + (Get-Date).ToString("yyyy-MM-dd HH:mm:ss"),
    "- Installed: " + $(if ($installedOk) { "YES" } else { "NO" }),
    "- Display Name: " + $(if ($finalInfo) { $finalInfo.Name } else { "N/A" }),
    "- Version: " + $(if ($finalInfo) { $finalInfo.Version } else { "N/A" }),
    "- Location: " + $(if ($finalInfo) { $finalInfo.Location } else { "N/A" }),
    "- Detection Method: " + $(if ($finalInfo) { $finalInfo.Method } else { "N/A" }),
    "- Desktop Shortcut: " + $(if (Test-Path -LiteralPath (Join-Path $desktop "$douyinCn.lnk")) { "Present" } else { "Not found" }),
    "- Status: " + $(if ($installedOk) { "SUCCESS" } else { "FAILED" })
)

Set-Content -LiteralPath $reportFile -Value $lines -Encoding UTF8
Write-Output "REPORT_WRITTEN=$reportFile"

if ($installedOk) {
    Write-Output "INSTALL_DOUYIN_TASK_SUCCESS=True"
    exit 0
} else {
    Write-Output "INSTALL_DOUYIN_TASK_FAILED=True"
    exit 1
}
