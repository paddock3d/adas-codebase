"""Blind Spot Monitoring (BSM) -- ASIL B, priority: Medium.

Monitors the vehicle's blind-spot zones and warns the driver of vehicles present in those zones.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject
from common.perception import objects_in_zones


def detect_object_in_blind_spot(state, zone):
    """Returns True if any detected object occupies the given blind-spot
    `zone` (e.g. "blind_spot_left"/"blind_spot_right").
    """
    return bool(objects_in_zones(state, (zone,)))

def escalate_on_turn_signal(state):
    """Returns True if the blind-spot warning should escalate to audible
    because the driver signaled toward an occupied blind-spot zone.
    """
    zone = f"blind_spot_{state.turn_signal}" if state.turn_signal else None
    return zone is not None and detect_object_in_blind_spot(state, zone)
