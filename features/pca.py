"""Park Collision Avoidance (PCA) -- ASIL B, priority: Medium.

Detects obstacles during low-speed parking maneuvers using ultrasonic and camera sensors and prevents collisions.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.proximity import warning_intensity
from common.driver_response import driver_has_responded


def detect_parking_obstacle(state, warn_distance_m=1.5):
    """Returns the warning intensity (0.0 - 1.0), scaled by proximity, for the
    nearest obstacle within `warn_distance_m` during a parking maneuver.
    """
    nearby = [o for o in state.detected_objects if o.relative_distance_m <= warn_distance_m]
    if not nearby:
        return 0.0
    closest = min(nearby, key=lambda o: o.relative_distance_m)
    return warning_intensity(closest.relative_distance_m, warn_distance_m)

def trigger_parking_autonomous_braking(state, brake_distance_m=0.3, driver_brake_threshold=0.3):
    """Returns True if autonomous braking should trigger during a parking
    maneuver because an obstacle is within `brake_distance_m` and the driver
    has not reacted.
    """
    closest = min(
        (o.relative_distance_m for o in state.detected_objects), default=None
    )
    return closest is not None and closest <= brake_distance_m and not driver_has_responded(state, driver_brake_threshold)
