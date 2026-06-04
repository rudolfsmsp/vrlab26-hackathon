# VRLab26 Hackathon

OpenXR virtual reality game built with **Unreal Engine 5.5+**, **C++**, and **Blender** for the VRLab26 hackathon.

## Tech stack

| Layer | Tools |
|-------|-------|
| Game engine | Unreal Engine 5.5+ (OpenXR, Enhanced Input) |
| Code | C++17, Blueprints (future gameplay) |
| 3D art | Blender 4.x → FBX → Unreal |
| VR | OpenXR (Quest Link, SteamVR, standalone Android) |
| Version control | Git + **Git LFS** for binary assets |

## Repository layout

```
├── VRLab26.uproject       # Open project in Unreal
├── Config/                # VR & OpenXR runtime settings
├── Source/VRLab26/        # C++ (VR character, game mode)
├── Content/VRLab26/       # Unreal assets (LFS)
├── Art/Blender/           # Source art & exports (LFS)
├── Audio/Source/          # Raw audio before UE import
├── Docs/                  # Setup, architecture, VR design
├── Scripts/               # Dev environment setup
└── .github/workflows/     # CI validation
```

See [Docs/ARCHITECTURE.md](Docs/ARCHITECTURE.md) for the full system diagram.

## Quick start

### 1. Clone with Git LFS

```bash
git clone https://github.com/rudolfsmsp/vrlab26-hackathon.git
cd vrlab26-hackathon
git lfs install
git lfs pull
```

### 2. Install tools

| Tool | Link |
|------|------|
| Unreal Engine 5.5+ | [unrealengine.com/download](https://www.unrealengine.com/download) |
| Visual Studio 2022 (C++) | [visualstudio.com](https://visualstudio.microsoft.com/) |
| Blender 4.x | [blender.org/download](https://www.blender.org/download/) |
| Git LFS | [git-lfs.github.com](https://git-lfs.github.com/) |

### 3. Generate project & open

**Windows:**

```powershell
.\Scripts\setup-dev.ps1
# Then double-click VRLab26.uproject
```

**Linux / macOS:**

```bash
chmod +x Scripts/*.sh
./Scripts/setup-dev.sh
```

Allow Unreal to compile C++ modules on first open. Connect a VR headset and use **VR Preview** to play.

Full instructions: **[Docs/SETUP.md](Docs/SETUP.md)**

## Documentation

| Doc | Description |
|-----|-------------|
| [SETUP.md](Docs/SETUP.md) | Install UE, OpenXR, Blender, build from source |
| [ARCHITECTURE.md](Docs/ARCHITECTURE.md) | Repo structure & system layers |
| [BLENDER_PIPELINE.md](Docs/BLENDER_PIPELINE.md) | Blender → Unreal export workflow |
| [VR_DESIGN.md](Docs/VR_DESIGN.md) | Comfort, performance, interaction guidelines |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Branching, LFS, PR checklist |

## C++ VR foundation

The project includes a minimal OpenXR-ready foundation:

- `AVRLab26GameMode` — assigns VR pawn & controller
- `AVRLab26VRCharacter` — HMD camera + left/right motion controllers
- `AVRLab26VRPlayerController` — enables HMD at play start

Extend under `Source/VRLab26/Public/` as gameplay systems are added.

## CI

GitHub Actions runs on every push/PR:

- **Validate Project** — structure, JSON, required plugins
- **LFS Check** — warns when large binaries skip LFS

## License

Hackathon project — add a license before public release if needed.
