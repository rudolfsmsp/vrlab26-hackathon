#!/usr/bin/env bash
# Package VRLab26 for Meta Quest 2/3 (Android ASTC)
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UPROJECT="$PROJECT_ROOT/VRLab26.uproject"
OUTPUT_DIR="$PROJECT_ROOT/Build/Quest"

UE_ROOT=""
for candidate in \
	"$HOME/UnrealEngine" \
	"/opt/UnrealEngine" \
	"$HOME/Epic/UnrealEngine"; do
	if [[ -f "$candidate/Engine/Build/BatchFiles/RunUAT.sh" ]]; then
		UE_ROOT="$candidate"
		break
	fi
done

if [[ -z "$UE_ROOT" ]]; then
	echo "ERROR: Unreal Engine 5.5+ not found." >&2
	exit 1
fi

if [[ ! -f "$PROJECT_ROOT/Plugins/MetaXR/OculusXR.uplugin" ]]; then
	echo "WARN: Meta XR plugin not installed. See Plugins/README.md" >&2
fi

RUNUAT="$UE_ROOT/Engine/Build/BatchFiles/RunUAT.sh"

echo "=== Packaging VRLab26 for Meta Quest (Android ASTC) ==="
echo "Output: $OUTPUT_DIR"

"$RUNUAT" BuildCookRun \
	-project="$UPROJECT" \
	-noP4 \
	-platform=Android \
	-clientconfig=Development \
	-cook -allmaps -build -stage -pak -archive \
	-archivedirectory="$OUTPUT_DIR" \
	-prereqs -compressed

echo ""
echo "Done. Install APK from $OUTPUT_DIR — see Docs/META_QUEST.md"
