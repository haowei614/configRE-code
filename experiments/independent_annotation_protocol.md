# Independent Domain-Relevance Annotation Protocol

Document date: 2026-05-07


Purpose: this document is an independent annotation packet for validating the domain relevance of quality/reasoning agents in the OpenRE-Bench case studies. The annotator should use only the case requirements and agent definitions in this document. Please do not consult any existing ground-truth labels, system outputs, experiment results, or previous author annotations.

## 1. Annotation Tasks

You are asked to complete two related tasks.

### Task A: Agent Relevance Labeling

For each case and each agent, mark whether the agent is relevant to the case requirements.

Use the following labels:

| Label | Meaning |
| --- | --- |
| `1` | Relevant. The agent addresses an explicitly stated requirement, domain constraint, quality concern, or core risk in the case. |
| `0` | Not relevant. The agent may be generally useful for software, but it is not central to the stated case requirements. |
| `U` | Uncertain. The requirement text is insufficient or ambiguous for deciding relevance. |

Please provide a short rationale for every `1` or `U` label. A rationale can be one sentence.

### Task B: Domain-Optimized Agent Selection

For each case, select the six most appropriate agents for a domain-optimized configuration.

Rules:

- Select exactly six agents per case.
- Rank them from 1 to 6, where rank 1 is the most important.
- Base the ranking on the case requirement text, not on any existing experiment result.
- If fewer than six agents seem clearly relevant, still choose the closest six and mark lower-confidence choices in the notes.

## 2. Independence Requirements

To preserve the validity of the annotation:

- Do not view the original author's ground-truth labels.
- Do not view the original author's domain-optimized agent choices.
- Do not view Phase0-Auto outputs, experiment metrics, plots, or generated results before completing the annotation.
- Use only the case requirements and agent definitions below.
- If you are unsure, use `U` instead of guessing.

## 3. Relevance Criteria

Mark an agent as relevant when at least one of the following is true:

- The requirement explicitly mentions a concern handled by the agent.
- The domain normally requires the concern for correctness, compliance, safety, or acceptance of the system.
- The case includes a conflict, constraint, or risk that the agent is designed to reason about.

Mark an agent as not relevant when:

- The concern is only a generic software engineering consideration.
- The requirement text gives no evidence that the concern is central for this case.
- Another more specific agent already captures the concern better.

Use `U` when:

- The requirement hints at the concern but does not clearly establish it.
- The agent boundary is unclear from the text.
- You would need additional domain information to decide.

## 4. Agent Definitions

Use the exact agent names below in your annotation.

| No. | Agent | Main concern |
| --- | --- | --- |
| 1 | `SafetyAgent` | Hazard prevention, physical harm avoidance, risk mitigation. |
| 2 | `ReliabilityAgent` | Fault tolerance, availability, recoverability, consistent correct operation. |
| 3 | `PerformanceAgent` | Response time, latency, throughput, real-time behavior, scalability under load. |
| 4 | `UsabilityAgent` | Ease of use, learnability, user error prevention, accessibility, interaction quality. |
| 5 | `EfficiencyAgent` | Efficient use of resources such as computation, memory, power, or optimization effort. |
| 6 | `SecurityAgent` | Authentication, authorization, access control, attack prevention, integrity protection. |
| 7 | `TrustworthinessAgent` | Trust, data protection, accountable handling of sensitive data, dependable behavior from a user or stakeholder perspective. |
| 8 | `MaintainabilityAgent` | Modularity, testability, evolvability, ease of updates and long-term maintenance. |
| 9 | `CompatibilityAgent` | Interoperability, coexistence, integration with external standards, systems, or data formats. |
| 10 | `FlexibilityAgent` | Adaptability, configurability, replaceability, support for changing contexts or requirements. |
| 11 | `FunctionalSafetyAgent` | Functional safety standards and fail-safe behavior, especially ISO 26262-like safety-critical control. |
| 12 | `ExplainabilityAgent` | Transparency, interpretability, explainable automated decisions or model behavior. |
| 13 | `PrivacyAgent` | Personal data protection, consent, data-subject rights, GDPR/FERPA-like privacy obligations. |
| 14 | `GreenAgent` | Energy saving, carbon footprint, environmental sustainability, ISO 14001-like concerns. |
| 15 | `ResponsibilityAgent` | Ethics, accountability, auditability, regulatory responsibility, compliance governance. |

