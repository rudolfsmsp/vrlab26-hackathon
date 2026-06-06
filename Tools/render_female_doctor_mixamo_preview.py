from pathlib import Path
import math

import bpy
import mathutils


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "Art" / "Blender" / "Characters" / "FemaleDoctorMixamoReady"
FBX_PATH = ASSET_DIR / "female_doctor_mixamo_ready.fbx"
PREVIEW_PATH = ASSET_DIR / "female_doctor_mixamo_ready_mixamo_preview.png"


def import_model():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    bpy.ops.import_scene.fbx(filepath=str(FBX_PATH))
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def frame_camera(meshes):
    points = [
        obj.matrix_world @ mathutils.Vector(corner)
        for obj in meshes
        for corner in obj.bound_box
    ]
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)
    min_z = min(point.z for point in points)
    max_z = max(point.z for point in points)
    target = mathutils.Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, min_z + (max_z - min_z) * 0.55))

    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.location = (target.x, target.y - 3.8, target.z + 0.08)
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 42
    bpy.context.scene.camera = camera


def setup_lighting():
    bpy.ops.object.light_add(type="AREA", location=(0.0, -3.6, 4.8))
    light = bpy.context.object
    light.rotation_euler = (math.radians(65), 0.0, 0.0)
    light.data.energy = 650
    light.data.size = 4.0
    bpy.context.scene.world.color = (0.03, 0.03, 0.03)


def render_preview():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 64
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.film_transparent = False
    scene.render.filepath = str(PREVIEW_PATH)
    bpy.ops.render.render(write_still=True)


def main():
    meshes = import_model()
    if not meshes:
        raise RuntimeError(f"No meshes imported from {FBX_PATH}")
    frame_camera(meshes)
    setup_lighting()
    render_preview()
    print(f"Wrote {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
