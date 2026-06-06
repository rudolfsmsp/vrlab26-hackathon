import math
from pathlib import Path

import bpy
import mathutils


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "Art" / "Blender" / "Characters" / "FemaleDoctorMixamoReady"
BLEND_PATH = ASSET_DIR / "female_doctor_mixamo_ready.blend"
FBX_PATH = ASSET_DIR / "female_doctor_mixamo_ready.fbx"
PREVIEW_PATH = ASSET_DIR / "female_doctor_mixamo_ready_preview.png"


COLORS = {
    "hairs": (0.36, 0.14, 0.055, 1.0),
    "shoes-1": (0.02, 0.10, 0.20, 1.0),
    "female doc body": (0.74, 0.42, 0.30, 1.0),
    "female gernal physition": (0.55, 0.86, 0.92, 1.0),
    "Stethoscope": (0.03, 0.04, 0.05, 1.0),
}

FACE_PREFIX = "FD_FACE_"
FACE_COLORS = {
    "EyeWhite": (0.98, 0.96, 0.90, 1.0),
    "EyeLine": (0.18, 0.075, 0.035, 1.0),
    "Iris": (0.22, 0.45, 0.52, 1.0),
    "Pupil": (0.015, 0.012, 0.010, 1.0),
    "Brow": (0.18, 0.075, 0.035, 1.0),
    "Smile": (0.46, 0.16, 0.14, 1.0),
    "Blush": (0.95, 0.46, 0.45, 1.0),
    "Nose": (0.58, 0.29, 0.22, 1.0),
}


def set_principled_color(material, color, roughness=0.5, metallic=0.0):
    material.use_nodes = True
    material.diffuse_color = color

    material.node_tree.nodes.clear()
    output = material.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (320, 0)
    node = material.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (0, 0)

    node.inputs["Base Color"].default_value = color
    node.inputs["Roughness"].default_value = roughness
    node.inputs["Metallic"].default_value = metallic
    material.node_tree.links.new(node.outputs["BSDF"], output.inputs["Surface"])


def normalized_name(name):
    return name.removesuffix(".001")


def apply_character_colors():
    for material in bpy.data.materials:
        key = normalized_name(material.name)
        if key not in COLORS:
            continue

        metallic = 0.0
        roughness = 0.62
        if key == "Stethoscope":
            metallic = 0.25
            roughness = 0.38
        elif key == "female gernal physition":
            roughness = 0.78

        set_principled_color(material, COLORS[key], roughness=roughness, metallic=metallic)


def get_or_create_material(name, color, roughness=0.55):
    material = bpy.data.materials.get(name)
    if not material:
        material = bpy.data.materials.new(name)
    set_principled_color(material, color, roughness=roughness)
    return material


def remove_existing_face_features():
    for obj in list(bpy.data.objects):
        if obj.name.startswith(FACE_PREFIX):
            bpy.data.objects.remove(obj, do_unlink=True)


def add_ellipsoid(name, location, scale, material, segments=32, ring_count=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=ring_count,
        radius=1.0,
        location=location,
    )
    obj = bpy.context.object
    obj.name = FACE_PREFIX + name
    obj.scale = scale
    obj.data.materials.append(material)
    return obj


def add_curve(name, points, material, bevel_depth=0.004, resolution=3):
    curve = bpy.data.curves.new(FACE_PREFIX + name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = resolution
    curve.bevel_depth = bevel_depth
    curve.bevel_resolution = 3

    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, coords in zip(spline.points, points):
        point.co = (*coords, 1.0)

    obj = bpy.data.objects.new(FACE_PREFIX + name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def add_friendly_face_features():
    remove_existing_face_features()

    materials = {
        key: get_or_create_material(f"MI_Face_{key}", color, roughness=0.68)
        for key, color in FACE_COLORS.items()
    }

    # The character faces negative Y. Keep these pieces just proud of the face
    # surface so they render clearly without cutting into the original mesh.
    eye_y = -0.171
    detail_y = -0.176
    left_x = -0.045
    right_x = 0.045

    add_curve(
        "Eye_L",
        [(-0.060, detail_y, 1.509), (-0.045, detail_y - 0.001, 1.518), (-0.030, detail_y, 1.509)],
        materials["EyeLine"],
        bevel_depth=0.003,
    )
    add_curve(
        "Eye_R",
        [(0.030, detail_y, 1.509), (0.045, detail_y - 0.001, 1.518), (0.060, detail_y, 1.509)],
        materials["EyeLine"],
        bevel_depth=0.003,
    )
    for side, x in (("L", left_x), ("R", right_x)):
        add_ellipsoid(f"Blush_{side}", (x * 1.45, -0.169, 1.444), (0.015, 0.002, 0.008), materials["Blush"], 24, 8)

    add_curve(
        "Brow_L",
        [(-0.067, detail_y, 1.548), (-0.046, detail_y - 0.001, 1.554), (-0.025, detail_y, 1.550)],
        materials["Brow"],
        bevel_depth=0.0025,
    )
    add_curve(
        "Brow_R",
        [(0.025, detail_y, 1.550), (0.046, detail_y - 0.001, 1.554), (0.067, detail_y, 1.548)],
        materials["Brow"],
        bevel_depth=0.0025,
    )
    add_curve(
        "Nose",
        [(-0.004, detail_y, 1.486), (0.003, detail_y - 0.001, 1.466), (-0.008, detail_y, 1.459)],
        materials["Nose"],
        bevel_depth=0.0018,
    )
    add_curve(
        "Smile",
        [(-0.036, detail_y, 1.424), (-0.016, detail_y - 0.001, 1.413), (0.0, detail_y - 0.0015, 1.410), (0.016, detail_y - 0.001, 1.413), (0.036, detail_y, 1.424)],
        materials["Smile"],
        bevel_depth=0.0025,
    )


def frame_camera():
    mesh = bpy.data.objects.get("female_doctor_mixamo_ready")
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


def setup_lighting():
    light = bpy.data.objects.get("Area")
    if not light:
        bpy.ops.object.light_add(type="AREA", location=(0.0, -3.0, 5.0))
        light = bpy.context.object
    light.location = (0.0, -3.6, 4.8)
    light.rotation_euler = (math.radians(65), 0.0, 0.0)
    light.data.energy = 550
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


def export_fbx():
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "ARMATURE"}:
            obj.select_set(True)
    bpy.ops.export_scene.fbx(
        filepath=str(FBX_PATH),
        use_selection=True,
        apply_unit_scale=True,
        bake_space_transform=False,
        path_mode="AUTO",
        embed_textures=False,
    )


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND_PATH))
    apply_character_colors()
    add_friendly_face_features()
    frame_camera()
    setup_lighting()
    export_fbx()
    render_preview()
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))


if __name__ == "__main__":
    main()
