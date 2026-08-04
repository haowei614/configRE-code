# Requirement Set W-Mobility-C

*Project domain: Personal Mobility Perception (Automotive / Industrial — Aisin)*  
*(You are not told which method produced this set. Rate only what you read.)*

## Specification Outline
- System Scope and Stakeholders
- Quality-Attribute Requirements (Efficiency/Responsibility/Safety/Sustainability/Trustworthiness)
- Negotiation and Conflict Resolution Decisions
- Verification and Compliance Evidence

## Quality-Attribute Requirements

### Efficiency
1. Efficiency objective for W-Mobility: - Sensor: single monocular RGB camera (no stereo, no LiDAR)
2. The system shall ensure efficiency (latency optimization): - Sensor: single monocular RGB camera (no stereo, no LiDAR)
3. The system shall ensure efficiency (throughput stability): - Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment
4. The system shall ensure efficiency (resource utilization): - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
5. The system shall ensure efficiency (latency optimization): - Power envelope: approximately 34 W
6. The system shall ensure efficiency (throughput stability): The system must comply with the Japanese Road Transport Vehicle Act safety standards and the regulations governing Spe...
7. The system shall ensure efficiency (resource utilization): Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced in pedestrian zones

### Responsibility
1. Responsibility objective for W-Mobility: The RE process is expected to yield actionable, verifiable safety requirements such as: required stopping distance per mode, minimum obstacle...
2. The system shall ensure responsibility (regulatory accountability): The RE process is expected to yield actionable, verifiable safety requirements such as: required stopping dis...
3. The system shall ensure responsibility (stakeholder transparency): [Conflict Scenario for Negotiation]
4. The system shall ensure responsibility (ethical compliance): - The SafetyAgent prioritizes never missing a step/staircase or pedestrian, favoring long detection range and conser...
5. The system shall ensure responsibility (regulatory accountability): - The PerformanceAgent and EfficiencyAgent are bounded by the 3-4 FPS cycle and the ~34 W / 8 GB edge budget,...
6. The system shall ensure responsibility (stakeholder transparency): - Potential Conflict: the detection range and low false-negative rate demanded by Safety may be infeasible wit...
7. The system shall ensure responsibility (ethical compliance): Project: AI-Based Perception System for a Personal Mobility Vehicle (Aisin Industrial Trial)
8. The system shall ensure responsibility (regulatory accountability): The target system is an AI-based perception subsystem deployed on a personal mobility vehicle (equivalent to...

### Safety
1. Safety objective for W-Mobility: It is operated on the Waseda University campus in a pedestrian-mixed environment
2. The system shall ensure safety (hazard prevention): It is operated on the Waseda University campus in a pedestrian-mixed environment
3. The system shall ensure safety (fault tolerance): The vehicle has a maximum speed of 20 km/h and two operating modes: a 20 km/h road mode (expected stopping distance ~8
4. The system shall ensure safety (risk mitigation): 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1
5. The system shall ensure safety (hazard prevention): Braking is actuated over a CAN-based brake control interface
6. The system shall ensure safety (fault tolerance): A commercial reference model exists (W-Mobility)
7. The system shall ensure safety (risk mitigation): [AI Perception Subsystem]
8. The system shall ensure safety (hazard prevention): - Sensor: single monocular RGB camera (no stereo, no LiDAR)

### Sustainability
1. Sustainability objective for W-Mobility: Pedestrian collision avoidance in mixed-traffic pedestrian zones
2. The system shall ensure sustainability (energy footprint reduction): Pedestrian collision avoidance in mixed-traffic pedestrian zones
3. The system shall ensure sustainability (resource lifecycle control): Staircase/step detection to prevent fall/tip-over (highest severity; must not be missed)
4. The system shall ensure sustainability (environmental impact awareness): Perception degradation under adverse conditions (night, backlight, motion blur)
5. The system shall ensure sustainability (energy footprint reduction): [Obstacle Categories by Severity]
6. The system shall ensure sustainability (resource lifecycle control): Staircase / step (highest severity)

### Trustworthiness
1. Trustworthiness objective for W-Mobility: Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode
2. The system shall ensure trustworthiness (security assurance): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode
3. The system shall ensure trustworthiness (auditability): Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which directly bounds achievable detection range and s...
4. The system shall ensure trustworthiness (integrity guarantees): Computational and power constraints of the Jetson Orin Nano (8 GB, ~34 W) at the edge
5. The system shall ensure trustworthiness (security assurance): Fail-safe behavior for step/staircase detection: a missed detection is safety-critical and must trigger a safe stop
6. The system shall ensure trustworthiness (auditability): Trade-off between safety and usability: overly conservative detection causes false braking, degrading ride usability, whi...

## Implementation Checklist
- Preserve canonical phase artifact compatibility
- Enforce strict provenance and taint controls
- Trace each integrated requirement to a verification signal