### Notes on Similar Agents

- `SafetyAgent` concerns general prevention of harm. `FunctionalSafetyAgent` concerns safety-critical control and formal functional-safety mechanisms.
- `SecurityAgent` concerns unauthorized access, attacks, and technical protection. `PrivacyAgent` concerns personal data rights and privacy obligations. `TrustworthinessAgent` concerns broader trust and dependable handling of sensitive or important data.
- `PerformanceAgent` concerns latency, throughput, response time, and real-time constraints. `EfficiencyAgent` concerns resource or optimization efficiency.
- `ResponsibilityAgent` concerns ethical accountability, governance, and regulatory responsibility; it should not be selected only because a system is important.

## 5. Case Requirements

### Case 1: AD

Case description: Autonomous Driving System (Baidu Apollo Planning & Control Module)

Requirement:

```text
Project: Baidu Apollo Autonomous Driving System (Planning & Control Module)

[System Context]
The system is a Level 4 autonomous driving platform operating in mixed traffic environments. It must strictly adhere to the "Apollo Pilot Safety Report" and the "EM Motion Planner" specifications.

[Safety Requirements - Based on Apollo Pilot Safety Report]
1. Multi-Layer Safety Architecture:
   - The system must implement "Passive Safety" (collision protection), "Active Safety" (ACC, AEB, LKA), and "Functional Safety" (fail-safe mechanisms).
2. Minimal Risk Maneuver (MRM):
   - Upon detecting a critical system failure (e.g., sensor loss, localization failure) or exiting the ODD, the vehicle must NOT simply stop in lane immediately if unsafe. It must execute an MRM to safely pull over or stop in a low-risk zone within a specific time window.
3. ODD (Operational Design Domain):
   - The system operates in specific urban and highway scenarios. It must continuously monitor ODD compliance and request human takeover (HMI warning) if boundaries are reached.

[Efficiency & Planning Requirements - Based on EM Motion Planner]
1. Multiobjective Optimization:
   - The planner must simultaneously optimize for three conflicting objectives: Safety (collision avoidance), Smoothness (passenger comfort), and Speed (reaching destination).
2. Path-Speed Decoupling (EM Framework):
   - The system must use the Expectation-Maximization (EM) framework.
   - Step 1 (E-step): Generate an optimal path in the Frenet Frame (SL-Graph).
   - Step 2 (M-step): Generate an optimal speed profile in the Station-Time Frame (ST-Graph).
3. Hard Constraints (Mathematical):
   - Trajectory smoothness is critical. The system must minimize "Jerk" (rate of change of acceleration) to ensure passenger comfort.
   - Curvature constraints ($kappa$) must be satisfied to prevent rollover or tire slip.
   - Non-convex obstacle constraints must be handled using iterative quadratic programming (QP).

[Conflict Scenario for Negotiation]
- The SafetyAgent prioritizes "Passive Safety" and strictly enforcing safe distances and MRM execution.
- The EfficiencyAgent prioritizes "Smoothness" and "Speed" using the QP function to minimize Jerk.
- Potential Conflict: An emergency MRM (Safety) triggered by a fault might violate the Jerk/Smoothness constraints (Efficiency), requiring architectural negotiation (e.g., relaxing smoothness constraints during MRM).
```

### Case 2: ATM

Case description: Automated Teller Machine System

Requirement:

