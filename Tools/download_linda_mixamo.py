"""Download BlenderKit asset b4589a8c and export it as Linda.

Run with Blender after logging into BlenderKit:
  blender --background --python Tools/download_linda_mixamo.py
"""

from __future__ import annotations

import json
import math
import re
import tempfile
from pathlib import Path
from urllib.parse import urlencode

import bpy
import mathutils
import requests

from bl_ext.user_default.blenderkit import paths, utils


ROOT = Path(__file__).resolve().parents[1]
ASSET_BASE_ID = "b4589a8c-4edc-44ca-b0f8-3688d4b20e4f"
ASSET_DIR = ROOT / "Art" / "Blender" / "Characters" / "Linda"
SOURCE_BLEND = ASSET_DIR / "linda.blend"
MIXAMO_FBX = ASSET_DIR / "linda_mixamo_ready.fbx"
PREVIEW_PNG = ASSET_DIR / "linda_preview.png"
REPORT_JSON = ASSET_DIR / "linda_mixamo_report.json"


def request_json(url: str, headers: dict, timeout: int = 90) -> dict:
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_asset_metadata(headers: dict) -> dict:
    query = urlencode(
        {
            "query": f"+asset_base_id:{ASSET_BASE_ID}",
            "page_size": "1",
            "dict_parameters": "1",
        }
    )
    data = request_json(f"{paths.BLENDERKIT_API}/search/?{query}", headers)
    results = data.get("results", [])
    if not results:
        raise RuntimeError(f"No BlenderKit result for asset_base_id {ASSET_BASE_ID}")
    return results[0]


def get_blend_url(metadata: dict, headers: dict, scene_uuid: str) -> str:
    blend_file = next(
        (file for file in metadata.get("files", []) if file.get("fileType") == "blend"),
        None,
    )
    if not blend_file or not blend_file.get("downloadUrl"):
        raise RuntimeError("BlenderKit asset has no .blend download endpoint.")

    separator = "&" if "?" in blend_file["downloadUrl"] else "?"
    data = request_json(
        f"{blend_file['downloadUrl']}{separator}{urlencode({'scene_uuid': scene_uuid})}",
        headers,
    )
    file_path = data.get("filePath")
    if not file_path:
        raise RuntimeError("BlenderKit download endpoint returned no filePath.")
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


def safe_name(value: str, fallback: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_]+", "_", value).strip("_")
    return value or fallback


def rename_linda_objects(objects: list[bpy.types.Object]) -> None:
    meshes = [obj for obj in objects if obj.type == "MESH"]
    for index, obj in enumerate(meshes, start=1):
        suffix = "" if index == 1 else f"_{index:02d}"
        obj.name = f"Linda{suffix}"
        obj.data.name = f"Linda_Mesh{suffix}"

    for obj in objects:
        if obj.type != "MESH":
            obj.name = safe_name(f"Linda_{obj.type}_{obj.name}", f"Linda_{obj.type}")


def mesh_objects() -> list[bpy.types.Object]:
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def bbox_for(meshes: list[bpy.types.Object]) -> dict | None:
    points = [
        obj.matrix_world @ mathutils.Vector(corner)
        for obj in meshes
        for corner in obj.bound_box
    ]
    if not points:
        return None
    return {
        "min": [min(point[i] for point in points) for i in range(3)],
        "max": [max(point[i] for point in points) for i in range(3)],
    }


def export_mixamo_fbx(meshes: list[bpy.types.Object]) -> None:
    if not meshes:
        raise RuntimeError("No mesh objects found to export for Linda.")

    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]

    bpy.ops.export_scene.fbx(
        filepath=str(MIXAMO_FBX),
        use_selection=True,
        object_types={"MESH"},
        apply_unit_scale=True,
        bake_space_transform=False,
        add_leaf_bones=False,
        bake_anim=False,
        use_mesh_modifiers=True,
        axis_forward="-Z",
        axis_up="Y",
        path_mode="COPY",
        embed_textures=True,
    )


