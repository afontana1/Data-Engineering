# 12. Security and trust boundaries

These questions test whether the candidate thinks in adversarial and boundary-aware terms. The goal is to see whether they understand what is trusted, what is not, what must be protected, and how security concerns shape system design.

## Table of contents

- [A. Trust boundaries and untrusted inputs](#a-trust-boundaries-and-untrusted-inputs)
- [B. Authentication, authorization, and access control](#b-authentication-authorization-and-access-control)
- [C. Sensitive data, secrets, and credentials](#c-sensitive-data-secrets-and-credentials)
- [D. Abuse cases and threat modeling](#d-abuse-cases-and-threat-modeling)
- [E. Compliance, auditability, and security tradeoffs](#e-compliance-auditability-and-security-tradeoffs)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched for appointments, booked or cancelled visits, and received reminders. Clinic staff used operational tools, external clinic systems exchanged scheduling data, and the platform handled patient identity, contact information, booking history, and integration credentials.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can identify trust changes, separate authentication from authorization, protect sensitive data across its lifecycle, reason about abuse, and connect security controls to product and operational tradeoffs.



## A. Trust boundaries and untrusted inputs

* What were the trust boundaries in this system?
* What inputs were untrusted?
* Which users, clients, services, or integrations could not be fully trusted?
* Where did data cross from an untrusted context into a trusted one?
* How did you validate, sanitize, or constrain untrusted inputs?
* What assumptions would be dangerous to make about client behavior?
* If this system were exposed publicly tomorrow, what would you re-check first?
* What boundary would a junior engineer be most likely to overlook?

What this reveals:
Whether they can identify where trust changes and where the system needs to defend itself.

### Clarifying questions a strong candidate may ask

* Should I focus on network boundaries, identity boundaries, or data boundaries?
* Would you like one trust transition in depth?
* Should I include internal services and operators as partially trusted?
* Are you interested in validation mechanics or threat assumptions?
* Should I describe what would change for public exposure?

These questions show that trust is contextual. Internal systems, authenticated users, partner integrations, and operators are not automatically fully trusted.

### Reasoning expected from the candidate

A strong answer should identify:

1. **Trust zones**
   * Browser, mobile app, public API, internal service, partner network, operator tool, database?
2. **Boundary crossings**
   * Where does data move from a lower-trust context to a higher-trust one?
3. **Assets**
   * What data, action, or capability is being protected?
4. **Threats**
   * Malformed input, impersonation, replay, privilege abuse, injection, or data leakage?
5. **Controls**
   * Authentication, authorization, schema validation, sanitization, rate limits, isolation, or auditing?
6. **Assumptions**
   * Which assumptions about clients or partners would be unsafe?
7. **Residual risk**
   * What remains possible even after validation?

A mature answer treats:

* clients as untrusted even when first-party;
* internal services as authenticated but not omnipotent;
* partner data as untrusted input;
* operator actions as high-risk due to privilege;
* caches, logs, queues, and analytics as additional data boundaries.

### Example of a strong coherent answer

> The primary trust boundary was between the patient browser and the public API. Everything from the browser was untrusted, including identifiers, hidden fields, timestamps, and role claims.
>
> A second boundary existed between our platform and clinic scheduling vendors. Those systems were authenticated partners, but their payloads could still be malformed, stale, duplicated, or semantically inconsistent.
>
> Internal service calls were not trusted solely because they came from the private network. Services authenticated with workload identity and were authorized for specific operations.
>
> Operator tools formed another important boundary because support staff had elevated access. Their actions required stronger authorization, narrow scopes, audit records, and safer defaults.
>
> Inputs crossed into trusted processing at API handlers and integration adapters. We applied schema validation, semantic checks, tenant and ownership resolution, size limits, and typed normalization before domain logic used the data.
>
> A dangerous assumption would have been trusting a client-supplied patient ID or tenant ID. Those values were derived from authenticated server context instead.
>
> If the system became public to third-party developers, I would first re-check authorization defaults, rate limits, error leakage, identifier predictability, dependency quotas, and undocumented assumptions in internal APIs.

### Question-by-question answer expectations

#### What were the trust boundaries in this system?

Strong answers identify changes in trust level rather than only firewalls.

Examples:

* browser to API;
* service to service;
* partner to adapter;
* operator to admin action;
* application to database;
* production to analytics;
* tenant to tenant.

#### What inputs were untrusted?

The candidate should include:

* request fields;
* headers;
* cookies;
* uploaded files;
* webhook payloads;
* partner data;
* configuration;
* queue messages;
* client-side state.

#### Which users, clients, services, or integrations could not be fully trusted?

A mature answer explains partial trust and least privilege.

#### Where did data cross from an untrusted context into a trusted one?

The candidate should name the entry point and the checks performed before domain use.

#### How did you validate, sanitize, or constrain untrusted inputs?

Strong mechanisms:

* schema validation;
* type checking;
* range limits;
* allowlists;
* canonicalization;
* content escaping;
* parameterized queries;
* file scanning;
* size limits;
* semantic validation.

#### What assumptions would be dangerous to make about client behavior?

Examples:

* client enforces permissions;
* hidden fields remain unchanged;
* requests arrive once;
* UI order is respected;
* timestamps are trustworthy;
* client version is current;
* IDs belong to the caller.

#### If this system were exposed publicly tomorrow, what would you re-check first?

High-signal answers prioritize:

* authn/authz;
* rate limiting;
* abuse prevention;
* error leakage;
* input limits;
* secret handling;
* tenancy;
* monitoring;
* dependency capacity.

#### What boundary would a junior engineer be most likely to overlook?

Strong answers identify a subtle boundary such as internal service identity, support tools, analytics exports, or webhook verification.

### Follow-up probes for the interviewer

* What made an internal service trustworthy enough?
* Did partner payloads get schema-validated?
* Who supplied the tenant context?
* What boundary existed around logs or analytics?
* Were admin tools on a separate trust path?
* What happened to rejected input?
* Could malformed input reach the database?
* What assumption was later proven unsafe?

### Weak-answer signals

Watch for answers that:

* trust first-party clients;
* treat internal networks as fully trusted;
* validate shape but not semantics;
* rely on hidden UI fields;
* use client-supplied authorization context;
* ignore operator and analytics boundaries;
* sanitize without understanding context;
* cannot identify a subtle trust transition.

---


## B. Authentication, authorization, and access control

* How did you think about authentication versus authorization?
* Who was allowed to perform which actions?
* Where was authorization enforced?
* Were there different roles, permissions, tenants, or ownership rules?
* How did you prevent one user, tenant, workflow, or service from affecting another improperly?
* Were there places where frontend-only checks would have been insufficient?
* What authorization edge case was easiest to miss?
* How would you test that access control was working correctly?

What this reveals:
Whether they understand that knowing who someone is and knowing what they can do are separate design problems.

### Clarifying questions a strong candidate may ask

* Should I focus on end-user access, service access, or both?
* Would you like role-based, ownership-based, or tenant-based rules in depth?
* Should I discuss where authorization was enforced?
* Are you interested in edge cases such as support access or delegated actions?
* Should I include how access control was tested?

These questions show that identity and permission are separate and often multi-dimensional.

### Reasoning expected from the candidate

A strong answer should distinguish:

* **authentication:** who or what is making the request;
* **authorization:** whether that identity may perform this action on this resource;
* **context:** tenant, role, ownership, workflow state, location, or purpose;
* **enforcement:** where the decision is made;
* **default:** deny unless explicitly allowed;
* **auditability:** whether sensitive decisions are attributable.

A mature answer should explain:

1. identity establishment;
2. permission model;
3. resource ownership;
4. tenant isolation;
5. service-to-service privileges;
6. server-side enforcement;
7. edge cases;
8. negative testing.

### Example of a strong coherent answer

> Authentication established the patient, clinic staff member, or service identity. Authorization then evaluated whether that identity could perform a particular action on a particular resource.
>
> Patients could search broadly but could only view or change bookings associated with their authenticated identity. Clinic staff access was scoped by clinic and role. Support staff had narrowly defined elevated actions with audit requirements.
>
> Tenant and ownership context came from the server-side identity session and resource lookup, not from client-supplied fields.
>
> Authorization was enforced in the backend near the domain action. The frontend hid actions the user could not perform for usability, but those checks were never treated as security controls.
>
> Service-to-service permissions were capability-scoped. The notification service could read delivery-relevant booking data but could not cancel appointments.
>
> An easy edge case to miss was a staff user moving between clinics while an old session retained stale permissions. We used short-lived claims plus server-side policy checks against current assignments for high-impact actions.
>
> We tested access control with role matrices, negative integration tests, cross-tenant ID substitution, direct API calls bypassing the UI, and audit review of privileged actions.

### Question-by-question answer expectations

#### How did you think about authentication versus authorization?

The candidate should clearly separate identity from permission.

#### Who was allowed to perform which actions?

Strong answers describe actors, actions, resources, and conditions.

#### Where was authorization enforced?

The authoritative check should be server-side.

Possible layers:

* API policy layer;
* domain service;
* database row policy;
* service mesh for coarse service access;
* object-level access check.

#### Were there different roles, permissions, tenants, or ownership rules?

The candidate should explain how these dimensions combined.

#### How did you prevent one user, tenant, workflow, or service from affecting another improperly?

Mechanisms:

* tenant-scoped queries;
* ownership checks;
* unguessable IDs plus authorization;
* row-level security;
* service capabilities;
* partitioning;
* policy tests.

Identifiers alone are not authorization.

#### Were there places where frontend-only checks would have been insufficient?

Strong candidates should say all security-sensitive actions require server enforcement.

#### What authorization edge case was easiest to miss?

Examples:

* indirect object reference;
* stale role;
* shared resource;
* delegated access;
* support override;
* background job acting without original context;
* cross-tenant search filters.

#### How would you test that access control was working correctly?

Strong methods:

* permission matrix;
* negative tests;
* cross-tenant substitution;
* fuzzed resource IDs;
* role-change tests;
* policy unit tests;
* audit sampling;
* penetration testing where appropriate.

### Follow-up probes for the interviewer

* Was access deny-by-default?
* Who resolved resource ownership?
* Could a service call bypass policy?
* Did background jobs preserve actor context?
* How were support overrides approved?
* What happened after role revocation?
* Were list queries tenant-scoped?
* Which negative test caught a real bug?

### Weak-answer signals

Watch for answers that:

* conflate authentication and authorization;
* trust frontend visibility controls;
* use role checks without resource ownership;
* accept tenant IDs from clients;
* assume unguessable IDs are sufficient;
* give internal services broad permissions;
* lack negative access tests;
* cannot identify an authorization edge case.

---


## C. Sensitive data, secrets, and credentials

* What was the most sensitive data in the system?
* How was sensitive data stored, transmitted, displayed, logged, or exported?
* Were there secrets, tokens, API keys, certificates, or credentials in the flow?
* How were secrets managed and rotated?
* How did you prevent sensitive data from leaking into logs, analytics, errors, or client responses?
* What data should never be trusted to the client?
* What data should never be persisted longer than necessary?
* What sensitive-data mistake would have had the highest impact?

What this reveals:
Whether they understand that security includes protecting data throughout its lifecycle, not just checking permissions at the entrance.

### Clarifying questions a strong candidate may ask

* Should I focus on patient data, operational secrets, or both?
* Would you like the full data lifecycle?
* Should I discuss encryption, logging, and retention?
* Are you interested in secret rotation mechanics?
* Should I include what data was intentionally excluded from clients?

These questions show that data protection includes collection, use, storage, transfer, logging, export, and deletion.

### Reasoning expected from the candidate

A strong answer should classify:

1. **Sensitivity**
   * Public, internal, confidential, regulated, credential, or secret?
2. **Collection**
   * Was every field necessary?
3. **Storage**
   * Encryption, access scope, and segregation?
4. **Transmission**
   * Secure transport and endpoint verification?
5. **Display**
   * Masking, least data, and role-based visibility?
6. **Logging and analytics**
   * Redaction, tokenization, and field allowlists?
7. **Retention**
   * How long and why?
8. **Deletion**
   * How was data removed from primary and derived stores?
9. **Secrets**
   * Storage, distribution, rotation, and revocation?

### Example of a strong coherent answer

> The most sensitive data included patient identity, contact information, appointment details, clinic affiliations, and audit history. Integration credentials and signing secrets were also highly sensitive.
>
> Data was encrypted in transit and at rest. Access to production data was role-scoped, and operational tools displayed only the fields needed for the support task.
>
> We used structured logging with an allowlist rather than logging full request bodies. Patient names, email addresses, free-text notes, access tokens, and external credentials were redacted or excluded. Analytics events used pseudonymous identifiers where possible.
>
> Secrets were stored in a managed secret system, delivered to workloads through short-lived identity-based access, and rotated without code changes. We avoided long-lived credentials in configuration files or source control.
>
> The client received only data needed for the current workflow. Internal integration tokens, audit details, policy inputs, and hidden authorization context never went to the browser.
>
> Temporary search and reconciliation payloads had bounded retention. Data no longer needed for the workflow was deleted or minimized according to policy.
>
> The highest-impact mistake would have been logging patient details or credentials into a broadly accessible observability system because that would create an uncontrolled secondary copy.

### Question-by-question answer expectations

#### What was the most sensitive data in the system?

The candidate should identify both user data and operational secrets.

#### How was sensitive data stored, transmitted, displayed, logged, or exported?

A strong answer covers the entire lifecycle and access paths.

#### Were there secrets, tokens, API keys, certificates, or credentials in the flow?

The candidate should explain purpose, ownership, lifetime, and scope.

#### How were secrets managed and rotated?

Strong mechanisms:

* managed secret store;
* workload identity;
* short-lived tokens;
* key versioning;
* rotation automation;
* revocation;
* audit.

#### How did you prevent sensitive data from leaking into logs, analytics, errors, or client responses?

Mechanisms:

* allowlist logging;
* redaction;
* structured errors;
* schema review;
* data classification;
* linting;
* test assertions;
* restricted observability access.

#### What data should never be trusted to the client?

Examples:

* authorization decisions;
* secret keys;
* internal policy configuration;
* unfiltered sensitive records;
* server-calculated prices or eligibility without verification;
* audit-only metadata.

#### What data should never be persisted longer than necessary?

Examples:

* access tokens;
* raw uploads;
* one-time codes;
* temporary exports;
* transient integration payloads;
* sensitive free text.

#### What sensitive-data mistake would have had the highest impact?

High-signal answers identify an uncontrolled copy, overbroad access, or irreversible exposure.

### Follow-up probes for the interviewer

* Were logs considered a separate data store?
* How were backups handled?
* Could secrets appear in crash dumps?
* What was the rotation period?
* How did old credentials get revoked?
* Were analytics fields reviewed?
* How was deletion propagated?
* What field was most likely to leak accidentally?

### Weak-answer signals

Watch for answers that:

* say encryption alone solved data protection;
* log full payloads;
* store secrets in source or static config;
* cannot explain rotation;
* expose unnecessary data to clients;
* ignore analytics and backups;
* keep temporary data indefinitely;
* have no data classification or retention reasoning.

---


## D. Abuse cases and threat modeling

* What abuse cases did you consider?
* How could a malicious user misuse the system while still using valid inputs?
* Were there risks around scraping, spam, privilege escalation, data exfiltration, fraud, denial of service, or tenant isolation?
* What rate limits, quotas, validation, monitoring, or approval flows protected against abuse?
* What product feature created the most security risk?
* What attack would be easy to underestimate?
* Did any security control create friction for legitimate users?
* How did you balance usability against abuse prevention?

What this reveals:
Whether they can think beyond accidental misuse and consider deliberate adversarial behavior.

### Clarifying questions a strong candidate may ask

* Should I focus on abuse using valid credentials?
* Would you like one abuse case in depth?
* Should I discuss automated abuse, insider misuse, or both?
* Are you interested in detection as well as prevention?
* Should I explain usability costs of the controls?

These questions show that malicious behavior often uses syntactically valid inputs and legitimate product features.

### Reasoning expected from the candidate

A strong threat-modeling answer should identify:

1. **Asset**
   * What does the attacker want?
2. **Actor**
   * Anonymous user, authenticated user, partner, insider, or compromised service?
3. **Capability**
   * What valid actions can they perform?
4. **Abuse path**
   * How can normal features be combined maliciously?
5. **Impact**
   * Data exposure, fraud, denial, spam, or privilege gain?
6. **Controls**
   * Preventive, detective, and responsive?
7. **Bypass**
   * How might controls be evaded?
8. **Usability cost**
   * What legitimate users experience friction?

### Example of a strong coherent answer

> We considered scraping of clinic availability, appointment hoarding, repeated booking and cancellation to deny access to others, credential stuffing, enumeration of booking identifiers, cross-tenant access, and abuse of support workflows.
>
> A malicious user could use valid requests to search every clinic continuously or reserve scarce slots repeatedly. Inputs would be valid, so schema validation alone would not help.
>
> Controls included per-user and per-IP rate limits, behavior-based quotas, idempotency, booking-attempt monitoring, cancellation-abuse detection, opaque identifiers, and stronger review for high-risk support actions.
>
> We also limited expensive search ranges and result sizes to protect backend capacity. Sensitive endpoints had stricter thresholds than general browsing.
>
> The most underestimated attack was enumeration through differences in error messages. Returning “booking exists but is not yours” would reveal valid identifiers, so unauthorized responses avoided disclosing existence.
>
> Some controls created friction. Strict rate limits could affect families or clinic networks sharing an address. We combined multiple signals and provided support paths rather than relying on one blunt threshold.
>
> We balanced usability and abuse prevention by applying stronger controls to high-impact actions while keeping low-risk browsing accessible.

### Question-by-question answer expectations

#### What abuse cases did you consider?

Strong answers include deliberate misuse, not only malformed input.

#### How could a malicious user misuse the system while still using valid inputs?

Examples:

* scraping;
* hoarding;
* spam;
* enumeration;
* automated account creation;
* repeated cancellation;
* quota evasion;
* business-logic abuse.

#### Were there risks around scraping, spam, privilege escalation, data exfiltration, fraud, denial of service, or tenant isolation?

The candidate should prioritize realistic risks for the product.

#### What rate limits, quotas, validation, monitoring, or approval flows protected against abuse?

A mature answer combines:

* prevention;
* detection;
* response;
* user recovery.

#### What product feature created the most security risk?

High-signal examples:

* bulk export;
* search;
* sharing;
* file upload;
* admin override;
* invitation;
* public link;
* automation.

#### What attack would be easy to underestimate?

Examples:

* identifier enumeration;
* workflow abuse;
* stale authorization;
* support social engineering;
* webhook replay;
* cost amplification;
* resource exhaustion with valid queries.

#### Did any security control create friction for legitimate users?

The candidate should discuss false positives and accessibility or recovery paths.

#### How did you balance usability against abuse prevention?

Strong answers apply controls proportionally and use progressive friction.

### Follow-up probes for the interviewer

* What was the attacker’s goal?
* Could rate limits be evaded?
* Were limits per user, tenant, IP, or operation?
* How were false positives handled?
* What anomaly triggered investigation?
* Could support controls be socially engineered?
* Did errors reveal resource existence?
* Which feature had the highest abuse leverage?

### Weak-answer signals

Watch for answers that:

* equate security with invalid-input rejection;
* cannot identify valid-feature abuse;
* rely only on IP rate limiting;
* ignore insiders and support workflows;
* have no detection or response;
* disclose existence through errors;
* add friction without measuring false positives;
* cannot identify a risky product feature.

---


## E. Compliance, auditability, and security tradeoffs

* Were there auditability, privacy, regulatory, or compliance requirements?
* What actions needed to be logged or attributable?
* How did you make security-sensitive behavior reviewable after the fact?
* Were there data retention, deletion, or consent requirements?
* Where did security requirements conflict with product speed or developer convenience?
* What security tradeoff did the team knowingly accept?
* What security concern was easiest for product teams to overlook?
* What would you improve if the system handled more sensitive data or more external users?

What this reveals:
Whether they understand security as part of system design, product behavior, and operational accountability.

### Clarifying questions a strong candidate may ask

* Should I focus on privacy, auditability, or regulatory constraints?
* Would you like one audit-sensitive workflow in depth?
* Should I discuss retention and deletion mechanics?
* Are you interested in a security-product tradeoff?
* Should I explain what would change for more sensitive use?

These questions show that security requirements shape data models, operations, and product workflows.

### Reasoning expected from the candidate

A strong answer should cover:

1. **Requirement**
   * Legal, regulatory, contractual, policy, or customer expectation?
2. **Sensitive action**
   * What needed attribution or review?
3. **Audit record**
   * Actor, action, resource, time, reason, outcome, and source?
4. **Integrity**
   * Could the audit trail be altered?
5. **Privacy**
   * Consent, minimization, retention, deletion, and access?
6. **Operational review**
   * Who could investigate and how?
7. **Tradeoff**
   * What delivery speed, convenience, or product flexibility was sacrificed?
8. **Future posture**
   * What would need strengthening at higher sensitivity or exposure?

A mature answer avoids claiming compliance based solely on technical controls. The candidate should describe the engineering requirements they implemented and avoid legal conclusions beyond their role.

### Example of a strong coherent answer

> The system had privacy and auditability requirements because it handled patient-related scheduling data.
>
> Security-sensitive actions included login events, booking creation and cancellation, support overrides, permission changes, export actions, secret access, and configuration changes.
>
> Audit records captured the actor, tenant, action, target resource, timestamp, reason where required, outcome, and correlation ID. Audit events were written through a restricted path and had limited mutation capability.
>
> Retention differed by data type. Operational booking history was retained according to business and policy needs, while temporary tokens, search payloads, and debug data had much shorter lifetimes.
>
> Deletion workflows needed to account for primary stores, caches, exports, and analytical copies. Some records could be removed, while others required minimization or retention due to operational obligations.
>
> Security requirements slowed some product work. Support initially wanted unrestricted search across patients for speed, but we required purpose-limited access, stronger logging, and narrower result display.
>
> A tradeoff we accepted was allowing bounded session lifetime for usability rather than requiring reauthentication for every action. We required step-up authentication for especially sensitive operations.
>
> If the system served more external users or handled more clinical detail, I would strengthen threat modeling, data segregation, access reviews, key management, penetration testing, and security monitoring.

### Question-by-question answer expectations

#### Were there auditability, privacy, regulatory, or compliance requirements?

The candidate should describe concrete engineering implications rather than naming frameworks only.

#### What actions needed to be logged or attributable?

Examples:

* access to sensitive records;
* permission changes;
* exports;
* destructive actions;
* support overrides;
* consent changes;
* secret access;
* admin configuration.

#### How did you make security-sensitive behavior reviewable after the fact?

Strong mechanisms:

* immutable or protected audit records;
* correlation IDs;
* actor context;
* reason capture;
* searchable operational tooling;
* retention;
* alerting.

#### Were there data retention, deletion, or consent requirements?

The candidate should explain data classification, lifecycle, and propagation to derived systems.

#### Where did security requirements conflict with product speed or developer convenience?

High-signal examples:

* admin access;
* production debugging;
* logging restrictions;
* approval flows;
* slower integration;
* stronger identity requirements;
* retention constraints.

#### What security tradeoff did the team knowingly accept?

A strong answer names risk, rationale, containment, and revisit condition.

#### What security concern was easiest for product teams to overlook?

Examples:

* secondary data copies;
* enumeration;
* support access;
* auditability;
* deletion propagation;
* partner trust;
* session revocation.

#### What would you improve if the system handled more sensitive data or more external users?

Strong answers prioritize controls based on increased threat and consequence.

### Follow-up probes for the interviewer

* Were audit records protected from mutation?
* Who could view them?
* How was deletion verified?
* What data could not be deleted and why?
* Was consent versioned?
* What required step-up authentication?
* What product request was narrowed?
* What accepted risk had a revisit trigger?

### Weak-answer signals

Watch for answers that:

* equate compliance with a checklist;
* log actions without actor or outcome;
* ignore audit integrity;
* cannot explain deletion across derived stores;
* retain everything indefinitely;
* say security never affected delivery;
* cannot name an accepted tradeoff;
* make legal claims unsupported by their role.

---

# Cross-section answer framework

Candidates can use this structure to answer most security questions:

1. **Identify the asset**
   * What data, capability, or user outcome must be protected?
2. **Identify the actor**
   * Anonymous user, authenticated user, partner, service, or operator?
3. **Draw the trust boundary**
   * Where does data or authority cross?
4. **State the threat**
   * Spoofing, tampering, disclosure, abuse, privilege escalation, or denial?
5. **Choose the control**
   * Authentication, authorization, validation, isolation, rate limit, encryption, audit, or approval?
6. **Protect the lifecycle**
   * Collection, storage, transit, logging, export, retention, and deletion.
7. **Test the negative path**
   * What direct or cross-tenant misuse should fail?
8. **Cover abuse**
   * How can valid features be used maliciously?
9. **State the tradeoff**
   * What usability, speed, or operational cost does the control add?
10. **Reflect**
   * What would need strengthening with more sensitive data or broader exposure?

A strong answer treats security as a design property across boundaries and workflows, not as a final validation layer.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* identifies trust boundaries beyond the public network edge;
* treats clients, partners, services, and operators with appropriate partial trust;
* separates authentication from authorization;
* enforces resource and tenant access server-side;
* designs least-privilege service access;
* explains sensitive-data handling across the lifecycle;
* manages and rotates secrets safely;
* prevents leakage into logs, analytics, and errors;
* identifies abuse using valid product features;
* uses proportional prevention, detection, and response controls;
* explains auditability, retention, and deletion implications;
* discusses security-product tradeoffs honestly.

## Mixed signal

The candidate:

* understands trust and access control but weakly covers internal services;
* protects primary data but overlooks logs or analytics;
* identifies abuse but relies heavily on basic rate limiting;
* has audit records but weak retention or deletion reasoning;
* understands security costs but lacks concrete testing examples.

## Weak signal

The candidate:

* trusts first-party clients or internal networks;
* conflates authentication and authorization;
* relies on frontend checks;
* uses client-supplied tenant or role context;
* stores long-lived secrets insecurely;
* logs sensitive payloads;
* cannot identify valid-input abuse;
* has no cross-tenant negative tests;
* treats compliance as a framework label;
* claims security had no effect on product or delivery.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What were the three most important trust boundaries?
2. Which inputs were untrusted?
3. What assumption about the client would have been dangerous?
4. How were authentication and authorization separated?
5. What prevented cross-tenant or cross-user access?
6. What was the most sensitive data?
7. How were secrets managed and rotated?
8. What data was excluded from logs and clients?
9. What valid-feature abuse case mattered most?
10. What control created user friction?
11. Which actions required auditability?
12. What would change with more sensitive data or public exposure?

A strong response should demonstrate explicit trust modeling, server-side authorization, lifecycle data protection, abuse-aware product design, and accountable security operations.