```text
The bank client must be able to deposit an amount to and withdraw an amount from his or her accounts using the bank application. Each transaction must be recorded, and the client must have the ability to review all transactions performed against a given account. Recorded transactions must include the date, time, transaction type, amount and account balance after the transaction.

A bank client can have two types of accounts. A checking-account and a saving-account. For each checking account, one related saving-account can exists. The application must verify that a client can gain access to his or her account by identification via a personal identification number (PIN) code.

Neither a checking-account nor a saving-account can have a negative balance. The application should automatically withdraw funds from a related saving-account if the requested withdrawal amount on the checking-account is more than its current balance. If the saving-account balance is insufficient to cover the requested withdrawal amount, the application should inform the user and terminate the transaction.
```

### Case 3: Library

Case description: Library Management System

Requirement:

```text
A library management system must allow library members to borrow and return books. The system must track which books are available, which are borrowed, and by whom. Members must be able to search for books by title, author, or ISBN. The system must enforce borrowing limits (e.g., maximum number of books per member) and track overdue books. Librarians must be able to add new books, remove books, and manage member accounts.
```

### Case 4: RollCall

Case description: Roll Call Attendance Tracking System

Requirement:

```text
A roll call system must track student attendance for classes. The system must allow teachers to mark students as present, absent, or late. Students must be able to view their own attendance records. The system must generate attendance reports for administrators and calculate attendance percentages. The system must support multiple classes and semesters, and maintain historical attendance data.
```

### Case 5: Bookkeeping

Case description: Bookkeeping Accounting System

Requirement:

```text
A bookkeeping system must record financial transactions including income and expenses. The system must support multiple accounts and categories. Users must be able to generate financial reports such as balance sheets, income statements, and cash flow statements. The system must ensure double-entry bookkeeping principles are followed and maintain an audit trail of all transactions. The system must support multiple currencies and handle currency conversion.
```

## 6. Annotator Information

Please complete this section before annotation.

| Field | Value |
| --- | --- |
| Annotator name or ID |  |
| Affiliation or role |  |
| Annotation date |  |
| Prior familiarity with this project? | Yes / No |
| Did you view any original author labels before annotation? | Yes / No |
| Notes on annotation process |  |

## 7. Task A Annotation Table

Fill `Label` with `1`, `0`, or `U`. Add a short rationale for every `1` or `U`.

