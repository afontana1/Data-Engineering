# 6. API and contract design

These questions test whether the candidate can design interfaces that are clear, durable, and safe to consume. For a full-stack role, this is especially useful because APIs often reveal whether someone thinks across boundaries instead of only inside one layer.

## Table of contents

- [A. Interface purpose and consumers](#a-interface-purpose-and-consumers)
- [B. Contract shape and usability](#b-contract-shape-and-usability)
- [C. Responses, errors, and edge cases](#c-responses-errors-and-edge-cases)
- [D. Change management and compatibility](#d-change-management-and-compatibility)
- [E. Operational and behavioral concerns](#e-operational-and-behavioral-concerns)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched for available visits, booked or cancelled appointments, and received reminders. The platform exposed APIs to a patient web application, internal clinic tools, background workers, notification services, analytics consumers, and vendor integration adapters. Clinic scheduling systems remained authoritative for final appointment inventory.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can explain who an interface serves, how the contract guides correct use, how errors and partial failure are represented, how compatibility is preserved, and how operational behavior is encoded.



## A. Interface purpose and consumers

* What were the major interfaces in the system?
* Who or what consumed those interfaces?
* Were the consumers frontend clients, internal services, external partners, background jobs, or other teams?
* What did each consumer need from the API?
* How did consumer needs shape the interface?
* Did the API expose domain concepts, UI-specific shapes, or implementation details?
* Which interface was most important to get right?
* What would a consumer misunderstand if the contract was poorly designed?

What this reveals:
Whether they think of APIs as boundaries between people, systems, and responsibilities rather than just endpoints.

### Clarifying questions a strong candidate may ask

* Should I focus on external APIs, internal service contracts, or both?
* Would you like the most important interface in depth or the whole interface landscape?
* Should I include event contracts and background-job messages?
* Are you interested in logical consumers or specific client applications?
* Should I explain the contract as originally designed or how it evolved?

These questions show that an interface can be synchronous, asynchronous, internal, external, human-facing, or machine-facing.

### Reasoning expected from the candidate

A strong candidate should explain:

1. **Purpose**
   * What capability did the interface expose?
2. **Consumer**
   * Who called or consumed it?
3. **Consumer constraints**
   * Latency, platform, expertise, release cadence, and compatibility needs?
4. **Contract level**
   * Domain-oriented, task-oriented, UI-oriented, or infrastructure-oriented?
5. **Ownership**
   * Who controlled changes?
6. **Misuse risk**
   * What could a caller misunderstand or do incorrectly?
7. **Priority**
   * Which interface carried the greatest product or system risk?

A mature answer distinguishes between the interface a user-facing client needs and the interface an internal service or event consumer needs.

### Example of a strong coherent answer

> The system had four major interface types.
>
> The patient web application used a task-oriented HTTP API for searching, booking, cancellation, and status. Those contracts were optimized around user workflows rather than exposing our internal database model.
>
> Clinic support tools used a more operational API that exposed workflow history, reconciliation state, and manual retry actions. Those consumers needed diagnostic detail that would have been inappropriate for the patient client.
>
> Internal services consumed domain events such as BookingConfirmed and BookingCancelled. Notification and analytics consumers depended on those events but did not need access to booking workflow internals.
>
> Vendor adapters implemented an internal scheduling-provider contract. That interface normalized vendor-specific availability, booking, cancellation, and error behavior into capabilities the core system understood.
>
> The patient booking contract was the most important to get right because it crossed the trust boundary, directly affected user experience, and had retry and timeout ambiguity. A poorly designed contract could lead clients to treat a request as confirmed when it was only accepted for processing.

### Question-by-question answer expectations

#### What were the major interfaces in the system?

Strong answers include more than REST endpoints.

Possible interfaces:

* public HTTP API;
* internal RPC;
* event schema;
* queue message;
* webhook;
* batch file;
* command-line or operator interface;
* database contract;
* library boundary.

The candidate should identify which were stable contracts versus implementation details.

#### Who or what consumed those interfaces?

The answer should identify:

* frontend applications;
* mobile clients;
* internal services;
* external partners;
* background workers;
* support tools;
* analytics consumers;
* operators.

#### Were the consumers frontend clients, internal services, external partners, background jobs, or other teams?

A strong candidate explains how release independence and trust level differed among consumers.

For example:

> The mobile client released slowly, so compatibility mattered more than for an internal service we controlled.

#### What did each consumer need from the API?

The candidate should identify differences in:

* data shape;
* latency;
* detail;
* authorization;
* diagnostics;
* batch support;
* stability;
* failure semantics.

#### How did consumer needs shape the interface?

Strong answers connect need to contract choice.

Examples:

* mobile bandwidth → smaller payloads;
* support tooling → richer diagnostics;
* external partners → strict versioning;
* UI workflow → task-oriented endpoint;
* event consumers → immutable facts.

#### Did the API expose domain concepts, UI-specific shapes, or implementation details?

A mature answer explains the balance.

Good design may expose domain concepts while introducing UI-specific aggregation at the edge, such as a backend-for-frontend. It should avoid leaking internal table structure unless that is intentional.

#### Which interface was most important to get right?

The candidate should choose one and explain risk.

Possible reasons:

* external compatibility;
* financial correctness;
* authorization;
* workflow finality;
* broad consumer count;
* difficult migration.

#### What would a consumer misunderstand if the contract was poorly designed?

High-signal examples:

* accepted versus completed;
* stale versus authoritative data;
* optional versus absent;
* retryable versus permanent failure;
* command versus event;
* page token stability;
* ownership or tenant scope.

### Follow-up probes for the interviewer

* Which consumer released most slowly?
* Which contract had the most consumers?
* What data was intentionally hidden?
* Did one API try to serve incompatible consumer needs?
* Which interface crossed the strongest trust boundary?
* What interface was internal but became effectively public?
* How did consumers discover the contract?
* Which interface would be hardest to replace?

### Weak-answer signals

Watch for answers that:

* treat APIs as only endpoint lists;
* cannot name consumers;
* expose storage models directly without rationale;
* claim one contract served every consumer equally well;
* ignore event or background-job contracts;
* cannot identify misuse risks;
* confuse internal implementation with stable interface;
* do not account for independent release cycles.

---


## B. Contract shape and usability

* How did you design the API or service contract?
* What did you optimize for: simplicity, flexibility, explicitness, consistency, or backward compatibility?
* How did clients know how to use the system correctly?
* What mistakes could consumers easily make?
* How did the API guide callers toward correct usage?
* Were there defaults, required fields, validation rules, or constraints that needed to be especially clear?
* What part of the contract was hardest to explain?
* If you had to make the API public, what would you redesign?

What this reveals:
Whether they understand that a good contract is not just technically functional, but understandable, hard to misuse, and aligned with consumer needs.

### Clarifying questions a strong candidate may ask

* Should I focus on request and response structure or the broader behavioral contract?
* Would you like one endpoint or message type in depth?
* Are you interested in naming, validation, defaults, or discoverability?
* Should I compare internal and public API usability?
* Should I include examples of misuse the contract prevented?

These questions show that contract design includes semantics, constraints, and behavior, not just fields.

### Reasoning expected from the candidate

A strong candidate should explain:

1. **Task model**
   * What user or system action did the contract represent?
2. **Resource and command semantics**
   * Was it querying state, requesting change, or reporting an event?
3. **Required information**
   * What was mandatory, optional, defaulted, or inferred?
4. **Validation**
   * What rules were enforced and where?
5. **Clarity**
   * Could a caller predict behavior from names and schema?
6. **Misuse resistance**
   * Did the contract make unsafe actions difficult?
7. **Consistency**
   * Did similar operations behave similarly?
8. **Public readiness**
   * What assumptions were acceptable internally but not externally?

### Example of a strong coherent answer

> We designed the patient APIs around tasks rather than internal entities. For example, booking was `POST /bookings` with an availability reference, patient context, appointment type, and idempotency key. The client did not send internal workflow status or vendor codes.
>
> We optimized for explicitness and consistency. Required fields were schema-validated, date-time values included time zones, identifiers were opaque strings, and optional fields had documented absence semantics. We avoided boolean combinations that could create invalid requests.
>
> The API guided callers by separating search references from confirmed booking identifiers. A search result could be submitted for booking, but it was not itself a booking. Confirmation returned a booking resource with an explicit status.
>
> The easiest mistake was retrying a timed-out booking without an idempotency key. We made the key required for mutation requests and documented that the same key represented the same logical operation.
>
> Internally, some APIs assumed shared knowledge of clinic configuration. If the API were public, I would remove those assumptions, add stronger capability discovery, formalize rate limits and deprecation, and make error documentation more complete.

### Question-by-question answer expectations

#### How did you design the API or service contract?

A strong answer covers:

* use cases;
* resource or command model;
* field naming;
* identifiers;
* validation;
* behavior;
* consistency;
* documentation.

#### What did you optimize for?

The candidate should rank qualities such as:

* simplicity;
* explicitness;
* flexibility;
* consistency;
* backward compatibility;
* low latency;
* evolvability;
* ease of generation.

They should explain the cost of the priority.

#### How did clients know how to use the system correctly?

Good mechanisms include:

* schema;
* examples;
* generated clients;
* type definitions;
* documentation;
* validation errors;
* discoverable resource links;
* capability endpoints;
* contract tests.

#### What mistakes could consumers easily make?

High-signal examples:

* duplicate mutation;
* mixing IDs from different scopes;
* using stale version data;
* omitting timezone;
* interpreting empty and absent identically;
* retrying non-idempotent operations;
* requesting unbounded results.

#### How did the API guide callers toward correct usage?

Strong mechanisms:

* required idempotency keys;
* separate commands;
* typed enums;
* opaque identifiers;
* precondition headers;
* validation;
* narrow permissions;
* bounded pagination;
* explicit status.

#### Were there defaults, required fields, validation rules, or constraints that needed to be especially clear?

The candidate should explain why a default was safe or why explicit input was required.

Ambiguous defaults around time, currency, tenant, or destructive behavior are warning signs.

#### What part of the contract was hardest to explain?

Good answers identify semantic complexity:

* eventual completion;
* partial success;
* capability differences;
* version preconditions;
* freshness;
* polymorphic resources.

#### If you had to make the API public, what would you redesign?

Strong answers may include:

* remove internal assumptions;
* improve stability;
* formalize authentication;
* add versioning;
* standardize errors;
* publish quotas;
* strengthen documentation;
* improve sandbox/testing;
* reduce implementation leakage.

### Follow-up probes for the interviewer

* Why was this a resource instead of a command?
* What did absence mean?
* How were dates and time zones represented?
* Were identifiers stable?
* Could callers construct invalid combinations?
* What behavior was documented but not encoded?
* Did generated clients help or hide complexity?
* What public assumption would fail first?

### Weak-answer signals

Watch for answers that:

* focus only on URL naming;
* have inconsistent field semantics;
* rely on documentation for critical safety;
* use ambiguous booleans or magic strings;
* cannot name likely misuse;
* default sensitive or destructive behavior silently;
* expose vendor or database internals unnecessarily;
* confuse flexibility with accepting arbitrary payloads.

---


## C. Responses, errors, and edge cases

* What response model did you choose, and why?
* What error model did you choose, and why?
* How did clients distinguish validation errors, authorization errors, dependency failures, conflicts, and unexpected failures?
* Were errors designed for machines, humans, or both?
* How did the API behave under partial failure?
* Were there cases where a request could partially succeed?
* What edge cases were important to represent clearly in the contract?
* What would poor error design have made harder for clients?

What this reveals:
Whether they understand that error handling and edge cases are part of the contract, not secondary implementation details.

### Clarifying questions a strong candidate may ask

* Should I describe synchronous errors, asynchronous failures, or both?
* Would you like the machine-readable schema or user-facing presentation?
* Should I focus on partial success and timeout uncertainty?
* Are you interested in HTTP semantics or domain error semantics?
* Should I explain one difficult edge case in depth?

These questions show that error behavior is part of the contract and may outlive the success-path shape.

### Reasoning expected from the candidate

A strong candidate should distinguish:

* **transport failure:** request did not complete at the protocol level;
* **validation error:** caller supplied invalid input;
* **authorization error:** caller is not permitted;
* **conflict:** current state prevents the operation;
* **dependency failure:** downstream system failed;
* **uncertain outcome:** completion is unknown;
* **domain rejection:** valid request cannot be fulfilled;
* **unexpected failure:** unclassified internal problem.

A mature error model includes:

1. stable machine-readable code;
2. human-readable message;
3. correlation or request identifier;
4. field-level details where appropriate;
5. retry guidance;
6. distinction between permanent and transient;
7. safe exposure of internal details;
8. partial-success representation.

### Example of a strong coherent answer

> Success responses returned explicit resource state rather than relying only on HTTP status. A booking creation could return `confirmed`, `rejected`, or `pending_reconciliation` depending on the external outcome.
>
> Errors used a stable code, message, request ID, and optional field details. Validation errors identified the exact fields. Authorization errors did not reveal whether a protected resource existed. Conflicts identified the current resource version or status when safe.
>
> We distinguished dependency failure from uncertain outcome. If the clinic system definitively rejected the booking, the API returned a domain rejection. If it timed out before any evidence of completion, we returned a retryable dependency error. If it timed out after the request may have committed, we returned an accepted booking resource in a pending-reconciliation state rather than encouraging an unsafe retry.
>
> Errors were designed for both machines and humans. Clients switched on stable codes and displayed localized messages. Internal diagnostic detail remained in logs linked by request ID.
>
> Partial success occurred in batch cancellation. Each item returned its own result, while the overall response summarized counts. That prevented one invalid item from hiding successful work.

### Question-by-question answer expectations

#### What response model did you choose, and why?

Strong answers explain:

* resource representation;
* envelope or no envelope;
* status field;
* pagination metadata;
* asynchronous job representation;
* version or ETag;
* consistency.

#### What error model did you choose, and why?

The candidate should describe stable structure and semantics.

Good error fields may include:

* code;
* message;
* details;
* field;
* retryable;
* request ID;
* documentation link.

#### How did clients distinguish validation, authorization, dependency, conflict, and unexpected failures?

A strong answer uses machine-readable categories and appropriate protocol status.

The client should not parse free-text messages.

#### Were errors designed for machines, humans, or both?

A mature answer separates stable code from display text and avoids exposing sensitive internals.

#### How did the API behave under partial failure?

Possible patterns:

* all-or-nothing;
* per-item result;
* accepted job;
* compensation;
* partial resource;
* degraded response.

The candidate should explain why the chosen behavior was safe.

#### Were there cases where a request could partially succeed?

The answer should identify:

* batch operations;
* multi-resource workflow;
* fan-out;
* external side effects;
* asynchronous consumers.

Strong candidates explain observability and retry semantics.

#### What edge cases were important to represent clearly in the contract?

Examples:

* duplicate request;
* stale version;
* expired token;
* vanished inventory;
* empty result;
* missing optional data;
* timeout after commit;
* out-of-order update;
* unsupported capability.

#### What would poor error design have made harder for clients?

Possible consequences:

* unsafe retry;
* misleading user messages;
* excessive support tickets;
* brittle parsing;
* inability to distinguish conflict from outage;
* hidden partial completion;
* poor monitoring.

### Follow-up probes for the interviewer

* Was the error retryable?
* How did the client know?
* Did authorization errors leak existence?
* What did a timeout mean?
* Could the client safely repeat the request?
* How was partial success reconciled?
* Were error codes versioned?
* Which error generated the most support volume?

### Weak-answer signals

Watch for answers that:

* return generic 500 errors for everything;
* encode all outcomes in free text;
* encourage retries without idempotency;
* confuse business rejection with system failure;
* expose stack traces or sensitive details;
* cannot represent uncertain outcomes;
* hide partial success;
* use HTTP status alone without stable domain semantics.

---


## D. Change management and compatibility

* How did you handle versioning or contract changes?
* What kinds of changes were backward-compatible?
* What kinds of changes would break clients?
* Did you ever have to support old and new clients at the same time?
* How did you deprecate fields, endpoints, or behaviors?
* How did consumers learn about contract changes?
* Were there contract tests, schema validation, documentation, or generated clients?
* What API decision was hardest to change later?

What this reveals:
Whether they understand that APIs become durable commitments and that changing them safely requires discipline.

### Clarifying questions a strong candidate may ask

* Should I focus on API versioning, event versioning, or both?
* Would you like one breaking change and its migration?
* Should I discuss internal clients as well as external ones?
* Are you interested in schema compatibility or behavioral compatibility?
* Should I explain how deprecation was monitored and completed?

These questions show that compatibility includes meaning and behavior, not only field presence.

### Reasoning expected from the candidate

A strong answer should cover:

1. **Consumer inventory**
   * Who depended on the contract?
2. **Compatibility rules**
   * What changes were safe?
3. **Version strategy**
   * URL, header, schema, event type, or negotiated capability?
4. **Rollout**
   * Could old and new versions coexist?
5. **Deprecation**
   * How were consumers notified and measured?
6. **Testing**
   * How was contract drift detected?
7. **Behavioral semantics**
   * Did the meaning remain stable?
8. **Hardest commitment**
   * What early decision became difficult to change?

### Example of a strong coherent answer

> We preferred additive evolution within a major version. Adding optional response fields or new enum values was generally safe only if clients were written to ignore unknown fields and handle unknown values defensively.
>
> Removing fields, changing required input, changing identifier meaning, or altering retry semantics was breaking even when the JSON shape looked similar.
>
> Mobile clients and external partners could remain on old versions for months, so we supported old and new behavior concurrently. We used versioned routes for major behavioral changes and versioned event types when semantics changed.
>
> Deprecation involved documentation, consumer-owner notification, usage dashboards, deadlines, and warning headers. We did not remove an endpoint until traffic had reached zero or an explicit exception had been resolved.
>
> We used schema validation, provider and consumer contract tests, generated clients for some languages, and replay tests against recorded payloads.
>
> The hardest decision to change was using a clinic-specific identifier as though it were globally stable. Later integrations required a composite identity, so we had to introduce opaque platform IDs while supporting the old field during migration.

### Question-by-question answer expectations

#### How did you handle versioning or contract changes?

The candidate should explain whether versioning was:

* explicit;
* additive;
* negotiated;
* event-based;
* date-based;
* compatibility-first.

#### What kinds of changes were backward-compatible?

Usually:

* adding optional fields;
* adding endpoints;
* widening accepted input carefully;
* adding non-breaking metadata.

But even additive changes can break fragile clients, so strong candidates discuss assumptions.

#### What kinds of changes would break clients?

Examples:

* removing or renaming fields;
* changing type;
* narrowing validation;
* changing default;
* altering ordering;
* changing error semantics;
* adding enum values to exhaustive clients;
* changing pagination stability.

#### Did you ever have to support old and new clients at the same time?

A strong answer explains routing, dual behavior, feature negotiation, or compatibility layers.

#### How did you deprecate fields, endpoints, or behaviors?

Good process:

1. announce;
2. document replacement;
3. instrument usage;
4. warn;
5. migrate;
6. verify;
7. remove.

#### How did consumers learn about contract changes?

Mechanisms include:

* changelog;
* schema registry;
* developer portal;
* release notes;
* direct ownership notifications;
* deprecation headers;
* migration guides.

#### Were there contract tests, schema validation, documentation, or generated clients?

The candidate should explain what each mechanism caught and where it was insufficient.

#### What API decision was hardest to change later?

High-signal examples:

* identifier semantics;
* pagination;
* error model;
* timestamp meaning;
* required fields;
* event ownership;
* null versus absent;
* sync versus async completion.

### Follow-up probes for the interviewer

* Did clients ignore unknown fields?
* How were enum additions handled?
* Was behavior versioned as well as schema?
* How did you find all consumers?
* What happened to abandoned clients?
* Did generated clients slow adoption?
* How long did deprecation take?
* What compatibility promise was accidental?

### Weak-answer signals

Watch for answers that:

* say “we just made a v2” with no migration story;
* define compatibility only by JSON shape;
* remove fields without usage data;
* assume internal clients can all upgrade together;
* have no consumer inventory;
* rely on manual testing only;
* change semantics under the same contract;
* cannot identify a hard-to-change decision.

---


## E. Operational and behavioral concerns

* Were there idempotency concerns?
* How did you think about retries, duplicate requests, or timeout uncertainty?
* How did you design pagination, filtering, sorting, partial updates, or batch operations?
* Were there rate limits, authorization boundaries, or tenant boundaries expressed through the API?
* Did the API need to support high-volume or latency-sensitive use cases?
* How did the contract protect the backend from expensive or unsafe requests?
* What behavior did clients rely on that was not obvious from the endpoint shape?
* What operational issue would a poorly designed API have created?

What this reveals:
Whether they understand that APIs encode behavior, reliability expectations, performance constraints, and safety boundaries.

### Clarifying questions a strong candidate may ask

* Should I focus on idempotency, pagination, rate limits, or the full operational contract?
* Would you like mutation behavior or high-volume read behavior in depth?
* Should I include tenant and authorization boundaries?
* Are you interested in client-visible guarantees or backend-protection mechanisms?
* Should I discuss behavior that was implicit and later documented?

These questions show that operational behavior is part of the API, even when it is not obvious from the payload.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Retry semantics**
   * Which operations were safe to repeat?
2. **Idempotency**
   * How was one logical operation identified?
3. **Timeout uncertainty**
   * Could the server have completed after the client gave up?
4. **Collection behavior**
   * Pagination, filtering, sorting, and stability?
5. **Mutation semantics**
   * Full replacement, partial update, preconditions, and conflicts?
6. **Protection**
   * Rate limits, quotas, bounded requests, and expensive-query controls?
7. **Security boundaries**
   * Tenant, role, and resource ownership?
8. **Hidden guarantees**
   * Ordering, freshness, retention, or eventual completion?

### Example of a strong coherent answer

> All externally visible mutation requests required an idempotency key. We stored the key with the logical operation and returned the original result for duplicates. The key was scoped to tenant and endpoint so unrelated operations could not collide.
>
> We treated client timeout as uncertainty, not proof of failure. Clients could retry with the same key or query booking status. For outcomes that remained uncertain because of an external vendor, the resource entered reconciliation.
>
> Search used cursor-based pagination because result sets changed frequently and offset pagination produced duplicates and skips. Sort options were limited to indexed fields. Filters were validated and bounded to prevent expensive arbitrary queries.
>
> Partial updates used explicit patch operations and version preconditions. If a client updated stale state, the API returned a conflict rather than silently overwriting a newer change.
>
> Rate limits were applied by tenant and operation. Search had higher quotas than booking, while expensive exports were asynchronous. Authorization was enforced on the server using tenant and ownership context; client-side filtering was not trusted.
>
> One behavior clients relied on but that was initially under-documented was that search results were not reservations. We made that explicit after clients started displaying countdown-like language that implied stronger guarantees than the API provided.

### Question-by-question answer expectations

#### Were there idempotency concerns?

The candidate should identify non-idempotent operations such as:

* payment;
* booking;
* message send;
* job creation;
* inventory reservation;
* external side effect.

They should explain key scope, retention, and result replay.

#### How did you think about retries, duplicate requests, or timeout uncertainty?

Strong answers distinguish:

* safe retry;
* same logical operation;
* server completion after timeout;
* duplicate side effects;
* reconciliation.

#### How did you design pagination, filtering, sorting, partial updates, or batch operations?

The candidate should discuss:

* cursor versus offset;
* stable sort;
* bounded page size;
* filter allowlist;
* partial failure;
* version preconditions;
* batch size limits.

#### Were there rate limits, authorization boundaries, or tenant boundaries expressed through the API?

A mature answer explains both contract and enforcement.

Examples:

* tenant-scoped IDs;
* quotas;
* permissions;
* ownership checks;
* non-disclosing authorization errors.

#### Did the API need to support high-volume or latency-sensitive use cases?

The candidate should connect operational requirements to:

* payload size;
* caching;
* async jobs;
* streaming;
* compression;
* batching;
* precomputation.

#### How did the contract protect the backend from expensive or unsafe requests?

Strong mechanisms:

* bounded ranges;
* pagination;
* query complexity limits;
* asynchronous export;
* rate limiting;
* validation;
* quotas;
* preconditions;
* command-specific endpoints.

#### What behavior did clients rely on that was not obvious from the endpoint shape?

Examples:

* ordering;
* freshness;
* idempotency retention;
* status finality;
* event delivery;
* default filters;
* timeout behavior.

Strong candidates recognize undocumented behavior as a contract risk.

#### What operational issue would a poorly designed API have created?

Possible consequences:

* retry storms;
* duplicate work;
* unbounded queries;
* noisy neighbors;
* data leakage;
* inconsistent clients;
* difficult incident diagnosis;
* expensive migrations.

### Follow-up probes for the interviewer

* How long were idempotency keys retained?
* What was the cursor stability guarantee?
* Could filters cause table scans?
* How were batch failures represented?
* What happened when a tenant exceeded quota?
* Did retries amplify outages?
* Were partial updates conflict-safe?
* Which implicit behavior became accidental contract?

### Weak-answer signals

Watch for answers that:

* say POST requests cannot be retried;
* use request IDs as idempotency keys without logical scoping;
* treat timeout as definite failure;
* expose unbounded list endpoints;
* use offset pagination without considering changing datasets;
* trust client-side authorization;
* allow arbitrary sorting or filtering without cost controls;
* ignore noisy-neighbor and retry-storm behavior.

---

# Cross-section answer framework

Candidates can use this structure to answer most API and contract questions:

1. **Identify the consumer**
   * Who uses the interface, and what constraints do they have?
2. **Define the task**
   * What query, command, event, or workflow does the contract represent?
3. **Explain the shape**
   * Required fields, identifiers, validation, defaults, and response state.
4. **Describe misuse prevention**
   * How does the contract guide callers toward correct behavior?
5. **Define errors**
   * How are validation, authorization, conflicts, dependency failures, and uncertainty represented?
6. **Explain compatibility**
   * What changes are safe, and how do old and new consumers coexist?
7. **Cover operational behavior**
   * Idempotency, retries, pagination, rate limits, and tenant isolation.
8. **Reflect**
   * Which contract decision became hardest to change?

A strong answer treats the interface as a durable behavioral agreement between independently changing parties.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* identifies consumers and their distinct needs;
* explains interfaces by purpose rather than endpoint count;
* uses domain- or task-oriented contracts intentionally;
* makes misuse difficult through structure and validation;
* distinguishes accepted, completed, rejected, and uncertain outcomes;
* provides stable machine-readable error semantics;
* understands partial success;
* explains backward and behavioral compatibility;
* has a deprecation and consumer-migration strategy;
* understands idempotency and timeout uncertainty;
* designs bounded pagination and query behavior;
* enforces tenant and authorization boundaries server-side;
* recognizes implicit behavior as contract risk.

## Mixed signal

The candidate:

* designs clear success-path contracts but weak error semantics;
* understands consumers but serves several through one awkward interface;
* discusses versioning but not migration;
* knows idempotency conceptually but cannot explain storage or scoping;
* uses pagination and rate limits without explaining guarantees;
* has documentation but limited contract testing.

## Weak signal

The candidate:

* treats APIs as URL naming exercises;
* exposes storage implementation directly without rationale;
* relies on free-text errors;
* cannot distinguish domain rejection from dependency failure;
* has no safe retry story;
* changes contracts without consumer inventory;
* assumes all clients update together;
* exposes unbounded or expensive requests;
* trusts client-side authorization;
* cannot identify an accidental contract.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What were the three most important interfaces?
2. Who consumed each one?
3. Which interface was hardest to get right?
4. Did the contract expose domain tasks, UI shapes, or implementation details?
5. What misuse was most likely?
6. How did the contract prevent it?
7. What did a successful mutation response mean?
8. How were validation, conflict, dependency, and unexpected errors distinguished?
9. What happened after a client timeout?
10. How were old and new clients supported?
11. What operational limits or authorization boundaries were encoded?
12. Which API decision would you redesign today?

A strong response should make the interface understandable as a contract among consumers, domain behavior, reliability expectations, and long-term compatibility.
