# Table of Contents

- [7. Service Discovery, Configuration, and Runtime Infrastructure Patterns](#7-service-discovery-configuration-and-runtime-infrastructure-patterns)
  - [31. Service Discovery / Service Registry](#31-service-discovery-service-registry)
  - [32. External Configuration](#32-external-configuration)
  - [33. Sidecar](#33-sidecar)

---
## 7. Service Discovery, Configuration, and Runtime Infrastructure Patterns

These patterns manage dynamic runtime environments and shared infrastructure concerns.

### 31. Service Discovery / Service Registry

**What it is**

Service Discovery allows services to find available service instances dynamically. A Service Registry is the directory where instances register and are discovered.

**What it solves**

It avoids hardcoded service addresses in dynamic environments.

**Use cases**

Use it in containerized, cloud-native, autoscaling, or service mesh environments.

**Benefits**

It enables dynamic routing, scaling, failover, and service-to-service communication.

**Trade-offs**

Discovery infrastructure must be reliable, and stale entries or DNS caching can cause traffic failures.

---

### 32. External Configuration

**What it is**

External Configuration stores application configuration outside code and deployment artifacts.

**What it solves**

It avoids rebuilding or redeploying code just to change configuration.

**Use cases**

Use it for environment-specific values, feature flags, timeout settings, retry policies, credentials, and service endpoints.

**Benefits**

It improves operational flexibility.

**Trade-offs**

Bad configuration can break good code, so validation, versioning, secret management, and rollback are important.

---

### 33. Sidecar

**What it is**

Sidecar runs a helper process or container beside the main service.

**What it solves**

It avoids duplicating infrastructure capabilities inside every service.

**Use cases**

Use it for service mesh proxies, logging agents, metrics collectors, certificate rotation, security agents, configuration reloaders, and local caching.

**Benefits**

It keeps application code focused on business logic.

**Trade-offs**

Sidecars add resource overhead and operational complexity.

---
