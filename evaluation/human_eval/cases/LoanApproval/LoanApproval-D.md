# Requirement Set LoanApproval-D

*Project domain: AI-Assisted Loan Approval (Finance / AI)*  
*(You are not told which method produced this set. Rate only what you read.)*

## Specification Outline
- System Scope and Stakeholders
- Quality-Attribute Requirements (Efficiency/Explainability/Performance/Privacy/Reliability/Responsibility/Security/Trustworthiness)
- Negotiation and Conflict Resolution Decisions
- Verification and Compliance Evidence

## Quality-Attribute Requirements

### Efficiency
1. Efficiency objective for LoanApproval: The system must support counterfactual explanations ('what would need to change for approval')
2. The system shall ensure efficiency (latency optimization): The system must support counterfactual explanations ('what would need to change for approval')
3. The system shall ensure efficiency (throughput stability): Model documentation must meet EU AI Act Article 13 transparency requirements
4. The system shall ensure efficiency (resource utilization): Fairness & Bias: The system must monitor and report demographic parity and equalized odds metrics across protected cla...
5. The system shall ensure efficiency (latency optimization): Disparate impact ratio must remain above 0
6. The system shall ensure efficiency (throughput stability): 8 for all protected groups
7. The system shall ensure efficiency (resource utilization): Privacy: Applicant PII must be processed under GDPR principles

### Explainability
1. Explainability objective for LoanApproval: Application Processing: The system shall accept loan applications through web portal, mobile app, and branch interfaces
2. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Application Processing: The system shall ac...
3. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Applications must be enriched with credit b...
4. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Risk Assessment: The ML pipeline shall prod...
5. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Decision Support: Loan officers shall recei...
6. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): The system must present the top contributin...
7. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Portfolio Management: The system shall cont...

### Performance
1. Performance objective for LoanApproval: Disparate impact ratio must remain above 0
2. The system shall ensure performance (time behaviour, resource utilisation, capacity): Disparate impact ratio must remain above 0
3. The system shall ensure performance (time behaviour, resource utilisation, capacity): 8 for all protected groups
4. The system shall ensure performance (time behaviour, resource utilisation, capacity): Privacy: Applicant PII must be processed under GDPR principles
5. The system shall ensure performance (time behaviour, resource utilisation, capacity): Data retention policies must automatically purge declined application details after 24 months
6. The system shall ensure performance (time behaviour, resource utilisation, capacity): Consent management must track data subject rights
7. The system shall ensure performance (time behaviour, resource utilisation, capacity): Security: The system must implement end-to-end encryption for all applicant data

### Privacy
1. Privacy objective for LoanApproval: Human loan officers review AI recommendations for final decisions
2. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Human loan officers review AI recommendations for final deci...
3. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): The system must comply with the Equal Credit Opportunity Act...
4. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): [Core Functional Requirements]
5. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Application Processing: The system shall accept loan applica...
6. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Applications must be enriched with credit bureau data, emplo...
7. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Risk Assessment: The ML pipeline shall produce a credit risk...

### Reliability
1. Reliability objective for LoanApproval: Consent management must track data subject rights
2. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Consent management must track data subject rights
3. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Security: The system must implement end-to-end encryption for all applicant data
4. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Access controls must enforce need-to-know principles with comprehensive audit trails
5. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Reliability: The risk scoring service must maintain 99
6. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): 9% availability during business hours
7. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Model serving must support graceful degradation to rule-based fallback if ML servi...

### Responsibility
1. Responsibility objective for LoanApproval: The system must present the top contributing features for each recommendation
2. The system shall ensure responsibility (regulatory accountability): The system must present the top contributing features for each recommendation
3. The system shall ensure responsibility (stakeholder transparency): Portfolio Management: The system shall continuously monitor approved loans for early default signals and updat...
4. The system shall ensure responsibility (ethical compliance): [Non-Functional Constraints]
5. The system shall ensure responsibility (regulatory accountability): Explainability: All AI-generated decisions must provide human-readable explanations citing specific applicant...
6. The system shall ensure responsibility (stakeholder transparency): The system must support counterfactual explanations ('what would need to change for approval')
7. The system shall ensure responsibility (ethical compliance): Model documentation must meet EU AI Act Article 13 transparency requirements

### Security
1. Security objective for LoanApproval: Reliability: The risk scoring service must maintain 99
2. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Reliability: The risk scoring service must maintain 99
3. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): 9% availability during business hours
4. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Model serving must support graceful degradation to rule-based fallback if ML serv...
5. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Performance: Batch processing of 10,000 applications must complete within 2 hours...
6. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Real-time scoring must complete within 5 seconds for walk-in applicants
7. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Project: AI-Assisted Consumer Loan Approval Platform for Regional Bank

### Trustworthiness
1. Trustworthiness objective for LoanApproval: Real-time scoring must complete within 5 seconds for walk-in applicants
2. The system shall ensure trustworthiness (security assurance): Real-time scoring must complete within 5 seconds for walk-in applicants
3. The system shall ensure trustworthiness (auditability): Project: AI-Assisted Consumer Loan Approval Platform for Regional Bank
4. The system shall ensure trustworthiness (integrity guarantees): The system is a machine learning-powered loan origination platform for a regional bank processing 50,000+ loan ap...
5. The system shall ensure trustworthiness (security assurance): It uses ML models to assess credit risk, detect fraud, and recommend approval decisions
6. The system shall ensure trustworthiness (auditability): Human loan officers review AI recommendations for final decisions
7. The system shall ensure trustworthiness (integrity guarantees): The system must comply with the Equal Credit Opportunity Act (ECOA), Fair Lending regulations, and the EU AI Act...

## Implementation Checklist
- Preserve canonical phase artifact compatibility
- Enforce strict provenance and taint controls
- Trace each integrated requirement to a verification signal
