# Blender source art

Authoritative `.blend` files and export presets for the VRLab26 VR game.

## Structure

```
Art/Blender/
├── Characters/     # Player avatars, NPCs, hands
├── Environments/     # Modular kits, props, set dressing
├── Props/            # Interactive & decorative objects
├── Materials/        # Shared node groups & material libraries
└── Exports/          # FBX/GLB exports staged for Unreal import
    └── .gitkeep
```

## Recommended Blender version

- **Blender 4.x** (latest LTS or stable release)
- Enable add-ons: *FBX*, *glTF 2.0*, *Node Wrangler*

## Export settings (→ Unreal)

| Setting | Value |
|---------|-------|
| Scale | 1.0 (1 Blender unit = 1 cm in UE) |
| Forward | `-Y Forward` |
| Up | `Z Up` |
| Apply transforms | Yes (Ctrl+A before export) |
| Mesh format | FBX 7.4 binary |
| Armature | Only selected bones, deform bones only |

See [Docs/BLENDER_PIPELINE.md](../Docs/BLENDER_PIPELINE.md) for the full workflow.

## Git LFS

`.blend`, `.fbx`, `.png`, and other binary art files are stored with Git LFS. Run `git lfs install` once after cloning.
