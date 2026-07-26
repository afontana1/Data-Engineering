# 5. Data modeling and state management

These questions test whether the candidate understands data design as behavior-driven. The goal is to see whether they can model entities, relationships, state, invariants, and access patterns in a way that supports correctness, maintainability, and future change.

## Table of contents

- [A. Core entities and relationships](#a-core-entities-and-relationships)
- [B. Invariants, consistency, and source of truth](#b-invariants-consistency-and-source-of-truth)
- [C. State placement and lifecycle](#c-state-placement-and-lifecycle)
- [D. Access patterns and data shape](#d-access-patterns-and-data-shape)
- [E. Schema evolution and long-term maintainability](#e-schema-evolution-and-long-term-maintainability)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched for appointments, booked or cancelled visits, and received reminders. Clinic scheduling systems remained authoritative for provider schedules and final inventory. The platform maintained normalized clinic configuration, availability read models, durable booking workflow state, idempotency records, audit history, and events consumed by notifications and analytics.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can explain how data structures represent behavior, where state belongs, which invariants matter, how access patterns shape models, and how schemas evolve safely.



## A. Core entities and relationships

* What were the core entities in the system?
* How did you decide which concepts deserved their own model or table?
* Which relationships between entities were most important to get right?
* Were there any relationships that looked simple at first but became more complicated?
* How closely did the data model reflect the business domain?
* Were there concepts that were hard to represent cleanly?
* What part of the model would a new engineer need to understand first?
* Looking back, was anything modeled at the wrong level of abstraction?

What this reveals:
Whether they can model data around real domain behavior and relationships rather than just creating storage structures.

### Clarifying questions a strong candidate may ask

* Should I describe the conceptual domain model, the physical database schema, or both?
* Would you like the original model or how it evolved?
* Should I focus on the whole system or the entities I personally owned?
* Are you most interested in entity boundaries, relationships, or lifecycle behavior?
* Should I explain where the model intentionally differed from the business language?

These questions show that a data model can be discussed at several levels. A strong candidate should distinguish business concepts from storage implementation.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Domain concepts**
   * What real-world things, events, or agreements did the system represent?
2. **Identity**
   * What made each entity distinct?
3. **Ownership**
   * Which aggregate or service controlled changes?
4. **Relationships**
   * How were entities connected over time?
5. **Behavior**
   * What actions and rules justified separate models?
6. **Cardinality and optionality**
   * Was the relationship one-to-one, one-to-many, many-to-many, or temporal?
7. **Abstraction**
   * Which concepts were explicit, and which were collapsed?
8. **Evolution**
   * Which modeling decisions later became awkward?

A mature candidate should not decide that every noun deserves a table. A concept usually deserves a first-class model when it has independent identity, behavior, lifecycle, invariants, ownership, or significant query needs.

### Example of a strong coherent answer

> The core entities were Patient, Clinic, Provider, AppointmentType, AvailabilitySlot, Booking, and BookingAttempt.
>
> Patient and Clinic represented stable business identities. Provider schedules and raw appointment inventory belonged to external clinic systems, so our AvailabilitySlot was a normalized projection rather than an authoritative appointment record.
>
> Booking was the most important domain entity in our system. It represented the patient’s requested appointment and moved through pending, confirmed, failed, cancelled, or reconciliation-required states. We modeled BookingAttempt separately because one logical booking could involve several external calls or retries, and we needed to preserve each outcome for idempotency and support investigation.
>
> AppointmentType deserved its own model because it carried duration, eligibility, clinic mapping, and cancellation policy. We did not model every vendor-specific code as a domain entity. Those remained in adapter metadata.
>
> The hardest relationship was between a visible availability slot and a confirmed booking. At first it looked one-to-one, but the slot was only a temporary projection. It could expire, be replaced, or map to a vendor-specific resource combination. We therefore stored the source reference and confirmation evidence instead of treating the search record as permanent truth.
>
> A new engineer needed to understand that AvailabilitySlot and Booking had different authority and lifecycles. Looking back, we initially modeled cancellation as a boolean on Booking. That was too weak because cancellation had its own request, policy decision, external attempt, outcome, and audit trail.

### Question-by-question answer expectations

#### What were the core entities in the system?

A strong answer names only the important concepts and explains their role.

Useful categories:

* actors;
* resources;
* transactions;
* policies;
* events;
* lifecycle records;
* configuration;
* audit or attempt records.

The candidate should identify which entities were authoritative and which were derived.

#### How did you decide which concepts deserved their own model or table?

Good criteria include:

* independent identity;
* separate lifecycle;
* behavior or rules;
* reuse across workflows;
* many relationships;
* auditing needs;
* ownership boundary;
* query frequency.

Weak rationale:

> It was a noun in the requirements.

#### Which relationships between entities were most important to get right?

Strong answers identify the relationship and its business consequence.

Examples:

* order to payment;
* user to tenant;
* booking to appointment;
* account to entitlement;
* document to version;
* event to aggregate.

The candidate should discuss cardinality and temporal behavior.

#### Were there any relationships that looked simple at first but became more complicated?

High-signal examples include:

* one user with multiple roles;
* one order with partial shipments;
* one booking with several attempts;
* one resource with historical owners;
* one product with regional variants;
* one event linked to several causes.

The candidate should explain how the model changed.

#### How closely did the data model reflect the business domain?

A strong answer identifies where alignment helped and where storage or integration concerns required translation.

Good models use business language without exposing every external or database detail.

#### Were there concepts that were hard to represent cleanly?

Examples:

* temporal validity;
* recurring schedules;
* partial completion;
* uncertain outcomes;
* inheritance-like product variants;
* policy exceptions;
* many-to-many relationships with attributes.

The candidate should explain the tradeoff chosen.

#### What part of the model would a new engineer need to understand first?

This should be the concept that organizes the rest of the model:

* aggregate root;
* source of truth;
* state machine;
* versioning model;
* tenant boundary;
* temporal model.

#### Looking back, was anything modeled at the wrong level of abstraction?

Strong answers identify over-modeling or under-modeling.

Examples:

* boolean where a lifecycle was needed;
* generic key-value data where structure mattered;
* separate tables for concepts that always changed together;
* one broad entity hiding distinct responsibilities.

### Follow-up probes for the interviewer

* What gave each entity identity?
* Which entity owned the invariant?
* Were relationships temporal?
* What was modeled as an event versus current state?
* Which table became overloaded?
* Which concept was duplicated?
* What did the database schema expose that the domain should not?
* What would you merge or split today?

### Weak-answer signals

Watch for answers that:

* list tables without explaining domain meaning;
* model every noun independently;
* cannot explain entity identity;
* ignore lifecycle and ownership;
* treat derived data as authoritative;
* cannot describe cardinality;
* use generic JSON fields for all future flexibility;
* cannot identify a modeling mistake or evolution.

---


## B. Invariants, consistency, and source of truth

* What were the most important invariants the data had to preserve?
* What data absolutely had to be correct at all times?
* What was the source of truth for the most important state?
* Were there multiple copies or derived versions of important data?
* Where was stale data acceptable, and where was it not?
* How did you prevent invalid or contradictory states?
* Were there consistency risks across services, caches, clients, or background jobs?
* What would have been the business impact of violating a key invariant?

What this reveals:
Whether they understand that data modeling is about preserving correctness and meaning, not just storing fields.

### Clarifying questions a strong candidate may ask

* Should I focus on domain invariants, database constraints, or distributed consistency?
* Would you like the strongest correctness requirement or several examples?
* Should I discuss consistency within one service or across the full workflow?
* Are you interested in stale reads, conflicting writes, or both?
* Should I explain what the system guaranteed versus what it only attempted?

These questions show that correctness exists at several layers and that guarantees should not be overstated.

### Reasoning expected from the candidate

A mature answer should distinguish:

* **invariant:** a condition that must remain true;
* **source of truth:** the authority for a fact;
* **derived data:** a copy or transformation that can be rebuilt;
* **consistency model:** when observers are expected to agree;
* **constraint:** an enforcement mechanism;
* **reconciliation:** repair when distributed state diverges.

A strong answer should explain:

1. the invariant;
2. why it matters;
3. where authority lives;
4. how it is enforced;
5. where stale data is acceptable;
6. what race or failure could violate it;
7. how violations are detected and repaired;
8. business impact.

### Example of a strong coherent answer

> The most important invariant was that one external appointment slot could not result in two confirmed bookings through our platform. The clinic scheduling system was authoritative for final inventory, but our database also enforced uniqueness on the external booking reference and idempotency key.
>
> Search availability was derived and could be stale for a bounded period. That was acceptable because search was advisory. Booking status, patient identity, external confirmation reference, and cancellation status had to be durable and correct.
>
> We maintained several copies of information: normalized availability in the search store, booking workflow state in the relational database, and events in the analytics pipeline. Those copies had different authority. The search store could be rebuilt. Analytics could lag. The booking record was authoritative for our workflow, while the clinic system was authoritative for whether the appointment existed operationally.
>
> We prevented contradictory states through database constraints, transactional state transitions, idempotent commands, and validation against the current state. Across systems, we could not use a single transaction, so uncertain outcomes entered reconciliation rather than being guessed.
>
> Violating the duplicate-booking invariant would waste scarce appointment capacity, create patient harm, and require manual intervention. That justified stronger controls than we used for search freshness.

### Question-by-question answer expectations

#### What were the most important invariants the data had to preserve?

Strong invariants are specific.

Examples:

* a payment is applied at most once;
* inventory never becomes negative;
* one user cannot access another tenant’s records;
* a confirmed booking has an external reference;
* a child cannot outlive a required parent;
* state transitions occur in allowed order.

#### What data absolutely had to be correct at all times?

The candidate should separate critical data from data that can lag.

Possible critical data:

* balances;
* authorization;
* ownership;
* confirmed workflow status;
* legal consent;
* fulfillment state.

#### What was the source of truth for the most important state?

A strong answer names the authority and explains why.

In distributed systems, different facts may have different authorities.

#### Were there multiple copies or derived versions of important data?

The candidate should identify:

* cache;
* replica;
* search index;
* materialized view;
* analytics warehouse;
* client state;
* event stream.

They should explain rebuildability and synchronization.

#### Where was stale data acceptable, and where was it not?

Good answers specify freshness bounds and consequences.

Example:

> Product descriptions could be minutes stale. Authorization and payment state could not be trusted from cache.

#### How did you prevent invalid or contradictory states?

Strong mechanisms include:

* database constraints;
* transactions;
* state machines;
* validation;
* optimistic concurrency;
* idempotency;
* uniqueness;
* foreign keys;
* reconciliation.

The candidate should connect mechanism to invariant.

#### Were there consistency risks across services, caches, clients, or background jobs?

High-signal answers discuss:

* delayed events;
* cache invalidation;
* duplicate delivery;
* out-of-order updates;
* concurrent writes;
* stale client state;
* partial failure.

#### What would have been the business impact of violating a key invariant?

A strong candidate connects correctness to user, financial, legal, or operational harm.

### Follow-up probes for the interviewer

* Where was the invariant enforced?
* Was enforcement duplicated?
* What happened under retry?
* Could stale data authorize an action?
* How was divergence detected?
* Which state could be rebuilt?
* What was the maximum tolerated inconsistency window?
* Did an invariant ever fail in production?

### Weak-answer signals

Watch for answers that:

* define invariants vaguely;
* claim everything was strongly consistent;
* cannot name a source of truth;
* treat all copies as equivalent;
* rely only on application code when database constraints were appropriate;
* ignore duplicate or out-of-order behavior;
* overstate exactly-once guarantees;
* cannot explain business impact.

---


## C. State placement and lifecycle

* What state lived in the database, in memory, in caches, in the client, or in external systems?
* How did you decide where each kind of state belonged?
* Which state was durable, temporary, derived, cached, or user-specific?
* What state transitions mattered most?
* Were there workflows where state moved through multiple stages?
* Did any state become difficult to reason about because it was spread across places?
* How did you handle state recovery after failure or restart?
* What state would have been dangerous to keep only in memory or only on the client?

What this reveals:
Whether they can reason about state as something with location, lifetime, ownership, and correctness implications.

### Clarifying questions a strong candidate may ask

* Should I describe state placement by layer or by workflow?
* Would you like durable and ephemeral state separated?
* Should I include client and external-system state?
* Are you most interested in lifecycle transitions or recovery after failure?
* Should I focus on one stateful workflow in depth?

These questions show that state has location, lifetime, ownership, and recovery semantics.

### Reasoning expected from the candidate

A strong answer should classify state by:

* **durability:** persistent or ephemeral;
* **authority:** source, replica, or derived;
* **scope:** global, tenant, user, session, or request;
* **lifetime:** request, session, workflow, or permanent;
* **ownership:** which component may mutate it;
* **recoverability:** can it be rebuilt?
* **sensitivity:** what security or privacy rules apply?

The candidate should then explain lifecycle transitions and failure recovery.

### Example of a strong coherent answer

> Durable booking workflow state lived in the relational database because it had to survive process restarts, retries, and uncertain external outcomes. That included the booking state, idempotency key, external references, attempt history, and timestamps.
>
> Availability search data lived in a cache-backed read model because it was derived from clinic systems and could be rebuilt. In-memory state was limited to request-local calculations and short-lived connection pools. We did not keep workflow progress only in process memory.
>
> The client held user-interface state such as selected filters, form progress, and optimistic navigation. It never held authoritative authorization or booking status. After a refresh, it reloaded status from the server.
>
> The clinic system held provider schedules and final appointment inventory. Our system stored references and normalized projections, not ownership of that state.
>
> The central lifecycle was pending → confirmed, failed, expired, or reconciliation required. Cancellation had a separate requested → processing → cancelled or rejected lifecycle.
>
> State became hardest to reason about when support overrides were represented partly in the database and partly through vendor-side notes. We later made the override action and result explicit in our audit model.
>
> After restart, workers resumed from durable workflow records and queues. Any state needed to complete or repair a user-visible operation had to be persisted before the external side effect.

### Question-by-question answer expectations

#### What state lived in the database, in memory, in caches, in the client, or in external systems?

The candidate should map each state category and justify placement.

Strong answers distinguish authoritative from convenient copies.

#### How did you decide where each kind of state belonged?

Useful criteria:

* durability;
* latency;
* sharing;
* consistency;
* recoverability;
* ownership;
* sensitivity;
* cost.

#### Which state was durable, temporary, derived, cached, or user-specific?

The candidate should classify representative state rather than say “the database stored everything.”

#### What state transitions mattered most?

Strong answers describe domain transitions and allowed paths.

Example:

> draft → submitted → approved → fulfilled

They should identify terminal, reversible, and exceptional states.

#### Were there workflows where state moved through multiple stages?

The candidate should explain:

* trigger;
* transition;
* persistence;
* external side effects;
* failure state;
* compensation or retry.

#### Did any state become difficult to reason about because it was spread across places?

High-signal examples:

* client plus server;
* cache plus database;
* several services;
* external vendor plus internal workflow;
* configuration in code and database.

The candidate should explain the remedy or remaining risk.

#### How did you handle state recovery after failure or restart?

Strong mechanisms include:

* durable queues;
* workflow records;
* checkpoints;
* leases;
* replay;
* reconciliation;
* idempotent reprocessing;
* write-ahead logs.

#### What state would have been dangerous to keep only in memory or only on the client?

Examples:

* payment progress;
* authorization decisions;
* inventory reservation;
* job ownership;
* user consent;
* distributed lock ownership;
* confirmed workflow status.

### Follow-up probes for the interviewer

* What state could be recomputed?
* What was written before the side effect?
* How were abandoned workflows found?
* Could two workers advance the same state?
* What happened after browser refresh?
* Which state had retention requirements?
* Was there a state-machine definition?
* How were illegal transitions prevented?

### Weak-answer signals

Watch for answers that:

* cannot classify state by authority or durability;
* keep important workflow progress only in memory;
* trust client state for authorization;
* have no recovery story;
* model lifecycle with unrelated booleans;
* cannot explain where external truth lives;
* spread mutation ownership across components;
* ignore abandoned or partial workflows.

---


## D. Access patterns and data shape

* What queries or access patterns shaped the data model?
* Which reads or writes were most important to optimize for?
* How did you decide what to normalize versus denormalize?
* Were there places where the ideal domain model conflicted with efficient access patterns?
* What indexes, aggregates, cached views, or derived fields became necessary?
* Which query became awkward because of an earlier modeling choice?
* Did reporting, search, filtering, or analytics needs influence the model?
* What would have changed if the primary access pattern had been different?

What this reveals:
Whether they understand that data models are shaped by how the system actually uses the data, not just by conceptual purity.

### Clarifying questions a strong candidate may ask

* Should I focus on transactional access patterns, search, analytics, or all three?
* Would you like the most important read and write paths?
* Should I discuss the conceptual model before physical optimization?
* Are you interested in normalization decisions or query performance?
* Should I include an access pattern that changed later?

These questions show that data models are shaped by use, not only by conceptual elegance.

### Reasoning expected from the candidate

A strong candidate should explain:

1. **Primary access patterns**
   * Key lookup, range query, filtering, aggregation, traversal, append, or update?
2. **Frequency and latency**
   * Which operations dominated and which were user-facing?
3. **Write behavior**
   * Single-row, batch, append-only, concurrent, or transactional?
4. **Data shape**
   * Cardinality, size, skew, and growth?
5. **Modeling choice**
   * Normalize, denormalize, index, materialize, partition, or cache?
6. **Tradeoff**
   * Duplication, freshness, write amplification, or complexity?
7. **Change**
   * What happened when access patterns evolved?

### Example of a strong coherent answer

> The two dominant access patterns were searching availability by clinic, appointment type, location, and time range, and loading a booking by patient or external reference.
>
> The normalized domain model was not sufficient for interactive search because answering a search request required joins across clinic configuration, provider schedules, appointment types, and vendor mappings. We created a denormalized availability read model keyed by clinic, appointment type, and time bucket.
>
> Booking state remained normalized in a relational schema because writes were less frequent and correctness across booking, attempts, and audit records mattered more than read simplicity.
>
> We added composite indexes for patient plus status, clinic plus time range, and external booking reference. We used cursor pagination for large search results and stored a derived display label to avoid repeated mapping work.
>
> Analytics requirements influenced event design rather than the transactional schema. We emitted domain events and built warehouse models separately instead of adding reporting-oriented columns to operational tables.
>
> One awkward query came from modeling provider capabilities as an unstructured JSON field. Filtering by capability became expensive and hard to validate. We later promoted the frequently queried attributes into explicit relational fields while retaining vendor-specific extras separately.
>
> If the primary workload had been reporting rather than booking, we would have favored append-oriented history and columnar models instead of transactional normalization.

### Question-by-question answer expectations

#### What queries or access patterns shaped the data model?

Strong answers name concrete patterns:

* lookup by ID;
* range by time;
* filter by tenant and status;
* append events;
* aggregate by day;
* traverse graph;
* full-text search;
* batch export.

#### Which reads or writes were most important to optimize for?

The candidate should prioritize by:

* frequency;
* latency sensitivity;
* business criticality;
* cost;
* contention;
* user visibility.

#### How did you decide what to normalize versus denormalize?

A strong answer discusses:

* correctness and update consistency;
* query cost;
* duplication;
* write frequency;
* ownership;
* rebuildability;
* read latency.

#### Were there places where the ideal domain model conflicted with efficient access patterns?

This is common and not inherently bad.

Good solutions include:

* read models;
* materialized views;
* search indexes;
* aggregates;
* caches;
* duplicated display fields.

#### What indexes, aggregates, cached views, or derived fields became necessary?

The candidate should explain the query each mechanism supported and its maintenance cost.

#### Which query became awkward because of an earlier modeling choice?

Strong answers show learning.

Examples:

* filtering inside JSON;
* many joins;
* missing temporal history;
* poor partition key;
* nullable polymorphic columns;
* lack of stable identifier.

#### Did reporting, search, filtering, or analytics needs influence the model?

A mature answer separates operational and analytical needs where appropriate.

#### What would have changed if the primary access pattern had been different?

The candidate should demonstrate conditional reasoning.

Examples:

* write-heavy workload → append-only model;
* graph traversal → graph-oriented storage;
* analytical scans → columnar warehouse;
* key-value lookup → simpler denormalized records.

### Follow-up probes for the interviewer

* What was the hottest query?
* How did you choose index order?
* What was the write amplification?
* How was denormalized data refreshed?
* What was the cache invalidation rule?
* How did skew affect the model?
* Were analytical queries isolated?
* What access pattern appeared later?

### Weak-answer signals

Watch for answers that:

* model data without reference to queries;
* normalize or denormalize as ideology;
* add indexes without explaining workload;
* ignore write costs of derived data;
* use JSON to avoid all schema decisions;
* mix analytics and transactional workloads without tradeoff discussion;
* cannot name an awkward query;
* choose storage technology before describing access patterns.

---


## E. Schema evolution and long-term maintainability

* How did the data model evolve over time?
* How did you handle schema changes without breaking existing behavior?
* Which parts of the schema were easiest to change?
* Which parts became too rigid or too loose?
* Were there migrations, backfills, or compatibility concerns?
* Did any early shortcut become expensive later?
* How did you communicate or coordinate data model changes with other parts of the system?
* If you redesigned the model today, what would you make more explicit or more flexible?

What this reveals:
Whether they understand that data models become long-lived contracts and must evolve safely as the system changes.

### Clarifying questions a strong candidate may ask

* Should I discuss additive changes, breaking changes, or both?
* Would you like database migrations, event schemas, and API compatibility included?
* Should I focus on one difficult migration?
* Are you interested in technical rollout or cross-team coordination?
* Should I explain what made the model rigid or overly loose?

These questions show that schema evolution is both a technical and organizational problem.

### Reasoning expected from the candidate

A strong answer should cover:

1. **Change type**
   * Additive, renaming, splitting, merging, constraint tightening, or ownership transfer?
2. **Compatibility**
   * Could old and new code run together?
3. **Migration sequence**
   * Expand, migrate, verify, switch, contract?
4. **Data transformation**
   * Backfill, dual write, shadow read, or lazy migration?
5. **Validation**
   * How did the team prove correctness?
6. **Rollback**
   * Could the change be reversed safely?
7. **Coordination**
   * Which services, clients, or teams depended on the schema?
8. **Long-term lesson**
   * What became too rigid or too generic?

### Example of a strong coherent answer

> The schema evolved from a simple confirmed-or-failed booking table into an explicit workflow model with attempt history, uncertain outcomes, cancellation state, and audit metadata.
>
> We handled changes using an expand-and-contract approach. For example, when replacing a cancellation boolean with a cancellation lifecycle, we first added new tables and nullable references, updated writers to populate both representations, backfilled historical data, switched readers to the new model, validated counts and sampled records, and only then removed the old field.
>
> Event and API schemas required longer compatibility windows than internal tables because downstream consumers released independently. We added fields rather than changing meaning in place and versioned events when semantics changed.
>
> The easiest parts to evolve were additive metadata and derived read models. The hardest were identifiers and fields that external consumers had treated as stable contracts.
>
> An early shortcut was storing vendor-specific eligibility details in one generic JSON column. It accelerated onboarding but made validation, querying, and migration difficult. We eventually separated stable domain fields from vendor extensions.
>
> If redesigning today, I would make temporal validity and workflow attempts explicit from the beginning, but I would still avoid modeling every possible vendor attribute as a first-class column.

### Question-by-question answer expectations

#### How did the data model evolve over time?

The candidate should describe why it changed:

* new workflows;
* scale;
* reporting;
* failures;
* compliance;
* integrations;
* ownership changes.

#### How did you handle schema changes without breaking existing behavior?

Strong approaches include:

* additive changes;
* expand-and-contract;
* dual reads or writes;
* versioned events;
* compatibility layers;
* feature flags;
* phased rollout.

#### Which parts of the schema were easiest to change?

Typically:

* internal additive fields;
* derived models;
* non-authoritative metadata;
* isolated tables.

The candidate should explain why.

#### Which parts became too rigid or too loose?

Too rigid:

* enums requiring coordinated releases;
* overloaded inheritance;
* fixed one-to-one assumptions;
* identifiers embedded in clients.

Too loose:

* unvalidated JSON;
* generic key-value tables;
* nullable columns representing many states;
* strings with implicit meaning.

#### Were there migrations, backfills, or compatibility concerns?

A strong answer explains:

* migration size;
* online versus offline;
* backfill safety;
* validation;
* throttling;
* rollback;
* old/new coexistence.

#### Did any early shortcut become expensive later?

High-signal examples:

* shared schema;
* weak identifiers;
* generic blobs;
* missing audit history;
* no temporal model;
* duplicated data without ownership.

#### How did you communicate or coordinate data model changes with other parts of the system?

Useful mechanisms:

* schema review;
* contract tests;
* migration plan;
* ownership registry;
* change announcement;
* consumer inventory;
* dashboards;
* deprecation timeline.

#### If you redesigned the model today, what would you make more explicit or more flexible?

Strong answers distinguish what should be strongly modeled from what should remain extensible.

### Follow-up probes for the interviewer

* Could old and new code run together?
* What was the backfill validation?
* How did you rollback?
* Who consumed the schema directly?
* Did dual writes diverge?
* Which identifier was hardest to change?
* What semantic change required versioning?
* What would you never store generically again?

### Weak-answer signals

Watch for answers that:

* treat migrations as simple DDL only;
* cannot explain compatibility;
* perform destructive changes in one step;
* have no backfill validation;
* use dual writes without reconciliation;
* ignore downstream consumers;
* cannot name a schema shortcut;
* propose redesign without migration reality.

---

# Cross-section answer framework

Candidates can use this structure to answer most data-modeling questions:

1. **Identify the domain concepts**
   * What real-world entities, events, and policies exist?
2. **Explain identity and ownership**
   * What makes each entity distinct, and who may change it?
3. **Describe relationships**
   * What cardinality, temporal behavior, and lifecycle matter?
4. **State invariants**
   * What conditions must remain true?
5. **Name the source of truth**
   * Which copy is authoritative, and which are derived?
6. **Place state**
   * What is durable, cached, ephemeral, client-side, or external?
7. **Connect access patterns**
   * Which reads and writes shaped the physical model?
8. **Explain tradeoffs**
   * Where did normalization, duplication, indexing, or caching help?
9. **Describe evolution**
   * How were schemas changed, backfilled, and validated?
10. **Reflect**
   * What was modeled too loosely, too rigidly, or at the wrong abstraction?

A strong answer connects domain meaning, correctness, storage, and change over time rather than discussing tables in isolation.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* explains entities by domain behavior and identity;
* distinguishes authoritative and derived models;
* identifies meaningful relationships and lifecycle complexity;
* names specific invariants and enforcement mechanisms;
* explains where stale data is acceptable;
* places state according to durability, ownership, and recovery needs;
* describes a clear state machine or workflow;
* connects access patterns to normalization, indexes, and read models;
* understands the costs of denormalization and caching;
* explains safe schema evolution and compatibility;
* discusses a real migration or backfill;
* reflects on a modeling shortcut or abstraction mistake.

## Mixed signal

The candidate:

* understands entities and relationships but weakly explains ownership;
* names invariants without enforcement detail;
* maps state placement but not recovery;
* discusses indexes and normalization generically;
* has migration experience but limited compatibility reasoning;
* understands the current model but not how it evolved.

## Weak signal

The candidate:

* lists tables without domain reasoning;
* cannot identify a source of truth;
* treats all copies as equally authoritative;
* models workflows with unrelated booleans;
* keeps critical state only in memory or the client;
* chooses normalization or denormalization dogmatically;
* cannot connect queries to schema;
* treats migrations as one-step destructive changes;
* has no validation or rollback story;
* cannot identify a modeling mistake.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What were the five most important entities?
2. What gave each one identity?
3. Which relationship was hardest to model?
4. What was the most important invariant?
5. Which system or table was authoritative for that fact?
6. What copies or derived models existed?
7. Where was stale data acceptable?
8. What was the main state lifecycle?
9. What state had to survive failure or restart?
10. Which access pattern most shaped the schema?
11. What schema migration was most difficult?
12. What would you model differently today?

A strong response should allow the interviewer to understand the domain model, the correctness rules, the location and lifecycle of state, the dominant access patterns, and how the model changed safely over time.
