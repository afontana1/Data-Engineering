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

API structure is about more than naming fields. It defines how clients pass information to an API, how servers return information, how relationships are represented, and how much context is included so clients can interpret the response correctly.

A good API structure should make the common case easy, the complex case understandable, and the contract stable enough that clients can depend on it.

In practice, API structure decisions answer questions such as:

- Should this input be a simple scalar value or a nested object?
- Should related parameters be grouped?
- Should IDs be opaque?
- Should the response include links?
- Should metadata be mixed with data or separated?
- Should the response include context like currency, locale, permissions, or freshness?
- How should large result sets be paginated?

The central idea is:

> Structure should reveal meaning without exposing unnecessary implementation details.

For example, this response is technically valid:

```json
{
  "id": "ord_123",
  "a": 12999,
  "c": "USD",
  "s": "CONFIRMED"
}
```

But this response is much clearer:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": {
    "amount": 129.99,
    "currency": "USD"
  }
}
```

Both responses carry data. Only the second one carries strong structure and meaning.

---

#### Atomic Parameter

**What it is**

An **Atomic Parameter** is a single indivisible value passed in a request or response.

Examples include:

- `customerId`
- `email`
- `limit`
- `status`
- `currency`
- `createdAfter`
- `includeInactive`
- `sortBy`

Atomic parameters are scalar values. They are not objects, arrays, trees, or collections.

Example query parameters:

```http
GET /orders?customerId=cus_123&status=CONFIRMED&limit=25
```

Example JSON request body:

```json
{
  "customerId": "cus_123",
  "status": "CONFIRMED",
  "limit": 25
}
```

The central idea is:

> Use an atomic parameter when the value is simple, independent, and has one clear meaning.

---

**What it solves**

Atomic parameters provide clarity for simple scalar values.

They make APIs easy to read and easy to call.

For example:

```http
GET /customers?email=alex@example.com
```

This is clearer than wrapping the same simple value in unnecessary structure:

```json
{
  "customerLookupCriteria": {
    "contactIdentity": {
      "emailAddress": {
        "value": "alex@example.com"
      }
    }
  }
}
```

Atomic parameters are useful when the API does not need extra hierarchy.

They keep simple operations simple.

---

**Use cases**

Use Atomic Parameters for:

- identifiers,
- filters,
- flags,
- sorting fields,
- limits,
- dates,
- timestamps,
- status values,
- language codes,
- currency codes,
- region codes,
- booleans,
- simple search terms.

Examples:

```http
GET /products?category=shoes
```

```http
GET /orders?status=PENDING
```

```http
GET /audit-events?createdAfter=2026-04-01T00:00:00Z
```

```http
GET /customers?limit=50
```

---

**Good design practices**

Atomic parameters should be:

- clearly named,
- strongly typed,
- documented,
- validated,
- stable,
- consistent across endpoints.

Good:

```http
GET /orders?createdAfter=2026-04-01T00:00:00Z
```

Less clear:

```http
GET /orders?date=2026-04-01
```

The second example does not explain whether `date` means created date, updated date, delivery date, or payment date.

Prefer names that include domain meaning.

---

**Validation**

Atomic parameters should have explicit validation rules.

Example rules:

| Parameter | Type | Validation |
|---|---|---|
| `limit` | integer | Minimum 1, maximum 100 |
| `status` | string enum | `PENDING`, `CONFIRMED`, `CANCELLED` |
| `createdAfter` | timestamp | ISO 8601 timestamp |
| `currency` | string | 3-letter currency code |
| `includeInactive` | boolean | `true` or `false` |

Example error response:

```json
{
  "error": "INVALID_PARAMETER",
  "message": "limit must be between 1 and 100",
  "parameter": "limit"
}
```

Do not leave scalar values loosely defined.

---

**Trade-offs**

Atomic parameters are simple, but too many atomic parameters can make an API hard to use.

Example:

```http
GET /reports?startDate=2026-04-01&endDate=2026-04-30&region=US&currency=USD&groupBy=day&includeRefunds=true&includeTaxes=false&sortBy=revenue&sortDirection=desc&limit=100
```

This may be acceptable for a moderately complex query, but if the number of parameters keeps growing, related values may need to be grouped.

For example, a request body may be clearer:

```json
{
  "dateRange": {
    "start": "2026-04-01",
    "end": "2026-04-30"
  },
  "filters": {
    "region": "US",
    "currency": "USD"
  },
  "grouping": {
    "field": "day"
  },
  "sorting": {
    "field": "revenue",
    "direction": "desc"
  },
  "limit": 100
}
```

Atomic parameters are best when there are only a few of them and each one is independent.

---

#### Atomic Parameter List

**What it is**

An **Atomic Parameter List** is a list of simple values passed for one purpose.

Examples:

```http
GET /customers?ids=cus_1,cus_2,cus_3
```

```http
GET /products?categories=shoes,jackets,bags
```

```http
GET /orders?statuses=PENDING,CONFIRMED
```

```http
GET /users?fields=id,name,email
```

In JSON, the same idea is usually represented as an array:

```json
{
  "orderIds": ["ord_1", "ord_2", "ord_3"]
}
```

The central idea is:

> Use an atomic parameter list when the client needs to pass multiple scalar values for the same purpose.

---

**What it solves**

Atomic Parameter Lists avoid creating unnecessary objects when a simple list is enough.

For example, this is simple and clear:

```json
{
  "customerIds": ["cus_1", "cus_2", "cus_3"]
}
```

This is unnecessarily complex:

```json
{
  "customerSelection": {
    "selectedCustomers": [
      { "customerIdentifier": { "value": "cus_1" } },
      { "customerIdentifier": { "value": "cus_2" } },
      { "customerIdentifier": { "value": "cus_3" } }
    ]
  }
}
```

Atomic lists are useful for batch retrieval, filtering, field selection, and simple multi-value conditions.

---

**Use cases**

Use Atomic Parameter Lists for:

- filtering by multiple IDs,
- selecting response fields,
- passing multiple statuses,
- passing tags,
- passing categories,
- batch retrieval keys,
- excluding fields,
- specifying sort fields,
- specifying allowed values.

Examples:

```http
GET /orders?ids=ord_123,ord_456,ord_789
```

```http
GET /products?tags=waterproof,trail,running
```

```http
GET /customers?fields=customerId,displayName,email
```

```json
{
  "productIds": ["prod_1", "prod_2", "prod_3"]
}
```

---

**Encoding options**

For query strings, lists need clear encoding rules.

Common formats:

| Format | Example |
|---|---|
| Comma-separated | `ids=1,2,3` |
| Repeated parameters | `ids=1&ids=2&ids=3` |
| Bracket syntax | `ids[]=1&ids[]=2&ids[]=3` |
| JSON body array | `{ "ids": ["1", "2", "3"] }` |

Pick one style and use it consistently.

Comma-separated values are compact, but escaping can be tricky if values may contain commas.

Repeated parameters are explicit, but not every client or framework handles them the same way.

JSON arrays are usually clearest for `POST` batch operations.

---

**Ordering**

Define whether list order matters.

For example, in field selection:

```http
GET /customers?fields=name,email,createdAt
```

Should the response fields appear in that order?

For ID batch retrieval:

```json
{
  "ids": ["prod_3", "prod_1", "prod_2"]
}
```

Should the response preserve request order?

If ordering matters, document it.

Example response preserving order:

```json
{
  "items": [
    { "productId": "prod_3", "name": "Backpack" },
    { "productId": "prod_1", "name": "Jacket" },
    { "productId": "prod_2", "name": "Shoes" }
  ]
}
```

If ordering does not matter, say so.

---

**Duplicate handling**

Define how duplicates are handled.

Request:

```http
GET /products?ids=prod_1,prod_1,prod_2
```

Possible behaviors:

- reject duplicates,
- ignore duplicates,
- preserve duplicates in response,
- return a warning.

Most APIs should either reject duplicates or deduplicate them.

Example error:

```json
{
  "error": "DUPLICATE_VALUES",
  "message": "ids contains duplicate values",
  "parameter": "ids"
}
```

---

**Maximum size**

Every list should have a maximum size.

Bad:

```http
GET /products?ids=100000-values-here
```

Better rule:

```text
ids may contain at most 100 values.
```

Example error:

```json
{
  "error": "TOO_MANY_VALUES",
  "message": "ids may contain at most 100 values",
  "parameter": "ids",
  "maxAllowed": 100
}
```

Maximum sizes protect the API from expensive queries and oversized URLs.

---

**Trade-offs**

Atomic Parameter Lists are simple, but they need clear rules for:

- encoding,
- ordering,
- duplicates,
- maximum size,
- invalid values,
- partial failures,
- missing values,
- response ordering.

For complex list items, do not use Atomic Parameter Lists. Use a structured object or array of objects instead.

For example, this should not be encoded as a comma-separated list:

```text
productId:quantity:warehouseId,productId:quantity:warehouseId
```

Use JSON:

```json
{
  "items": [
    {
      "productId": "prod_123",
      "quantity": 2,
      "warehouseId": "wh_1"
    }
  ]
}
```

---

#### Parameter Tree

**What it is**

A **Parameter Tree** is a nested parameter structure that represents parent-child relationships.

It is useful when flat parameters cannot express the request clearly.

Example:

```json
{
  "filter": {
    "and": [
      {
        "field": "status",
        "operator": "equals",
        "value": "CONFIRMED"
      },
      {
        "field": "totalAmount",
        "operator": "greaterThan",
        "value": 100
      }
    ]
  }
}
```

The central idea is:

> Use a tree when the request has nested structure or hierarchy.

---

**What it solves**

A Parameter Tree supports complex inputs that flat query parameters cannot express cleanly.

For example, this query is hard to express with simple parameters:

```text
Find orders where status is CONFIRMED and either amount is greater than 100 or customer tier is GOLD.
```

A tree can express it:

```json
{
  "filter": {
    "and": [
      {
        "field": "status",
        "operator": "equals",
        "value": "CONFIRMED"
      },
      {
        "or": [
          {
            "field": "totalAmount",
            "operator": "greaterThan",
            "value": 100
          },
          {
            "field": "customerTier",
            "operator": "equals",
            "value": "GOLD"
          }
        ]
      }
    ]
  }
}
```

A tree makes the logical structure explicit.

---

**Use cases**

Use Parameter Trees for:

- nested filters,
- search queries,
- validation rules,
- complex configuration,
- access policies,
- product option trees,
- hierarchical categories,
- workflow rules,
- feature targeting rules,
- pricing rules.

Example access policy:

```json
{
  "policy": {
    "anyOf": [
      {
        "role": "ADMIN"
      },
      {
        "allOf": [
          {
            "permission": "orders:read"
          },
          {
            "tenantId": "tenant_123"
          }
        ]
      }
    ]
  }
}
```

Example product option tree:

```json
{
  "productOptions": {
    "size": {
      "values": ["S", "M", "L"],
      "dependsOn": null
    },
    "color": {
      "values": ["Black", "Blue"],
      "dependsOn": "size"
    }
  }
}
```

---

**GET vs POST for parameter trees**

Simple filters can fit in query strings.

```http
GET /orders?status=CONFIRMED&createdAfter=2026-04-01
```

Complex trees usually belong in a request body.

```http
POST /order-searches
Content-Type: application/json
```

```json
{
  "filter": {
    "and": [
      { "field": "status", "operator": "equals", "value": "CONFIRMED" },
      { "field": "totalAmount", "operator": "greaterThan", "value": 100 }
    ]
  }
}
```

This avoids huge URLs and awkward encoding.

A common design is:

- use `GET` for simple retrieval and simple filters,
- use `POST` to a search or query resource for complex structured queries.

---

**Validation**

Parameter Trees need strong validation.

Validate:

- allowed fields,
- allowed operators,
- value types,
- maximum tree depth,
- maximum number of nodes,
- allowed nesting combinations,
- required fields,
- invalid logical combinations.

Example validation error:

```json
{
  "error": "INVALID_FILTER",
  "message": "Operator greaterThan is not allowed for field status",
  "path": "filter.and[0].operator"
}
```

The `path` is important because nested validation errors can otherwise be hard to locate.

---

**Trade-offs**

Parameter Trees are expressive, but they are harder to:

- validate,
- document,
- test,
- secure,
- cache,
- support in simple clients,
- encode in query strings.

They can also become mini programming languages if not constrained.

For example, a flexible rule tree may invite clients to build extremely expensive queries.

Set limits:

```json
{
  "maxDepth": 5,
  "maxConditions": 50,
  "allowedOperators": ["equals", "in", "greaterThan", "lessThan"]
}
```

Use Parameter Trees when the structure is necessary, not as a default for simple inputs.

---

#### Parameter Forest

**What it is**

A **Parameter Forest** is a collection of multiple parameter trees in one request.

Each tree represents a different structured concern.

Example:

```json
{
  "filter": {
    "and": [
      { "field": "status", "operator": "equals", "value": "CONFIRMED" }
    ]
  },
  "sort": [
    { "field": "createdAt", "direction": "desc" }
  ],
  "pagination": {
    "limit": 50,
    "cursor": "eyJvZmZzZXQiOjUwfQ"
  },
  "output": {
    "fields": ["orderId", "status", "totalAmount"]
  }
}
```

The central idea is:

> Use a Parameter Forest when a request has several independent structured parts.

---

**What it solves**

A Parameter Forest groups multiple structured concerns cleanly.

Instead of flattening everything into one long list of parameters, the request separates concerns:

- filtering,
- sorting,
- pagination,
- grouping,
- output selection,
- aggregations,
- context.

This makes complex requests more understandable.

For example, an analytics query may need filters, metrics, grouping, and time range:

```json
{
  "timeRange": {
    "start": "2026-04-01",
    "end": "2026-04-30"
  },
  "metrics": ["revenue", "orderCount"],
  "groupBy": ["region", "day"],
  "filters": {
    "and": [
      { "field": "currency", "operator": "equals", "value": "USD" },
      { "field": "status", "operator": "equals", "value": "CONFIRMED" }
    ]
  }
}
```

A flat query string would be much harder to understand.

---

**Use cases**

Use Parameter Forests for:

- advanced search,
- complex reports,
- analytics queries,
- batch operations,
- rule engines,
- policy evaluation,
- configurable workflows,
- export jobs,
- recommendation requests,
- dashboard queries.

Example report request:

```json
{
  "report": {
    "type": "REVENUE_BY_REGION"
  },
  "timeRange": {
    "start": "2026-01-01",
    "end": "2026-03-31"
  },
  "filters": {
    "regions": ["US", "EU"],
    "currency": "USD"
  },
  "format": {
    "type": "CSV",
    "includeHeaders": true
  }
}
```

---

**Design principles**

Each tree in the forest should have a clear responsibility.

Good:

```json
{
  "filter": {},
  "sort": [],
  "pagination": {},
  "fields": []
}
```

Less good:

```json
{
  "options": {
    "filterStatus": "CONFIRMED",
    "sortCreatedAt": "desc",
    "pageLimit": 50,
    "includeFields": "orderId,status"
  }
}
```

The second example hides different concerns inside a vague `options` object.

Prefer explicit top-level groups.

---

**Validation**

Parameter Forests need validation at two levels:

1. Validate each tree individually.
2. Validate interactions between trees.

For example:

```json
{
  "groupBy": ["region"],
  "sort": [
    { "field": "customerName", "direction": "asc" }
  ]
}
```

If the query groups by region, sorting by customer name may not make sense.

Example error:

```json
{
  "error": "INVALID_QUERY",
  "message": "Cannot sort by customerName when grouping by region",
  "path": "sort[0].field"
}
```

---

**Trade-offs**

Parameter Forests are powerful, but they can be difficult for clients to construct and servers to validate.

Risks include:

- too much flexibility,
- query planner complexity,
- expensive server-side execution,
- unclear validation errors,
- poor documentation,
- client-side confusion,
- hidden coupling to internal query engines.

Use them when the API really needs complex structured input.

For simpler endpoints, prefer atomic parameters or small objects.

---

#### Data Element

**What it is**

A **Data Element** is a normal business data field in an API representation.

Examples:

- `name`
- `amount`
- `status`
- `createdAt`
- `description`
- `email`
- `quantity`
- `shippingAddress`

Example:

```json
{
  "customerId": "cus_123",
  "displayName": "Alex Morgan",
  "email": "alex@example.com",
  "status": "ACTIVE"
}
```

Here, `displayName`, `email`, and `status` are data elements.

The central idea is:

> Data elements represent the business content of a resource.

---

**What it solves**

Data Elements separate business content from identifiers, links, and metadata.

For example:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": {
    "amount": 129.99,
    "currency": "USD"
  },
  "links": {
    "self": "/orders/ord_123"
  },
  "metadata": {
    "version": 7
  }
}
```