| Case | Agent | Label | Rationale |
| --- | --- | --- | --- |
| AD | `SafetyAgent` |  |  |
| AD | `ReliabilityAgent` |  |  |
| AD | `PerformanceAgent` |  |  |
| AD | `UsabilityAgent` |  |  |
| AD | `EfficiencyAgent` |  |  |
| AD | `SecurityAgent` |  |  |
| AD | `TrustworthinessAgent` |  |  |
| AD | `MaintainabilityAgent` |  |  |
| AD | `CompatibilityAgent` |  |  |
| AD | `FlexibilityAgent` |  |  |
| AD | `FunctionalSafetyAgent` |  |  |
| AD | `ExplainabilityAgent` |  |  |
| AD | `PrivacyAgent` |  |  |
| AD | `GreenAgent` |  |  |
| AD | `ResponsibilityAgent` |  |  |
| ATM | `SafetyAgent` |  |  |
| ATM | `ReliabilityAgent` |  |  |
| ATM | `PerformanceAgent` |  |  |
| ATM | `UsabilityAgent` |  |  |
| ATM | `EfficiencyAgent` |  |  |
| ATM | `SecurityAgent` |  |  |
| ATM | `TrustworthinessAgent` |  |  |
| ATM | `MaintainabilityAgent` |  |  |
| ATM | `CompatibilityAgent` |  |  |
| ATM | `FlexibilityAgent` |  |  |
| ATM | `FunctionalSafetyAgent` |  |  |
| ATM | `ExplainabilityAgent` |  |  |
| ATM | `PrivacyAgent` |  |  |
| ATM | `GreenAgent` |  |  |
| ATM | `ResponsibilityAgent` |  |  |
| Library | `SafetyAgent` |  |  |
| Library | `ReliabilityAgent` |  |  |
| Library | `PerformanceAgent` |  |  |
| Library | `UsabilityAgent` |  |  |
| Library | `EfficiencyAgent` |  |  |
| Library | `SecurityAgent` |  |  |
| Library | `TrustworthinessAgent` |  |  |
| Library | `MaintainabilityAgent` |  |  |
| Library | `CompatibilityAgent` |  |  |
| Library | `FlexibilityAgent` |  |  |
| Library | `FunctionalSafetyAgent` |  |  |
| Library | `ExplainabilityAgent` |  |  |
| Library | `PrivacyAgent` |  |  |
| Library | `GreenAgent` |  |  |
| Library | `ResponsibilityAgent` |  |  |
| RollCall | `SafetyAgent` |  |  |
| RollCall | `ReliabilityAgent` |  |  |
| RollCall | `PerformanceAgent` |  |  |
| RollCall | `UsabilityAgent` |  |  |
| RollCall | `EfficiencyAgent` |  |  |
| RollCall | `SecurityAgent` |  |  |
| RollCall | `TrustworthinessAgent` |  |  |
| RollCall | `MaintainabilityAgent` |  |  |
| RollCall | `CompatibilityAgent` |  |  |
| RollCall | `FlexibilityAgent` |  |  |
| RollCall | `FunctionalSafetyAgent` |  |  |
| RollCall | `ExplainabilityAgent` |  |  |
| RollCall | `PrivacyAgent` |  |  |
| RollCall | `GreenAgent` |  |  |
| RollCall | `ResponsibilityAgent` |  |  |
| Bookkeeping | `SafetyAgent` |  |  |
| Bookkeeping | `ReliabilityAgent` |  |  |
| Bookkeeping | `PerformanceAgent` |  |  |
| Bookkeeping | `UsabilityAgent` |  |  |
| Bookkeeping | `EfficiencyAgent` |  |  |
| Bookkeeping | `SecurityAgent` |  |  |
| Bookkeeping | `TrustworthinessAgent` |  |  |
| Bookkeeping | `MaintainabilityAgent` |  |  |
| Bookkeeping | `CompatibilityAgent` |  |  |
| Bookkeeping | `FlexibilityAgent` |  |  |
| Bookkeeping | `FunctionalSafetyAgent` |  |  |
| Bookkeeping | `ExplainabilityAgent` |  |  |
| Bookkeeping | `PrivacyAgent` |  |  |
| Bookkeeping | `GreenAgent` |  |  |
| Bookkeeping | `ResponsibilityAgent` |  |  |

## 8. Task B Domain-Optimized Selection Table

Select exactly six agents for each case and rank them by importance.

| Case | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AD |  |  |  |  |  |  |  |
| ATM |  |  |  |  |  |  |  |
| Library |  |  |  |  |  |  |  |
| RollCall |  |  |  |  |  |  |  |
| Bookkeeping |  |  |  |  |  |  |  |

## 9. Optional CSV Template

If you prefer to annotate in Excel or a spreadsheet, copy the following CSV structure and fill it in.

