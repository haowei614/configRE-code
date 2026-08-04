# Requirement Set W-Mobility-B

*Project domain: Personal Mobility Perception (Automotive / Industrial — Aisin)*  
*(You are not told which method produced this set. Rate only what you read.)*

## Specification Outline
- System Scope and Stakeholders
- Quality-Attribute Requirements (Compatibility/Efficiency/Explainability/Flexibility/Functional Safety/Maintainability/Performance/Privacy/Reliability/Responsibility/Safety/Security/Sustainability/Trustworthiness/Usability)
- Negotiation and Conflict Resolution Decisions
- Verification and Compliance Evidence

## Quality-Attribute Requirements

### Compatibility
1. Compatibility objective for W-Mobility: Perception degradation under adverse conditions (night, backlight, motion blur)
2. The system shall ensure compatibility (co-existence, interoperability): Perception degradation under adverse conditions (night, backlight, motion blur)
3. The system shall ensure compatibility (co-existence, interoperability): [Obstacle Categories by Severity]
4. The system shall ensure compatibility (co-existence, interoperability): Staircase / step (highest severity)
5. The system shall ensure compatibility (co-existence, interoperability): [Key Quality Concerns and Constraints]
6. The system shall ensure compatibility (co-existence, interoperability): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode
7. The system shall ensure compatibility (co-existence, interoperability): Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which directly bounds achievable detec...

### Efficiency
1. Efficiency objective for W-Mobility: 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1
2. The system shall ensure efficiency (latency optimization): 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1
3. The system shall ensure efficiency (throughput stability): Braking is actuated over a CAN-based brake control interface
4. The system shall ensure efficiency (resource utilization): A commercial reference model exists (W-Mobility)
5. The system shall ensure efficiency (latency optimization): [AI Perception Subsystem]
6. The system shall ensure efficiency (throughput stability): - Sensor: single monocular RGB camera (no stereo, no LiDAR)
7. The system shall ensure efficiency (resource utilization): - Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment

### Explainability
1. Explainability objective for W-Mobility: Reliability of perception under environmental degradation (night, backlight, motion blur) using only a monocular camera
2. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Reliability of perception under environment...
3. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): [Expected Derived Safety Requirements (quan...
4. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): The RE process is expected to yield actiona...
5. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): [Conflict Scenario for Negotiation]
6. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): - The SafetyAgent prioritizes never missing...
7. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): - The PerformanceAgent and EfficiencyAgent...

### Flexibility
1. Flexibility objective for W-Mobility: Staircase / step (highest severity)
2. The system shall ensure flexibility (adaptability, installability, replaceability): Staircase / step (highest severity)
3. The system shall ensure flexibility (adaptability, installability, replaceability): [Key Quality Concerns and Constraints]
4. The system shall ensure flexibility (adaptability, installability, replaceability): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode
5. The system shall ensure flexibility (adaptability, installability, replaceability): Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which directly bounds achi...
6. The system shall ensure flexibility (adaptability, installability, replaceability): Computational and power constraints of the Jetson Orin Nano (8 GB, ~34 W) at the edge
7. The system shall ensure flexibility (adaptability, installability, replaceability): Fail-safe behavior for step/staircase detection: a missed detection is safety-critical and mu...

### Functional Safety
1. Functional Safety objective for W-Mobility: Fail-safe behavior for step/staircase detection: a missed detection is safety-critical and must trigger a safe stop
2. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Fail-safe behavior for step/staircase detection: a mi...
3. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Trade-off between safety and usability: overly conser...
4. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): Reliability of perception under environmental degrada...
5. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): [Expected Derived Safety Requirements (quantitative)]
6. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): The RE process is expected to yield actionable, verif...
7. The system shall ensure functional safety (hazard analysis, safety mechanisms, ASIL levels, fault tolerance per ISO 26262): [Conflict Scenario for Negotiation]