In this response:

- `orderId` is an ID element,
- `status` and `totalAmount` are data elements,
- `links` contains link elements,
- `metadata` contains metadata elements.

This separation helps clients understand what each field is for.

---

**Use cases**

Use Data Elements for:

- customer names,
- order totals,
- product descriptions,
- payment statuses,
- shipping addresses,
- invoice amounts,
- subscription plans,
- support ticket subjects,
- appointment times,
- product attributes,
- account balances.

Example order representation:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "createdAt": "2026-04-29T12:00:00Z",
  "totalAmount": {
    "amount": 129.99,
    "currency": "USD"
  },
  "items": [
    {
      "productId": "prod_456",
      "name": "Trail Running Shoe",
      "quantity": 1,
      "unitPrice": {
        "amount": 129.99,
        "currency": "USD"
      }
    }
  ]
}
```

---

**Field naming**

Data element names should be clear and domain-specific.

Good:

```json
{
  "createdAt": "2026-04-29T12:00:00Z",
  "cancelledAt": "2026-04-30T09:00:00Z"
}
```

Less clear:

```json
{
  "date1": "2026-04-29T12:00:00Z",
  "date2": "2026-04-30T09:00:00Z"
}
```

Good:

```json
{
  "totalAmount": 129.99
}
```

Less clear:

```json
{
  "amount": 129.99
}
```

`amount` may be acceptable when context is obvious, but `totalAmount`, `taxAmount`, `refundAmount`, or `subtotalAmount` is usually safer.

---

**Stability**

Data elements must be stable and clearly defined because changes can break consumers.

Breaking changes include:

- renaming a field,
- removing a field,
- changing a field type,
- changing enum values,
- changing field meaning,
- changing units,
- changing timestamp format.

For example, this is breaking if clients expect dollars:

```json
{
  "totalAmount": 12999
}
```

when it used to mean:

```json
{
  "totalAmount": 129.99
}
```

If you need to change units, introduce a new field:

```json
{
  "totalAmount": 129.99,
  "totalAmountCents": 12999
}
```

Then deprecate carefully.

---

**Trade-offs**

Data elements are the core of representations, so their design has long-term consequences.

Too few fields can force clients to make extra calls.

Too many fields can create bloated responses and accidental dependencies.

A good representation includes the data needed for the resource’s intended use case, while avoiding unrelated internal details.

---

#### Id Element

**What it is**

An **Id Element** uniquely identifies a resource or element.

Examples:

```json
{
  "customerId": "cus_123",
  "orderId": "ord_456",
  "paymentId": "pay_789"
}
```

IDs allow clients and services to refer to resources consistently.

The central idea is:

> IDs provide stable identity across API interactions.

---

**What it solves**

Id Elements give clients a stable way to reference resources.

For example:

```http
GET /orders/ord_123
```

The client can store `ord_123`, pass it to another endpoint, or use it in support workflows.

IDs are also used for:

- foreign references,
- correlation,
- deduplication,
- idempotency,
- linking,
- pagination cursors,
- audit trails,
- event streams.

Example event:

```json
{
  "eventId": "evt_123",
  "eventType": "OrderConfirmed",
  "orderId": "ord_456",
  "correlationId": "corr_789"
}
```

---

**Opaque IDs**

IDs should usually be opaque.

That means clients should not depend on internal meaning inside the ID.

Good:

```json
{
  "orderId": "ord_8f3a9c2"
}
```

Risky:

```json
{
  "orderId": "2026-US-WEST-DB03-000001"
}
```

The second ID exposes implementation details:

- year,
- region,
- database shard,
- sequence number.

If clients start parsing that structure, future changes become difficult.

A safe rule:

> Clients may store and send IDs back, but they should not interpret their internal structure.

---

**Stable IDs**

IDs should be stable for the lifetime of the resource.

Bad:

```text
Customer ID changes when customer email changes.
```

Good:

```text
Customer ID remains the same even if email changes.
```

Do not use mutable business attributes as primary identifiers unless the domain guarantees immutability.

For example, email addresses are usually not good customer IDs because users can change email addresses.

---

**ID naming**

Prefer explicit ID names.

Good:

```json
{
  "customerId": "cus_123",
  "billingAccountId": "acct_456"
}
```

Potentially unclear:

```json
{
  "id": "cus_123",
  "accountId": "acct_456"
}
```

Inside a resource, `id` can be acceptable:

```json
{
  "id": "cus_123",
  "displayName": "Alex Morgan"
}
```

But in nested or composite representations, explicit names are often clearer:

```json
{
  "customerId": "cus_123",
  "orderId": "ord_456"
}
```

---

**Idempotency IDs**

IDs can also support idempotency.

Example:

```http
POST /orders
Idempotency-Key: create-order-req-123
```

The idempotency key is not the order ID. It identifies the client’s request attempt so duplicate submissions can be handled safely.

Example response:

```json
{
  "orderId": "ord_123",
  "idempotencyKey": "create-order-req-123"
}
```

---

**Trade-offs**

IDs should be stable, opaque, and not expose sensitive implementation details.

Avoid IDs that reveal:

- database sequence size,
- shard location,
- tenant count,
- user count,
- internal system topology,
- sensitive business information.

Also avoid changing ID formats casually. Even if IDs are documented as opaque, clients may still store, log, or validate them.

---

#### Link Element

**What it is**

A **Link Element** provides a URI or reference to another resource or action.

Example:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "links": {
    "self": "/orders/ord_123",
    "customer": "/customers/cus_456",
    "items": "/orders/ord_123/items"
  }
}
```

