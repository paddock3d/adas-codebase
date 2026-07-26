"""Lane Departure Warning (LDW) -- ASIL C, priority: High.

Detects unintended lane departures using forward camera lane-marking data and alerts the driver.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.lane_sensing import lane_boundary_crossed


def detect_unintended_departure(state, lane_offset_m, lane_half_width_m=1.75):
    """Returns True if the vehicle has crossed the lane boundary with no
    matching turn signal.
    """
    crossed = lane_boundary_crossed(lane_offset_m, lane_half_width_m)
    signaling_that_way = (
        (lane_offset_m > 0 and state.turn_signal == "right")
        or (lane_offset_m < 0 and state.turn_signal == "left")
    )
    return crossed and not signaling_that_way

def suppress_warning_below_speed_or_confidence(state, min_speed_kph=60.0, min_confidence=0.6):
    """Returns True if LDW should be suppressed due to low speed or unreliable
    lane-marking detection.
    """
    return state.speed_kph < min_speed_kph or state.lane_marking_confidence < min_confidence
