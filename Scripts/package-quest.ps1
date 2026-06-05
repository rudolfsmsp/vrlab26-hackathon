#Requires -Version 5.1
<#
.SYNOPSIS
    Package VRLab26 for Meta Quest 2/3 (Android ASTC).
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$UProject = Join-Path $ProjectRoot "VRLab26.uproject"

$UeCandidates = @(
	"$env:ProgramFiles\Epic Games\UE_5.5",
	"$env:ProgramFiles\Epic Games\UE_5.6",
	"$env:ProgramFiles\Epic Games\UE_5.7"
)

$UeRoot = $UeCandidates | Where-Object { Test-Path (Join-Path $_ "Engine\Build\BatchFiles\RunUAT.bat") } | Select-Object -First 1
if (-not $UeRoot) {
	Write-Error "Unreal Engine 5.5+ not found. Install via Epic Games Launcher."
}

$MetaPlugin = Join-Path $ProjectRoot "Plugins\MetaXR\OculusXR.uplugin"
if (-not (Test-Path $MetaPlugin)) {
	Write-Warning "Meta XR plugin not found at Plugins/MetaXR/. Install before Quest packaging."
	Write-Warning "See Plugins/README.md and Docs/META_QUEST.md"
}

$RunUAT = Join-Path $UeRoot "Engine\Build\BatchFiles\RunUAT.bat"
$OutputDir = Join-Path $ProjectRoot "Build\Quest"

Write-Host "=== Packaging VRLab26 for Meta Quest (Android ASTC) ===" -ForegroundColor Cyan
Write-Host "Output: $OutputDir"

& $RunUAT BuildCookRun `
	-project="$UProject" `
	-noP4 `
	-platform=Android `
	-clientconfig=Development `
	-cook `
	-allmaps `
	-build `
	-stage `
	-pak `
	-archive `
	-archivedirectory="$OutputDir" `
	-prereqs `
	-compressed

Write-Host ""
Write-Host "Done. Install the APK from $OutputDir via Meta Quest Developer Hub or adb." -ForegroundColor Green
Write-Host "See Docs/META_QUEST.md for install steps."