The central idea is:

> Links help clients navigate related resources and available actions without hardcoding every URI.

---

**What it solves**

Link Elements improve discoverability and reduce hardcoded client navigation.

Instead of requiring the client to construct every URL, the API can return relevant links.

For example:

```json
{
  "ticketId": "ticket_123",
  "status": "OPEN",
  "links": {
    "self": "/support-tickets/ticket_123",
    "close": "/support-tickets/ticket_123/closure",
    "assign": "/support-tickets/ticket_123/assignment"
  }
}
```

The client can see which operations are available for this resource.

If the ticket is already closed, the `close` link may be omitted.

---

**Use cases**

Use Link Elements for:

- self links,
- related resources,
- available actions,
- pagination links,
- download links,
- upload links,
- state-dependent operations,
- next workflow steps,
- documentation links,
- external references.

Example pagination links:

```json
{
  "items": [],
  "links": {
    "self": "/orders?limit=50&cursor=abc",
    "next": "/orders?limit=50&cursor=def",
    "previous": "/orders?limit=50&cursor=xyz"
  }
}
```

Example download link:

```json
{
  "reportId": "report_123",
  "status": "COMPLETED",
  "links": {
    "download": "/reports/report_123/download"
  }
}
```

---

**Action links**

Links can represent available actions.

