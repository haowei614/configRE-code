# Requirement Set W-Mobility-A

*Project domain: Personal Mobility Perception (Automotive / Industrial — Aisin)*  
*(You are not told which method produced this set. Rate only what you read.)*

## Specification Outline
- System Scope and Stakeholders
- Quality-Attribute Requirements (Efficiency/Functional Safety/Performance/Reliability/Safety/Usability)
- Negotiation and Conflict Resolution Decisions
- Verification and Compliance Evidence

## Quality-Attribute Requirements

### Efficiency
1. Efficiency objective for W-Mobility: [AI Perception Subsystem]
2. The system shall ensure efficiency (latency optimization): [AI Perception Subsystem]
3. The system shall ensure efficiency (throughput stability): - Sensor: single monocular RGB camera (no stereo, no LiDAR)
4. The system shall ensure efficiency (resource utilization): - Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment
5. The system shall ensure efficiency (latency optimization): - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
6. The system shall ensure efficiency (throughput stability): - Power envelope: approximately 34 W
7. The system shall ensure efficiency (resource utilization): The system must comply with the Japanese Road Transport Vehicle Act safety standards and the regulations governing Spe...

### Functional Safety
1. Functional Safety objective for W-Mobility: Fail-safe behavior for step/staircase detection: a missed detection is safety-critical and must trigger a safe stop
2. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Fail-safe behavior for step/staircase detection: a mi...
3. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Trade-off between safety and usability: overly conser...
4. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Reliability of perception under environmental degrada...
5. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): [Expected Derived Safety Requirements (quantitative)]
6. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): The RE process is expected to yield actionable, verif...
7. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): [Conflict Scenario for Negotiation]

### Performance
1. Performance objective for W-Mobility: Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced in pedestrian zones
2. The system shall ensure performance (time behaviour, resource utilisation, capacity): Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced in pedestr...
3. The system shall ensure performance (time behaviour, resource utilisation, capacity): [Critical Scenarios]
4. The system shall ensure performance (time behaviour, resource utilisation, capacity): Pedestrian collision avoidance in mixed-traffic pedestrian zones
5. The system shall ensure performance (time behaviour, resource utilisation, capacity): Staircase/step detection to prevent fall/tip-over (highest severity; must not be missed)
6. The system shall ensure performance (time behaviour, resource utilisation, capacity): Perception degradation under adverse conditions (night, backlight, motion blur)
7. The system shall ensure performance (time behaviour, resource utilisation, capacity): [Obstacle Categories by Severity]

### Reliability
1. Reliability objective for W-Mobility: [Obstacle Categories by Severity]
2. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): [Obstacle Categories by Severity]
3. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Staircase / step (highest severity)
4. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): [Key Quality Concerns and Constraints]
5. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone...
6. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which directly...
7. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Computational and power constraints of the Jetson Orin Nano (8 GB, ~34 W) at the edge

### Safety
1. Safety objective for W-Mobility: It is operated on the Waseda University campus in a pedestrian-mixed environment
2. The system shall ensure safety (hazard prevention): It is operated on the Waseda University campus in a pedestrian-mixed environment
3. The system shall ensure safety (fault tolerance): The vehicle has a maximum speed of 20 km/h and two operating modes: a 20 km/h road mode (expected stopping distance ~8
4. The system shall ensure safety (risk mitigation): 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1
5. The system shall ensure safety (hazard prevention): Braking is actuated over a CAN-based brake control interface
6. The system shall ensure safety (fault tolerance): A commercial reference model exists (W-Mobility)
7. The system shall ensure safety (risk mitigation): [AI Perception Subsystem]

### Usability
1. Usability objective for W-Mobility: [Conflict Scenario for Negotiation]
2. The system shall ensure usability (learnability, operability, user error protection, accessibility): [Conflict Scenario for Negotiation]
3. The system shall ensure usability (learnability, operability, user error protection, accessibility): - The SafetyAgent prioritizes never missing a step/staircase or pedestrian,...
4. The system shall ensure usability (learnability, operability, user error protection, accessibility): - The PerformanceAgent and EfficiencyAgent are bounded by the 3-4 FPS cycle...
5. The system shall ensure usability (learnability, operability, user error protection, accessibility): - Potential Conflict: the detection range and low false-negative rate demand...
6. The system shall ensure usability (learnability, operability, user error protection, accessibility): Project: AI-Based Perception System for a Personal Mobility Vehicle (Aisin I...
7. The system shall ensure usability (learnability, operability, user error protection, accessibility): The target system is an AI-based perception subsystem deployed on a personal...

## Implementation Checklist
- Preserve canonical phase artifact compatibility
- Enforce strict provenance and taint controls
- Trace each integrated requirement to a verification signal
