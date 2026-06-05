#!/usr/bin/env bash
# Validates repository structure and key config files for CI.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERRORS=0

check_file() {
	if [[ ! -f "$1" ]]; then
		echo "MISSING: $1"
		ERRORS=$((ERRORS + 1))
	fi
}

check_dir() {
	if [[ ! -d "$1" ]]; then
		echo "MISSING DIR: $1"
		ERRORS=$((ERRORS + 1))
	fi
}

echo "=== VRLab26 project validation ==="

check_file "VRLab26.uproject"
check_file ".gitattributes"
check_file ".gitignore"
check_file "Config/DefaultEngine.ini"
check_file "Config/DefaultGame.ini"
check_file "Config/DefaultDeviceProfiles.ini"
check_file "Config/Android/AndroidEngine.ini"
check_file "Docs/META_QUEST.md"
check_file "Plugins/README.md"
check_file "Source/VRLab26/VRLab26.Build.cs"
check_file "Source/VRLab26/Private/VRLab26.cpp"
check_file "Docs/SETUP.md"
check_file "Docs/ARCHITECTURE.md"

check_dir "Content/VRLab26"
check_dir "Art/Blender"
check_dir "Source/VRLab26/Public/VR"

# Validate uproject JSON
if command -v python3 >/dev/null 2>&1; then
	python3 -c "import json; json.load(open('VRLab26.uproject'))" && echo "[OK] VRLab26.uproject is valid JSON"
else
	echo "[SKIP] python3 not available for JSON validation"
fi

# Ensure Git LFS tracks uasset
if grep -q '\*\.uasset filter=lfs' .gitattributes 2>/dev/null; then
	echo "[OK] Git LFS configured for .uasset"
else
	echo "WARN: .uasset not in .gitattributes LFS rules"
	ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
	echo ""
	echo "Validation failed with $ERRORS error(s)."
	exit 1
fi

echo ""
echo "All checks passed."