Example order response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "links": {
    "self": "/orders/ord_123",
    "cancel": "/orders/ord_123/cancellation",
    "payment": "/payments/pay_456"
  }
}
```

If the order is shipped, cancellation may no longer be available:

```json
{
  "orderId": "ord_123",
  "status": "SHIPPED",
  "links": {
    "self": "/orders/ord_123",
    "shipment": "/shipments/shp_789"
  }
}
```

This helps clients avoid presenting invalid actions.

However, the server must still enforce business rules. Links are helpful hints, not security guarantees.

---

**Link object format**

Simple links can be strings:

```json
{
  "links": {
    "self": "/orders/ord_123"
  }
}
```

Richer links can include metadata:

```json
{
  "links": {
    "cancel": {
      "href": "/orders/ord_123/cancellation",
      "method": "POST",
      "title": "Cancel order"
    }
  }
}
```

Use richer links when clients need more information about how to use the link.

---

**Trade-offs**

Hypermedia-style APIs require client support and discipline.

Trade-offs include:

- larger responses,
- more response design work,
- more client logic,
- more consistency requirements,
- possible mismatch with simple generated clients.

Links are most valuable when relationships or actions are dynamic.

If every client already knows a stable URI pattern and the relationship is obvious, links may add less value.

---

#### Metadata Element

**What it is**

A **Metadata Element** describes a representation or resource but is not the main business data.

Examples:

- `version`
- `etag`
- `lastUpdatedAt`
- `source`
- `locale`
- `confidence`
- `processingStatus`
- `syncToken`
- `generatedAt`
- `projectionLagMs`

Example:

```json
{
  "data": {
    "orderId": "ord_123",
    "status": "CONFIRMED"
  },
  "metadata": {
    "version": 7,
    "lastUpdatedAt": "2026-04-29T12:00:00Z",
    "source": "order-service"
  }
}
```

The central idea is:

> Metadata helps clients interpret, cache, synchronize, or trust the data.

---

**What it solves**

Metadata gives clients context about the representation.

For example, this data is incomplete without knowing freshness:

```json
{
  "inventoryStatus": "IN_STOCK"
}
```

A better response may include metadata:

```json
{
  "inventoryStatus": "IN_STOCK",
  "metadata": {
    "lastUpdatedAt": "2026-04-29T12:00:00Z",
    "projectionLagMs": 500
  }
}
```

Now the client knows how fresh the status is.

---

**Use cases**

Use Metadata Elements for:

- audit fields,
- ETags,
- versions,
- synchronization markers,
- locale,
- source,
- confidence,
- processing status,
- freshness,
- pagination state,
- projection lag,
- deprecation notices,
- schema version,
- generated timestamps.

Example:

```json
{
  "customerId": "cus_123",
  "displayName": "Alex Morgan",
  "metadata": {
    "schemaVersion": 2,
    "lastUpdatedAt": "2026-04-29T12:00:00Z",
    "etag": "W/\"customer-7\""
  }
}
```

---

**Metadata vs data**

Do not hide business data in metadata.

Bad:

```json
{
  "customerId": "cus_123",
  "metadata": {
    "subscriptionPlan": "ENTERPRISE"
  }
}
```

If `subscriptionPlan` is business data that clients rely on, it should be a data element:

```json
{
  "customerId": "cus_123",
  "subscriptionPlan": "ENTERPRISE",
  "metadata": {
    "lastUpdatedAt": "2026-04-29T12:00:00Z"
  }
}
```

Metadata should describe data, not smuggle important business content into a vague container.

---

**Freshness metadata**

Freshness metadata is especially useful for read models, caches, and derived data.

Example:

```json
{
  "orderId": "ord_123",
  "paymentStatus": "AUTHORIZED",
  "shipmentStatus": "PENDING",
  "metadata": {
    "generatedAt": "2026-04-29T12:00:03Z",
    "sourceEventsThrough": "2026-04-29T12:00:02Z",
    "projectionLagMs": 750
  }
}
```

This helps clients and operators understand whether stale data may be involved.

---

**Trade-offs**

Metadata should not become a dumping ground for unclear fields.

If a field is important to business behavior, name it clearly and place it in the main representation.

Too much metadata can make responses noisy.

Include metadata when it helps clients:

- cache,
- synchronize,
- debug,
- interpret,
- localize,
- understand freshness,
- evaluate confidence.

Do not include metadata only because it is available internally.

---

#### Annotated Parameter Collection

**What it is**

An **Annotated Parameter Collection** groups parameters with descriptive metadata such as labels, required flags, validation rules, allowed values, or display hints.

Example:

```json
{
  "parameters": [
    {
      "name": "startDate",
      "type": "date",
      "label": "Start date",
      "required": true
    },
    {
      "name": "region",
      "type": "string",
      "label": "Region",
      "required": false,
      "allowedValues": ["US", "EU", "APAC"]
    }
  ]
}
```

The central idea is:

> Parameters can be described in a way that helps clients dynamically render, validate, or interpret them.

---

**What it solves**

Annotated Parameter Collections help clients understand how to use parameters without hardcoding every rule.

This is useful when the API drives dynamic behavior.

For example, a report API may expose the parameters required for a report type:

```http
GET /report-types/revenue-summary/parameters
```

Response:

```json
{
  "reportType": "revenue-summary",
  "parameters": [
    {
      "name": "dateRange",
      "type": "dateRange",
      "required": true,
      "label": "Date range"
    },
    {
      "name": "currency",
      "type": "enum",
      "required": true,
      "allowedValues": ["USD", "EUR", "GBP"]
    }
  ]
}
```

A client can use this to render a form or validate input.

---

**Use cases**

Use Annotated Parameter Collections for:

- dynamic forms,
- API-driven UI,
- configurable workflows,
- validation-driven clients,
- self-describing parameters,
- report builders,
- rule editors,
- admin tools,
- integration setup forms,
- workflow configuration.

Example dynamic integration configuration:

```json
{
  "integrationType": "webhook",
  "parameters": [
    {
      "name": "callbackUrl",
      "type": "url",
      "required": true,
      "label": "Callback URL"
    },
    {
      "name": "events",
      "type": "stringList",
      "required": true,
      "allowedValues": ["OrderCreated", "PaymentFailed", "RefundIssued"]
    }
  ]
}
```

---

**Validation hints**

Annotations can include validation rules.

```json
{
  "name": "quantity",
  "type": "integer",
  "required": true,
  "minimum": 1,
  "maximum": 100,
  "label": "Quantity"
}
```

They can also include patterns:

```json
{
  "name": "email",
  "type": "string",
  "format": "email",
  "required": true
}
```

The server must still validate. Client-side validation is convenience, not trust.

---

**Display hints**

Annotated parameters may include display hints:

```json
{
  "name": "deliverySpeed",
  "type": "enum",
  "label": "Delivery speed",
  "control": "radio",
  "allowedValues": [
    {
      "value": "STANDARD",
      "label": "Standard"
    },
    {
      "value": "EXPRESS",
      "label": "Express"
    }
  ]
}
```

This is useful for internal tools and dynamic UI.

Be careful, though: too much UI-specific detail can make the API responsible for presentation logic.

---

**Trade-offs**

Annotated Parameter Collections can blur the line between API design and UI design.

They are powerful when clients are dynamic, but they add complexity.

Risks include:

- API becomes tightly coupled to UI rendering,
- annotations become inconsistent,
- clients interpret hints differently,
- validation rules drift from server rules,
- response becomes large and complex,
- business logic leaks into metadata.

Use this pattern when dynamic behavior is a real requirement.

For fixed, hand-coded clients, normal documentation and schema definitions may be enough.

---

#### Context Representation

**What it is**

A **Context Representation** includes surrounding information needed to interpret primary data correctly.

Example:

```json
{
  "price": {
    "amount": 129.99,
    "currency": "USD",
    "taxIncluded": false,
    "validUntil": "2026-04-29T13:00:00Z"
  }
}
```

The amount alone is not enough. The client also needs currency, tax treatment, and validity period.

The central idea is:

> Include the context required for correct interpretation.

---

**What it solves**

Context Representation prevents ambiguity.

For example, this is ambiguous:

```json
{
  "price": 129.99
}
```

Questions:

- Which currency?
- Is tax included?
- Is this price valid now?
- Is it personalized?
- Is it regional?
- Is it discounted?

Better:

```json
{
  "price": {
    "amount": 129.99,
    "currency": "USD",
    "taxIncluded": false,
    "region": "US",
    "validUntil": "2026-04-29T13:00:00Z"
  }
}
```

Now the client can interpret the value correctly.

---

**Use cases**

Use Context Representation for:

- localization,
- pricing,
- tax rules,
- permissions,
- regional behavior,
- time-sensitive data,
- personalization,
- multi-tenant APIs,
- legal terms,
- inventory availability,
- feature availability,
- confidence scores,
- measurement units.

Example localized content:

```json
{
  "title": "Trail Running Shoe",
  "context": {
    "locale": "en-US",
    "region": "US"
  }
}
```

Example permission context:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "actions": {
    "canCancel": true,
    "canRefund": false
  },
  "context": {
    "evaluatedForUserId": "user_456",
    "evaluatedAt": "2026-04-29T12:00:00Z"
  }
}
```

