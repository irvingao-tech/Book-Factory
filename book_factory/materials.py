"""Material helpers for generated books."""

import random

import bpy


def resolve_cover_material(parameters):
    """Return the selected material or a deterministic palette material."""
    if not parameters["random_cover_colors"]:
        return parameters["cover_material"]

    # Quantization keeps the material count bounded while preserving variation.
    step = round(random.random() * 11) / 11
    color_a = parameters["cover_color_primary"]
    color_b = parameters["cover_color_secondary"]
    color = tuple(a + (b - a) * step for a, b in zip(color_a, color_b))
    roughness = parameters["cover_roughness"]
    color_key = "".join(f"{round(channel * 255):02x}" for channel in color[:3])
    roughness_key = round(roughness * 100)
    name = f"BookGen2_Cover_{color_key}_{roughness_key:03d}"

    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
        material.use_nodes = True

    material.diffuse_color = color
    principled = material.node_tree.nodes.get("Principled BSDF") if material.node_tree else None
    if principled:
        principled.inputs["Base Color"].default_value = color
        principled.inputs["Roughness"].default_value = roughness
    return material
