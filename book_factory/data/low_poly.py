"""Single-shell low-poly book geometry with curved spine and fore edge."""

from math import cos, pi, sin


def get_low_poly_geometry(
    width,
    height,
    depth,
    spine_curl,
    spine_rounding,
    page_front_curve,
    page_front_roundness,
    curve_segments,
):
    """Return vertices, quad faces, UVs, and the page-face start index."""
    segments = min(max(1, int(curve_segments)), 6)
    half_width = width / 2.0
    back_side = -depth / 2.0
    front_side = depth / 2.0
    half_height = height / 2.0
    front_depth = max(spine_curl, 0.0) * page_front_curve
    vertices = []

    for index in range(segments + 1):
        factor = index / segments
        pointed = 1.0 - abs(2.0 * factor - 1.0)
        rounded = sin(pi * factor)
        spine_profile = pointed * (1.0 - spine_rounding) + rounded * spine_rounding
        front_profile = pointed * (1.0 - page_front_roundness) + rounded * page_front_roundness
        x = half_width * cos(pi * factor)
        back_y = back_side - spine_curl * spine_profile
        front_y = front_side - front_depth * front_profile
        vertices.extend(
            (
                (x, back_y, half_height),
                (x, back_y, -half_height),
                (x, front_y, half_height),
                (x, front_y, -half_height),
            )
        )

    faces = []
    uvs = []

    def append_strip(face, region_start, region_end, index, count):
        faces.append(face)
        u0 = region_start + (region_end - region_start) * index / count
        u1 = region_start + (region_end - region_start) * (index + 1) / count
        uvs.append(((u0, 0.02), (u0, 0.98), (u1, 0.98), (u1, 0.02)))

    for index in range(segments):
        current = index * 4
        following = (index + 1) * 4
        append_strip((current + 1, current, following, following + 1), 0.0, 0.2, index, segments)
    for index in range(segments):
        current = index * 4
        following = (index + 1) * 4
        append_strip((current, current + 2, following + 2, following), 0.2, 0.4, index, segments)
    for index in range(segments):
        current = index * 4
        following = (index + 1) * 4
        append_strip((current + 3, current + 1, following + 1, following + 3), 0.4, 0.6, index, segments)

    last = segments * 4
    faces.append((1, 3, 2, 0))
    uvs.append(((0.60, 0.02), (0.60, 0.98), (0.70, 0.98), (0.70, 0.02)))
    faces.append((last + 1, last, last + 2, last + 3))
    uvs.append(((0.70, 0.02), (0.70, 0.98), (0.80, 0.98), (0.80, 0.02)))

    page_face_start = len(faces)
    for index in range(segments):
        current = index * 4
        following = (index + 1) * 4
        append_strip((following + 3, following + 2, current + 2, current + 3), 0.8, 1.0, index, segments)

    return vertices, faces, uvs, page_face_start