---

**Units and measurements**

Never return measurements without units if ambiguity is possible.

Ambiguous:

```json
{
  "weight": 10
}
```

Clear:

```json
{
  "weight": {
    "value": 10,
    "unit": "kg"
  }
}
```

Ambiguous:

```json
{
  "distance": 5
}
```

Clear:

```json
{
  "distance": {
    "value": 5,
    "unit": "km"
  }
}
```

Context prevents wrong assumptions.

---

**Multi-tenant context**

In multi-tenant APIs, context can clarify tenant-specific interpretation.

```json
{
  "feature": "advanced-reporting",
  "enabled": true,
  "context": {
    "tenantId": "tenant_123",
    "plan": "ENTERPRISE",
    "evaluatedAt": "2026-04-29T12:00:00Z"
  }
}
```

This helps clients and operators understand why a value was returned.

---

**Trade-offs**

Context increases response size.

Do not include every possible piece of context. Include what is necessary for correct interpretation.

For example, a simple internal API may not need full regional tax context in every response.

But a pricing API almost certainly does.

A good rule:

> Include context when a reasonable client could otherwise misinterpret the data.

---

#### Pagination

**What it is**

**Pagination** splits large result sets into smaller pages or chunks.

Instead of returning every item at once, the API returns a limited number and gives the client a way to request more.

