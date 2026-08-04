# Requirement Set LoanApproval-B

*Project domain: AI-Assisted Loan Approval (Finance / AI)*  
*(You are not told which method produced this set. Rate only what you read.)*

## Specification Outline
- System Scope and Stakeholders
- Quality-Attribute Requirements (Explainability/Performance/Privacy/Reliability/Responsibility/Security)
- Negotiation and Conflict Resolution Decisions
- Verification and Compliance Evidence

## Quality-Attribute Requirements

### Explainability
1. Explainability objective for LoanApproval: The system must support counterfactual explanations ('what would need to change for approval')
2. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): The system must support counterfactual expl...
3. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Model documentation must meet EU AI Act Art...
4. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Fairness & Bias: The system must monitor an...
5. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Disparate impact ratio must remain above 0
6. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): 8 for all protected groups
7. The system shall ensure explainability (model transparency, decision interpretability, human reviewability per EU AI Act Article 13): Privacy: Applicant PII must be processed un...

### Performance
1. Performance objective for LoanApproval: Decision Support: Loan officers shall receive the AI recommendation with key risk factors highlighted
2. The system shall ensure performance (time behaviour, resource utilisation, capacity): Decision Support: Loan officers shall receive the AI recommendation with key risk factors h...
3. The system shall ensure performance (time behaviour, resource utilisation, capacity): The system must present the top contributing features for each recommendation
4. The system shall ensure performance (time behaviour, resource utilisation, capacity): Portfolio Management: The system shall continuously monitor approved loans for early defaul...
5. The system shall ensure performance (time behaviour, resource utilisation, capacity): [Non-Functional Constraints]
6. The system shall ensure performance (time behaviour, resource utilisation, capacity): Explainability: All AI-generated decisions must provide human-readable explanations citing...
7. The system shall ensure performance (time behaviour, resource utilisation, capacity): The system must support counterfactual explanations ('what would need to change for approval')

### Privacy
1. Privacy objective for LoanApproval: Access controls must enforce need-to-know principles with comprehensive audit trails
2. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Access controls must enforce need-to-know principles with co...
3. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Reliability: The risk scoring service must maintain 99
4. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): 9% availability during business hours
5. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Model serving must support graceful degradation to rule-base...
6. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Performance: Batch processing of 10,000 applications must co...
7. The system shall ensure privacy (data minimisation, consent management, data subject rights per GDPR and ISO 27701): Real-time scoring must complete within 5 seconds for walk-in...

### Reliability
1. Reliability objective for LoanApproval: Real-time scoring must complete within 5 seconds for walk-in applicants
2. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Real-time scoring must complete within 5 seconds for walk-in applicants
3. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Project: AI-Assisted Consumer Loan Approval Platform for Regional Bank
4. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): The system is a machine learning-powered loan origination platform for a regional...
5. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): It uses ML models to assess credit risk, detect fraud, and recommend approval deci...
6. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): Human loan officers review AI recommendations for final decisions
7. The system shall ensure reliability (maturity, availability, fault tolerance, recoverability): The system must comply with the Equal Credit Opportunity Act (ECOA), Fair Lending...

### Responsibility
1. Responsibility objective for LoanApproval: The system must comply with the Equal Credit Opportunity Act (ECOA), Fair Lending regulations, and the EU AI Act for high-risk AI systems
2. The system shall ensure responsibility (regulatory accountability): The system must comply with the Equal Credit Opportunity Act (ECOA), Fair Lending regulations, and the EU AI...
3. The system shall ensure responsibility (stakeholder transparency): [Core Functional Requirements]
4. The system shall ensure responsibility (ethical compliance): Application Processing: The system shall accept loan applications through web portal, mobile app, and branch interfaces
5. The system shall ensure responsibility (regulatory accountability): Applications must be enriched with credit bureau data, employment verification, and property appraisal data
6. The system shall ensure responsibility (stakeholder transparency): Risk Assessment: The ML pipeline shall produce a credit risk score, fraud probability score, and recommended d...
7. The system shall ensure responsibility (ethical compliance): Decision Support: Loan officers shall receive the AI recommendation with key risk factors highlighted

### Security
1. Security objective for LoanApproval: 8 for all protected groups
2. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): 8 for all protected groups
3. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Privacy: Applicant PII must be processed under GDPR principles
4. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Data retention policies must automatically purge declined application details aft...
5. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Consent management must track data subject rights
6. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Security: The system must implement end-to-end encryption for all applicant data
7. The system shall ensure security (confidentiality, integrity, non-repudiation, authentication): Access controls must enforce need-to-know principles with comprehensive audit trails

## Implementation Checklist
- Preserve canonical phase artifact compatibility
- Enforce strict provenance and taint controls
- Trace each integrated requirement to a verification signal
