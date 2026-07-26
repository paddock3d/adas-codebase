# ADAS Sample Codebase (Sanitized)

This is a **sanitized sample codebase** prepared for tooling/process
validation. It does not represent any production vehicle software and
should not be used as a reference ADAS implementation.

## Layout

- `common/vehicle_state.py` -- shared mock vehicle/sensor state model.
- `common/perception.py` -- shared object-zone lookup and time-to-collision
  math, used by ACC, AEB, FCW, BSM, RCTA, AHC.
- `common/driver_response.py` -- shared "has the driver responded"
  evaluation, used by AEB, FCW, RCTA, PCA.
- `common/proximity.py` -- shared distance-to-warning-intensity scaling,
  used by PCA, SVM.
- `common/driver_monitoring.py` -- shared duration/timeout evaluation, used
  by LKA and TJA (TJA's limit is additionally derated using a drowsiness
  score fed from DDD).
- `common/lane_sensing.py` -- shared lane-boundary-crossing definition,
  used by LDW and LKA.
- `features/<feature>.py` -- one module per ADAS feature. Each function
  implements one piece of feature behavior (see module/function docstrings).
  `features/tja.py` additionally imports and calls directly into
  `features/acc.py` and `features/lka.py` for its combined-control logic.

Several features share common helper modules or call directly into one
another. A change to a shared module or to a directly-called function can
affect more than one feature's behavior -- see the accompanying
Feature Interconnection Map for the full picture of which features are
coupled to which, and why.

## Features included

- **ACC** -- Adaptive Cruise Control (ASIL C, High priority)
- **AEB** -- Autonomous Emergency Braking (ASIL D, Critical priority)
- **FCW** -- Forward Collision Warning (ASIL C, High priority)
- **LDW** -- Lane Departure Warning (ASIL C, High priority)
- **LKA** -- Lane Keep Assist (ASIL C, High priority)
- **BSM** -- Blind Spot Monitoring (ASIL B, Medium priority)
- **RCTA** -- Rear Cross Traffic Alert (ASIL B, Medium priority)
- **PCA** -- Park Collision Avoidance (ASIL B, Medium priority)
- **TSR** -- Traffic Sign Recognition (ASIL A, Medium priority)
- **DDD** -- Driver Drowsiness Detection (ASIL B, Medium priority)
- **AHC** -- Adaptive Headlight Control (ASIL A, Low priority)
- **SVM** -- Surround View Monitor (ASIL A, Low priority)
- **TJA** -- Traffic Jam Assist (ASIL D, Critical priority)
