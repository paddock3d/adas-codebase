"""Forward Collision Warning (FCW) -- ASIL C, priority: High.

Warns the driver of an impending collision with a forward vehicle or obstacle based on calculated time-to-collision (TTC).

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.perception import nearest_object_in_zone, time_to_collision
from common.driver_response import driver_has_responded


def evaluate_time_to_collision(state, ttc_threshold_s=2.5):
    """Returns True if a forward-collision warning should be issued because the
    computed time-to-collision is below `ttc_threshold_s`.
    """
    obj = nearest_object_in_zone(state, ("forward",))
    ttc = time_to_collision(obj)
    return ttc is not None and ttc < ttc_threshold_s

def suppress_alert_if_driver_braking(state, required_decel_input=0.6):
    """Returns True if the FCW alert should be suppressed because the driver is
    already braking at or above the required deceleration input.
    """
    return driver_has_responded(state, required_decel_input)
