"""Shared constant-curvature layout helpers."""

from math import cos, sin


def arc_coordinates(distance, total_length, total_angle):
    """Return arc-axis distance, lateral offset, and tangent angle from a fixed start."""
    if total_length <= 1e-12:
        return 0.0, 0.0, 0.0
    distance = min(max(distance, 0.0), total_length)
    if abs(total_angle) <= 1e-8:
        return distance, 0.0, 0.0
    tangent = total_angle * distance / total_length
    radius = total_length / total_angle
    along = radius * sin(tangent)
    lateral = radius * (1.0 - cos(tangent))
    return along, lateral, tangent
