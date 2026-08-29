"""Fast single-mesh construction for procedural book groupings."""

from math import radians

import bpy
from mathutils import Vector

from .data.creases import get_creases
from .data.uvs import get_uvs


def clear_collection_objects(collection):
    """Remove generated objects and their exclusive meshes in one dependency-graph update."""
    objects = list(collection.objects)
    if not objects:
        return
    object_counts = {}
    for obj in objects:
        if obj.type == "MESH":
            pointer = obj.data.as_pointer()
            object_counts[pointer] = object_counts.get(pointer, 0) + 1
    meshes = {
        obj.data.as_pointer(): obj.data
        for obj in objects
        if obj.type == "MESH" and obj.data.users <= object_counts[obj.data.as_pointer()]
    }
    bpy.data.batch_remove(ids=[*objects, *meshes.values()])


def build_books_object(books, name, with_uvs=True):
    """Build all books into one mesh while retaining per-book metadata."""
    vertices = []
    faces = []
    face_uvs = []
    face_materials = []
    face_book_indices = []
    crease_edges = set()
    materials = []
    material_indices = {}

    def material_index(material):
        if material is None:
            material = bpy.data.materials.get("BookGen Default")
            if material is None:
                material = bpy.data.materials.new("BookGen Default")
                material.diffuse_color = (0.8, 0.8, 0.8, 1.0)
        key = material.as_pointer()
        if key not in material_indices:
            material_indices[key] = len(materials)
            materials.append(material)
        return material_indices[key]

    for book_index, book in enumerate(books):
        vertex_offset = len(vertices)
        vertices.extend(book.rotation @ Vector(vertex) + book.location for vertex in book.vertices)
        faces.extend(tuple(vertex_offset + index for index in face) for face in book.faces)
        face_book_indices.extend([book_index] * len(book.faces))

        for face_index in range(len(book.faces)):
            if face_index >= book.page_face_start and book.page_material is not None:
                material = book.page_material
            else:
                material = book.cover_material
            face_materials.append(material_index(material))

        if with_uvs:
            face_uvs.extend(book.get_uvs())

        crease_edges.update(
            tuple(sorted((vertex_offset + edge[0], vertex_offset + edge[1])))
            for edge in book.creases
        )

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    for material in materials:
        mesh.materials.append(material)

    for polygon, material_slot in zip(mesh.polygons, face_materials):
        polygon.material_index = material_slot
        polygon.use_smooth = True

    if with_uvs:
        uv_layer = mesh.uv_layers.new(name="BookGenUV")
        for polygon, polygon_uvs in zip(mesh.polygons, face_uvs):
            for loop_index, uv in zip(polygon.loop_indices, polygon_uvs):
                uv_layer.data[loop_index].uv = uv

    book_index_attribute = mesh.attributes.new(name="book_index", type="INT", domain="FACE")
    for value, book_index in zip(book_index_attribute.data, face_book_indices):
        value.value = book_index

    crease_attribute = mesh.attributes.new(name="crease_edge", type="FLOAT", domain="EDGE")
    for edge, crease_value in zip(mesh.edges, crease_attribute.data):
        edge_key = tuple(sorted(edge.vertices))
        if edge_key in crease_edges:
            crease_value.value = 1.0

    mesh.update()
    mesh.set_sharp_from_angle(angle=radians(85))

    obj = bpy.data.objects.new(name, mesh)
    obj["bookgen_combined"] = True
    obj["book_count"] = len(books)
    return obj
