# Human Evaluation Rubric: Downstream Requirements Quality

Evaluators assess Phase 5 output (final requirements specification) produced under each configuration strategy. Evaluation is blind: evaluators do not know which configuration produced each output.

## Protocol
- **Evaluators:** 2-3 evaluators with RE or software engineering background
- **Cases Evaluated:** 2-3 selected case studies (recommend: AD, ATM, LoanApproval for domain diversity)
- **Configurations Compared:** ['Fixed-5', 'Full-15', 'Domain-opt', 'Phase0-Auto']
- **Blinding:** Each output is labeled with a random code (e.g., A, B, C, D). Evaluators do not know the configuration strategy.
- **Input Provided:** Original project description + Phase 5 output for each configuration
- **Output Format:** Likert 1-5 score for each dimension + free-text justification

## Scoring Dimensions (Likert 1–5)

### D1. Completeness
Do the generated requirements adequately cover the quality dimensions that are important for this project domain?

- **1** — Missing most domain-critical quality requirements; major gaps in coverage
- **2** — Covers some quality dimensions but misses 2+ important ones for this domain
- **3** — Covers the main quality dimensions but with notable gaps in depth or specificity
- **4** — Covers most domain-relevant quality dimensions with reasonable depth
- **5** — Comprehensive coverage of all domain-relevant quality dimensions with specific, actionable requirements

### D2. Relevance
Are the generated requirements relevant to the project domain, or do they include unnecessary/off-topic quality concerns?

- **1** — Most requirements are irrelevant or generic; significant noise from off-topic quality concerns
- **2** — Many requirements are only marginally relevant; noticeable off-topic content
- **3** — Most requirements are relevant but some unnecessary quality concerns are included
- **4** — Nearly all requirements are relevant to the project domain with minimal noise
- **5** — All requirements are highly relevant and well-targeted to the specific project domain

### D3. Actionability
Are the requirements specific and concrete enough to guide implementation, or are they vague and abstract?

- **1** — Requirements are vague platitudes with no actionable guidance for developers
- **2** — Some requirements are specific but most lack measurable criteria or concrete constraints
- **3** — Mix of specific and vague requirements; some have measurable criteria
- **4** — Most requirements include specific criteria, thresholds, or testable conditions
- **5** — All requirements are specific, measurable, and directly implementable with clear acceptance criteria

### D4. Consistency
Are the requirements internally consistent, or do they contain contradictions between quality dimensions?

- **1** — Multiple direct contradictions between requirements from different quality agents
- **2** — Several inconsistencies or unresolved tensions between quality dimensions
- **3** — Minor inconsistencies present but no direct contradictions; some tensions left unaddressed
- **4** — Generally consistent with explicit acknowledgment and resolution of trade-offs
- **5** — Fully consistent with clear prioritization and documented trade-off resolutions
