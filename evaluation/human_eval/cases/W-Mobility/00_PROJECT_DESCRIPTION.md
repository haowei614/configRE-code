# Project Description — Personal Mobility Perception (Automotive / Industrial — Aisin)

**Case:** W-Mobility

AI-Based Perception System for a Personal Mobility Platform (Aisin industrial trial; low-speed pedestrian-mixed environment, edge deployment)

## Requirement Brief

```
Project: AI-Based Perception System for a Personal Mobility Vehicle (Aisin Industrial Trial)

[System Context]
The target system is an AI-based perception subsystem deployed on a personal mobility vehicle (equivalent to a Japanese "specified small motorized bicycle"), dimensions 1570x680x1680 mm, with 1 front and 2 rear wheels. It is operated on the Waseda University campus in a pedestrian-mixed environment. The vehicle has a maximum speed of 20 km/h and two operating modes: a 20 km/h road mode (expected stopping distance ~8.2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1.4 m). Braking is actuated over a CAN-based brake control interface. A commercial reference model exists (W-Mobility).

[AI Perception Subsystem]
- Sensor: single monocular RGB camera (no stereo, no LiDAR).
- Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment.
- Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle).
- Power envelope: approximately 34 W.

[Regulatory Scope]
The system must comply with the Japanese Road Transport Vehicle Act safety standards and the regulations governing Specified Small Motorized Bicycles (as published by the Tokyo Metropolitan Police Department). Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced in pedestrian zones.

[Critical Scenarios]
1. Pedestrian collision avoidance in mixed-traffic pedestrian zones.
2. Staircase/step detection to prevent fall/tip-over (highest severity; must not be missed).
3. Perception degradation under adverse conditions (night, backlight, motion blur).

[Obstacle Categories by Severity]
1. Staircase / step (highest severity).
2. Pedestrians.
3. Bicycles.
4. Other obstacles.

[Key Quality Concerns and Constraints]
1. Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode.
2. Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which directly bounds achievable detection range and safe stopping behavior.
3. Computational and power constraints of the Jetson Orin Nano (8 GB, ~34 W) at the edge.
4. Fail-safe behavior for step/staircase detection: a missed detection is safety-critical and must trigger a safe stop.
5. Trade-off between safety and usability: overly conservative detection causes false braking, degrading ride usability, while under-detection risks collision or fall.
6. Reliability of perception under environmental degradation (night, backlight, motion blur) using only a monocular camera.

[Expected Derived Safety Requirements (quantitative)]
The RE process is expected to yield actionable, verifiable safety requirements such as: required stopping distance per mode, minimum obstacle detection range, maximum end-to-end perception-to-brake response time, and bounds on false-positive / false-negative detection rates for the prioritized obstacle categories.

[Conflict Scenario for Negotiation]
- The SafetyAgent prioritizes never missing a step/staircase or pedestrian, favoring long detection range and conservative braking (low false-negative rate).
- The PerformanceAgent and EfficiencyAgent are bounded by the 3-4 FPS cycle and the ~34 W / 8 GB edge budget, favoring lighter models and lower latency.
- Potential Conflict: the detection range and low false-negative rate demanded by Safety may be infeasible within the latency and compute/power budget enforced by Performance/Efficiency, requiring negotiation over model complexity, perception frame rate, and mode-dependent speed limits.
```
