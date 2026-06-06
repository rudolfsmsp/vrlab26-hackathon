#Requires -Version 5.1
<#
.SYNOPSIS
    Upload environment.fbx from Desktop to GitHub (Git LFS, correct folder).
.DESCRIPTION
    Run from the repo root after cloning:
      .\Scripts\upload-environment.ps1

    Default source: C:\Users\rudol\Desktop\environment.fbx
    Target: Art/Blender/Exports/Environments/environment.fbx
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$SourceFile = "C:\Users\rudol\Desktop\environment.fbx"
$DestDir = Join-Path $ProjectRoot "Art\Blender\Exports\Environments"
$DestFile = Join-Path $DestDir "environment.fbx"

Write-Host "=== Upload environment.fbx to GitHub ===" -ForegroundColor Cyan
Write-Host "Repo:   $ProjectRoot"
Write-Host "Source: $SourceFile"
Write-Host "Dest:   $DestFile"
Write-Host ""

if (-not (Test-Path $SourceFile)) {
    Write-Error "File not found: $SourceFile`nPlace environment.fbx on your Desktop or pass -SourceFile 'C:\path\to\environment.fbx'"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed. Install from https://git-scm.com/"
}

Push-Location $ProjectRoot

try {
    if (-not (Get-Command git-lfs -ErrorAction SilentlyContinue)) {
        Write-Warning "Git LFS not found — install from https://git-lfs.github.com/"
    } else {
        git lfs install | Out-Null
    }

    Write-Host "[1/5] Pulling latest from GitHub..."
    git pull origin main

    Write-Host "[2/5] Copying FBX to Art/Blender/Exports/Environments/..."
    New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
    Copy-Item -Path $SourceFile -Destination $DestFile -Force

    Write-Host "[3/5] Staging with Git LFS..."
    git add $DestFile
    git lfs status

    $Status = git status --porcelain
    if (-not $Status) {
        Write-Host "Nothing to commit — file may already be uploaded." -ForegroundColor Yellow
        exit 0
    }

    Write-Host "[4/5] Committing..."
    git commit -m "Add environment FBX export (Art/Blender/Exports/Environments)"

    Write-Host "[5/5] Pushing to GitHub..."
    git push origin main

    Write-Host ""
    Write-Host "Done! environment.fbx is on GitHub at:" -ForegroundColor Green
    Write-Host "  Art/Blender/Exports/Environments/environment.fbx"
    Write-Host ""
    Write-Host "Next: import into Unreal -> Content/VRLab26/Meshes/ or Maps/"
}
finally {
    Pop-Location
}
