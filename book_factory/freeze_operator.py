"""Merge a generated grouping into one editable mesh with ordered UV tiles."""

from math import ceil, sqrt

import bpy
from bpy.props import FloatProperty
from mathutils import Vector

from .utils import get_active_grouping


class BOOKGEN_OT_MergeFreeze(bpy.types.Operator):
    """Create a frozen copy of the active Book Factory grouping."""

    bl_idname = "bookgen.merge_freeze"
    bl_label = "Merge & Freeze"
    bl_description = (
        "Create an independent frozen mesh copy while preserving the editable Book Factory source group"
    )
    bl_options = {"REGISTER", "UNDO"}

    uv_padding: FloatProperty(
        name="UV Tile Padding",
        description="Padding inside each book's UV grid cell",
        subtype="FACTOR",
        min=0.0,
        max=0.2,
        default=0.03,
    )

    @classmethod
    def poll(cls, context):
        if context.mode != "OBJECT":
            return False
        grouping = get_active_grouping(context, create=False)
        return grouping is not None and any(obj.type == "MESH" for obj in grouping.objects)

    def execute(self, context):
        grouping = get_active_grouping(context, create=False)
        source_objects = [obj for obj in grouping.objects if obj.type == "MESH"]
        if not source_objects:
            self.report({"ERROR"}, "The active Book Factory group contains no mesh objects")
            return {"CANCELLED"}

        total_book_count = sum(max(1, int(obj.get("book_count", 1))) for obj in source_objects)
        columns = max(1, ceil(sqrt(total_book_count)))
        rows = max(1, ceil(total_book_count / columns))
        padding = self.uv_padding
        depsgraph = context.evaluated_depsgraph_get()

        vertices = []
        faces = []
        face_uvs = []
        face_materials = []
        face_smooth = []
        face_book_indices = []
        sharp_edges = set()
        materials = []
        material_indices = {}

        def material_index(material):
            if material is None:
                material = bpy.data.materials.get("BookGen Frozen Default")
                if material is None:
                    material = bpy.data.materials.new("BookGen Frozen Default")
                    material.diffuse_color = (0.8, 0.8, 0.8, 1.0)
            key = material.as_pointer()
            if key not in material_indices:
                material_indices[key] = len(materials)
                materials.append(material)
            return material_indices[key]

        book_index_offset = 0
        for source_object in source_objects:
            evaluated_object = None
            if source_object.modifiers:
                evaluated_object = source_object.evaluated_get(depsgraph)
                source_mesh = evaluated_object.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                matrix = evaluated_object.matrix_world
            else:
                source_mesh = source_object.data
                matrix = source_object.matrix_world
            vertex_offset = len(vertices)
            vertices.extend(matrix @ vertex.co for vertex in source_mesh.vertices)

            source_materials = list(source_mesh.materials)
            uv_data = source_mesh.uv_layers.active.data if source_mesh.uv_layers.active else None
            source_book_count = max(1, int(source_object.get("book_count", 1)))
            source_book_attribute = source_mesh.attributes.get("book_index")

            for edge in source_mesh.edges:
                if getattr(edge, "use_edge_sharp", False):
                    sharp_edges.add(
                        tuple(sorted((vertex_offset + edge.vertices[0], vertex_offset + edge.vertices[1])))
                    )

            for polygon in source_mesh.polygons:
                local_book_index = (
                    source_book_attribute.data[polygon.index].value
                    if source_book_attribute is not None
                    and source_book_attribute.domain == "FACE"
                    and polygon.index < len(source_book_attribute.data)
                    else 0
                )
                book_index = min(book_index_offset + local_book_index, total_book_count - 1)
                tile_column = book_index % columns
                tile_row = rows - 1 - book_index // columns
                faces.append(tuple(vertex_offset + vertex_index for vertex_index in polygon.vertices))
                source_material = (
                    source_materials[polygon.material_index]
                    if polygon.material_index < len(source_materials)
                    else None
                )
                face_materials.append(material_index(source_material))
                face_smooth.append(polygon.use_smooth)
                face_book_indices.append(book_index)

                polygon_uvs = []
                for loop_index in polygon.loop_indices:
                    uv = uv_data[loop_index].uv if uv_data else (0.5, 0.5)
                    u = min(max(float(uv[0]), 0.0), 1.0)
                    v = min(max(float(uv[1]), 0.0), 1.0)
                    polygon_uvs.append(
                        (
                            (tile_column + padding + u * (1.0 - 2.0 * padding)) / columns,
                            (tile_row + padding + v * (1.0 - 2.0 * padding)) / rows,
                        )
                    )
                face_uvs.append(polygon_uvs)

            if evaluated_object is not None:
                evaluated_object.to_mesh_clear()
            book_index_offset += source_book_count

        if not vertices or not faces:
            self.report({"ERROR"}, "Unable to evaluate the generated book meshes")
            return {"CANCELLED"}

        minimum = Vector((min(v.x for v in vertices), min(v.y for v in vertices), min(v.z for v in vertices)))
        maximum = Vector((max(v.x for v in vertices), max(v.y for v in vertices), max(v.z for v in vertices)))
        origin = (minimum + maximum) / 2.0
        local_vertices = [vertex - origin for vertex in vertices]

        merged_mesh = bpy.data.meshes.new(f"{grouping.name}_Frozen")
        merged_mesh.from_pydata(local_vertices, [], faces)
        for material in materials:
            merged_mesh.materials.append(material)

        uv_layer = merged_mesh.uv_layers.new(name="Book_Order_UV")
        for polygon, polygon_uvs, material_slot, smooth in zip(
            merged_mesh.polygons, face_uvs, face_materials, face_smooth
        ):
            polygon.material_index = material_slot
            polygon.use_smooth = smooth
            for loop_index, uv in zip(polygon.loop_indices, polygon_uvs):
                uv_layer.data[loop_index].uv = uv

        for edge in merged_mesh.edges:
            if tuple(sorted(edge.vertices)) in sharp_edges:
                edge.use_edge_sharp = True

        book_index_attribute = merged_mesh.attributes.new(name="book_index", type="INT", domain="FACE")
        for attribute_value, book_index in zip(book_index_attribute.data, face_book_indices):
            attribute_value.value = book_index
        merged_mesh.update()

        merged_object = bpy.data.objects.new(f"{grouping.name}_Frozen", merged_mesh)
        merged_object.location = origin
        merged_object["bookgen_frozen"] = True
        merged_object["book_count"] = total_book_count
        merged_object["uv_grid_columns"] = columns
        merged_object["uv_grid_rows"] = rows
        merged_object["source_group"] = grouping.name
        context.scene.collection.objects.link(merged_object)

        for selected_object in context.selected_objects:
            selected_object.select_set(False)
        merged_object.select_set(True)
        context.view_layer.objects.active = merged_object

        self.report(
            {"INFO"},
            f"Created frozen copy of {total_book_count} books with a {columns} x {rows} ordered UV grid",
        )
        return {"FINISHED"}
