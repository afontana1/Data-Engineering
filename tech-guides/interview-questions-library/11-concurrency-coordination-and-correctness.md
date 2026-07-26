# 11. Concurrency, coordination, and correctness

These questions test whether the candidate understands correctness under real-world execution. They are especially useful for systems with multiple users, background jobs, async workflows, distributed services, shared state, or operations that may be retried, reordered, duplicated, or interleaved.

## Table of contents

- [A. Concurrent actors and shared state](#a-concurrent-actors-and-shared-state)
- [B. Correctness guarantees and invariants](#b-correctness-guarantees-and-invariants)
- [C. Async workflows and background processing](#c-async-workflows-and-background-processing)
- [D. Ordering, duplication, and eventual consistency](#d-ordering-duplication-and-eventual-consistency)
- [E. Coordination strategy and tradeoffs](#e-coordination-strategy-and-tradeoffs)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Multiple patients could search and attempt to book the same slot, background workers refreshed availability and reconciled uncertain bookings, external clinic systems could retry or reorder responses, and several services consumed booking events independently.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can identify concurrent actors, connect concurrency controls to invariants, explain async failure and recovery, reason about ordering and duplication, and justify the coordination mechanisms they chose.



## A. Concurrent actors and shared state

* Were there any concurrency concerns in the system?
* What users, workers, services, jobs, or processes could act on the same state?
* Could two users or processes race in a way that caused incorrect behavior?
* Which shared resources or records were most vulnerable to concurrent updates?
* What assumptions did the system make about operation ordering?
* What behavior was safe under sequential execution but risky under concurrency?
* What concurrency issue would have been hardest for a tester to reproduce?
* How did you reason about the system when multiple actors were active at once?

What this reveals:
Whether they can recognize concurrency as a correctness problem, not just a performance or infrastructure issue.

### Clarifying questions a strong candidate may ask

* Should I focus on user concurrency, worker concurrency, or distributed service concurrency?
* Would you like one race condition in depth?
* Should I discuss database-level and application-level shared state?
* Are you interested in production incidents or design-time reasoning?
* Should I explain the execution interleaving that created the risk?

These questions show that concurrency is about overlapping operations on shared state, not merely many requests per second.

### Reasoning expected from the candidate

A strong answer should identify:

1. **Actors**
   * Users, threads, workers, services, scheduled jobs, or external systems?
2. **Shared state**
   * Which record, resource, counter, slot, or workflow did they touch?
3. **Interleaving**
   * In what order could reads and writes overlap?
4. **Invariant at risk**
   * What incorrect final state could appear?
5. **Conflict frequency**
   * Rare edge case or common workload?
6. **Detection difficulty**
   * Deterministic, timing-dependent, or load-dependent?
7. **Control**
   * Constraint, transaction, lock, version check, queue, or idempotency?
8. **Residual risk**
   * What remained possible?

A mature answer can describe the unsafe interleaving step by step.

### Example of a strong coherent answer

> The clearest concurrency risk was two patients attempting to book the same external appointment slot at nearly the same time.
>
> Both clients could read the slot as available from the search read model. If our backend simply checked local availability and then wrote a confirmed booking, both requests could succeed under sequential-looking application code.
>
> The authoritative clinic system performed the final reservation atomically. We also used an idempotency key per logical booking request and a uniqueness constraint on the external slot reference where the vendor contract allowed it.
>
> Other concurrent actors included reconciliation workers, cancellation workers, support operators, and event consumers. A support retry could overlap with an automated retry, so workflow updates used version checks and valid state transitions rather than unconditional writes.
>
> The hardest bug to reproduce involved a worker reading a pending booking, an operator resolving it manually, and the worker then writing an older result. That only appeared under a narrow timing window. We fixed it with optimistic concurrency and transition guards.
>
> We reasoned about concurrency by identifying shared records, writing explicit interleavings, and asking whether every possible order preserved the booking invariants.

### Question-by-question answer expectations

#### Were there any concurrency concerns in the system?

A strong answer should name a concrete shared resource and competing actors.

#### What users, workers, services, jobs, or processes could act on the same state?

The candidate should map all mutation paths, including administrative and recovery workflows.

#### Could two users or processes race in a way that caused incorrect behavior?

Strong answers describe the race precisely.

Useful pattern:

1. Actor A reads state.
2. Actor B reads or changes state.
3. Actor A writes based on stale state.
4. Invariant is violated.

#### Which shared resources or records were most vulnerable to concurrent updates?

Examples:

* inventory;
* balance;
* booking slot;
* workflow status;
* lease;
* sequence number;
* aggregate counter;
* queue ownership.

#### What assumptions did the system make about operation ordering?

The candidate should identify assumptions such as:

* one writer;
* FIFO delivery;
* monotonic timestamps;
* transaction serialization;
* client request order;
* leader ownership.

#### What behavior was safe under sequential execution but risky under concurrency?

Examples:

* check-then-act;
* read-modify-write;
* increment;
* create-if-absent;
* deduplicate;
* reserve then confirm;
* status transition.

#### What concurrency issue would have been hardest for a tester to reproduce?

High-signal answers involve timing, retries, stale reads, or process crashes.

#### How did you reason about the system when multiple actors were active at once?

Strong methods:

* interleaving analysis;
* state-machine transitions;
* invariant review;
* property-based testing;
* race injection;
* load testing;
* model checking where warranted.

### Follow-up probes for the interviewer

* Show me the exact interleaving.
* Which actor had stale state?
* Was there a single writer?
* Could an operator race with automation?
* Which race was prevented by the database?
* Which race remained in application code?
* Was the conflict common or rare?
* How was the bug observed?

### Weak-answer signals

Watch for answers that:

* equate concurrency with traffic volume only;
* cannot name shared state;
* say transactions solved everything without detail;
* ignore operator and retry races;
* cannot describe an unsafe interleaving;
* assume request order equals execution order;
* rely on client-side prevention;
* have no strategy for timing-dependent tests.

---


## B. Correctness guarantees and invariants

* What invariants were hardest to preserve?
* How did you preserve correctness under concurrent updates?
* What state transitions needed to be atomic?
* Where did you rely on database constraints, transactions, locks, optimistic concurrency, queues, or idempotency?
* What would an invalid final state look like?
* Were there operations that needed exactly-once behavior, or was at-least-once with idempotency acceptable?
* What correctness guarantee mattered most to users or the business?
* How did you know the system preserved that guarantee?

What this reveals:
Whether they can connect concurrency mechanisms to the actual invariants the system needs to protect.

### Clarifying questions a strong candidate may ask

* Should I focus on one invariant or the overall correctness model?
* Would you like the database mechanism or distributed mechanism in depth?
* Should I discuss exactly-once claims?
* Are you interested in atomic state transitions?
* Should I include how correctness was verified in production?

These questions show that mechanisms should be selected to protect explicit invariants.

### Reasoning expected from the candidate

A strong answer should follow:

1. **Invariant**
   * What must remain true?
2. **Scope**
   * One row, one transaction, one service, or several systems?
3. **Failure and race**
   * What interleaving could violate it?
4. **Mechanism**
   * Constraint, transaction, lock, version, queue, idempotency, or reconciliation?
5. **Guarantee level**
   * Strong, eventual, at-most-once, or at-least-once?
6. **Proof or evidence**
   * Test, database guarantee, metric, or audit?
7. **Business meaning**
   * Why does the invariant matter?

A mature candidate avoids claiming exactly-once delivery when the real design is at-least-once processing with idempotent effects.

### Example of a strong coherent answer

> The hardest invariant was that one external appointment slot could not produce more than one confirmed booking through our platform.
>
> Within our database, booking state transitions and attempt records were committed transactionally. We used uniqueness constraints on idempotency keys and external booking references.
>
> Across the clinic system boundary, we could not use a distributed transaction. We relied on the clinic system’s atomic reservation operation, idempotent request identifiers where supported, and reconciliation for uncertain outcomes.
>
> A booking could move from pending to confirmed, failed, cancelled, or reconciliation-required, but not from a terminal state back to pending. Updates used optimistic version checks so stale workers could not overwrite newer state.
>
> We did not require exactly-once message delivery. The event bus provided at-least-once delivery, and consumers stored processed event IDs or wrote idempotently.
>
> We knew the guarantee held through database constraints, transition tests, duplicate-delivery tests, reconciliation metrics, and audits for duplicate external references.

### Question-by-question answer expectations

#### What invariants were hardest to preserve?

Strong answers state a precise final-state property.

#### How did you preserve correctness under concurrent updates?

The candidate should connect mechanism to conflict pattern.

#### What state transitions needed to be atomic?

Examples:

* debit and credit;
* reserve and status update;
* order and payment record;
* job claim and lease;
* state and outbox event.

#### Where did you rely on database constraints, transactions, locks, optimistic concurrency, queues, or idempotency?

A mature answer explains why each was appropriate.

* constraints protect local invariants;
* transactions group local changes;
* locks serialize access;
* optimistic concurrency detects stale writes;
* queues control ownership or order;
* idempotency handles repeated execution.

#### What would an invalid final state look like?

The candidate should be concrete.

Examples:

* two confirmed bookings for one slot;
* negative inventory;
* both cancelled and fulfilled;
* event published without durable state;
* two active lease owners.

#### Were there operations that needed exactly-once behavior, or was at-least-once with idempotency acceptable?

Strong answers distinguish delivery from effect.

#### What correctness guarantee mattered most to users or the business?

The candidate should translate technical correctness into user or financial consequences.

#### How did you know the system preserved that guarantee?

Good evidence:

* constraints;
* invariant checks;
* tests;
* reconciliation;
* anomaly dashboards;
* audit queries;
* incident history.

### Follow-up probes for the interviewer

* Was the invariant local or distributed?
* What isolation level was used?
* Could a stale worker overwrite state?
* What was the idempotency scope?
* How were duplicate events detected?
* What did the database guarantee directly?
* What required reconciliation?
* Did the invariant ever fail?

### Weak-answer signals

Watch for answers that:

* name mechanisms without invariants;
* claim exactly-once delivery casually;
* rely only on application checks for uniqueness;
* cannot explain transaction boundaries;
* use locks without ownership or timeout semantics;
* ignore stale writes;
* have no evidence the guarantee held;
* describe correctness only as “no errors.”

---


## C. Async workflows and background processing

* Were there background jobs or asynchronous workflows?
* What made those workflows tricky?
* How did work move between synchronous request paths and asynchronous processing?
* How did you handle retries, timeouts, or failed jobs?
* How did you avoid duplicate processing?
* What happened if a worker crashed halfway through a task?
* Did the system need compensation, reconciliation, or cleanup jobs?
* How did you make asynchronous behavior visible to users or operators?

What this reveals:
Whether they understand the correctness and operational complexity introduced by background work and async execution.

### Clarifying questions a strong candidate may ask

* Should I focus on one asynchronous workflow?
* Would you like the request-to-job handoff in detail?
* Should I discuss crash recovery and retries?
* Are you interested in user visibility or operator visibility?
* Should I include compensation and reconciliation?

These questions show that async work creates separate correctness, ownership, and observability concerns.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Trigger**
   * What synchronous action created work?
2. **Durability**
   * Was the work request persisted before response?
3. **Ownership**
   * Which worker claimed it, and how?
4. **Execution**
   * What side effects occurred?
5. **Retry**
   * What failures were retryable?
6. **Crash point**
   * What if the worker stopped after a side effect?
7. **Deduplication**
   * How were repeated jobs made safe?
8. **Terminal failure**
   * Dead letter, manual review, or compensation?
9. **Visibility**
   * How did users and operators know progress?

### Example of a strong coherent answer

> Availability refresh, reminder delivery, event publication, and booking reconciliation were asynchronous.
>
> The synchronous booking path persisted the booking state and an outbox record in one transaction. A publisher later emitted the event. That prevented a confirmed booking from being committed without its event intent being durable.
>
> Workers claimed jobs using queue visibility leases. Processing was at-least-once, so handlers were idempotent. Reminder sends used a deduplication key based on booking, reminder type, and schedule window.
>
> If a worker crashed after calling a clinic system but before updating our database, the job was retried. The external request identifier allowed us to query or deduplicate the operation. If the outcome remained unknown, the booking entered reconciliation.
>
> Repeated failures moved to a dead-letter queue with the error, attempt count, and correlation IDs. Operators could inspect and replay after correcting the cause.
>
> Users saw booking states such as pending confirmation or being verified. Operators saw queue age, retry count, reconciliation status, and stuck-workflow dashboards.

### Question-by-question answer expectations

#### Were there background jobs or asynchronous workflows?

The candidate should identify both business and infrastructure work.

#### What made those workflows tricky?

High-signal issues:

* duplicate delivery;
* uncertain side effects;
* ordering;
* retry timing;
* visibility;
* ownership;
* poison messages;
* state drift.

#### How did work move between synchronous request paths and asynchronous processing?

Strong handoff mechanisms:

* transactional outbox;
* durable queue;
* job table;
* event log;
* commit then publish with recovery.

The candidate should discuss the lost-work window.

#### How did you handle retries, timeouts, or failed jobs?

A mature answer covers retry classification, backoff, maximum attempts, and terminal handling.

#### How did you avoid duplicate processing?

Mechanisms:

* idempotency key;
* unique constraint;
* processed-event table;
* compare-and-set;
* deterministic output key;
* external deduplication ID.

#### What happened if a worker crashed halfway through a task?

The candidate should distinguish crash before side effect, after side effect, and after state update.

#### Did the system need compensation, reconciliation, or cleanup jobs?

Strong answers explain why and what they repaired.

#### How did you make asynchronous behavior visible to users or operators?

Examples:

* status resource;
* progress;
* audit trail;
* queue metrics;
* stuck-state alert;
* replay tool.

### Follow-up probes for the interviewer

* Was the enqueue atomic with state change?
* How long was the visibility lease?
* What happened after max retries?
* Could a job run concurrently twice?
* Was compensation guaranteed?
* How were poison messages isolated?
* Could users leave and return?
* How were stuck workflows detected?

### Weak-answer signals

Watch for answers that:

* fire-and-forget work without durability;
* assume jobs run once;
* have no crash-point reasoning;
* retry every failure indefinitely;
* lack dead-letter or terminal handling;
* cannot explain enqueue consistency;
* hide async progress from users and operators;
* use compensation without defining its limits.

---


## D. Ordering, duplication, and eventual consistency

* Did ordering matter anywhere?
* What happened if events or updates arrived out of order?
* What was eventually consistent, and how did you make that safe?
* Where was stale state acceptable, and where was it dangerous?
* How did you handle duplicate messages, repeated requests, or replayed events?
* Were there cases where two parts of the system could temporarily disagree?
* How did users or downstream systems know when state was final?
* What bug class only appeared under timing variation, reordering, or duplication?

What this reveals:
Whether they understand that distributed and async systems often require explicit reasoning about ordering, duplication, and temporary inconsistency.

### Clarifying questions a strong candidate may ask

* Should I focus on event order, request order, or data freshness?
* Would you like one out-of-order scenario in depth?
* Should I discuss per-key ordering versus global ordering?
* Are you interested in duplicate delivery and replay?
* Should I explain how finality was communicated?

These questions show that ordering and consistency guarantees are usually scoped, not global.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Order domain**
   * Which operations or entity key required ordering?
2. **Guarantee**
   * FIFO per partition, sequence number, version, or no order?
3. **Out-of-order handling**
   * Ignore stale update, buffer, reconcile, or recompute?
4. **Duplicate handling**
   * Deduplicate or apply idempotently?
5. **Eventual consistency**
   * Which copies lagged and for how long?
6. **Safety**
   * What decisions could use stale data?
7. **Finality**
   * How did users or consumers know state was settled?
8. **Bug class**
   * What failed only under timing variation?

### Example of a strong coherent answer

> Ordering mattered for updates to the same booking, but not globally across all bookings.
>
> Each booking event carried an aggregate version. Consumers applied an event only if its version was newer than the version already processed. That prevented a delayed BookingPending event from overwriting BookingConfirmed.
>
> The event bus preserved order within a partition keyed by booking ID, but we still treated duplicates and replay as normal. Consumers used event IDs and idempotent writes.
>
> Search availability was eventually consistent with clinic systems. Bounded staleness was acceptable during browsing, but booking always revalidated against the authoritative source.
>
> Notification and analytics state could temporarily disagree with the booking database. The booking resource was the final operational authority, and consumers could rebuild from events or query status if needed.
>
> One timing-dependent bug occurred when a cancellation event arrived before the consumer had processed the confirmation event. The original consumer rejected cancellation because no booking projection existed. We changed it to use versioned upserts and tolerate missing earlier events during replay.

### Question-by-question answer expectations

#### Did ordering matter anywhere?

The candidate should define the scope:

* per entity;
* per account;
* per partition;
* per workflow;
* global.

Global ordering is rarely necessary and is expensive.

#### What happened if events or updates arrived out of order?

Strong responses:

* sequence check;
* version compare;
* buffer;
* replay;
* state recomputation;
* ignore stale;
* manual reconciliation.

#### What was eventually consistent, and how did you make that safe?

The candidate should name:

* replicas;
* caches;
* search index;
* analytics;
* notification projection;
* external system copy.

They should explain permitted uses during lag.

#### Where was stale state acceptable, and where was it dangerous?

Strong answers connect staleness to decisions.

#### How did you handle duplicate messages, repeated requests, or replayed events?

The candidate should discuss effect-level idempotency.

#### Were there cases where two parts of the system could temporarily disagree?

A mature answer acknowledges divergence and names authority and convergence path.

#### How did users or downstream systems know when state was final?

Mechanisms:

* terminal status;
* version;
* completion event;
* watermark;
* reconciliation result;
* status endpoint.

#### What bug class only appeared under timing variation, reordering, or duplication?

High-signal examples:

* stale overwrite;
* double side effect;
* missing predecessor;
* inconsistent projection;
* premature completion;
* duplicate notification.

### Follow-up probes for the interviewer

* Was ordering per key or global?
* What was the sequence source?
* Could sequence numbers reset?
* How were events replayed?
* What was the consistency window?
* Which state was authoritative?
* Could a stale projection trigger a write?
* How was finality defined?

### Weak-answer signals

Watch for answers that:

* assume queues guarantee global order;
* ignore duplicates;
* say eventual consistency without a convergence mechanism;
* cannot define acceptable staleness;
* let stale projections authorize critical writes;
* cannot identify authority;
* rely on timestamps without clock-skew reasoning;
* have no replay strategy.

---


## E. Coordination strategy and tradeoffs

* What coordination mechanism did you choose, and why?
* Where did you avoid coordination to keep the system simpler or faster?
* Where was coordination unavoidable?
* Did you use locking, leader election, transactions, leases, queues, sagas, or compensating actions?
* What was the cost of that coordination in latency, complexity, or operational risk?
* What would have been simpler in a single-process or single-database design?
* Did the coordination approach ever become a bottleneck?
* What coordination decision would you revisit if the system grew significantly?

What this reveals:
Whether they can choose coordination deliberately and understand the tradeoff between correctness, simplicity, latency, and scalability.

### Clarifying questions a strong candidate may ask

* Should I focus on one coordination mechanism?
* Would you like the mechanism we avoided as well as the one we used?
* Should I discuss local and distributed coordination separately?
* Are you interested in coordination cost or scaling limits?
* Should I explain what I would change at higher scale?

These questions show that coordination should be minimized but not avoided where correctness requires it.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Invariant requiring coordination**
   * What must actors agree on?
2. **Scope**
   * One row, partition, resource, or global singleton?
3. **Mechanism**
   * Transaction, lock, lease, queue, leader, saga, or compensation?
4. **Ownership and expiry**
   * Who holds coordination and for how long?
5. **Failure behavior**
   * Crash, split brain, lease loss, timeout, or partial commit?
6. **Cost**
   * Latency, contention, availability, or operational complexity?
7. **Avoidance**
   * Where could partitioning, idempotency, or commutative operations remove coordination?
8. **Scaling limit**
   * When does the mechanism become a bottleneck?

### Example of a strong coherent answer

> We used database transactions and optimistic concurrency for booking-state updates because the invariant was local to one booking record and its attempts.
>
> We avoided distributed locks for clinic availability search. Search data was a projection, so independent refresh workers could write versioned partitions and stale writes could be rejected.
>
> Coordination was unavoidable for scheduled reconciliation ownership. Workers acquired short leases on booking IDs so only one worker actively reconciled a record. Leases expired automatically if a worker crashed.
>
> For cross-system booking and cancellation, we used saga-like explicit workflow state and compensating actions rather than a distributed transaction. Compensation was best-effort and visible to operators because the external systems did not provide atomic rollback.
>
> The cost of coordination was additional latency, contention, lease management, and more failure states. In a single-process design, in-memory locking would have been simpler, but it would not survive scaling or process failure.
>
> At higher scale, one central reconciliation queue could become a bottleneck. I would partition ownership by clinic or vendor and preserve per-booking serialization rather than introduce global coordination.

### Question-by-question answer expectations

#### What coordination mechanism did you choose, and why?

The candidate should name the invariant and mechanism together.

#### Where did you avoid coordination to keep the system simpler or faster?

Examples:

* partition by key;
* accept eventual consistency;
* use idempotent operations;
* use commutative updates;
* tolerate duplicates;
* derive state independently.

#### Where was coordination unavoidable?

Examples:

* unique reservation;
* leader-only scheduling;
* lease ownership;
* state transition;
* one-time settlement;
* schema migration cutover.

#### Did you use locking, leader election, transactions, leases, queues, sagas, or compensating actions?

A strong answer explains semantics, not just names.

#### What was the cost of that coordination in latency, complexity, or operational risk?

Possible costs:

* contention;
* reduced availability;
* deadlock;
* lock expiry;
* split brain;
* queue hot spot;
* operational recovery;
* difficult testing.

#### What would have been simpler in a single-process or single-database design?

This tests understanding of distribution cost.

#### Did the coordination approach ever become a bottleneck?

The candidate should discuss metrics or symptoms such as lock waits, hot partitions, or leader saturation.

#### What coordination decision would you revisit if the system grew significantly?

Strong answers propose scoped coordination, partitioning, or redesign of the invariant.

### Follow-up probes for the interviewer

* What exactly did the lock protect?
* How did the lease expire?
* Could two leaders exist?
* What happened after partial compensation?
* Was the queue a serialization point?
* Could the operation be made commutative?
* What was the contention rate?
* How would you partition coordination?

### Weak-answer signals

Watch for answers that:

* use distributed locks without lease or failure semantics;
* coordinate globally when per-key scope would work;
* avoid coordination despite a hard invariant;
* use sagas as a buzzword without compensation detail;
* claim compensation restores exact prior state automatically;
* ignore split-brain or lease expiry;
* cannot explain the single-process simplification;
* have no scaling-limit reasoning.

---

# Cross-section answer framework

Candidates can use this structure to answer most concurrency and coordination questions:

1. **Identify the actors**
   * Who can act at the same time?
2. **Identify shared state**
   * What record, resource, or workflow do they touch?
3. **Describe the unsafe interleaving**
   * Which reads and writes can overlap?
4. **State the invariant**
   * What final condition must remain true?
5. **Choose the mechanism**
   * Constraint, transaction, lock, version check, queue, lease, or idempotency.
6. **Cover async execution**
   * What happens on retry, crash, and duplicate delivery?
7. **Define ordering and consistency**
   * What is ordered, what may lag, and what is authoritative?
8. **Explain coordination cost**
   * Latency, contention, failure modes, and operations.
9. **Describe verification**
   * Tests, invariant checks, reconciliation, and production metrics.
10. **Reflect**
   * What would change at higher scale?

A strong answer treats concurrency as a correctness problem first and a performance problem second.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* identifies concrete concurrent actors and shared state;
* describes unsafe interleavings precisely;
* connects mechanisms to explicit invariants;
* understands atomic transitions and stale-write prevention;
* distinguishes delivery guarantees from effect guarantees;
* designs async handoff durably;
* handles worker crashes and duplicate processing;
* reasons about scoped ordering and replay;
* names authoritative and eventually consistent state;
* uses coordination only where required;
* explains lock, lease, queue, or saga failure semantics;
* identifies coordination bottlenecks and scaling paths.

## Mixed signal

The candidate:

* recognizes races but weakly explains interleavings;
* uses transactions correctly but has limited distributed reasoning;
* handles retries but weakly covers crash-after-side-effect cases;
* understands eventual consistency but not finality;
* chooses coordination mechanisms without fully discussing costs.

## Weak signal

The candidate:

* treats concurrency only as throughput;
* cannot identify shared state;
* claims transactions or locks solve everything;
* assumes exactly-once delivery;
* has no idempotency or crash-recovery story;
* assumes queues guarantee global order;
* cannot define convergence or authority;
* uses distributed locks without lease semantics;
* avoids coordination where invariants require it.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. Which actors could mutate the same state?
2. What was the most dangerous race?
3. What exact interleaving caused it?
4. Which invariant was at risk?
5. What mechanism protected it?
6. Which state transition had to be atomic?
7. What async workflow was hardest?
8. What happened if a worker crashed after a side effect?
9. How were duplicates and replay handled?
10. What ordering guarantee existed?
11. Where was coordination unavoidable?
12. What coordination decision would change at 10x scale?

A strong response should demonstrate explicit interleaving analysis, invariant-driven controls, safe async execution, scoped ordering, idempotent effects, and deliberate coordination tradeoffs.
