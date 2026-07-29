# Requirements Document Template

Use placeholders as unresolved decisions, not suggested defaults. Replace them
only with sourced facts or explicitly owned decisions.

**Status:** [Draft / In Review / Accepted]
**Scope owner:** [Role or owner]
**Authoritative inputs:** [Sources]

## Introduction

[PROJECT NAME] is a [SYSTEM TYPE] designed for [TARGET USERS]. The system [PRIMARY PURPOSE].

## System Context

### Architectural Overview
- **Components:** [List major system components]
- **Data Flow:** [High-level data movement]
- **Integration Points:** [External systems/APIs]
- **Deployment Model:** [Cloud/On-premise/Hybrid]

## Glossary

- **[Term]**: [Definition specific to this system]
- **Component**: Major system module or service
- **Integration Point**: Connection to external system or API

## Functional Requirements

### REQ-1: [Feature Name]

**User Story:** As a [user role], I want [feature], so that [benefit]
**Source/Owner:** [Evidence or decision owner]
**Priority/Status:** [Project-defined priority] / [Status]

**Acceptance Criteria:**
1. WHEN [condition], THE system SHALL [behavior]
2. THE system SHALL [requirement] within [time constraint]
3. IF [error condition], THEN THE system SHALL [error handling]

**Components Involved:** [COMP-1, COMP-2]
**Data Flow:** [How data moves for this requirement]

### REQ-2: [Feature Name]

**User Story:** As a [user role], I want [feature], so that [benefit]

**Acceptance Criteria:**
1. WHEN [condition], THE system SHALL [behavior]
2. WHERE [context], THE system SHALL [behavior]
3. THE system SHALL persist [data] with [attributes]

**Components Involved:** [COMP-3, COMP-4]
**Integration Points:** [External systems used]

## Non-Functional Requirements

### Performance Requirements
- Response time: Under [workload and environment], THE system SHALL meet
  [approved percentile and threshold], measured by [method]
- Concurrency: THE system SHALL support [approved workload profile], measured
  by [method]
- Data processing: THE system SHALL process [approved rate and data profile],
  measured by [method]

### Security Requirements  
- Identity: [State whether authentication is required and why]
- Authorization: [Approved access model and denied behavior]
- Data protection: [Classification, threat, approved control, and evidence]

### Reliability Requirements
- Availability: THE system SHALL meet [approved objective and measurement window]
- Recovery: THE system SHALL meet [approved recovery objective], measured by [method]
- Data integrity: THE system SHALL provide [approved consistency and durability behavior]

### Scalability Requirements
- Capacity: [Approved workload and growth model]
- Scaling approach: [Decision supported by measurements and constraints]
- Limits and backpressure: [Observable behavior at approved boundaries]

## Constraints and Boundaries

### Technical Constraints
- Technology: [Programming languages, frameworks, databases]
- Infrastructure: [Cloud provider, hardware limitations]

### Business Constraints
- Budget: [Cost limitations]
- Timeline: [Delivery deadlines]
- Compliance: [Regulatory requirements]

### Scope Boundaries
- **In Scope:** [What's included]
- **Out of Scope:** [What's explicitly excluded]
- **Future Considerations:** [Deferred features]

## Traceability

| Requirement | Design coverage | Delivery tasks | Verification | Status |
|---|---|---|---|---|
| REQ-1 | [Design IDs] | [Task IDs] | [Evidence] | [Status] |
