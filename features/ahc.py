"""Adaptive Headlight Control (AHC) -- ASIL A, priority: Low.

Automatically adjusts headlight beam pattern based on ambient light, oncoming traffic, and vehicle speed.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.perception import objects_in_zones


def select_beam_pattern(state, low_light_threshold_lux=5.0, min_high_beam_speed_kph=40.0):
    """Returns "high" or "low" beam selection based on ambient light and speed.
    """
    if state.ambient_light_lux <= low_light_threshold_lux and state.speed_kph >= min_high_beam_speed_kph:
        return "high"
    return "low"

def suppress_high_beam_near_traffic(state, detection_range_m=250.0):
    """Returns True if automatic high-beam should be suppressed because an
    oncoming or preceding vehicle is within `detection_range_m`.
    """
    nearby = objects_in_zones(state, ("forward", "oncoming"))
    return any(o.relative_distance_m <= detection_range_m for o in nearby)
