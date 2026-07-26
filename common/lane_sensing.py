"""Shared lane-geometry helpers used by lane-position features.

LDW and LKA both reason about lane offset relative to the same lane
boundary definition, so both rely on this single implementation rather
than each defining their own crossing rule. Sanitized sample code only.
"""


def lane_boundary_crossed(lane_offset_m, lane_half_width_m):
    """Return True if `lane_offset_m` has crossed the lane boundary."""
    return abs(lane_offset_m) > lane_half_width_m
