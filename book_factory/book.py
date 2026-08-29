# ====================== BEGIN GPL LICENSE BLOCK ======================
#    This file is part of the  bookGen-addon for generating books in Blender
#    Copyright (c) 2014 Oliver Weissbarth
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ======================= END GPL LICENSE BLOCK ========================

"""
This file contains the book class
"""

from math import radians, atan

import bpy
import bmesh
from mathutils import Vector, Matrix

from .data.vertices import get_vertices
from .data.faces import get_faces, normalized_page_segments
from .data.uvs import get_uvs
from .data.creases import get_creases
from .data.low_poly import get_low_poly_geometry


class Book:
    """
    This stores information about a single book. It can export the book as blender object
    or return the raw geometry for previz.
    """

    def __init__(
        self,
        cover_height,
        cover_thickness,
        cover_depth,
        page_height,
        page_depth,
        page_thickness,
        spine_curl,
        hinge_inset,
        hinge_width,
        lean=0,
        lean_angle=0,
        subsurf=False,
        cover_material=None,
        page_material=None,
        preset_key="CUSTOM",
        page_curve_match=1.0,
        page_front_curve=0.6,
        page_front_roundness=1.0,
        page_curve_segments=6,
        spine_rounding=1.0,
        spine_segments=4,
        planar_offset=0.0,
        low_poly=False,
        low_poly_segments=4,
    ):
        self.height = cover_height
        self.width = page_thickness + 2 * cover_thickness
        self.depth = cover_depth
        self.lean_angle = lean_angle
        self.lean = lean
        self.page_thickness = page_thickness
        self.page_height = page_height
        self.page_depth = page_depth
        self.cover_depth = cover_depth
        self.cover_height = cover_height
        self.cover_thickness = cover_thickness
        self.hinge_inset = hinge_inset
        self.hinge_width = hinge_width
        self.spine_curl = spine_curl
        self.subsurf = subsurf
        self.cover_material = cover_material
        self.page_material = page_material
        self.preset_key = preset_key
        self.page_curve_match = page_curve_match
        self.page_front_curve = page_front_curve
        self.page_front_roundness = page_front_roundness
        unified_segments = normalized_page_segments(max(int(page_curve_segments), int(spine_segments)))
        self.page_curve_segments = unified_segments
        self.spine_rounding = spine_rounding
        self.spine_segments = unified_segments
        self.low_poly = low_poly
        self.low_poly_segments = min(max(int(low_poly_segments), 2), 6)
        self.planar_offset = (
            Vector((0.0, float(planar_offset)))
            if isinstance(planar_offset, (int, float))
            else Vector(planar_offset)
        )
        self.location = Vector([0, 0, 0])
        self.rotation = Vector([0, 0, 0])

        self.obj = None

        if low_poly:
            self.vertices, self.faces, self._uvs, self.page_face_start = get_low_poly_geometry(
                self.width,
                cover_height,
                cover_depth,
                spine_curl,
                spine_rounding,
                page_front_curve,
                page_front_roundness,
                self.low_poly_segments,
            )
            self.creases = []
        else:
            self.vertices = get_vertices(
                page_thickness,
                page_height,
                cover_depth,
                cover_height,
                cover_thickness,
                page_depth,
                hinge_inset,
                hinge_width,
                spine_curl,
                page_curve_match,
                page_front_curve,
                page_front_roundness,
                self.page_curve_segments,
                spine_rounding,
                self.spine_segments,
            )
            self.faces = get_faces(self.spine_segments, self.page_curve_segments)
            self.page_face_start = len(self.faces) - 4 * self.page_curve_segments
            self.creases = get_creases(self.spine_segments)

    def to_object(self, with_uvs=False):
        """
        Exports the book as a blender object
        """

        def index_to_vert(face):
            lst = []
            for i in face:
                lst.append(vert_ob[i])
            return tuple(lst)

        mesh = bpy.data.meshes.new("book")

        creases = self.creases

        if with_uvs:
            uvs = self.get_uvs()

        self.obj = bpy.data.objects.new("book", mesh)

        bm = bmesh.new()
        bm.from_mesh(mesh)
        vert_ob = []
        for vert in self.vertices:
            vert_ob.append(bm.verts.new(vert))

        bm.verts.index_update()
        bm.verts.ensure_lookup_table()

        crease_layer = bm.edges.layers.float.new("crease_edge")
        for crease in creases:
            edge = bm.edges.new((bm.verts[crease[0]], bm.verts[crease[1]]))
            edge[crease_layer] = 1.0

        for face_index in self.faces:
            face = bm.faces.new(index_to_vert(face_index))
            face.smooth = True

        bm.faces.index_update()
        bm.edges.ensure_lookup_table()

        if with_uvs:
            uv_layer = bm.loops.layers.uv.verify()
            for face, face_uvs in zip(bm.faces, uvs):
                for loop, uv in zip(face.loops, face_uvs):
                    loop_uv = loop[uv_layer]
                    loop_uv.uv.x = uv[0]
                    loop_uv.uv.y = uv[1]

        bm.normal_update()

        if self.cover_material:
            if self.obj.data.materials:
                self.obj.data.materials[0] = self.cover_material
            else:
                self.obj.data.materials.append(self.cover_material)

        if self.page_material:
            self.obj.data.materials.append(self.page_material)
            bm.faces.ensure_lookup_table()
            for face in bm.faces[self.page_face_start :]:
                face.material_index = 1

        self.obj.matrix_world = Matrix.Translation(self.location) @ self.rotation.to_4x4()

        bm.to_mesh(mesh)
        bm.free()

        if bpy.app.version >= (4,1,0):
            mesh.set_sharp_from_angle(angle=radians(85))
        else:
            mesh.use_auto_smooth = True
            mesh.auto_smooth_angle = radians(85)

        return self.obj

    def get_uvs(self):
        """Return UV coordinates matching the selected geometry model."""
        if self.low_poly:
            return self._uvs
        return get_uvs(
            self.page_thickness,
            self.page_height,
            self.cover_depth,
            self.cover_height,
            self.cover_thickness,
            self.page_depth,
            self.hinge_inset,
            self.hinge_width,
            self.spine_curl,
            self.page_curve_match,
            self.page_front_curve,
            self.page_front_roundness,
            self.page_curve_segments,
            self.spine_rounding,
            self.spine_segments,
        )

    def get_geometry(self):
        """
        Returns the raw geometry of a book
        """
        transformed_verts = map(lambda v: self.rotation @ Vector(v) + self.location, self.vertices)
        return transformed_verts, self.faces
