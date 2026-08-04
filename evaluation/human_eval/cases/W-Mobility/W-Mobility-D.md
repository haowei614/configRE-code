# Requirement Set W-Mobility-D

*Project domain: Personal Mobility Perception (Automotive / Industrial — Aisin)*  
*(You are not told which method produced this set. Rate only what you read.)*

## Specification Outline
- System Scope and Stakeholders
- Quality-Attribute Requirements (Efficiency/Functional Safety/Performance/Privacy/Reliability/Safety/Usability)
- Negotiation and Conflict Resolution Decisions
- Verification and Compliance Evidence

## Quality-Attribute Requirements

### Efficiency
1. Efficiency objective for W-Mobility: - Power envelope: approximately 34 W
2. The system shall ensure efficiency (latency optimization): - Power envelope: approximately 34 W
3. The system shall ensure efficiency (throughput stability): The system must comply with the Japanese Road Transport Vehicle Act safety standards and the regulations governing Spe...
4. The system shall ensure efficiency (resource utilization): Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced in pedestrian zones
5. The system shall ensure efficiency (latency optimization): [Critical Scenarios]
6. The system shall ensure efficiency (throughput stability): Pedestrian collision avoidance in mixed-traffic pedestrian zones
7. The system shall ensure efficiency (resource utilization): Staircase/step detection to prevent fall/tip-over (highest severity; must not be missed)

### Functional Safety
1. Functional Safety objective for W-Mobility: Trade-off between safety and usability: overly conservative detection causes false braking, degrading ride usability, while under-detectio...
2. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Trade-off between safety and usability: overly conser...
3. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Reliability of perception under environmental degrada...
4. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): [Expected Derived Safety Requirements (quantitative)]
5. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): The RE process is expected to yield actionable, verif...
6. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): [Conflict Scenario for Negotiation]
7. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): - The SafetyAgent prioritizes never missing a step/st...

### Performance
1. Performance objective for W-Mobility: A commercial reference model exists (W-Mobility)
2. The system shall ensure performance (time behaviour, resource utilisation, capacity): A commercial reference model exists (W-Mobility)
3. The system shall ensure performance (time behaviour, resource utilisation, capacity): [AI Perception Subsystem]
4. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Sensor: single monocular RGB camera (no stereo, no LiDAR)
5. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment
6. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
7. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Power envelope: approximately 34 W

### Privacy
1. Privacy objective for W-Mobility: - The SafetyAgent prioritizes never missing a step/staircase or pedestrian, favoring long detection range and conservative braking (low false-negati...
2. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): - The SafetyAgent prioritizes never missing a step/staircase...
3. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): - The PerformanceAgent and EfficiencyAgent are bounded by th...
4. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): - Potential Conflict: the detection range and low false-nega...
5. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Project: AI-Based Perception System for a Personal Mobility...
6. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): The target system is an AI-based perception subsystem deploy...
7. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): It is operated on the Waseda University campus in a pedestri...

### Reliability
1. Reliability objective for W-Mobility: Staircase/step detection to prevent fall/tip-over (highest severity; must not be missed)
2. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Staircase/step detection to prevent fall/tip-over (highest severity; must not be m...
3. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Perception degradation under adverse conditions (night, backlight, motion blur)
4. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): [Obstacle Categories by Severity]
5. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Staircase / step (highest severity)
6. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): [Key Quality Concerns and Constraints]
7. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone...

### Safety
1. Safety objective for W-Mobility: It is operated on the Waseda University campus in a pedestrian-mixed environment
2. The system shall ensure safety (hazard prevention): It is operated on the Waseda University campus in a pedestrian-mixed environment
3. The system shall ensure safety (fault tolerance): The vehicle has a maximum speed of 20 km/h and two operating modes: a 20 km/h road mode (expected stopping distance ~8
4. The system shall ensure safety (risk mitigation): 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1
5. The system shall ensure safety (hazard prevention): Braking is actuated over a CAN-based brake control interface
6. The system shall ensure safety (fault tolerance): A commercial reference model exists (W-Mobility)
7. The system shall ensure safety (risk mitigation): [AI Perception Subsystem]

### Usability
1. Usability objective for W-Mobility: [Key Quality Concerns and Constraints]
2. The system shall ensure usability (learnability, operability, user error protection, accessibility): [Key Quality Concerns and Constraints]
3. The system shall ensure usability (learnability, operability, user error protection, accessibility): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian...
4. The system shall ensure usability (learnability, operability, user error protection, accessibility): Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which dir...
5. The system shall ensure usability (learnability, operability, user error protection, accessibility): Computational and power constraints of the Jetson Orin Nano (8 GB, ~34 W) at...
6. The system shall ensure usability (learnability, operability, user error protection, accessibility): Fail-safe behavior for step/staircase detection: a missed detection is safet...
7. The system shall ensure usability (learnability, operability, user error protection, accessibility): Trade-off between safety and usability: overly conservative detection causes...

## Implementation Checklist
- Preserve canonical phase artifact compatibility
- Enforce strict provenance and taint controls
- Trace each integrated requirement to a verification signal