```csv
case_id,agent,label,rationale
AD,SafetyAgent,,
AD,ReliabilityAgent,,
AD,PerformanceAgent,,
AD,UsabilityAgent,,
AD,EfficiencyAgent,,
AD,SecurityAgent,,
AD,TrustworthinessAgent,,
AD,MaintainabilityAgent,,
AD,CompatibilityAgent,,
AD,FlexibilityAgent,,
AD,FunctionalSafetyAgent,,
AD,ExplainabilityAgent,,
AD,PrivacyAgent,,
AD,GreenAgent,,
AD,ResponsibilityAgent,,
ATM,SafetyAgent,,
ATM,ReliabilityAgent,,
ATM,PerformanceAgent,,
ATM,UsabilityAgent,,
ATM,EfficiencyAgent,,
ATM,SecurityAgent,,
ATM,TrustworthinessAgent,,
ATM,MaintainabilityAgent,,
ATM,CompatibilityAgent,,
ATM,FlexibilityAgent,,
ATM,FunctionalSafetyAgent,,
ATM,ExplainabilityAgent,,
ATM,PrivacyAgent,,
ATM,GreenAgent,,
ATM,ResponsibilityAgent,,
Library,SafetyAgent,,
Library,ReliabilityAgent,,
Library,PerformanceAgent,,
Library,UsabilityAgent,,
Library,EfficiencyAgent,,
Library,SecurityAgent,,
Library,TrustworthinessAgent,,
Library,MaintainabilityAgent,,
Library,CompatibilityAgent,,
Library,FlexibilityAgent,,
Library,FunctionalSafetyAgent,,
Library,ExplainabilityAgent,,
Library,PrivacyAgent,,
Library,GreenAgent,,
Library,ResponsibilityAgent,,
RollCall,SafetyAgent,,
RollCall,ReliabilityAgent,,
RollCall,PerformanceAgent,,
RollCall,UsabilityAgent,,
RollCall,EfficiencyAgent,,
RollCall,SecurityAgent,,
RollCall,TrustworthinessAgent,,
RollCall,MaintainabilityAgent,,
RollCall,CompatibilityAgent,,
RollCall,FlexibilityAgent,,
RollCall,FunctionalSafetyAgent,,
RollCall,ExplainabilityAgent,,
RollCall,PrivacyAgent,,
RollCall,GreenAgent,,
RollCall,ResponsibilityAgent,,
Bookkeeping,SafetyAgent,,
Bookkeeping,ReliabilityAgent,,
Bookkeeping,PerformanceAgent,,
Bookkeeping,UsabilityAgent,,
Bookkeeping,EfficiencyAgent,,
Bookkeeping,SecurityAgent,,
Bookkeeping,TrustworthinessAgent,,
Bookkeeping,MaintainabilityAgent,,
Bookkeeping,CompatibilityAgent,,
Bookkeeping,FlexibilityAgent,,
Bookkeeping,FunctionalSafetyAgent,,
Bookkeeping,ExplainabilityAgent,,
Bookkeeping,PrivacyAgent,,
Bookkeeping,GreenAgent,,
Bookkeeping,ResponsibilityAgent,,
```

Domain-optimized selection CSV:

```csv
case_id,rank_1,rank_2,rank_3,rank_4,rank_5,rank_6,notes
AD,,,,,,,
ATM,,,,,,,
Library,,,,,,,
RollCall,,,,,,,
Bookkeeping,,,,,,,
```

## 10. Annotator Declaration

Please complete after annotation.

I confirm that I completed the annotation independently using the case requirements and agent definitions in this document.

| Field | Value |
| --- | --- |
| Annotator signature or typed name |  |
| Completion date |  |
| Any uncertainty or concerns about the protocol |  |

## 11. Completed Annotation: Annotator-2

This section records the completed independent annotation returned by Annotator-2. The original blank protocol above is retained as the annotation instrument.

### Annotator Metadata

| Field | Value |
| --- | --- |
| Annotator name or ID | Annotator-2 (Chong L.) |
| Affiliation or role | Post-doc Researcher, Tongji University |
| Annotation date | 2026-05-05 |
| Prior familiarity with this project? | No |
| Did you view any original author labels before annotation? | No |
| Notes on annotation process | Followed protocol strictly; labeled independently; rationale for all 1/U; selected exactly 6 agents per case for domain-optimized set. |

### Task A Completed Labels

