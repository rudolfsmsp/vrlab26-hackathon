# Development setup

Everything you need to clone, build, and run the VRLab26 VR game locally.

## Prerequisites

### Required (all developers)

| Tool | Version | Notes |
|------|---------|-------|
| **Git** | 2.40+ | With Git LFS |
| **Git LFS** | 3.x | `git lfs install` after clone |
| **Unreal Engine** | 5.5+ | Install via Epic Games Launcher |
| **Visual Studio 2022** | Latest | Workload: *Game development with C++* (Windows) |
| **Blender** | 4.x | For 3D asset authoring |

### VR hardware / runtime

**Primary target: Meta Quest 2 & Quest 3** — see **[META_QUEST.md](./META_QUEST.md)** for Link, Meta XR plugin, and APK packaging.

| Platform | Runtime |
|----------|---------|
| Meta Quest 2/3 (PC) | Meta Quest Link + OpenXR + Meta XR plugin |
| SteamVR headsets | SteamVR + OpenXR |
| Meta Quest 2/3 (standalone) | Meta XR plugin + Android SDK + `Scripts/package-quest.ps1` |

## Quick start (Windows)

```powershell
# 1. Clone with LFS
git clone https://github.com/rudolfsmsp/vrlab26-hackathon.git
cd vrlab26-hackathon
git lfs install
git lfs pull

# 2. Run setup script (checks tools, generates project files)
.\Scripts\setup-dev.ps1

# 3. Open in Unreal
# Double-click VRLab26.uproject → "Yes" to rebuild modules
# Enable OpenXR plugin if prompted
# Play In VR (PIE) with headset connected
```

## Quick start (Linux / macOS)

Linux supports UE editor builds; macOS is editor-only (no VR PIE on Mac for most setups).

```bash
git clone https://github.com/rudolfsmsp/vrlab26-hackathon.git
cd vrlab26-hackathon
git lfs install && git lfs pull
./Scripts/setup-dev.sh
# Open VRLab26.uproject with UE 5.5+ from Epic Launcher
```

## Unreal Engine installation

1. Install [Epic Games Launcher](https://www.unrealengine.com/download).
2. Library → **+** → install **Unreal Engine 5.5** (or newer).
3. Optional components: *Android*, *Linux*, *Win64* toolchains for your targets.
4. Associate engine: right-click `VRLab26.uproject` → *Switch Unreal Engine version*.

## OpenXR / VR configuration

The project ships with these plugins enabled in `VRLab26.uproject`:

- **OpenXR** — cross-platform VR API
- **OpenXRHandTracking** — hand tracking on supported devices
- **EnhancedInput** — modern input mapping

Runtime settings live in `Config/DefaultEngine.ini` under `HMDRuntimeSettings` and `OpenXRHMDSettings`.

### Verify VR in editor

1. Connect headset and start OpenXR/SteamVR/Quest Link.
2. Editor → *Play* dropdown → **VR Preview**.
3. You should spawn as `AVRLab26VRCharacter` with tracked controllers.

## Blender setup

1. Install [Blender 4.x](https://www.blender.org/download/).
2. Set scene units: *Scene Properties → Units → Metric*, scale 0.01 for UE compatibility (1 unit = 1 cm).
3. Follow [BLENDER_PIPELINE.md](./BLENDER_PIPELINE.md) for export/import.

## Building from command line

```powershell
# Windows — generate VS solution
& "C:\Program Files\Epic Games\UE_5.5\Engine\Build\BatchFiles\Build.bat" VRLab26Editor Win64 Development -Project="$PWD\VRLab26.uproject" -WaitMutex
```

Adjust the UE install path to match your machine.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| LFS files show as pointers | Run `git lfs pull` |
| Module failed to load | Rebuild from `.uproject` or regenerate project files |
| No VR in PIE | Confirm OpenXR runtime is active; use VR Preview |
| Android build fails | Install Android Studio + NDK via UE *Platforms* settings |

## GitHub LFS quota

Binary assets consume LFS bandwidth and storage. Keep high-res sources in `Art/Blender/` and only commit optimized exports needed in-engine.