Example:

```http
GET /orders?limit=50
```

Response:

```json
{
  "items": [
    { "orderId": "ord_1" },
    { "orderId": "ord_2" }
  ],
  "pagination": {
    "limit": 50,
    "nextCursor": "eyJjcmVhdGVkQXQiOiIyMDI2LTA0LTI5In0"
  }
}
```

The central idea is:

> Large collections should be retrieved incrementally, not all at once.

---

**What it solves**

Pagination prevents huge responses that are slow, expensive, or impractical.

Without pagination:

```http
GET /audit-events
```

The API might try to return millions of records.

That can cause:

- slow responses,
- high memory usage,
- network overhead,
- timeouts,
- database load,
- poor client performance.

With pagination:

```http
GET /audit-events?limit=100&cursor=abc
```

The API returns manageable chunks.

---

**Use cases**

Use Pagination for:

- lists,
- search results,
- audit logs,
- event streams,
- transaction histories,
- product catalogs,
- user directories,
- support tickets,
- reports,
- notification feeds,
- admin tables.

Any endpoint that can return many items should have a pagination strategy.

---

**Offset pagination**

Offset pagination uses `limit` and `offset`.

Example:

```http
GET /orders?limit=50&offset=100
```

This means:

```text
Skip the first 100 records and return the next 50.
```

