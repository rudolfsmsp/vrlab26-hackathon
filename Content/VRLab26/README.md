# Content

Unreal Engine assets live here. Binary files (`.uasset`, `.umap`, textures, audio) are tracked with **Git LFS**.

## Folder layout

```
Content/VRLab26/
├── Animations/     # Animation sequences & montages
├── Audio/          # Sound cues, attenuation, meta sounds
├── Blueprints/     # Gameplay, interactables, systems
├── Characters/     # Meshes, materials, anim BP for avatars
├── FX/             # Niagara systems & materials
├── Maps/           # Shipping levels
│   └── Dev/        # Sandbox / test maps (not shipped)
├── Materials/      # Master materials & instances
├── Meshes/         # Static & skeletal mesh assets
├── UI/             # Widgets & VR menu assets
└── VR/             # OpenXR-specific assets (teleport, hands)
```

## First-time setup

1. Open `VRLab26.uproject` in Unreal Engine 5.5+.
2. Create placeholder maps referenced in `Config/DefaultEngine.ini`:
   - `Content/VRLab26/Maps/MainMenu`
   - `Content/VRLab26/Maps/Dev/DevSandbox`
3. Commit new assets through Git LFS (`git lfs status` before pushing).

## Naming conventions

| Type | Pattern | Example |
|------|---------|---------|
| Blueprint | `BP_<Feature>_<Name>` | `BP_VR_Teleport` |
| Material | `M_<Surface>` / `MI_<Surface>_<Variant>` | `M_Stone`, `MI_Stone_Wet` |
| Static mesh | `SM_<Category>_<Name>` | `SM_Env_WallPanel_A` |
| Skeletal mesh | `SK_<Character>_<Part>` | `SK_Player_Hands` |
| Texture | `T_<Name>_<Channel>` | `T_Wall_BaseColor` |
| Map | `<Area>_<Purpose>` | `MainMenu`, `DevSandbox` |
