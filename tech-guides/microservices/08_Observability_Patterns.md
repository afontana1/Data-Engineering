# Table of Contents

- [8. Observability Patterns](#8-observability-patterns)
  - [34. Log Aggregation](#34-log-aggregation)
  - [35. Performance Metrics](#35-performance-metrics)
  - [36. Distributed Tracing](#36-distributed-tracing)

---
## 8. Observability Patterns

These patterns make distributed systems understandable, debuggable, and operable.

### 34. Log Aggregation

**What it is**

Log Aggregation collects logs from all services into a centralized searchable system.

**What it solves**

It solves scattered logs across many services, hosts, or containers.

**Use cases**

Use it for debugging, incident investigation, auditing, error detection, and request correlation.

**Benefits**

It gives teams one place to search and analyze logs.

**Trade-offs**

It can become expensive and requires retention policies, sensitive-data filtering, structured logging, and noise reduction.

---

### 35. Performance Metrics

**What it is**

Performance Metrics are numeric signals collected from services and infrastructure.

**What it solves**

They show whether the system is healthy, degraded, overloaded, or improving.

**Use cases**

Use metrics for dashboards, alerting, autoscaling, capacity planning, SLO monitoring, and regression detection.

**Benefits**

Metrics provide fast, high-level visibility.

**Trade-offs**

Metrics show what changed but not always why. Label cardinality and naming conventions must be managed carefully.

---

### 36. Distributed Tracing

**What it is**

Distributed Tracing follows a single request as it travels across multiple services.

**What it solves**

It helps teams understand request flow and latency in distributed systems.

**Use cases**

Use tracing to debug slow requests, identify bottlenecks, map dependencies, and investigate partial failures.

**Benefits**

It provides end-to-end visibility across service boundaries.

**Trade-offs**

It requires instrumentation, context propagation, sampling, and consistent metadata practices.

---
