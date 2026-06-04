#!/usr/bin/env bash
# VRLab26 development environment setup (Linux / macOS)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPROJECT="$PROJECT_ROOT/VRLab26.uproject"

echo "=== VRLab26 Dev Setup ==="
echo "Project: $PROJECT_ROOT"

command -v git >/dev/null 2>&1 || { echo "ERROR: Git is required." >&2; exit 1; }
echo "[OK] $(git --version)"

if command -v git-lfs >/dev/null 2>&1; then
	git lfs install >/dev/null 2>&1 || true
	cd "$PROJECT_ROOT" && git lfs pull >/dev/null 2>&1 || true
	echo "[OK] Git LFS configured"
else
	echo "[WARN] Git LFS not found — install from https://git-lfs.github.com/"
fi

# Locate Unreal Engine (common install paths)
UE_ROOT=""
for candidate in \
	"$HOME/UnrealEngine" \
	"/opt/UnrealEngine" \
	"$HOME/Epic/UnrealEngine"; do
	if [[ -f "$candidate/Engine/Build/BatchFiles/Linux/Build.sh" ]] || \
	   [[ -f "$candidate/Engine/Build/BatchFiles/Mac/Build.sh" ]]; then
		UE_ROOT="$candidate"
		break
	fi
done

if [[ -n "$UE_ROOT" ]]; then
	echo "[OK] Unreal Engine: $UE_ROOT"
	GEN_SH="$UE_ROOT/Engine/Build/BatchFiles/$(uname | sed 's/Linux/Linux/;s/Darwin/Mac/')/GenerateProjectFiles.sh"
	if [[ -f "$GEN_SH" ]]; then
		echo "Generating project files..."
		"$GEN_SH" -project="$UPROJECT" -game -engine
		echo "[OK] Project files generated"
	fi
else
	echo "[WARN] Unreal Engine not found. Install UE 5.5+ via Epic Launcher."
fi

command -v blender >/dev/null 2>&1 && echo "[OK] blender found" || echo "[--] blender not in PATH (optional)"

echo ""
echo "Next steps:"
echo "  1. Open VRLab26.uproject in Unreal Engine 5.5+"
echo "  2. Rebuild C++ modules when prompted"
echo "  3. Read Docs/SETUP.md for VR and Blender setup"
