"""Export the requested BlenderKit model assets as FBX files on the Desktop.

Run with Blender after logging into BlenderKit:
  blender --background --python Tools/export_blenderkit_assets_to_fbx.py

This script avoids BlenderKit's local background client and uses the
authenticated web API directly:
  search metadata -> signed .blend URL -> append objects -> export FBX.
"""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from urllib.parse import urlencode

import bpy
import requests

from bl_ext.user_default.blenderkit import paths, utils


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "Art" / "Blender" / "BlenderKitAssets" / "blenderkit_assets_manifest.json"
EXPORT_DIR = Path.home() / "Desktop" / "BlenderKit_FBX_Exports"


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value[:72] or fallback


def load_manifest_assets() -> list[dict]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assets = [asset for asset in manifest["assets"] if asset.get("status") == "resolved"]
    if not assets:
        raise RuntimeError(f"No resolved BlenderKit assets found in {MANIFEST_PATH}")
    return assets


def request_json(url: str, headers: dict, timeout: int = 90) -> dict:
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_asset_metadata(asset_base_id: str, headers: dict) -> dict:
    query = urlencode(
        {
            "query": f"+asset_base_id:{asset_base_id}",
            "page_size": "1",
            "dict_parameters": "1",
        }
    )
    data = request_json(f"{paths.BLENDERKIT_API}/search/?{query}", headers)
    results = data.get("results", [])
    if not results:
        raise RuntimeError(f"No BlenderKit search result for {asset_base_id}")
    return results[0]


def get_blend_download_url(asset_metadata: dict, headers: dict, scene_uuid: str) -> str:
    blend_file = next(
        (file for file in asset_metadata.get("files", []) if file.get("fileType") == "blend"),
        None,
    )
    if not blend_file or not blend_file.get("downloadUrl"):
        raise RuntimeError(f"No .blend download endpoint for {asset_metadata.get('assetBaseId')}")

    separator = "&" if "?" in blend_file["downloadUrl"] else "?"
    data = request_json(
        f"{blend_file['downloadUrl']}{separator}{urlencode({'scene_uuid': scene_uuid})}",
        headers,
    )
    file_path = data.get("filePath")
    if not file_path:
        raise RuntimeError(f"Download endpoint returned no filePath for {asset_metadata.get('assetBaseId')}")
    return file_path


def download_file(url: str, destination: Path) -> None:
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with destination.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def clear_scene() -> None:
    if bpy.context.object:
        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except RuntimeError:
            pass
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    try:
        bpy.ops.outliner.orphans_purge(do_recursive=True)
    except RuntimeError:
        pass


def append_blend_objects(blend_path: Path) -> list[bpy.types.Object]:
    with bpy.data.libraries.load(str(blend_path), link=False) as (data_from, data_to):
        data_to.objects = list(data_from.objects)

    objects = [obj for obj in data_to.objects if obj is not None]
    for obj in objects:
        if not obj.users_collection:
            bpy.context.collection.objects.link(obj)

    return objects


def export_fbx(objects: list[bpy.types.Object], out_path: Path) -> None:
    exportable_types = {"MESH", "EMPTY", "ARMATURE", "CURVE", "SURFACE", "FONT"}
    exportable = [obj for obj in objects if obj.type in exportable_types]
    if not exportable:
        exportable = [
            obj for obj in bpy.context.scene.objects if obj.type in exportable_types
        ]
    if not exportable:
        raise RuntimeError("No exportable objects found after appending .blend asset.")

    bpy.ops.object.select_all(action="DESELECT")
    for obj in exportable:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = exportable[0]

    bpy.ops.export_scene.fbx(
        filepath=str(out_path),
        use_selection=True,
        apply_unit_scale=True,
        bake_space_transform=False,
        object_types={"EMPTY", "MESH", "ARMATURE", "OTHER"},
        path_mode="COPY",
        embed_textures=True,
    )


def main() -> None:
    prefs = bpy.context.preferences.addons["bl_ext.user_default.blenderkit"].preferences
    if not prefs.api_key:
        raise RuntimeError("BlenderKit API key is not configured in Blender preferences.")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    headers = utils.get_headers(prefs.api_key)
    scene_uuid = utils.get_scene_id()
    assets = load_manifest_assets()

    with tempfile.TemporaryDirectory(prefix="blenderkit_fbx_") as temp_dir:
        temp_root = Path(temp_dir)
        for index, manifest_asset in enumerate(assets, start=1):
            clear_scene()
            asset_base_id = manifest_asset["asset_base_id"]
            label = manifest_asset.get("display_name") or asset_base_id
            slug = slugify(label, asset_base_id[:8])
            blend_path = temp_root / f"{index:02d}_{slug}.blend"
            out_path = EXPORT_DIR / f"{index:02d}_{slug}_{asset_base_id[:8]}.fbx"

            print(f"[{index}/{len(assets)}] Resolving {label}")
            metadata = get_asset_metadata(asset_base_id, headers)
            signed_url = get_blend_download_url(metadata, headers, scene_uuid)

            print(f"[{index}/{len(assets)}] Downloading .blend for {label}")
            download_file(signed_url, blend_path)

            print(f"[{index}/{len(assets)}] Exporting FBX for {label}")
            objects = append_blend_objects(blend_path)
            export_fbx(objects, out_path)
            print(f"[{index}/{len(assets)}] Wrote {out_path}")

    print(f"Done. FBX exports are in {EXPORT_DIR}")


if __name__ == "__main__":
    main()
