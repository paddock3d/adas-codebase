"""Autonomous Emergency Braking (AEB) -- ASIL D, priority: Critical.

Automatically applies braking to avoid or mitigate a forward collision when the driver does not respond in time to a detected imminent collision.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.perception import nearest_object_in_zone, time_to_collision
from common.driver_response import driver_has_responded


def trigger_autonomous_braking(state, ttc_threshold_s=0.5, driver_brake_threshold=0.7):
    """Returns True if autonomous full braking should be triggered: an object
    is on a collision course within `ttc_threshold_s` and the driver has not
    applied sufficient braking or steering to avoid it.
    """
    obj = nearest_object_in_zone(state, ("forward",))
    ttc = time_to_collision(obj)
    if ttc is None:
        return False
    responded = driver_has_responded(state, driver_brake_threshold, allow_steering_override=True)
    return ttc <= ttc_threshold_s and not responded

def issue_precollision_warning(state, warning_lead_time_s=0.6):
    """Returns True if a pre-collision warning should be raised, i.e. TTC is
    within `warning_lead_time_s` of the autonomous-braking trigger point.
    """
    obj = nearest_object_in_zone(state, ("forward",))
    ttc = time_to_collision(obj)
    return ttc is not None and ttc <= warning_lead_time_s


def _nearest_cross_traffic_object(state):
    """Nearest object among the left/right cross-traffic zones, or None."""
    left = nearest_object_in_zone(state, ("cross_left",))
    right = nearest_object_in_zone(state, ("cross_right",))
    candidates = [o for o in (left, right) if o is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda o: o.relative_distance_m)


def trigger_cross_traffic_braking(state, ttc_threshold_s=0.8):
    """Returns True if autonomous braking should be triggered for a crossing
    object at a junction (Junction & Cross-Traffic Braking). Checks the
    existing forward-collision trigger first -- if that is already braking
    for a forward hazard this cycle, junction/cross-traffic braking does not
    also fire, to avoid two conflicting brake commands for the same event.
    """
    if trigger_autonomous_braking(state):
        return False
    obj = _nearest_cross_traffic_object(state)
    ttc = time_to_collision(obj)
    return ttc is not None and ttc <= ttc_threshold_s


def issue_cross_traffic_warning(state, warning_lead_time_s=1.2):
    """Returns True if a pre-collision warning for crossing traffic should be
    raised, i.e. TTC to the nearest cross-traffic object is within
    `warning_lead_time_s` of the junction/cross-traffic braking trigger
    point.
    """
    obj = _nearest_cross_traffic_object(state)
    ttc = time_to_collision(obj)
    return ttc is not None and ttc <= warning_lead_time_s
