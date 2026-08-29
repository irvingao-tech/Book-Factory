"""
Contains the parameterized uvs of a single book.
"""


def get_uvs(
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
    margin=0.02,
):
    """
    Returns the parameterized uvs of a single book.
    """
    # generate all islands starting at left bottom corner (0,0)
    top_face = 0
    top = [[0, 0], [page_height, 0], [page_height, page_thickness], [0, page_thickness]]
    bottom_face = 1
    bottom = [[0, 0], [page_height, 0], [page_height, page_thickness], [0, page_thickness]]
    left_face = 2
    left = [[0, 0], [page_depth, 0], [page_depth, page_thickness], [0, page_thickness]]
    right_face = 3
    right = [[0, 0], [page_depth, 0], [page_depth, page_thickness], [0, page_thickness]]

    exterior_faces = [
        4,
        37,
        7,
        8,
        9,
        13,
        15,
        16,
        10,
        14,
        17,
        35,
        12,
        31,
        32,
        26,
        27,
        30,
        28,
        23,
        29,
        24,
        21,
        34,
        22,
        19,
    ]
    exterior = [
        [
            [cover_thickness, 0],
            [cover_thickness + cover_height, 0],
            [cover_thickness + cover_height, cover_thickness],
            [cover_thickness, cover_thickness],
        ],
        [
            [cover_thickness, cover_thickness],
            [cover_thickness + cover_height, cover_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth],
            [cover_thickness, cover_thickness + cover_depth],
        ],
        [
            [cover_thickness, cover_thickness],
            [cover_thickness, cover_thickness + cover_depth],
            [0, cover_thickness + cover_depth],
            [0, cover_thickness],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth],
            [cover_thickness + cover_height, cover_thickness],
            [cover_thickness * 2 + cover_height, cover_thickness],
            [cover_thickness * 2 + cover_height, cover_thickness + cover_depth],
        ],
        [
            [0, cover_thickness + cover_depth],
            [cover_thickness, cover_thickness + cover_depth],
            [cover_thickness, cover_thickness + cover_depth + hinge_width / 2],
            [0, cover_thickness + cover_depth + hinge_width / 2],
        ],
        [
            [0, cover_thickness + cover_depth + hinge_width / 2],
            [cover_thickness, cover_thickness + cover_depth + hinge_width / 2],
            [cover_thickness, cover_thickness + cover_depth + hinge_width],
            [0, cover_thickness + cover_depth + hinge_width],
        ],
        [
            [cover_thickness, cover_thickness + cover_depth],
            [cover_thickness + cover_height, cover_thickness + cover_depth],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width / 2],
            [cover_thickness, cover_thickness + cover_depth + hinge_width / 2],
        ],
        [
            [cover_thickness, cover_thickness + cover_depth + hinge_width / 2],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width / 2],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width],
            [cover_thickness, cover_thickness + cover_depth + hinge_width],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width / 2],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width / 2],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width / 2],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width / 2],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width],
        ],
        [
            [0, cover_thickness + cover_depth + hinge_width],
            [cover_thickness, cover_thickness + cover_depth + hinge_width],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [0, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
        ],
        [
            [cover_thickness, cover_thickness + cover_depth + hinge_width],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
        ],
        [
            [0, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness],
            [0, cover_thickness + cover_depth + hinge_width + page_thickness],
        ],
        [
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness / 2],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness],
        ],
        [
            [0, cover_thickness + cover_depth + hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [0, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + hinge_width + page_thickness],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
        ],
        [
            [0, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [0, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + 1.5 * hinge_width + page_thickness],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [0, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [0, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness + cover_height, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [2 * cover_thickness + cover_height, cover_thickness + cover_depth + 2 * hinge_width + page_thickness],
            [2 * cover_thickness + cover_height, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [cover_thickness, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness + cover_height, cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness + cover_height, 2 * cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
            [cover_thickness, 2 * cover_thickness + 2 * cover_depth + 2 * hinge_width + page_thickness],
        ],
    ]

    interior_faces = [33, 20, 25, 5, 18, 11, 6, 36]
    interior = [
        [[0, 0], [cover_height, 0], [cover_height, cover_depth], [0, cover_depth]],
        [
            [0, cover_depth],
            [cover_height, cover_depth],
            [cover_height, cover_depth + hinge_width / 2],
            [0, cover_depth + hinge_width / 2],
        ],
        [
            [0, cover_depth + hinge_width / 2],
            [cover_height, cover_depth + hinge_width / 2],
            [cover_height, cover_depth + hinge_width],
            [0, cover_depth + hinge_width],
        ],
        [
            [0, cover_depth + hinge_width],
            [cover_height, cover_depth + hinge_width],
            [cover_height, cover_depth + hinge_width + page_thickness / 2],
            [0, cover_depth + hinge_width + page_thickness / 2],
        ],
        [
            [0, cover_depth + hinge_width + page_thickness / 2],
            [cover_height, cover_depth + hinge_width + page_thickness / 2],
            [cover_height, cover_depth + hinge_width + page_thickness],
            [0, cover_depth + hinge_width + page_thickness],
        ],
        [
            [0, cover_depth + hinge_width + page_thickness],
            [cover_height, cover_depth + hinge_width + page_thickness],
            [cover_height, cover_depth + 1.5 * hinge_width + page_thickness],
            [0, cover_depth + 1.5 * hinge_width + page_thickness],
        ],
        [
            [0, cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_height, cover_depth + 1.5 * hinge_width + page_thickness],
            [cover_height, cover_depth + 2 * hinge_width + page_thickness],
            [0, cover_depth + 2 * hinge_width + page_thickness],
        ],
        [
            [0, cover_depth + 2 * hinge_width + page_thickness],
            [cover_height, cover_depth + 2 * hinge_width + page_thickness],
            [cover_height, 2 * cover_depth + 2 * hinge_width + page_thickness],
            [0, 2 * cover_depth + 2 * hinge_width + page_thickness],
        ],
    ]

    islands = [top, bottom, left, right, exterior, interior]

    # compute effective size of all islands combined without margin
    x = max(cover_thickness * 2 + 2 * cover_height, page_height + page_depth)
    y = page_thickness * 2 + cover_thickness * 2 + 2 * hinge_width + page_thickness + 2 * cover_depth

    if x > y:
        longest_side = x
        margins = 3 * margin
    else:
        longest_side = y
        margins = 4 * margin

    scale_factor = (1 - margins) / longest_side
    # scale islands to fit layout

    for v in range(len(top)):
        for co in range(len(top[v])):
            top[v][co] *= scale_factor

    for v in range(len(bottom)):
        for co in range(len(bottom[v])):
            bottom[v][co] *= scale_factor

    for v in range(len(left)):
        for co in range(len(left[v])):
            left[v][co] *= scale_factor

    for v in range(len(right)):
        for co in range(len(right[v])):
            right[v][co] *= scale_factor

    for f in range(len(exterior)):
        for v in range(len(exterior[f])):
            for co in range(len(exterior[f][v])):
                exterior[f][v][co] *= scale_factor

    for f in range(len(interior)):
        for v in range(len(interior[f])):
            for co in range(len(interior[f][v])):
                interior[f][v][co] *= scale_factor

    # position islands in uv map

    exterior_y = scale_factor * (2 * cover_thickness + 2 * cover_depth + page_thickness + 2 * hinge_width)

    interior_y = scale_factor * (2 * cover_depth + page_thickness + 2 * hinge_width)

    exterior_x = scale_factor * (2 * cover_thickness + cover_height)

    for v in range(len(top)):
        top[v][0] += margin
        top[v][1] += 1 - margin - scale_factor * page_thickness

    for v in range(len(left)):
        left[v][0] += 2 * margin + scale_factor * page_height
        left[v][1] += 1 - margin - scale_factor * page_thickness

    for v in range(len(bottom)):
        bottom[v][0] += margin
        bottom[v][1] += margin

    for v in range(len(right)):
        right[v][0] += 2 * margin + scale_factor * page_height
        right[v][1] += margin

    for f in range(len(interior)):
        for v in range(len(interior[f])):
            interior[f][v][0] += 2 * margin + exterior_x
            interior[f][v][1] += 0.5 - interior_y / 2

    for f in range(len(exterior)):
        for v in range(len(exterior[f])):
            exterior[f][v][0] += margin
            exterior[f][v][1] += 0.5 - exterior_y / 2

    def find_uvs_for_face(face_id):
        if face_id in exterior_faces:
            return exterior[exterior_faces.index(face_id)]
        if face_id in interior_faces:
            return interior[interior_faces.index(face_id)]
        if face_id == top_face:
            return top
        if face_id == bottom_face:
            return bottom
        if face_id == left_face:
            return left
        if face_id == right_face:
            return right

    total_faces = len(exterior_faces) + len(interior_faces) + 4
    uvs = [None] * total_faces
    for i in range(total_faces):
        uvs[i] = find_uvs_for_face(i)

    from .faces import normalized_page_segments

    spine_count = max(2, int(spine_segments))
    page_count = normalized_page_segments(page_curve_segments)
    replaced_faces = {0, 1, 2, 3, 5, 12, 17, 18, 26, 31, 32, 35}
    dynamic_uvs = [face_uvs for index, face_uvs in enumerate(uvs) if index not in replaced_faces]

    def bounds(face_indices):
        points = [point for face_index in face_indices for point in uvs[face_index]]
        return (
            min(point[0] for point in points),
            max(point[0] for point in points),
            min(point[1] for point in points),
            max(point[1] for point in points),
        )

    outer_bounds = bounds((32, 35))
    inner_bounds = bounds((5, 18))
    top_bounds = bounds((12, 26))
    bottom_bounds = bounds((17, 31))
    page_front_bounds = bounds((0,))
    page_back_bounds = bounds((1,))
    page_bottom_bounds = bounds((2,))
    page_top_bounds = bounds((3,))

    def segment_range(region, index, segment_count):
        min_u, max_u, min_v, max_v = region
        u0 = min_u + (max_u - min_u) * index / segment_count
        u1 = min_u + (max_u - min_u) * (index + 1) / segment_count
        return u0, u1, min_v, max_v

    for index in range(spine_count):
        outer_u0, outer_u1, outer_v0, outer_v1 = segment_range(outer_bounds, index, spine_count)
        inner_u0, inner_u1, inner_v0, inner_v1 = segment_range(inner_bounds, index, spine_count)
        top_u0, top_u1, top_v0, top_v1 = segment_range(top_bounds, index, spine_count)
        bottom_u0, bottom_u1, bottom_v0, bottom_v1 = segment_range(bottom_bounds, index, spine_count)
        dynamic_uvs.append(
            [[outer_u0, outer_v0], [outer_u0, outer_v1], [outer_u1, outer_v1], [outer_u1, outer_v0]]
        )
        dynamic_uvs.append(
            [[inner_u0, inner_v1], [inner_u0, inner_v0], [inner_u1, inner_v0], [inner_u1, inner_v1]]
        )
        dynamic_uvs.append(
            [[top_u0, top_v0], [top_u0, top_v1], [top_u1, top_v1], [top_u1, top_v0]]
        )
        dynamic_uvs.append(
            [[bottom_u0, bottom_v1], [bottom_u0, bottom_v0], [bottom_u1, bottom_v0], [bottom_u1, bottom_v1]]
        )

    for index in range(page_count):
        front_u0, front_u1, front_v0, front_v1 = segment_range(page_front_bounds, index, page_count)
        back_u0, back_u1, back_v0, back_v1 = segment_range(page_back_bounds, index, page_count)
        bottom_u0, bottom_u1, bottom_v0, bottom_v1 = segment_range(page_bottom_bounds, index, page_count)
        top_u0, top_u1, top_v0, top_v1 = segment_range(page_top_bounds, index, page_count)
        dynamic_uvs.append(
            [[front_u1, front_v0], [front_u1, front_v1], [front_u0, front_v1], [front_u0, front_v0]]
        )
        dynamic_uvs.append(
            [[back_u0, back_v0], [back_u0, back_v1], [back_u1, back_v1], [back_u1, back_v0]]
        )
        dynamic_uvs.append(
            [[bottom_u0, bottom_v0], [bottom_u0, bottom_v1], [bottom_u1, bottom_v1], [bottom_u1, bottom_v0]]
        )
        dynamic_uvs.append(
            [[top_u0, top_v1], [top_u0, top_v0], [top_u1, top_v0], [top_u1, top_v1]]
        )
    return dynamic_uvs
