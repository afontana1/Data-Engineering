# 8. Performance and complexity

These questions surface whether the candidate can connect computer science fundamentals to practical system behavior. The goal is not to ask abstract algorithm trivia, but to understand whether they can identify expensive operations, reason about complexity, measure bottlenecks, and choose appropriate optimizations.

## Table of contents

- [A. Performance-sensitive paths](#a-performance-sensitive-paths)
- [B. Complexity and data structure choices](#b-complexity-and-data-structure-choices)
- [C. Measurement, diagnosis, and bottlenecks](#c-measurement-diagnosis-and-bottlenecks)
- [D. Optimization techniques and tradeoffs](#d-optimization-techniques-and-tradeoffs)
- [E. Caching, freshness, and invalidation](#e-caching-freshness-and-invalidation)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched across clinics, booked appointments, and received reminders. Search was high-volume and latency-sensitive, booking was lower-volume but correctness-sensitive, and several clinic scheduling systems imposed variable latency and rate limits.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can identify which paths actually matter, reason about algorithmic and data-structure costs, measure bottlenecks, choose optimizations based on evidence, and explain the freshness and correctness tradeoffs introduced by caching.



## A. Performance-sensitive paths

* What operations in the system were performance-sensitive?
* What were the main hot paths?
* Which user flows or backend jobs had the strictest latency expectations?
* Which operations affected throughput, cost, or user experience the most?
* What part of the system was slowest under normal conditions?
* What part became slow only under load?
* How did you know which operations mattered most?
* What performance issue would users notice first?

What this reveals:
Whether they can identify where performance actually matters instead of optimizing randomly or prematurely.

### Clarifying questions a strong candidate may ask

* Should I focus on user-facing latency, backend throughput, cost, or all three?
* Would you like normal behavior or performance under peak load?
* Should I describe one hot path in depth?
* Are you interested in measured service-level targets?
* Should I separate synchronous request paths from background jobs?

These questions show that performance has several dimensions and that not every slow operation deserves equal attention.

### Reasoning expected from the candidate

A strong answer should establish:

1. **Critical operation**
   * Which user action or backend job mattered most?
2. **Performance objective**
   * Latency, throughput, cost, resource use, or deadline?
3. **Workload shape**
   * Average, peak, burst, and tail behavior?
4. **Critical path**
   * Which steps blocked completion?
5. **User or business consequence**
   * What happened if the path was slow?
6. **Evidence**
   * Which metrics or observations proved importance?
7. **Prioritization**
   * Why was this path optimized before others?

A mature candidate distinguishes average latency from tail latency and recognizes that a low-volume workflow may still be the most critical if it blocks a high-value action.

### Example of a strong coherent answer

> The most performance-sensitive path was appointment search. Users compared several result pages, so even modest delays compounded and increased abandonment. We targeted a fast first page and monitored p50, p95, and p99 latency rather than only averages.
>
> Booking confirmation had a looser latency target but a higher correctness requirement. Users would tolerate a few seconds if the UI showed clear progress, but they would not tolerate duplicate bookings or an ambiguous final state.
>
> The main search hot path was request validation, filtering the normalized availability read model, joining clinic display metadata, ranking results, serializing the response, and returning the first page.
>
> Under normal conditions, vendor refresh jobs were the slowest operations, but they were asynchronous and did not directly block users. Under load, search became slow when hot clinic partitions caused database contention and response serialization grew with large result sets.
>
> We knew search mattered most from conversion funnels, real-user monitoring, trace data, and support complaints. The first issue users noticed was delayed result updates after changing filters, not background processing lag.

### Question-by-question answer expectations

#### What operations in the system were performance-sensitive?

Strong answers name operations and the relevant dimension.

Examples:

* interactive search latency;
* checkout completion;
* batch deadline;
* stream-processing lag;
* cost per inference;
* queue drain rate;
* page render time.

#### What were the main hot paths?

The candidate should describe the sequence of expensive steps rather than saying “the API.”

Useful pattern:

> request parsing → authorization → data lookup → computation → dependency call → serialization → response

#### Which user flows or backend jobs had the strictest latency expectations?

A strong answer differentiates:

* interactive versus asynchronous;
* human patience versus machine deadline;
* end-to-end versus component latency;
* hard deadline versus soft target.

#### Which operations affected throughput, cost, or user experience the most?

The candidate should explain whether frequency, expense per operation, or criticality drove impact.

#### What part of the system was slowest under normal conditions?

A strong answer explains whether the slowest operation was actually important.

Some slow work is acceptable if asynchronous, infrequent, or outside the user’s critical path.

#### What part became slow only under load?

Examples:

* lock contention;
* connection pools;
* garbage collection;
* queueing;
* hot partitions;
* rate limiting;
* cache stampede;
* rendering large lists.

#### How did you know which operations mattered most?

Good evidence includes:

* real-user monitoring;
* tracing;
* conversion data;
* service-level objectives;
* CPU profiles;
* cost reports;
* queue lag;
* incident history.

#### What performance issue would users notice first?

The candidate should connect technical behavior to visible symptoms.

### Follow-up probes for the interviewer

* What was the p95 or p99 target?
* What percentage of total time came from each step?
* Did the slowest component dominate end-to-end latency?
* What happened to error rate under load?
* Was the issue server-side, network-side, or rendering-side?
* Which operation was expensive but low priority?
* How was user impact measured?
* What changed after optimization?

### Weak-answer signals

Watch for answers that:

* optimize everything equally;
* discuss only average latency;
* cannot identify a critical path;
* name a slow component with no user impact;
* use infrastructure metrics without product context;
* confuse throughput and latency;
* cannot explain performance under load;
* optimize based on intuition alone.

---


## B. Complexity and data structure choices

* Where did time complexity or space complexity meaningfully affect the design?
* Did any hot path require attention to asymptotic complexity?
* What data structures were important to the system’s behavior?
* Can you describe one place where a data structure choice materially changed performance or correctness?
* Were there places where a simple linear approach was good enough?
* Were there places where an initially simple approach stopped working?
* Did you ever redesign an algorithm or access pattern after observing real usage?
* What complexity tradeoff was worth making, and what was not?

What this reveals:
Whether they can apply algorithmic thinking pragmatically, with judgment about when complexity matters and when it does not.

### Clarifying questions a strong candidate may ask

* Should I focus on asymptotic complexity or practical constant factors?
* Would you like one algorithm or data structure in depth?
* Should I discuss memory tradeoffs as well as time?
* Are you interested in a case where the simple approach was sufficient?
* Should I include a design that changed after scale increased?

These questions show that algorithmic reasoning should be applied pragmatically rather than performatively.

### Reasoning expected from the candidate

A strong candidate should explain:

1. **Operation**
   * What computation or lookup occurred?
2. **Input size**
   * What did `n` represent?
3. **Original complexity**
   * Time and space behavior?
4. **Observed threshold**
   * When did the approach become costly?
5. **Alternative**
   * Different algorithm, data structure, precomputation, or index?
6. **Tradeoff**
   * Memory, update cost, complexity, or freshness?
7. **Validation**
   * What evidence showed improvement?

A mature answer recognizes that `O(n)` may be entirely appropriate when `n` is small and bounded, while a theoretically better structure may be worse due to complexity or constants.

### Example of a strong coherent answer

> One important hot path ranked availability results. The initial implementation filtered and sorted all matching slots in memory. That was roughly `O(n log n)` after retrieval and worked well when each clinic returned a few hundred slots.
>
> As onboarding expanded, some searches returned tens of thousands of candidates. Sorting everything before pagination increased latency and memory use. We moved more filtering and ordering into the indexed read store and used a bounded top-k approach for relevance ranking.
>
> We also replaced repeated membership checks against a list of eligible clinic IDs with a hash set. That changed a nested `O(n × m)` pattern into roughly `O(n + m)` and simplified the code.
>
> Not every linear scan was worth removing. Validation over a maximum of ten requested appointment types remained a simple loop because the bound was small and clearer than maintaining another index.
>
> The data-structure tradeoff was memory versus speed. Precomputed maps and indexes increased storage and write cost, but they reduced repeated work on a heavily read path.

### Question-by-question answer expectations

#### Where did time complexity or space complexity meaningfully affect the design?

The candidate should identify a real operation and define the input size.

Examples:

* sorting result sets;
* graph traversal;
* duplicate detection;
* aggregation;
* matching;
* cache size;
* in-memory buffering.

#### Did any hot path require attention to asymptotic complexity?

A strong answer explains both asymptotic behavior and practical scale.

#### What data structures were important to the system’s behavior?

Examples:

* hash map;
* set;
* priority queue;
* ring buffer;
* tree;
* trie;
* bitmap;
* graph;
* bloom filter;
* append-only log.

The candidate should explain why the structure fit the access pattern.

#### Can you describe one place where a data structure choice materially changed performance or correctness?

A strong answer includes before, after, and measurable consequence.

#### Were there places where a simple linear approach was good enough?

High-signal answers show judgment.

Good reasons:

* bounded input;
* infrequent path;
* clearer code;
* low memory;
* no measured bottleneck.

#### Were there places where an initially simple approach stopped working?

The candidate should identify the scale or access-pattern change that crossed the threshold.

#### Did you ever redesign an algorithm or access pattern after observing real usage?

Strong answers use production evidence rather than hypothetical optimization.

#### What complexity tradeoff was worth making, and what was not?

Examples:

* more memory for lower latency;
* precomputation for repeated reads;
* index maintenance for faster lookup;
* avoiding a complex distributed algorithm for small data.

### Follow-up probes for the interviewer

* What did `n` represent?
* What was the input bound?
* What was the memory overhead?
* Did the better asymptotic approach improve real latency?
* Was the bottleneck CPU or I/O?
* Could the database perform the operation more efficiently?
* What did the simpler code buy?
* Where did constant factors dominate?

### Weak-answer signals

Watch for answers that:

* recite Big O without a real workload;
* cannot define input size;
* optimize bounded small collections unnecessarily;
* ignore memory and update costs;
* claim a data structure was faster without measurement;
* use theoretically superior algorithms with worse practical behavior;
* cannot identify when the simple approach stopped scaling;
* treat algorithmic complexity as separate from system design.

---


## C. Measurement, diagnosis, and bottlenecks

* What was the most expensive operation in the system, and how did you know?
* What metrics, profiling, tracing, logs, or benchmarks helped you diagnose performance?
* Did the bottleneck come from computation, database access, network calls, serialization, rendering, locking, or external dependencies?
* Was the bottleneck where you expected it to be?
* How did you distinguish actual bottlenecks from suspected ones?
* What performance issue was hardest to reproduce?
* Were there misleading signals that initially pointed you in the wrong direction?
* What would you measure first if the system suddenly became slow?

What this reveals:
Whether they can diagnose performance based on evidence rather than guesses.

### Clarifying questions a strong candidate may ask

* Should I describe a production incident or a planned performance investigation?
* Would you like the diagnostic sequence in detail?
* Should I include frontend, backend, database, and dependency signals?
* Are you interested in the suspected bottleneck or the measured one?
* Should I explain how we reproduced the issue?

These questions show that performance diagnosis is an evidence-gathering process.

### Reasoning expected from the candidate

A strong diagnostic approach should:

1. **Define the symptom**
   * Which user flow, endpoint, job, or percentile degraded?
2. **Establish scope**
   * One user, tenant, region, release, or everyone?
3. **Check saturation**
   * CPU, memory, I/O, connections, queues, locks, or quotas?
4. **Trace the path**
   * Where was time spent?
5. **Compare baseline**
   * What changed from normal?
6. **Form and test hypotheses**
   * Use profiling or controlled experiments.
7. **Find the causal bottleneck**
   * Avoid optimizing correlated symptoms.
8. **Validate the fix**
   * Re-measure end-to-end behavior and regression risk.

### Example of a strong coherent answer

> The most expensive operation was refreshing availability from one clinic vendor. We knew because distributed traces showed that vendor calls dominated wall-clock time and queue workers spent most of their time waiting on network responses.
>
> For user-facing search, we used real-user monitoring, service latency histograms, database query timing, request traces, and response-size metrics. Profiling showed that large-response serialization consumed more CPU than expected.
>
> The bottleneck we initially suspected was the database because CPU on the database host was high. Query analysis showed the main queries were still fast. The actual issue was a cache miss storm that increased result size and caused application-side sorting and serialization. Database CPU was a downstream symptom.
>
> The hardest issue to reproduce occurred only for a few large clinics during weekday peaks. We replayed anonymized request shapes against production-like data and added per-clinic tracing tags to reveal skew.
>
> If the system suddenly became slow, I would first identify which endpoint and percentile changed, compare error rate and traffic, inspect queueing and dependency latency, then use traces to locate where end-to-end time accumulated.

### Question-by-question answer expectations

#### What was the most expensive operation in the system, and how did you know?

Strong answers provide:

* cost dimension;
* measurement source;
* relative contribution;
* context.

#### What metrics, profiling, tracing, logs, or benchmarks helped you diagnose performance?

The candidate should explain the role of each:

* metrics reveal trends;
* traces reveal path timing;
* profiles reveal CPU or memory use;
* logs explain specific events;
* benchmarks compare controlled implementations.

#### Did the bottleneck come from computation, database access, network calls, serialization, rendering, locking, or external dependencies?

A mature answer distinguishes wait time from compute time and local work from remote work.

#### Was the bottleneck where you expected it to be?

Strong candidates are willing to say no and explain what evidence changed their view.

#### How did you distinguish actual bottlenecks from suspected ones?

Good methods:

* contribution analysis;
* controlled removal;
* profiling;
* load tests;
* before/after comparison;
* dependency isolation;
* queueing metrics.

#### What performance issue was hardest to reproduce?

High-signal examples involve:

* data skew;
* race conditions;
* cache state;
* warm-up;
* production traffic mix;
* regional dependency behavior;
* browser/device differences.

#### Were there misleading signals that initially pointed you in the wrong direction?

The candidate should explain correlation versus causation.

#### What would you measure first if the system suddenly became slow?

Strong sequence:

1. affected path and percentile;
2. traffic and errors;
3. saturation;
4. dependency latency;
5. queueing and contention;
6. traces;
7. recent changes.

### Follow-up probes for the interviewer

* What was the baseline?
* Which metric was a symptom, not a cause?
* Did the issue reproduce with production-like data?
* How did skew appear?
* Was tracing sampled?
* What did profiling change?
* Did the fix move the bottleneck?
* How was regression prevented?

### Weak-answer signals

Watch for answers that:

* guess without measurement;
* look only at CPU;
* treat high utilization as proof of causality;
* cannot distinguish end-to-end from component latency;
* benchmark unrealistic data;
* change several variables at once;
* cannot describe a diagnostic sequence;
* validate fixes only by subjective impression.

---


## D. Optimization techniques and tradeoffs

* Where did caching, batching, indexing, precomputation, memoization, pagination, streaming, or async processing help?
* What optimization had the biggest impact?
* What optimization added the most complexity?
* Did any optimization make the system harder to reason about or operate?
* How did you think about latency versus throughput?
* How did you decide between optimizing code, changing data access patterns, or scaling infrastructure?
* What did you deliberately choose not to optimize?
* What was the simplest improvement that delivered meaningful performance gains?

What this reveals:
Whether they understand optimization as a tradeoff between speed, complexity, correctness, cost, and maintainability.

### Clarifying questions a strong candidate may ask

* Should I focus on one optimization with measurable impact?
* Would you like code-level, database-level, or architectural optimizations?
* Should I discuss the operational cost introduced?
* Are you interested in latency, throughput, or infrastructure cost?
* Should I include an optimization we deliberately rejected?

These questions show that optimization should be evaluated as a system tradeoff.

### Reasoning expected from the candidate

A strong optimization explanation should follow:

> Measured bottleneck → candidate changes → expected effect → implementation cost → measured outcome → new tradeoff

Possible optimization categories:

* reduce work;
* avoid repeated work;
* move work earlier;
* batch work;
* parallelize safely;
* defer work;
* improve locality;
* use a better index;
* change data shape;
* add capacity.

A mature candidate considers whether adding infrastructure is cheaper and safer than adding code complexity.

### Example of a strong coherent answer

> The highest-impact optimization was replacing synchronous vendor fan-out during search with an asynchronously refreshed read model. It reduced p95 search latency from several seconds to under one second and reduced vendor quota pressure.
>
> The most complex optimization was cache invalidation and refresh prioritization. It introduced freshness monitoring, deduplication, and fallback behavior.
>
> A simpler but valuable improvement was adding a composite index on clinic, appointment type, and time range. That reduced query latency without changing application architecture.
>
> We considered parallelizing every vendor call during refresh, but rejected unbounded concurrency because it would increase rate limiting and failure amplification. We used per-vendor concurrency controls instead.
>
> We chose code optimization only after traces showed CPU-heavy sorting and serialization. For database-bound paths, changing queries and indexes delivered more value. For predictable peak events, temporary capacity increases were cheaper than redesign.
>
> We deliberately did not optimize a nightly reporting job that completed in twenty minutes against a two-hour deadline. Improving it would have added complexity with no user or cost benefit.

### Question-by-question answer expectations

#### Where did caching, batching, indexing, precomputation, memoization, pagination, streaming, or async processing help?

The candidate should connect each technique to a measured pressure.

#### What optimization had the biggest impact?

A strong answer includes before-and-after evidence.

#### What optimization added the most complexity?

The candidate should name operational and correctness costs, not only code volume.

#### Did any optimization make the system harder to reason about or operate?

Examples:

* stale caches;
* asynchronous completion;
* duplicated state;
* retries;
* partitioning;
* background refresh;
* distributed coordination.

#### How did you think about latency versus throughput?

A mature answer recognizes:

* batching improves throughput but may increase latency;
* concurrency reduces latency until saturation;
* queueing smooths bursts but delays completion;
* larger pages reduce round trips but increase response time.

#### How did you decide between optimizing code, changing data access patterns, or scaling infrastructure?

Strong decision factors:

* bottleneck type;
* cost;
* risk;
* reversibility;
* expected lifetime;
* operational burden;
* measured headroom.

#### What did you deliberately choose not to optimize?

This is a high-signal judgment question.

#### What was the simplest improvement that delivered meaningful performance gains?

Examples:

* index;
* remove N+1 calls;
* compress payload;
* cap result size;
* reuse connection;
* avoid redundant serialization;
* fix cache key.

### Follow-up probes for the interviewer

* What was the measured improvement?
* What new failure mode appeared?
* Was the optimization reversible?
* What did it cost to operate?
* Did throughput improve at the expense of tail latency?
* Could capacity have solved it more cheaply?
* Which optimization created technical debt?
* What would you remove if load decreased?

### Weak-answer signals

Watch for answers that:

* optimize before measuring;
* discuss techniques without a bottleneck;
* provide no before-and-after evidence;
* ignore operational cost;
* parallelize without bounded concurrency;
* cache without freshness requirements;
* cannot name anything intentionally left unoptimized;
* assume code optimization is always better than infrastructure.

---


## E. Caching, freshness, and invalidation

* Did you have a caching strategy?
* What data was safe to cache, and what was not?
* How fresh did the cached data need to be?
* What invalidation challenges came with caching?
* Were there cases where stale data was acceptable?
* Were there cases where stale data would be dangerous?
* How did caching affect correctness, debugging, or user trust?
* If the cache failed or was empty, how did the system behave?

What this reveals:
Whether they understand that caching is not just a performance technique; it creates consistency, freshness, and operational tradeoffs.

### Clarifying questions a strong candidate may ask

* Should I discuss application caches, CDN caches, database caches, or all layers?
* Would you like one cache in depth?
* Are you interested in freshness guarantees or invalidation mechanics?
* Should I include failure and cold-start behavior?
* Should I explain how users were protected from stale data?

These questions show that caching is a consistency and operations decision, not merely a speed technique.

### Reasoning expected from the candidate

A strong caching explanation should cover:

1. **Cached object**
   * What data or computation was cached?
2. **Reason**
   * Latency, load, quota, or cost?
3. **Authority**
   * Where was the source of truth?
4. **Freshness requirement**
   * Time-to-live, event-driven invalidation, or version check?
5. **Key design**
   * Scope, tenant, permissions, and query parameters?
6. **Invalidation**
   * How did updates propagate?
7. **Failure behavior**
   * Cold cache, unavailable cache, stale cache, or stampede?
8. **Correctness**
   * Could stale data cause harmful decisions?

### Example of a strong coherent answer

> We cached normalized appointment availability and clinic display metadata. The clinic systems remained authoritative.
>
> Availability could be several minutes stale during search because final booking revalidated the slot. Authorization, patient identity, and confirmed booking state were not trusted from a long-lived cache.
>
> Cache keys included clinic, appointment type, time range, locale, and relevant eligibility scope. Tenant and permission-sensitive data used separate keys to avoid leakage.
>
> Availability was refreshed asynchronously and expired with a bounded TTL. Configuration changes triggered targeted invalidation. We also tracked source version and cache age so the API could avoid serving data beyond the agreed freshness window.
>
> The hardest problem was stampede behavior after large invalidations. We used request coalescing, jittered expiration, background refresh, and stale-while-revalidate for safe search data.
>
> If the cache was empty, the system could rebuild from the read store or degrade to a narrower direct query. If the cache service failed, search became slower but booking correctness remained unaffected.
>
> Caching made debugging harder because users and operators could observe different versions. We added cache-age metadata to traces and support tooling.

### Question-by-question answer expectations

#### Did you have a caching strategy?

A strong answer identifies layers and purpose.

Possible layers:

* browser;
* CDN;
* application;
* distributed cache;
* database buffer;
* computed read model.

#### What data was safe to cache, and what was not?

The candidate should classify by:

* sensitivity;
* authority;
* freshness;
* user scope;
* cost of staleness;
* mutation frequency.

#### How fresh did the cached data need to be?

Strong answers specify a bound or policy.

Examples:

* seconds;
* minutes;
* until event invalidation;
* stale while revalidating;
* version-checked before action.

#### What invalidation challenges came with caching?

Examples:

* multiple writers;
* fan-out;
* missed events;
* key explosion;
* dependency versioning;
* tenant boundaries;
* cascading invalidation.

#### Were there cases where stale data was acceptable?

The candidate should explain why and for how long.

#### Were there cases where stale data would be dangerous?

Examples:

* authorization;
* price charged;
* account balance;
* inventory reservation;
* medical eligibility;
* destructive action state.

#### How did caching affect correctness, debugging, or user trust?

High-signal answers discuss:

* inconsistent views;
* stale decisions;
* support confusion;
* hidden cache keys;
* race conditions;
* observability.

#### If the cache failed or was empty, how did the system behave?

Strong answers describe:

* fall back;
* rebuild;
* degrade;
* rate limit;
* serve stale safely;
* fail closed where necessary.

### Follow-up probes for the interviewer

* What was the TTL?
* How was jitter used?
* Could one tenant read another’s cached data?
* What happened after missed invalidation?
* How was cache age observed?
* Did stale-while-revalidate apply?
* Was there a stampede?
* Could the source handle a cold cache?

### Weak-answer signals

Watch for answers that:

* cache everything;
* cannot name the source of truth;
* have no freshness requirement;
* use only TTL without considering correctness;
* ignore tenant and permission scope;
* have no cold-cache plan;
* cannot detect stale data;
* treat cache failure as impossible.

---

# Cross-section answer framework

Candidates can use this structure to answer most performance questions:

1. **Identify the important path**
   * Which operation mattered to users, throughput, cost, or deadlines?
2. **Define the objective**
   * Latency percentile, throughput, resource use, or completion deadline.
3. **Describe the workload**
   * Input size, request mix, peak pattern, and data skew.
4. **Locate the bottleneck**
   * Use metrics, traces, profiles, and realistic tests.
5. **Explain complexity**
   * Which algorithm or data structure influenced cost?
6. **Choose the optimization**
   * Reduce work, cache, batch, index, precompute, defer, or add capacity.
7. **State the tradeoff**
   * Freshness, memory, write amplification, operations, or code complexity.
8. **Validate**
   * Compare before and after, including tail latency and error rate.
9. **Cover failure behavior**
   * Cold cache, dependency slowdown, saturation, or fallback.
10. **Reflect**
   * What was deliberately not optimized?

A strong answer combines computer science fundamentals with production measurement and practical judgment.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* identifies specific performance-sensitive paths;
* distinguishes latency, throughput, cost, and deadlines;
* discusses average and tail behavior;
* explains one real algorithm or data-structure tradeoff;
* recognizes when a simple linear approach is sufficient;
* diagnoses using evidence rather than intuition;
* distinguishes symptoms from causes;
* provides measurable before-and-after results;
* explains operational costs of optimization;
* knows when scaling infrastructure is appropriate;
* defines cache authority, freshness, invalidation, and fallback;
* identifies what was intentionally left unoptimized.

## Mixed signal

The candidate:

* identifies hot paths but weakly quantifies them;
* knows complexity concepts but not practical thresholds;
* uses metrics but lacks a clear diagnostic sequence;
* explains optimization benefits but not operational cost;
* has a cache strategy but weak freshness or failure reasoning.

## Weak signal

The candidate:

* optimizes randomly or prematurely;
* discusses only average latency;
* recites Big O without workload context;
* cannot distinguish actual from suspected bottlenecks;
* has no before-and-after measurement;
* uses unbounded parallelism;
* caches data without authority or freshness rules;
* has no cold-cache or invalidation strategy;
* cannot name anything deliberately left unoptimized.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What was the most performance-sensitive path?
2. What objective mattered: latency, throughput, cost, or deadline?
3. What did normal and peak workload look like?
4. Which operation dominated the critical path?
5. What algorithm or data structure mattered?
6. Where was a simple approach good enough?
7. What evidence identified the bottleneck?
8. What signal initially misled the team?
9. Which optimization had the largest measured impact?
10. What complexity did that optimization introduce?
11. What data was cached, and how fresh could it be?
12. What happened on cache failure or cold start?

A strong response should demonstrate prioritization, algorithmic reasoning, evidence-based diagnosis, measured optimization, and clear freshness and failure semantics.
