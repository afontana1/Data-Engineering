# API Design Patterns - Structure

# Table of Contents

- [Structure](#structure)
  - [Atomic Parameter](#atomic-parameter)
  - [Atomic Parameter List](#atomic-parameter-list)
  - [Parameter Tree](#parameter-tree)
  - [Parameter Forest](#parameter-forest)
  - [Data Element](#data-element)
  - [Id Element](#id-element)
  - [Link Element](#link-element)
  - [Metadata Element](#metadata-element)
  - [Annotated Parameter Collection](#annotated-parameter-collection)
  - [Context Representation](#context-representation)
  - [Pagination](#pagination)

---
### Structure

These patterns describe how API representations are shaped.

#### Atomic Parameter

**What it is**

An Atomic Parameter is a single indivisible value passed in a request or response, such as `customerId`, `email`, `limit`, `status`, or `currency`.

**What it solves**

It provides clarity for simple scalar values.

**Use cases**

Use it for identifiers, filters, flags, sorting fields, limits, dates, timestamps, and status values.

**Trade-offs**

Too many atomic parameters can make APIs hard to use. Related parameters may be better grouped.

---

#### Atomic Parameter List

**What it is**

An Atomic Parameter List is a list of simple values, such as `ids=1,2,3` or `fields=id,name,email`.

**What it solves**

It passes multiple values for the same purpose without creating a complex object.

**Use cases**

Use it for filtering by multiple IDs, selecting fields, passing multiple statuses, tags, categories, or batch retrieval keys.

**Trade-offs**

Lists need clear encoding, ordering, duplicate handling, maximum size, and error rules.

---

#### Parameter Tree

**What it is**

A Parameter Tree is a nested parameter structure that represents parent-child relationships.

**What it solves**

It supports complex inputs that flat query parameters cannot express cleanly.

**Use cases**

Use it for nested filters, search queries, validation rules, complex configuration, access policies, product option trees, and hierarchical categories.

**Trade-offs**

It is expressive but harder to validate, document, and support in simple GET query strings.

---

#### Parameter Forest

**What it is**

A Parameter Forest is a collection of multiple parameter trees in one request.

**What it solves**

It groups multiple structured concerns, such as filters, sorting, pagination, grouping, and output format.

**Use cases**

Use it for advanced search, complex reports, analytics queries, batch operations, and rule engines.

**Trade-offs**

It can be difficult for clients to construct and servers to validate.

---

#### Data Element

**What it is**

A Data Element is a normal business data field in a representation, such as name, amount, status, createdAt, or description.

**What it solves**

It separates business content from identifiers, links, and metadata.

**Use cases**

Use it for customer names, order totals, product descriptions, payment statuses, shipping addresses, and invoice amounts.

**Trade-offs**

Data elements must be stable and clearly defined because changes can break consumers.

---

#### Id Element

**What it is**

An Id Element uniquely identifies a resource or element.

**What it solves**

It gives clients a stable way to reference resources.

**Use cases**

Use IDs for resource identity, foreign references, correlation, deduplication, idempotency, and linking.

**Trade-offs**

IDs should be stable, opaque, and not expose sensitive implementation details.

---

#### Link Element

**What it is**

A Link Element provides a URI or reference to another resource or action.

**What it solves**

It improves discoverability and reduces hardcoded client navigation.

**Use cases**

Use it for self links, related resources, available actions, pagination links, download links, and state-dependent operations.

**Trade-offs**

Hypermedia-style APIs require client support and discipline.

---

#### Metadata Element

**What it is**

A Metadata Element describes the representation or resource but is not the main business data.

**What it solves**

It gives clients context about freshness, versioning, caching, lineage, localization, and interpretation.

**Use cases**

Use it for audit fields, ETags, versions, synchronization markers, locale, source, confidence, and processing status.

**Trade-offs**

Metadata should not become a dumping ground for unclear fields.

---

#### Annotated Parameter Collection

**What it is**

An Annotated Parameter Collection groups parameters with descriptive metadata such as labels, required flags, validation rules, or display hints.

**What it solves**

It helps clients dynamically render, validate, or interpret parameters.

**Use cases**

Use it for dynamic forms, API-driven UI, configurable workflows, validation-driven clients, and self-describing parameters.

**Trade-offs**

It can blur the line between API design and UI design.

---

#### Context Representation

**What it is**

A Context Representation includes surrounding information needed to interpret primary data.

**What it solves**

It prevents ambiguity, such as a price without currency, region, tax rules, or validity period.

**Use cases**

Use it for localization, pricing, tax rules, permissions, regional behavior, time-sensitive data, personalization, and multi-tenant APIs.

**Trade-offs**

Context increases response size, so include only what is necessary for correct interpretation.

---

#### Pagination

**What it is**

Pagination splits large result sets into smaller pages or chunks.

**What it solves**

It prevents huge responses that are slow, expensive, or impractical.

**Use cases**

Use it for lists, search results, audit logs, event streams, transaction histories, product catalogs, and user directories.

**Trade-offs**

Offset pagination is simple but can be inconsistent when data changes. Cursor pagination handles large changing datasets better but is more complex.

---
