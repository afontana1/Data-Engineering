# API Design Patterns - Evolution

# Table of Contents

- [Evolution](#evolution)
  - [Version Identifier](#version-identifier)
  - [Semantic Versioning](#semantic-versioning)
  - [Two In Production](#two-in-production)
  - [Aggressive Obsolescence](#aggressive-obsolescence)
  - [Experimental Preview](#experimental-preview)
  - [Limited Lifetime Guarantee](#limited-lifetime-guarantee)
  - [Eternal Lifetime Guarantee](#eternal-lifetime-guarantee)

---
### Evolution

These patterns help APIs change over time without breaking consumers unnecessarily.

#### Version Identifier

**What it is**

A Version Identifier marks which version of an API, resource, or representation a client is using.

**What it solves**

It allows APIs to evolve while preserving compatibility for existing clients.

**Use cases**

Use it for breaking changes such as removing fields, renaming fields, changing response structures, changing semantics, changing validation rules, or replacing endpoint behavior.

**Trade-offs**

Versioning creates maintenance overhead and should not be used for every minor additive change.

---

#### Semantic Versioning

**What it is**

Semantic Versioning uses version numbers to communicate change type: major for breaking changes, minor for backward-compatible features, and patch for backward-compatible fixes.

**What it solves**

It helps consumers understand upgrade risk.

**Use cases**

Use it for SDKs, API schemas, event contracts, API specifications, client libraries, and public developer platforms.

**Trade-offs**

It requires discipline and a shared definition of what counts as breaking, additive, or patch-level change.

---

#### Two In Production

**What it is**

Two In Production means running two API versions in production at the same time.

**What it solves**

It enables gradual migration when clients cannot all upgrade at once.

**Use cases**

Use it for breaking changes, public APIs, enterprise customers, and mobile apps that cannot be updated instantly.

**Trade-offs**

Running multiple versions increases support and operational cost.

---

#### Aggressive Obsolescence

**What it is**

Aggressive Obsolescence retires old API versions quickly after a new version is available.

**What it solves**

It prevents the provider from supporting too many old versions for too long.

**Use cases**

Use it for internal APIs, coordinated consumers, security-driven deprecations, or expensive legacy endpoints.

**Trade-offs**

Short migration windows can frustrate or break consumers without strong communication and monitoring.

---

#### Experimental Preview

**What it is**

Experimental Preview exposes a feature early with the understanding that it may change.

**What it solves**

It lets API providers gather feedback before committing to a stable contract.

**Use cases**

Use it for beta features, new endpoints, new response formats, early partner testing, research-backed features, and new algorithms or workflows.

**Trade-offs**

Preview APIs must be clearly labeled so consumers understand compatibility is not guaranteed.

---

#### Limited Lifetime Guarantee

**What it is**

A Limited Lifetime Guarantee promises support for an API version or contract for a defined time period.

**What it solves**

It balances consumer stability with provider maintainability.

**Use cases**

Use it for public APIs, partner APIs, enterprise integrations, versioned APIs, and contract migrations.

**Trade-offs**

Providers must track release dates, deprecation notices, and client usage.

---

#### Eternal Lifetime Guarantee

**What it is**

An Eternal Lifetime Guarantee promises that an API version or contract will remain supported indefinitely or for a very long time.

**What it solves**

It provides maximum stability for consumers that are difficult to update.

**Use cases**

Use it rarely, usually for public APIs with massive adoption, critical infrastructure APIs, standards-based APIs, embedded clients, or long-lived enterprise integrations.

**Trade-offs**

It is expensive and can freeze bad design decisions indefinitely.
