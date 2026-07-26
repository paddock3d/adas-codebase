"""Rear Cross Traffic Alert (RCTA) -- ASIL B, priority: Medium.

Detects approaching cross traffic while the vehicle is reversing and warns the driver, with autonomous braking as a backstop.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.perception import objects_in_zones, time_to_collision
from common.driver_response import driver_has_responded


def detect_approaching_cross_traffic(state, ttc_threshold_s=3.0):
    """Returns True if cross traffic approaching the rear zone is within
    `ttc_threshold_s`.
    """
    for obj in objects_in_zones(state, ("rear_cross",)):
        ttc = time_to_collision(obj)
        if ttc is not None and ttc < ttc_threshold_s:
            return True
    return False

def trigger_reverse_autonomous_braking(state, ttc_threshold_s=0.8, driver_brake_threshold=0.5):
    """Returns True if autonomous braking should trigger while reversing
    because a collision with cross traffic is imminent and the driver has
    not responded.
    """
    for obj in objects_in_zones(state, ("rear_cross",)):
        ttc = time_to_collision(obj)
        if ttc is not None and ttc <= ttc_threshold_s and not driver_has_responded(state, driver_brake_threshold):
            return True
    return False