Benefits:

- simple,
- easy to understand,
- works well for small stable datasets,
- easy for page numbers.

Example response:

```json
{
  "items": [],
  "pagination": {
    "limit": 50,
    "offset": 100,
    "totalCount": 1234
  }
}
```

Trade-offs:

- can be slow for large offsets,
- can produce duplicates or missing items when data changes,
- total counts can be expensive,
- less suitable for live feeds.

Example problem:

1. Client requests page 1.
2. New items are inserted.
3. Client requests page 2.
4. Some items may appear twice or be skipped.

---

**Cursor pagination**

Cursor pagination uses an opaque cursor that points to the next position.

Example:

```http
GET /orders?limit=50&cursor=eyJjcmVhdGVkQXQiOiIyMDI2LTA0LTI5VDEyOjAwOjAwWiJ9
```

Response:

```json
{
  "items": [],
  "pagination": {
    "limit": 50,
    "nextCursor": "eyJjcmVhdGVkQXQiOiIyMDI2LTA0LTI5VDExOjU5OjAwWiJ9",
    "hasMore": true
  }
}
```

Benefits:

- better for large datasets,
- better for changing datasets,
- avoids large offset scans,
- works well with stable sort keys.

Trade-offs:

- more complex,
- harder to jump to arbitrary pages,
- cursors must be treated as opaque,
- requires stable ordering.

