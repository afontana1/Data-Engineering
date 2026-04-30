# API Design Patterns - Responsibility

# Table of Contents

- [Responsibility](#responsibility)
  - [Processing Resource](#processing-resource)
  - [Information Holder Resource](#information-holder-resource)
  - [Computation Function](#computation-function)
  - [State Creation Operation](#state-creation-operation)
  - [Retrieval Operation](#retrieval-operation)
  - [State Transition Operation](#state-transition-operation)
  - [Operational Data Holder](#operational-data-holder)
  - [Master Data Holder](#master-data-holder)
  - [Reference Data Holder](#reference-data-holder)
  - [Data Transfer Resource](#data-transfer-resource)
  - [Link Lookup Resource](#link-lookup-resource)

---
### Responsibility

These patterns describe what an API endpoint or resource is responsible for.

#### Processing Resource

**What it is**

A Processing Resource is an API resource that represents processing activity rather than a simple data object. It triggers computation, processing, validation, transformation, or workflow execution.

**What it solves**

It avoids forcing every API operation into CRUD-style resource modeling and prevents awkward action endpoints such as `/doPayment` or `/convertDocument`.

**Use cases**

Use it to start jobs, validate data, convert representations, run calculations, authorize payments, generate reports, or trigger asynchronous workflows.

**Example**

`POST /conversion-jobs` creates a document conversion job and returns a job ID.

**Trade-offs**

Processing resources should be named carefully. If overused, the API can become action-oriented and inconsistent.

---

#### Information Holder Resource

**What it is**

An Information Holder Resource represents a business object or data-holding entity, such as `/customers`, `/orders`, `/products`, `/accounts`, or `/invoices`.

**What it solves**

It models business information clearly and gives clients stable resources to retrieve, create, update, or delete.

**Use cases**

Use it for business entities, master data, operational records, reference data, documents, user profiles, orders, products, payments, and accounts.

**Trade-offs**

Not every capability should be modeled as an information holder. Some workflows are clearer as processing resources or transition operations.

---

#### Computation Function

**What it is**

A Computation Function calculates or derives a result without necessarily creating durable state.

**What it solves**

It exposes calculations cleanly through an API when the result is computed from inputs rather than stored as a permanent resource.

**Use cases**

Use it for tax calculation, pricing, shipping estimates, eligibility checks, risk scoring, currency conversion, recommendation scoring, and validation checks.

**Example**

`POST /shipping-estimates` returns available shipping options and costs based on cart and destination.

**Trade-offs**

These operations should usually be idempotent when possible.

---

#### State Creation Operation

**What it is**

A State Creation Operation creates a new resource or new system state, usually through `POST`.

**What it solves**

It distinguishes creating new state from reading or updating existing state.

**Use cases**

Use it to create orders, register users, open accounts, submit applications, start payment authorizations, create support tickets, or upload documents.

**Trade-offs**

Creation operations must handle duplicate submissions carefully, often with idempotency keys.

---

#### Retrieval Operation

**What it is**

A Retrieval Operation returns existing information without changing server-side state, usually through `GET`.

**What it solves**

It provides safe, predictable data access.

**Use cases**

Use it to fetch resources, search collections, list data, read status, download documents, or retrieve reference data.

**Trade-offs**

Retrieval endpoints can become expensive if they return too much data or support overly flexible queries. Pagination, filtering, field selection, and caching are often needed.

---

#### State Transition Operation

**What it is**

A State Transition Operation moves a resource from one meaningful lifecycle state to another.

**What it solves**

It models business workflows explicitly instead of letting clients patch arbitrary status fields.

**Use cases**

Use it for submitting applications, approving invoices, canceling orders, refunding payments, activating subscriptions, suspending accounts, closing tickets, or publishing articles.

**Example**

`POST /orders/123/cancellation` is clearer and safer than `PATCH /orders/123 { "status": "cancelled" }`.

**Trade-offs**

Too many transition endpoints can make the API large, but explicit transitions are often safer for important workflows.

---

#### Operational Data Holder

**What it is**

An Operational Data Holder stores data generated or used by day-to-day business operations, such as orders, payments, shipments, support tickets, and appointments.

**What it solves**

It distinguishes active business records from stable master or reference data.

**Use cases**

Use it for transactions, claims, bookings, work items, support tickets, payment attempts, and delivery records.

**Trade-offs**

Operational data often has complex lifecycle rules, so APIs should expose clear transitions and retrieval behavior.

---

#### Master Data Holder

**What it is**

A Master Data Holder represents core business entities reused across many processes, such as customers, products, suppliers, employees, and accounts.

**What it solves**

It provides canonical data across systems and processes.

**Use cases**

Use it for customer profiles, product catalog entries, merchant records, organization accounts, employee profiles, and supplier information.

**Trade-offs**

Master data often requires strong governance, duplicate detection, identity management, validation, versioning, and access control.

---

#### Reference Data Holder

**What it is**

A Reference Data Holder represents stable lookup data used to classify or constrain other data.

**What it solves**

It prevents clients from hardcoding valid values and classifications.

**Use cases**

Use it for country codes, currencies, status values, reason codes, product categories, tax categories, and shipping methods.

**Trade-offs**

Reference data is often cacheable, but clients need a way to detect changes.

---

#### Data Transfer Resource

**What it is**

A Data Transfer Resource represents resources designed mainly to move data across systems or API boundaries.

**What it solves**

It supports bulk movement, imports, exports, reporting, synchronization, and batch transfer.

**Use cases**

Use it for customer exports, catalog imports, bulk user uploads, reports, data snapshots, and synchronization jobs.

**Trade-offs**

Data transfer resources can be large, slow, and security-sensitive. They often need asynchronous processing, access controls, expiration, and audit logging.

---

#### Link Lookup Resource

**What it is**

A Link Lookup Resource helps clients discover or retrieve links to related resources.

**What it solves**

It improves discoverability and relationship navigation.

**Use cases**

Use it when resource links depend on permissions, resource state, dynamic relationships, or hypermedia-style navigation.

**Trade-offs**

It adds metadata and design complexity, so it is most valuable when relationships are dynamic.

---
