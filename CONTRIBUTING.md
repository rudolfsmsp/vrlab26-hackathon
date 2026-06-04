# Contributing to VRLab26

Thank you for building the VR game with us. These guidelines keep the repo fast and merge-friendly.

## Getting started

1. Read [Docs/SETUP.md](Docs/SETUP.md) and run `Scripts/setup-dev.ps1` (Windows) or `Scripts/setup-dev.sh` (Linux/macOS).
2. Create a branch from `main`: `feature/short-description` or `art/asset-name`.
3. Make changes and test in Unreal Editor with **VR Preview** when touching gameplay or VR UX.

## Git LFS rules

Always use Git LFS for:

- Unreal assets (`.uasset`, `.umap`)
- Blender files (`.blend`)
- Meshes (`.fbx`, `.glb`)
- Textures and audio

Never commit: `Binaries/`, `Intermediate/`, `DerivedDataCache/`, `Saved/`, or personal IDE folders.

```bash
git lfs install
git lfs status   # before every push
```

## Code style

- **C++**: match existing Unreal style — tabs, `U`/`A`/`F` prefixes, copyright header on new files.
- **Blueprints**: prefix with `BP_`, keep logic in functions/macros over Event Tick when possible.
- **Assets**: follow naming in [Content/VRLab26/README.md](Content/VRLab26/README.md).

## Pull requests

- Keep PRs focused — one feature or asset family per PR.
- Fill out the PR template checklist.
- Attach video for VR interaction changes.
- Ensure CI **Validate Project** workflow passes.

## Art pipeline

Author in `Art/Blender/`, export to `Art/Blender/Exports/`, import into `Content/VRLab26/`. See [Docs/BLENDER_PIPELINE.md](Docs/BLENDER_PIPELINE.md).

## Questions

Open a GitHub issue with the **Feature request** or **Bug report** template.
