# Blender → Unreal pipeline

End-to-end workflow for getting 3D assets from Blender into the VRLab26 VR game.

## 1. Scene setup (once per file)

1. *File → New → General*.
2. *Scene Properties → Units*: Metric, Unit Scale **0.01** (matches Unreal centimeters).
3. Apply scale on all meshes before export (*Ctrl+A → Scale*).

## 2. Modeling conventions

- **Origin**: bottom-center for props, root bone for characters.
- **Poly budget (VR)**: props < 5k tris, hero assets < 20k, environments use modular pieces.
- **UVs**: single UV channel, no overlapping unless intentional (lightmap channel 1 for static meshes).
- **Naming**: match Unreal prefix — `SM_`, `SK_`, etc.

## 3. Materials

Author materials in Unreal when possible. In Blender:

- Use **Principled BSDF** only (maps to UE PBR).
- Bake textures if needed: Base Color, Normal, Roughness, AO.
- Export textures as PNG (sRGB for color, linear for data maps).

## 4. Export to FBX

*File → Export → FBX (.fbx)*

| Option | Value |
|--------|-------|
| Selected Objects | On (unless exporting full scene) |
| Scale | 1.0 |
| Apply Scalings | FBX All |
| Forward | `-Y Forward` |
| Up | `Z Up` |
| Mesh | Smoothing: Face, Export Subdiv, Apply Modifiers |
| Armature | Deformed Bones Only, Add Leaf Bones: Off |

Save to `Art/Blender/Exports/<Category>/`.

## 5. Import to Unreal

1. Content Browser → *Import* → select FBX.
2. Suggested import settings:
   - **Import as Skeletal** for rigged meshes, **Static** otherwise.
   - Transform: uniform scale 1.0 (already scaled in Blender).
   - Generate lightmap UVs for static meshes.
   - Import materials: off (create MI_ in UE).
3. Place imported assets under `Content/VRLab26/Meshes/` or `Characters/`.

## 6. Validation checklist

- [ ] No non-uniform scale on export
- [ ] Normals face outward (Ctrl+N recalculate)
- [ ] Collision: generate in UE or author UCX simple collision in Blender
- [ ] LODs: generate in UE *Nanite* (static) or manual LODs for VR performance
- [ ] File committed via Git LFS

## Automation (future)

Planned: Python batch export script in `Tools/Blender/export_to_fbx.py` and Unreal Editor Utility Widget for folder import.