### Maintainability
1. Maintainability objective for W-Mobility: Pedestrian collision avoidance in mixed-traffic pedestrian zones
2. The system shall ensure maintainability (modularity, reusability, analysability, modifiability, testability): Pedestrian collision avoidance in mixed-traffic pedestrian zones
3. The system shall ensure maintainability (modularity, reusability, analysability, modifiability, testability): Staircase/step detection to prevent fall/tip-over (highest severity...
4. The system shall ensure maintainability (modularity, reusability, analysability, modifiability, testability): Perception degradation under adverse conditions (night, backlight,...
5. The system shall ensure maintainability (modularity, reusability, analysability, modifiability, testability): [Obstacle Categories by Severity]
6. The system shall ensure maintainability (modularity, reusability, analysability, modifiability, testability): Staircase / step (highest severity)
7. The system shall ensure maintainability (modularity, reusability, analysability, modifiability, testability): [Key Quality Concerns and Constraints]

### Performance
1. Performance objective for W-Mobility: A commercial reference model exists (W-Mobility)
2. The system shall ensure performance (time behaviour, resource utilisation, capacity): A commercial reference model exists (W-Mobility)
3. The system shall ensure performance (time behaviour, resource utilisation, capacity): [AI Perception Subsystem]
4. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Sensor: single monocular RGB camera (no stereo, no LiDAR)
5. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment
6. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
7. The system shall ensure performance (time behaviour, resource utilisation, capacity): - Power envelope: approximately 34 W

### Privacy
1. Privacy objective for W-Mobility: The RE process is expected to yield actionable, verifiable safety requirements such as: required stopping distance per mode, minimum obstacle detect...
2. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): The RE process is expected to yield actionable, verifiable s...
3. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): [Conflict Scenario for Negotiation]
4. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): - The SafetyAgent prioritizes never missing a step/staircase...
5. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): - The PerformanceAgent and EfficiencyAgent are bounded by th...
6. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): - Potential Conflict: the detection range and low false-nega...
7. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Project: AI-Based Perception System for a Personal Mobility...

### Reliability
1. Reliability objective for W-Mobility: - Sensor: single monocular RGB camera (no stereo, no LiDAR)
2. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): - Sensor: single monocular RGB camera (no stereo, no LiDAR)
3. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): - Compute device: NVIDIA Jetson Orin Nano (8 GB), edge deployment
4. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
5. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): - Power envelope: approximately 34 W
6. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): The system must comply with the Japanese Road Transport Vehicle Act safety standar...
7. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced i...