---

**Cursor design**

A cursor should usually be opaque to clients.

Bad:

```http
GET /orders?cursor=createdAt:2026-04-29T12:00:00Z,id:ord_123
```

Better:

```http
GET /orders?cursor=eyJjcmVhdGVkQXQiOiIyMDI2LTA0LTI5VDEyOjAwOjAwWiIsImlkIjoib3JkXzEyMyJ9
```

The server may encode state inside the cursor, but clients should not depend on the format.

A cursor may contain:

```json
{
  "createdAt": "2026-04-29T12:00:00Z",
  "orderId": "ord_123",
  "sortDirection": "desc"
}
```

The API should document that the cursor is opaque.

---

**Stable sorting**

Pagination requires stable ordering.

Bad:

```http
GET /orders?sortBy=status
```

If many orders have the same status, the order may shift between requests.

Better:

```http
GET /orders?sortBy=createdAt&direction=desc
```

Even better, use a tie-breaker:

```text
ORDER BY created_at DESC, order_id DESC
```

This ensures consistent ordering when multiple records have the same timestamp.

---

**Page size**

APIs should enforce page size limits.

Example:

```http
GET /orders?limit=1000
```

If the maximum allowed page size is 100, return:

```json
{
  "error": "INVALID_LIMIT",
  "message": "limit must be between 1 and 100",
  "maxAllowed": 100
}
```

Recommended behavior:

- define default limit,
- define maximum limit,
- reject invalid values,
- document limits.

Example:

```text
Default limit: 50
Maximum limit: 100
```

---

**Pagination metadata**

Responses should include enough pagination metadata.

Cursor pagination example:

```json
{
  "items": [],
  "pagination": {
    "limit": 50,
    "nextCursor": "abc",
    "hasMore": true
  }
}
```

Offset pagination example:

```json
{
  "items": [],
  "pagination": {
    "limit": 50,
    "offset": 100,
    "totalCount": 1234
  }
}
```

Include `totalCount` only when it is cheap and meaningful. In large or changing datasets, exact counts may be expensive or misleading.

---

**Pagination links**

Pagination can include links:

```json
{
  "items": [],
  "links": {
    "self": "/orders?limit=50&cursor=abc",
    "next": "/orders?limit=50&cursor=def"
  }
}
```

Links reduce client URL construction and can make navigation easier.

---

**Trade-offs**

Offset pagination is simple but can be inconsistent when data changes.

Cursor pagination handles large changing datasets better but is more complex.

Choose based on the data:

| Dataset type | Better option |
|---|---|
| Small stable admin list | Offset pagination |
| Large transaction history | Cursor pagination |
| Live activity feed | Cursor pagination |
| Search results | Cursor or search-engine pagination |
| Audit events | Cursor pagination |
| Reports with fixed result sets | Offset or generated file |

A good pagination design protects the server and gives clients predictable navigation.

---

#### Summary

API structure patterns define how requests and responses are shaped.

The central idea is:

> Good structure makes API contracts easier to understand, validate, evolve, and consume.

Use:

- **Atomic Parameters** for simple scalar values.
- **Atomic Parameter Lists** for lists of simple values.
- **Parameter Trees** for nested logic or hierarchy.
- **Parameter Forests** for complex requests with multiple structured concerns.
- **Data Elements** for business data.
- **Id Elements** for stable resource identity.
- **Link Elements** for navigation and available actions.
- **Metadata Elements** for context about representation, freshness, versioning, and interpretation.
- **Annotated Parameter Collections** for dynamic forms, validation, and self-describing parameters.
- **Context Representations** when data needs surrounding information to be interpreted correctly.
- **Pagination** whenever result sets can become large.

The best API structures are explicit without being verbose, flexible without becoming vague, and stable without freezing unnecessary implementation details.
