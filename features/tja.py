"""Traffic Jam Assist (TJA) -- ASIL D, priority: Critical.

Combines ACC and LKA to provide semi-automated driving in congested traffic below a calibrated speed threshold, with mandatory driver supervision.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.driver_monitoring import duration_exceeded, derate_limit
from features import acc, lka


def engage_combined_control(state, set_speed_kph=None, lane_offset_m=0.0, max_speed_kph=60.0):
    """Combined ACC+LKA control: engages only if speed is below
    `max_speed_kph` and hands are on the wheel, and when engaged it calls
    directly into `features.acc.maintain_following_distance` and
    `features.lka.apply_corrective_steering_torque` to produce the combined
    command, rather than re-implementing that logic locally. Returns a dict:
    {"engaged": bool, "throttle": float, "brake": float, "steering_torque": float}.
    """
    can_engage = state.speed_kph <= max_speed_kph and state.hands_on_wheel
    if not can_engage:
        return {"engaged": False, "throttle": 0.0, "brake": 0.0, "steering_torque": 0.0}

    target_speed = set_speed_kph if set_speed_kph is not None else state.speed_kph
    longitudinal = acc.maintain_following_distance(state, target_speed)
    steering_torque = lka.apply_corrective_steering_torque(state, lane_offset_m)
    return {
        "engaged": True,
        "throttle": longitudinal["throttle"],
        "brake": longitudinal["brake"],
        "steering_torque": steering_torque,
    }

def enforce_hands_on_confirmation(state, confirmation_interval_s=20.0, drowsiness_score=0.0):
    """Returns True if TJA should disengage with an escalating alert because
    hands-on-wheel confirmation was not received within the (possibly
    drowsiness-derated) confirmation interval. `drowsiness_score` is meant
    to be supplied from DDD's `compute_drowsiness_score`; a higher score
    shortens the effective interval via `common.driver_monitoring.derate_limit`.
    """
    effective_interval_s = derate_limit(confirmation_interval_s, drowsiness_score)
    return duration_exceeded(state.drowsiness_confirmation_pending_s, effective_interval_s)
