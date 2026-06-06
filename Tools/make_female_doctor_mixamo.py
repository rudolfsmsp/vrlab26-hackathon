"""Build a Mixamo-friendly FBX from the current colored doctor asset.

The source .blend is kept visually intact. The body and facial feature meshes
stay separate because joining them changes tiny rendered face pixels. Mixamo can
accept FBX humanoid uploads with multiple meshes, so the export is cleaned by
including only the character meshes: no cameras, lights, armatures, or animation.
"""

from __future__ import annotations

import array
import json
import math
import tempfile
from pathlib import Path

import bpy
import mathutils


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "Art" / "Blender" / "Characters" / "FemaleDoctorMixamoReady"
BLEND_PATH = ASSET_DIR / "female_doctor_mixamo_ready.blend"
FBX_PATH = ASSET_DIR / "female_doctor_mixamo_ready.fbx"
REPORT_PATH = ASSET_DIR / "female_doctor_mixamo_ready_mixamo_report.json"

BODY_NAME = "female_doctor_mixamo_ready"
FACE_PREFIX = "FD_FACE_"


def mesh_objects() -> list[bpy.types.Object]:
    return [
        obj
        for obj in bpy.context.scene.objects
        if obj.type == "MESH" and (obj.name == BODY_NAME or obj.name.startswith(FACE_PREFIX))
    ]


def frame_camera() -> None:
    mesh = bpy.data.objects.get(BODY_NAME)
    target = mathutils.Vector((0.0, 0.0, 0.9))
    if mesh:
        points = [mesh.matrix_world @ mathutils.Vector(corner) for corner in mesh.bound_box]
        min_z = min(point.z for point in points)
        max_z = max(point.z for point in points)
        target = mathutils.Vector((0.0, 0.0, min_z + (max_z - min_z) * 0.55))

    camera = bpy.data.objects.get("Camera")
    if not camera:
        bpy.ops.object.camera_add()
        camera = bpy.context.object

    bpy.context.scene.camera = camera
    camera.location = (0.0, -3.8, target.z + 0.08)
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 42
    camera.data.dof.use_dof = False


def setup_lighting() -> None:
    light = bpy.data.objects.get("Area")
    if not light:
        bpy.ops.object.light_add(type="AREA", location=(0.0, -3.0, 5.0))
        light = bpy.context.object
    light.location = (0.0, -3.6, 4.8)
    light.rotation_euler = (math.radians(65), 0.0, 0.0)
    light.data.energy = 550
    light.data.size = 4.0
    bpy.context.scene.world.color = (0.03, 0.03, 0.03)


def render_png(path: Path) -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 64
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.film_transparent = False
    scene.render.filepath = str(path)
    # Use one deterministic sample for the preservation check. Multi-sample
    # Eevee renders can jitter a few edge pixels even when the scene is equal.
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 1
    bpy.ops.render.render(write_still=True)


def load_pixels(path: Path) -> array.array:
    image = bpy.data.images.load(str(path), check_existing=False)
    pixels = array.array("f", [0.0]) * len(image.pixels)
    image.pixels.foreach_get(pixels)
    bpy.data.images.remove(image)
    return pixels


def compare_renders(reference: Path, candidate: Path) -> dict:
    ref_pixels = load_pixels(reference)
    candidate_pixels = load_pixels(candidate)
    if len(ref_pixels) != len(candidate_pixels):
        return {
            "pixel_count_match": False,
            "max_channel_delta": None,
            "changed_channels": None,
        }

    max_delta = 0.0
    changed = 0
    for a, b in zip(ref_pixels, candidate_pixels):
        delta = abs(a - b)
        if delta > 0:
            changed += 1
            if delta > max_delta:
                max_delta = delta

    return {
        "pixel_count_match": True,
        "max_channel_delta": max_delta,
        "changed_channels": changed,
    }


def material_snapshot() -> dict:
    snapshot = {}
    for obj in mesh_objects():
        snapshot[obj.name] = [
            {
                "slot": index,
                "name": material.name if material else None,
                "diffuse_color": list(material.diffuse_color) if material else None,
            }
            for index, material in enumerate(obj.data.materials)
        ]
    return snapshot


