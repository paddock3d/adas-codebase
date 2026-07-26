"""Surround View Monitor (SVM) -- ASIL A, priority: Low.

Combines multiple camera feeds into a 360-degree top-down view with overlaid proximity warnings for low-speed maneuvers.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.proximity import warning_intensity


def compose_surround_view(camera_frames):
    """Combines a dict of {camera_name: frame} into a single ordered
    composite for the 360-degree view. Returns the ordered frame list.
    """
    order = ["front", "rear", "left", "right"]
    return [camera_frames[name] for name in order if name in camera_frames]

def overlay_proximity_warnings(composite_view, state, warn_distance_m=1.0):
    """Returns the composite view annotated with proximity-warning markers for
    any object within `warn_distance_m`.
    """
    warnings = [
        o.object_id for o in state.detected_objects
        if warning_intensity(o.relative_distance_m, warn_distance_m) > 0.0
    ]
    return {"view": composite_view, "proximity_warnings": warnings}
