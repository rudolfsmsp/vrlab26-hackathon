# Meta XR Plugin (required for Quest 2 / 3 standalone)

The **Meta XR plugin** is not included in this Git repo (Meta license + size). Install it once per machine before opening the project for Quest builds.

## Install (one time)

1. Download **Unreal Engine 5 Integration** from Meta:  
   https://developer.oculus.com/downloads/package/unreal-engine-5-integration/

   Match the version to your Unreal Engine (e.g. UE **5.5** → Meta integration **v78** or latest listed for 5.5).

2. Extract into this project's `Plugins/` folder:

```
vrlab26-hackathon/
└── Plugins/
    └── MetaXR/          ← from UnrealMetaXRPlugin zip
        └── OculusXR.uplugin
```

3. *(Optional)* Meta XR Platform SDK for social/store features:  
   https://developer.oculus.com/downloads/package/unreal-5-platform-sdk-plugin/  
   Extract to `Plugins/MetaXRPlatform/`.

4. Open `VRLab26.uproject`. If prompted:
   - Enable **Meta XR** (OculusXR) plugin
   - Enable **OpenXR** and **OpenXR Hand Tracking**
   - Restart the editor

5. In **Edit → Project Settings → Plugins → Meta XR → General**:
   - **XR API:** `Epic Native OpenXR` (recommended)
   - **Supported Devices:** Quest 2, Quest 3
   - **Color Space:** P3 (Quest default)

## Verify

```powershell
# Plugin folder exists
Test-Path Plugins/MetaXR/OculusXR.uplugin
```

## PC VR only (Quest Link, no standalone build)

You can develop on PC with **Quest Link** + **OpenXR** without packaging for Android. The Meta XR plugin still improves Quest-specific features when using Link.

## Do not commit

Never commit the `Plugins/MetaXR/` download to Git — each developer installs locally. Only this README is versioned.
