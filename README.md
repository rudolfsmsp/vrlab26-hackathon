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
| VR headsets | **Meta Quest 2 & Quest 3** (Link + standalone APK) |

## Meta Quest 2 / 3

This project is configured for **Meta Quest 2** and **Quest 3** via Unreal Engine + OpenXR:

| Path | Use |
|------|-----|
| **PC VR** | Quest Link → Unreal **VR Preview** (fastest for daily dev) |
| **Standalone** | Package Android APK → install on headset |

**Setup guide:** **[Docs/META_QUEST.md](Docs/META_QUEST.md)**  
**Meta XR plugin install:** **[Plugins/README.md](Plugins/README.md)** (required once per machine, not in Git)

```powershell
# Package for Quest after Android SDK is configured
.\Scripts\package-quest.ps1
```


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

**New to the repo?** Read **[Docs/ARCHITECTURE_README.md](Docs/ARCHITECTURE_README.md)** — where to put code, art, audio, and config (and why).

See also [Docs/ARCHITECTURE.md](Docs/ARCHITECTURE.md) for the system diagram.

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
## Git & GitHub cheatsheet (copy & paste)

New to Git? Run these commands in a terminal from the project folder (`vrlab26-hackathon/`).

> **Tip:** Install [Git](https://git-scm.com/downloads) and [Git LFS](https://git-lfs.github.com/) first. On Windows, use **Git Bash** or PowerShell.

### First time — get the project

```bash
git clone https://github.com/rudolfsmsp/vrlab26-hackathon.git
cd vrlab26-hackathon
git lfs install
git lfs pull
```

### Every day — get the latest changes from GitHub

```bash
cd vrlab26-hackathon
git pull origin main
git lfs pull
```

### See what changed locally

```bash
git status                  # changed / new / deleted files
git diff                    # line-by-line code changes (unstaged)
git lfs status              # large files (Blender, textures, .uasset)
```

### Save your work and upload to GitHub

**1. Create a branch** (keeps `main` clean — use your feature name):

```bash
git checkout main
git pull origin main
git checkout -b feature/my-change
```

**2. Stage files** (tell Git what to include):

```bash
git add .                           # all changes
git add path/to/file.cpp            # one file only
git add Content/VRLab26/            # one folder
```

**3. Commit** (save a snapshot locally):

```bash
git commit -m "Add grabbable mug prop and import mesh"
```

**4. Push to GitHub** (upload your branch):

```bash
git push -u origin feature/my-change
```

**5. Open a Pull Request** on GitHub:  
https://github.com/rudolfsmsp/vrlab26-hackathon/compare  
→ choose your branch → **Create pull request** → merge after review.

### Push updates to an existing branch

```bash
git add .
git commit -m "Fix teleport height check"
git push
```

### Working with large files (Unreal / Blender / audio)

This repo uses **Git LFS** for binaries. Always run once after clone:

```bash
git lfs install
```

Before every push with art or Unreal assets:

```bash
git lfs status          # confirm large files are tracked by LFS
git lfs pull            # download teammates' binary assets
```

If a push fails due to large files, make sure the file type is in `.gitattributes` (e.g. `.uasset`, `.blend`, `.fbx`, `.png`, `.wav`).

### Useful extras

```bash
git log --oneline -5              # last 5 commits
git branch                        # list local branches
git checkout main                 # switch back to main
git fetch origin                  # check GitHub without merging
git pull origin main              # download + merge latest main
```

### If something goes wrong

| Problem | Command |
|---------|---------|
| Discard **uncommitted** changes to one file | `git checkout -- path/to/file` |
| Discard **all** uncommitted changes | `git checkout -- .` |
| Pull rejected (remote has new commits) | `git pull origin main` then fix conflicts, then `git push` |
| Wrong files staged | `git reset HEAD path/to/file` |
| See remote URL | `git remote -v` |

### Command flow (at a glance)

```
pull latest  →  edit files  →  git add  →  git commit  →  git push  →  Pull Request on GitHub
```

More team rules: [CONTRIBUTING.md](CONTRIBUTING.md)


## Documentation

| Doc | Description |
|-----|-------------|
| [SETUP.md](Docs/SETUP.md) | Install UE, OpenXR, Blender, build from source |
| [ARCHITECTURE_README.md](Docs/ARCHITECTURE_README.md) | **Where to put what** — folders, workflows, examples |
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
