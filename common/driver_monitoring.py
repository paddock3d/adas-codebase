"""Shared duration/timeout evaluation used by driver-attention features.

LKA (hands-off-wheel) and TJA (hands-on confirmation) both decide whether
an elapsed duration has exceeded an allowed limit using the same
comparison. TJA additionally derates its limit using a drowsiness score
supplied by DDD, so a drowsy driver gets a shorter confirmation window.
Sanitized sample code only.
"""


def duration_exceeded(current_s, limit_s):
    """Return True if `current_s` has exceeded `limit_s`."""
    return current_s > limit_s


def derate_limit(limit_s, drowsiness_score, max_derating=0.5):
    """Scale down a duration limit as drowsiness score rises.

    At `drowsiness_score` 0.0 the limit is unchanged; at 1.0 the limit is
    reduced by `max_derating` (fraction). Used by TJA so a driver flagged
    as drowsy by DDD gets a shorter hands-on confirmation window.
    """
    score = min(1.0, max(0.0, drowsiness_score))
    return limit_s * (1.0 - max_derating * score)
