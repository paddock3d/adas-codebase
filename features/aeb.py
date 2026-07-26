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