### Responsibility
1. Responsibility objective for W-Mobility: - Potential Conflict: the detection range and low false-negative rate demanded by Safety may be infeasible within the latency and compute/pow...
2. The system shall ensure responsibility (regulatory accountability): - Potential Conflict: the detection range and low false-negative rate demanded by Safety may be infeasible wi...
3. The system shall ensure responsibility (stakeholder transparency): Project: AI-Based Perception System for a Personal Mobility Vehicle (Aisin Industrial Trial)
4. The system shall ensure responsibility (ethical compliance): The target system is an AI-based perception subsystem deployed on a personal mobility vehicle (equivalent to a Japan...
5. The system shall ensure responsibility (regulatory accountability): It is operated on the Waseda University campus in a pedestrian-mixed environment
6. The system shall ensure responsibility (stakeholder transparency): The vehicle has a maximum speed of 20 km/h and two operating modes: a 20 km/h road mode (expected stopping dis...
7. The system shall ensure responsibility (ethical compliance): 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1

### Safety
1. Safety objective for W-Mobility: It is operated on the Waseda University campus in a pedestrian-mixed environment
2. The system shall ensure safety (hazard prevention): It is operated on the Waseda University campus in a pedestrian-mixed environment
3. The system shall ensure safety (fault tolerance): The vehicle has a maximum speed of 20 km/h and two operating modes: a 20 km/h road mode (expected stopping distance ~8
4. The system shall ensure safety (risk mitigation): 2 m) and a 6 km/h pedestrian-zone mode (expected stopping distance ~1
5. The system shall ensure safety (hazard prevention): Braking is actuated over a CAN-based brake control interface
6. The system shall ensure safety (fault tolerance): A commercial reference model exists (W-Mobility)
7. The system shall ensure safety (risk mitigation): [AI Perception Subsystem]

### Security
1. Security objective for W-Mobility: Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced in pedestrian zones
2. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Pedestrian priority is a legal requirement, and the 6 km/h mode must be enforced...
3. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): [Critical Scenarios]
4. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Pedestrian collision avoidance in mixed-traffic pedestrian zones
5. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Staircase/step detection to prevent fall/tip-over (highest severity; must not be...
6. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Perception degradation under adverse conditions (night, backlight, motion blur)
7. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): [Obstacle Categories by Severity]

### Sustainability
1. Sustainability objective for W-Mobility: - The SafetyAgent prioritizes never missing a step/staircase or pedestrian, favoring long detection range and conservative braking (low false...
2. The system shall ensure sustainability (energy footprint reduction): - The SafetyAgent prioritizes never missing a step/staircase or pedestrian, favoring long detection range an...
3. The system shall ensure sustainability (resource lifecycle control): - The PerformanceAgent and EfficiencyAgent are bounded by the 3-4 FPS cycle and the ~34 W / 8 GB edge budget...
4. The system shall ensure sustainability (environmental impact awareness): - Potential Conflict: the detection range and low false-negative rate demanded by Safety may be infeasib...
5. The system shall ensure sustainability (energy footprint reduction): Project: AI-Based Perception System for a Personal Mobility Vehicle (Aisin Industrial Trial)
6. The system shall ensure sustainability (resource lifecycle control): The target system is an AI-based perception subsystem deployed on a personal mobility vehicle (equivalent to...
7. The system shall ensure sustainability (environmental impact awareness): It is operated on the Waseda University campus in a pedestrian-mixed environment

### Trustworthiness
1. Trustworthiness objective for W-Mobility: Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode
2. The system shall ensure trustworthiness (security assurance): Pedestrian priority (legal) and correct enforcement of the 6 km/h pedestrian-zone mode
3. The system shall ensure trustworthiness (auditability): Perception latency: at 3-4 FPS the perception cycle is 250-300 ms, which directly bounds achievable detection range and s...
4. The system shall ensure trustworthiness (integrity guarantees): Computational and power constraints of the Jetson Orin Nano (8 GB, ~34 W) at the edge
5. The system shall ensure trustworthiness (security assurance): Fail-safe behavior for step/staircase detection: a missed detection is safety-critical and must trigger a safe stop
6. The system shall ensure trustworthiness (auditability): Trade-off between safety and usability: overly conservative detection causes false braking, degrading ride usability, whi...
7. The system shall ensure trustworthiness (integrity guarantees): Reliability of perception under environmental degradation (night, backlight, motion blur) using only a monocular...

### Usability
1. Usability objective for W-Mobility: - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
2. The system shall ensure usability (learnability, operability, user error protection, accessibility): - Real-time processing budget: 3-4 FPS (~250-300 ms perception cycle)
3. The system shall ensure usability (learnability, operability, user error protection, accessibility): - Power envelope: approximately 34 W
4. The system shall ensure usability (learnability, operability, user error protection, accessibility): The system must comply with the Japanese Road Transport Vehicle Act safety s...
5. The system shall ensure usability (learnability, operability, user error protection, accessibility): Pedestrian priority is a legal requirement, and the 6 km/h mode must be enfo...
6. The system shall ensure usability (learnability, operability, user error protection, accessibility): [Critical Scenarios]
7. The system shall ensure usability (learnability, operability, user error protection, accessibility): Pedestrian collision avoidance in mixed-traffic pedestrian zones

## Implementation Checklist
- Preserve canonical phase artifact compatibility
- Enforce strict provenance and taint controls
- Trace each integrated requirement to a verification signal
