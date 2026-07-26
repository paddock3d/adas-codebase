"""Driver Drowsiness Detection (DDD) -- ASIL B, priority: Medium.

Monitors driver behavior to estimate drowsiness or inattention and issues escalating alerts.

Sanitized sample module prepared for tooling/process validation. It does
not represent any production vehicle software.
"""
from common.vehicle_state import VehicleState, DetectedObject


def compute_drowsiness_score(steering_variability, eyelid_closure_ratio):
    """Returns a normalized 0.0 - 1.0 drowsiness score combining steering-
    pattern variability and eyelid-closure ratio. This score is intended to
    be passed into TJA's `enforce_hands_on_confirmation` (see that module)
    so a drowsy driver gets a shorter hands-on confirmation window.
    """
    score = 0.5 * min(1.0, steering_variability) + 0.5 * min(1.0, eyelid_closure_ratio)
    return round(min(1.0, max(0.0, score)), 3)

def issue_escalating_alert(drowsiness_score, threshold=0.6):
    """Returns the alert level ("none", "visual", "visual+audio",
    "visual+audio+haptic") based on how far the score exceeds `threshold`.
    """
    if drowsiness_score < threshold:
        return "none"
    if drowsiness_score < threshold + 0.15:
        return "visual"
    if drowsiness_score < threshold + 0.3:
        return "visual+audio"
    return "visual+audio+haptic"
