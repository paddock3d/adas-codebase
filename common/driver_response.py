"""Shared driver-response evaluation used by warning/braking features.

Centralizes the definition of "the driver has already responded"
so AEB, FCW, RCTA, and PCA agree on what counts as sufficient driver
input before an autonomous intervention (or its warning) is suppressed.
Sanitized sample code only.
"""


def driver_has_responded(state, brake_threshold, allow_steering_override=False):
    """Return True if the driver's own input meets the response threshold.

    `allow_steering_override` additionally treats an active steering
    override as a sufficient response (used by AEB only).
    """
    responded = state.driver_brake_input >= brake_threshold
    if allow_steering_override:
        responded = responded or state.driver_steering_override
    return responded