| Case | Agent | Label | Rationale |
| --- | --- | --- | --- |
| AD | `SafetyAgent` | 1 | Explicit hazard prevention and collision avoidance. |
| AD | `ReliabilityAgent` | 1 | Requires fault tolerance for sensor/localization failure. |
| AD | `PerformanceAgent` | 1 | Real-time response and latency constraints. |
| AD | `UsabilityAgent` | 0 |  |
| AD | `EfficiencyAgent` | 1 | Explicit smoothness and Jerk optimization. |
| AD | `SecurityAgent` | 0 |  |
| AD | `TrustworthinessAgent` | U | HMI interaction mentioned but not central. |
| AD | `MaintainabilityAgent` | 0 |  |
| AD | `CompatibilityAgent` | 0 |  |
| AD | `FlexibilityAgent` | 0 |  |
| AD | `FunctionalSafetyAgent` | 1 | ISO 26262-style fail-safe and MRM required. |
| AD | `ExplainabilityAgent` | 0 |  |
| AD | `PrivacyAgent` | 0 |  |
| AD | `GreenAgent` | 0 |  |
| AD | `ResponsibilityAgent` | U | Regulatory context implied but not explicit. |
| ATM | `SafetyAgent` | 0 |  |
| ATM | `ReliabilityAgent` | 1 | Transaction integrity and consistent operation. |
| ATM | `PerformanceAgent` | 1 | Responsive transaction processing. |
| ATM | `UsabilityAgent` | 1 | Clear user interaction for deposit/withdraw. |
| ATM | `EfficiencyAgent` | 0 |  |
| ATM | `SecurityAgent` | 1 | PIN authentication and access control. |
| ATM | `TrustworthinessAgent` | 1 | Dependable handling of financial data. |
| ATM | `MaintainabilityAgent` | 0 |  |
| ATM | `CompatibilityAgent` | 0 |  |
| ATM | `FlexibilityAgent` | 0 |  |
| ATM | `FunctionalSafetyAgent` | 0 |  |
| ATM | `ExplainabilityAgent` | 0 |  |
| ATM | `PrivacyAgent` | 1 | Sensitive account and personal data protection. |
| ATM | `GreenAgent` | 0 |  |
| ATM | `ResponsibilityAgent` | 0 |  |
| Library | `SafetyAgent` | 0 |  |
| Library | `ReliabilityAgent` | 1 | Track books and members consistently. |
| Library | `PerformanceAgent` | 0 |  |
| Library | `UsabilityAgent` | 1 | Search, borrow, return user interaction core. |
| Library | `EfficiencyAgent` | 0 |  |
| Library | `SecurityAgent` | 1 | Account and borrowing record protection. |
| Library | `TrustworthinessAgent` | 0 |  |
| Library | `MaintainabilityAgent` | 1 | Manage books and accounts long-term. |
| Library | `CompatibilityAgent` | 1 | Integrate with library catalog standards. |
| Library | `FlexibilityAgent` | 1 | Support borrowing limits and overdue rules. |
| Library | `FunctionalSafetyAgent` | 0 |  |
| Library | `ExplainabilityAgent` | 0 |  |
| Library | `PrivacyAgent` | 0 |  |
| Library | `GreenAgent` | 0 |  |
| Library | `ResponsibilityAgent` | 0 |  |
| RollCall | `SafetyAgent` | 0 |  |
| RollCall | `ReliabilityAgent` | 1 | Record attendance accurately. |
| RollCall | `PerformanceAgent` | 1 | Quick marking and report generation. |
| RollCall | `UsabilityAgent` | 1 | Teacher/student interface core. |
| RollCall | `EfficiencyAgent` | 0 |  |
| RollCall | `SecurityAgent` | 1 | Protect student attendance data. |
| RollCall | `TrustworthinessAgent` | 0 |  |
| RollCall | `MaintainabilityAgent` | 1 | Historical data management. |
| RollCall | `CompatibilityAgent` | 0 |  |
| RollCall | `FlexibilityAgent` | 1 | Support multiple classes/semesters. |
| RollCall | `FunctionalSafetyAgent` | 0 |  |
| RollCall | `ExplainabilityAgent` | 0 |  |
| RollCall | `PrivacyAgent` | 0 |  |
| RollCall | `GreenAgent` | 0 |  |
| RollCall | `ResponsibilityAgent` | 0 |  |
| Bookkeeping | `SafetyAgent` | 0 |  |
| Bookkeeping | `ReliabilityAgent` | 1 | Double-entry consistency and audit trail. |
| Bookkeeping | `PerformanceAgent` | 1 | Fast report generation. |
| Bookkeeping | `UsabilityAgent` | 0 |  |
| Bookkeeping | `EfficiencyAgent` | 0 |  |
| Bookkeeping | `SecurityAgent` | 1 | Protect financial transaction data. |
| Bookkeeping | `TrustworthinessAgent` | 1 | Accountable and auditable behavior. |
| Bookkeeping | `MaintainabilityAgent` | 0 |  |
| Bookkeeping | `CompatibilityAgent` | 0 |  |
| Bookkeeping | `FlexibilityAgent` | 0 |  |
| Bookkeeping | `FunctionalSafetyAgent` | 0 |  |
| Bookkeeping | `ExplainabilityAgent` | 0 |  |
| Bookkeeping | `PrivacyAgent` | 1 | Sensitive financial data protection. |
| Bookkeeping | `GreenAgent` | 0 |  |
| Bookkeeping | `ResponsibilityAgent` | 1 | Regulatory compliance and audit. |

