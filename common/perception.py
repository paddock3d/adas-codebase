"""Shared perception helpers used by multiple ADAS features.

Every feature that reasons about a detected object's zone or closing time
calls into these helpers, so a change here (e.g. how "forward" defaults
are matched, or how time-to-collision is computed) simultaneously affects
ACC, AEB, FCW, BSM, RCTA, and AHC. Sanitized sample code only.
"""


def objects_in_zones(state, zones):
    """Return all detected objects whose `zone` is in `zones`.

    An object with `zone is None` is treated as being in the "forward"
    zone for convenience (this is the untagged default for a plain
    forward-radar/camera detection).
    """
    zones = set(zones)
    return [
        o for o in state.detected_objects
        if (o.zone in zones) or (o.zone is None and "forward" in zones)
    ]


def nearest_object_in_zone(state, zones):
    """Return the nearest object among `objects_in_zones(state, zones)`."""
    candidates = objects_in_zones(state, zones)
    if not candidates:
        return None
    return min(candidates, key=lambda o: o.relative_distance_m)


def time_to_collision(obj):
    """Return time-to-collision in seconds for a closing object, or None.

    Only defined when the object is closing (negative relative speed).
    """
    if obj is None or obj.relative_speed_mps >= 0:
        return None
    return obj.relative_distance_m / abs(obj.relative_speed_mps)