def import_fbx_for_verification() -> dict:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(MIXAMO_FBX))
    objects = list(bpy.context.scene.objects)
    meshes = [obj for obj in objects if obj.type == "MESH"]
    armatures = [obj for obj in objects if obj.type == "ARMATURE"]
    cameras = [obj for obj in objects if obj.type == "CAMERA"]
    lights = [obj for obj in objects if obj.type == "LIGHT"]
    materials = sorted(
        {
            material.name
            for obj in meshes
            for material in obj.data.materials
            if material is not None
        }
    )
    return {
        "mesh_count": len(meshes),
        "armature_count": len(armatures),
        "camera_count": len(cameras),
        "light_count": len(lights),
        "materials": materials,
        "bbox": bbox_for(meshes),
    }


def frame_camera(meshes: list[bpy.types.Object]) -> None:
    bbox = bbox_for(meshes)
    if bbox is None:
        raise RuntimeError("Cannot frame camera without mesh bounds.")

    min_x, min_y, min_z = bbox["min"]
    max_x, max_y, max_z = bbox["max"]
    target = mathutils.Vector(
        ((min_x + max_x) / 2, (min_y + max_y) / 2, min_z + (max_z - min_z) * 0.55)
    )
    height = max(max_z - min_z, 1.0)
    width = max(max_x - min_x, max_y - min_y, 1.0)
    distance = max(height * 2.3, width * 3.0, 3.5)

    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.location = (target.x, target.y - distance, target.z + height * 0.05)
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 42
    bpy.context.scene.camera = camera


def setup_lighting(meshes: list[bpy.types.Object]) -> None:
    bbox = bbox_for(meshes)
    max_z = bbox["max"][2] if bbox else 2.0
    bpy.ops.object.light_add(type="AREA", location=(0.0, -3.6, max_z + 3.0))
    light = bpy.context.object
    light.rotation_euler = (math.radians(65), 0.0, 0.0)
    light.data.energy = 800
    light.data.size = 5.0
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("Linda Preview World")
    bpy.context.scene.world.color = (0.03, 0.03, 0.03)


def render_preview() -> None:
    meshes = mesh_objects()
    frame_camera(meshes)
    setup_lighting(meshes)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 64
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.film_transparent = False
    scene.render.filepath = str(PREVIEW_PNG)
    bpy.ops.render.render(write_still=True)


def main() -> None:
    prefs = bpy.context.preferences.addons["bl_ext.user_default.blenderkit"].preferences
    if not prefs.api_key:
        raise RuntimeError("BlenderKit API key is not configured in Blender preferences.")

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    headers = utils.get_headers(prefs.api_key)
    scene_uuid = utils.get_scene_id()

    metadata = get_asset_metadata(headers)
    display_name = metadata.get("displayName") or metadata.get("name") or "Linda"
    author = metadata.get("author", {})

    with tempfile.TemporaryDirectory(prefix="linda_blenderkit_") as temp_dir:
        temp_blend = Path(temp_dir) / "source.blend"
        signed_url = get_blend_url(metadata, headers, scene_uuid)
        download_file(signed_url, temp_blend)

        clear_scene()
        objects = append_blend_objects(temp_blend)
        rename_linda_objects(objects)
        bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE_BLEND))

    meshes = mesh_objects()
    source_verification = {
        "mesh_count": len(meshes),
        "armature_count": len([obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]),
        "camera_count": len([obj for obj in bpy.context.scene.objects if obj.type == "CAMERA"]),
        "light_count": len([obj for obj in bpy.context.scene.objects if obj.type == "LIGHT"]),
        "bbox": bbox_for(meshes),
    }
    export_mixamo_fbx(meshes)
    fbx_verification = import_fbx_for_verification()
    render_preview()

    report = {
        "name": "Linda",
        "asset_base_id": ASSET_BASE_ID,
        "blenderkit_display_name": display_name,
        "blenderkit_asset_id": metadata.get("id", ""),
        "license": metadata.get("license", ""),
        "author": {
            "id": str(author.get("id", "")),
            "name": author.get("fullName", ""),
        },
        "source_blend": str(SOURCE_BLEND.relative_to(ROOT)).replace("\\", "/"),
        "mixamo_fbx": str(MIXAMO_FBX.relative_to(ROOT)).replace("\\", "/"),
        "preview_png": str(PREVIEW_PNG.relative_to(ROOT)).replace("\\", "/"),
        "mixamo_export_policy": {
            "mesh_only_export": True,
            "no_animation": True,
            "no_armature_in_fbx": True,
            "no_camera_or_light_in_fbx": True,
        },
        "source_verification": source_verification,
        "fbx_verification": fbx_verification,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
