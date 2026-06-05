#Requires -Version 5.1
<#
.SYNOPSIS
    VRLab26 development environment setup (Windows).
.DESCRIPTION
    Verifies Git LFS, locates Unreal Engine, and generates Visual Studio project files.
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$UProject = Join-Path $ProjectRoot "VRLab26.uproject"

Write-Host "=== VRLab26 Dev Setup ===" -ForegroundColor Cyan
Write-Host "Project: $ProjectRoot"

function Test-Command($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

# Git LFS
if (-not (Test-Command "git")) {
    Write-Error "Git is not installed. Install from https://git-scm.com/"
}
Write-Host "[OK] Git $(git --version)"

if (-not (Test-Command "git-lfs")) {
    Write-Warning "Git LFS not found. Install from https://git-lfs.github.com/ then run: git lfs install"
} else {
    git lfs install 2>$null | Out-Null
    Push-Location $ProjectRoot
    git lfs pull 2>$null | Out-Null
    Pop-Location
    Write-Host "[OK] Git LFS configured"
}

# Find Unreal Engine
$UeCandidates = @(
    "$env:ProgramFiles\Epic Games\UE_5.5",
    "$env:ProgramFiles\Epic Games\UE_5.6",
    "$env:ProgramFiles\Epic Games\UE_5.7",
    "${env:ProgramFiles(x86)}\Epic Games\Launcher\Engine\Binaries\Win64"
)

$UeRoot = $UeCandidates | Where-Object { Test-Path (Join-Path $_ "Engine\Build\BatchFiles\Build.bat") } | Select-Object -First 1

if (-not $UeRoot) {
    Write-Warning "Unreal Engine 5.5+ not found in default paths."
    Write-Warning "Install via Epic Games Launcher, then re-run this script."
} else {
    Write-Host "[OK] Unreal Engine: $UeRoot"
    $BuildBat = Join-Path $UeRoot "Engine\Build\BatchFiles\Build.bat"
    $GenBat = Join-Path $UeRoot "Engine\Build\BatchFiles\GenerateProjectFiles.bat"

    if (Test-Path $GenBat) {
        Write-Host "Generating Visual Studio project files..."
        & $GenBat -project="$UProject" -game -engine -progress
        Write-Host "[OK] Project files generated"
    } else {
        Write-Warning "GenerateProjectFiles.bat not found. Open .uproject in Unreal Editor to generate."
    }
}

# Optional tools
foreach ($tool in @("blender")) {
    if (Test-Command $tool) {
        Write-Host "[OK] $tool found"
    } else {
        Write-Host "[--] $tool not in PATH (optional for artists)" -ForegroundColor DarkYellow
    }
}

Write-Host ""
$MetaPlugin = Join-Path $ProjectRoot "Plugins\MetaXR\OculusXR.uplugin"
if (Test-Path $MetaPlugin) {
    Write-Host "[OK] Meta XR plugin found (Quest 2/3 standalone ready)"
} else {
    Write-Host "[!!] Meta XR plugin NOT installed — required for Quest APK builds" -ForegroundColor Yellow
    Write-Host "     See Plugins/README.md and Docs/META_QUEST.md"
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Open VRLab26.uproject in Unreal Engine 5.5+"
Write-Host "  2. Allow C++ module rebuild when prompted"
Write-Host "  3. Install Meta XR plugin for Quest 2/3 (Plugins/README.md)"
Write-Host "  4. Connect Quest via Link and use VR Preview"
Write-Host "  5. Read Docs/META_QUEST.md for standalone APK builds"
Write-Host "  6. Read Docs/SETUP.md for full documentation"
