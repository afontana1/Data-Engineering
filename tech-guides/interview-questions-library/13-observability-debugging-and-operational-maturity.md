# 13. Observability, debugging, and operational maturity

These questions distinguish candidates who only build systems from candidates who understand how systems behave in production. The goal is to see whether they can reason about health, diagnosis, alerts, debugging, and operational feedback loops.

## Table of contents

- [A. Health signals and production visibility](#a-health-signals-and-production-visibility)
- [B. Debugging user-facing issues](#b-debugging-user-facing-issues)
- [C. Cross-service and distributed debugging](#c-cross-service-and-distributed-debugging)
- [D. Alerts, incidents, and operational response](#d-alerts-incidents-and-operational-response)
- [E. Feedback from production into design](#e-feedback-from-production-into-design)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched for appointments, booked or cancelled visits, and received reminders. The platform included a web client, APIs, booking workflow state, asynchronous workers, an event bus, vendor-specific clinic integrations, caches, and support tooling.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can define health in user and system terms, move from vague symptoms to evidence, trace work across synchronous and asynchronous boundaries, distinguish page-worthy incidents from lower-priority issues, and feed operational learning back into design.



## A. Health signals and production visibility

* How did you know the system was healthy?
* What metrics, logs, traces, dashboards, or events mattered most?
* Which signals reflected user experience?
* Which signals reflected internal system health?
* What were the most important leading indicators of trouble?
* What could be broken even if the main dashboard looked fine?
* Which failures were easy to detect, and which were silent?
* What did you wish you had instrumented earlier?

What this reveals:
Whether they understand that production health needs explicit signals, and that “it is running” is not the same as “it is working.”

### Clarifying questions a strong candidate may ask

* Should I focus on user-visible health, infrastructure health, or both?
* Would you like the most important service-level indicators?
* Should I discuss synchronous and asynchronous paths separately?
* Are you interested in leading indicators or incident symptoms?
* Should I include observability gaps we discovered later?

These questions show that health is multidimensional. A process can be running while users are unable to complete the core workflow.

### Reasoning expected from the candidate

A strong answer should define:

1. **Critical user journeys**
   * Search, booking, cancellation, login, or another core outcome?
2. **Service-level indicators**
   * Success rate, latency, freshness, completion time, or correctness?
3. **Internal health**
   * Saturation, queue lag, dependency latency, cache age, error rate?
4. **Leading indicators**
   * What deteriorates before users experience full failure?
5. **Silent failure**
   * What can drift without obvious errors?
6. **Segmentation**
   * Can health be viewed by tenant, region, vendor, client, or operation?
7. **Coverage**
   * Are logs, metrics, traces, and domain events complementary?
8. **Gap**
   * What signal was missing initially?

A mature answer distinguishes:

* **availability:** can the system respond?
* **correctness:** is the answer right?
* **freshness:** is the answer current enough?
* **completion:** did the workflow finish?
* **operability:** can the team explain what happened?

### Example of a strong coherent answer

> We defined health around the patient journey, not only server uptime.
>
> The primary user-facing signals were search success rate, p95 and p99 search latency, booking confirmation rate, time spent in pending state, cancellation completion rate, and the percentage of results served beyond the allowed freshness window.
>
> Internal signals included API saturation, database connection use, queue depth and age, cache hit rate, per-vendor latency and error rate, retry volume, reconciliation backlog, and event-consumer lag.
>
> The most useful leading indicators were rising queue age, vendor throttling, cache age, and the ratio of bookings entering reconciliation. Those often degraded before the overall booking success rate dropped.
>
> A silent failure could occur if booking events stopped reaching the notification service while booking itself remained healthy. The main API dashboard would look normal, but reminders would not be sent. We therefore tracked domain-event production versus consumption and synthetic end-to-end journeys.
>
> Search and booking failures were easy to detect. Stale clinic mappings and stuck reconciliation were harder because requests still returned successfully.
>
> I wish we had instrumented workflow-state age and per-clinic data freshness from the beginning. Aggregate system metrics hid a small number of clinics with serious issues.

### Question-by-question answer expectations

#### How did you know the system was healthy?

A strong answer names user outcomes and system conditions rather than saying “the dashboard was green.”

#### What metrics, logs, traces, dashboards, or events mattered most?

The candidate should explain the role of each:

* metrics for trends and alerting;
* logs for detailed events;
* traces for path timing and dependency contribution;
* dashboards for operational views;
* domain events for business outcomes.

#### Which signals reflected user experience?

Examples:

* page interaction time;
* workflow success rate;
* abandonment;
* freshness;
* pending duration;
* failed confirmation;
* error-message frequency.

#### Which signals reflected internal system health?

Examples:

* CPU;
* memory;
* queue lag;
* connection saturation;
* error rate;
* retry volume;
* lock wait;
* cache hit rate;
* dependency latency.

#### What were the most important leading indicators of trouble?

High-signal answers identify precursors rather than outage symptoms.

Examples:

* rising saturation;
* queue growth;
* cache age;
* retry rate;
* error-budget burn;
* throttling;
* reconciliation backlog.

#### What could be broken even if the main dashboard looked fine?

Examples:

* one tenant;
* one vendor;
* one region;
* async consumer;
* stale data;
* rare workflow;
* client-side rendering;
* silent event loss.

#### Which failures were easy to detect, and which were silent?

A mature candidate explains detection gaps and compensating signals.

#### What did you wish you had instrumented earlier?

Strong answers identify a real missing dimension and the operational cost it created.

### Follow-up probes for the interviewer

* What was the primary service-level objective?
* Which metric was closest to user value?
* Could one clinic be broken while aggregates looked healthy?
* What was the freshness signal?
* How were silent failures detected?
* Were synthetic journeys used?
* Which dashboard did on-call open first?
* What did operators still need logs for?

### Weak-answer signals

Watch for answers that:

* define health as host or process uptime;
* rely on one aggregate dashboard;
* cannot name user-facing indicators;
* ignore async completion and freshness;
* have no leading indicators;
* cannot identify silent failure;
* collect logs without structured fields;
* have no visibility by tenant, region, or dependency.

---


## B. Debugging user-facing issues

* How would you diagnose a user report that “the system is slow”?
* How would you distinguish frontend issues from backend issues?
* How would you trace a failed or slow user action end to end?
* What information would you want from the user report?
* What logs or traces would you check first?
* How would you tell whether the issue affected one user, one tenant, one region, or everyone?
* What made user-facing bugs hard to reproduce?
* What debugging workflow became easier after better instrumentation?

What this reveals:
Whether they can move from vague symptoms to evidence-based diagnosis across the full stack.

### Clarifying questions a strong candidate may ask

* Should I diagnose a single-user report or a broad degradation?
* Would you like the frontend-to-backend path step by step?
* Should I include browser and network evidence?
* Are you interested in the information needed from the reporter?
* Should I explain how scope was narrowed?

These questions show that user reports are symptoms that must be translated into reproducible and measurable conditions.

### Reasoning expected from the candidate

A strong debugging workflow should:

1. **Clarify the symptom**
   * Slow compared with what, and at which action?
2. **Gather context**
   * Time, user, tenant, browser, device, request ID, region, and steps?
3. **Establish scope**
   * One user, one client, one tenant, one region, or global?
4. **Split the path**
   * Client rendering, network, API, database, queue, or dependency?
5. **Correlate evidence**
   * Real-user monitoring, browser timing, traces, logs, and metrics?
6. **Compare baseline**
   * What differs from healthy cases?
7. **Reproduce**
   * Use equivalent data, permissions, device, and timing.
8. **Validate**
   * Confirm the fix from the user’s perspective.

### Example of a strong coherent answer

> If a user reported that “the system is slow,” I would first identify the exact action: initial page load, changing search filters, opening appointment details, or booking confirmation.
>
> I would ask for the approximate time, clinic or tenant, browser and device, whether the problem was repeatable, and any request or support reference shown in the UI.
>
> I would compare real-user monitoring for that interaction with backend latency for the same period. If browser time was high but API time was normal, I would inspect bundle loading, rendering, client errors, and network timing. If API time was high, I would open the distributed trace and break down database, cache, serialization, and vendor time.
>
> I would segment by clinic, region, client version, and endpoint to determine scope. A problem affecting one clinic usually pointed to data skew or a vendor integration, while all users suggested platform saturation or a release issue.
>
> User-facing bugs were hard to reproduce when they depended on patient permissions, stale client cache, specific clinic data, or a narrow race.
>
> Instrumentation improved debugging once every user action carried a correlation ID visible in support tooling and traces. Support could move directly from a user report to the exact backend workflow.

### Question-by-question answer expectations

#### How would you diagnose a user report that “the system is slow”?

A strong answer turns the vague symptom into:

* exact interaction;
* time window;
* percentile;
* affected scope;
* critical-path breakdown.

#### How would you distinguish frontend issues from backend issues?

Useful evidence:

* browser navigation timing;
* real-user monitoring;
* API duration;
* server timing headers;
* client error logs;
* trace span duration;
* rendering profiles;
* network waterfall.

#### How would you trace a failed or slow user action end to end?

The candidate should describe the path from client action to request, service, dependency, async work, and final state.

#### What information would you want from the user report?

Examples:

* approximate time;
* action;
* user or tenant identifier;
* browser and device;
* client version;
* screenshots;
* request ID;
* reproducibility;
* region.

Sensitive information should be collected carefully.

#### What logs or traces would you check first?

A strong answer starts with the critical path and known correlation identifiers rather than searching raw logs blindly.

#### How would you tell whether the issue affected one user, one tenant, one region, or everyone?

The candidate should segment metrics and compare matched cohorts.

#### What made user-facing bugs hard to reproduce?

High-signal examples:

* timing;
* client state;
* permissions;
* feature flags;
* region;
* specific data shape;
* dependency state;
* browser extension or device behavior.

#### What debugging workflow became easier after better instrumentation?

Strong answers provide a concrete before-and-after improvement.

### Follow-up probes for the interviewer

* What exact user information was safe to collect?
* How did the request ID reach support?
* What if the backend was fast but the screen was slow?
* What if only one tenant was affected?
* Could client and server clocks differ?
* How did feature flags affect reproduction?
* What did real-user monitoring reveal?
* How was the fix confirmed?

### Weak-answer signals

Watch for answers that:

* immediately restart services;
* treat “slow” as one metric;
* inspect backend only;
* have no way to correlate a user action;
* cannot scope the issue;
* ask users for sensitive data unnecessarily;
* reproduce only against generic test data;
* stop after a component-level metric improves.

---


## C. Cross-service and distributed debugging

* How did you debug complex cross-service or end-to-end issues?
* Were requests, jobs, or events traceable across system boundaries?
* Did you use correlation IDs, request IDs, event IDs, or structured logs?
* How did you debug async workflows where cause and effect were separated in time?
* What made distributed behavior hard to reason about?
* Were there places where logs existed but did not answer the right questions?
* How did you identify the actual failing component in a chain of dependencies?
* What would have made cross-system debugging easier?

What this reveals:
Whether they understand that observability must follow the shape of the architecture, especially across service, queue, and client boundaries.

### Clarifying questions a strong candidate may ask

* Should I focus on synchronous requests or asynchronous workflows?
* Would you like one cross-service incident in depth?
* Should I discuss correlation identifiers and context propagation?
* Are you interested in logs, traces, or event history?
* Should I explain where observability broke at a boundary?

These questions show that distributed debugging requires context to survive every architectural transition.

### Reasoning expected from the candidate

A strong answer should explain:

1. **Identity of work**
   * Request ID, trace ID, booking ID, job ID, event ID, and causation ID?
2. **Context propagation**
   * HTTP headers, message metadata, and log fields?
3. **Synchronous tracing**
   * Which service or dependency consumed time or failed?
4. **Asynchronous tracing**
   * What caused the job or event, and what happened later?
5. **Domain timeline**
   * Could operators see state transitions in business terms?
6. **Boundary gaps**
   * Where did context disappear?
7. **Fault attribution**
   * Which component originated the failure versus propagated it?
8. **Privacy**
   * Were identifiers useful without leaking sensitive data?

### Example of a strong coherent answer

> Every patient action created or propagated a trace ID and request ID. Booking workflows also had a stable booking ID and each external attempt had its own attempt ID.
>
> HTTP calls propagated trace context in headers. Queue messages carried trace or causation metadata, event ID, aggregate ID, and version. Structured logs included these fields consistently.
>
> For async debugging, traces alone were not sufficient because work could continue hours later. We maintained a domain timeline showing booking creation, external attempts, state transitions, event publication, retries, and reconciliation.
>
> Distributed behavior was difficult when a downstream service logged only its local request ID. We fixed that by standardizing context propagation and adding contract tests around message metadata.
>
> To identify the actual failing component, we looked for the earliest span or domain event where expected behavior diverged. A downstream timeout might be caused by upstream queueing or an overloaded dependency, so we avoided blaming the component that returned the final error without examining the full path.
>
> Cross-system debugging would have been easier with consistent error taxonomy and stronger links between traces, workflow state, and support tools.

### Question-by-question answer expectations

#### How did you debug complex cross-service or end-to-end issues?

The candidate should describe a repeatable workflow, not ad hoc log searching.

#### Were requests, jobs, or events traceable across system boundaries?

A strong answer explains each boundary and propagation mechanism.

#### Did you use correlation IDs, request IDs, event IDs, or structured logs?

The candidate should distinguish:

* trace ID for distributed execution;
* request ID for one request;
* event ID for deduplication and investigation;
* domain ID for long-lived workflow;
* causation ID for why work occurred.

#### How did you debug async workflows where cause and effect were separated in time?

Strong mechanisms:

* workflow timeline;
* event history;
* job-attempt records;
* causation links;
* queue metrics;
* replay tooling;
* state-age dashboards.

#### What made distributed behavior hard to reason about?

Examples:

* partial failure;
* retries;
* duplicate delivery;
* clock differences;
* missing context;
* sampling;
* eventual consistency;
* data ownership.

#### Were there places where logs existed but did not answer the right questions?

High-signal answers identify missing domain context, state transitions, or dependency contribution.

#### How did you identify the actual failing component in a chain of dependencies?

The candidate should trace causality and distinguish origin from propagation.

#### What would have made cross-system debugging easier?

Examples:

* consistent field names;
* domain timeline;
* better trace sampling;
* error taxonomy;
* context propagation;
* replayable events;
* support correlation.

### Follow-up probes for the interviewer

* What identifier survived for the full workflow?
* How was async causation recorded?
* Could trace sampling omit the failing request?
* Were clocks synchronized?
* Did logs include domain state?
* How were retries represented?
* What was the earliest divergence?
* Could operators replay safely?

### Weak-answer signals

Watch for answers that:

* rely on unstructured text logs;
* use one local request ID per service with no propagation;
* assume traces alone cover long-running workflows;
* cannot link events to causes;
* blame the final failing service without path analysis;
* log sensitive payloads for convenience;
* have no domain timeline;
* cannot explain where context was lost.

---


## D. Alerts, incidents, and operational response

* What alerts would you set up for this system?
* What conditions should wake someone up?
* What conditions should create a ticket but not page anyone?
* How did you avoid noisy or low-value alerts?
* If I woke you up at 2 a.m. because this system was broken, where would you look first?
* What runbooks, dashboards, or mitigation tools existed?
* What was the fastest safe mitigation for a serious issue?
* What incident taught you something about how the system actually behaved?

What this reveals:
Whether they can think operationally about urgency, signal quality, mitigation, and production ownership.

### Clarifying questions a strong candidate may ask

* Should I focus on page-worthy alerts or the broader alert strategy?
* Would you like one incident response flow in depth?
* Should I discuss service-level objectives and error budgets?
* Are you interested in mitigation tools and runbooks?
* Should I include an alert we removed because it was noisy?

These questions show that alerts should drive action and reflect urgency, not merely report interesting metrics.

### Reasoning expected from the candidate

A strong operational answer should classify:

1. **Page**
   * Immediate user harm, security risk, data corruption, or rapidly worsening failure?
2. **Ticket**
   * Important but not urgent maintenance or degradation?
3. **Dashboard only**
   * Contextual information with no direct action?
4. **Signal quality**
   * Does the alert identify a symptom, scope, and first action?
5. **Actionability**
   * Can on-call mitigate safely?
6. **Runbook**
   * What decision tree exists?
7. **Escalation**
   * Which team or dependency owner is involved?
8. **Learning**
   * How were alerts improved after incidents?

A mature answer pages on user-impacting symptoms or imminent exhaustion, not every infrastructure anomaly.

### Example of a strong coherent answer

> I would page for sustained booking failure above the service-level threshold, cross-tenant authorization anomalies, data-integrity violations, rapidly growing queue age that threatened booking recovery, or a critical dependency outage with no safe fallback.
>
> I would create tickets for gradual storage growth, low-volume dead-letter messages, non-urgent stale analytics, or a dependency nearing but not yet reaching capacity.
>
> We avoided paging directly on CPU unless it correlated with user impact or imminent saturation. Instead, alerts used multi-window error-budget burn, queue-age thresholds, and per-vendor failure segmentation.
>
> At 2 a.m., I would open the user-journey dashboard first, confirm scope, check recent deployments and configuration changes, inspect dependency and queue health, then open representative traces.
>
> Runbooks included safe feature disablement, vendor circuit isolation, rollback, queue throttling, serving bounded stale search data, and escalation contacts.
>
> The fastest safe mitigation for one serious incident was disabling a failing vendor integration for search while preserving other clinics and booking-status access.
>
> An incident taught us that aggregate booking success hid one vendor’s complete failure. We changed alerts and dashboards to segment by vendor and clinic.

### Question-by-question answer expectations

#### What alerts would you set up for this system?

Strong categories:

* user-journey failure;
* latency;
* saturation;
* queue lag;
* dependency health;
* correctness invariant;
* security anomaly;
* data freshness;
* dead-letter growth.

#### What conditions should wake someone up?

Page-worthy conditions should be:

* urgent;
* actionable;
* user- or data-impacting;
* likely to worsen without intervention.

#### What conditions should create a ticket but not page anyone?

Examples:

* slow capacity trend;
* isolated non-critical job;
* minor data lag;
* low-volume deprecation usage;
* non-urgent cleanup.

#### How did you avoid noisy or low-value alerts?

Mechanisms:

* alert on symptoms;
* use sustained windows;
* group related alerts;
* segment intelligently;
* remove non-actionable pages;
* route by ownership;
* include context.

#### If I woke you up at 2 a.m. because this system was broken, where would you look first?

A strong answer begins with user impact and scope, then recent changes and likely dependencies.

#### What runbooks, dashboards, or mitigation tools existed?

The candidate should name concrete controls and safe actions.

#### What was the fastest safe mitigation for a serious issue?

Examples:

* rollback;
* disable feature;
* isolate vendor;
* rate limit;
* serve stale;
* pause worker;
* switch traffic;
* block destructive writes.

#### What incident taught you something about how the system actually behaved?

Strong answers include expectation, reality, response, and change.

### Follow-up probes for the interviewer

* What exact symptom caused the page?
* Was the page actionable?
* What was the first safe mitigation?
* Could the mitigation create data loss?
* Which alert was removed?
* How were dependency owners contacted?
* What did the runbook fail to cover?
* How did the incident change monitoring?

### Weak-answer signals

Watch for answers that:

* page on every infrastructure threshold;
* cannot distinguish page from ticket;
* have no safe mitigation;
* start with host metrics rather than user impact;
* lack runbooks or ownership;
* accept persistent alert noise;
* cannot name an incident lesson;
* use aggregate alerts that hide isolated failures.

---


## E. Feedback from production into design

* What signals told you the design was or was not working in production?
* Did production behavior ever invalidate an assumption from the design phase?
* What recurring operational issue led to a code, architecture, or process change?
* How did observability influence future design decisions?
* What metric or production signal changed how you prioritized work?
* What operational burden did the system create for the team?
* What would you redesign to make the system easier to operate?
* What did operating the system teach you that design review did not?

What this reveals:
Whether they understand that operating a system is part of designing it, and that production feedback should shape future engineering choices.

### Clarifying questions a strong candidate may ask

* Should I focus on one production signal that changed the design?
* Would you like an invalidated design assumption?
* Should I discuss code, architecture, and process changes?
* Are you interested in operational burden on the team?
* Should I explain what I would redesign for operability?

These questions show that observability is valuable only when it changes decisions.

### Reasoning expected from the candidate

A strong answer should explain a feedback loop:

1. **Original assumption**
   * What did design expect?
2. **Production signal**
   * Metric, trace, incident, support pattern, or operational cost?
3. **Interpretation**
   * What did the signal reveal?
4. **Change**
   * Code, architecture, tooling, ownership, or process?
5. **Outcome**
   * Did the burden or user impact improve?
6. **New design principle**
   * What did the team carry forward?
7. **Remaining burden**
   * What is still hard to operate?

### Example of a strong coherent answer

> We originally assumed infrastructure capacity would be the main scaling concern. Production showed that vendor inconsistency and reconciliation workload created more operational burden than CPU or database load.
>
> The signal was a growing number of bookings spending too long in uncertain states, combined with support tickets that were difficult to investigate. That led us to add workflow-age metrics, richer attempt history, per-vendor dashboards, and automated reconciliation prioritization.
>
> Another recurring issue was one clinic’s bad configuration affecting all its search results. We introduced staged configuration rollout, validation, versioning, and per-clinic health checks.
>
> Observability also changed API design. We began requiring correlation IDs and exposing stable operation status because long-running workflows needed to be traceable across user sessions.
>
> A production metric that changed prioritization was the rate of manual support interventions per thousand bookings. Improving that reduced operational cost more than another small latency optimization.
>
> The system burdened the team through noisy vendor-specific alerts and manual replay. I would redesign the operational model so every async workflow had explicit ownership, age-based alerts, safe replay, and a standard timeline from the beginning.
>
> Operating the system taught us that diagnosability and recovery paths are first-class architecture requirements, not post-launch additions.

### Question-by-question answer expectations

#### What signals told you the design was or was not working in production?

Strong answers include user, system, and operational signals.

#### Did production behavior ever invalidate an assumption from the design phase?

The candidate should state the original assumption and evidence against it.

#### What recurring operational issue led to a code, architecture, or process change?

High-signal examples:

* manual reconciliation;
* noisy alerts;
* slow deploy recovery;
* hard-to-debug async work;
* data skew;
* dependency instability;
* configuration errors.

#### How did observability influence future design decisions?

Examples:

* required correlation IDs;
* explicit state model;
* smaller failure domains;
* richer audit history;
* better ownership;
* domain metrics;
* replayable workflows.

#### What metric or production signal changed how you prioritized work?

Strong answers tie the metric to user impact or operational burden.

#### What operational burden did the system create for the team?

Examples:

* on-call pages;
* manual data repair;
* alert triage;
* vendor escalation;
* replay;
* difficult local reproduction;
* deployment coordination.

#### What would you redesign to make the system easier to operate?

A mature answer includes architecture, tooling, and ownership.

#### What did operating the system teach you that design review did not?

Strong answers name emergent behavior, real data shape, human workflows, or failure interactions.

### Follow-up probes for the interviewer

* What was the original assumption?
* Which metric disproved it?
* What operational work was manual?
* Did the change reduce pages or support volume?
* What signal became a design requirement?
* What remains hard?
* Which dashboard changed prioritization?
* What would be instrumented before launch now?

### Weak-answer signals

Watch for answers that:

* collect telemetry without changing design;
* cannot name an invalidated assumption;
* treat operations as another team’s problem;
* optimize infrastructure while ignoring manual burden;
* have no domain-level metrics;
* cannot link incidents to architectural changes;
* redesign only dashboards rather than failure behavior;
* claim design review predicted production accurately.

---

# Cross-section answer framework

Candidates can use this structure to answer most observability and operations questions:

1. **Define the user journey**
   * What must users be able to complete?
2. **Define health**
   * Success, latency, freshness, correctness, and completion.
3. **Map internal signals**
   * Saturation, queues, dependencies, caches, and retries.
4. **Preserve work identity**
   * Request, trace, event, job, and domain identifiers.
5. **Diagnose by scope**
   * One user, tenant, region, dependency, or global?
6. **Trace the critical path**
   * Client, network, API, database, queue, and external services.
7. **Alert on action**
   * Page only when urgent intervention is needed.
8. **Mitigate safely**
   * Rollback, isolate, degrade, pause, or rate limit.
9. **Learn from production**
   * Which assumption changed, and what design followed?
10. **Reflect**
   * What would make the system easier to understand and operate?

A strong answer demonstrates that observability is designed around the architecture and user workflows, not added as generic logging after implementation.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* defines health through user outcomes and internal conditions;
* distinguishes availability, correctness, freshness, and completion;
* identifies leading indicators and silent failures;
* segments health by tenant, region, vendor, or workflow;
* uses metrics, logs, traces, and domain events for different purposes;
* follows a structured full-stack debugging workflow;
* preserves correlation across synchronous and asynchronous boundaries;
* distinguishes failure origin from error propagation;
* pages on urgent actionable conditions;
* has safe mitigation and runbook thinking;
* uses production signals to change architecture and priorities;
* recognizes operational burden as a design concern.

## Mixed signal

The candidate:

* has good infrastructure visibility but limited user-journey metrics;
* can debug synchronous paths but weakly handles async workflows;
* uses correlation IDs but lacks a durable domain timeline;
* has alerts but some are noisy or weakly actionable;
* learns from incidents but does not consistently feed lessons into design.

## Weak signal

The candidate:

* defines health as uptime;
* relies on aggregate dashboards;
* cannot trace a user action end to end;
* searches unstructured logs manually;
* loses context at queues or service boundaries;
* pages on every resource threshold;
* has no safe mitigation or runbook;
* treats operations as separate from design;
* cannot name a production signal that changed an assumption.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What user journey defined system health?
2. What were the three most important user-facing signals?
3. What internal signal gave the earliest warning?
4. What failure could remain silent?
5. How would you diagnose a vague “slow” report?
6. How did request or workflow identity cross system boundaries?
7. How were async jobs and events traced to their cause?
8. What condition should page someone?
9. What issue should create only a ticket?
10. What was the fastest safe mitigation?
11. Which production signal invalidated a design assumption?
12. What would you redesign for operability?

A strong response should demonstrate user-centered health definitions, evidence-based diagnosis, distributed context propagation, actionable incident response, and a clear operational feedback loop into design.
