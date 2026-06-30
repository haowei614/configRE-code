# Prompt Templates Used in Phase 0

This document discloses all prompt templates used in the three-tier agent selection mechanism (Phase 0). All prompts are reproduced verbatim from `src/openre_bench/pipeline/phase0.py`.

## Tier 1: LLM-Based Relevance Scoring

**Purpose**: Evaluate the relevance of each ISO/IEC 25010 quality characteristic to a given project description.

**Parameters**: `temperature=0.0`, `max_tokens=250`, `seed=0`

**Prompt template** (one call per agent, 10 agents total):

```
You are a senior requirements engineer assessing quality attribute relevance
for a specific project.
Project Description:
{project_description}
Quality Characteristic: {characteristic_name}
Sub-characteristics: {lens_phrase}
Assess whether this quality characteristic is a PRIMARY concern for this
specific project -- not whether it is "nice to have" or "generally relevant
to software engineering."
Scoring criteria:

1.0 = This is a critical, non-negotiable quality concern explicitly demanded
by the project
0.8 = This is a major concern strongly implied by the project domain and
constraints
0.5 = This is a secondary concern that may matter but is not a primary driver
0.3 = This has minor or indirect relevance to this specific project
0.0 = This is irrelevant to this project

Domain-specific guidance:

Safety is about preventing PHYSICAL harm to humans or the environment.
Software that handles financial data, manages records, or processes
transactions is NOT safety-critical even if data accuracy is important.
Data accuracy is Reliability, not Safety.
Performance is about response time, throughput, and resource utilization
under load. Standard CRUD applications with moderate user counts are not
performance-critical.

Important: Most quality characteristics will score 0.3 or below for any given
project. A typical project has 4-6 primary quality concerns, not 8-10. Be
selective.
Respond in JSON only, no markdown, no explanation outside JSON:
{"relevance_score": <float>, "reasoning": "<one sentence explaining why this
is or is not a primary concern>"}
```

**System message**: `"You return strict JSON only for OpenRE-Bench preprocessing."`

### Quality Characteristic Sub-characteristics (lens phrases)

| Characteristic | Sub-characteristics |
|---|---|
| Safety | hazard prevention, fault tolerance, risk mitigation |
| Efficiency | latency optimization, throughput stability, resource utilization |
| Performance | time behaviour, resource utilisation, capacity |
| Reliability | maturity, availability, fault tolerance, recoverability |
| Usability | learnability, operability, user error protection, accessibility |
| Security | confidentiality, integrity, non-repudiation, authentication |
| Trustworthiness | security assurance, auditability, integrity guarantees |
| Maintainability | modularity, reusability, analysability, modifiability, testability |
| Compatibility | co-existence, interoperability |
| Flexibility | adaptability, installability, replaceability |

---

## Tier 2: Domain-Regulatory Mapping

**Purpose**: Identify the project's primary application domain and activate corresponding regulatory-mandatory agents.

**Parameters**: `temperature=0.0`, `max_tokens=250`, `seed=1`

**Prompt template** (one call per project):

```
Identify the PRIMARY application domain of the following project. Select only
domains that directly determine which regulatory standards and safety
certifications apply to this system.
Project Description:
{project_description}
Available domains (select only those with direct regulatory implications for this
project):

automotive: Vehicle systems subject to ISO 26262 functional safety
medical: Medical devices subject to IEC 62304
financial: Financial systems subject to data protection regulations
AI/ML: AI systems subject to EU AI Act transparency requirements (only if AI
decision-making is the primary product, not if AI is merely used as an
implementation technique)
IoT/embedded: IoT devices with specific connectivity/resource constraints
web/enterprise: Enterprise software systems
government: Government systems with specific compliance requirements
telecommunications: Telecom systems with specific regulations

Important: An autonomous vehicle that uses AI internally is "automotive", not
"AI/ML". A medical device that connects to the internet is "medical", not
"IoT/embedded". Select the domain that determines the primary regulatory
framework.
Respond in JSON only:
{"domains": ["<primary_domain>"], "reasoning": "<one sentence>"}
```

