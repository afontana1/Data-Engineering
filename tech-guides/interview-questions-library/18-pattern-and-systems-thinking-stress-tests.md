# 18. Pattern- and systems-thinking stress tests

These questions are useful when you want to distinguish seniority without running a formal design exercise. They force the candidate to reason across boundaries, abstractions, invariants, tradeoffs, and system-wide consequences.

## Table of contents

- [A. Cross-cutting concerns and system-wide consistency](#a-cross-cutting-concerns-and-system-wide-consistency)
- [B. Local choices with system-wide consequences](#b-local-choices-with-system-wide-consequences)
- [C. Invariants, domain concepts, and hidden structure](#c-invariants-domain-concepts-and-hidden-structure)
- [D. Abstractions, optionality, and pattern judgment](#d-abstractions-optionality-and-pattern-judgment)
- [E. Senior-level tradeoff judgment](#e-senior-level-tradeoff-judgment)

## How to use this section

This chapter is intended to function as both an interviewer stress-test guide and a candidate preparation resource.

The examples below continue the same hypothetical project used throughout the library:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched for appointments, booked or cancelled visits, and received reminders. The platform included a web client, backend APIs, a normalized availability read model, a durable booking workflow, external clinic integrations, background workers, events, support tooling, and shared security and observability mechanisms.

These questions are most useful after a candidate has already explained the architecture. The interviewer can then use one question to test whether the candidate can connect a local implementation detail to system-wide behavior, identify a central invariant, explain where an abstraction preserves optionality, or expose a subtle tradeoff.

A strong candidate does not need to produce the same answer as the interviewer. The important signal is whether they reason across components, users, operators, time horizons, and failure modes rather than discussing one module in isolation.



## A. Cross-cutting concerns and system-wide consistency

* What is one cross-cutting concern in this system, and how was it handled consistently?
* Where did logging, auth, validation, retries, tracing, caching, metrics, or auditing cut across multiple components?
* Where was consistency important across the codebase or architecture?
* How did you avoid scattering the same concern everywhere?
* Where did centralizing a concern help?
* Where did centralizing a concern make behavior harder to see?
* What cross-cutting concern would become painful as the system grew?
* What would a junior engineer likely implement inconsistently?

What this reveals:
Whether they can recognize concerns that span the system and reason about how to handle them without creating hidden complexity.

### Clarifying questions a strong candidate may ask

* Should I focus on one cross-cutting concern in depth?
* Would you like infrastructure concerns or domain-wide policy?
* Should I compare centralized and explicit behavior?
* Are you interested in how the concern evolved with scale?
* Should I include where consistency failed?

These questions show that cross-cutting concerns require both uniformity and visibility.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Concern**
   * What behavior spans multiple components?
2. **Scope**
   * Which clients, services, jobs, or data paths participate?
3. **Consistency requirement**
   * What must behave the same everywhere?
4. **Mechanism**
   * Middleware, policy layer, wrapper, library, interceptor, framework hook, or shared contract?
5. **Explicit decision**
   * What still needs to remain visible at the call site?
6. **Failure risk**
   * What inconsistency would cause user, security, or operational problems?
7. **Hidden behavior**
   * What did centralization make harder to understand?
8. **Growth pressure**
   * What becomes painful as the system expands?

A mature answer distinguishes between:

* centralizing repetitive mechanics;
* keeping domain-sensitive decisions explicit;
* standardizing semantics without creating global magic.

### Example of a strong coherent answer

> Authorization was one important cross-cutting concern. Every patient, clinic staff, support, and service action needed identity, tenant scope, and resource-level policy.
>
> Authentication parsing and tenant-context establishment were centralized in middleware because those mechanics were uniform. Resource-specific authorization remained explicit in domain handlers because the decision depended on booking ownership, clinic assignment, workflow state, and action type.
>
> We used shared policy helpers and a common decision model so denial semantics, audit fields, and metrics stayed consistent.
>
> Centralization helped prevent endpoints from forgetting baseline checks and gave us one place to add trace and audit context. It became dangerous when engineers assumed middleware had completed all authorization. We addressed that with explicit policy calls and negative integration tests.
>
> As the system grew, authorization exceptions for support tooling would have become painful if represented as ad hoc role checks. We moved toward purpose-specific capabilities and audited override policies.
>
> A less experienced engineer might hide buttons in the frontend and assume that was sufficient, or scatter slightly different tenant checks through each controller.

### Question-by-question answer expectations

#### What is one cross-cutting concern in this system, and how was it handled consistently?

Strong examples:

* authentication;
* authorization;
* validation;
* tracing;
* logging;
* retries;
* rate limiting;
* caching;
* transactions;
* auditing;
* feature flags.

The candidate should identify the common semantic contract.

#### Where did logging, auth, validation, retries, tracing, caching, metrics, or auditing cut across multiple components?

The answer should identify concrete paths and boundaries.

#### Where was consistency important across the codebase or architecture?

Examples:

* error taxonomy;
* request identity;
* tenant isolation;
* retry timing;
* sensitive-data redaction;
* audit attribution;
* cache freshness semantics;
* transaction handling.

#### How did you avoid scattering the same concern everywhere?

Strong mechanisms include:

* shared infrastructure wrapper;
* policy object;
* middleware;
* generated client;
* common schema;
* framework extension;
* test fixture;
* lint or static rule.

#### Where did centralizing a concern help?

Benefits may include:

* fewer omissions;
* standardized telemetry;
* easier policy changes;
* consistent security;
* shared operational controls.

#### Where did centralizing a concern make behavior harder to see?

High-signal examples:

* invisible retries;
* hidden transactions;
* automatic cache reads;
* swallowed exceptions;
* authorization assumed rather than shown;
* framework magic.

#### What cross-cutting concern would become painful as the system grew?

The candidate should identify a concern whose cost increases with services, teams, tenants, or policies.

#### What would a junior engineer likely implement inconsistently?

Good answers identify a common category mistake rather than criticizing individuals.

### Follow-up probes for the interviewer

* What remained explicit at the call site?
* Could a component bypass the shared mechanism?
* What behavior became invisible?
* How did you test consistency?
* Was there one owner for the concern?
* What happened across async boundaries?
* Which exception became a maintenance problem?
* How would the mechanism change with more services?

### Weak-answer signals

Watch for answers that:

* centralize everything without discussing hidden behavior;
* scatter critical policy through many handlers;
* confuse shared utilities with consistent semantics;
* retry automatically without operation knowledge;
* hide transaction or authorization boundaries;
* cannot identify a growth pressure;
* treat frontend checks as security enforcement;
* have no way to test system-wide consistency.

---


## B. Local choices with system-wide consequences

* Where did local optimizations create system-wide complexity?
* Where did a simple local decision make another team’s or component’s job harder?
* What small design choice had surprisingly large consequences?
* Where did one component push complexity onto another?
* What looked like an implementation detail but became an architectural issue?
* Where did the system optimize one path at the expense of another?
* Who paid the cost of the local decision?
* What would you change to make the global behavior cleaner?

What this reveals:
Whether they understand that local implementation choices can reshape the behavior, cost, and complexity of the whole system.

### Clarifying questions a strong candidate may ask

* Should I focus on a performance, API, or data decision?
* Would you like the consequence across teams or components?
* Should I explain who benefited and who paid?
* Are you interested in a decision that later became architectural?
* Should I include how the global behavior was cleaned up?

These questions show that local decisions should be evaluated by their externalized costs.

### Reasoning expected from the candidate

A strong answer should map:

1. **Local choice**
   * What optimization or simplification was made?
2. **Local benefit**
   * What became faster, easier, or cheaper?
3. **Externalized cost**
   * What another component, team, user, or operator had to absorb?
4. **Propagation**
   * How did the choice spread through contracts, data, or operations?
5. **Architectural effect**
   * Did the decision become difficult to reverse?
6. **Cost owner**
   * Who paid now and over time?
7. **Detection**
   * When did the system-wide consequence become visible?
8. **Correction**
   * How could the global behavior be improved?

A mature candidate recognizes that:

* a local performance improvement can create global staleness;
* a simpler producer can make every consumer complex;
* a flexible API can push validation onto clients;
* a database convenience can create organization-wide coupling.

### Example of a strong coherent answer

> An early local optimization let each vendor adapter return its native appointment-type codes and pushed mapping into the search layer.
>
> That made each adapter faster to implement, but it externalized complexity. Search, booking, analytics, and support tooling all developed their own mappings and fallback behavior.
>
> What looked like a serialization detail became an architectural issue because the external codes leaked into stored events and client-visible payloads.
>
> The integration team benefited initially. Every downstream owner paid the long-term cost through duplicated logic, inconsistent behavior, and harder vendor replacement.
>
> We corrected it by introducing a normalized domain type at the adapter boundary, migrating stored mappings, and adding contract tests. Vendor-native values remained available only as diagnostic metadata.
>
> The lesson was that translation belongs where foreign concepts enter the system. Keeping the local adapter “simple” made the global system much harder.

### Question-by-question answer expectations

#### Where did local optimizations create system-wide complexity?

Examples:

* per-service cache;
* denormalized payload;
* custom retry;
* direct database access;
* local event schema;
* client-side aggregation;
* broad shared library.

#### Where did a simple local decision make another team’s or component’s job harder?

The candidate should identify both parties and the transferred work.

#### What small design choice had surprisingly large consequences?

High-signal examples:

* nullable field semantics;
* identifier format;
* timestamp timezone;
* event naming;
* default timeout;
* pagination choice;
* status enum;
* cache key scope.

#### Where did one component push complexity onto another?

Examples:

* producer sends raw data;
* backend exposes internal errors;
* frontend orchestrates services;
* platform requires every team to implement retry logic;
* shared library imposes coordinated upgrades.

#### What looked like an implementation detail but became an architectural issue?

Good answers identify durable contracts or broad coupling created accidentally.

#### Where did the system optimize one path at the expense of another?

Examples:

* read speed versus write complexity;
* synchronous simplicity versus async recovery;
* frontend responsiveness versus stale state;
* throughput versus tail latency;
* deployment autonomy versus duplicated infrastructure.

#### Who paid the cost of the local decision?

The candidate should name users, developers, operators, clients, or future maintainers.

#### What would you change to make the global behavior cleaner?

Strong answers move responsibility toward the correct boundary, not merely add more documentation.

### Follow-up probes for the interviewer

* Why was the local choice attractive?
* When did the global cost become visible?
* Was the cost one-time or recurring?
* Which contract made reversal difficult?
* Could the complexity be moved to a better boundary?
* Did another team object?
* What migration was required?
* What local metric hid global harm?

### Weak-answer signals

Watch for answers that:

* evaluate components only by local metrics;
* cannot identify externalized cost;
* treat downstream complexity as another team’s problem;
* optimize one path without naming the harmed path;
* cannot identify a small choice with large consequences;
* fix global issues through coordination rather than design;
* ignore future maintainers;
* claim implementation details never become architecture.

---


## C. Invariants, domain concepts, and hidden structure

* What concept or invariant tied multiple parts of the system together?
* What domain idea was most important to model correctly?
* Where did the architecture reflect the business domain well?
* Where did it leak implementation details?
* What would break if that central concept was misunderstood?
* What invariant required careful reasoning even though it was not much code?
* Where was the real complexity conceptual rather than technical?
* What would a junior engineer likely misunderstand about the domain or invariant?

What this reveals:
Whether they can identify the deep structure of a system: the concepts and guarantees that make the pieces fit together.

### Clarifying questions a strong candidate may ask

* Should I focus on one domain invariant?
* Would you like the business meaning before the implementation?
* Should I include where the model leaked infrastructure concepts?
* Are you interested in a concept that crossed many components?
* Should I explain how misunderstanding it would fail?

These questions show that the deepest complexity is often conceptual rather than algorithmic.

### Reasoning expected from the candidate

A strong answer should identify:

1. **Domain concept**
   * What business idea or guarantee organizes the system?
2. **Meaning**
   * What does it mean to users and the business?
3. **Invariant**
   * What must always or eventually be true?
4. **Representation**
   * How is the concept modeled in data, APIs, events, and UI?
5. **Cross-system influence**
   * Which components depend on the same meaning?
6. **Leakage**
   * Where do vendor or storage details distort the concept?
7. **Failure**
   * What breaks if the concept is modeled incorrectly?
8. **Learning**
   * What would a less experienced engineer likely oversimplify?

A mature candidate can identify a concept that is small in code but central in meaning.

### Example of a strong coherent answer

> The central concept was the distinction between appointment availability and a confirmed booking.
>
> Availability was advisory, potentially stale, and safe to cache. A confirmed booking was authoritative, user-visible, and required external confirmation or explicit reconciliation.
>
> That distinction tied together the search read model, API contracts, UI wording, caching strategy, booking state machine, retries, support tooling, and metrics.
>
> The key invariant was that the system must never tell a patient an appointment is confirmed unless the authoritative clinic system or reconciliation process had established that result.
>
> The architecture reflected the domain well when search references and booking IDs were separate and the workflow modeled pending, confirmed, rejected, and uncertain outcomes.
>
> It leaked implementation details when vendor-specific status codes appeared in support and event payloads.
>
> If the concept were misunderstood, a developer might treat selecting a search result as reserving a slot, use optimistic confirmation, or retry a timed-out booking unsafely.
>
> The real complexity was not a large amount of code. It was preserving one meaning consistently across every layer.

### Question-by-question answer expectations

#### What concept or invariant tied multiple parts of the system together?

The candidate should name one central idea and trace it across layers.

#### What domain idea was most important to model correctly?

Examples:

* reservation versus confirmation;
* account balance;
* ownership;
* consent;
* order finality;
* eligibility;
* tenant;
* workflow status;
* source of truth.

#### Where did the architecture reflect the business domain well?

Strong examples:

* domain-named states;
* explicit boundaries;
* separate commands and events;
* policy objects;
* source-of-truth ownership;
* domain-oriented APIs.

#### Where did it leak implementation details?

Examples:

* database IDs;
* vendor codes;
* transport errors;
* queue semantics;
* cache status;
* table structure;
* framework types.

#### What would break if that central concept was misunderstood?

The candidate should name technical and user-facing consequences.

#### What invariant required careful reasoning even though it was not much code?

High-signal examples involve uniqueness, ownership, finality, or transition validity.

#### Where was the real complexity conceptual rather than technical?

Good answers explain why simple code still required deep shared understanding.

#### What would a junior engineer likely misunderstand about the domain or invariant?

The answer should identify a plausible oversimplification.

### Follow-up probes for the interviewer

* How was the concept represented in the API?
* Was the same language used in the UI and events?
* What was authoritative?
* Which implementation detail leaked most?
* Was the invariant local or distributed?
* Which test protected the concept?
* What incident revealed misunderstanding?
* How would you teach this concept to a new engineer?

### Weak-answer signals

Watch for answers that:

* cannot identify a central domain concept;
* describe only technical components;
* state an invariant vaguely;
* use vendor or database terminology as domain language;
* cannot explain consequences of misunderstanding;
* assume conceptual simplicity because code is short;
* model state with contradictory flags;
* have inconsistent meaning across APIs, UI, and events.

---


## D. Abstractions, optionality, and pattern judgment

* What abstraction in this system exists mainly to preserve optionality?
* Where did you use a general pattern in a domain-specific way?
* Where did an abstraction make future change easier?
* Where did an abstraction make the current system harder to understand?
* What pattern would be tempting here but probably wrong?
* Where did composition, adapters, strategies, events, state machines, or dependency inversion help?
* Where would a more direct implementation have been better?
* What abstraction would you remove if the system stopped changing?

What this reveals:
Whether they can evaluate abstractions and patterns based on the forces in the system, not based on pattern vocabulary.

### Clarifying questions a strong candidate may ask

* Should I focus on an abstraction that preserves replacement options?
* Would you like a useful and a harmful abstraction compared?
* Should I discuss named patterns or problem-specific structure?
* Are you interested in what could be removed today?
* Should I explain where direct code would be clearer?

These questions show that abstraction value depends on actual change pressure.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Change pressure**
   * What variation or replacement was expected?
2. **Abstraction**
   * What interface, adapter, policy, state model, or event boundary was introduced?
3. **Optionality**
   * Which future choices remained open?
4. **Current cost**
   * What indirection or cognitive load appeared immediately?
5. **Domain adaptation**
   * How was a general pattern shaped to fit this system?
6. **Misfit**
   * Which tempting pattern would add ceremony or hide behavior?
7. **Direct alternative**
   * Where would straightforward code be better?
8. **Removal condition**
   * When does the abstraction stop paying for itself?

A mature answer recognizes that optionality has carrying cost. Preserving every possible future is not good design.

### Example of a strong coherent answer

> The scheduling-provider adapter preserved optionality around clinic vendors. The booking workflow depended on a domain contract rather than a specific SDK, which allowed us to add and replace vendors incrementally.
>
> We used the general Adapter pattern in a domain-specific way. The adapter did not merely rename fields; it normalized identifiers, capabilities, error semantics, and uncertain outcomes.
>
> The abstraction made vendor change easier but introduced capability negotiation, translation tests, and another layer to debug.
>
> A tempting but wrong pattern would have been a fully generic workflow engine. Booking and cancellation had explicit state, retries, and compensation, but the problem was still understandable as domain code. A general engine would have hidden control flow and produced configuration complexity.
>
> Direct implementation was better for a small, bounded set of patient-display formatting rules. Creating strategies and factories for those rules would not have preserved meaningful optionality.
>
> If the system stopped adding vendors and standardized permanently on one provider, I would consider collapsing some adapter abstractions while preserving the internal domain model and anti-corruption boundary.

### Question-by-question answer expectations

#### What abstraction in this system exists mainly to preserve optionality?

Strong examples:

* adapter;
* facade;
* versioned API;
* repository;
* strategy;
* event contract;
* feature flag;
* compatibility layer.

The candidate should state which option remains open.

#### Where did you use a general pattern in a domain-specific way?

High-signal answers show adaptation rather than textbook ceremony.

#### Where did an abstraction make future change easier?

The candidate should name a real change that became cheaper.

#### Where did an abstraction make the current system harder to understand?

Possible costs:

* indirection;
* generic types;
* hidden control flow;
* configuration;
* test setup;
* operational debugging.

#### What pattern would be tempting here but probably wrong?

Examples:

* microservices;
* event sourcing;
* generic workflow engine;
* inheritance hierarchy;
* repository around every table;
* pub-sub for direct commands;
* plugin system for one implementation.

#### Where did composition, adapters, strategies, events, state machines, or dependency inversion help?

The candidate should connect each used pattern to a force.

#### Where would a more direct implementation have been better?

Strong answers identify low-variation, bounded, readable behavior.

#### What abstraction would you remove if the system stopped changing?

This tests whether the candidate sees abstractions as conditional investments.

### Follow-up probes for the interviewer

* What option remained open?
* How often was that option exercised?
* What was the carrying cost?
* Did the abstraction leak?
* What direct code would replace it?
* Was the pattern adapted or copied?
* Which abstraction became permanent accidentally?
* What would trigger removal?

### Weak-answer signals

Watch for answers that:

* preserve optionality with no likely variation;
* use pattern names without system forces;
* cannot identify carrying cost;
* never prefer direct code;
* cannot name a tempting but wrong pattern;
* claim abstractions always improve understanding;
* preserve obsolete compatibility layers indefinitely;
* have no removal criteria.

---


## E. Senior-level tradeoff judgment

* Where did you trade correctness for latency, or flexibility for simplicity?
* What part of the system required the most careful reasoning, even though it was not the most code?
* What decision reduced risk even though it slowed delivery?
* What decision sped up delivery but created future risk?
* What design choice shows your understanding of systems rather than just implementation?
* What tradeoff would a less experienced engineer likely miss?
* What was the hardest judgment call in the design?
* What would you ask another senior engineer to challenge in this design?

What this reveals:
Whether they can think like a senior engineer: reasoning across time, people, failure modes, complexity, and consequences rather than just solving the immediate task.

### Clarifying questions a strong candidate may ask

* Should I focus on one judgment call in depth?
* Would you like delivery, correctness, or organizational tradeoffs?
* Should I explain the challenge I would ask another senior engineer to make?
* Are you interested in a decision with limited evidence?
* Should I include what a less experienced engineer might optimize incorrectly?

These questions show that senior judgment is most visible where multiple valid goals conflict.

### Reasoning expected from the candidate

A strong answer should cover:

1. **Decision**
   * What choice required broad reasoning?
2. **Competing values**
   * Correctness, latency, simplicity, flexibility, cost, delivery, or usability?
3. **System scope**
   * Which users, teams, components, and future changes were affected?
4. **Risk**
   * What could fail now and later?
5. **Evidence**
   * What information existed, and what remained uncertain?
6. **Choice**
   * Which value was prioritized and why?
7. **Mitigation**
   * How was the accepted downside contained?
8. **Challenge**
   * What should another senior engineer question?
9. **Outcome**
   * How did the decision age?

A mature answer does not imply that seniority means choosing maximum robustness. It means choosing proportional robustness with awareness of the whole system.

### Example of a strong coherent answer

> The hardest judgment call was deciding how much correctness and workflow complexity to introduce for uncertain booking outcomes.
>
> A simpler design would have improved delivery speed and reduced code. A richer workflow protected users from duplicate or misleading outcomes but required more API states, UI behavior, support tooling, and operational ownership.
>
> We prioritized correctness for final booking state because the user and business cost of a duplicate or falsely failed booking was high. We accepted bounded staleness and simpler guarantees in search because final booking revalidated availability.
>
> The decision that reduced risk but slowed delivery was adding idempotency, explicit pending states, and reconciliation before broad rollout.
>
> The decision that sped delivery but created future risk was keeping some clinic policy in conditionals during the pilot. We contained it by limiting supported clinics and documenting a trigger for policy extraction.
>
> The design choice that best demonstrates systems thinking was separating advisory search from authoritative booking, because it connected user experience, caching, external dependency behavior, correctness, and operations.
>
> I would ask another senior engineer to challenge whether reconciliation was sufficiently automated or whether we had transferred too much complexity to operators.

### Question-by-question answer expectations

#### Where did you trade correctness for latency, or flexibility for simplicity?

The candidate should state the exact exchange and scope.

Correctness should not be treated as one undifferentiated property. Some data may be stale safely while final actions require stronger guarantees.

#### What part of the system required the most careful reasoning, even though it was not the most code?

High-signal examples:

* state semantics;
* source of truth;
* timeout handling;
* tenancy;
* identifier design;
* migration order;
* authorization policy.

#### What decision reduced risk even though it slowed delivery?

Examples:

* migration staging;
* idempotency;
* audit model;
* threat review;
* contract testing;
* workflow state;
* rollback tooling.

#### What decision sped up delivery but created future risk?

The candidate should explain why the risk was acceptable and bounded.

#### What design choice shows your understanding of systems rather than just implementation?

Strong answers connect several system dimensions.

#### What tradeoff would a less experienced engineer likely miss?

Examples:

* local simplicity versus downstream complexity;
* average latency versus tail behavior;
* retries versus duplicate effects;
* abstraction optionality versus carrying cost;
* availability versus misleading success;
* automation versus operator burden.

#### What was the hardest judgment call in the design?

The candidate should identify a decision with no dominant answer.

#### What would you ask another senior engineer to challenge in this design?

High-signal candidates actively seek critique of assumptions, failure modes, cost ownership, or migration risk.

### Follow-up probes for the interviewer

* What value was prioritized?
* Who paid the downside?
* What evidence was missing?
* Was the risk reversible?
* What assumption should be challenged?
* Did the choice age well?
* What did an operator experience?
* What would change under stricter requirements?

### Weak-answer signals

Watch for answers that:

* present correctness and latency as always aligned;
* cannot identify a judgment-heavy small area;
* never accept future risk;
* cannot name a decision that slowed delivery;
* describe systems thinking as using more technology;
* cannot identify a subtle tradeoff;
* resist peer challenge;
* evaluate decisions only by implementation success.

---

# Cross-section answer framework

Candidates can use this structure to answer most systems-thinking stress tests:

1. **Name the local decision or concern**
   * What code, component, policy, or abstraction is under discussion?
2. **Expand the system boundary**
   * Which users, services, teams, and operators are affected?
3. **Identify the central concept**
   * What invariant or domain meaning ties the behavior together?
4. **Map cost movement**
   * What became easier locally, and who paid elsewhere?
5. **Explain the abstraction**
   * What change or optionality does it preserve?
6. **State the carrying cost**
   * What complexity exists today because of it?
7. **Name the tradeoff**
   * Correctness, latency, flexibility, simplicity, delivery, or operations?
8. **Identify the limit**
   * What assumption or growth pressure breaks the design?
9. **Invite challenge**
   * What should another senior engineer question?
10. **Reflect**
   * What would be centralized, simplified, moved, or removed now?

A strong answer moves fluently between a local implementation choice and its system-wide consequences.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* identifies system-wide concerns and consistent semantics;
* balances centralization with visible domain decisions;
* recognizes externalized costs of local choices;
* names who pays those costs;
* identifies one central domain concept or invariant;
* traces that concept across data, APIs, UI, events, and operations;
* evaluates abstractions by real optionality and carrying cost;
* can reject tempting but inappropriate patterns;
* distinguishes conceptual complexity from code volume;
* explains difficult tradeoffs across time and teams;
* invites challenge to assumptions and operational burden;
* proposes cleaner global behavior rather than local patches.

## Mixed signal

The candidate:

* recognizes cross-cutting concerns but weakly discusses hidden behavior;
* identifies local/global effects but not the full cost owner;
* names important invariants but weakly traces them across layers;
* understands pattern fit but has limited removal criteria;
* discusses tradeoffs but not how they aged.

## Weak signal

The candidate:

* reasons only within one component;
* centralizes concerns through opaque magic;
* ignores downstream and operational costs;
* cannot identify a central invariant;
* discusses patterns as vocabulary;
* preserves optionality without evidence;
* cannot name a tempting but wrong pattern;
* treats seniority as adding architecture;
* resists critique of assumptions or design limits.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What cross-cutting concern required system-wide consistency?
2. What part was centralized?
3. What remained explicit?
4. What local decision pushed complexity elsewhere?
5. Who paid that cost?
6. What domain invariant tied the system together?
7. Where did implementation details leak into the domain?
8. What abstraction preserved meaningful optionality?
9. What pattern would have been tempting but wrong?
10. What small area required the deepest reasoning?
11. What risk-reducing decision slowed delivery?
12. What would you ask another senior engineer to challenge?

A strong response should demonstrate system-wide consistency, cost-accounting across boundaries, explicit invariants, contextual pattern judgment, and senior-level awareness of consequences over time.
