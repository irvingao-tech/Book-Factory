"""
Contains the parameterized vertices of a single book.
"""

from math import atan, cos, pi, sin, tan


def get_vertices(
    page_thickness,
    page_height,
    cover_depth,
    cover_height,
    cover_thickness,
    page_depth,
    hinge_inset,
    hinge_width,
    spine_curl,
    page_curve_match=1.0,
    page_front_curve=0.6,
    page_front_roundness=1.0,
    page_curve_segments=6,
    spine_rounding=1.0,
    spine_segments=4,
):
    """
    Returns the vertices given the dimensions
    """
    spine_angle = atan(spine_curl / cover_thickness)
    spine_offset_center = cover_thickness * cos(spine_angle)
    spine_offset_side = tan(spine_angle / 2) * cover_thickness

    vertices = [
        # textblock
        [-page_thickness / 2, page_depth / 2, -page_height / 2],
        [-page_thickness / 2, page_depth / 2, page_height / 2],
        [page_thickness / 2, page_depth / 2, -page_height / 2],
        [page_thickness / 2, page_depth / 2, page_height / 2],
        [-page_thickness / 2, -page_depth / 2, -page_height / 2],
        [-page_thickness / 2, -page_depth / 2, page_height / 2],
        [page_thickness / 2, -page_depth / 2, -page_height / 2],
        [page_thickness / 2, -page_depth / 2, page_height / 2],
        # left cover
        [page_thickness / 2, cover_depth / 2, -cover_height / 2],
        [page_thickness / 2, cover_depth / 2, cover_height / 2],
        [(page_thickness / 2 + cover_thickness), cover_depth / 2, -cover_height / 2],
        [(page_thickness / 2 + cover_thickness), cover_depth / 2, cover_height / 2],
        [(page_thickness / 2), -page_depth / 2 + hinge_width / 2, -cover_height / 2],
        [(page_thickness / 2), -page_depth / 2 + hinge_width / 2, cover_height / 2],
        [(page_thickness / 2 + cover_thickness), -page_depth / 2 + hinge_width / 2, -cover_height / 2],
        [(page_thickness / 2 + cover_thickness), -page_depth / 2 + hinge_width / 2, cover_height / 2],
        [(page_thickness / 2 + cover_thickness - hinge_inset), -page_depth / 2, cover_height / 2],
        [(page_thickness / 2 + cover_thickness - hinge_inset), -page_depth / 2, -cover_height / 2],
        [(page_thickness / 2), -page_depth / 2, -cover_height / 2],
        [(page_thickness / 2), -page_depth / 2, cover_height / 2],
        [
            (page_thickness / 2 + cover_thickness),
            -page_depth / 2 - hinge_width / 2 - spine_offset_side,
            cover_height / 2,
        ],
        [
            (page_thickness / 2 + cover_thickness),
            -page_depth / 2 - hinge_width / 2 - spine_offset_side,
            -cover_height / 2,
        ],
        [(page_thickness / 2), -page_depth / 2 - hinge_width / 2, -cover_height / 2],
        [(page_thickness / 2), -page_depth / 2 - hinge_width / 2, cover_height / 2],
        [0.0, -cover_depth / 2 - spine_curl, -cover_height / 2],
        [0.0, -cover_depth / 2 - spine_curl, cover_height / 2],
        # right cover
        [-page_thickness / 2, cover_depth / 2, -cover_height / 2],
        [-page_thickness / 2, cover_depth / 2, cover_height / 2],
        [-(page_thickness / 2 + cover_thickness), cover_depth / 2, -cover_height / 2],
        [-(page_thickness / 2 + cover_thickness), cover_depth / 2, cover_height / 2],
        [-(page_thickness / 2), -page_depth / 2 + hinge_width / 2, -cover_height / 2],
        [-(page_thickness / 2), -page_depth / 2 + hinge_width / 2, cover_height / 2],
        [-(page_thickness / 2 + cover_thickness), -page_depth / 2 + hinge_width / 2, -cover_height / 2],
        [-(page_thickness / 2 + cover_thickness), -page_depth / 2 + hinge_width / 2, cover_height / 2],
        [-(page_thickness / 2 + cover_thickness - hinge_inset), -page_depth / 2, cover_height / 2],
        [-(page_thickness / 2 + cover_thickness - hinge_inset), -page_depth / 2, -cover_height / 2],
        [-(page_thickness / 2), -page_depth / 2, -cover_height / 2],
        [-(page_thickness / 2), -page_depth / 2, cover_height / 2],
        [
            -(page_thickness / 2 + cover_thickness),
            -page_depth / 2 - hinge_width / 2 - spine_offset_side,
            cover_height / 2,
        ],
        [
            -(page_thickness / 2 + cover_thickness),
            -page_depth / 2 - hinge_width / 2 - spine_offset_side,
            -cover_height / 2,
        ],
        [-(page_thickness / 2), -page_depth / 2 - hinge_width / 2, -cover_height / 2],
        [-(page_thickness / 2), -page_depth / 2 - hinge_width / 2, cover_height / 2],
        [0.0, -cover_depth / 2 - spine_curl - spine_offset_center, cover_height / 2],
        [0.0, -cover_depth / 2 - spine_curl - spine_offset_center, -cover_height / 2],
    ]

    segments = max(2, int(spine_segments))
    rounding = min(max(float(spine_rounding), 0.0), 1.0)
    reuse_index = segments // 2
    outer_side_y = (vertices[20][1] + vertices[38][1]) / 2.0
    inner_side_y = (vertices[23][1] + vertices[41][1]) / 2.0
    outer_center_y = vertices[42][1]
    inner_center_y = vertices[25][1]
    outer_half_width = vertices[20][0]
    inner_half_width = vertices[23][0]
    shell_width = (
        (vertices[20][0] - vertices[23][0]) ** 2
        + (vertices[20][1] - vertices[23][1]) ** 2
    ) ** 0.5
    def curve_point(factor):
        pointed_profile = 1.0 - abs(2.0 * factor - 1.0)
        rounded_profile = sin(pi * factor)
        profile = pointed_profile * (1.0 - rounding) + rounded_profile * rounding
        outer_x = outer_half_width * cos(pi * factor)
        outer_y = outer_side_y + (outer_center_y - outer_side_y) * profile
        preliminary_inner_x = inner_half_width * cos(pi * factor)
        preliminary_inner_y = inner_side_y + (inner_center_y - inner_side_y) * profile
        offset_x = preliminary_inner_x - outer_x
        offset_y = preliminary_inner_y - outer_y
        offset_length = max((offset_x**2 + offset_y**2) ** 0.5, 1e-12)
        inner_x = outer_x + offset_x / offset_length * shell_width
        inner_y = outer_y + offset_y / offset_length * shell_width
        return outer_x, outer_y, inner_x, inner_y

    for index in range(1, segments):
        factor = index / segments
        outer_x, outer_y, inner_x, inner_y = curve_point(factor)
        outer_top = [outer_x, outer_y, cover_height / 2]
        outer_bottom = [outer_x, outer_y, -cover_height / 2]
        inner_top = [inner_x, inner_y, cover_height / 2]
        inner_bottom = [inner_x, inner_y, -cover_height / 2]

        if index == reuse_index:
            vertices[42] = outer_top
            vertices[43] = outer_bottom
            vertices[25] = inner_top
            vertices[24] = inner_bottom
        else:
            vertices.extend((outer_top, outer_bottom, inner_top, inner_bottom))

    from .faces import normalized_page_segments

    page_segments = normalized_page_segments(page_curve_segments)
    page_match = min(max(float(page_curve_match), 0.0), 2.0)
    front_match = min(max(float(page_front_curve), -1.0), 3.0)
    front_roundness = min(max(float(page_front_roundness), 0.0), 1.0)
    _center_outer_x, _center_outer_y, _center_inner_x, center_inner_y = curve_point(0.5)
    inner_curve_depth = max(inner_side_y - center_inner_y, 0.0)
    page_back_y = -page_depth / 2
    page_front_y = page_depth / 2
    for index in range(1, page_segments):
        factor = index / page_segments
        _outer_x, _outer_y, inner_x, inner_y = curve_point(factor)
        pointed_profile = 1.0 - abs(2.0 * factor - 1.0)
        rounded_profile = sin(pi * factor)
        front_profile = pointed_profile * (1.0 - front_roundness) + rounded_profile * front_roundness
        curved_page_y = page_back_y + (inner_y - inner_side_y) * page_match
        curved_front_y = page_front_y - inner_curve_depth * front_match * front_profile
        vertices.extend(
            (
                [inner_x, curved_page_y, page_height / 2],
                [inner_x, curved_page_y, -page_height / 2],
                [inner_x, curved_front_y, page_height / 2],
                [inner_x, curved_front_y, -page_height / 2],
            )
        )

    return vertices
