# Meta Quest 2 / 3 setup (Unreal Engine)

This project targets **Meta Quest 2** and **Meta Quest 3** through Unreal Engine 5.5+ using **OpenXR** + the **Meta XR plugin**.

## Two ways to run on Quest

| Mode | How it works | Best for |
|------|----------------|----------|
| **PC VR (Quest Link / Air Link)** | Headset streams from your PC; OpenXR via Meta Link app | Fast iteration, VR Preview in editor |
| **Standalone (.apk on headset)** | Packaged Android build installed on Quest | Final performance testing, demo on device |

```
Git repo  →  Unreal Engine 5.5+  →  Meta XR + OpenXR  →  Quest 2 / Quest 3
                ↑                        ↑
         C++ / Content            Link (PC) or APK (standalone)
```

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| [Unreal Engine 5.5+](https://www.unrealengine.com/download) | Game engine |
| [Meta XR UE Integration](https://developer.oculus.com/downloads/package/unreal-engine-5-integration/) | Quest 2/3 support — see [Plugins/README.md](../Plugins/README.md) |
| [Meta Quest Link](https://www.meta.com/quest/setup/) (PC) | PC VR testing |
| [Meta Quest Developer Hub](https://developer.oculus.com/documentation/unity/unity-qs-developer-hub/) | Install APK, device logs |
| Android Studio + SDK (standalone only) | API 34, NDK — install via UE *Platforms → Android* |

Enable Android support in Epic Launcher: *Unreal Engine → Library → Engine → Options → Target Platforms → Android*.

---

## Step 1 — Install Meta XR plugin

Follow **[Plugins/README.md](../Plugins/README.md)**. Without this plugin, standalone Quest builds will not work correctly.

After install, confirm in **Edit → Plugins → Virtual Reality**:

- ✅ OpenXR  
- ✅ OpenXR Hand Tracking  
- ✅ Meta XR (OculusXR)  
- ❌ Oculus VR (legacy — keep **disabled**)

---

## Step 2 — Project settings (already in repo)

These are pre-configured in `Config/`:

| Setting | File | Value |
|---------|------|-------|
| Package name | `DefaultEngine.ini` | `com.vrlab26.quest` |
| Min / Target SDK | `DefaultEngine.ini` | 32 / 34 |
| Quest devices | `DefaultEngine.ini` | `quest2 \| quest3` |
| Vulkan, ARM64 | `DefaultEngine.ini` | On |
| Meta Quest packaging | `DefaultEngine.ini` | `bPackageForMetaQuest=True` |
| Quest 2 device profile | `DefaultDeviceProfiles.ini` | `Oculus_Quest2` (lower quality) |
| Quest 3 device profile | `DefaultDeviceProfiles.ini` | `Meta_Quest_3` (higher quality) |
| Mobile renderer | `Config/Android/AndroidEngine.ini` | No Lumen, mobile VR flags |

In editor, verify **Edit → Project Settings → Platforms → Android** has no red errors (SDK paths configured).

---

## Step 3 — PC VR with Quest Link (daily development)

1. Install **Meta Quest Link** on PC and enable Link on the headset.
2. Connect Quest 2/3 via USB or Air Link.
3. Open `VRLab26.uproject` in Unreal.
4. **Edit → Project Settings → Meta XR → PC** — ensure Link runtime is detected.
5. Press **Play** dropdown → **VR Preview** (or **Standalone Game** with `-vr`).

You should spawn as `AVRLab26VRCharacter` with grip + aim controllers tracked.

---

## Step 4 — Standalone build (APK on Quest)

### A. Configure signing (first time)

1. **Project Settings → Platforms → Android → Android Package Signing**
2. Create or select a keystore (debug keystore is fine for hackathon testing).

### B. Package

**Editor:** *Platforms → Android → Android (ASTC)* → **Package Project**

**Command line (Windows):**

```powershell
.\Scripts\package-quest.ps1
```

**Command line (Linux/macOS):**

```bash
./Scripts/package-quest.sh
```

### C. Install on headset

1. Enable **Developer Mode** on Quest (Meta Quest app on phone).
2. Connect USB → open **Meta Quest Developer Hub** → *Device Manager* → install APK  
   — or use `adb install VRLab26-Android-Shipping.apk`

---

## C++ VR pawn (Quest-ready)

`AVRLab26VRCharacter` uses OpenXR motion sources recommended by Meta:

| Component | Motion source | Use |
|-----------|---------------|-----|
| `LeftGripController` | `LeftGrip` | Attach held objects |
| `RightGripController` | `RightGrip` | Attach held objects |
| `LeftAimController` | `LeftAim` | Line traces, UI laser |
| `RightAimController` | `RightAim` | Line traces, UI laser |

Hand tracking is enabled via OpenXR Hand Tracking plugin + manifest metadata in `DefaultEngine.ini`.

---

## Performance targets

| Device | Refresh rate | Notes |
|--------|--------------|-------|
| Quest 2 | 72 Hz (default) | Use `Oculus_Quest2` profile — lower pixel density |
| Quest 3 | 90 Hz (target) | Use `Meta_Quest_3` profile — higher texture pool |

See [VR_DESIGN.md](./VR_DESIGN.md) for draw call and triangle budgets.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Meta XR plugin missing" on open | Install plugin — [Plugins/README.md](../Plugins/README.md) |
| Black screen in headset | Confirm OpenXR runtime active (Link app running) |
| Controllers frozen | Check motion sources are `LeftGrip`/`RightGrip`, not legacy Oculus poses |
| Android packaging fails | Install SDK/NDK via UE; set `ANDROID_HOME` |
| App not listed on Quest | Verify `com.oculus.supportedDevices` includes `quest2|quest3` |
| Low FPS on Quest 2 | Lower scalability; reduce `vr.PixelDensity` in device profile |

---

## Related docs

- [SETUP.md](./SETUP.md) — general Unreal + Git LFS setup  
- [ARCHITECTURE_README.md](./ARCHITECTURE_README.md) — where to put assets  
- [VR_DESIGN.md](./VR_DESIGN.md) — comfort & performance guidelines
