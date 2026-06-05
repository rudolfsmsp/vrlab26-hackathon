# VR design guidelines

Design principles for the VRLab26 hackathon VR experience.

## Comfort

- Prefer **teleport locomotion** or smooth movement with vignette option.
- Maintain **90 FPS** minimum on target hardware (72 Hz on standalone Quest).
- Avoid forced camera rotation; snap-turn in 30–45° increments if needed.
- Keep UI at **1.5–3 m** from the player, world-locked or wrist-attached.

## Interaction

- Use **motion controller** grab and ray for primary interactions.
- Provide **haptic feedback** on successful grabs and button presses.
- Audio spatialization: all gameplay sounds use attenuation with HRTF.

## Scale & presence

- Real-world scale: doorways ~200 cm, counters ~90 cm, grab objects sized for hands.
- Player capsule height: 96 cm radius 42 (default character) — tune in `VRLab26VRCharacter`.

## Performance budgets (Quest standalone)

| Asset type | Budget |
|------------|--------|
| Draw calls (visible) | < 200 |
| Triangles (on screen) | < 750k |
| Texture size (hero) | 2K max, 1K for props |
| Blueprint tick | Avoid per-frame tick; use timers/events |

## OpenXR targets

Primary: PC VR via OpenXR (Quest Link, SteamVR).  
Secondary: Android standalone (Quest) — test early on device.

## Playtesting checklist

- [ ] Comfortable locomotion for 10+ minutes
- [ ] Readable UI at default IPD
- [ ] Interactions work with left and right hand
- [ ] No z-fighting or scale mismatches in room-scale
- [ ] Stable framerate in worst-case scene
