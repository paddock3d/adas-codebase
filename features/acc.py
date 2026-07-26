"""Adaptive Cruise Control (ACC) -- ASIL C, priority: High.

Automatically maintains a set speed and a safe following distance/time gap from the vehicle ahead by modulating throttle and brake, without continuous driver input.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.perception import nearest_object_in_zone
from common.driver_monitoring import duration_exceeded


def _speed_to_throttle(current_kph, set_kph, gain=0.05):
    return max(0.0, min(1.0, gain * (set_kph - current_kph)))


def maintain_following_distance(state, set_speed_kph, min_gap_s=1.8):
    """Adjusts throttle/brake command to hold `min_gap_s` seconds of following
    gap to the nearest forward object, capped at `set_speed_kph`.
    Returns a dict with the commanded throttle/brake (0.0 - 1.0 each).
    """
    lead = nearest_object_in_zone(state, ("forward",))
    if lead is None:
        return {"throttle": _speed_to_throttle(state.speed_kph, set_speed_kph), "brake": 0.0}

    gap_s = lead.relative_distance_m / max(state.speed_kph / 3.6, 0.1)
    if gap_s < min_gap_s:
        deficit = (min_gap_s - gap_s) / min_gap_s
        return {"throttle": 0.0, "brake": min(1.0, deficit)}
    return {"throttle": _speed_to_throttle(state.speed_kph, set_speed_kph), "brake": 0.0}

def disengage_on_low_confidence(state, confidence_threshold=0.5):
    """Returns True (ACC disengaged, alert raised) if sensor confidence has
    dropped below `confidence_threshold` or the driver has manually braked.
    """
    lead = nearest_object_in_zone(state, ("forward",))
    low_confidence = lead is not None and lead.confidence < confidence_threshold
    return low_confidence or state.driver_brake_input > 0.0


def hold_at_stop(state, stop_gap_m=3.0, stopped_speed_kph=2.0):
    """Returns True (Stop-and-Go holds the vehicle stationary) if the ego
    vehicle is already at or below `stopped_speed_kph` and the nearest
    forward object is within `stop_gap_m` -- i.e. queued directly behind a
    stopped lead vehicle, not merely slowing toward one further away.
    """
    if state.speed_kph > stopped_speed_kph:
        return False
    lead = nearest_object_in_zone(state, ("forward",))
    return lead is not None and lead.relative_distance_m <= stop_gap_m


def resume_when_lead_departs(state, stop_duration_s, set_speed_kph,
                              resume_gap_m=6.0, max_autonomous_hold_s=180.0):
    """Returns True (Stop-and-Go resumes normal ACC control and moves off)
    once the lead has pulled at least `resume_gap_m` ahead and ACC's own
    following-distance command for `set_speed_kph` calls for forward
    throttle rather than braking. Returns False (stay held, hand back to
    the driver) once `stop_duration_s` exceeds `max_autonomous_hold_s`.
    """
    if duration_exceeded(stop_duration_s, max_autonomous_hold_s):
        return False
    lead = nearest_object_in_zone(state, ("forward",))
    if lead is not None and lead.relative_distance_m < resume_gap_m:
        return False
    command = maintain_following_distance(state, set_speed_kph)
    return command["throttle"] > 0.0
