"""Mock vehicle/sensor state shared by all ADAS feature modules.

This is a sanitized sample data model only -- it does not represent any
production vehicle bus signal set. Values are simplified for illustration.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DetectedObject:
    """A simplified object detection from camera/radar/ultrasonic fusion."""
    object_id: str
    relative_distance_m: float
    relative_speed_mps: float
    lateral_offset_m: float = 0.0
    confidence: float = 1.0
    zone: Optional[str] = None  # e.g. "blind_spot_left", "forward", "rear"


@dataclass
class VehicleState:
    """Simplified snapshot of vehicle and driver state for one control cycle."""
    speed_kph: float = 0.0
    driver_brake_input: float = 0.0        # 0.0 - 1.0
    driver_steering_override: bool = False
    turn_signal: Optional[str] = None       # "left", "right", None
    hands_on_wheel: bool = True
    hands_off_duration_s: float = 0.0
    lane_marking_confidence: float = 1.0
    ambient_light_lux: float = 10.0
    drowsiness_confirmation_pending_s: float = 0.0
    detected_objects: List[DetectedObject] = field(default_factory=list)
