# Quality Agent Pool (15 agents)

Each agent advocates a distinct, standards-grounded quality concern. When
annotating, decide whether each agent's concern is important enough that a
dedicated agent should participate in requirements negotiation for the system.

| #  | Agent           | Standard  | Sub-focus                                   |
|----|-----------------|-----------|---------------------------------------------|
| 1  | Safety          | ISO 25010 | Hazard prevention, risk mitigation          |
| 2  | Performance     | ISO 25010 | Response time, throughput, capacity         |
| 3  | Efficiency      | ISO 25010 | Resource utilization, energy usage          |
| 4  | Reliability     | ISO 25010 | Fault tolerance, recoverability             |
| 5  | Usability       | ISO 25010 | Learnability, error protection              |
| 6  | Security        | ISO 25010 | Authentication, access control              |
| 7  | Trustworthiness | ISO 25010 | Privacy, data protection, trust             |
| 8  | Maintainability | ISO 25010 | Modularity, testability                     |
| 9  | Compatibility   | ISO 25010 | Interoperability, co-existence              |
| 10 | Flexibility     | ISO 25010 | Adaptability, replaceability                |
| 11 | Func. Safety    | ISO 26262 | ASIL levels, hazard analysis                |
| 12 | Explainability  | EU AI Act | Model transparency, interpretability        |
| 13 | Privacy         | GDPR      | Consent, data subject rights                |
| 14 | Green           | ISO 14001 | Energy efficiency, carbon footprint         |
| 15 | Responsibility  | IEEE 7000 | Ethical accountability, compliance          |

Notes:
- **Trustworthiness** (ISO 25010) is a broad privacy/trust concern; **Privacy**
  (GDPR) is the narrower regulatory data-subject-rights concern. They may both
  apply, one, or neither — judge each independently.
- **Efficiency** (resource/energy use) vs **Green** (sustainability / carbon
  footprint) can overlap; mark each on its own merits.
- **Safety** (general hazard prevention) vs **Func. Safety** (ISO 26262-style
  functional-safety analysis) are distinct.
