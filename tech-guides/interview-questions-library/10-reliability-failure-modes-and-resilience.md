# 10. Reliability, failure modes, and resilience

These questions test whether the candidate can reason beyond the happy path. The goal is to see whether they understand how systems fail, how failures spread, how to reduce blast radius, and how to design graceful behavior under stress, bad inputs, dependency problems, and operational mistakes.

## Table of contents

- [A. Failure modes and risk classification](#a-failure-modes-and-risk-classification)
- [B. Dependency failure and partial failure](#b-dependency-failure-and-partial-failure)
- [C. Degradation, recovery, and user impact](#c-degradation-recovery-and-user-impact)
- [D. Bad inputs, bad data, and operator error](#d-bad-inputs-bad-data-and-operator-error)
- [E. Resilience tradeoffs and lessons learned](#e-resilience-tradeoffs-and-lessons-learned)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched across clinics, booked or cancelled appointments, and received reminders. The platform depended on several external clinic scheduling systems with different latency and failure behavior, maintained durable booking workflow state, and supported operational reconciliation when outcomes were uncertain.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can identify realistic failure modes, prioritize risk, contain dependency failure, design graceful degradation and recovery, protect against bad data and human error, and discuss resilience as a tradeoff rather than a checklist.



## A. Failure modes and risk classification

* What were the most likely ways this system could fail?
* Which failures were acceptable, and which were catastrophic?
* What failures would users notice immediately?
* What failures could remain silent for a long time?
* What failure mode worried you the most?
* What scenario kept you up at night?
* Were there any failures that looked unlikely but would have had a high impact?
* How did you decide which risks were worth designing around?

What this reveals:
Whether they can identify and prioritize realistic failure modes instead of treating reliability as a vague concern.

### Clarifying questions a strong candidate may ask

* Should I focus on user-facing failures, data-integrity failures, or operational failures?
* Would you like the most likely risks or the highest-impact risks?
* Should I discuss failures known during design or those discovered in production?
* Are you interested in one failure scenario in depth?
* Should I explain how we ranked and mitigated risks?

These questions show that failure analysis requires prioritization. Frequency, impact, detectability, and recoverability all matter.

### Reasoning expected from the candidate

A strong answer should classify failures along dimensions such as:

1. **Likelihood**
   * How often could this happen?
2. **Impact**
   * User harm, financial loss, data corruption, security exposure, or downtime?
3. **Detectability**
   * Immediate alert or silent drift?
4. **Recoverability**
   * Automatic retry, manual repair, or irreversible harm?
5. **Blast radius**
   * One request, one tenant, one region, or the whole system?
6. **Time sensitivity**
   * Does delayed recovery increase harm?
7. **Risk treatment**
   * Prevent, detect, contain, degrade, reconcile, or accept?

A mature candidate distinguishes between:

* **availability failure:** service cannot respond;
* **correctness failure:** service responds incorrectly;
* **integrity failure:** data becomes contradictory or lost;
* **security failure:** trust boundary is violated;
* **operational failure:** humans cannot diagnose or recover;
* **silent failure:** outputs look normal while state is wrong.

### Example of a strong coherent answer

> The most likely failures were external clinic API timeouts, stale availability, malformed vendor responses, notification delays, and transient database or queue issues.
>
> Some failures were acceptable in a bounded form. A search result could be a few minutes stale, or a reminder could be delayed briefly, as long as the final booking confirmation remained correct and support could identify the issue.
>
> Catastrophic failures included duplicate confirmed bookings, cross-patient data exposure, silently lost cancellations, or a migration that corrupted booking state.
>
> Users would notice search or booking outages immediately. Silent reconciliation failures were more dangerous because a booking might remain uncertain for hours without a visible error.
>
> The scenario that worried me most was a timeout after the external clinic system had actually committed the booking. A naive retry could create duplicate work, while treating the timeout as failure could mislead the patient. We designed an explicit uncertain state, idempotency, and reconciliation around that case.
>
> We prioritized risks using likelihood, user harm, detectability, and recovery cost. We invested most in failures that affected correctness or could remain silent, even if they were less frequent than visible availability issues.

### Question-by-question answer expectations

#### What were the most likely ways this system could fail?

Strong answers include realistic categories:

* dependency timeout;
* queue backlog;
* stale cache;
* malformed input;
* data corruption;
* bad deployment;
* lost event;
* duplicate processing;
* configuration error;
* capacity saturation.

#### Which failures were acceptable, and which were catastrophic?

The candidate should define the boundary.

Acceptable failures are usually:

* bounded;
* detectable;
* reversible;
* low-impact;
* gracefully degraded.

Catastrophic failures often involve:

* irreversible user harm;
* data corruption;
* security breach;
* financial loss;
* silent incorrectness;
* broad blast radius.

#### What failures would users notice immediately?

Examples:

* outage;
* high latency;
* missing results;
* failed checkout;
* broken login;
* visible inconsistency.

#### What failures could remain silent for a long time?

High-signal examples:

* dropped events;
* incomplete backfills;
* stale replicas;
* reconciliation gaps;
* incorrect analytics;
* missing audit records;
* partial data corruption.

#### What failure mode worried you the most?

The candidate should choose one and explain likelihood, impact, and mitigation.

#### What scenario kept you up at night?

A strong answer is concrete rather than theatrical.

Examples:

* timeout after commit;
* wrong-tenant access;
* undetected duplicate charge;
* irreversible migration corruption;
* queue poison-message blockage.

#### Were there any failures that looked unlikely but would have had a high impact?

The candidate should discuss low-frequency, high-severity events and proportional safeguards.

#### How did you decide which risks were worth designing around?

Useful methods:

* risk matrix;
* failure-mode analysis;
* threat modeling;
* incident history;
* business impact;
* compliance requirements;
* error budget;
* game days;
* tabletop exercises.

### Follow-up probes for the interviewer

* Which failure was hardest to detect?
* Which failure had the largest blast radius?
* What was the recovery time?
* What was the business impact?
* Which risk did you consciously accept?
* What failure was initially underestimated?
* How did you validate mitigation?
* What would be catastrophic despite low traffic?

### Weak-answer signals

Watch for answers that:

* discuss only crashes and outages;
* ignore silent incorrectness;
* cannot rank risks;
* call every failure catastrophic;
* have no blast-radius reasoning;
* rely on low probability as the only mitigation;
* cannot identify a high-impact scenario;
* treat reliability as uptime only.

---


## B. Dependency failure and partial failure

* What happened if one dependency became slow or unavailable?
* How did the system behave if only part of a workflow failed?
* Were there external services, databases, queues, APIs, or clients that could fail independently?
* How did you think about timeouts, retries, backoff, and circuit breaking?
* Did the system ever risk doing duplicate work after a retry?
* How did you prevent retry storms or cascading failure?
* What failure in a dependency had the largest blast radius?
* How would you test the system’s behavior during dependency outages?

What this reveals:
Whether they understand that real systems fail partially, and that dependency behavior changes correctness, latency, and reliability.

### Clarifying questions a strong candidate may ask

* Should I focus on one critical dependency or the dependency graph overall?
* Would you like slow-dependency behavior as well as complete outage?
* Should I discuss synchronous and asynchronous dependencies separately?
* Are you interested in retries, circuit breaking, or partial workflow state?
* Should I include how outages were tested?

These questions show that dependency failure is not binary. Slowness, intermittent errors, bad responses, and ambiguous outcomes are often more difficult than total outage.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Dependency role**
   * What capability did it provide?
2. **Failure modes**
   * Slow, unavailable, incorrect, rate-limited, or partially successful?
3. **Timeout**
   * How long did the caller wait?
4. **Retry safety**
   * Could the operation be repeated?
5. **Backoff and limits**
   * How were retries bounded and jittered?
6. **Isolation**
   * Could failure consume all threads, connections, or workers?
7. **Partial workflow**
   * What durable state remained?
8. **Recovery**
   * Queue, reconcile, compensate, or expose pending status?
9. **Testing**
   * How was outage behavior validated?

### Example of a strong coherent answer

> The clinic scheduling APIs were the most critical dependencies. Search could continue from cached availability for a bounded period, but booking confirmation required an authoritative response or an explicit uncertain outcome.
>
> We set dependency-specific timeouts based on observed latency and user-flow budgets. Retries used exponential backoff with jitter and were only enabled for operations known to be idempotent or protected by an idempotency key.
>
> If a vendor became slow, we applied per-vendor concurrency limits and circuit breaking so it could not exhaust the entire worker pool. Search degraded to cached results with freshness indicators. Booking requests entered a pending or reconciliation-required state rather than retrying blindly.
>
> Partial workflow failure was expected. A booking could be persisted internally while notification publication failed. The booking remained confirmed, and an outbox process retried the event separately.
>
> We prevented retry storms with bounded attempts, backoff, jitter, queue-level rate controls, and shared circuit state. We tested dependency outages using fault injection, fake adapters, delayed responses, malformed payloads, and staging game days.

### Question-by-question answer expectations

#### What happened if one dependency became slow or unavailable?

The candidate should distinguish slow, unavailable, and incorrect behavior.

#### How did the system behave if only part of a workflow failed?

Strong answers discuss durable intermediate state, independent retries, and user-visible status.

#### Were there external services, databases, queues, APIs, or clients that could fail independently?

The candidate should map independent failure domains rather than treating the system as one unit.

#### How did you think about timeouts, retries, backoff, and circuit breaking?

A mature answer covers:

* timeout budget;
* idempotency;
* bounded retries;
* exponential backoff;
* jitter;
* circuit thresholds;
* half-open testing;
* telemetry.

#### Did the system ever risk doing duplicate work after a retry?

High-signal examples:

* duplicate booking;
* duplicate charge;
* duplicate message;
* repeated job;
* repeated external mutation.

The candidate should explain deduplication or idempotency.

#### How did you prevent retry storms or cascading failure?

Mechanisms:

* bounded retries;
* jitter;
* backpressure;
* circuit breakers;
* rate limits;
* bulkheads;
* queue smoothing;
* load shedding.

#### What failure in a dependency had the largest blast radius?

The candidate should identify why the dependency was central and how blast radius was reduced.

#### How would you test the system’s behavior during dependency outages?

Strong methods:

* fault injection;
* network delay;
* error simulation;
* malformed data;
* queue pause;
* database failover;
* game day;
* chaos test;
* synthetic monitoring.

### Follow-up probes for the interviewer

* What was the timeout value and why?
* Was the retry safe?
* What happened after all retries failed?
* Did the circuit breaker operate per vendor or globally?
* Could one dependency consume all connections?
* How was partial completion exposed?
* Were poison messages isolated?
* What outage surprised the team?

### Weak-answer signals

Watch for answers that:

* retry every failure automatically;
* have no timeout budget;
* ignore slow dependencies;
* treat timeout as definite failure;
* lack idempotency;
* use global retries that amplify outages;
* have no isolation or backpressure;
* test only happy-path integrations.

---


## C. Degradation, recovery, and user impact

* How did you decide whether the system should fail open, fail closed, queue work, serve stale data, or disable features?
* What degraded behavior was acceptable?
* What behavior needed to stop completely if the system could not guarantee correctness?
* How did the system recover after a temporary failure?
* Were users able to retry safely?
* Were there workflows that needed reconciliation after recovery?
* What did the user experience look like during degraded operation?
* How did you balance availability against correctness?

What this reveals:
Whether they can design controlled degradation and recovery paths rather than assuming the system is either fully working or fully down.

### Clarifying questions a strong candidate may ask

* Should I focus on fail-open versus fail-closed decisions?
* Would you like one degraded mode in depth?
* Should I discuss user experience during recovery?
* Are you interested in automatic recovery, manual reconciliation, or both?
* Should I explain how availability was balanced against correctness?

These questions show that degraded operation should be intentional and tied to risk.

### Reasoning expected from the candidate

A strong answer should evaluate each function by:

1. **Criticality**
   * Is incorrect behavior worse than unavailability?
2. **Freshness**
   * Can stale data be served safely?
3. **Recoverability**
   * Can work be queued or replayed?
4. **User harm**
   * What misleading behavior must be avoided?
5. **Dependency**
   * Is there a safe fallback?
6. **Finality**
   * Can the system expose pending state?
7. **Recovery**
   * How does normal operation resume?
8. **Reconciliation**
   * How are uncertain or divergent records repaired?

A mature candidate avoids one global fail-open or fail-closed rule. Different capabilities require different choices.

### Example of a strong coherent answer

> Search failed open to bounded stale availability because the result was advisory and final booking revalidated it. Booking confirmation failed closed when the system had a definitive inability to guarantee correctness.
>
> When the outcome was uncertain, we did not classify it as either success or failure. We persisted a reconciliation-required state and told the patient that confirmation was still being checked.
>
> Reminder delivery could queue and retry because delay was safer than duplicate or lost scheduling state. Analytics could lag without affecting the operational workflow.
>
> During degraded operation, the UI displayed available clinics from the last successful refresh and disabled unsupported actions rather than failing the entire application. It preserved the user’s filters and explained when a result needed reconfirmation.
>
> Recovery involved draining queued work, refreshing stale read models, and reconciling uncertain bookings against clinic systems. Users could retry safely when an idempotency key or status check made the operation unambiguous.
>
> We favored correctness over availability for final booking state, but favored availability over freshness for search.

### Question-by-question answer expectations

#### How did you decide whether to fail open, fail closed, queue work, serve stale data, or disable features?

The candidate should tie the decision to user harm and correctness.

#### What degraded behavior was acceptable?

Examples:

* stale read-only data;
* disabled optional features;
* delayed notification;
* queued export;
* reduced result set;
* manual fallback.

#### What behavior needed to stop completely if the system could not guarantee correctness?

Examples:

* payment capture;
* booking confirmation;
* permission grant;
* destructive write;
* final settlement;
* security-sensitive action.

#### How did the system recover after a temporary failure?

Strong answers include:

* retry;
* queue replay;
* state rebuild;
* cache refresh;
* dependency health check;
* backfill;
* reconciliation;
* operator workflow.

#### Were users able to retry safely?

The candidate should explain idempotency, conflict detection, or status lookup.

#### Were there workflows that needed reconciliation after recovery?

High-signal examples involve uncertain external side effects, dropped events, or temporary divergence.

#### What did the user experience look like during degraded operation?

A strong answer is concrete:

* message;
* available alternatives;
* preserved state;
* retry timing;
* visible pending status;
* support reference.

#### How did you balance availability against correctness?

The candidate should make the tradeoff explicit per capability.

### Follow-up probes for the interviewer

* Which data was safe to serve stale?
* What feature was disabled first?
* What did “pending” mean?
* How long could reconciliation take?
* Could users leave and return?
* What happened if recovery replayed duplicates?
* Was degraded mode tested?
* Which fallback was misleading and removed?

### Weak-answer signals

Watch for answers that:

* use one fail-open or fail-closed rule everywhere;
* serve stale authoritative data;
* hide uncertain outcomes as failure;
* have no recovery sequence;
* let users retry unsafe mutations;
* fail the whole product when one optional dependency fails;
* ignore user communication;
* cannot explain reconciliation.

---


## D. Bad inputs, bad data, and operator error

* What did the system do under bad inputs or malformed requests?
* What kinds of invalid state or bad data were most dangerous?
* What protections existed against accidental bad writes or destructive actions?
* What protections existed against operator error?
* What was the blast radius of a bad deployment, configuration change, or data migration?
* Were there guardrails, validation layers, approvals, dry runs, or rollback mechanisms?
* What kind of mistake could a well-intentioned engineer or operator make?
* What part of the design looked safe but was actually fragile?

What this reveals:
Whether they think about reliability as including human mistakes, malformed data, and operational risk, not just server crashes.

### Clarifying questions a strong candidate may ask

* Should I focus on external bad inputs, internal bad data, or operator mistakes?
* Would you like one deployment or migration risk in depth?
* Should I include preventive and detective controls?
* Are you interested in destructive-action safeguards?
* Should I explain how blast radius was limited?

These questions show that reliability includes adversarial, accidental, and operational error.

### Reasoning expected from the candidate

A strong answer should cover:

1. **Input validation**
   * Shape, type, range, ownership, and semantic validity?
2. **Data quality**
   * How were malformed or contradictory records handled?
3. **Write protection**
   * Constraints, transactions, preconditions, and idempotency?
4. **Operator safety**
   * Least privilege, approvals, dry runs, and reversible actions?
5. **Deployment safety**
   * Canary, feature flag, rollback, and compatibility?
6. **Migration safety**
   * Backups, checksums, dual reads, sampling, and pause controls?
7. **Blast radius**
   * Tenant, partition, environment, or percentage rollout?
8. **Detection**
   * Alerts, audits, and anomaly checks?

### Example of a strong coherent answer

> External requests were schema-validated and semantically checked. We rejected invalid time ranges, unknown clinic identifiers, expired availability references, and cross-tenant resource access.
>
> Vendor data was treated as untrusted even though it came from partners. Malformed records were quarantined, counted, and excluded from search rather than partially interpreted.
>
> Critical writes used database constraints, version preconditions, and transactional state transitions. Destructive support actions required elevated permissions, a reason, and an audit record.
>
> Operator tooling defaulted to read-only. Bulk actions supported dry-run mode and displayed the exact number and scope of affected records. High-impact changes required a second approval.
>
> Deployments used canaries, feature flags, health checks, and automated rollback. Schema changes followed expand-and-contract so old and new code could coexist.
>
> The largest migration risk was a backfill that could mark stale bookings as active. We processed one clinic at a time, validated counts and samples, and had a pause and rollback plan.
>
> A fragile design area was configuration. One malformed mapping could affect every search for a clinic. We added schema validation, staged rollout, and versioned configuration after an incident.

### Question-by-question answer expectations

#### What did the system do under bad inputs or malformed requests?

Strong answers distinguish rejection, normalization, quarantine, and safe defaults.

#### What kinds of invalid state or bad data were most dangerous?

Examples:

* cross-tenant ownership;
* contradictory workflow state;
* duplicate financial record;
* malformed permission;
* missing source reference;
* corrupted migration;
* incorrect unit or timezone.

#### What protections existed against accidental bad writes or destructive actions?

Mechanisms:

* constraints;
* transactions;
* preconditions;
* confirmation;
* dry run;
* approval;
* audit;
* soft delete;
* undo;
* backups.

#### What protections existed against operator error?

Strong answers discuss human-centered design, not just access control.

#### What was the blast radius of a bad deployment, configuration change, or data migration?

The candidate should identify how rollout scope was bounded.

#### Were there guardrails, validation layers, approvals, dry runs, or rollback mechanisms?

A mature answer explains which control matched which risk.

#### What kind of mistake could a well-intentioned engineer or operator make?

High-signal examples:

* run against production;
* select wrong tenant;
* retry a non-idempotent action;
* load unvalidated configuration;
* skip a migration step;
* interpret timezone incorrectly.

#### What part of the design looked safe but was actually fragile?

The candidate should name hidden coupling or unsafe assumptions.

### Follow-up probes for the interviewer

* Was bad partner data quarantined?
* Could a bulk action be previewed?
* What required two-person approval?
* How was rollback tested?
* What was the smallest rollout unit?
* Could an operator affect all tenants?
* Were migrations resumable?
* What mistake actually happened?

### Weak-answer signals

Watch for answers that:

* trust internal or partner data blindly;
* rely only on UI validation;
* have destructive admin tools with broad defaults;
* cannot bound deployment blast radius;
* perform migrations without validation or pause controls;
* use backups as the only rollback plan;
* ignore operator ergonomics;
* cannot identify a fragile assumption.

---


## E. Resilience tradeoffs and lessons learned

* What reliability tradeoffs did you knowingly make?
* Where did you accept a higher failure risk because the alternative was too complex or expensive?
* Where did you add complexity specifically to improve resilience?
* Tell me about a failure mode you discovered late. Why was it easy to miss?
* Did any reliability mechanism create new complexity or new failure modes?
* What would you redesign to make the system more resilient?
* What resilience improvement gave the most leverage?
* What did operating or testing the system teach you about its real failure behavior?

What this reveals:
Whether they can reflect on resilience as a set of design tradeoffs with costs, not just a checklist of protective mechanisms.

### Clarifying questions a strong candidate may ask

* Should I focus on one resilience tradeoff or several?
* Would you like a mechanism that created a new failure mode?
* Should I discuss decisions made under cost or delivery constraints?
* Are you interested in lessons from incidents, testing, or both?
* Should I explain what I would redesign under the same constraints?

These questions show that resilience improvements have costs and can create new complexity.

### Reasoning expected from the candidate

A strong retrospective should explain:

1. **Reliability goal**
   * What failure was being reduced?
2. **Mechanism**
   * Retry, replication, queue, circuit breaker, fallback, or reconciliation?
3. **Cost**
   * Complexity, latency, stale data, duplicated state, or operations?
4. **New risk**
   * Retry storm, split brain, hidden backlog, stale cache, or delayed failure?
5. **Observed outcome**
   * What happened in testing or production?
6. **Lesson**
   * Which principle changed future design?
7. **Redesign**
   * What would improve resilience without unnecessary complexity?

### Example of a strong coherent answer

> We knowingly accepted limited search staleness because fully live fan-out would have made availability dependent on every clinic system. That was a reliability tradeoff in favor of availability and isolation.
>
> We added durable workflow state, idempotency, an outbox, and reconciliation to improve booking resilience. Those mechanisms increased schema complexity and operational tooling needs.
>
> A failure mode we discovered late was a poison event that repeatedly failed and blocked one consumer partition. It was easy to miss because normal retry tests used transient failures. We added dead-letter handling, per-message visibility, and replay tooling.
>
> Circuit breaking improved dependency isolation, but an early global breaker caused healthy clinics to be affected by one failing vendor. We changed it to operate per vendor and operation.
>
> The highest-leverage improvement was making uncertain outcomes explicit. Once the system had a durable pending/reconciliation state, retries, support workflows, and user communication became safer.
>
> If redesigning, I would add operability earlier: queue age dashboards, reconciliation ownership, replay tooling, and clearer runbooks. Production taught us that resilience mechanisms are only useful if people can see and control them.

### Question-by-question answer expectations

#### What reliability tradeoffs did you knowingly make?

Examples:

* availability versus freshness;
* correctness versus latency;
* redundancy versus cost;
* consistency versus partition tolerance;
* automation versus operator control;
* delivery speed versus fault isolation.

#### Where did you accept a higher failure risk because the alternative was too complex or expensive?

A strong answer describes containment and monitoring.

#### Where did you add complexity specifically to improve resilience?

Examples:

* retries;
* idempotency;
* circuit breakers;
* replication;
* durable queues;
* reconciliation;
* multi-region;
* outbox.

#### Tell me about a failure mode you discovered late. Why was it easy to miss?

High-signal answers explain hidden assumptions or unrealistic test conditions.

#### Did any reliability mechanism create new complexity or new failure modes?

Examples:

* retry storms;
* stale fallback;
* queue backlog;
* cache inconsistency;
* replica lag;
* split brain;
* circuit flapping.

#### What would you redesign to make the system more resilient?

Strong answers include architecture and operability.

#### What resilience improvement gave the most leverage?

The candidate should explain why one mechanism solved several classes of failure.

#### What did operating or testing the system teach you about its real failure behavior?

Good answers compare expected and observed behavior.

### Follow-up probes for the interviewer

* What new failure did the mechanism create?
* How was the tradeoff measured?
* Which resilience feature was too expensive?
* What was accepted rather than fixed?
* What did the incident reveal?
* Could operators see the mechanism working?
* What would you remove?
* Which lesson changed later systems?

### Weak-answer signals

Watch for answers that:

* present resilience as free;
* add retries, caches, or replication without discussing new risks;
* cannot name an accepted risk;
* have no late-discovered failure;
* focus only on architecture and ignore operability;
* claim all resilience mechanisms worked as intended;
* redesign everything without original constraints;
* cannot identify a highest-leverage improvement.

---

# Cross-section answer framework

Candidates can use this structure to answer most reliability questions:

1. **Name the failure**
   * What could go wrong?
2. **Classify the risk**
   * Likelihood, impact, detectability, recoverability, and blast radius.
3. **Describe propagation**
   * How could the failure spread?
4. **Choose the response**
   * Prevent, isolate, degrade, queue, retry, fail closed, or reconcile.
5. **Preserve correctness**
   * What invariant must remain true?
6. **Explain user impact**
   * What would users see or be able to do?
7. **Describe recovery**
   * How does the system return to normal and repair uncertain state?
8. **Cover human error**
   * What guardrails protect operators and deployments?
9. **State the tradeoff**
   * What complexity or cost did resilience introduce?
10. **Reflect**
   * What did production reveal that design review missed?

A strong answer shows that reliability is a system property involving code, dependencies, data, users, and operators.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* identifies availability, correctness, integrity, and silent-failure risks;
* prioritizes risk by likelihood, impact, detectability, and recovery;
* understands slow and partial dependency failure;
* uses timeouts, retries, backoff, and circuit breaking selectively;
* reasons about idempotency and uncertain outcomes;
* prevents retry storms and cascading failure;
* chooses degradation behavior per capability;
* explains recovery and reconciliation;
* protects against malformed data and operator error;
* bounds deployment and migration blast radius;
* discusses resilience costs and new failure modes;
* reflects on lessons from production or realistic testing.

## Mixed signal

The candidate:

* identifies realistic failures but weakly prioritizes them;
* understands retries but not timeout uncertainty;
* has graceful degradation but limited reconciliation;
* uses operational safeguards but lacks clear blast-radius reasoning;
* discusses resilience mechanisms but weakly explains their costs.

## Weak signal

The candidate:

* treats reliability as uptime only;
* retries every failure automatically;
* has no idempotency or backpressure reasoning;
* cannot distinguish stale-safe from stale-dangerous data;
* hides uncertain outcomes;
* has no recovery or reconciliation path;
* trusts internal data and operators implicitly;
* performs broad deployments or migrations without safeguards;
* presents resilience mechanisms as cost-free.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What were the three most likely failure modes?
2. Which failure was catastrophic?
3. Which failure could remain silent?
4. What dependency had the largest blast radius?
5. What happened when it became slow?
6. Which operations were safe to retry?
7. How did the system prevent duplicate work?
8. What degraded behavior was acceptable?
9. What state required reconciliation?
10. What operator or deployment mistake was most dangerous?
11. What resilience mechanism created a new failure mode?
12. What would you redesign after operating the system?

A strong response should demonstrate realistic risk classification, controlled partial failure, safe degradation, recoverable workflows, bounded human error, and honest tradeoff reasoning.