### Task B Completed Domain-Optimized Selection

| Case | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Rank 5 | Rank 6 |
| --- | --- | --- | --- | --- | --- | --- |
| AD | `FunctionalSafetyAgent` | `SafetyAgent` | `PerformanceAgent` | `EfficiencyAgent` | `ReliabilityAgent` | `TrustworthinessAgent` |
| ATM | `SecurityAgent` | `PrivacyAgent` | `ReliabilityAgent` | `TrustworthinessAgent` | `PerformanceAgent` | `UsabilityAgent` |
| Library | `UsabilityAgent` | `ReliabilityAgent` | `SecurityAgent` | `MaintainabilityAgent` | `CompatibilityAgent` | `FlexibilityAgent` |
| RollCall | `UsabilityAgent` | `ReliabilityAgent` | `PerformanceAgent` | `SecurityAgent` | `FlexibilityAgent` | `MaintainabilityAgent` |
| Bookkeeping | `SecurityAgent` | `ReliabilityAgent` | `PrivacyAgent` | `TrustworthinessAgent` | `PerformanceAgent` | `ResponsibilityAgent` |

## 12. Agreement Summary

Agreement was recomputed against the original author labels in `experiments/ground_truth/domain_relevance.json`. For the calculation below, labels marked `1` are treated as positive/relevant labels. Labels marked `0` or `U` are treated as non-positive labels for binary agreement calculation.

| Case | Author positive labels | Annotator-2 positive labels | Jaccard similarity | Cohen's kappa |
| --- | ---: | ---: | ---: | ---: |
| AD | 6 | 5 | 0.833 | 0.857 |
| ATM | 6 | 6 | 0.714 | 0.722 |
| Library | 5 | 6 | 0.833 | 0.857 |
| RollCall | 5 | 6 | 0.571 | 0.571 |
| Bookkeeping | 5 | 6 | 0.571 | 0.571 |
| Average | 5.4 | 5.8 | 0.705 | 0.716 |

Pooled over all 75 binary case-agent decisions, the observed agreement is 0.867, pooled Jaccard similarity is 0.697, and pooled Cohen's kappa is 0.715.

Interpretation: the independent annotation shows substantial agreement with the original author labels. Main disagreements occur in the boundary cases around `GreenAgent` for AD, `ResponsibilityAgent` versus `PerformanceAgent` for ATM, `PrivacyAgent` versus `FlexibilityAgent`/`MaintainabilityAgent` for RollCall, and `UsabilityAgent` versus `PrivacyAgent`/`PerformanceAgent` for Bookkeeping.

