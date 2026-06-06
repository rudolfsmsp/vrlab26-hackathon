"""Download the project BlenderKit asset set into a local Blender scene.

Run with Blender after logging into BlenderKit:
  blender --background --python Tools/download_blenderkit_assets.py

The generated output is intentionally ignored by git. The repo is public and
the requested BlenderKit assets are royalty-free, so raw model files should be
rehydrated by authenticated team members instead of committed.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import bpy

from bl_ext.user_default.blenderkit import download, tasks_queue


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "Art" / "Blender" / "BlenderKitAssets" / "blenderkit_assets_manifest.json"
OUT_DIR = ROOT / "Art" / "Blender" / "BlenderKitAssets" / "LocalDownloads"
OUT_BLEND = OUT_DIR / "blenderkit_assets_scene.blend"


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def ensure_output_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_assets() -> list[dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assets = [asset for asset in manifest["assets"] if asset.get("status") == "resolved"]
    if not assets:
        raise RuntimeError(f"No resolved assets found in {MANIFEST_PATH}")
    return assets


def layout_location(index: int, columns: int = 6, spacing: float = 4.0) -> tuple[float, float, float]:
    return ((index % columns) * spacing, (index // columns) * spacing, 0.0)


def process_blenderkit_timers(timeout_seconds: float = 900.0) -> None:
    started = time.monotonic()
    while download.download_tasks or not tasks_queue.get_queue().empty():
        if time.monotonic() - started > timeout_seconds:
            pending = [task.get("text", task_id) for task_id, task in download.download_tasks.items()]
            raise TimeoutError(f"Timed out waiting for BlenderKit downloads: {pending}")
        tasks_queue.queue_worker()
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
        time.sleep(0.25)


def add_camera_and_light(asset_count: int) -> None:
    rows = max(1, math.ceil(asset_count / 6))
    center_x = (min(asset_count, 6) - 1) * 2.0
    center_y = (rows - 1) * 2.0

    bpy.ops.object.light_add(type="AREA", location=(center_x, center_y - 7.5, 8.0))
    light = bpy.context.object
    light.name = "BlenderKit_Asset_AreaLight"
    light.data.energy = 700
    light.data.size = 5

    bpy.ops.object.camera_add(location=(center_x, center_y - 13.0, 7.0), rotation=(math.radians(60), 0, 0))
    camera = bpy.context.object
    camera.name = "BlenderKit_Asset_OverviewCamera"
    bpy.context.scene.camera = camera


def main() -> None:
    prefs = bpy.context.preferences.addons["bl_ext.user_default.blenderkit"].preferences
    if not prefs.api_key:
        raise RuntimeError("BlenderKit API key is not configured in Blender preferences.")

    ensure_output_dir()
    clear_scene()
    assets = load_assets()

    for index, asset in enumerate(assets):
        print(f"Downloading {index + 1}/{len(assets)}: {asset['display_name']}")
        bpy.ops.scene.blenderkit_download(
            asset_base_id=asset["asset_base_id"],
            model_location=layout_location(index),
            model_rotation=(0.0, 0.0, 0.0),
        )
        process_blenderkit_timers()

    add_camera_and_light(len(assets))
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND))
    print(f"Saved local BlenderKit asset scene to {OUT_BLEND}")


if __name__ == "__main__":
    main()