### Domain → Agent Mapping (deterministic)

| Domain | Activated Agents |
|---|---|
| automotive | FunctionalSafetyAgent |
| medical | FunctionalSafetyAgent |
| AI/ML | ExplainabilityAgent |
| financial | PrivacyAgent |
| government | PrivacyAgent |
| IoT/embedded | _(none)_ |
| web/enterprise | _(none)_ |
| telecommunications | _(none)_ |

### Heuristic Fallback Keywords

If LLM domain classification fails, keyword-based detection is used:

| Domain | Keywords |
|---|---|
| automotive | vehicle, automotive, autonomous driving, iso 26262 |
| medical | medical, patient, clinical, healthcare |
| financial | bank, account, transaction, atm, financial |
| AI/ML | ai, machine learning, model, prediction |
| IoT/embedded | embedded, sensor, device, iot |
| web/enterprise | web, enterprise, application, service |
| government | government, public sector, regulation |
| telecommunications | telecom, network, 5g, communication |

---

## Tier 3: Project-Level Constraint Extraction

**Purpose**: Extract explicit quality constraints from the project description and map them to agents not yet activated by Tiers 1-2.

**Parameters**: `temperature=0.0`, `max_tokens=900`, `seed=2`

**Prompt template** (one call per project):

```
Extract specific quality-related constraints from the following project description.
For each constraint, identify which quality agent is most relevant.
Project Description:
{project_description}
Available quality agents and their concerns:
{agent_descriptions_list}
IMPORTANT constraints on agent activation:

FunctionalSafetyAgent: ONLY for systems where malfunction could cause physical
harm to humans (vehicles, medical devices, industrial machinery, robotics).
Software correctness, data integrity, and business rule enforcement do NOT
qualify as functional safety. A bookkeeping system ensuring accurate
calculations is Reliability, not Functional Safety.
FlexibilityAgent: ONLY when the project explicitly requires deployment across
multiple platforms, migration between environments, or runtime adaptability.
Standard feature extensibility does not qualify.
CompatibilityAgent: ONLY when the project explicitly requires integration with
external systems, standards, or protocols. Internal data format handling (like
multi-currency support) is Functional Suitability, not Compatibility.
SafetyAgent: ONLY for systems where the software's behavior could lead to
physical harm, environmental damage, or loss of life. Financial data accuracy
is Reliability, not Safety.

Only activate agents in Tier 3 that are NOT already covered by Tier 1 and
Tier 2 selections. Do not duplicate activations.
When in doubt about whether a constraint maps to a specialized agent, DO NOT
activate that agent. It is better to miss a marginal agent than to activate
an irrelevant one.
Respond in JSON only:
{"constraints": [
{"constraint_text": "<exact phrase from description>", "agent_name": "<AgentName>",
"priority": "high|medium|low", "reasoning": "<why this agent>"}
]}
Only extract constraints that are explicitly stated or strongly implied in the
description. Do not invent constraints.
```

### Activation Rules

- Only constraints with `priority` = "high" or "medium" result in agent activation
- Only agents not already in C₁ ∪ C₂ are added
- Agent names must match entries in the agent pool (`AGENT_QUALITY_METADATA`)

---

## Merge Strategy

The final activated set is: **AG\* = C₁ ∪ C₂ ∪ C₃**

- Tiers are **additive**: each tier can only add agents, never remove
- Ordering is stable: C₁ agents first, then C₂, then C₃ (no duplicates)
- Agent names must exist in `AGENT_QUALITY_METADATA` to be included

---

## Phase 1-5 Agent Prompts

Phase 1-5 agent prompts follow the QUARE/ArgRE protocol. Each quality agent receives:

1. **Role definition**: Specifies the quality dimension and decision stance
2. **Quality lens cues**: Sub-characteristics from the table above
3. **Reasoning instructions**: How to critique and refine requirements
4. **Output schema**: JSON-structured requirements format

Full Phase 1-5 prompts are implemented in `src/openre_bench/pipeline/_core.py` and follow the OpenRE-Bench artifact contract. See the replication package for the complete implementation.
