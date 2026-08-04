# Ground-Truth Annotation Request — W-Mobility Perception Case

Dear Aisin team,

To evaluate our automated agent-configuration process (ConfigRE) on your
personal-mobility perception trial, we need an **expert ground truth**: from the
15-agent quality pool below, please mark **which quality dimensions are relevant**
(i.e., which specialized agents *should* participate in requirements negotiation
for this system) and give a one-line rationale for each decision.

- Base your judgement only on the project description (see `W-Mobility_input.json`).
- "Relevant" = this quality concern is important enough that a dedicated agent
  should reason about it and negotiate trade-offs for this system.
- There is no fixed number; typical systems need 5–7 relevant dimensions.

## Quality Agent Pool (15 agents)

| # | Agent | Standard | Sub-focus | Relevant? (Y/N) | Rationale |
|---|-------|----------|-----------|-----------------|-----------|
| 1 | Safety          | ISO 25010 | Hazard prevention, risk mitigation | | |
| 2 | Performance     | ISO 25010 | Response time, throughput, capacity | | |
| 3 | Efficiency      | ISO 25010 | Resource utilization, energy usage | | |
| 4 | Reliability     | ISO 25010 | Fault tolerance, recoverability | | |
| 5 | Usability       | ISO 25010 | Learnability, error protection | | |
| 6 | Security        | ISO 25010 | Authentication, access control | | |
| 7 | Trustworthiness | ISO 25010 | Privacy, data protection, trust | | |
| 8 | Maintainability | ISO 25010 | Modularity, testability | | |
| 9 | Compatibility   | ISO 25010 | Interoperability, co-existence | | |
| 10 | Flexibility    | ISO 25010 | Adaptability, replaceability | | |
| 11 | Func. Safety   | ISO 26262 | ASIL levels, hazard analysis | | |
| 12 | Explainability | EU AI Act | Model transparency, interpretability | | |
| 13 | Privacy        | GDPR      | Consent, data subject rights | | |
| 14 | Green          | ISO 14001 | Energy efficiency, carbon footprint | | |
| 15 | Responsibility | IEEE 7000 | Ethical accountability, compliance | | |

## Our tentative suggestion (please confirm or correct)

Based on the description, we would tentatively expect the following to be
**relevant** (this is only a starting point — your expert judgement overrides it):

- **Safety** — pedestrian collision & step-detection fail-safe are the core concern
- **Func. Safety** — Japanese Road Transport Vehicle Act / specified small motorized bicycle safety standards
- **Performance** — 3–4 FPS (250–300 ms) perception latency directly bounds safe stopping
- **Efficiency** — Jetson Orin Nano 8 GB / ~34 W edge compute & power budget
- **Reliability** — perception robustness under night / backlight / motion blur (monocular only)
- **Usability** — safety-vs-usability trade-off (false braking) — *borderline, please judge*

Please return this table filled in (Y/N + rationale). We will encode it into
`w-mobility_ground_truth.json` for the experiment.
