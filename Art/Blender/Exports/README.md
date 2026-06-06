# FBX exports (Git LFS)

Staged mesh exports from Blender, ready to import into Unreal.

## Folder layout

```
Exports/
├── Characters/
├── Environments/     ← level kits, terrain, room geometry (environment.fbx goes here)
└── Props/
```

## Upload checklist

1. Place `.fbx` in the matching category folder
2. Run `git lfs install` (once)
3. `git add` → `git commit` → `git push`
4. Verify with `git lfs status` before pushing

All `*.fbx` files are tracked via **Git LFS** (see `.gitattributes`).