def join_to_single_mixamo_mesh() -> bpy.types.Object:
    meshes = mesh_objects()
    if not meshes:
        raise RuntimeError("No doctor mesh objects found.")

    body = bpy.data.objects.get(BODY_NAME)
    if body is None or body.type != "MESH":
        raise RuntimeError(f"Body mesh '{BODY_NAME}' was not found.")

    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()

    joined = bpy.context.view_layer.objects.active
    joined.name = BODY_NAME
    joined.data.name = BODY_NAME + "_Mesh"

    # Bake object transforms into mesh data so Mixamo gets a single upright mesh
    # at scene origin without changing the visible world-space geometry.
    bpy.ops.object.select_all(action="DESELECT")
    joined.select_set(True)
    bpy.context.view_layer.objects.active = joined
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    joined.location = (0.0, 0.0, 0.0)
    joined.rotation_euler = (0.0, 0.0, 0.0)
    joined.scale = (1.0, 1.0, 1.0)
    return joined


def bbox_for(obj: bpy.types.Object) -> dict:
    points = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    return {
        "min": [min(point[i] for point in points) for i in range(3)],
        "max": [max(point[i] for point in points) for i in range(3)],
    }


def export_mixamo_fbx(objects: list[bpy.types.Object]) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.fbx(
        filepath=str(FBX_PATH),
        use_selection=True,
        object_types={"MESH"},
        apply_unit_scale=True,
        bake_space_transform=False,
        add_leaf_bones=False,
        use_armature_deform_only=True,
        bake_anim=False,
        axis_forward="-Z",
        axis_up="Y",
        path_mode="COPY",
        embed_textures=True,
    )


def verify_exported_fbx() -> dict:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(FBX_PATH))
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
    all_points = [
        obj.matrix_world @ mathutils.Vector(corner)
        for obj in meshes
        for corner in obj.bound_box
    ]
    bbox = None
    if all_points:
        bbox = {
            "min": [min(point[i] for point in all_points) for i in range(3)],
            "max": [max(point[i] for point in all_points) for i in range(3)],
        }
    return {
        "mesh_count": len(meshes),
        "armature_count": len(armatures),
        "camera_count": len(cameras),
        "light_count": len(lights),
        "materials": materials,
        "bbox": bbox,
    }


def write_report(report: dict) -> None:
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")


def main() -> None:
    bpy.ops.wm.open_mainfile(filepath=str(BLEND_PATH))
    frame_camera()
    setup_lighting()

    before_materials = material_snapshot()
    export_objects = mesh_objects()
    source_mesh_object_count = len(export_objects)
    source_armature_count = len([obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"])

    with tempfile.TemporaryDirectory(prefix="female_doctor_mixamo_") as temp_dir:
        reference_render = Path(temp_dir) / "reference.png"
        mixamo_render = Path(temp_dir) / "mixamo.png"

        render_png(reference_render)
        export_mixamo_fbx(export_objects)
        render_png(mixamo_render)
        visual_compare = compare_renders(reference_render, mixamo_render)

    if (
        not visual_compare["pixel_count_match"]
        or visual_compare["max_channel_delta"] != 0.0
        or visual_compare["changed_channels"] != 0
    ):
        raise RuntimeError(f"Mixamo export changed the source scene render: {visual_compare}")

    fbx_verification = verify_exported_fbx()

    report = {
        "source_blend": str(BLEND_PATH.relative_to(ROOT)).replace("\\", "/"),
        "mixamo_fbx": str(FBX_PATH.relative_to(ROOT)).replace("\\", "/"),
        "visual_compare": visual_compare,
        "mixamo_export_policy": {
            "preserved_as_multi_mesh": True,
            "reason": "Joining the facial feature meshes changed rendered pixels; multi-mesh FBX preserves the current look exactly.",
            "no_animation": True,
            "mesh_only_export": True,
        },
        "fbx_verification": fbx_verification,
        "source_mesh_object_count": source_mesh_object_count,
        "source_armature_count": source_armature_count,
        "source_materials": before_materials,
    }
    write_report(report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
