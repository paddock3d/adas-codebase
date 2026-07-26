"""Traffic Sign Recognition (TSR) -- ASIL A, priority: Medium.

Recognizes and classifies posted speed-limit signs using the forward-facing camera and displays the detected limit to the driver.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject


def recognize_speed_limit_sign(detected_value_kph, confidence, confidence_threshold=0.7):
    """Returns the recognized speed limit if `confidence` meets
    `confidence_threshold`, otherwise None (no display update).
    """
    return detected_value_kph if confidence >= confidence_threshold else None

def filter_low_confidence_detection(detections, confidence_threshold=0.7):
    """Filters a list of (value, confidence) sign detections, discarding any
    below `confidence_threshold`.
    """
    return [v for v, c in detections if c >= confidence_threshold]
