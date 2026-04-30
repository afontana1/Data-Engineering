# API Design Patterns - Quality

# Table of Contents

- [Quality](#quality)
  - [API Key](#api-key)
  - [Rate Limit](#rate-limit)
  - [Rate Plan](#rate-plan)
  - [Service Level Agreement](#service-level-agreement)
  - [Error Report](#error-report)
  - [Conditional Request](#conditional-request)
  - [Request Bundle](#request-bundle)
  - [Wish List](#wish-list)
  - [Wish Template](#wish-template)
  - [Embedded Entity](#embedded-entity)
  - [Linked Information Holder](#linked-information-holder)

---
### Quality

These patterns improve API reliability, efficiency, governance, security, and usability.

#### API Key

**What it is**

An API Key is a token used to identify and sometimes authenticate an API consumer.

**What it solves**

It supports access control, usage tracking, quota enforcement, billing, and abuse prevention.

**Use cases**

Use it for developer access, partner integrations, usage tracking, rate limiting, simple authentication, and environment-specific access.

**Trade-offs**

API keys can be leaked or copied and are often not enough for strong security.

---

#### Rate Limit

**What it is**

A Rate Limit restricts how many requests a client can make within a time window.

**What it solves**

It protects APIs from overload and abuse while enforcing fair usage.

**Use cases**

Use it for public APIs, partner APIs, expensive endpoints, login endpoints, search APIs, write-heavy operations, and third-party integrations.

**Trade-offs**

Limits must be communicated clearly. Overly strict limits frustrate legitimate users; overly loose limits expose systems to overload.

---

#### Rate Plan

**What it is**

A Rate Plan defines different usage tiers for different consumers.

**What it solves**

It supports differentiated access, monetization, and capacity management.

**Use cases**

Use it for SaaS APIs, developer platforms, partner ecosystems, usage-based billing, customer-specific quotas, and internal versus external tiers.

**Trade-offs**

It requires account management, billing integration, monitoring, fair enforcement, and upgrade paths.

---

#### Service Level Agreement

**What it is**

A Service Level Agreement defines expected service levels such as availability, latency, support response time, error rate, throughput, data freshness, or recovery time.

**What it solves**

It sets expectations and accountability between provider and consumer.

**Use cases**

Use it for enterprise APIs, partner integrations, internal platform APIs, mission-critical systems, and paid API products.

**Trade-offs**

SLAs require measurement, monitoring, incident management, and sometimes financial penalties.

---

#### Error Report

**What it is**

An Error Report is a structured error response that helps clients understand what went wrong and how to respond.

**What it solves**

It replaces vague failures with programmatically useful error information.

**Use cases**

Use it for validation errors, authentication failures, authorization failures, rate limit errors, business rule violations, dependency failures, and partial failures.

**Trade-offs**

Errors must be useful without leaking sensitive information such as stack traces, secrets, or infrastructure details.

---

#### Conditional Request

**What it is**

A Conditional Request lets clients ask the server to return data only if it has changed.

**What it solves**

It reduces unnecessary data transfer.

**Use cases**

Use it for cached resources, static or semi-static data, product catalogs, reference data, user profiles, documents, and large responses.

**Trade-offs**

It requires correct cache validators such as ETags or last-modified timestamps.

---

#### Request Bundle

**What it is**

A Request Bundle combines multiple requests into one API call.

**What it solves**

It reduces network round trips.

**Use cases**

Use it for batch reads, batch updates, mobile APIs, offline sync, bulk operations, and reducing client chattiness.

**Trade-offs**

Batch APIs are harder to validate, authorize, execute, and partially fail.

---

#### Wish List

**What it is**

A Wish List lets clients specify which fields or related data they want included in the response.

**What it solves**

It prevents over-fetching.

**Use cases**

Use it when resources are large, different clients need different fields, mobile clients need smaller payloads, or responses include optional embedded data.

**Trade-offs**

Field selection increases API complexity and can create inefficient server-side query generation.

---

#### Wish Template

**What it is**

A Wish Template is a reusable named set of requested fields or included data.

**What it solves**

It standardizes repeated response shapes.

**Use cases**

Use it for summary views, detail views, mobile views, admin views, export views, and partner-specific views.

**Trade-offs**

Too many templates become hard to maintain and version.

---

#### Embedded Entity

**What it is**

An Embedded Entity includes a related resource directly inside the response.

**What it solves**

It reduces follow-up requests.

**Use cases**

Use it for order-with-customer summaries, product-with-category details, invoice-with-billing-address, shipment-with-carrier, and comment-with-author.

**Trade-offs**

Embedding increases response size and can introduce staleness or ownership ambiguity.

---

#### Linked Information Holder

**What it is**

A Linked Information Holder references related data through a link or identifier instead of embedding the full entity.

**What it solves**

It avoids over-fetching and preserves clear ownership of related resources.

**Use cases**

Use it when related data is large, changes frequently, is not always needed, or has different access control.

**Trade-offs**

Clients may need additional requests unless caching, prefetching, or optional embedding is available.

---
