"""Lane Keep Assist (LKA) -- ASIL C, priority: High.

Applies corrective steering torque to keep the vehicle centered within its detected lane.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.lane_sensing import lane_boundary_crossed
from common.driver_monitoring import duration_exceeded


def apply_corrective_steering_torque(state, lane_offset_m, max_torque_nm=3.0, gain=1.5,
                                      lane_half_width_m=1.75, boundary_gain_multiplier=1.0):
    """Returns the corrective steering torque (Nm), proportional to lane
    offset and clamped to `max_torque_nm`. Once the shared lane boundary
    (see `common.lane_sensing`) has actually been crossed, `gain` is scaled
    by `boundary_gain_multiplier` (defaults to no change).
    """
    effective_gain = gain
    if lane_boundary_crossed(lane_offset_m, lane_half_width_m):
        effective_gain = gain * boundary_gain_multiplier
    torque = -effective_gain * lane_offset_m
    return max(-max_torque_nm, min(max_torque_nm, torque))

def disengage_on_hands_off(state, max_hands_off_s=15.0):
    """Returns True if LKA should disengage and alert the driver because
    hands-off-wheel duration exceeded `max_hands_off_s`.
    """
    return (not state.hands_on_wheel) and duration_exceeded(state.hands_off_duration_s, max_hands_off_s)
