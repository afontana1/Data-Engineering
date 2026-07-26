# 4. High-level architecture and major tradeoffs

These questions probe whether the candidate can reason about the system at an architectural level. The goal is to see whether they can explain the major components, why the design took its shape, what alternatives were considered, and what tradeoffs the team knowingly accepted.

## Table of contents

- [A. Architectural overview and system shape](#a-architectural-overview-and-system-shape)
- [B. Architectural alternatives and decision rationale](#b-architectural-alternatives-and-decision-rationale)
- [C. Major tradeoffs and design priorities](#c-major-tradeoffs-and-design-priorities)
- [D. Placement of complexity and responsibility](#d-placement-of-complexity-and-responsibility)
- [E. Coupling, cohesion, and architectural seams](#e-coupling-cohesion-and-architectural-seams)
- [F. Design risks and lessons learned](#f-design-risks-and-lessons-learned)

## How to use this section

This chapter is intended to function as both an interviewer guide and a candidate preparation resource.

The examples below use a consistent hypothetical project so the answers remain coherent across the section:

> **Running example:** A healthcare organization built a self-service appointment scheduling platform. Patients searched for appointments, booked or cancelled visits, and received reminders. Existing clinic scheduling systems remained authoritative. The platform used a patient-facing web application, an API layer, a normalized availability read model, booking workflow orchestration, vendor-specific integration adapters, asynchronous refresh workers, an event bus, and operational tooling.

A strong candidate does not need to have worked on an identical system. The important signal is whether they can describe architecture at the right level, explain why it took that shape, compare alternatives, identify where complexity lives, and discuss the consequences honestly.



## A. Architectural overview and system shape

* Can you walk me through the architecture at a high level?
* What were the major components or layers in the system?
* What role did each major component play?
* How did data, requests, or events flow through the architecture?
* Which part of the architecture was most central to the system’s behavior?
* What part would a new engineer need to understand first?
* What was intentionally simple in the architecture?
* What was inherently complex because of the problem itself?

What this reveals:
Whether they can describe the system clearly at the right level of abstraction, without getting lost in implementation details too early.

### Clarifying questions a strong candidate may ask

* Would you like the logical architecture, deployment architecture, or both?
* Should I begin with the main user flow and then explain the components?
* Do you want the current architecture or the original version?
* Should I focus on the whole system or the part I personally owned?
* Would a verbal context diagram be useful before I go deeper?

These questions show that “architecture” can refer to several views. A strong candidate chooses the level that best explains responsibilities and flow.

### Reasoning expected from the candidate

A strong architectural overview should:

1. **Start with the system’s purpose**
   * What user or business capability did it provide?
2. **Name the major components**
   * Only the components necessary to understand the main flow.
3. **Explain responsibilities**
   * What role did each component play?
4. **Describe the main path**
   * How did requests, data, or events move?
5. **Identify state and authority**
   * Where was durable state, and what was authoritative?
6. **Call out asynchronous boundaries**
   * What happened later, through queues, jobs, or events?
7. **Identify the conceptual center**
   * Which component or invariant made the architecture understandable?
8. **Separate essential complexity from accidental complexity**
   * What was complicated because the domain was complicated?

The candidate should avoid narrating every library, deployment unit, or table. The goal is to build a mental model.

### Example of a strong coherent answer

> At a high level, the platform had six main parts.
>
> First, the patient web application handled search, booking, cancellation, and status display. It called a backend API that authenticated requests, validated input, and exposed stable product-level contracts.
>
> Second, the search path used a normalized availability read model. Background workers refreshed that model from multiple clinic scheduling vendors through vendor-specific adapters. That let search remain fast and consistent even though the source systems differed in latency and data shape.
>
> Third, booking used a separate workflow orchestrator. It created a durable pending record, called the authoritative clinic system, handled definitive success or rejection, and moved uncertain outcomes into reconciliation.
>
> Fourth, confirmed booking events were published to an event bus. Notification, analytics, and operational consumers processed those events independently.
>
> Fifth, the platform stored workflow state and normalized configuration in a relational database. The clinic scheduling systems still owned provider schedules and final appointment inventory.
>
> Finally, support tooling exposed workflow history, dependency responses, and reconciliation status.
>
> The most central concept was the distinction between advisory search availability and authoritative booking confirmation. A new engineer needed to understand that first. The API layer was intentionally thin, while the inherently complex part was coordinating several external systems that had different contracts and ambiguous timeout behavior.

### Question-by-question answer expectations

#### Can you walk me through the architecture at a high level?

A strong answer should be understandable without code-level detail.

Useful order:

> User/client → entry point → core domain behavior → persistence → external dependencies → async side effects → operations

The candidate should pause after the overview and allow deeper follow-up.

#### What were the major components or layers in the system?

Strong candidates name components by responsibility, not only technology.

Better:

* booking orchestrator;
* availability read model;
* vendor adapter layer;
* notification consumer.

Weaker:

* React;
* Node;
* PostgreSQL;
* Kafka.

Technologies may be included after responsibilities are clear.

#### What role did each major component play?

The answer should make boundaries visible.

Good phrasing:

> This component owned X, depended on Y, and emitted Z.

#### How did data, requests, or events flow through the architecture?

A strong candidate explains at least one end-to-end flow.

The answer should identify:

* synchronous versus asynchronous steps;
* durable state changes;
* authoritative checks;
* emitted events;
* failure or retry points.

#### Which part of the architecture was most central to the system’s behavior?

This tests whether the candidate recognizes the conceptual center.

Possible answers:

* state machine;
* workflow engine;
* domain model;
* event log;
* read model;
* policy layer;
* shared data contract.

The candidate should explain why.

#### What part would a new engineer need to understand first?

A strong answer identifies the mental model that prevents common mistakes.

Examples:

* source of truth;
* ownership boundary;
* consistency model;
* lifecycle state machine;
* event semantics;
* tenant boundary.

#### What was intentionally simple in the architecture?

Good answers may include:

* one relational database;
* stateless API layer;
* single-region deployment;
* thin clients;
* managed queue;
* direct service calls for low-risk paths.

The candidate should show that simplicity was a choice, not an omission.

#### What was inherently complex because of the problem itself?

The candidate should distinguish domain complexity from accidental complexity.

Examples:

* eligibility rules;
* uncertain external outcomes;
* multi-party approval;
* temporal scheduling;
* regulatory auditability;
* distributed ownership.

### Follow-up probes for the interviewer

* Can you draw the main request path verbally?
* Where was durable state written?
* Which system was authoritative?
* What happened after the response returned?
* Where could partial failure occur?
* Which component had the broadest blast radius?
* What would you remove to simplify the architecture?
* Which component was easiest to misunderstand?

### Weak-answer signals

Watch for answers that:

* list technologies instead of responsibilities;
* start at implementation detail with no system overview;
* cannot explain a complete request flow;
* omit state ownership;
* ignore asynchronous work;
* describe every component as equally important;
* cannot distinguish domain complexity from architectural complexity;
* provide a polished diagram narrative with no explanation of why components exist.

---


## B. Architectural alternatives and decision rationale

* Why did you choose this architecture instead of one or two plausible alternatives?
* What other designs did you seriously consider?
* What made those alternatives less appropriate in this context?
* Which constraints or goals pushed you toward the chosen design?
* Was there an architecture that would have been technically cleaner but less practical?
* Was there an architecture that would have been faster to ship but harder to evolve?
* If a different team built the same product, what architectural choice might they reasonably make differently?
* What would have had to be true for you to choose a different architecture?

What this reveals:
Whether they can reason from context to design choice, and whether they understand that architecture is selected among alternatives rather than discovered as a single “correct” answer.

### Clarifying questions a strong candidate may ask

* Should I compare the final design with the original design or with external alternatives?
* Would you like one alternative in depth or several briefly?
* Should I include alternatives that were rejected for organizational reasons?
* Are you most interested in architecture style, data flow, or deployment choices?
* Should I explain what conditions would have made another option preferable?

These questions show that architecture is contextual. A strong candidate does not present the chosen design as universally correct.

### Reasoning expected from the candidate

A mature comparison should cover:

1. **Chosen option**
   * What was selected?
2. **Plausible alternatives**
   * What else could reasonably have worked?
3. **Evaluation criteria**
   * Delivery time, correctness, cost, scale, ownership, migration, or operations?
4. **Context**
   * Which constraints made one option better?
5. **Rejected costs**
   * Why were alternatives less appropriate?
6. **Conditionality**
   * Under what different assumptions would the decision change?
7. **Reversibility**
   * How difficult would it be to change later?

A strong candidate compares real alternatives rather than obviously bad strawmen.

### Example of a strong coherent answer

> We considered three broad designs.
>
> The first was direct fan-out from the patient request to every clinic scheduling system. It would have been fast to prototype and always queried fresh data, but search latency and availability would have been coupled to the slowest vendor. It also would have consumed vendor quotas quickly.
>
> The second was to copy all appointment inventory into a new centralized scheduling database and make our platform authoritative. That would have simplified the online experience technically, but it required replacing operational workflows across hundreds of clinics. It was not realistic for the rollout timeline or ownership model.
>
> The chosen design used an asynchronously refreshed availability read model for search and authoritative vendor confirmation for booking. It accepted limited search staleness in exchange for lower latency and less dependency coupling, while preserving correctness at confirmation.
>
> We also considered a broad microservice decomposition. We chose a smaller number of services because the team was small and the domain boundaries were still evolving. A larger organization with independently owned clinic domains might reasonably split the system differently.
>
> If clinic systems had provided fast, reliable, standardized APIs with generous quotas, direct querying would have been more attractive. If the organization had committed to replacing clinic schedulers, a centralized source-of-truth architecture might have been better.

### Question-by-question answer expectations

#### Why did you choose this architecture instead of one or two plausible alternatives?

The candidate should state:

* alternatives;
* criteria;
* chosen tradeoff;
* context.

Strong answer pattern:

> We chose X over Y because constraint Z made A more important than B.

#### What other designs did you seriously consider?

Good alternatives should be plausible.

Examples:

* monolith versus services;
* synchronous versus event-driven;
* direct query versus read model;
* relational versus document storage;
* centralized orchestration versus choreography;
* build versus managed service.

#### What made those alternatives less appropriate in this context?

The candidate should explain specific costs:

* migration risk;
* operational burden;
* weak team ownership;
* latency;
* consistency;
* external limits;
* delivery timing;
* high fixed cost.

#### Which constraints or goals pushed you toward the chosen design?

The answer should trace context to architecture.

Examples:

* strict correctness → authoritative confirmation;
* bursty work → queueing;
* small team → fewer deployment units;
* vendor diversity → adapters;
* fast launch → managed infrastructure;
* high read ratio → denormalized read model.

#### Was there an architecture that would have been technically cleaner but less practical?

Strong candidates recognize that organizational migration and delivery constraints matter.

Examples:

* clean rewrite versus incremental integration;
* perfect domain split versus existing ownership;
* custom platform versus managed service;
* unified schema versus compatibility adapters.

#### Was there an architecture that would have been faster to ship but harder to evolve?

Good answers explain the debt intentionally accepted or avoided.

Examples:

* direct database sharing;
* client-specific endpoints;
* synchronous chaining;
* duplicated rules;
* one oversized service.

#### If a different team built the same product, what architectural choice might they reasonably make differently?

This tests intellectual humility.

A strong answer identifies a choice sensitive to:

* team size;
* existing platforms;
* operational maturity;
* customer mix;
* regulatory environment;
* scale.

#### What would have had to be true for you to choose a different architecture?

This is a high-signal conditional reasoning question.

Good answers name changed assumptions, not personal preference.

### Follow-up probes for the interviewer

* Which alternative came closest to winning?
* Who advocated for it?
* What evidence changed the decision?
* Which option had the lowest migration cost?
* Which choice was hardest to reverse?
* Was the decision documented?
* Did production invalidate any comparison?
* Which alternative would you choose today?

### Weak-answer signals

Watch for answers that:

* claim there was only one reasonable design;
* compare against obviously bad alternatives;
* use “best practice” as the main rationale;
* cannot explain evaluation criteria;
* ignore team and operational context;
* present more distributed architecture as automatically superior;
* cannot state what conditions would change the decision;
* defend the chosen architecture without acknowledging costs.

---


## C. Major tradeoffs and design priorities

* What were the top design decisions that shaped the rest of the system?
* Which tradeoffs did you knowingly make around simplicity, performance, reliability, flexibility, cost, and speed of delivery?
* Which quality did you optimize for most strongly?
* What did you intentionally sacrifice or de-prioritize?
* Where did the design favor short-term delivery over long-term flexibility?
* Where did it favor reliability or correctness over simplicity?
* Which tradeoff was hardest to explain to stakeholders or teammates?
* Looking back, which tradeoff still feels right, and which one would you revisit?

What this reveals:
Whether they understand architecture as priority-setting and tradeoff navigation, not as applying generic best practices.

### Clarifying questions a strong candidate may ask

* Should I focus on the top two or three tradeoffs rather than every decision?
* Would you like product and organizational tradeoffs as well as technical ones?
* Should I discuss tradeoffs at launch or those revealed later?
* Are you most interested in which quality attributes we prioritized?
* Should I include a tradeoff I would now reverse?

These questions signal that architecture is a prioritization exercise.

### Reasoning expected from the candidate

A strong answer should name the competing qualities explicitly:

* simplicity versus flexibility;
* latency versus freshness;
* correctness versus availability;
* delivery speed versus long-term adaptability;
* cost versus resilience;
* local autonomy versus consistency;
* developer convenience versus operational transparency.

The candidate should explain:

1. what was optimized;
2. what was sacrificed;
3. why that priority was appropriate;
4. who paid the cost;
5. how the tradeoff was monitored;
6. whether it remained valid.

### Example of a strong coherent answer

> Three tradeoffs shaped the architecture.
>
> First, we chose search responsiveness and dependency isolation over perfectly fresh availability. The read model could be several minutes stale, but booking confirmation always revalidated against the clinic system.
>
> Second, we chose correctness and recoverability over implementation simplicity in booking. A simple request-response flow would have been easier, but uncertain vendor outcomes required durable workflow state and reconciliation.
>
> Third, we chose fewer services over maximum team autonomy. The team was small and the domain boundaries were still changing, so a larger microservice split would have increased deployment and coordination overhead.
>
> We intentionally deprioritized global multi-region availability and support for every clinic-specific rule in the first release. The hardest tradeoff to explain was why a slot shown in search could occasionally disappear during confirmation. Product initially viewed that as inconsistency, but it was the result of preserving a fast browsing experience while keeping final booking correct.
>
> Looking back, the freshness tradeoff still feels right. I would revisit how much responsibility accumulated in the booking orchestrator because adding more workflow variants made it harder to change safely.

### Question-by-question answer expectations

#### What were the top design decisions that shaped the rest of the system?

The candidate should choose only the decisions with broad consequences.

Examples:

* source of truth;
* sync versus async boundary;
* state ownership;
* service decomposition;
* consistency model;
* deployment model;
* data partitioning.

#### Which tradeoffs did you knowingly make?

A strong answer names both sides.

Weak:

> We chose caching for performance.

Strong:

> We accepted bounded staleness and invalidation complexity to reduce latency and vendor load.

#### Which quality did you optimize for most strongly?

The candidate should identify one dominant quality and justify it.

Possible answers:

* correctness;
* availability;
* speed of delivery;
* developer velocity;
* cost;
* latency;
* evolvability.

#### What did you intentionally sacrifice or de-prioritize?

High-signal answers include explicit non-goals.

The candidate should avoid pretending nothing was sacrificed.

#### Where did the design favor short-term delivery over long-term flexibility?

A mature answer explains why the debt was acceptable and how it was contained.

Examples:

* limited configuration;
* manual operations;
* adapter duplication;
* single-region deployment;
* temporary compatibility layer.

#### Where did it favor reliability or correctness over simplicity?

Good examples:

* idempotency;
* reconciliation;
* transaction boundaries;
* durable state;
* duplicate detection;
* conservative fail-closed behavior.

#### Which tradeoff was hardest to explain to stakeholders or teammates?

The candidate should explain:

* why it was unintuitive;
* how it was communicated;
* what evidence or prototype helped;
* what compromise was accepted.

#### Looking back, which tradeoff still feels right, and which one would you revisit?

Strong answers demonstrate reflection without rewriting history unfairly.

### Follow-up probes for the interviewer

* Who paid the cost of that tradeoff?
* What metric represented the sacrificed quality?
* What would have made the opposite choice better?
* Did the tradeoff change after launch?
* Which tradeoff was reversible?
* Which one became structural?
* What did stakeholders initially misunderstand?
* What tradeoff would a junior engineer miss?

### Weak-answer signals

Watch for answers that:

* describe benefits without costs;
* say all quality attributes were equally prioritized;
* cannot name an explicit sacrifice;
* use “scalable and maintainable” without specifics;
* justify short-term debt with no containment plan;
* cannot identify who paid the cost;
* defend every original decision;
* discuss tradeoffs only in generic textbook language.

---


## D. Placement of complexity and responsibility

* Where did you centralize complexity?
* Where did you push complexity to the edges?
* What logic belonged in the core system versus clients, workers, services, or integrations?
* Which parts of the system were kept deliberately dumb or thin?
* Which component carried the most responsibility, and was that intentional?
* Did the architecture create any “god component” or overly powerful coordination point?
* Where did the architecture reduce complexity for one group but increase it for another?
* Who paid the cost of the hardest complexity: users, developers, operators, clients, or downstream systems?

What this reveals:
Whether they can reason about where complexity lives in a system and how architectural decisions shift burden between components and people.

### Clarifying questions a strong candidate may ask

* Should I discuss domain complexity, integration complexity, or operational complexity?
* Would you like the original placement of responsibility or how it shifted over time?
* Should I focus on one component that accumulated too much responsibility?
* Are you interested in client-server placement as well as service boundaries?
* Should I explain who benefited and who absorbed the complexity?

These questions show awareness that architecture does not remove complexity; it relocates it.

### Reasoning expected from the candidate

A mature answer should explain:

1. **What complexity existed**
   * Rules, state transitions, integration differences, retries, or policy?
2. **Where it was placed**
   * Core domain, adapter, client, worker, middleware, or operator process?
3. **Why**
   * Consistency, ownership, security, testability, or reuse?
4. **Who benefited**
   * Clients, users, developers, or operators?
5. **Who paid**
   * Another component or team often absorbs the burden.
6. **Visibility**
   * Was complexity explicit or hidden?
7. **Concentration risk**
   * Did one component become a bottleneck or “god component”?

### Example of a strong coherent answer

> We centralized booking lifecycle complexity in the workflow orchestrator because correctness rules, retries, idempotency, and reconciliation needed one consistent owner. That kept the web client and API layer thin and prevented vendor-specific behavior from leaking into product code.
>
> We pushed vendor translation to adapters at the edge. Each adapter converted vendor-specific identifiers, statuses, and errors into a normalized contract. That increased adapter implementation work, but protected the core domain from external inconsistency.
>
> The patient client handled presentation state and optimistic navigation, but it did not own booking truth or authorization. Notification consumers were deliberately dumb: they reacted to confirmed domain events rather than reconstructing booking rules.
>
> Over time, the orchestrator accumulated eligibility rules, cancellation variants, and support overrides. It became too powerful. The original centralization was intentional, but the internal structure did not evolve enough. I would separate policy evaluation from workflow coordination while keeping final state transitions centralized.
>
> The complexity reduction for frontend developers increased the burden on backend and operations teams. That was acceptable because correctness and supportability required a single authoritative workflow, but it needed better internal modularity and tooling.

### Question-by-question answer expectations

#### Where did you centralize complexity?

Strong candidates name complexity that benefits from one owner:

* authorization;
* state machine;
* pricing;
* workflow coordination;
* policy;
* schema translation;
* audit logging.

They should explain why centralization improved consistency.

#### Where did you push complexity to the edges?

Common edge complexity:

* external adapters;
* serialization;
* protocol handling;
* client presentation;
* ingestion normalization;
* compatibility shims.

The candidate should explain why the core was protected.

#### What logic belonged in the core system versus clients, workers, services, or integrations?

A strong answer uses principles such as:

* business invariants stay authoritative on the server;
* presentation logic stays in clients;
* slow or retryable work moves to workers;
* vendor-specific behavior stays in adapters;
* shared policy stays near the domain owner.

#### Which parts of the system were kept deliberately dumb or thin?

Good answers identify components that should not make domain decisions.

Examples:

* API gateway;
* transport controller;
* event consumer;
* UI component;
* vendor wrapper;
* queue worker.

#### Which component carried the most responsibility, and was that intentional?

The candidate should distinguish healthy centrality from accidental accumulation.

#### Did the architecture create any “god component” or overly powerful coordination point?

Strong answers acknowledge warning signs:

* many unrelated reasons to change;
* broad dependency graph;
* central release bottleneck;
* hard-to-test branching;
* team ownership conflict;
* disproportionate incident impact.

#### Where did the architecture reduce complexity for one group but increase it for another?

This is a high-signal cost-shifting question.

Examples:

* backend-for-frontend simplifies UI but increases API variants;
* platform abstraction simplifies product teams but burdens platform operators;
* async processing improves latency but complicates support;
* schema normalization simplifies consumers but burdens ingestion.

#### Who paid the cost of the hardest complexity?

The candidate should name the people or systems carrying operational or cognitive burden.

### Follow-up probes for the interviewer

* What logic was duplicated?
* What complexity became hidden?
* Which component changed most often?
* Who owned the central component?
* What did clients no longer need to know?
* What did operators need to understand?
* How would you split the god component?
* Which complexity was unavoidable?

### Weak-answer signals

Watch for answers that:

* claim architecture eliminated complexity;
* place business rules in multiple clients;
* centralize everything without ownership rationale;
* push correctness to external systems blindly;
* cannot identify who absorbed complexity;
* ignore operational complexity;
* deny that any component became too powerful;
* confuse thin components with unimportant components.

---


## E. Coupling, cohesion, and architectural seams

* What parts of the system were tightly coupled?
* Was that coupling intentional?
* Where did you try to preserve loose coupling?
* What were the most important architectural seams or interfaces?
* Which components changed together most often?
* Which components could be replaced or evolved independently?
* Did the architecture reflect the business domain well, or did it expose implementation details?
* What coupling seemed harmless early but became painful later?

What this reveals:
Whether they understand how architectural boundaries affect changeability, ownership, coordination, and long-term maintainability.

### Clarifying questions a strong candidate may ask

* Should I focus on code-level coupling, service coupling, data coupling, or team coupling?
* Would you like examples of intentional tight coupling and accidental coupling?
* Should I discuss current seams or seams we wished we had?
* Are you interested in replacement boundaries or change frequency?
* Should I explain how coupling showed up operationally?

These questions show that coupling exists through data, deployments, behavior, timing, and organizational coordination.

### Reasoning expected from the candidate

A strong answer should analyze:

* **structural coupling:** direct dependencies;
* **data coupling:** shared schema or database;
* **temporal coupling:** both systems must be available together;
* **behavioral coupling:** one component depends on undocumented behavior;
* **deployment coupling:** changes must release together;
* **organizational coupling:** teams must coordinate for every change.

The candidate should also discuss cohesion:

* Do responsibilities inside a component belong together?
* Do components change for related reasons?

Architectural seams should correspond to stable concepts, ownership boundaries, or replaceable integrations.

### Example of a strong coherent answer

> The booking orchestrator was intentionally tightly coupled to the booking state model because those responsibilities changed together and shared invariants.
>
> Vendor adapters were loosely coupled to the core through a normalized scheduling contract. That allowed us to add or replace vendors without changing product-facing APIs, although the abstraction was imperfect because some vendor capabilities did not map cleanly.
>
> The most important seams were the patient API contract, the vendor adapter interface, and confirmed booking events. The notification service could evolve independently because it consumed a stable fact rather than querying internal workflow tables.
>
> The most painful coupling was shared clinic configuration. Several services read the same schema directly, so a field change required coordinated releases. It seemed harmless because the data was simple, but it became a deployment constraint. We later introduced a configuration service and versioned contract.
>
> The architecture reflected the business domain reasonably well around booking and appointment inventory, but some vendor error codes leaked into internal workflow states. That exposed integration details and made support behavior inconsistent.

### Question-by-question answer expectations

#### What parts of the system were tightly coupled?

A strong answer names the coupling type and reason.

Tight coupling is not automatically bad. It may be appropriate when responsibilities share invariants and change together.

#### Was that coupling intentional?

The candidate should distinguish:

* deliberate cohesion;
* tolerated debt;
* accidental leakage;
* temporary migration coupling.

#### Where did you try to preserve loose coupling?

Common mechanisms:

* stable interfaces;
* events;
* adapters;
* owned databases;
* versioned schemas;
* asynchronous boundaries;
* anti-corruption layers.

The candidate should discuss the cost of loose coupling too.

#### What were the most important architectural seams or interfaces?

Strong seams often align with:

* domain boundary;
* external integration;
* team ownership;
* data ownership;
* replaceable component;
* lifecycle stage.

#### Which components changed together most often?

This tests whether actual change patterns match architecture.

If components always change together, the boundary may be artificial or the contract unstable.

#### Which components could be replaced or evolved independently?

The candidate should explain what makes replacement realistic:

* stable contract;
* isolated data;
* test harness;
* migration path;
* limited side effects;
* no shared database.

#### Did the architecture reflect the business domain well, or did it expose implementation details?

Strong answers identify both good alignment and leakage.

Examples of leakage:

* database IDs in public APIs;
* vendor statuses in domain models;
* UI-specific shapes in core services;
* transport errors becoming business outcomes.

#### What coupling seemed harmless early but became painful later?

High-signal examples:

* shared database;
* shared utility library;
* synchronous call chain;
* duplicated enum;
* direct event payload reuse;
* shared deployment pipeline;
* implicit ordering.

### Follow-up probes for the interviewer

* Could the components deploy independently?
* Did they share a database?
* What happened when the contract changed?
* Was the event truly stable?
* Which seam had the most versioning pain?
* Where was temporal coupling hidden?
* Which components should be merged?
* Which should be separated?

### Weak-answer signals

Watch for answers that:

* say all coupling is bad;
* cannot identify coupling beyond imports;
* use events but remain tightly coupled to payload internals;
* claim services are independent despite shared databases and coordinated releases;
* cannot identify change patterns;
* confuse loose coupling with lack of contracts;
* ignore team and deployment coupling;
* cannot name a painful seam.

---


## F. Design risks and lessons learned

* What part of the design gave you the most concern at the time?
* What part looked good on paper but turned out awkward in practice?
* Which design decision bought the most leverage?
* Which decision created the most future work?
* What surprised you after the system was built or operated?
* What would you redesign if you were starting again?
* What did this architecture make easier than expected?
* What did it make harder than expected?

What this reveals:
Whether they can reflect honestly on architectural risk, unintended consequences, and what they learned from real usage rather than only defending the original design.

### Clarifying questions a strong candidate may ask

* Should I focus on risks known during design or those discovered in production?
* Would you like one design mistake in depth?
* Should I discuss my personal judgment or the team’s overall decision?
* Are you interested in technical lessons, operational lessons, or both?
* Should I explain what I would redesign under the same constraints?

These questions show that reflection should account for the information and constraints available at the time.

### Reasoning expected from the candidate

A strong retrospective answer should include:

1. **Original concern**
   * What risk was known?
2. **Prediction**
   * What did the team expect?
3. **Observed reality**
   * What happened in production?
4. **Consequence**
   * Cost, incidents, delivery friction, or user impact?
5. **Response**
   * What changed?
6. **Lesson**
   * What principle or judgment improved?
7. **Fair redesign**
   * What would change under the same constraints, not an imaginary greenfield?

A mature candidate can defend some decisions and criticize others without becoming defensive.

### Example of a strong coherent answer

> The area that concerned us most was uncertain booking outcomes from external systems. We addressed it with durable pending state and reconciliation, and that investment paid off. It prevented duplicate bookings and gave support teams a recoverable workflow.
>
> The design that looked cleaner on paper than in practice was the normalized vendor contract. We tried to make every scheduling vendor look identical, but some had fundamentally different cancellation and eligibility semantics. The abstraction hid important differences until runtime. We later made capabilities explicit rather than forcing every vendor into the same shape.
>
> The highest-leverage decision was separating search from authoritative confirmation. It reduced latency and quota pressure without weakening final correctness.
>
> The decision that created the most future work was allowing multiple services to read clinic configuration tables directly. It accelerated the pilot but created schema and deployment coupling.
>
> What surprised us was that operational investigation, not core throughput, became the dominant challenge. The architecture needed richer workflow history and replay tooling earlier.
>
> If rebuilding under the same constraints, I would keep the overall system shape but create a clearer policy layer, capability-aware vendor contracts, and stronger ownership around shared configuration.

### Question-by-question answer expectations

#### What part of the design gave you the most concern at the time?

The candidate should explain:

* risk;
* likelihood;
* impact;
* mitigation;
* residual uncertainty.

#### What part looked good on paper but turned out awkward in practice?

Strong answers identify the mismatch between model and reality.

Examples:

* overly generic abstraction;
* event choreography hard to trace;
* service boundary requiring constant coordination;
* cache invalidation burden;
* shared schema instability;
* serverless cold-start behavior.

#### Which design decision bought the most leverage?

A good answer names a decision that simplified multiple future problems.

Examples:

* clear source of truth;
* durable event log;
* adapter boundary;
* modular monolith;
* shared identity platform;
* state machine.

#### Which decision created the most future work?

The candidate should identify downstream consequences, not merely say “technical debt.”

#### What surprised you after the system was built or operated?

High-signal answers may involve:

* unexpected traffic shape;
* support burden;
* data quality;
* dependency behavior;
* user workflow;
* organizational ownership;
* cost profile.

#### What would you redesign if you were starting again?

A strong answer preserves constraints and explains expected benefit.

#### What did this architecture make easier than expected?

Examples:

* adding new consumers;
* isolating vendor failure;
* scaling reads;
* replacing a client;
* testing workflows;
* onboarding teams.

#### What did it make harder than expected?

Examples:

* debugging async flows;
* evolving shared schemas;
* local development;
* incident ownership;
* cross-service transactions;
* maintaining duplicated read models.

### Follow-up probes for the interviewer

* What evidence changed your mind?
* Did you recognize the risk before launch?
* What did the team do afterward?
* Which lesson generalized to later projects?
* What would you keep exactly the same?
* Was the issue architectural or operational?
* Which change paid back quickly?
* What warning sign did you miss?

### Weak-answer signals

Watch for answers that:

* claim nothing significant went wrong;
* blame only implementation quality;
* redesign everything as a greenfield system;
* cannot name a surprise;
* defend all original choices;
* provide lessons with no concrete event;
* confuse hindsight with obviousness;
* cannot connect architecture to future work or operational burden.

---

# Cross-section answer framework

Candidates can use this structure to answer most architecture questions:

1. **Purpose**
   * What capability did the system provide?
2. **Shape**
   * What were the major components and responsibilities?
3. **Flow**
   * How did requests, data, and events move?
4. **Authority**
   * Where did state live, and what was the source of truth?
5. **Alternatives**
   * What other plausible designs were considered?
6. **Decision criteria**
   * Which goals and constraints favored the chosen design?
7. **Tradeoffs**
   * What became easier, and what became harder?
8. **Complexity placement**
   * Where did the hardest logic live, and who paid the cost?
9. **Coupling**
   * Which seams enabled independent change, and which became painful?
10. **Reflection**
   * What worked, what surprised the team, and what would change?

A strong answer gives the interviewer a mental model first, then uses one or two deep examples to demonstrate judgment.

---

# Interviewer scoring guide

## Strong signal

The candidate:

* explains architecture by responsibility rather than technology;
* describes a coherent end-to-end flow;
* identifies sources of truth and durable state;
* distinguishes synchronous and asynchronous behavior;
* compares plausible alternatives fairly;
* ties decisions to constraints and goals;
* names explicit tradeoffs and sacrificed qualities;
* explains where complexity was centralized or pushed outward;
* recognizes data, temporal, deployment, and team coupling;
* identifies one leverage point and one source of future work;
* reflects honestly on production surprises;
* proposes a redesign consistent with the original constraints.

## Mixed signal

The candidate:

* gives a reasonable component overview but weak decision rationale;
* names alternatives without comparing costs;
* discusses tradeoffs generically;
* understands service boundaries but not operational coupling;
* identifies lessons but cannot trace them to concrete outcomes;
* explains the architecture but not why it took that shape.

## Weak signal

The candidate:

* lists technologies instead of architecture;
* cannot describe a full flow;
* presents the chosen design as the only valid option;
* uses best-practice language without context;
* cannot name what was sacrificed;
* claims complexity was eliminated;
* ignores coupling outside code imports;
* cannot identify a design risk or surprise;
* redesigns everything without acknowledging migration, team, or delivery constraints.

---

# Practice exercise for candidates

Choose one project and answer the following in one coherent narrative:

1. What capability did the architecture provide?
2. What were the five or fewer major components?
3. How did the most important request flow through them?
4. Where was durable state, and what was authoritative?
5. What was the conceptual center of the design?
6. What two alternatives were seriously considered?
7. Which constraints favored the chosen option?
8. What were the top two architectural tradeoffs?
9. Where did the hardest complexity live?
10. Which coupling was intentional, and which became painful?
11. What decision created the most leverage?
12. What would you redesign under the same constraints?

A strong response should be clear enough for someone to sketch the architecture, understand why it was chosen, and identify its main strengths, costs, and limits.
