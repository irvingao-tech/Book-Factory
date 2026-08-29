"""
Contains the face indices of a single book
"""


def get_spine_rails(spine_segments=4):
    """Return matching outer and inner top/bottom rail indices."""
    segments = max(2, int(spine_segments))
    reuse_index = segments // 2
    next_index = 44
    outer_rails = [(20, 21)]
    inner_rails = [(23, 22)]
    for index in range(1, segments):
        if index == reuse_index:
            outer_rails.append((42, 43))
            inner_rails.append((25, 24))
        else:
            outer_rails.append((next_index, next_index + 1))
            inner_rails.append((next_index + 2, next_index + 3))
            next_index += 4
    outer_rails.append((38, 39))
    inner_rails.append((41, 40))
    return outer_rails, inner_rails


def normalized_page_segments(page_curve_segments=6):
    """Clamp page curve resolution and guarantee an exact center rail."""
    segments = min(max(int(page_curve_segments), 4), 12)
    return segments if segments % 2 == 0 else min(segments + 1, 12)


def get_page_rails(spine_segments=4, page_curve_segments=6):
    """Return matching curved-back and straight-front text-block rail indices."""
    spine_count = max(2, int(spine_segments))
    page_count = normalized_page_segments(page_curve_segments)
    next_index = 44 + 4 * (spine_count - 2)
    back_rails = [(7, 6)]
    front_rails = [(3, 2)]
    for _index in range(1, page_count):
        back_rails.append((next_index, next_index + 1))
        front_rails.append((next_index + 2, next_index + 3))
        next_index += 4
    back_rails.append((5, 4))
    front_rails.append((1, 0))
    return back_rails, front_rails


def get_faces(spine_segments=4, page_curve_segments=6):
    """
    Returns the face indices of a single book
    """
    base_faces = [
        [0, 1, 3, 2],
        [6, 7, 5, 4],
        [2, 6, 4, 0],
        [7, 3, 1, 5],
        [8, 9, 11, 10],
        [25, 24, 40, 41],
        [13, 12, 18, 19],
        [10, 14, 12, 8],
        [15, 11, 9, 13],
        [12, 14, 17, 18],
        [15, 13, 19, 16],
        [19, 18, 22, 23],
        [20, 23, 25, 42],
        [18, 17, 21, 22],
        [16, 19, 23, 20],
        [14, 15, 16, 17],
        [17, 16, 20, 21],
        [22, 21, 43, 24],
        [23, 22, 24, 25],
        [26, 28, 29, 27],
        [37, 36, 30, 31],
        [28, 26, 30, 32],
        [33, 31, 27, 29],
        [30, 36, 35, 32],
        [33, 34, 37, 31],
        [41, 40, 36, 37],
        [38, 42, 25, 41],
        [36, 40, 39, 35],
        [34, 38, 41, 37],
        [32, 35, 34, 33],
        [35, 39, 38, 34],
        [40, 24, 43, 39],
        [39, 43, 42, 38],
        [30, 26, 27, 31],
        [28, 32, 33, 29],
        [21, 20, 42, 43],
        [12, 13, 9, 8],
        [10, 11, 15, 14],
    ]

    replaced_faces = {0, 1, 2, 3, 5, 12, 17, 18, 26, 31, 32, 35}
    faces = [face for index, face in enumerate(base_faces) if index not in replaced_faces]
    outer_rails, inner_rails = get_spine_rails(spine_segments)
    for outer_a, outer_b, inner_a, inner_b in zip(
        outer_rails, outer_rails[1:], inner_rails, inner_rails[1:]
    ):
        outer_top_a, outer_bottom_a = outer_a
        outer_top_b, outer_bottom_b = outer_b
        inner_top_a, inner_bottom_a = inner_a
        inner_top_b, inner_bottom_b = inner_b
        faces.append([outer_bottom_a, outer_top_a, outer_top_b, outer_bottom_b])
        faces.append([inner_top_a, inner_bottom_a, inner_bottom_b, inner_top_b])
        faces.append([outer_top_a, inner_top_a, inner_top_b, outer_top_b])
        faces.append([inner_bottom_a, outer_bottom_a, outer_bottom_b, inner_bottom_b])

    back_rails, front_rails = get_page_rails(spine_segments, page_curve_segments)
    for back_a, back_b, front_a, front_b in zip(
        back_rails, back_rails[1:], front_rails, front_rails[1:]
    ):
        back_top_a, back_bottom_a = back_a
        back_top_b, back_bottom_b = back_b
        front_top_a, front_bottom_a = front_a
        front_top_b, front_bottom_b = front_b
        faces.append([front_bottom_b, front_top_b, front_top_a, front_bottom_a])
        faces.append([back_bottom_a, back_top_a, back_top_b, back_bottom_b])
        faces.append([front_bottom_a, back_bottom_a, back_bottom_b, front_bottom_b])
        faces.append([back_top_a, front_top_a, front_top_b, back_top_b])
    return faces
