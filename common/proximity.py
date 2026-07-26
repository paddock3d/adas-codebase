"""Shared proximity-warning scaling used by close-range features.

PCA (parking) and SVM (surround-view overlays) both need to turn a raw
distance into a 0.0 - 1.0 "how close is too close" warning intensity, and
both use the same curve so their warning behavior stays consistent.
Sanitized sample code only.
"""


def warning_intensity(distance_m, warn_distance_m):
    """Return proximity-scaled warning intensity in [0.0, 1.0]."""
    if warn_distance_m <= 0:
        return 0.0
    return max(0.0, 1.0 - (distance_m / warn_distance_m))
