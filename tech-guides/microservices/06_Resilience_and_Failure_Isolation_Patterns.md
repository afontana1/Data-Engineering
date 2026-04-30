# Table of Contents

- [6. Resilience and Failure Isolation Patterns](#6-resilience-and-failure-isolation-patterns)
  - [27. Circuit Breaker](#27-circuit-breaker)
  - [28. Retry](#28-retry)
  - [29. Bulkhead](#29-bulkhead)
  - [30. Health Check](#30-health-check)

---
## 6. Resilience and Failure Isolation Patterns

These patterns prevent localized failures from becoming system-wide outages.

### 27. Circuit Breaker

**What it is**

Circuit Breaker prevents repeated calls to a failing or slow dependency.

**What it solves**

It prevents cascading failure and resource exhaustion.

**Use cases**

Use it around service calls, third-party APIs, databases, payment providers, search services, and notification providers.

**Benefits**

It protects callers, reduces latency during outages, and gives dependencies time to recover.

**Trade-offs**

Thresholds must be tuned carefully.

---

### 28. Retry

**What it is**

Retry repeats an operation after a transient failure.

**What it solves**

It handles temporary failures such as network blips, service restarts, database failovers, throttling, DNS issues, and intermittent third-party failures.

**Use cases**

Use it for reads, idempotent writes, message processing, temporary API failures, and transient infrastructure errors.

**Benefits**

It improves reliability when failures are brief.

**Trade-offs**

Bad retries can create retry storms or duplicate non-idempotent operations.

---

### 29. Bulkhead

**What it is**

Bulkhead isolates resources so failure in one area does not consume all capacity.

**What it solves**

It limits blast radius.

**Use cases**

Use it for separate thread pools, connection pools, queues, compute resources, tenants, or critical versus non-critical workloads.

**Benefits**

It improves resilience and allows critical functions to survive partial failures.

**Trade-offs**

Too much isolation can waste resources; too little isolation leaves the system vulnerable.

---

### 30. Health Check

**What it is**

Health Check exposes whether a service instance is alive, ready, or healthy.

**What it solves**

It prevents traffic from being sent to unhealthy instances.

**Use cases**

Use it with Kubernetes, load balancers, service discovery, deployment systems, and autoscaling.

**Benefits**

It supports automated recovery, safer deployments, and better routing.

**Trade-offs**

Bad health checks can cause outages if they remove too many instances during temporary dependency failures.

---
