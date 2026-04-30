# Microservice and API Pattern Master List

# Table of Contents

## 1. Service Boundary and Decomposition Patterns
- [1. Decompose by Business Capability](#1-decompose-by-business-capability)
- [2. Decompose by Subdomain](#2-decompose-by-subdomain)
- [3. Decompose by Transaction or Workflow Boundary](#3-decompose-by-transaction-or-workflow-boundary)
- [4. Stateless Services](#4-stateless-services)

## 2. Legacy Migration and Boundary Protection Patterns
- [5. Strangler Fig Pattern](#5-strangler-fig-pattern)
- [6. Anti-Corruption Layer](#6-anti-corruption-layer)

## 3. Client Access, API Edge, and Composition Patterns
- [7. API Gateway](#7-api-gateway)
- [8. Gateway Routing](#8-gateway-routing)
- [9. Gateway Aggregation / Aggregator Pattern](#9-gateway-aggregation--aggregator-pattern)
- [10. Gateway Offloading](#10-gateway-offloading)
- [11. Backends for Frontends](#11-backends-for-frontends)
- [12. Proxy Pattern](#12-proxy-pattern)
- [13. Client-Side UI Composition / Micro Frontend Composition](#13-client-side-ui-composition--micro-frontend-composition)

## 4. Service Communication and Workflow Patterns
- [14. Smart Endpoints, Dumb Pipes](#14-smart-endpoints-dumb-pipes)
- [15. Chained Microservice Pattern](#15-chained-microservice-pattern)
- [16. Branch Pattern](#16-branch-pattern)
- [17. Async Messaging](#17-async-messaging)
- [18. Choreography](#18-choreography)
- [19. Saga Pattern](#19-saga-pattern)
- [20. Consumer-Driven Contracts](#20-consumer-driven-contracts)

## 5. Data Ownership, Persistence, and Consistency Patterns
- [21. Database per Service](#21-database-per-service)
- [22. Shared Database](#22-shared-database)
- [23. CQRS](#23-cqrs)
- [24. Event Sourcing](#24-event-sourcing)
- [25. Polyglot Persistence](#25-polyglot-persistence)
- [26. Data Sharding](#26-data-sharding)

## 6. Resilience and Failure Isolation Patterns
- [27. Circuit Breaker](#27-circuit-breaker)
- [28. Retry](#28-retry)
- [29. Bulkhead](#29-bulkhead)
- [30. Health Check](#30-health-check)

## 7. Service Discovery, Configuration, and Runtime Infrastructure Patterns
- [31. Service Discovery / Service Registry](#31-service-discovery--service-registry)
- [32. External Configuration](#32-external-configuration)
- [33. Sidecar](#33-sidecar)

## 8. Observability Patterns
- [34. Log Aggregation](#34-log-aggregation)
- [35. Performance Metrics](#35-performance-metrics)
- [36. Distributed Tracing](#36-distributed-tracing)

## 9. Deployment, Release, and Production Validation Patterns
- [37. Blue-Green Deployment](#37-blue-green-deployment)
- [38. Shadow Deployment](#38-shadow-deployment)

## 10. API Design Patterns
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
- [Evolution](#evolution)
  - [Version Identifier](#version-identifier)
  - [Semantic Versioning](#semantic-versioning)
  - [Two In Production](#two-in-production)
  - [Aggressive Obsolescence](#aggressive-obsolescence)
  - [Experimental Preview](#experimental-preview)
  - [Limited Lifetime Guarantee](#limited-lifetime-guarantee)
  - [Eternal Lifetime Guarantee](#eternal-lifetime-guarantee)

---

## 1. Service Boundary and Decomposition Patterns

These patterns define what services should exist and what each service should own.

### 1. Decompose by Business Capability

#### What it is

**Decompose by Business Capability** means splitting a system around the major things the business does, rather than around technical layers.

A **business capability** is a stable business function that helps the organization deliver value. Examples include order management, payments, billing, shipping, inventory, identity, catalog management, customer support, search, fraud detection, claims processing, or subscription management.

The core idea is:

> A service should own a meaningful business function end to end.

That means a service owns the API, business rules, data, and operational behavior for that capability.

For example, an e-commerce system should not be split like this:


```mermaid
flowchart TD
    subgraph App["Layered Application"]
        UI["UI Layer"]
        API["API Layer"]
        Business["Business Logic Layer"]
        Data["Data Access Layer"]
    end

    DB[("Shared Database")]

    UI --> API
    API --> Business
    Business --> Data
    Data --> DB
```

That structure may work inside a monolith, but it is usually a poor way to split microservices. It groups code by technical responsibility rather than by business meaning.

Instead, you aim for a structure like this:

```mermaid
flowchart TD
    Client[Client Applications]
    Gateway[API Gateway]

    Client --> Gateway

    subgraph Services[Business Capability Services]
        Orders[Order Service]
        Payments[Payment Service]
        Inventory[Inventory Service]
        Shipping[Shipping Service]
    end

    subgraph Databases[Service-Owned Databases]
        OrdersDB[(Orders DB)]
        PaymentsDB[(Payments DB)]
        InventoryDB[(Inventory DB)]
        ShippingDB[(Shipping DB)]
    end

    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Inventory
    Gateway --> Shipping

    Orders --> OrdersDB
    Payments --> PaymentsDB
    Inventory --> InventoryDB
    Shipping --> ShippingDB
```

Each service represents a business capability:

| Service           | Business capability it owns                                          |
| ----------------- | -------------------------------------------------------------------- |
| Order Service     | Creating, updating, cancelling, and tracking orders                  |
| Payment Service   | Authorizing, capturing, refunding, and reconciling payments          |
| Inventory Service | Tracking stock, reserving inventory, and managing availability       |
| Shipping Service  | Creating shipments, tracking delivery, and integrating with carriers |

A capability-based service is not just a technical wrapper around a database table. It should own real business behavior.

For example, an **Order Service** might own:

* order creation,
* order cancellation rules,
* order status transitions,
* order history,
* order totals,
* order confirmation,
* order-related events.

It should not own:

* credit card authorization,
* warehouse stock adjustment,
* shipment label generation,
* customer identity verification.

Those belong to other capabilities.

---

#### Why this pattern exists

Many systems start as layered monoliths. A single application contains controllers, business logic, data access code, and database tables.

That is not automatically bad. A layered structure can be simple and productive when the system is small or when one team owns the whole application.

The problem appears when teams try to turn technical layers into separate services.

For example:

```mermaid
flowchart TD
    Client[Client]
    Web[Web Service]
    Logic[Business Logic Service]
    Data[Data Service]
    DB[(Database)]

    Client --> Web
    Web --> Logic
    Logic --> Data
    Data --> DB
```

This may look like microservices, but it usually behaves like a distributed monolith. The services are separated by the network, but they are still tightly coupled.

A request to create an order might look like this:

```mermaid
sequenceDiagram
    participant Client
    participant Web as Web Service
    participant Logic as Business Logic Service
    participant Data as Data Service
    participant DB as Database

    Client->>Web: POST /orders
    Web->>Logic: Validate and create order
    Logic->>Data: Persist order
    Data->>DB: INSERT order
    DB-->>Data: Success
    Data-->>Logic: Success
    Logic-->>Web: Success
    Web-->>Client: 201 Created
```

This design has many problems:

* The services usually cannot be deployed independently.
* A business change often requires changes across several services.
* Every request crosses multiple network boundaries.
* The system gains latency without gaining autonomy.
* The business rules are not owned by a clear business capability.
* The database often remains a shared coupling point.

Decomposing by business capability avoids this by grouping together the things that naturally change together.

---

#### What it solves

This pattern solves **layer-based coupling**.

In a layered architecture, a single business feature often touches many technical layers.

For example, suppose the business wants to allow customers to cancel an order.

```mermaid
flowchart TD
    Feature[Feature: Cancel an Order]

    Feature --> UI[Update UI]
    Feature --> API[Update API]
    Feature --> Rules[Update Business Rules]
    Feature --> DB[Update Data Model]
    Feature --> Notifications[Update Notifications]
    Feature --> Reporting[Update Reporting]
```

The work is spread across technical areas. If different teams own those layers, the feature requires coordination across all of them.

With a capability-based design, most of the change should belong to the service that owns the capability.

```mermaid
flowchart TD
    Feature[Feature: Cancel an Order]
    Orders[Order Service]

    Feature --> Orders

    subgraph OrderService[Inside Order Service]
        API[Order API]
        Rules[Order State Rules]
        DB[(Order Data)]
        Events[Publish OrderCancelled Event]
    end

    Orders --> API
    Orders --> Rules
    Orders --> DB
    Orders --> Events
```

Other services may still need to react, but they react through APIs or events rather than by sharing the same code and database.

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Orders -->|OrderCancelled| Bus

    Bus --> Payments[Payment Service]
    Bus --> Inventory[Inventory Service]
    Bus --> Notifications[Notification Service]
```

For example:

* Payment Service may issue a refund.
* Inventory Service may release reserved stock.
* Notification Service may send the customer a cancellation email.

The Order Service owns the fact that the order was cancelled. Other services own their own reactions to that fact.

---

#### Example: e-commerce capability map

A useful way to start is by building a **capability map**.

A capability map describes what the business does without immediately deciding what the services are.

For an e-commerce platform, the capability map might look like this:

```mermaid
flowchart TD
    Platform[E-commerce Platform]

    Platform --> Sell[Sell Products]
    Platform --> Fulfill[Fulfill Orders]
    Platform --> Money[Collect Money]
    Platform --> Support[Support Customers]

    Sell --> Catalog[Catalog]
    Sell --> Search[Search]
    Sell --> Pricing[Pricing]
    Sell --> Recommendations[Recommendations]

    Fulfill --> Orders[Order Management]
    Fulfill --> Inventory[Inventory]
    Fulfill --> Shipping[Shipping]
    Fulfill --> Returns[Returns]

    Money --> Payments[Payments]
    Money --> Billing[Billing]
    Money --> Refunds[Refunds]
    Money --> Tax[Tax]

    Support --> Customers[Customer Profile]
    Support --> Notifications[Notifications]
    Support --> Helpdesk[Customer Support]
    Support --> Loyalty[Loyalty]
```

This map is not the final architecture. It is a discovery tool.

Some capabilities may become separate services. Others may stay as modules inside a larger service. Some may be merged because they are small. Some may be split because they are complex.

For example:

| Capability    | Possible design decision                                               |
| ------------- | ---------------------------------------------------------------------- |
| Catalog       | Separate service because product data changes often and is widely used |
| Search        | Separate service because it has different scaling and indexing needs   |
| Pricing       | Separate service if pricing rules are complex                          |
| Tax           | Separate service or external provider integration                      |
| Returns       | Separate service if return workflows are complex                       |
| Notifications | Separate service because many other services need to send messages     |

The point is not to create a service for every box in the capability map. The point is to understand the business shape before choosing service boundaries.

---

#### How to identify business capabilities

A business capability is usually discovered by talking to domain experts, product managers, operations teams, support teams, and engineers.

Good questions include:

1. **What does the business actually do?**
   For example: sell products, collect money, ship packages, approve claims, manage subscriptions, detect fraud.

2. **Which parts of the system use different business language?**
   The warehouse team may talk about stock, reservations, bins, picks, packs, and replenishment. The finance team may talk about authorization, capture, settlement, refunds, and chargebacks.

3. **Which things change for different reasons?**
   Payment rules may change because of compliance. Catalog rules may change because of merchandising. Shipping rules may change because of carrier contracts.

4. **Which areas need different scaling characteristics?**
   Search may need to handle many read requests. Payments may need lower volume but stronger reliability and auditability.

5. **Which areas require different compliance or security controls?**
   Payment processing may have PCI concerns. Healthcare records may have privacy controls. Identity may have stricter access requirements.

6. **Which data has a natural owner?**
   Order data should be owned by the Order capability. Payment transaction data should be owned by the Payment capability. Inventory availability should be owned by the Inventory capability.

7. **Which teams can own these capabilities long term?**
   A microservice boundary is also an ownership boundary. If no team can own it, it may not be a good service boundary yet.

---

A common technique is to start with a business capability map:

```mermaid
mindmap
  root((Online Retail))
    Sell Products
      Catalog
      Search
      Recommendations
      Pricing
    Fulfill Orders
      Order Management
      Inventory
      Shipping
      Returns
    Collect Money
      Payments
      Billing
      Refunds
      Tax
    Support Customers
      Customer Profile
      Notifications
      Customer Support
      Loyalty
```

#### Capability size: not too large, not too small

The hardest part of this pattern is choosing the right size.

If the service is too broad, it becomes a mini-monolith.

```mermaid
flowchart TD
    Commerce[Commerce Service]

    Commerce --> Catalog[Catalog]
    Commerce --> Cart[Cart]
    Commerce --> Orders[Orders]
    Commerce --> Payments[Payments]
    Commerce --> Inventory[Inventory]
    Commerce --> Shipping[Shipping]
    Commerce --> Returns[Returns]
```

This may be acceptable early on, especially in a modular monolith or small system. But as a microservice, it can become a problem because too many unrelated changes happen in one deployable unit.

Symptoms of a service that is too large:

* many teams need to change it,
* it contains unrelated business rules,
* deployments are risky,
* the codebase has unclear ownership,
* changes in one area often break another area,
* the service is hard to describe in one sentence.

If the service is too narrow, the system becomes over-fragmented.

```mermaid
flowchart TD
    Client[Client]
    OrderAPI[Order API Service]
    Validation[Order Validation Service]
    Pricing[Order Pricing Service]
    Persistence[Order Persistence Service]
    Status[Order Status Service]
    DB[(Orders DB)]

    Client --> OrderAPI
    OrderAPI --> Validation
    Validation --> Pricing
    Pricing --> Persistence
    Persistence --> Status
    Status --> DB
```

This creates a different set of problems:

* too many network calls,
* too many deployments,
* too much operational overhead,
* difficult local development,
* unclear ownership,
* fragile request chains,
* excessive synchronous communication.

A useful rule of thumb is:

> A service should be small enough to be owned independently, but large enough to make a meaningful business decision.

`Payment Service` is usually a reasonable capability.
`CreditCardFormatValidationService` is usually too small.
`EntireCommercePlatformService` is usually too large.

---

#### Example: Order Service boundary

A well-scoped Order Service should own the order lifecycle.

```mermaid
flowchart TD
    Client[Client]

    subgraph OrderService[Order Service]
        API[Order API]
        Domain[Order Domain Logic]
        Workflow[Order Workflow]
        Repository[Order Repository]
        Events[Event Publisher]
        DB[(Orders Database)]
    end

    Client --> API
    API --> Domain
    Domain --> Workflow
    Workflow --> Repository
    Repository --> DB
    Workflow --> Events
```

The Order Service may expose endpoints such as:

```http
POST /orders
GET /orders/{orderId}
POST /orders/{orderId}/confirm
POST /orders/{orderId}/cancel
GET /customers/{customerId}/orders
```

It may publish events such as:

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt_87321",
  "occurredAt": "2026-04-29T18:25:43Z",
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456",
    "totalAmount": 129.99,
    "currency": "USD"
  }
}
```

It may consume events from other services:

```json
{
  "eventType": "PaymentAuthorized",
  "eventId": "evt_88410",
  "occurredAt": "2026-04-29T18:26:11Z",
  "data": {
    "orderId": "ord_123",
    "paymentId": "pay_789",
    "authorizedAmount": 129.99
  }
}
```

The Order Service owns order state, but it does not own the internal details of payments, inventory, or shipping.

---

#### Example implementation

Here is a simplified Order Service in TypeScript using Express.

```ts
import express, { Request, Response } from "express";
import crypto from "crypto";

const app = express();
app.use(express.json());

type OrderStatus =
  | "PENDING_PAYMENT"
  | "CONFIRMED"
  | "CANCELLED"
  | "SHIPPED";

type OrderItem = {
  productId: string;
  quantity: number;
  unitPrice: number;
};

type Order = {
  id: string;
  customerId: string;
  items: OrderItem[];
  totalAmount: number;
  status: OrderStatus;
  createdAt: string;
};

const orders = new Map<string, Order>();

function calculateTotal(items: OrderItem[]): number {
  return items.reduce(
    (total, item) => total + item.quantity * item.unitPrice,
    0
  );
}

function publishEvent(eventType: string, data: Record<string, unknown>): void {
  // In a real system, this would publish to Kafka, RabbitMQ, SNS/SQS,
  // NATS, Google Pub/Sub, Azure Service Bus, or another broker.
  console.log(JSON.stringify({
    eventType,
    eventId: `evt_${crypto.randomUUID()}`,
    occurredAt: new Date().toISOString(),
    data
  }));
}

function createOrder(customerId: string, items: OrderItem[]): Order {
  if (!customerId) {
    throw new Error("customerId is required");
  }

  if (!items || items.length === 0) {
    throw new Error("order must contain at least one item");
  }

  for (const item of items) {
    if (item.quantity <= 0) {
      throw new Error("item quantity must be greater than zero");
    }

    if (item.unitPrice < 0) {
      throw new Error("item unit price cannot be negative");
    }
  }

  const order: Order = {
    id: `ord_${crypto.randomUUID()}`,
    customerId,
    items,
    totalAmount: calculateTotal(items),
    status: "PENDING_PAYMENT",
    createdAt: new Date().toISOString()
  };

  orders.set(order.id, order);

  publishEvent("OrderCreated", {
    orderId: order.id,
    customerId: order.customerId,
    totalAmount: order.totalAmount
  });

  return order;
}

function cancelOrder(orderId: string): Order {
  const order = orders.get(orderId);

  if (!order) {
    throw new Error("order not found");
  }

  if (order.status === "SHIPPED") {
    throw new Error("cannot cancel an order that has already shipped");
  }

  if (order.status === "CANCELLED") {
    return order;
  }

  order.status = "CANCELLED";

  publishEvent("OrderCancelled", {
    orderId: order.id,
    customerId: order.customerId
  });

  return order;
}

app.post("/orders", (req: Request, res: Response) => {
  try {
    const order = createOrder(req.body.customerId, req.body.items ?? []);
    res.status(201).json(order);
  } catch (error) {
    res.status(400).json({
      error: "INVALID_ORDER",
      message: error instanceof Error ? error.message : "Unknown error"
    });
  }
});

app.get("/orders/:orderId", (req: Request, res: Response) => {
  const order = orders.get(req.params.orderId);

  if (!order) {
    res.status(404).json({
      error: "ORDER_NOT_FOUND"
    });
    return;
  }

  res.json(order);
});

app.post("/orders/:orderId/cancel", (req: Request, res: Response) => {
  try {
    const order = cancelOrder(req.params.orderId);
    res.json(order);
  } catch (error) {
    res.status(400).json({
      error: "ORDER_CANCELLATION_FAILED",
      message: error instanceof Error ? error.message : "Unknown error"
    });
  }
});

app.listen(3000, () => {
  console.log("Order Service listening on port 3000");
});
```

This example is intentionally simple. In a production system, the service would usually include:

* persistent storage,
* schema migrations,
* authentication and authorization,
* idempotency keys,
* structured logging,
* tracing,
* retries for external calls,
* event publishing with delivery guarantees,
* validation,
* metrics,
* integration tests,
* contract tests.

The important architectural point is that the Order Service owns order behavior. It does not directly own payment authorization, inventory reservation, or shipment execution.

---

#### Collaboration between capability services

Business capability services still need to collaborate. The difference is that they collaborate through explicit contracts instead of shared internals.

A checkout flow might be orchestrated by a Checkout Service:

```mermaid
sequenceDiagram
    participant Client
    participant Checkout as Checkout Service
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service
    participant Shipping as Shipping Service

    Client->>Checkout: Submit checkout
    Checkout->>Orders: Create order
    Orders-->>Checkout: Order created

    Checkout->>Payments: Authorize payment
    Payments-->>Checkout: Payment authorized

    Checkout->>Inventory: Reserve inventory
    Inventory-->>Checkout: Inventory reserved

    Checkout->>Orders: Confirm order
    Orders-->>Checkout: Order confirmed

    Checkout->>Shipping: Create shipment request
    Shipping-->>Checkout: Shipment requested

    Checkout-->>Client: Checkout complete
```

This style makes the workflow explicit. It can be easier to understand when the business process has a clear sequence.

Another option is event-driven collaboration:

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Bus[(Event Bus)]

    Orders -->|OrderCreated| Bus

    Bus --> Payments
    Bus --> Inventory

    Payments -->|PaymentAuthorized| Bus
    Inventory -->|InventoryReserved| Bus

    Bus --> Orders

    Orders -->|OrderConfirmed| Bus
    Bus --> Shipping
```

This style reduces direct coupling between services. Services publish facts about what happened, and other services react.

Both approaches are valid. The choice depends on:

* how much control the workflow needs,
* how visible the process should be,
* how much eventual consistency is acceptable,
* how failures should be handled,
* whether the process is mostly sequential or reactive.

---

#### Data ownership

Capability-based decomposition usually works best when each service owns its data.

A problematic design is a shared database used by many services:

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    SharedDB[(Shared Database)]

    Orders --> SharedDB
    Payments --> SharedDB
    Inventory --> SharedDB
    Shipping --> SharedDB
```

This creates hidden coupling. If the schema changes, multiple services may break. Teams may also bypass each other’s business rules by directly reading or writing shared tables.

A better design is database ownership by service:

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    OrdersDB[(Orders DB)]
    PaymentsDB[(Payments DB)]
    InventoryDB[(Inventory DB)]
    ShippingDB[(Shipping DB)]

    Orders --> OrdersDB
    Payments --> PaymentsDB
    Inventory --> InventoryDB
    Shipping --> ShippingDB

    Orders -. API or Events .-> Payments
    Orders -. API or Events .-> Inventory
    Orders -. API or Events .-> Shipping
```

This does not mean every service must use a physically separate database server. The key rule is **ownership**:

> Only the owning service should directly read and write its data model.

Other services should use APIs, events, replicated read models, or analytics pipelines.

---

#### Modular monolith as a stepping stone

You do not always need to start with microservices. If the business domain is still evolving, a modular monolith may be a better first step.

```mermaid
flowchart TD
    subgraph App[Modular Monolith]
        Orders[Orders Module]
        Payments[Payments Module]
        Inventory[Inventory Module]
        Shipping[Shipping Module]
    end

    App --> DB[(Database)]
```

A modular monolith can still be organized around business capabilities. The modules can enforce internal boundaries while avoiding the operational complexity of distributed services.

Later, if a module needs independent scaling, deployment, or ownership, it can be extracted into a service.

This is often safer than creating many microservices too early.

---

#### Team ownership

Business-capability decomposition works best when architecture and team ownership align.

```mermaid
flowchart TD
    OrdersTeam[Orders Team]
    PaymentsTeam[Payments Team]
    InventoryTeam[Inventory Team]

    OrdersService[Order Service]
    PaymentsService[Payment Service]
    InventoryService[Inventory Service]

    OrdersTeam --> OrdersService
    PaymentsTeam --> PaymentsService
    InventoryTeam --> InventoryService
```

The goal is for teams to own business outcomes, not just technical components.

For example:

* The Orders Team owns order lifecycle reliability.
* The Payments Team owns successful and compliant payment processing.
* The Inventory Team owns accurate stock availability.

This improves accountability. When a business process fails, ownership is clearer.

---

#### When to use it

Use this pattern when:

* the business domain has recognizable functional areas,
* different parts of the system change for different reasons,
* different capabilities need different scaling characteristics,
* different areas have different compliance or reliability needs,
* teams can own services long term,
* you want independent deployment by business area,
* you want services to own their own data,
* you are migrating from a monolith and need stable extraction boundaries.

It works especially well when business capabilities are relatively stable. Capabilities do change, but they usually change more slowly than screens, database schemas, or implementation details.

---

#### When not to use it

Avoid or delay this pattern when:

* the product is very early and the domain is unclear,
* the team is too small to operate multiple services,
* the main problem is code organization rather than independent deployment,
* most features require strong transactions across the same data,
* the organization cannot support service ownership,
* observability, deployment, and operational practices are immature,
* service boundaries are being guessed without domain understanding.

In those cases, start with a modular monolith organized around business capabilities. That gives you many of the design benefits without immediately taking on distributed systems complexity.

---

#### Benefits

**1. Aligns architecture with the business**

Services are named after business functions, so the architecture is easier for engineers, product managers, and business stakeholders to discuss.

**2. Improves team autonomy**

Teams can own a capability end to end and release changes without coordinating across every technical layer.

**3. Enables independent scaling**

Different capabilities can scale differently. Search may need high read throughput. Payments may need high reliability and auditability. Notifications may need asynchronous throughput.

**4. Clarifies data ownership**

Each service owns the data required for its capability. This reduces accidental coupling through shared tables.

**5. Improves change isolation**

A change to shipping carrier integration should not require redeploying catalog, payments, and customer profile code.

**6. Supports fault isolation**

If recommendations fail, checkout may still work. If notifications are delayed, order creation may still succeed.

**7. Encourages business-focused APIs**

APIs become centered around meaningful business operations rather than generic CRUD over database tables.

---

#### Trade-offs

**1. Boundaries are difficult to identify**

Business capabilities are not always obvious. For example, pricing might belong to Catalog, Checkout, Orders, or its own Pricing Service.

**2. Workflows become distributed**

Processes like checkout, returns, refunds, or account closure may span many services. This introduces complexity around retries, idempotency, eventual consistency, and failure handling.

**3. Queries become harder**

When each service owns its data, cross-service reporting cannot rely on simple database joins. You may need read models, search indexes, event streams, or analytical data stores.

**4. Some data duplication is normal**

The Order Service may store the product name and price as they appeared at purchase time, even though the Catalog Service also stores product information.

**5. Operational complexity increases**

More services require more deployment pipelines, monitoring, logging, alerting, security policies, and on-call practices.

**6. Service sprawl is a risk**

If boundaries are too small, the system becomes fragmented and expensive to operate.

**7. Consistency models become more complex**

A monolith can often use one database transaction. Microservices often require eventual consistency and compensating actions.

---

#### Common mistakes

**Mistake 1: Splitting by technical layer**

Avoid creating services like:

* UI Service
* Business Logic Service
* Data Service
* Validation Service

These usually produce distributed monoliths.

**Mistake 2: Sharing databases between services**

A shared database makes services look independent while keeping them tightly coupled.

**Mistake 3: Making services too small**

Do not create a service for every class, table, operation, or validation rule.

**Mistake 4: Making services too broad**

A service that owns too many unrelated capabilities becomes a mini-monolith.

**Mistake 5: Ignoring team ownership**

A service without a clear owner often becomes neglected or chaotic.

**Mistake 6: Confusing entities with capabilities**

A database entity is not always a service boundary. For example, `Customer` may appear in Orders, Billing, Support, and Identity, but each capability may need a different view of the customer.

**Mistake 7: Assuming microservices remove coordination**

They reduce some kinds of coordination but introduce others, especially around contracts, events, observability, and distributed workflows.

---

#### Distributed monolith warning

A system can have many services and still behave like a monolith.

```mermaid
flowchart TD
    Client[Client]
    Controller[Order Controller Service]
    Validation[Order Validation Service]
    Rules[Order Rules Service]
    Persistence[Order Persistence Service]
    Notification[Order Notification Service]
    DB[(Orders DB)]

    Client --> Controller
    Controller --> Validation
    Validation --> Rules
    Rules --> Persistence
    Persistence --> DB
    Persistence --> Notification
```

This design is service-oriented in shape, but not in autonomy. The services are too dependent on each other and probably must change together.

A better boundary would keep order-specific behavior inside the Order Service and communicate with other capabilities through APIs or events.

---

#### Practical design checklist

A proposed service boundary is probably strong if:

* it maps to language the business already uses,
* it owns a clear business outcome,
* it contains related business rules,
* it can own its data,
* it can be changed by one team most of the time,
* it exposes a clear API or event contract,
* it has high internal cohesion,
* it has low coupling to unrelated services,
* it can be deployed independently,
* its failure can be isolated or degraded gracefully.

A proposed service boundary is probably weak if:

* it is named after a technical layer,
* it mostly forwards calls to another service,
* it has little or no business logic,
* it needs direct access to another service’s database,
* every change requires several services to be deployed together,
* its purpose is hard to explain to a non-engineer,
* it is too small to make a business decision,
* it is so broad that many unrelated teams must change it.

---

#### Related patterns

| Pattern                   | Relationship                                                       |
| ------------------------- | ------------------------------------------------------------------ |
| Decompose by Subdomain    | A more domain-driven way to find business-aligned boundaries       |
| Database per Service      | Often follows from service ownership of a capability               |
| API Gateway               | Gives clients a single entry point to capability services          |
| Backends for Frontends    | Adapts capability services to specific client needs                |
| Saga                      | Coordinates business workflows across multiple capability services |
| Event-Driven Architecture | Lets services react to business events without tight coupling      |
| Anti-Corruption Layer     | Protects a service from legacy or external domain models           |
| Modular Monolith          | Useful stepping stone before extracting services                   |
| Consumer-Driven Contracts | Helps keep service APIs safe for consumers as they evolve          |

---

#### Summary

Decomposing by business capability means designing services around what the business does, not around technical layers.

A good capability service owns:

* a clear business responsibility,
* the rules for that responsibility,
* the data required for that responsibility,
* the APIs and events that expose that responsibility,
* the operational reliability of that responsibility.

The goal is not to create the maximum number of services. The goal is to create boundaries that match how the business changes.

A strong service boundary should be easy to describe:

> The Payment Service owns payment authorization, capture, refunds, and payment state.

> The Inventory Service owns stock availability, reservations, and inventory adjustments.

> The Order Service owns order creation, order status, cancellation, and order history.

If a service cannot be explained clearly in business language, the boundary probably needs more work.


---

### 2. Decompose by Subdomain

#### What it is

**Decompose by Subdomain** is a microservice decomposition pattern based on **Domain-Driven Design**, often abbreviated as **DDD**. Instead of splitting the system around broad business capabilities alone, this pattern splits the system around **subdomains** and **bounded contexts** inside the larger business domain.

A **domain** is the overall business area your software supports.

For example:

| Company Type        | Overall Domain                                     |
| ------------------- | -------------------------------------------------- |
| Online retailer     | Selling and fulfilling products                    |
| Bank                | Managing financial accounts and transactions       |
| Insurance company   | Selling policies and handling claims               |
| Streaming platform  | Delivering media subscriptions and recommendations |
| Healthcare platform | Managing patient care and clinical workflows       |

A **subdomain** is a smaller area within that larger domain.

For an online retailer, subdomains might include:

* catalog management,
* pricing,
* checkout,
* order management,
* inventory,
* payments,
* shipping,
* returns,
* customer support,
* recommendations.

The important idea is that each subdomain may have its own concepts, rules, workflows, and language.

A **bounded context** is the boundary within which a particular domain model is valid.

For example, the word **product** may mean different things in different parts of the business:

| Context   | Meaning of “Product”                                                                           |
| --------- | ---------------------------------------------------------------------------------------------- |
| Catalog   | A sellable item with title, description, images, attributes, and categories                    |
| Inventory | A stock-keeping unit that can be counted, reserved, picked, and replenished                    |
| Pricing   | An item with a base price, discounts, tax rules, and promotion eligibility                     |
| Shipping  | A physical package with weight, dimensions, carrier restrictions, and hazardous-material rules |
| Support   | Something a customer bought and may ask questions about                                        |

A single universal `Product` model would likely become messy because every part of the business needs different information and behavior.

A subdomain-based architecture allows each context to model the concept in the way that makes sense locally.

```mermaid
flowchart TD
    Domain[Online Retail Domain]

    Domain --> Catalog[Catalog Context]
    Domain --> Inventory[Inventory Context]
    Domain --> Pricing[Pricing Context]
    Domain --> Shipping[Shipping Context]
    Domain --> Support[Support Context]

    Catalog --> CatalogProduct[Product means sellable listing]
    Inventory --> InventoryProduct[Product means stock-keeping unit]
    Pricing --> PricingProduct[Product means priceable item]
    Shipping --> ShippingProduct[Product means shippable package]
    Support --> SupportProduct[Product means purchased item]
```

The goal is not to eliminate differences in meaning. The goal is to make those differences explicit and contained.

---

#### Business capability vs subdomain

Business capability decomposition and subdomain decomposition are closely related, but they are not exactly the same.

**Business capability decomposition** asks:

> What does the business do?

**Subdomain decomposition** asks:

> What distinct areas of business knowledge, rules, and language exist inside the domain?

A business capability is often more organizational and functional. A subdomain is more about the underlying domain model and knowledge.

For example:

| Perspective         | Example                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------- |
| Business capability | “We need to manage inventory.”                                                                                |
| Subdomain           | “Inventory has its own model of stock, reservations, warehouses, bins, replenishment, and availability.”      |
| Business capability | “We need to collect payments.”                                                                                |
| Subdomain           | “Payments has its own model of authorization, capture, settlement, refunds, chargebacks, and risk.”           |
| Business capability | “We need customer support.”                                                                                   |
| Subdomain           | “Support has its own model of tickets, agents, cases, priorities, escalations, and service-level agreements.” |

In many systems, one subdomain becomes one microservice. But that is not a rule. A complex subdomain may become several services, and a simple subdomain may remain a module inside another service.

```mermaid
flowchart TD
    Business[Business Domain]

    Business --> SubdomainA[Subdomain A]
    Business --> SubdomainB[Subdomain B]
    Business --> SubdomainC[Subdomain C]

    SubdomainA --> ServiceA[Service A]
    SubdomainB --> ServiceB[Service B]
    SubdomainC --> ModuleC[Module inside another service]
```

The mapping depends on complexity, team ownership, operational needs, and how independently the subdomain changes.

---

#### Why this pattern exists

Large systems often fail because they try to force the entire business into one shared model.

At first, a shared model can feel convenient:

```mermaid
flowchart TD
    SharedModel[Enterprise Shared Domain Model]

    SharedModel --> Orders[Orders]
    SharedModel --> Payments[Payments]
    SharedModel --> Inventory[Inventory]
    SharedModel --> Shipping[Shipping]
    SharedModel --> Support[Support]
```

But as the business grows, the model becomes overloaded.

A `Customer` might mean:

* a person with login credentials in Identity,
* a buyer with saved addresses in Commerce,
* an account holder in Billing,
* a recipient in Shipping,
* a case requester in Support,
* a segment member in Marketing.

A `Status` might mean:

* payment status,
* order status,
* shipment status,
* account status,
* support ticket status.

A `Product` might mean:

* a catalog listing,
* a physical SKU,
* a subscription plan,
* a licensed entitlement,
* a bundled offer.

When one model tries to serve every context, it often becomes vague and bloated:

```ts
type Product = {
  id: string;

  // Catalog fields
  title?: string;
  description?: string;
  images?: string[];
  categoryId?: string;

  // Inventory fields
  sku?: string;
  warehouseId?: string;
  quantityAvailable?: number;
  reorderThreshold?: number;

  // Pricing fields
  basePrice?: number;
  discountRules?: unknown[];
  taxCategory?: string;

  // Shipping fields
  weight?: number;
  length?: number;
  width?: number;
  height?: number;
  hazardousMaterialCode?: string;

  // Support fields
  warrantyPeriodDays?: number;
  supportArticleIds?: string[];
};
```

This model looks reusable, but it creates several problems:

* Most fields are irrelevant in most contexts.
* Different teams may disagree about what fields mean.
* One team’s change can break another team’s assumptions.
* The model becomes hard to validate.
* The model encourages database and code coupling.
* Business rules end up scattered across unrelated areas.

Subdomain decomposition solves this by allowing different models in different bounded contexts.

```mermaid
flowchart TD
    ProductConcept[Concept: Product]

    ProductConcept --> CatalogModel[Catalog Product Model]
    ProductConcept --> InventoryModel[Inventory SKU Model]
    ProductConcept --> PricingModel[Pricing Item Model]
    ProductConcept --> ShippingModel[Shipping Package Model]

    CatalogModel --> CatalogService[Catalog Service]
    InventoryModel --> InventoryService[Inventory Service]
    PricingModel --> PricingService[Pricing Service]
    ShippingModel --> ShippingService[Shipping Service]
```

Each service can model the concept precisely for its own purpose.

---

#### What it solves

This pattern solves **semantic coupling**.

Semantic coupling happens when different parts of the system depend on the same concept but mean different things by it.

For example, consider the word **available**.

In the Catalog context:

> Available means the product is visible and sellable on the website.

In the Inventory context:

> Available means there is stock that can be reserved.

In the Shipping context:

> Available means the item can be shipped to the customer’s destination.

In the Compliance context:

> Available means the item is legally allowed to be sold in that region.

If all of these meanings are collapsed into one field like this:

```json
{
  "productId": "prod_123",
  "available": true
}
```

the system becomes ambiguous. Different teams may interpret the value differently.

A better design makes the contexts explicit:

```json
{
  "productId": "prod_123",
  "catalogVisibility": "VISIBLE",
  "inventoryAvailability": "IN_STOCK",
  "shippingEligibility": "SHIPPABLE",
  "regionalCompliance": "ALLOWED"
}
```

Or, more commonly in microservices, each context owns its own state and exposes it through APIs or events.

```mermaid
flowchart TD
    ProductPage[Product Page]

    ProductPage --> Catalog[Catalog Service]
    ProductPage --> Inventory[Inventory Service]
    ProductPage --> Shipping[Shipping Service]
    ProductPage --> Compliance[Compliance Service]

    Catalog --> CatalogMeaning[Visible for sale]
    Inventory --> InventoryMeaning[Stock can be reserved]
    Shipping --> ShippingMeaning[Can ship to address]
    Compliance --> ComplianceMeaning[Legal in region]
```

The UI or API composition layer can combine these signals when needed, but the meanings remain owned by the right contexts.

---

#### Core, supporting, and generic subdomains

Domain-Driven Design often classifies subdomains into three types:

1. **Core subdomains**
2. **Supporting subdomains**
3. **Generic subdomains**

This classification helps teams decide where to invest the most design effort.

##### Core subdomain

A **core subdomain** is the part of the business that creates competitive advantage.

It is what makes the company meaningfully different from competitors.

Examples:

| Business                | Possible Core Subdomain                                                    |
| ----------------------- | -------------------------------------------------------------------------- |
| Streaming platform      | Recommendations and personalization                                        |
| Logistics company       | Route optimization and delivery planning                                   |
| Marketplace             | Matching buyers and sellers                                                |
| Fraud detection company | Risk scoring and fraud models                                              |
| Online retailer         | Pricing, fulfillment optimization, or merchandising, depending on strategy |

Core subdomains deserve the most careful modeling, the strongest engineering investment, and often the most experienced teams.

##### Supporting subdomain

A **supporting subdomain** is important to the business but not usually a source of unique advantage.

Examples:

* customer support ticketing,
* internal admin workflows,
* standard reporting,
* product import tools,
* approval workflows.

These still need to work well, but they may not require the same level of custom design as a core subdomain.

##### Generic subdomain

A **generic subdomain** is common across many businesses and can often be bought or reused.

Examples:

* authentication,
* email delivery,
* payment gateway integration,
* tax calculation,
* logging,
* file storage,
* basic CRM,
* content management.

Generic subdomains are often good candidates for third-party services or platform components.

```mermaid
flowchart TD
    Domain[Business Domain]

    Domain --> Core[Core Subdomains]
    Domain --> Supporting[Supporting Subdomains]
    Domain --> Generic[Generic Subdomains]

    Core --> Differentiating[High business differentiation]
    Core --> Invest[Invest deeply]

    Supporting --> Necessary[Business-specific but not differentiating]
    Supporting --> Build[Build simply]

    Generic --> Commodity[Common across companies]
    Generic --> Buy[Buy or reuse when possible]
```

This matters because not every part of the system deserves the same architectural complexity.

You may build a sophisticated custom model for a core subdomain, a simpler internal tool for a supporting subdomain, and use an external provider for a generic subdomain.

---

#### Example: insurance domain

Subdomain decomposition is especially useful in complex domains like insurance.

An insurance company might have subdomains such as:

```mermaid
flowchart TD
    Insurance[Insurance Domain]

    Insurance --> Quoting[Quoting]
    Insurance --> Underwriting[Underwriting]
    Insurance --> Policy[Policy Management]
    Insurance --> Billing[Billing]
    Insurance --> Claims[Claims]
    Insurance --> Fraud[Fraud Detection]
    Insurance --> Reinsurance[Reinsurance]
    Insurance --> Customer[Customer Service]
```

Several of these contexts use the same words differently.

For example, a **policy** can mean different things:

| Context           | Meaning of “Policy”                                                |
| ----------------- | ------------------------------------------------------------------ |
| Quoting           | A proposed product configuration used to estimate price            |
| Underwriting      | A risk decision requiring approval, conditions, or rejection       |
| Policy Management | A legal contract with coverages, endorsements, and effective dates |
| Billing           | A billable account with premiums, invoices, and payment schedules  |
| Claims            | A source of coverage rules used to decide whether a claim is valid |
| Customer Service  | Something a customer asks questions about                          |

Trying to create one universal `Policy` model across all of these contexts would make the system rigid and confusing.

Instead, each bounded context models policy in the way that serves its own rules.

```mermaid
flowchart TD
    PolicyConcept[Concept: Policy]

    PolicyConcept --> QuotePolicy[Quoted Policy]
    PolicyConcept --> UnderwritingPolicy[Underwriting Case]
    PolicyConcept --> ActivePolicy[Active Policy Contract]
    PolicyConcept --> BillingAccount[Billing Account]
    PolicyConcept --> ClaimCoverage[Claim Coverage Reference]

    QuotePolicy --> QuotingService[Quoting Service]
    UnderwritingPolicy --> UnderwritingService[Underwriting Service]
    ActivePolicy --> PolicyService[Policy Service]
    BillingAccount --> BillingService[Billing Service]
    ClaimCoverage --> ClaimsService[Claims Service]
```

The contexts can still communicate, but they should not all be forced into the same object model.

---

#### Bounded contexts and translation

Bounded contexts need to communicate. The important part is that they should not leak their internal model into every other context.

For example, the Catalog Service may publish an event when a product is created:

```json
{
  "eventType": "CatalogProductCreated",
  "eventId": "evt_1001",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "catalogProductId": "cat_123",
    "title": "Trail Running Shoe",
    "brand": "SummitRun",
    "category": "Footwear"
  }
}
```

The Inventory Service may consume this event, but it should translate it into its own model:

```ts
type CatalogProductCreated = {
  catalogProductId: string;
  title: string;
  brand: string;
  category: string;
};

type InventoryItem = {
  sku: string;
  catalogProductId: string;
  stockingStatus: "NOT_STOCKED" | "STOCKED" | "DISCONTINUED";
  reorderThreshold: number;
};

function createInventoryItemFromCatalogEvent(
  event: CatalogProductCreated
): InventoryItem {
  return {
    sku: `sku_${event.catalogProductId}`,
    catalogProductId: event.catalogProductId,
    stockingStatus: "NOT_STOCKED",
    reorderThreshold: 0
  };
}
```

Notice that the Inventory model does not blindly copy the Catalog model. It stores only what it needs and adds inventory-specific meaning.

This translation boundary protects each context.

```mermaid
flowchart TD
    Catalog[Catalog Context]
    Event[CatalogProductCreated Event]
    Translator[Translation Logic]
    Inventory[Inventory Context]

    Catalog --> Event
    Event --> Translator
    Translator --> Inventory

    Inventory --> InventoryModel[Inventory Item Model]
```

This is closely related to the **Anti-Corruption Layer** pattern. An anti-corruption layer protects one domain model from being polluted by another model.

---

#### Context mapping

A **context map** shows how bounded contexts relate to each other.

It helps teams understand integration relationships, ownership, and dependency direction.

For example:

```mermaid
flowchart TD
    Catalog[Catalog Context]
    Pricing[Pricing Context]
    Inventory[Inventory Context]
    Checkout[Checkout Context]
    Orders[Order Context]
    Payments[Payment Context]
    Shipping[Shipping Context]

    Catalog --> Checkout
    Pricing --> Checkout
    Inventory --> Checkout
    Checkout --> Orders
    Checkout --> Payments
    Orders --> Shipping
```

This tells us Checkout depends on information from Catalog, Pricing, and Inventory. Orders and Payments are downstream of Checkout. Shipping depends on Orders.

But this diagram does not yet explain the type of relationship. DDD names several types of context relationships. The most common practical ones are:

| Relationship          | Meaning                                                    |
| --------------------- | ---------------------------------------------------------- |
| Customer/Supplier     | One context provides something another context depends on  |
| Conformist            | One context must follow another context’s model            |
| Anti-Corruption Layer | One context translates another model to protect itself     |
| Shared Kernel         | Two contexts intentionally share a small part of the model |
| Published Language    | Contexts communicate through a documented, stable contract |
| Open Host Service     | One context exposes a formal API for many consumers        |

For most microservice architectures, **Published Language**, **Open Host Service**, and **Anti-Corruption Layer** are especially important.

```mermaid
flowchart TD
    Upstream[Upstream Context]
    Contract[Published API or Event Contract]
    Translator[Anti-Corruption Layer]
    Downstream[Downstream Context]

    Upstream --> Contract
    Contract --> Translator
    Translator --> Downstream
```

The downstream context should depend on a stable contract, not the upstream context’s internal database or internal objects.

---

#### Example implementation: separating models by context

A common mistake is trying to reuse the same DTO, database table, or class across contexts.

For example:

```ts
type SharedCustomer = {
  id: string;
  email: string;
  passwordHash: string;
  billingAddress: string;
  shippingAddress: string;
  supportTier: "STANDARD" | "PREMIUM";
  marketingSegment: string;
  creditLimit: number;
};
```

This type mixes concerns from Identity, Billing, Shipping, Support, Marketing, and Credit.

A subdomain-based design would separate the models:

```ts
type IdentityUser = {
  userId: string;
  email: string;
  passwordHash: string;
  mfaEnabled: boolean;
};

type BillingCustomer = {
  billingCustomerId: string;
  userId: string;
  billingAddressId: string;
  taxRegion: string;
  paymentTerms: "PREPAID" | "NET_30";
};

type ShippingRecipient = {
  recipientId: string;
  userId: string;
  defaultShippingAddressId: string;
  deliveryPreferences: string[];
};

type SupportCustomer = {
  supportCustomerId: string;
  userId: string;
  supportTier: "STANDARD" | "PREMIUM" | "ENTERPRISE";
  openCaseCount: number;
};

type MarketingProfile = {
  profileId: string;
  userId: string;
  segments: string[];
  emailOptIn: boolean;
};
```

These models may all refer to the same real-world person, but they serve different business contexts.

This gives each context freedom to evolve.

---

#### API example: context-specific representation

Suppose a client asks for customer information from different services.

The Identity Service might return:

```json
{
  "userId": "usr_123",
  "email": "alex@example.com",
  "mfaEnabled": true
}
```

The Support Service might return:

```json
{
  "supportCustomerId": "sup_456",
  "userId": "usr_123",
  "supportTier": "PREMIUM",
  "openCaseCount": 2,
  "lastContactedAt": "2026-04-25T14:30:00Z"
}
```

The Billing Service might return:

```json
{
  "billingCustomerId": "bill_789",
  "userId": "usr_123",
  "paymentTerms": "NET_30",
  "taxRegion": "US-CA",
  "billingStatus": "CURRENT"
}
```

These are not duplicate models by accident. They are different models for different contexts.

That is the point of bounded contexts.

---

#### When to use it

Use this pattern when:

* the domain is complex,
* the same words mean different things in different areas,
* business rules vary significantly across parts of the organization,
* a shared enterprise model is becoming confusing,
* different teams need to evolve their models independently,
* you need to distinguish core, supporting, and generic areas,
* domain experts use different language depending on context,
* service boundaries need to reflect business meaning, not just workflows.

This pattern is especially useful in domains such as:

* finance,
* insurance,
* healthcare,
* logistics,
* marketplaces,
* enterprise SaaS,
* telecommunications,
* supply chain,
* legal technology,
* education platforms.

These domains often contain rich business rules and specialized terminology.

---

#### When not to use it

Avoid applying this pattern too aggressively when:

* the domain is simple,
* the business language is already consistent,
* the team does not yet understand the domain,
* the product is still searching for product-market fit,
* service boundaries are likely to change weekly,
* the cost of separate services is higher than the benefit,
* a modular monolith would provide enough separation.

DDD can be powerful, but it can also be overused. Not every noun needs a bounded context. Not every context needs a separate microservice.

A simple CRUD application may not need deep subdomain decomposition.

---

#### Benefits

**1. More precise domain models**

Each bounded context can model its own concepts accurately without compromising for unrelated use cases.

**2. Less semantic confusion**

Teams can use the same word differently as long as the boundary is clear.

**3. Reduced accidental coupling**

A change in one context’s model does not automatically force changes in every other context.

**4. Better alignment with domain experts**

Engineers can work with the specific experts for a subdomain and use that context’s language.

**5. Better prioritization**

Core subdomains can receive deeper investment, while generic subdomains can be bought or simplified.

**6. Cleaner APIs and events**

Contracts become explicit translations between contexts instead of leaking internal models everywhere.

**7. Easier long-term evolution**

Each context can evolve its model as the business changes.

---

#### Trade-offs

**1. Requires deep domain understanding**

You cannot identify good subdomains purely from database tables or URL paths. You need conversations with domain experts.

**2. Boundaries may be unstable early**

If the business is still poorly understood, early boundaries may be wrong and require refactoring.

**3. More models to maintain**

The same real-world entity may have several context-specific representations. This is intentional, but it adds cognitive load.

**4. Integration requires translation**

Contexts need APIs, events, mapping logic, and anti-corruption layers.

**5. Reporting can become more complex**

Data is distributed across contexts, so analytical views may require pipelines or read models.

**6. Risk of over-modeling**

Teams may create too many contexts, too many abstractions, or overly elaborate domain models for simple problems.

**7. Requires strong collaboration**

The architecture depends on shared understanding between engineers, product owners, operations teams, and domain experts.

---

#### Common mistakes

**Mistake 1: Treating every entity as a service**

A `Customer` table does not automatically mean you need a Customer Service. Ask what business capability or subdomain owns each part of customer meaning.

**Mistake 2: Creating one enterprise-wide model**

A universal model often becomes bloated, ambiguous, and politically difficult to change.

**Mistake 3: Ignoring language differences**

If two teams use the same word differently, that is a strong signal of separate bounded contexts.

**Mistake 4: Sharing internal database tables**

Contexts should not integrate by directly reading each other’s tables.

**Mistake 5: Copying upstream models blindly**

A downstream context should translate external models into its own language.

**Mistake 6: Making every bounded context a microservice immediately**

A bounded context can be a module first. Extract it into a service only when independent deployment, scaling, or ownership is valuable.

**Mistake 7: Neglecting generic subdomains**

Teams sometimes build custom solutions for generic problems where buying or reusing would be cheaper and safer.

---

#### Practical design checklist

A proposed subdomain boundary is probably strong if:

* domain experts recognize it as a distinct area,
* it has its own vocabulary,
* it has its own business rules,
* it changes for different reasons than neighboring areas,
* it has a clear data owner,
* it can expose stable APIs or events,
* it can be understood without knowing the entire enterprise model,
* it has clear upstream and downstream relationships,
* its model is cohesive internally,
* it does not require direct database access to another context.

A proposed boundary is probably weak if:

* it is based only on a database table,
* it has no distinct language,
* it has no distinct business rules,
* it mostly exists because of a technical layer,
* it changes every time another context changes,
* its concepts are vague or overloaded,
* it is difficult to explain to domain experts,
* it requires constant cross-team coordination,
* it leaks internal model details into many other contexts.

---

#### Related patterns

| Pattern                          | Relationship                                                                            |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| Decompose by Business Capability | Often overlaps with subdomain decomposition, but focuses more on what the business does |
| Bounded Context                  | The DDD boundary where a model has a specific meaning                                   |
| Anti-Corruption Layer            | Protects one context from another context’s model                                       |
| Database per Service             | Supports model ownership and autonomy                                                   |
| Published Language               | Defines stable contracts between contexts                                               |
| Open Host Service                | Provides a formal API for other contexts                                                |
| Saga                             | Coordinates workflows across contexts                                                   |
| Event-Driven Architecture        | Allows contexts to publish and react to domain events                                   |
| Consumer-Driven Contracts        | Tests that context contracts satisfy downstream needs                                   |
| Modular Monolith                 | Useful way to implement bounded contexts before extracting services                     |

---

#### Summary

Decomposing by subdomain means designing service boundaries around distinct areas of business knowledge and meaning.

The central idea is:

> Different parts of the business may use the same words differently, and that is okay. The architecture should make those boundaries explicit.

Instead of forcing one shared model across the whole system, each bounded context gets its own model, rules, language, APIs, and data ownership.

This pattern is especially valuable in complex domains where business language matters. It helps teams avoid semantic confusion, reduce accidental coupling, and invest most deeply in the parts of the system that create competitive advantage.

A strong subdomain boundary should be easy to describe:

> In Catalog, a product is a sellable listing.

> In Inventory, a product is stock that can be counted and reserved.

> In Shipping, a product is a physical item with weight, dimensions, and delivery restrictions.

When those meanings are kept separate, each part of the system can evolve more safely and more accurately.


---

### 3. Decompose by Transaction or Workflow Boundary

#### What it is

**Decompose by Transaction or Workflow Boundary** means designing services around business operations that need to complete as a meaningful unit of work.

A **transaction boundary** is the scope within which the system can make a change safely and consistently.

A **workflow boundary** is a meaningful stage in a larger business process.

This pattern asks:

> What part of this business process must be consistent immediately, and what parts can happen later?

In a monolith, one database transaction might handle an entire operation:

```mermaid
flowchart TD
    Client[Client]
    App[Application]
    DB[(Single Database)]

    Client --> App
    App --> DB

    subgraph Transaction[Single Database Transaction]
        CreateOrder[Create Order]
        ChargePayment[Record Payment]
        ReduceStock[Reduce Stock]
        CreateShipment[Create Shipment]
    end

    DB --> Transaction
```

In a microservice architecture, that same operation may involve several services, each with its own database:

```mermaid
flowchart TD
    Client[Client]
    Checkout[Checkout Workflow]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    OrdersDB[(Orders DB)]
    PaymentsDB[(Payments DB)]
    InventoryDB[(Inventory DB)]
    ShippingDB[(Shipping DB)]

    Client --> Checkout

    Checkout --> Orders
    Checkout --> Payments
    Checkout --> Inventory
    Checkout --> Shipping

    Orders --> OrdersDB
    Payments --> PaymentsDB
    Inventory --> InventoryDB
    Shipping --> ShippingDB
```

There is no single database transaction across all of these services. Instead, each service owns a **local transaction**.

For example:

| Service           | Local transaction it owns                                       |
| ----------------- | --------------------------------------------------------------- |
| Order Service     | Create order, update order status, cancel order                 |
| Payment Service   | Authorize payment, capture payment, refund payment              |
| Inventory Service | Reserve stock, release reservation, commit stock deduction      |
| Shipping Service  | Create shipment request, assign carrier, update shipment status |

The workflow as a whole may take seconds, minutes, hours, or even days. The system must be designed so each step can succeed, fail, retry, or compensate safely.

---

#### Why this pattern exists

Microservices make strong consistency harder.

Inside a monolith, it is common to rely on one ACID database transaction:

```sql
BEGIN;

INSERT INTO orders (...);
INSERT INTO payments (...);
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 'prod_123';
INSERT INTO shipments (...);

COMMIT;
```

If anything fails, the database can roll everything back.

That model becomes difficult when order data, payment data, inventory data, and shipping data are owned by different services.

```mermaid
flowchart TD
    Operation[Place Order]

    Operation --> OrderDB[(Orders DB)]
    Operation --> PaymentDB[(Payments DB)]
    Operation --> InventoryDB[(Inventory DB)]
    Operation --> ShippingDB[(Shipping DB)]

    Problem[No single database transaction covers all databases]

    OrderDB --> Problem
    PaymentDB --> Problem
    InventoryDB --> Problem
    ShippingDB --> Problem
```

Distributed transactions are possible in some environments, but they are often avoided in microservice systems because they can:

* reduce service autonomy,
* couple databases and infrastructure,
* increase latency,
* make failures harder to recover from,
* create locks across service boundaries,
* reduce availability,
* complicate scaling.

This pattern exists to make consistency boundaries explicit. Instead of pretending one global transaction exists, the architecture defines where local consistency is required and where eventual consistency is acceptable.

---

#### What it solves

This pattern solves the problem of **unclear consistency ownership**.

Without clear transaction or workflow boundaries, business logic can become scattered across many services:

```mermaid
flowchart TD
    Client[Client]
    ServiceA[Service A]
    ServiceB[Service B]
    ServiceC[Service C]
    ServiceD[Service D]

    Client --> ServiceA
    ServiceA --> ServiceB
    ServiceB --> ServiceC
    ServiceC --> ServiceD

    ServiceA --> Rule1[Some order rules]
    ServiceB --> Rule2[Some payment rules]
    ServiceC --> Rule3[Some inventory rules]
    ServiceD --> Rule4[Some shipping rules]
```

This makes it hard to answer basic questions:

* Which service owns the transaction?
* Which service decides whether the operation is complete?
* What happens if step three fails?
* Which changes must be rolled back?
* Which changes should be compensated?
* Which service owns the user-visible status?
* Can the workflow be retried safely?
* What state is the business process currently in?

A workflow-boundary design makes each step explicit:

```mermaid
flowchart TD
    Start[Start Checkout]

    Start --> CreateOrder[Create Order]
    CreateOrder --> AuthorizePayment[Authorize Payment]
    AuthorizePayment --> ReserveInventory[Reserve Inventory]
    ReserveInventory --> ConfirmOrder[Confirm Order]
    ConfirmOrder --> ArrangeShipping[Arrange Shipping]

    CreateOrder --> OrderLocalTx[Local transaction in Order Service]
    AuthorizePayment --> PaymentLocalTx[Local transaction in Payment Service]
    ReserveInventory --> InventoryLocalTx[Local transaction in Inventory Service]
    ArrangeShipping --> ShippingLocalTx[Local transaction in Shipping Service]
```

Each local transaction is owned by a service. The larger business workflow is coordinated through orchestration, events, or a saga.

---

#### Transaction boundary vs workflow boundary

A **transaction boundary** is about immediate consistency.

A **workflow boundary** is about business progress over time.

For example, in a checkout system:

| Boundary Type        | Example                | Consistency expectation                                 |
| -------------------- | ---------------------- | ------------------------------------------------------- |
| Transaction boundary | Create an order record | Must be immediately consistent inside Order Service     |
| Transaction boundary | Reserve inventory      | Must be immediately consistent inside Inventory Service |
| Transaction boundary | Authorize payment      | Must be immediately consistent inside Payment Service   |
| Workflow boundary    | Complete checkout      | May require several local transactions                  |
| Workflow boundary    | Fulfill order          | May take hours or days                                  |
| Workflow boundary    | Process refund         | May depend on payment, inventory, and returns           |

A local transaction can usually be implemented with a normal database transaction inside one service.

A workflow often needs multiple service interactions and must tolerate partial completion.

```mermaid
flowchart TD
    Workflow[Business Workflow]

    Workflow --> Step1[Step 1: Local Transaction]
    Workflow --> Step2[Step 2: Local Transaction]
    Workflow --> Step3[Step 3: Local Transaction]
    Workflow --> Step4[Step 4: Local Transaction]

    Step1 --> State1[Committed]
    Step2 --> State2[Committed]
    Step3 --> Failure[Failed]
    Step4 --> Skipped[Not Started]

    Failure --> Recovery[Retry or Compensate]
```

The system should be designed with this reality in mind.

---

#### Example: order placement workflow

Consider a simplified order placement workflow:

```mermaid
sequenceDiagram
    participant Client
    participant Checkout as Checkout Service
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service
    participant Shipping as Shipping Service

    Client->>Checkout: Place order
    Checkout->>Orders: Create pending order
    Orders-->>Checkout: Order created

    Checkout->>Payments: Authorize payment
    Payments-->>Checkout: Payment authorized

    Checkout->>Inventory: Reserve items
    Inventory-->>Checkout: Items reserved

    Checkout->>Orders: Confirm order
    Orders-->>Checkout: Order confirmed

    Checkout->>Shipping: Create shipment request
    Shipping-->>Checkout: Shipment requested

    Checkout-->>Client: Order accepted
```

Each service owns a different transaction:

| Step                    | Service           | Local transaction                                |
| ----------------------- | ----------------- | ------------------------------------------------ |
| Create pending order    | Order Service     | Insert order with status `PENDING`               |
| Authorize payment       | Payment Service   | Create payment authorization record              |
| Reserve items           | Inventory Service | Create reservation and reduce available quantity |
| Confirm order           | Order Service     | Change order status to `CONFIRMED`               |
| Create shipment request | Shipping Service  | Insert shipment request                          |

The whole checkout is not one database transaction. It is a workflow made of several committed local transactions.

---

#### Local transaction example

Inside the Inventory Service, reserving inventory should be a local transaction.

```ts
type ReservationStatus = "ACTIVE" | "RELEASED" | "COMMITTED";

type InventoryItem = {
  productId: string;
  availableQuantity: number;
};

type InventoryReservation = {
  reservationId: string;
  orderId: string;
  productId: string;
  quantity: number;
  status: ReservationStatus;
};

async function reserveInventory(
  db: Database,
  orderId: string,
  productId: string,
  quantity: number
): Promise<InventoryReservation> {
  return db.transaction(async (tx) => {
    const item = await tx.inventory.findByProductIdForUpdate(productId);

    if (!item) {
      throw new Error("inventory item not found");
    }

    if (item.availableQuantity < quantity) {
      throw new Error("insufficient inventory");
    }

    await tx.inventory.update(productId, {
      availableQuantity: item.availableQuantity - quantity
    });

    const reservation = await tx.reservations.insert({
      reservationId: crypto.randomUUID(),
      orderId,
      productId,
      quantity,
      status: "ACTIVE"
    });

    return reservation;
  });
}
```

This transaction is local to the Inventory Service. It makes the inventory update and reservation record consistent with each other.

The Inventory Service does not update the Order database. It may publish an event instead:

```json
{
  "eventType": "InventoryReserved",
  "eventId": "evt_3029",
  "occurredAt": "2026-04-29T19:10:00Z",
  "data": {
    "orderId": "ord_123",
    "reservationId": "res_456",
    "productId": "prod_789",
    "quantity": 2
  }
}
```

---

#### Workflow state

For long-running workflows, it is often useful to store explicit workflow state.

For checkout, a workflow state model might look like:

```ts
type CheckoutStatus =
  | "STARTED"
  | "ORDER_CREATED"
  | "PAYMENT_AUTHORIZED"
  | "INVENTORY_RESERVED"
  | "ORDER_CONFIRMED"
  | "SHIPMENT_REQUESTED"
  | "FAILED"
  | "COMPENSATED";

type CheckoutWorkflow = {
  workflowId: string;
  orderId?: string;
  paymentId?: string;
  reservationId?: string;
  shipmentId?: string;
  status: CheckoutStatus;
  failureReason?: string;
  createdAt: string;
  updatedAt: string;
};
```

This makes the progress of the workflow observable and recoverable.

```mermaid
stateDiagram-v2
    [*] --> STARTED
    STARTED --> ORDER_CREATED
    ORDER_CREATED --> PAYMENT_AUTHORIZED
    PAYMENT_AUTHORIZED --> INVENTORY_RESERVED
    INVENTORY_RESERVED --> ORDER_CONFIRMED
    ORDER_CONFIRMED --> SHIPMENT_REQUESTED
    SHIPMENT_REQUESTED --> [*]

    ORDER_CREATED --> FAILED
    PAYMENT_AUTHORIZED --> FAILED
    INVENTORY_RESERVED --> FAILED
    FAILED --> COMPENSATED
```

Without workflow state, failures can leave the system in confusing partial states.

---

#### Handling failure

Failures are normal in distributed workflows.

For example, payment may succeed but inventory reservation may fail:

```mermaid
sequenceDiagram
    participant Checkout as Checkout Service
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service

    Checkout->>Orders: Create pending order
    Orders-->>Checkout: Order created

    Checkout->>Payments: Authorize payment
    Payments-->>Checkout: Payment authorized

    Checkout->>Inventory: Reserve inventory
    Inventory-->>Checkout: Insufficient stock

    Checkout->>Payments: Void authorization
    Payments-->>Checkout: Authorization voided

    Checkout->>Orders: Cancel order
    Orders-->>Checkout: Order cancelled
```

The system cannot simply roll back the payment service’s database from outside. Instead, it performs a **compensating action**.

| Completed step     | Failure later          | Compensation                |
| ------------------ | ---------------------- | --------------------------- |
| Order created      | Payment failed         | Cancel order                |
| Payment authorized | Inventory unavailable  | Void authorization          |
| Inventory reserved | Payment capture failed | Release inventory           |
| Shipment created   | Order cancelled        | Cancel shipment if possible |
| Payment captured   | Return approved        | Refund payment              |

This is why workflow decomposition often pairs with the **Saga** pattern.

---

#### Orchestration approach

One way to manage a workflow is orchestration.

In orchestration, a central coordinator tells each service what to do next.

```mermaid
flowchart TD
    Client[Client]
    Orchestrator[Checkout Orchestrator]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    Client --> Orchestrator

    Orchestrator --> Orders
    Orchestrator --> Payments
    Orchestrator --> Inventory
    Orchestrator --> Shipping

    Orchestrator --> State[(Workflow State)]
```

The orchestrator owns the workflow sequence.

Example pseudo-code:

```ts
async function placeOrder(command: PlaceOrderCommand): Promise<void> {
  const workflow = await workflowStore.create({
    status: "STARTED",
    customerId: command.customerId
  });

  try {
    const order = await orderClient.createPendingOrder(command);
    await workflowStore.update(workflow.id, {
      orderId: order.id,
      status: "ORDER_CREATED"
    });

    const payment = await paymentClient.authorize({
      orderId: order.id,
      amount: order.totalAmount,
      paymentMethodId: command.paymentMethodId
    });
    await workflowStore.update(workflow.id, {
      paymentId: payment.id,
      status: "PAYMENT_AUTHORIZED"
    });

    const reservation = await inventoryClient.reserve({
      orderId: order.id,
      items: command.items
    });
    await workflowStore.update(workflow.id, {
      reservationId: reservation.id,
      status: "INVENTORY_RESERVED"
    });

    await orderClient.confirm(order.id);
    await workflowStore.update(workflow.id, {
      status: "ORDER_CONFIRMED"
    });

    await shippingClient.createShipmentRequest({
      orderId: order.id,
      address: command.shippingAddress
    });
    await workflowStore.update(workflow.id, {
      status: "SHIPMENT_REQUESTED"
    });
  } catch (error) {
    await compensate(workflow.id, error);
    throw error;
  }
}
```

Orchestration is often easier to understand because the workflow is visible in one place.

The trade-off is that the orchestrator can become too powerful if it starts owning business logic that belongs inside the domain services.

---

#### Choreography approach

Another way is choreography.

In choreography, services react to events. No single service tells every other service what to do.

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Bus[(Event Bus)]

    Orders -->|OrderCreated| Bus
    Bus --> Payments

    Payments -->|PaymentAuthorized| Bus
    Bus --> Inventory

    Inventory -->|InventoryReserved| Bus
    Bus --> Orders

    Orders -->|OrderConfirmed| Bus
    Bus --> Shipping
```

Each service owns its own reaction:

* Payment Service reacts to `OrderCreated`.
* Inventory Service reacts to `PaymentAuthorized`.
* Order Service reacts to `InventoryReserved`.
* Shipping Service reacts to `OrderConfirmed`.

This can reduce direct coupling, but it can also make the overall workflow harder to see.

A common failure mode is that the business process becomes hidden inside event subscriptions.

---

#### Orchestration vs choreography

| Question                       | Orchestration                      | Choreography                                |
| ------------------------------ | ---------------------------------- | ------------------------------------------- |
| Where is the workflow visible? | In the orchestrator                | Spread across event handlers                |
| Coupling style                 | Direct commands                    | Events                                      |
| Easier to debug?               | Often yes                          | Sometimes harder                            |
| Easier to extend?              | Depends on orchestrator design     | Often easier for independent reactions      |
| Risk                           | Orchestrator becomes a god service | Workflow becomes implicit and hard to trace |
| Good for                       | Clear sequential workflows         | Reactive, loosely coupled processes         |

A practical approach is often hybrid:

* use orchestration for critical workflows with strict business sequence,
* use events for side effects and downstream reactions.

For example, checkout may be orchestrated, while notifications, analytics, fraud monitoring, and search indexing happen asynchronously through events.

---

#### Idempotency

Distributed workflows require **idempotency**.

An operation is idempotent if running it more than once has the same effect as running it once.

This matters because network calls can fail ambiguously.

For example, the Checkout Service may call Payment Service to authorize a payment. The Payment Service may succeed, but the response may time out. The Checkout Service does not know whether the payment happened.

Bad design:

```http
POST /payments/authorize
```

If retried, this might create two authorizations.

Better design:

```http
POST /payments/authorize
Idempotency-Key: checkout_ord_123_authorize
```

Example handler:

```ts
async function authorizePayment(req: Request, res: Response) {
  const idempotencyKey = req.header("Idempotency-Key");

  if (!idempotencyKey) {
    res.status(400).json({
      error: "IDEMPOTENCY_KEY_REQUIRED"
    });
    return;
  }

  const existing = await idempotencyStore.find(idempotencyKey);

  if (existing) {
    res.status(existing.statusCode).json(existing.responseBody);
    return;
  }

  const authorization = await paymentService.authorize(req.body);

  await idempotencyStore.save({
    key: idempotencyKey,
    statusCode: 201,
    responseBody: authorization
  });

  res.status(201).json(authorization);
}
```

Idempotency is essential for safe retries.

---

#### The outbox pattern

A common problem is updating a database and publishing an event atomically.

Suppose the Order Service creates an order and then publishes `OrderCreated`.

Bad version:

```ts
await db.orders.insert(order);
await eventBus.publish("OrderCreated", order);
```

If the database insert succeeds but event publishing fails, the order exists but no one knows about it.

The **Outbox Pattern** solves this by writing the event to the same database transaction as the business change.

```mermaid
flowchart TD
    Service[Order Service]
    DB[(Orders DB)]
    Outbox[(Outbox Table)]
    Publisher[Outbox Publisher]
    Bus[(Event Bus)]

    Service --> DB
    Service --> Outbox

    DB --> Publisher
    Outbox --> Publisher
    Publisher --> Bus
```

Example:

```ts
async function createOrder(db: Database, command: CreateOrderCommand) {
  return db.transaction(async (tx) => {
    const order = await tx.orders.insert({
      customerId: command.customerId,
      status: "PENDING_PAYMENT"
    });

    await tx.outbox.insert({
      eventId: crypto.randomUUID(),
      eventType: "OrderCreated",
      payload: JSON.stringify({
        orderId: order.id,
        customerId: order.customerId
      }),
      published: false,
      createdAt: new Date()
    });

    return order;
  });
}
```

A separate publisher process reads unpublished outbox rows and sends them to the message broker.

This helps preserve consistency between local transactions and emitted events.

---

#### When to use it

Use this pattern when:

* a business process has clear stages,
* each stage has its own local consistency needs,
* a single global transaction would be impractical,
* different steps are owned by different services or teams,
* some steps can complete later,
* compensation is acceptable for some failures,
* workflow state needs to be visible and recoverable,
* you need to decide where strong consistency ends and eventual consistency begins.

Common examples include:

* order placement,
* payment authorization,
* inventory reservation,
* shipment creation,
* hotel or flight booking,
* claims processing,
* loan approval,
* account onboarding,
* subscription activation,
* refund processing,
* identity verification,
* document approval workflows.

---

#### When not to use it

Avoid this pattern when:

* the operation is simple and belongs naturally inside one service,
* all required data is owned by one bounded context,
* strong immediate consistency is mandatory across all changes,
* the business cannot tolerate intermediate states,
* compensation is impossible or legally unacceptable,
* the team lacks the operational maturity to monitor distributed workflows,
* a modular monolith or single-service transaction would be simpler and safer.

For example, updating a customer’s display name probably does not need workflow decomposition. It should usually be a simple local transaction in the Customer or Identity Service.

---

#### Benefits

**1. Makes consistency boundaries explicit**

Teams know which service owns which local transaction.

**2. Reduces reliance on distributed transactions**

Instead of trying to commit across many databases, each service commits its own state.

**3. Improves failure handling**

Workflows can define retries, compensation, timeouts, and recovery steps.

**4. Clarifies ownership**

Each workflow step has a clear service owner.

**5. Improves observability**

Explicit workflow state makes it easier to see where a business process is stuck.

**6. Supports long-running processes**

Some business processes naturally take time. This pattern supports workflows that do not complete in a single request.

**7. Works well with event-driven systems**

Services can communicate progress through domain events.

---

#### Trade-offs

**1. More complex than a single transaction**

You must design for partial success, retries, timeouts, and compensation.

**2. Eventual consistency may confuse users**

A user may see “order pending” while payment or inventory confirmation is still in progress.

**3. Requires idempotency**

Every step may be retried, so commands and event handlers must be safe to run more than once.

**4. Requires observability**

You need logs, metrics, traces, workflow state, and alerts to diagnose stuck processes.

**5. Compensation is not always simple**

Refunding a payment or cancelling a shipment may not perfectly undo the original action.

**6. Workflow logic can become centralized**

In orchestration, the coordinator can become a god service if it owns too much business logic.

**7. Choreography can become hard to understand**

In event-driven workflows, the process can become invisible unless documented and traced well.

---

#### Common mistakes

**Mistake 1: Pretending the workflow is atomic**

A multi-service workflow is not one database transaction. Design for partial completion.

**Mistake 2: Ignoring failure paths**

Every step needs an answer for: What happens if this fails? What happens if the response times out?

**Mistake 3: Forgetting idempotency**

Retries without idempotency can create duplicate payments, duplicate shipments, or duplicate reservations.

**Mistake 4: Mixing workflow ownership with domain ownership**

The orchestrator may coordinate, but the domain service should still own its own business rules.

**Mistake 5: Not storing workflow state**

Without state, recovery and debugging become much harder.

**Mistake 6: Publishing events outside the transaction**

If database updates and event publishing are not coordinated, other services may miss important changes.

**Mistake 7: Making every workflow synchronous**

Long workflows should often return an accepted or pending status instead of blocking the user until every downstream step finishes.

---

#### Practical design checklist

For each workflow, answer these questions:

* What is the business process?
* What are the major workflow steps?
* Which service owns each step?
* What data must be consistent immediately?
* What data can become consistent later?
* What is the local transaction in each service?
* What events or commands connect the steps?
* What happens if each step fails?
* Which actions are retryable?
* Which actions need compensation?
* Are all commands idempotent?
* Are all event handlers idempotent?
* Where is workflow state stored?
* How can operators see stuck workflows?
* What status should users see during partial completion?
* What is the timeout policy?
* What is the manual recovery process?

---

#### Related patterns

| Pattern                   | Relationship                                                                    |
| ------------------------- | ------------------------------------------------------------------------------- |
| Saga                      | Coordinates multi-service workflows through local transactions and compensation |
| Async Messaging           | Allows workflow steps to communicate without blocking                           |
| Event-Driven Architecture | Enables services to publish and react to workflow progress                      |
| CQRS                      | Separates write workflows from read models used by clients                      |
| Event Sourcing            | Stores state changes as events, useful for audit-heavy workflows                |
| Outbox Pattern            | Keeps local database changes and event publishing consistent                    |
| Circuit Breaker           | Prevents repeated calls to failing workflow dependencies                        |
| Retry                     | Handles transient failures in workflow steps                                    |
| Idempotency Key           | Makes retries safe                                                              |
| Decompose by Subdomain    | Helps identify which service owns each workflow step                            |
| Database per Service      | Makes local transaction boundaries explicit                                     |

---

#### Summary

Decomposing by transaction or workflow boundary means designing services around meaningful units of business consistency and business progress.

The central idea is:

> Each service should own a local transaction, while larger workflows are coordinated through explicit steps, events, retries, and compensation.

This pattern is useful when a business process spans multiple services but cannot rely on one global database transaction.

A good workflow design makes clear:

* which service owns each step,
* which state changes are locally consistent,
* where eventual consistency is acceptable,
* what happens when a step fails,
* how retries are handled,
* how compensation works,
* how users and operators can see workflow progress.

The goal is not to make distributed workflows feel like single transactions. The goal is to design them honestly as distributed business processes.

---

### 4. Stateless Services

#### What it is

**Stateless Services** are services that do not store user session state, request-specific state, or business-critical durable state inside a particular running service instance.

A stateless service instance can handle a request without depending on what happened in a previous request to that same instance.

That means this should be safe:

```mermaid
flowchart TD
    Client[Client]
    LB[Load Balancer]

    InstanceA[Service Instance A]
    InstanceB[Service Instance B]
    InstanceC[Service Instance C]

    Client --> LB

    LB --> InstanceA
    LB --> InstanceB
    LB --> InstanceC
```

If the first request goes to Instance A and the next request goes to Instance C, the system should still work.

The key rule is:

> Any healthy instance should be able to handle any valid request.

This does **not** mean the application has no state. Every useful business system has state somewhere. It means state is not stored only in the memory or local disk of one service instance.

Durable state usually belongs in external systems such as:

* relational databases,
* document databases,
* distributed caches,
* message brokers,
* object storage,
* session stores,
* workflow engines,
* event stores.

A stateless service may still use memory for temporary work while processing one request. For example, it can parse JSON, validate input, call another service, and build a response. The important point is that the service should not require future requests to return to the same process.

---

#### Stateful vs stateless service instances

A **stateful service instance** keeps important data locally:

```mermaid
flowchart TD
    Client[Client]
    LB[Load Balancer]

    A[Instance A<br/>Session data in memory]
    B[Instance B<br/>Empty memory]
    C[Instance C<br/>Empty memory]

    Client --> LB
    LB --> A
    LB --> B
    LB --> C
```

If the client logs in through Instance A, Instance A may store the session in memory. Later, if the next request goes to Instance B, Instance B does not know the user is logged in.

That often leads to sticky sessions:

```mermaid
flowchart TD
    Client1[Client 1]
    Client2[Client 2]
    LB[Load Balancer<br/>Sticky Sessions]

    A[Instance A<br/>Client 1 session]
    B[Instance B<br/>Client 2 session]

    Client1 --> LB
    Client2 --> LB

    LB -->|Always route Client 1| A
    LB -->|Always route Client 2| B
```

Sticky sessions can work, but they reduce flexibility. If Instance A fails, Client 1’s session may be lost. If Instance A becomes overloaded, traffic cannot be easily spread.

A **stateless service instance** keeps durable session state outside the instance:

```mermaid
flowchart TD
    Client[Client]
    LB[Load Balancer]

    A[Instance A]
    B[Instance B]
    C[Instance C]

    SessionStore[(External Session Store)]

    Client --> LB

    LB --> A
    LB --> B
    LB --> C

    A --> SessionStore
    B --> SessionStore
    C --> SessionStore
```

Now any instance can handle the request because the session data is stored externally.

---

#### What it solves

Stateless services solve operational problems caused by local instance state.

Without statelessness, the system can suffer from:

* difficult horizontal scaling,
* fragile failover,
* uneven load distribution,
* complicated deployments,
* lost sessions during restarts,
* hard-to-debug behavior,
* poor autoscaling behavior,
* dependence on sticky sessions.

For example, suppose one service instance stores shopping cart state in memory:

```mermaid
flowchart TD
    User[User]
    A[Cart Service Instance A<br/>Cart in memory]
    B[Cart Service Instance B<br/>No cart data]
    C[Cart Service Instance C<br/>No cart data]

    User -->|Add item| A
    User -->|View cart| B
    B --> Missing[Cart appears empty]
```

The user’s cart appears empty because the second request reached a different instance.

A stateless design stores the cart in an external data store:

```mermaid
flowchart TD
    User[User]
    LB[Load Balancer]

    A[Cart Service Instance A]
    B[Cart Service Instance B]
    C[Cart Service Instance C]

    CartStore[(Cart Store)]

    User --> LB
    LB -->|Add item| A
    LB -->|View cart| B

    A --> CartStore
    B --> CartStore
    C --> CartStore
```

Now the cart is independent of any one service instance.

---

#### What “state” means

State can mean several different things.

| Type of state          | Example                                       | Should it live inside one service instance?                |
| ---------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| Request-local state    | Parsed request body, local variables          | Yes, temporarily                                           |
| User session state     | Login session, shopping cart, wizard progress | Usually no                                                 |
| Durable business state | Orders, payments, inventory, invoices         | No                                                         |
| Cache state            | Product cache, auth token cache               | Maybe, but must be disposable                              |
| Workflow state         | Checkout progress, onboarding status          | No                                                         |
| Configuration state    | Feature flags, tenant settings                | No                                                         |
| Connection state       | Open DB connections, HTTP pools               | Yes, but recreatable                                       |
| In-memory locks        | Local mutexes                                 | Only for process-local safety, not distributed correctness |

A stateless service can still use memory. The key distinction is whether losing that memory breaks correctness.

Safe local memory:

```ts
const total = order.items.reduce((sum, item) => {
  return sum + item.quantity * item.unitPrice;
}, 0);
```

Risky local memory:

```ts
const sessions = new Map<string, UserSession>();

sessions.set(sessionId, {
  userId: "user_123",
  expiresAt: Date.now() + 3600_000
});
```

If the process restarts, the session is gone. If the next request goes to another instance, the session is invisible.

---

#### Example: local session state problem

Here is a simple Express example that stores sessions in process memory.

```ts
import express from "express";
import crypto from "crypto";

const app = express();
app.use(express.json());

type Session = {
  userId: string;
  createdAt: string;
};

const sessions = new Map<string, Session>();

app.post("/login", (req, res) => {
  const sessionId = crypto.randomUUID();

  sessions.set(sessionId, {
    userId: req.body.userId,
    createdAt: new Date().toISOString()
  });

  res.json({ sessionId });
});

app.get("/me", (req, res) => {
  const sessionId = req.header("X-Session-Id");

  if (!sessionId) {
    res.status(401).json({ error: "MISSING_SESSION" });
    return;
  }

  const session = sessions.get(sessionId);

  if (!session) {
    res.status(401).json({ error: "INVALID_SESSION" });
    return;
  }

  res.json({ userId: session.userId });
});

app.listen(3000);
```

This works during local development with one process. It fails when there are multiple instances behind a load balancer.

Problems:

* Instance B cannot see sessions created by Instance A.
* Restarting the process deletes all sessions.
* Deployments can log users out.
* Autoscaling creates inconsistent behavior.
* Sticky sessions become necessary.

---

#### Better option: external session store

A better design stores sessions in an external store such as Redis, DynamoDB, PostgreSQL, or another shared system.

```mermaid
flowchart TD
    Client[Client]
    API[API Service]
    SessionStore[(Session Store)]

    Client --> API
    API --> SessionStore
```

Example using a Redis-like interface:

```ts
import express from "express";
import crypto from "crypto";

const app = express();
app.use(express.json());

type RedisClient = {
  setEx(key: string, seconds: number, value: string): Promise<void>;
  get(key: string): Promise<string | null>;
};

const redis: RedisClient = getRedisClient();

type Session = {
  userId: string;
  createdAt: string;
};

app.post("/login", async (req, res) => {
  const sessionId = crypto.randomUUID();

  const session: Session = {
    userId: req.body.userId,
    createdAt: new Date().toISOString()
  };

  await redis.setEx(
    `session:${sessionId}`,
    3600,
    JSON.stringify(session)
  );

  res.json({ sessionId });
});

app.get("/me", async (req, res) => {
  const sessionId = req.header("X-Session-Id");

  if (!sessionId) {
    res.status(401).json({ error: "MISSING_SESSION" });
    return;
  }

  const rawSession = await redis.get(`session:${sessionId}`);

  if (!rawSession) {
    res.status(401).json({ error: "INVALID_SESSION" });
    return;
  }

  const session = JSON.parse(rawSession) as Session;

  res.json({ userId: session.userId });
});

app.listen(3000);
```

Now any service instance can validate the session.

The service instances remain stateless because the session is not tied to a specific process.

---

#### Another option: token-based authentication

Many APIs avoid server-side session storage by using signed tokens, such as JWTs or opaque tokens validated by an identity service.

With a signed token, the service can verify the request without storing session data locally.

```mermaid
flowchart TD
    Client[Client]
    Auth[Identity Service]
    API[API Service]

    Client -->|Login| Auth
    Auth -->|Signed token| Client
    Client -->|Request with token| API
    API -->|Verify signature or introspect token| API
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

Simplified middleware:

```ts
import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

type AuthenticatedRequest = Request & {
  user?: {
    userId: string;
    roles: string[];
  };
};

function authenticate(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
) {
  const authorization = req.header("Authorization");

  if (!authorization?.startsWith("Bearer ")) {
    res.status(401).json({ error: "MISSING_TOKEN" });
    return;
  }

  const token = authorization.slice("Bearer ".length);

  try {
    const payload = jwt.verify(token, process.env.JWT_PUBLIC_KEY!) as {
      sub: string;
      roles?: string[];
    };

    req.user = {
      userId: payload.sub,
      roles: payload.roles ?? []
    };

    next();
  } catch {
    res.status(401).json({ error: "INVALID_TOKEN" });
  }
}
```

Token-based authentication can reduce dependency on a central session store, but it has trade-offs.

| Approach                        | Strengths                                                | Trade-offs                                      |
| ------------------------------- | -------------------------------------------------------- | ----------------------------------------------- |
| Server-side session store       | Easy revocation, small client token, centralized control | Requires highly available session store         |
| Signed token                    | Fewer storage lookups, works well for APIs               | Revocation and permission changes can be harder |
| Opaque token with introspection | Centralized validation, easier revocation                | Adds dependency on identity service or cache    |

A stateless service can use any of these approaches as long as it does not require local instance memory for correctness.

---

#### Durable business state

Stateless services should not store durable business state on local disk or in process memory.

Bad example:

```ts
const orders = new Map<string, Order>();

app.post("/orders", (req, res) => {
  const order = createOrder(req.body);
  orders.set(order.id, order);
  res.status(201).json(order);
});
```

This loses orders when the process restarts.

A better design stores orders in a durable database:

```mermaid
flowchart TD
    Client[Client]
    OrderService[Order Service]
    OrdersDB[(Orders Database)]

    Client --> OrderService
    OrderService --> OrdersDB
```

Example:

```ts
app.post("/orders", async (req, res) => {
  const order = await orderRepository.create({
    customerId: req.body.customerId,
    items: req.body.items,
    status: "PENDING_PAYMENT"
  });

  res.status(201).json(order);
});
```

The service instance can be replaced at any time because the order data lives outside the process.

---

#### Horizontal scaling

Stateless services are much easier to scale horizontally.

If traffic increases, the platform can add more instances:

```mermaid
flowchart TD
    Traffic[Incoming Traffic]
    LB[Load Balancer]

    A[API Instance A]
    B[API Instance B]
    C[API Instance C]
    D[API Instance D]
    E[API Instance E]

    DB[(External State Store)]

    Traffic --> LB

    LB --> A
    LB --> B
    LB --> C
    LB --> D
    LB --> E

    A --> DB
    B --> DB
    C --> DB
    D --> DB
    E --> DB
```

In Kubernetes, this maps naturally to replicas behind a Service:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orders-api
  template:
    metadata:
      labels:
        app: orders-api
    spec:
      containers:
        - name: orders-api
          image: example/orders-api:1.0.0
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: orders-db
                  key: url
```

Scaling the service becomes mostly a matter of adding replicas.

```bash
kubectl scale deployment orders-api --replicas=10
```

This works because no replica owns unique local state.

---

#### Failover and replacement

Stateless services are easier to restart, replace, and move.

If one instance fails, traffic can move to another instance:

```mermaid
flowchart TD
    Client[Client]
    LB[Load Balancer]

    A[Instance A<br/>Failed]
    B[Instance B<br/>Healthy]
    C[Instance C<br/>Healthy]

    Store[(External State Store)]

    Client --> LB
    LB -. no traffic .-> A
    LB --> B
    LB --> C

    B --> Store
    C --> Store
```

This is important for:

* rolling deployments,
* autoscaling,
* node failures,
* container restarts,
* blue-green deployments,
* canary releases,
* Kubernetes rescheduling.

A stateless instance should be disposable.

A useful test is:

> If this container is killed right now, does the system lose business-critical data?

For a properly stateless API service, the answer should be no.

---

#### Stateless does not mean no caching

Stateless services can use local caches, but local caches must be treated as disposable.

Acceptable local cache:

```ts
const productCache = new Map<string, CachedProduct>();

async function getProduct(productId: string): Promise<Product> {
  const cached = productCache.get(productId);

  if (cached && cached.expiresAt > Date.now()) {
    return cached.product;
  }

  const product = await catalogClient.getProduct(productId);

  productCache.set(productId, {
    product,
    expiresAt: Date.now() + 60_000
  });

  return product;
}
```

This is okay if losing the cache only hurts performance, not correctness.

Risky local cache:

```ts
const usedCouponCodes = new Set<string>();

function redeemCoupon(code: string) {
  if (usedCouponCodes.has(code)) {
    throw new Error("coupon already used");
  }

  usedCouponCodes.add(code);
}
```

This is not safe because another instance will not know the coupon was used. Coupon redemption must be stored in a shared durable store or enforced by a database constraint.

Rule of thumb:

> Local memory can be used for performance, but not as the source of truth.

---

#### Stateless services and background jobs

Statelessness also matters for workers and background processors.

A worker should not rely on local memory to remember which jobs were processed. Instead, durable state should live in a queue, database, or workflow engine.

```mermaid
flowchart TD
    Queue[(Message Queue)]
    WorkerA[Worker A]
    WorkerB[Worker B]
    WorkerC[Worker C]
    DB[(Database)]

    Queue --> WorkerA
    Queue --> WorkerB
    Queue --> WorkerC

    WorkerA --> DB
    WorkerB --> DB
    WorkerC --> DB
```

If Worker A crashes while processing a job, the queue should eventually make the job available again or move it to a dead-letter queue.

A worker should be designed for:

* retries,
* idempotency,
* duplicate messages,
* timeouts,
* dead-letter handling,
* safe shutdown.

Example idempotent job handler:

```ts
async function handlePaymentCaptured(event: PaymentCapturedEvent) {
  const existing = await db.processedEvents.findById(event.eventId);

  if (existing) {
    return;
  }

  await db.transaction(async (tx) => {
    await tx.orders.markAsPaid(event.orderId);
    await tx.processedEvents.insert({
      eventId: event.eventId,
      processedAt: new Date()
    });
  });
}
```

The worker can crash and restart because the processing state is persisted.

---

#### Configuration and environment

Stateless services should not require manual local configuration that differs between instances.

Configuration should come from external sources such as:

* environment variables,
* Kubernetes ConfigMaps,
* Kubernetes Secrets,
* service discovery,
* external configuration services,
* feature flag systems.

Example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: orders-api-config
data:
  LOG_LEVEL: "info"
  PAYMENT_SERVICE_URL: "http://payments-service"
  INVENTORY_SERVICE_URL: "http://inventory-service"
```

And secrets:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: orders-api-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgres://orders_user:password@orders-db/orders"
```

The same container image can run in different environments by changing configuration outside the image.

This supports:

* repeatable deployments,
* immutable infrastructure,
* easier rollback,
* safer scaling,
* environment-specific configuration.

---

#### Readiness and graceful shutdown

Stateless services still need careful lifecycle behavior.

In Kubernetes or any orchestrated environment, a service should expose health endpoints.

```http
GET /health/live
GET /health/ready
```

Example:

```ts
app.get("/health/live", (_req, res) => {
  res.status(200).json({ status: "alive" });
});

app.get("/health/ready", async (_req, res) => {
  const dbHealthy = await database.ping();
  const cacheHealthy = await cache.ping();

  if (!dbHealthy || !cacheHealthy) {
    res.status(503).json({
      status: "not_ready",
      dependencies: {
        database: dbHealthy,
        cache: cacheHealthy
      }
    });
    return;
  }

  res.status(200).json({ status: "ready" });
});
```

During shutdown, the service should stop accepting new work and finish in-flight requests if possible.

```ts
const server = app.listen(3000);

process.on("SIGTERM", () => {
  console.log("Received SIGTERM, shutting down gracefully");

  server.close(() => {
    console.log("HTTP server closed");
    process.exit(0);
  });

  setTimeout(() => {
    console.error("Forced shutdown after timeout");
    process.exit(1);
  }, 30_000);
});
```

Stateless does not mean careless. It means instances can be safely replaced because important state is externalized.

---

#### External state store design

Moving state out of the service instance does not make state problems disappear. It moves them into external systems that must be designed properly.

For each external state store, consider:

| Concern         | Questions to ask                                      |
| --------------- | ----------------------------------------------------- |
| Availability    | What happens if the store is unavailable?             |
| Latency         | Can the service tolerate the lookup on every request? |
| Consistency     | Do reads need to be strongly consistent?              |
| Durability      | Can this data be lost?                                |
| Security        | Is the state encrypted and access-controlled?         |
| Scaling         | Can the store handle peak traffic?                    |
| Expiration      | Should the data have a TTL?                           |
| Recovery        | How is data backed up and restored?                   |
| Region strategy | Is state local to one region or replicated globally?  |

For example, an external session store must be highly available because many requests may depend on it. A product cache can be less durable because the source of truth is elsewhere.

---

#### Common external state locations

| State                       | Common location                                          |
| --------------------------- | -------------------------------------------------------- |
| User sessions               | Redis, DynamoDB, database, identity provider             |
| Shopping carts              | Redis, document DB, relational DB                        |
| Orders                      | Relational DB, document DB                               |
| Payments                    | Relational DB with strong auditability                   |
| Files                       | Object storage                                           |
| Long-running workflow state | Workflow engine, database                                |
| Events                      | Kafka, Pulsar, event store                               |
| Cached reads                | Redis, CDN, in-memory cache                              |
| Feature flags               | Feature flag platform                                    |
| Configuration               | Environment, config service, Kubernetes ConfigMap/Secret |

The right store depends on consistency, durability, latency, and operational needs.

---

#### Sticky sessions

Sticky sessions route the same client to the same service instance.

```mermaid
flowchart TD
    Client[Client]
    LB[Load Balancer<br/>Sticky Session]
    A[Instance A<br/>User session]
    B[Instance B]
    C[Instance C]

    Client --> LB
    LB -->|Same client each time| A
```

Sticky sessions can be useful as a temporary compatibility mechanism, but they are usually not ideal for cloud-native services.

Problems with sticky sessions:

* traffic may become uneven,
* failed instances lose local sessions,
* deployments become harder,
* autoscaling is less effective,
* clients may be tied to unhealthy instances,
* multi-region routing becomes harder.

If sticky sessions are required, ask why. Often the answer is that state has not been externalized.

---

#### Idempotency and statelessness

Stateless services often rely on retries. Retries require idempotency.

For example, a client may send the same `POST /orders` request twice because the first response timed out.

If the service is stateless, it cannot rely on local memory to remember that the request already happened. It should use an external idempotency store or a database constraint.

```http
POST /orders
Idempotency-Key: checkout_123_create_order
```

Example:

```ts
async function createOrderWithIdempotency(req: Request, res: Response) {
  const key = req.header("Idempotency-Key");

  if (!key) {
    res.status(400).json({ error: "IDEMPOTENCY_KEY_REQUIRED" });
    return;
  }

  const existing = await idempotencyRepository.findByKey(key);

  if (existing) {
    res.status(existing.statusCode).json(existing.responseBody);
    return;
  }

  const order = await orderRepository.create(req.body);

  await idempotencyRepository.save({
    key,
    statusCode: 201,
    responseBody: order
  });

  res.status(201).json(order);
}
```

This allows the service to remain stateless while still handling duplicate requests safely.

---

#### When to use it

Use stateless services for:

* public APIs,
* internal APIs,
* Kubernetes workloads,
* services behind load balancers,
* horizontally scalable services,
* autoscaled services,
* cloud-native applications,
* request/response microservices,
* worker fleets,
* systems that need fast failover,
* systems that need rolling deployments or blue-green deployments.

This pattern is especially important when instances are ephemeral, meaning they can be started, stopped, replaced, or rescheduled at any time.

---

#### When not to use it

Some systems are naturally stateful.

Examples include:

* databases,
* distributed caches,
* message brokers,
* stream processors,
* search clusters,
* workflow engines,
* game servers with real-time session state,
* WebSocket gateways with active connections,
* machine learning model servers with large loaded models,
* systems that require local durable storage.

Even then, the design should be intentional. Stateful systems need different operational patterns:

* stable identity,
* persistent volumes,
* leader election,
* replication,
* partitioning,
* backup and restore,
* careful rolling upgrades,
* data recovery plans.

A stateful component is not bad. It just requires more careful operational design.

---

#### Benefits

**1. Easier horizontal scaling**

More instances can be added without moving local user state.

**2. Better failover**

If one instance dies, another instance can continue handling requests.

**3. Simpler deployments**

Rolling deployments can replace instances without losing sessions or business data.

**4. Better load balancing**

Requests can be distributed across healthy instances without sticky routing.

**5. Easier autoscaling**

The platform can add or remove instances based on traffic.

**6. Better resource isolation**

Individual instances become disposable units of compute.

**7. Cloud-native compatibility**

Stateless services fit naturally with containers, Kubernetes, serverless platforms, and immutable infrastructure.

---

#### Trade-offs

**1. State still has to live somewhere**

Externalizing state does not remove the need to design state. It moves responsibility to databases, caches, queues, or identity providers.

**2. External stores can become bottlenecks**

A session store or cache can become a central dependency that limits scalability.

**3. Latency may increase**

Reading state from an external system may be slower than reading memory.

**4. Availability depends on dependencies**

If the external state store is down, the stateless service may also be unable to serve requests.

**5. Consistency becomes a design question**

Different stores provide different consistency guarantees.

**6. Security becomes more important**

External state stores may contain sensitive session, user, or business data.

**7. More infrastructure is required**

A stateless service may require databases, caches, queues, secrets management, and observability to work safely.

---

#### Common mistakes

**Mistake 1: Storing sessions in process memory**

This breaks horizontal scaling and failover.

**Mistake 2: Storing business data in local files**

Containers and service instances are often ephemeral. Local disk may disappear when the instance is rescheduled.

**Mistake 3: Relying on sticky sessions as the main solution**

Sticky sessions hide the problem rather than solving it.

**Mistake 4: Treating local cache as source of truth**

Local cache must be disposable.

**Mistake 5: Ignoring idempotency**

Stateless services often retry operations. Without idempotency, retries can create duplicate side effects.

**Mistake 6: Externalizing state without designing the store**

A poorly designed external session store can become the new single point of failure.

**Mistake 7: Assuming stateless means no lifecycle handling**

Services still need health checks, graceful shutdown, timeouts, and dependency checks.

---

#### Practical design checklist

A service is likely stateless if:

* any instance can handle any request,
* user sessions are stored externally or represented by verifiable tokens,
* business data is stored in durable external systems,
* local memory is used only for temporary or disposable data,
* local caches can be lost without correctness issues,
* the service does not require sticky sessions,
* instances can be restarted without losing important data,
* deployments can replace instances safely,
* idempotency is handled through durable storage or constraints,
* configuration comes from external environment or config systems.

A service is probably stateful if:

* users must return to the same instance,
* sessions are stored in memory,
* business data is written to local disk,
* local cache is required for correctness,
* the service cannot be restarted safely,
* scaling requires moving local state,
* failover loses user progress or business data.

---

#### Related patterns

| Pattern                | Relationship                                            |
| ---------------------- | ------------------------------------------------------- |
| External Configuration | Keeps settings outside the service image                |
| Database per Service   | Stores durable business state outside service instances |
| Service Discovery      | Helps route to healthy stateless instances              |
| Health Check           | Allows load balancers to remove unhealthy instances     |
| Circuit Breaker        | Protects stateless services from failing dependencies   |
| Retry                  | Commonly used when requests can be safely retried       |
| Idempotency Key        | Makes retries safe for state-changing operations        |
| API Gateway            | Routes requests across stateless backend services       |
| Load Balancing         | Distributes traffic across interchangeable instances    |
| Blue-Green Deployment  | Easier when instances are stateless and replaceable     |
| Outbox Pattern         | Keeps state changes and event publishing consistent     |

---

#### Summary

Stateless Services avoid storing durable or request-dependent state inside one specific service instance.

The central idea is:

> Any healthy instance should be able to handle any valid request.

This makes services easier to scale, restart, replace, deploy, and fail over.

Stateless does not mean the system has no state. It means important state is externalized into systems designed to store it safely, such as databases, caches, queues, identity providers, or workflow stores.

A good stateless service should be disposable. If an instance can be killed and replaced without losing business-critical data or user session correctness, the design is likely on the right track.


---

## 2. Legacy Migration and Boundary Protection Patterns

These patterns help modernize legacy systems and integrate with external systems without polluting the new architecture.

### 5. Strangler Fig Pattern

#### What it is

The **Strangler Fig Pattern** is a legacy modernization pattern where a new system gradually grows around an old system until the old system can be safely retired.

The name comes from the strangler fig tree, which grows around an existing tree over time. In software, the new architecture slowly surrounds and replaces parts of the legacy system.

Instead of rewriting the whole system at once, you replace one capability, workflow, API, or route at a time.

```mermaid
flowchart TD
    Client[Client Applications]
    Router[Router / API Gateway]

    Legacy[Legacy Monolith]
    NewA[New Service A]
    NewB[New Service B]

    Client --> Router

    Router -->|Unmigrated routes| Legacy
    Router -->|Migrated capability A| NewA
    Router -->|Migrated capability B| NewB
```

At the beginning, almost all traffic goes to the legacy system.

```mermaid
flowchart TD
    Client[Client]
    Router[Router]

    Legacy[Legacy System]
    New[New System]

    Client --> Router
    Router -->|95 percent traffic| Legacy
    Router -->|5 percent traffic| New
```

Over time, more functionality moves to the new system.

```mermaid
flowchart TD
    Client[Client]
    Router[Router]

    Legacy[Legacy System]
    New[New System]

    Client --> Router
    Router -->|40 percent traffic| Legacy
    Router -->|60 percent traffic| New
```

Eventually, the legacy system receives no traffic and can be retired.

```mermaid
flowchart TD
    Client[Client]
    Router[Router]

    New[New System]
    Retired[Legacy System Retired]

    Client --> Router
    Router --> New
    Retired -. removed .-> Router
```

The central idea is:

> Replace the legacy system gradually by intercepting and redirecting specific functionality to the new system.

---

#### Why this pattern exists

Large rewrites are risky.

A big-bang rewrite usually tries to replace the entire legacy system in one major release:

```mermaid
flowchart TD
    Old[Legacy System]
    Rewrite[Full Rewrite Project]
    New[New System]

    Old --> Rewrite
    Rewrite --> New

    Risk[Big cutover risk]
    Rewrite --> Risk
```

This often fails because:

* the legacy system contains years of hidden behavior,
* documentation is incomplete,
* business rules are embedded in old code,
* edge cases are discovered late,
* the new system takes too long to deliver value,
* teams underestimate data migration complexity,
* clients depend on undocumented behavior,
* the business cannot stop while engineering rewrites everything.

The Strangler Fig Pattern avoids this by making modernization incremental.

Instead of replacing everything at once, you choose one slice, build its replacement, route traffic to it, validate it, and repeat.

```mermaid
flowchart TD
    Step1[Choose a small capability]
    Step2[Build replacement]
    Step3[Route limited traffic]
    Step4[Validate behavior]
    Step5[Increase traffic]
    Step6[Retire legacy slice]

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
    Step5 --> Step6
```

This lets teams learn from production behavior while reducing blast radius.

---

#### What it solves

The pattern solves the risk of **big-bang legacy replacement**.

A legacy monolith may contain many capabilities:

```mermaid
flowchart TD
    Legacy[Legacy Monolith]

    Legacy --> Auth[Authentication]
    Legacy --> Catalog[Catalog]
    Legacy --> Orders[Orders]
    Legacy --> Payments[Payments]
    Legacy --> Inventory[Inventory]
    Legacy --> Shipping[Shipping]
    Legacy --> Reporting[Reporting]
```

Trying to replace all of these at once is dangerous. The Strangler Fig Pattern replaces one area at a time.

```mermaid
flowchart TD
    Legacy[Legacy Monolith]

    Legacy --> Auth[Authentication]
    Legacy --> Catalog[Catalog]
    Legacy --> Orders[Orders]
    Legacy --> Payments[Payments]
    Legacy --> Inventory[Inventory]
    Legacy --> Shipping[Shipping]
    Legacy --> Reporting[Reporting]

    NewCatalog[New Catalog Service]
    NewOrders[New Order Service]

    Catalog -. replaced by .-> NewCatalog
    Orders -. replaced by .-> NewOrders
```

This creates a controlled migration path.

The old system keeps running while the new system gradually takes ownership of selected functionality.

---

#### Basic architecture

A Strangler Fig migration usually needs a routing layer in front of the legacy system.

That routing layer may be:

* an API gateway,
* a reverse proxy,
* a load balancer,
* a service mesh,
* an edge function,
* a facade service,
* an application-level routing module.

```mermaid
flowchart TD
    Clients[Clients]
    Gateway[Gateway / Facade / Proxy]

    Legacy[Legacy System]
    NewOrders[New Order Service]
    NewCatalog[New Catalog Service]
    NewPayments[New Payment Service]

    Clients --> Gateway

    Gateway -->|/legacy/*| Legacy
    Gateway -->|/orders/*| NewOrders
    Gateway -->|/catalog/*| NewCatalog
    Gateway -->|/payments/*| NewPayments
```

The gateway decides whether a request should go to the legacy system or to the new system.

For example:

| Route                      | Destination         |
| -------------------------- | ------------------- |
| `GET /products/{id}`       | New Catalog Service |
| `POST /orders`             | New Order Service   |
| `GET /customers/{id}`      | Legacy System       |
| `POST /payments/authorize` | New Payment Service |
| `GET /reports/daily-sales` | Legacy System       |

The route table changes gradually as functionality is migrated.

---

#### Example: route-based migration

Suppose the legacy system exposes these routes:

```http
GET /products/{productId}
GET /products/search
POST /orders
GET /orders/{orderId}
POST /payments/authorize
GET /customers/{customerId}
```

You might first migrate product reads to a new Catalog Service.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Legacy[Legacy Monolith]
    Catalog[Catalog Service]

    Client --> Gateway

    Gateway -->|GET /products/*| Catalog
    Gateway -->|Everything else| Legacy
```

Example NGINX-style routing:

```nginx
location /products/ {
    proxy_pass http://catalog-service;
}

location / {
    proxy_pass http://legacy-monolith;
}
```

Later, you might migrate orders:

```nginx
location /products/ {
    proxy_pass http://catalog-service;
}

location /orders/ {
    proxy_pass http://order-service;
}

location / {
    proxy_pass http://legacy-monolith;
}
```

Then payments:

```nginx
location /products/ {
    proxy_pass http://catalog-service;
}

location /orders/ {
    proxy_pass http://order-service;
}

location /payments/ {
    proxy_pass http://payment-service;
}

location / {
    proxy_pass http://legacy-monolith;
}
```

This is the simplest form of strangling: route by endpoint.

---

#### Example: feature-based migration

Sometimes route-based migration is too coarse.

You may want only some users, tenants, regions, or feature flags to use the new system.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[Gateway]

    Decision{Use new implementation?}

    Legacy[Legacy System]
    New[New Service]

    Request --> Gateway
    Gateway --> Decision

    Decision -->|No| Legacy
    Decision -->|Yes| New
```

Routing decisions can be based on:

* user ID,
* tenant ID,
* region,
* product type,
* feature flag,
* request header,
* client version,
* percentage rollout,
* internal beta group.

Example pseudo-code:

```ts
function routeOrderRequest(req: Request): Target {
  const tenantId = req.header("X-Tenant-Id");
  const userId = req.header("X-User-Id");

  if (featureFlags.isEnabled("new-order-service", { tenantId, userId })) {
    return {
      service: "order-service",
      baseUrl: "http://orders-service"
    };
  }

  return {
    service: "legacy-monolith",
    baseUrl: "http://legacy-monolith"
  };
}
```

Feature-based migration is useful when you want a controlled rollout:

```mermaid
flowchart TD
    Users[Users]

    Users --> Internal[Internal users]
    Users --> Beta[Beta customers]
    Users --> Region[One region]
    Users --> All[All users]

    Internal --> Step1[Route to new service]
    Beta --> Step2[Expand rollout]
    Region --> Step3[Validate at scale]
    All --> Step4[Complete migration]
```

---

#### Example: API facade

Sometimes old clients must keep using the same API contract even while the backend changes.

In that case, add a facade.

```mermaid
flowchart TD
    Client[Existing Client]
    Facade[Compatibility Facade]

    Legacy[Legacy System]
    NewService[New Service]

    Client --> Facade

    Facade -->|Old contract requests| Legacy
    Facade -->|Translated requests| NewService
```

The facade preserves the old external API while translating selected operations to the new system.

Example:

```ts
app.get("/api/v1/products/:id", async (req, res) => {
  if (await shouldUseNewCatalog(req.params.id)) {
    const product = await catalogClient.getProduct(req.params.id);

    res.json({
      id: product.productId,
      name: product.title,
      description: product.description,
      price: product.currentPrice.amount
    });

    return;
  }

  const legacyProduct = await legacyClient.getProduct(req.params.id);
  res.json(legacyProduct);
});
```

This lets clients migrate later. The backend can evolve first.

The trade-off is that the facade can become complex if it accumulates too much translation logic.

---

#### Data migration strategies

The hardest part of strangling a legacy system is often not routing. It is data.

Legacy and new systems may need access to overlapping data during the migration.

There are several common strategies.

---

##### Strategy 1: New service reads legacy database temporarily

The new service may temporarily read from the legacy database.

```mermaid
flowchart TD
    NewService[New Service]
    LegacyDB[(Legacy Database)]

    NewService --> LegacyDB
```

This can speed up migration, but it creates coupling.

Use this only as a temporary step. The new service is not truly independent while it depends on the legacy schema.

Risks:

* legacy schema changes can break the new service,
* new service inherits legacy data quality problems,
* business rules may be bypassed,
* database load increases,
* ownership remains unclear.

---

##### Strategy 2: New service owns new data only

The new service handles new records, while old records remain in the legacy system.

```mermaid
flowchart TD
    Gateway[Gateway]

    Legacy[Legacy System]
    NewService[New Service]

    LegacyDB[(Legacy DB)]
    NewDB[(New DB)]

    Gateway -->|Old records| Legacy
    Gateway -->|New records| NewService

    Legacy --> LegacyDB
    NewService --> NewDB
```

This works well when records have a natural cutover point.

Examples:

* new orders go to the new Order Service,
* old orders remain in the legacy system,
* new customers use the new onboarding system,
* existing customers remain in legacy until migrated.

Routing may depend on record creation date, ID format, tenant, or migration status.

---

##### Strategy 3: Replicate legacy data into the new system

The new service may maintain a copy of legacy data.

```mermaid
flowchart TD
    Legacy[Legacy System]
    LegacyDB[(Legacy DB)]

    Replicator[Data Replication / CDC]

    NewDB[(New Service DB)]
    NewService[New Service]

    Legacy --> LegacyDB
    LegacyDB --> Replicator
    Replicator --> NewDB
    NewService --> NewDB
```

This can be done with:

* change data capture,
* database triggers,
* event streams,
* scheduled batch jobs,
* ETL pipelines,
* dual publishing from the legacy system.

This is useful when the new service needs fast reads without depending directly on the legacy database.

---

##### Strategy 4: Dual-write during transition

Both legacy and new systems may be written during migration.

```mermaid
flowchart TD
    Writer[Write Request]

    Writer --> Legacy[Legacy System]
    Writer --> New[New System]

    Legacy --> LegacyDB[(Legacy DB)]
    New --> NewDB[(New DB)]
```

This is risky because one write may succeed and the other may fail.

If dual-write is unavoidable, use safeguards:

* idempotency keys,
* retry queues,
* reconciliation jobs,
* outbox pattern,
* clear source-of-truth rules,
* monitoring for divergence,
* manual repair tools.

A safer approach is usually to write to one source of truth and propagate changes asynchronously.

---

##### Strategy 5: New system becomes source of truth

At the end of migration, the new service owns the data.

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway]
    NewService[New Service]
    NewDB[(New DB)]

    Client --> Gateway
    Gateway --> NewService
    NewService --> NewDB

    Legacy[Legacy System]
    Legacy -. retired .-> Gateway
```

This is the target state. The legacy system no longer owns that capability or its data.

---

#### Source of truth during migration

A strangler migration must define source of truth clearly.

For every capability being migrated, ask:

| Question                                  | Example answer                                      |
| ----------------------------------------- | --------------------------------------------------- |
| Who owns reads today?                     | Legacy System                                       |
| Who owns writes today?                    | Legacy System                                       |
| Who owns reads during migration?          | New Service for migrated tenants, Legacy for others |
| Who owns writes during migration?         | New Service                                         |
| How is old data migrated?                 | CDC plus backfill                                   |
| When is legacy no longer source of truth? | After reconciliation passes for 30 days             |
| How is divergence detected?               | Daily comparison job                                |
| How is rollback handled?                  | Route traffic back to legacy for unmigrated records |

Without clear ownership, the system can end up with inconsistent data and unclear operational responsibility.

---

#### Anti-corruption layer

A new system should not blindly copy the legacy system’s model.

Legacy systems often contain old naming, outdated assumptions, overloaded fields, and technical constraints.

An **Anti-Corruption Layer** protects the new model by translating between legacy concepts and new concepts.

```mermaid
flowchart TD
    NewService[New Service]
    ACL[Anti-Corruption Layer]
    Legacy[Legacy System]

    NewService --> ACL
    ACL --> Legacy

    ACL --> Translate[Translate legacy model<br/>into new domain model]
```

Example:

```ts
type LegacyCustomer = {
  cust_no: string;
  stat: "A" | "I" | "S";
  bill_addr_1: string;
  bill_addr_2?: string;
};

type Customer = {
  customerId: string;
  status: "ACTIVE" | "INACTIVE" | "SUSPENDED";
  billingAddress: {
    line1: string;
    line2?: string;
  };
};

function mapLegacyCustomer(legacy: LegacyCustomer): Customer {
  return {
    customerId: legacy.cust_no,
    status: mapStatus(legacy.stat),
    billingAddress: {
      line1: legacy.bill_addr_1,
      line2: legacy.bill_addr_2
    }
  };
}

function mapStatus(status: LegacyCustomer["stat"]): Customer["status"] {
  switch (status) {
    case "A":
      return "ACTIVE";
    case "I":
      return "INACTIVE";
    case "S":
      return "SUSPENDED";
  }
}
```

This translation prevents old concepts from leaking into the new service.

---

#### Migration phases

A typical Strangler Fig migration happens in phases.

```mermaid
flowchart TD
    Phase1[1. Understand legacy behavior]
    Phase2[2. Add routing layer]
    Phase3[3. Choose first migration slice]
    Phase4[4. Build new implementation]
    Phase5[5. Run in parallel or shadow mode]
    Phase6[6. Route limited traffic]
    Phase7[7. Expand traffic]
    Phase8[8. Retire legacy slice]
    Phase9[9. Repeat]

    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Phase5
    Phase5 --> Phase6
    Phase6 --> Phase7
    Phase7 --> Phase8
    Phase8 --> Phase9
```

Each phase reduces risk.

---

##### Phase 1: Understand legacy behavior

Before replacing anything, observe the legacy system.

Useful activities:

* map routes and APIs,
* identify database tables,
* capture production traffic,
* document business rules,
* interview domain experts,
* identify high-risk workflows,
* inspect logs and reports,
* find undocumented client behavior,
* write characterization tests.

A **characterization test** captures how the old system behaves today, even if the behavior is strange.

Example:

```ts
describe("legacy discount behavior", () => {
  it("applies VIP discount before seasonal discount", async () => {
    const result = await legacyClient.calculatePrice({
      customerType: "VIP",
      productId: "prod_123",
      basePrice: 100,
      seasonalDiscount: 10
    });

    expect(result.finalPrice).toBe(80);
  });
});
```

The goal is not to prove the legacy system is elegant. The goal is to avoid accidentally breaking behavior the business relies on.

---

##### Phase 2: Add a routing layer

Introduce a routing layer that can send traffic to either the legacy or new system.

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway]

    Legacy[Legacy System]
    New[New System]

    Client --> Gateway
    Gateway --> Legacy
    Gateway -. future route .-> New
```

At first, the gateway may route everything to legacy. This creates the control point needed for future migration.

---

##### Phase 3: Choose the first migration slice

Start with a slice that is valuable but not too risky.

Good first candidates:

* read-only endpoints,
* internal admin features,
* low-traffic routes,
* isolated workflows,
* one tenant,
* one region,
* one product category,
* non-critical background jobs.

Bad first candidates:

* payment settlement,
* mission-critical writes,
* workflows with many unknown dependencies,
* high-traffic endpoints without observability,
* areas with unclear business ownership.

---

##### Phase 4: Build the new implementation

Build the replacement with modern architecture, but avoid overbuilding.

The new slice should have:

* clear ownership,
* tests,
* monitoring,
* API compatibility or translation,
* data migration plan,
* rollback plan,
* source-of-truth decision,
* operational runbook.

---

##### Phase 5: Run in shadow mode

Before serving real responses, the new system can receive copied traffic.

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway]

    Legacy[Legacy System]
    New[New System]

    Compare[Compare Results]

    Client --> Gateway
    Gateway -->|Primary response| Legacy
    Gateway -. shadow traffic .-> New

    Legacy --> Compare
    New --> Compare
```

The legacy system still serves users. The new system processes the same requests in the background. Differences are logged and analyzed.

This helps validate the new implementation with real production traffic.

---

##### Phase 6: Route limited traffic

Once shadow testing looks good, route a small amount of real traffic to the new system.

```mermaid
flowchart TD
    Requests[Requests]
    Router[Router]

    Legacy[Legacy System]
    New[New System]

    Requests --> Router

    Router -->|Most traffic| Legacy
    Router -->|Small rollout| New
```

Start with low-risk traffic:

* internal users,
* test tenants,
* beta customers,
* one region,
* one percent rollout.

---

##### Phase 7: Expand traffic

Increase traffic gradually while monitoring:

* error rates,
* latency,
* database load,
* user complaints,
* business metrics,
* data divergence,
* downstream failures,
* support tickets.

```mermaid
flowchart TD
    Internal[Internal users]
    OnePercent[1 percent]
    TenPercent[10 percent]
    FiftyPercent[50 percent]
    All[100 percent]

    Internal --> OnePercent
    OnePercent --> TenPercent
    TenPercent --> FiftyPercent
    FiftyPercent --> All
```

At each stage, compare the new system against expected behavior.

---

##### Phase 8: Retire the legacy slice

After the new system has fully taken over a capability, remove the old path.

Retirement should include:

* disabling old routes,
* removing old jobs,
* archiving or deleting old code,
* removing unused tables,
* updating documentation,
* removing temporary sync logic,
* shutting down unused infrastructure,
* updating operational ownership.

A migration is not complete until the old path is gone.

---

#### Example: migrating product catalog

Suppose a retail monolith owns product catalog, search, orders, and payments.

You decide to migrate catalog first.

Initial state:

```mermaid
flowchart TD
    Client[Client]
    Monolith[Retail Monolith]
    LegacyDB[(Legacy DB)]

    Client --> Monolith
    Monolith --> LegacyDB
```

Step 1: Add gateway.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Monolith[Retail Monolith]
    LegacyDB[(Legacy DB)]

    Client --> Gateway
    Gateway --> Monolith
    Monolith --> LegacyDB
```

Step 2: Add Catalog Service with replicated product data.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Monolith[Retail Monolith]
    LegacyDB[(Legacy DB)]

    CDC[Change Data Capture]
    CatalogDB[(Catalog DB)]
    Catalog[Catalog Service]

    Client --> Gateway

    Gateway --> Monolith

    Monolith --> LegacyDB
    LegacyDB --> CDC
    CDC --> CatalogDB
    Catalog --> CatalogDB
```

Step 3: Route product reads to the new service.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Monolith[Retail Monolith]
    Catalog[Catalog Service]

    LegacyDB[(Legacy DB)]
    CatalogDB[(Catalog DB)]

    Client --> Gateway

    Gateway -->|Product reads| Catalog
    Gateway -->|Other routes| Monolith

    Monolith --> LegacyDB
    Catalog --> CatalogDB
```

Step 4: Move product writes to the new service.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Monolith[Retail Monolith]
    Catalog[Catalog Service]

    LegacyDB[(Legacy DB)]
    CatalogDB[(Catalog DB)]

    Client --> Gateway

    Gateway -->|Catalog reads and writes| Catalog
    Gateway -->|Other routes| Monolith

    Catalog --> CatalogDB
    Monolith --> LegacyDB

    Catalog -. publish product events .-> Monolith
```

Step 5: Remove catalog code from the monolith.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Monolith[Retail Monolith<br/>Catalog removed]
    Catalog[Catalog Service]
    CatalogDB[(Catalog DB)]

    Client --> Gateway

    Gateway --> Catalog
    Gateway --> Monolith

    Catalog --> CatalogDB
```

At this point, the Catalog capability has been strangled out of the legacy system.

---

#### Testing strategy

Testing is critical because the legacy system may contain hidden behavior.

Useful tests include:

| Test type                 | Purpose                                             |
| ------------------------- | --------------------------------------------------- |
| Characterization tests    | Capture current legacy behavior                     |
| Contract tests            | Ensure old clients still receive expected responses |
| Regression tests          | Confirm existing workflows still work               |
| Shadow comparisons        | Compare legacy and new responses under real traffic |
| Data reconciliation tests | Detect divergence between legacy and new stores     |
| Load tests                | Ensure new services can handle production traffic   |
| Rollback tests            | Confirm traffic can be routed back safely           |

Example response comparison:

```ts
async function compareProductResponse(productId: string) {
  const legacy = await legacyClient.getProduct(productId);
  const modern = await catalogClient.getProduct(productId);

  const normalizedLegacy = normalizeLegacyProduct(legacy);
  const normalizedModern = normalizeModernProduct(modern);

  if (!deepEqual(normalizedLegacy, normalizedModern)) {
    await comparisonLog.write({
      productId,
      legacy: normalizedLegacy,
      modern: normalizedModern,
      comparedAt: new Date().toISOString()
    });
  }
}
```

This is especially useful during shadow mode.

---

#### Rollback strategy

Every migration slice needs a rollback plan.

Rollback may mean:

* route traffic back to legacy,
* disable a feature flag,
* stop a data sync job,
* restore from backup,
* replay events,
* run a repair job,
* pause rollout.

```mermaid
flowchart TD
    Monitor[Monitor new system]
    Problem{Problem detected?}

    Continue[Continue rollout]
    Rollback[Route traffic back to legacy]
    Investigate[Investigate and repair]

    Monitor --> Problem

    Problem -->|No| Continue
    Problem -->|Yes| Rollback
    Rollback --> Investigate
```

Rollback is easier when the legacy system remains the source of truth. It becomes harder once writes move to the new system.

That is why source-of-truth decisions must be explicit.

---

#### Observability

During a strangler migration, you need visibility into both systems.

Track:

* traffic split,
* route destination,
* error rate by destination,
* latency by destination,
* data synchronization lag,
* response differences,
* business KPIs,
* dependency failures,
* fallback frequency,
* rollback events.

Example structured log:

```json
{
  "requestId": "req_123",
  "route": "/products/prod_456",
  "targetSystem": "catalog-service",
  "migrationSlice": "catalog-read-v2",
  "tenantId": "tenant_001",
  "statusCode": 200,
  "latencyMs": 42
}
```

This helps answer:

* Which traffic is still using legacy?
* Which traffic is using the new service?
* Are errors higher in the new path?
* Are users getting different results?
* Is data synchronization delayed?
* Is the migration safe to expand?

---

#### When to use it

Use the Strangler Fig Pattern when:

* replacing a large legacy system,
* migrating from monolith to microservices,
* modernizing old APIs,
* moving from on-premise to cloud,
* replacing a legacy database,
* decomposing a tightly coupled platform,
* migrating one tenant, region, or product line at a time,
* reducing risk is more important than speed,
* the business must keep running during modernization.

It is especially useful when the legacy system is too important to shut down and too large to rewrite safely.

---

#### When not to use it

Avoid or reconsider this pattern when:

* the system is small enough to replace safely,
* the legacy system is near end-of-life and barely used,
* the old and new systems cannot coexist,
* data synchronization would be too risky,
* the business can tolerate a clean cutover,
* the team cannot maintain two systems at once,
* the migration boundary cannot be isolated,
* there is no way to route traffic selectively.

For small systems, a direct rewrite may be simpler. For highly coupled data systems, a database-first migration or modular refactoring may be needed before strangling routes.

---

#### Benefits

**1. Reduces big-bang risk**

Functionality is replaced incrementally rather than all at once.

**2. Delivers value earlier**

Teams can ship the first migrated slice before the entire replacement is complete.

**3. Allows production validation**

New services can be tested with real traffic gradually.

**4. Supports rollback**

Traffic can often be routed back to legacy if something goes wrong.

**5. Enables learning**

Each migration slice teaches the team more about legacy behavior, data, clients, and operational needs.

**6. Preserves business continuity**

The legacy system keeps running while modernization happens.

**7. Helps prioritize**

Teams can migrate high-value or high-pain areas first.

---

#### Trade-offs

**1. Temporary complexity increases**

For a while, both legacy and new systems exist together.

**2. Routing becomes more complicated**

The gateway or facade must decide which system handles each request.

**3. Data synchronization is difficult**

Keeping old and new data consistent can be the hardest part.

**4. Duplicate logic may exist temporarily**

Some business rules may live in both systems during migration.

**5. Testing becomes more complex**

Both paths must be tested until the legacy slice is retired.

**6. Operational burden increases**

Teams must monitor, deploy, and support both old and new systems.

**7. Migrations can stall**

Without discipline, the organization may keep both systems forever.

---

#### Common mistakes

**Mistake 1: Not defining the source of truth**

If both systems can write the same data without clear ownership, divergence is likely.

**Mistake 2: Letting the facade become a new monolith**

A gateway or facade should route and translate, not accumulate all business logic.

**Mistake 3: Migrating the hardest part first**

Start with a slice that teaches you something but does not put the business at extreme risk.

**Mistake 4: Keeping dual-write logic forever**

Temporary migration logic should have an owner and a removal plan.

**Mistake 5: Ignoring legacy edge cases**

Old systems often contain undocumented behavior that users rely on.

**Mistake 6: Failing to retire old code**

A migration is incomplete until the legacy path is removed.

**Mistake 7: Not investing in observability**

Without route-level metrics and comparison logs, teams cannot safely expand traffic.

---

#### Practical design checklist

Before starting a strangler migration, answer:

* What capability or route is being migrated first?
* Why is this slice a good first candidate?
* How will traffic be routed?
* What is the rollback mechanism?
* Which system is source of truth for reads?
* Which system is source of truth for writes?
* Does the new system need legacy data?
* How will data be backfilled?
* How will ongoing data changes be synchronized?
* How will data divergence be detected?
* How will old and new responses be compared?
* What clients depend on the old behavior?
* What contracts must remain compatible?
* What metrics determine whether rollout can expand?
* Who owns the legacy path?
* Who owns the new path?
* When will the old code be removed?

---

#### Related patterns

| Pattern                          | Relationship                                                    |
| -------------------------------- | --------------------------------------------------------------- |
| Anti-Corruption Layer            | Protects the new model from legacy assumptions                  |
| API Gateway                      | Commonly used to route traffic between old and new systems      |
| Facade                           | Preserves old contracts while backend implementation changes    |
| Shadow Deployment                | Sends copied traffic to the new system before serving responses |
| Blue-Green Deployment            | Useful for switching traffic between versions                   |
| Database per Service             | Often the target state after migration                          |
| Change Data Capture              | Helps replicate legacy data into new services                   |
| Outbox Pattern                   | Helps publish reliable events during migration                  |
| Consumer-Driven Contracts        | Ensures clients are not broken during replacement               |
| Feature Flags                    | Enable controlled rollout and rollback                          |
| Decompose by Business Capability | Helps choose migration slices                                   |
| Decompose by Subdomain           | Helps avoid copying bad legacy boundaries                       |

---

#### Summary

The Strangler Fig Pattern replaces a legacy system gradually by building new functionality around it and routing traffic piece by piece.

The central idea is:

> Do not replace the whole legacy system in one risky cutover. Replace one slice at a time while the business keeps running.

A good strangler migration has:

* a clear routing layer,
* a carefully chosen first slice,
* explicit source-of-truth rules,
* data synchronization strategy,
* compatibility testing,
* observability,
* rollback,
* and a plan to remove old code.

The pattern reduces modernization risk, but it does not eliminate complexity. During the migration, the organization must operate both old and new systems. The migration only succeeds if each legacy slice is eventually retired, not just bypassed.

---

### 6. Anti-Corruption Layer

#### What it is

An **Anti-Corruption Layer**, often abbreviated as **ACL**, is a translation boundary between two systems that have different models, APIs, terminology, data formats, workflows, or assumptions.

Its purpose is to protect one system’s domain model from being polluted by another system’s model.

The most common use case is protecting a new service from a legacy system:

```mermaid
flowchart TD
    NewService[New Service]
    ACL[Anti-Corruption Layer]
    Legacy[Legacy System]

    NewService --> ACL
    ACL --> Legacy
```

The new service speaks its own clean domain language. The legacy system speaks its old language. The Anti-Corruption Layer translates between them.

The central idea is:

> Do not let another system’s model become your model by accident.

For example, suppose a legacy system represents customers like this:

```json
{
  "cust_no": "C12345",
  "stat": "A",
  "addr1": "100 Market Street",
  "addr2": "Suite 400",
  "acct_typ": "P",
  "vip_flg": "Y"
}
```

A new service should not blindly spread these fields throughout its codebase.

Instead, the Anti-Corruption Layer translates the legacy representation into the new service’s own model:

```json
{
  "customerId": "C12345",
  "status": "ACTIVE",
  "billingAddress": {
    "line1": "100 Market Street",
    "line2": "Suite 400"
  },
  "accountType": "PREMIUM",
  "isVip": true
}
```

The translation may look simple in this example, but in real systems it often includes business rules, workflow mapping, error handling, retries, identity mapping, and data normalization.

---

#### Why this pattern exists

Systems rarely agree on meaning.

A legacy monolith, a vendor API, an ERP, a CRM, and a new microservice may all use different names and assumptions for the same business concept.

For example, one system may use:

| Concept            | Legacy system     | New service                  |
| ------------------ | ----------------- | ---------------------------- |
| Customer ID        | `cust_no`         | `customerId`                 |
| Active customer    | `stat = A`        | `status = ACTIVE`            |
| Suspended customer | `stat = S`        | `status = SUSPENDED`         |
| Premium account    | `acct_typ = P`    | `accountType = PREMIUM`      |
| Deleted record     | `delete_flag = Y` | `lifecycleStatus = ARCHIVED` |

At first, it can seem faster to reuse the external model everywhere:

```mermaid
flowchart TD
    Legacy[Legacy System]
    NewService[New Service]
    Domain[New Domain Logic]
    DB[(New Service DB)]

    Legacy --> NewService
    NewService --> Domain
    Domain --> DB

    LegacyModel[Legacy fields leak everywhere]
    NewService --> LegacyModel
    Domain --> LegacyModel
    DB --> LegacyModel
```

This creates long-term coupling.

The new system begins to inherit legacy names, legacy status codes, legacy workflows, and legacy mistakes. Over time, the new system becomes difficult to evolve because its internal model is shaped by a system it was supposed to replace or integrate with.

An Anti-Corruption Layer prevents this by isolating translation logic:

```mermaid
flowchart TD
    Legacy[Legacy System]
    ACL[Anti-Corruption Layer]
    Domain[Clean Domain Model]
    NewService[New Service]

    Legacy --> ACL
    ACL --> Domain
    Domain --> NewService
```

The external model still exists, but it is contained.

---

#### What it solves

The Anti-Corruption Layer solves **model contamination**.

Model contamination happens when one system’s assumptions leak into another system.

Common signs include:

* legacy field names appear throughout new code,
* new services use old status codes directly,
* external API response shapes become internal domain objects,
* vendor-specific terminology appears in business logic,
* database column names shape service APIs,
* error handling depends on raw external error strings,
* new workflows are forced to match old workflows,
* teams cannot change the new model without changing legacy integration code.

For example, this is contaminated domain logic:

```ts id="vlj407"
function canPlaceOrder(customer: LegacyCustomer): boolean {
  return customer.stat === "A" && customer.del_flg !== "Y";
}
```

The business rule is about whether the customer can place an order, but the logic depends directly on legacy fields.

A cleaner version isolates legacy interpretation:

```ts id="o9med2"
function canPlaceOrder(customer: Customer): boolean {
  return customer.status === "ACTIVE" && customer.lifecycleStatus !== "ARCHIVED";
}
```

The mapping from `stat` and `del_flg` happens outside the domain logic.

---

#### Basic architecture

An Anti-Corruption Layer usually sits between the new service and the external system.

```mermaid
flowchart TD
    Client[Client]

    subgraph NewService[New Service]
        API[Service API]
        Domain[Domain Logic]
        Port[External System Port]
    end

    ACL[Anti-Corruption Layer]
    External[Legacy or External System]

    Client --> API
    API --> Domain
    Domain --> Port
    Port --> ACL
    ACL --> External
```

The new service talks to a local interface that makes sense in its own domain. The ACL implements that interface by calling the external system and translating results.

This keeps external details away from the core business logic.

---

#### Example: customer integration

Suppose a new Order Service needs customer status from a legacy CRM before allowing an order.

The Order Service wants to think in this model:

```ts id="ec1gra"
type Customer = {
  customerId: string;
  status: "ACTIVE" | "INACTIVE" | "SUSPENDED";
  lifecycleStatus: "CURRENT" | "ARCHIVED";
  accountType: "STANDARD" | "PREMIUM";
};
```

The legacy CRM returns this model:

```ts id="7aj5h5"
type LegacyCrmCustomer = {
  cust_no: string;
  stat: "A" | "I" | "S";
  del_flg: "Y" | "N";
  acct_typ: "S" | "P";
};
```

The Anti-Corruption Layer translates between them:

```ts id="38r9u9"
function mapLegacyCustomer(legacy: LegacyCrmCustomer): Customer {
  return {
    customerId: legacy.cust_no,
    status: mapStatus(legacy.stat),
    lifecycleStatus: legacy.del_flg === "Y" ? "ARCHIVED" : "CURRENT",
    accountType: legacy.acct_typ === "P" ? "PREMIUM" : "STANDARD"
  };
}

function mapStatus(status: LegacyCrmCustomer["stat"]): Customer["status"] {
  switch (status) {
    case "A":
      return "ACTIVE";
    case "I":
      return "INACTIVE";
    case "S":
      return "SUSPENDED";
  }
}
```

The domain logic uses only the clean model:

```ts id="tn7d22"
function validateCustomerCanOrder(customer: Customer): void {
  if (customer.lifecycleStatus === "ARCHIVED") {
    throw new Error("Archived customers cannot place orders");
  }

  if (customer.status !== "ACTIVE") {
    throw new Error("Customer is not active");
  }
}
```

The Order Service never needs to know that the CRM uses `stat = A` for active customers.

---

#### ACL as adapter

A common implementation is the **adapter pattern**.

The domain defines an interface it needs:

```ts id="318q2a"
type CustomerProfile = {
  customerId: string;
  status: "ACTIVE" | "INACTIVE" | "SUSPENDED";
  accountType: "STANDARD" | "PREMIUM";
};

interface CustomerDirectory {
  getCustomer(customerId: string): Promise<CustomerProfile>;
}
```

The Anti-Corruption Layer implements that interface using the legacy system:

```ts id="krkkn1"
class LegacyCrmCustomerDirectory implements CustomerDirectory {
  constructor(private readonly httpClient: HttpClient) {}

  async getCustomer(customerId: string): Promise<CustomerProfile> {
    const response = await this.httpClient.get<LegacyCrmCustomer>(
      `/legacy-crm/customers/${customerId}`
    );

    return mapLegacyCustomerToProfile(response.data);
  }
}

function mapLegacyCustomerToProfile(
  legacy: LegacyCrmCustomer
): CustomerProfile {
  return {
    customerId: legacy.cust_no,
    status: mapLegacyStatus(legacy.stat),
    accountType: legacy.acct_typ === "P" ? "PREMIUM" : "STANDARD"
  };
}
```

The domain service depends on the interface, not the legacy API:

```ts id="s9wwd6"
class OrderPlacementService {
  constructor(private readonly customerDirectory: CustomerDirectory) {}

  async placeOrder(command: PlaceOrderCommand): Promise<Order> {
    const customer = await this.customerDirectory.getCustomer(command.customerId);

    if (customer.status !== "ACTIVE") {
      throw new Error("Customer is not eligible to place orders");
    }

    return createOrder(command);
  }
}
```

This means the legacy CRM can later be replaced without changing order placement logic. Only the adapter changes.

---

#### ACL for outbound requests

Anti-Corruption Layers are not only for reading external data. They also translate outbound commands.

Suppose the new Payment Service uses this command:

```ts id="0x8cx7"
type AuthorizePaymentCommand = {
  paymentId: string;
  orderId: string;
  amount: {
    value: number;
    currency: "USD" | "EUR" | "GBP";
  };
  paymentMethodToken: string;
};
```

But the legacy payment gateway expects this request:

```json
{
  "txn_ref": "pay_123",
  "ord_ref": "ord_456",
  "amt_cents": 12999,
  "curr": "USD",
  "pm_token": "tok_abc"
}
```

The ACL maps the outbound command:

```ts id="92w64p"
function toLegacyPaymentRequest(
  command: AuthorizePaymentCommand
): LegacyPaymentRequest {
  return {
    txn_ref: command.paymentId,
    ord_ref: command.orderId,
    amt_cents: Math.round(command.amount.value * 100),
    curr: command.amount.currency,
    pm_token: command.paymentMethodToken
  };
}
```

It also maps the response:

```ts id="7vh8s2"
function fromLegacyPaymentResponse(
  response: LegacyPaymentResponse
): PaymentAuthorization {
  return {
    paymentId: response.txn_ref,
    authorizationId: response.auth_code,
    status: mapPaymentStatus(response.resp_cd),
    authorizedAt: new Date(response.ts)
  };
}
```

The rest of the Payment Service uses the clean domain model.

---

#### ACL for workflow translation

Sometimes translation is not just about fields. The systems may have different workflow semantics.

For example, a new Order Service may have a simple order lifecycle:

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Confirmed
    Confirmed --> Shipped
    Confirmed --> Cancelled
    Shipped --> Delivered
```

But a legacy fulfillment system may use different states:

```mermaid
stateDiagram-v2
    [*] --> N
    N --> A
    A --> P
    P --> D
    A --> X
```

Where:

| Legacy state | Meaning           |
| ------------ | ----------------- |
| `N`          | New               |
| `A`          | Allocated         |
| `P`          | Picked and packed |
| `D`          | Dispatched        |
| `X`          | Cancelled         |

The ACL translates workflow state:

```ts id="0o039o"
type OrderStatus =
  | "PENDING"
  | "CONFIRMED"
  | "SHIPPED"
  | "CANCELLED"
  | "DELIVERED";

type LegacyFulfillmentStatus = "N" | "A" | "P" | "D" | "X";

function mapFulfillmentStatus(
  status: LegacyFulfillmentStatus
): OrderStatus {
  switch (status) {
    case "N":
      return "PENDING";
    case "A":
      return "CONFIRMED";
    case "P":
      return "CONFIRMED";
    case "D":
      return "SHIPPED";
    case "X":
      return "CANCELLED";
  }
}
```

This mapping is more than renaming. It compresses and interprets another system’s lifecycle.

That is why Anti-Corruption Layers can become complex. Real translation often involves business meaning.

---

#### ACL for error translation

External systems often return errors that do not match the new service’s error model.

Legacy error:

```json
{
  "err": "CUST_STAT_INVALID",
  "code": 8817,
  "msg": "Customer status is not valid for operation"
}
```

New service error:

```json
{
  "error": "CUSTOMER_NOT_ELIGIBLE",
  "message": "Customer is not eligible to place an order"
}
```

The ACL should translate errors too:

```ts id="l4wx7m"
class CustomerNotEligibleError extends Error {}
class ExternalSystemUnavailableError extends Error {}

function mapLegacyCrmError(error: LegacyCrmError): Error {
  switch (error.code) {
    case 8817:
      return new CustomerNotEligibleError(
        "Customer is not eligible to place an order"
      );

    case 9001:
    case 9002:
      return new ExternalSystemUnavailableError(
        "Customer system is temporarily unavailable"
      );

    default:
      return new Error("Unexpected customer system error");
  }
}
```

This prevents raw legacy errors from leaking into your API, logs, and business logic.

---

#### ACL for identity mapping

Different systems often use different identifiers for the same real-world thing.

For example:

| Entity   | New service ID | Legacy ID        |
| -------- | -------------- | ---------------- |
| Customer | `cus_123`      | `C0009981`       |
| Product  | `prod_456`     | `SKU-8841`       |
| Order    | `ord_789`      | `SO-2024-000331` |

The ACL may need an identity mapping table:

```mermaid
flowchart TD
    NewService[New Service]
    ACL[Anti-Corruption Layer]
    MappingDB[(ID Mapping Table)]
    Legacy[Legacy System]

    NewService --> ACL
    ACL --> MappingDB
    ACL --> Legacy
```

Example table:

| Local ID   | External system | External ID      |
| ---------- | --------------- | ---------------- |
| `cus_123`  | Legacy CRM      | `C0009981`       |
| `prod_456` | Legacy ERP      | `SKU-8841`       |
| `ord_789`  | Legacy OMS      | `SO-2024-000331` |

Example lookup:

```ts id="skltui"
async function getLegacyCustomerId(customerId: string): Promise<string> {
  const mapping = await idMappingRepository.find({
    localId: customerId,
    externalSystem: "LEGACY_CRM"
  });

  if (!mapping) {
    throw new Error(`No legacy customer mapping for ${customerId}`);
  }

  return mapping.externalId;
}
```

Identity mapping is often one of the most important parts of an ACL during legacy migration.

---

#### ACL placement options

An Anti-Corruption Layer can be implemented in several places.

##### Option 1: Inside the consuming service

```mermaid
flowchart TD
    Service[New Service]

    subgraph ServiceBox[Inside New Service]
        Domain[Domain Logic]
        Adapter[Legacy Adapter / ACL]
    end

    Legacy[Legacy System]

    Service --> ServiceBox
    Domain --> Adapter
    Adapter --> Legacy
```

This is common when only one service needs the translation.

Benefits:

* simple deployment,
* translation is close to the domain,
* easy to test with the service,
* no extra network hop.

Trade-off:

* translation may be duplicated if many services need it.

##### Option 2: Separate ACL service

```mermaid
flowchart TD
    ServiceA[Service A]
    ServiceB[Service B]
    ACLService[Shared ACL Service]
    Legacy[Legacy System]

    ServiceA --> ACLService
    ServiceB --> ACLService
    ACLService --> Legacy
```

This can be useful when many services need the same protected access to a legacy system.

Benefits:

* shared translation,
* centralized access control,
* one place to handle legacy quirks,
* easier legacy throttling and caching.

Trade-offs:

* extra deployment,
* extra network hop,
* risk of becoming a bottleneck,
* risk of becoming a new mini-monolith.

##### Option 3: At the edge or gateway

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway with Translation]
    Legacy[Legacy System]
    NewService[New Service]

    Client --> Gateway
    Gateway --> Legacy
    Gateway --> NewService
```

This is useful for client compatibility, but should be used carefully. Gateways are usually better for routing, authentication, rate limiting, and protocol translation than deep domain translation.

If a gateway accumulates too much business mapping, it can become a new monolith.

---

#### Example: separate ACL service API

A dedicated ACL service may expose a clean API:

```http id="5x8rc5"
GET /customers/{customerId}/profile
```

Internally, it calls the legacy CRM:

```http id="nl410h"
GET /crm/v2/cust?cust_no=C0009981&include_flags=Y
```

The clean response:

```json
{
  "customerId": "cus_123",
  "status": "ACTIVE",
  "accountType": "PREMIUM",
  "billingAddress": {
    "line1": "100 Market Street",
    "line2": "Suite 400"
  }
}
```

The consuming services never see the legacy CRM response shape.

---

#### ACL and caching

Sometimes the Anti-Corruption Layer caches translated data.

```mermaid
flowchart TD
    Service[New Service]
    ACL[Anti-Corruption Layer]
    Cache[(Cache)]
    Legacy[Legacy System]

    Service --> ACL
    ACL --> Cache
    ACL --> Legacy
```

Caching can reduce load on slow or expensive legacy systems.

But be careful. Cached data may become stale.

Useful questions:

* How fresh does the data need to be?
* Is stale data acceptable?
* What is the cache TTL?
* How is the cache invalidated?
* What happens if the legacy system is unavailable?
* Can the ACL serve stale data during outages?
* Is the cached data sensitive?

Example:

```ts id="u6l5kz"
async function getCustomerProfile(customerId: string): Promise<CustomerProfile> {
  const cacheKey = `customer-profile:${customerId}`;

  const cached = await cache.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  const legacy = await legacyCrmClient.getCustomer(customerId);
  const profile = mapLegacyCustomerToProfile(legacy);

  await cache.set(cacheKey, JSON.stringify(profile), {
    ttlSeconds: 300
  });

  return profile;
}
```

Caching belongs in the ACL when the cache is part of protecting the domain from legacy latency, instability, or rate limits.

---

#### ACL and resilience

Legacy and external systems are often slow, unreliable, rate-limited, or hard to scale.

An Anti-Corruption Layer is a good place to add resilience logic:

* timeouts,
* retries,
* circuit breakers,
* rate limiting,
* fallback behavior,
* bulkheads,
* request normalization,
* response validation.

```mermaid
flowchart TD
    Service[New Service]
    ACL[Anti-Corruption Layer]

    Timeout[Timeouts]
    Retry[Retries]
    Circuit[Circuit Breaker]
    Mapping[Model Translation]

    Legacy[Legacy System]

    Service --> ACL

    ACL --> Timeout
    Timeout --> Retry
    Retry --> Circuit
    Circuit --> Mapping
    Mapping --> Legacy
```

Example:

```ts id="d5g4rr"
async function callLegacyWithTimeout<T>(
  operation: () => Promise<T>,
  timeoutMs: number
): Promise<T> {
  return Promise.race([
    operation(),
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error("Legacy call timed out")), timeoutMs)
    )
  ]);
}
```

The rest of the domain should not need to know about legacy timeout behavior. It should receive a meaningful domain error.

---

#### ACL and events

Anti-Corruption Layers can also translate events.

Suppose a legacy system emits this event:

```json
{
  "type": "CUST_UPD",
  "cust_no": "C0009981",
  "stat": "S",
  "upd_ts": "20260429120000"
}
```

The ACL can publish a clean domain event:

```json
{
  "eventType": "CustomerSuspended",
  "eventId": "evt_123",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "customerId": "cus_123",
    "reason": "STATUS_CHANGED"
  }
}
```

Architecture:

```mermaid
flowchart TD
    Legacy[Legacy Event Source]
    ACL[Event Translation ACL]
    Bus[(Event Bus)]
    Consumers[New Services]

    Legacy --> ACL
    ACL --> Bus
    Bus --> Consumers
```

This prevents all new services from having to understand legacy event codes.

---

#### ACL vs simple adapter

A simple adapter translates technical details such as protocol or field names.

An Anti-Corruption Layer does more: it protects the domain model.

| Concern                    | Simple adapter  | Anti-Corruption Layer |
| -------------------------- | --------------- | --------------------- |
| Protocol conversion        | Yes             | Yes                   |
| Field mapping              | Yes             | Yes                   |
| Domain meaning translation | Maybe           | Yes                   |
| Workflow translation       | Usually no      | Often yes             |
| Error translation          | Maybe           | Yes                   |
| Identity mapping           | Maybe           | Often yes             |
| Protecting local model     | Not necessarily | Core purpose          |

A simple adapter might be enough when systems mostly agree on meaning.

An ACL is needed when the external system’s model would distort your own model if used directly.

---

#### ACL vs facade

A **facade** provides a simplified interface to a subsystem.

An **Anti-Corruption Layer** protects a domain model from another model.

They can overlap, but the intent is different.

```mermaid
flowchart TD
    Client[Client]
    Facade[Facade]
    Subsystem[Complex Subsystem]

    Domain[Domain Service]
    ACL[Anti-Corruption Layer]
    External[External Model]

    Client --> Facade
    Facade --> Subsystem

    Domain --> ACL
    ACL --> External
```

A facade is mostly about simplifying access.
An ACL is about preserving model integrity.

---

#### When to use it

Use an Anti-Corruption Layer when integrating with:

* a legacy monolith,
* a vendor API,
* an ERP system,
* a CRM system,
* a payment gateway,
* an external database,
* another bounded context,
* a partner API,
* a mainframe,
* a system with different terminology,
* a system with incompatible workflow semantics,
* a system you do not control.

It is especially useful when:

* the external model is ugly, unstable, or outdated,
* the external system uses different language,
* the new domain model needs to stay clean,
* the legacy system will eventually be replaced,
* multiple systems disagree about business meaning,
* external errors need to be normalized,
* external IDs need to be mapped to internal IDs.

---

#### When not to use it

Do not add a heavy ACL when:

* the integration is simple,
* the external model is already aligned with your model,
* there is no meaningful domain translation,
* the data is used only in one small place,
* the extra layer would add complexity without protection,
* the external API is already the canonical domain contract.

For simple cases, a small adapter or client library may be enough.

Example:

```ts id="b11rb3"
const response = await exchangeRateClient.getLatestRates("USD");
```

If the external service provides a clean and stable exchange-rate model that matches your needs, a full ACL may be unnecessary.

---

#### Benefits

**1. Protects the domain model**

Legacy or vendor concepts do not leak into your business logic.

**2. Localizes translation logic**

Mapping, normalization, and error handling live in one place.

**3. Reduces coupling**

The new service depends on its own interface rather than the external system’s raw contract.

**4. Supports legacy migration**

New services can be built with clean models while still interoperating with old systems.

**5. Improves testability**

Translation logic can be unit tested separately from domain logic.

**6. Makes replacement easier**

If the external system changes or is replaced, fewer parts of the codebase need to change.

**7. Normalizes errors and behavior**

The service can expose consistent errors even when external systems behave inconsistently.

---

#### Trade-offs

**1. Adds another component or layer**

An ACL must be designed, implemented, tested, deployed, and maintained.

**2. Translation can become complex**

Mapping workflows, identities, errors, and lifecycle states can be difficult.

**3. Risk of becoming a dumping ground**

If not managed, the ACL can accumulate unrelated logic and become messy.

**4. Performance overhead**

Translation, network calls, and caching can add latency.

**5. Debugging can be harder**

Issues may require tracing through both the new model and external model.

**6. Data freshness can be tricky**

If the ACL caches or replicates data, it must manage staleness and invalidation.

**7. Ownership must be clear**

Teams must know who owns the ACL, especially if many services depend on it.

---

#### Common mistakes

**Mistake 1: Letting legacy fields leak through**

If `cust_no`, `acct_typ`, or `stat_cd` appear throughout the new domain logic, the ACL is not doing its job.

**Mistake 2: Treating field mapping as the whole problem**

The hardest translation is often business meaning, workflow state, identity, and error semantics.

**Mistake 3: Putting too much business logic in the ACL**

The ACL should translate and protect. It should not become the owner of core domain behavior unless that behavior is specifically integration-related.

**Mistake 4: Making the ACL a shared bottleneck**

A central ACL service can become a dependency for too many services.

**Mistake 5: Skipping tests for mappings**

Mapping bugs can create subtle business errors.

**Mistake 6: Ignoring unknown external values**

External systems may send new status codes, null fields, malformed dates, or unexpected errors. The ACL should handle them deliberately.

**Mistake 7: Forgetting observability**

Translation failures, legacy timeouts, and mapping errors should be logged and monitored.

---

#### Testing strategy

The ACL should have strong tests because it carries important translation logic.

Useful tests include:

| Test type               | Purpose                                               |
| ----------------------- | ----------------------------------------------------- |
| Mapping tests           | Verify field and status translation                   |
| Error translation tests | Verify external errors become domain errors           |
| Contract tests          | Verify assumptions about the external API             |
| Integration tests       | Verify real calls to sandbox or test external systems |
| Regression tests        | Preserve behavior for known legacy edge cases         |
| Resilience tests        | Verify timeout, retry, and fallback behavior          |
| Unknown-value tests     | Verify safe handling of unexpected external values    |

Example mapping test:

```ts id="sq5nm5"
describe("mapLegacyCustomer", () => {
  it("maps active premium customer", () => {
    const legacy: LegacyCrmCustomer = {
      cust_no: "C12345",
      stat: "A",
      del_flg: "N",
      acct_typ: "P"
    };

    expect(mapLegacyCustomer(legacy)).toEqual({
      customerId: "C12345",
      status: "ACTIVE",
      lifecycleStatus: "CURRENT",
      accountType: "PREMIUM"
    });
  });

  it("maps deleted customer as archived", () => {
    const legacy: LegacyCrmCustomer = {
      cust_no: "C12345",
      stat: "I",
      del_flg: "Y",
      acct_typ: "S"
    };

    expect(mapLegacyCustomer(legacy).lifecycleStatus).toBe("ARCHIVED");
  });
});
```

---

#### Practical design checklist

Use this checklist when designing an Anti-Corruption Layer.

A good ACL should answer:

* What external system is being isolated?
* What local domain model are we protecting?
* What terminology differs between the systems?
* What field mappings are needed?
* What status mappings are needed?
* What workflow mappings are needed?
* What identifiers need translation?
* What external errors need normalization?
* What external assumptions must not leak inward?
* Where should the ACL live?
* Who owns the ACL?
* Does the ACL need caching?
* Does the ACL need retry, timeout, or circuit breaker logic?
* How will translation failures be observed?
* How will the ACL handle unknown external values?
* How will the ACL be tested?
* What happens if the external system changes?

A proposed ACL is probably useful if:

* it prevents external terminology from spreading,
* it hides legacy or vendor-specific APIs,
* it translates business meaning, not just field names,
* it gives the local domain a clean interface,
* it can be tested independently,
* it has clear ownership.

A proposed ACL is probably unnecessary if:

* it only wraps a clean API with identical concepts,
* it adds no meaningful protection,
* it duplicates a stable internal contract,
* it makes the system harder to understand without reducing coupling.

---

#### Related patterns

| Pattern                   | Relationship                                                       |
| ------------------------- | ------------------------------------------------------------------ |
| Strangler Fig Pattern     | ACLs often protect new services during legacy migration            |
| Decompose by Subdomain    | ACLs protect bounded contexts from each other’s models             |
| Published Language        | A stable contract can reduce the amount of translation needed      |
| Open Host Service         | A well-designed API can make downstream ACLs simpler               |
| Adapter Pattern           | A technical implementation style often used inside ACLs            |
| Facade                    | Can simplify access to a legacy system, sometimes alongside an ACL |
| API Gateway               | May route to an ACL or perform light protocol translation          |
| Consumer-Driven Contracts | Helps verify the ACL satisfies consuming services                  |
| Circuit Breaker           | Protects services from unreliable external systems                 |
| Outbox Pattern            | Helps translate and publish reliable events across boundaries      |

---

#### Summary

An Anti-Corruption Layer is a protective translation boundary between systems with different models, terminology, APIs, or assumptions.

The central idea is:

> Let the external system be messy at the boundary, not inside your domain.

A good Anti-Corruption Layer:

* translates external models into local domain models,
* maps identifiers and statuses,
* normalizes errors,
* protects business logic from legacy or vendor concepts,
* contains integration-specific complexity,
* and makes future replacement easier.

It is especially valuable during legacy modernization, vendor integration, and communication between bounded contexts.

The trade-off is that the ACL itself becomes something you must design and maintain. It should be strong enough to protect the domain, but not so large that it becomes the new place where all business logic goes.


---

## 3. Client Access, API Edge, and Composition Patterns

These patterns simplify how clients access distributed backend services.

### 7. API Gateway

#### What it is

An **API Gateway** is a single entry point that clients use to access backend services.

Instead of clients calling many services directly, they call the gateway. The gateway then routes each request to the correct backend service.

```mermaid
flowchart TD
    Client[Client Applications]
    Gateway[API Gateway]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    Client --> Gateway

    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Inventory
    Gateway --> Shipping
```

The API Gateway sits at the edge of the backend system. It hides the internal service topology from clients.

Without a gateway, a client may need to know about every backend service:

```mermaid
flowchart TD
    Web[Web Client]
    Mobile[Mobile Client]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Notifications[Notification Service]

    Web --> Orders
    Web --> Payments
    Web --> Inventory
    Web --> Shipping
    Web --> Notifications

    Mobile --> Orders
    Mobile --> Payments
    Mobile --> Inventory
    Mobile --> Shipping
    Mobile --> Notifications
```

This creates tight coupling between clients and backend services.

With a gateway, clients only need to know one public API surface:

```mermaid
flowchart TD
    Web[Web Client]
    Mobile[Mobile Client]
    Partner[Partner Client]

    Gateway[API Gateway]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Notifications[Notification Service]

    Web --> Gateway
    Mobile --> Gateway
    Partner --> Gateway

    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Inventory
    Gateway --> Shipping
    Gateway --> Notifications
```

The central idea is:

> Clients should not need to understand the internal structure of the backend system.

The gateway provides a stable external boundary while backend services remain free to evolve internally.

---

#### Why this pattern exists

Microservices create many backend services. Each service may have its own:

* hostname,
* protocol,
* authentication requirements,
* version,
* deployment lifecycle,
* data model,
* scaling pattern,
* authorization rules,
* rate limits,
* error formats.

If clients directly depend on all of that, client development becomes difficult.

For example, a mobile app showing an order details screen may need:

* order data from Order Service,
* payment status from Payment Service,
* shipment tracking from Shipping Service,
* product images from Catalog Service,
* support eligibility from Customer Support Service.

Without a gateway, the mobile app might need to call all of them:

```mermaid
sequenceDiagram
    participant Mobile as Mobile App
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Shipping as Shipping Service
    participant Catalog as Catalog Service
    participant Support as Support Service

    Mobile->>Orders: GET /orders/ord_123
    Mobile->>Payments: GET /payments?orderId=ord_123
    Mobile->>Shipping: GET /shipments?orderId=ord_123
    Mobile->>Catalog: GET /products/prod_456
    Mobile->>Support: GET /support/eligibility?orderId=ord_123
```

That design creates several problems:

* The client knows too much about backend internals.
* The client must handle many network calls.
* Backend service changes can break clients.
* Authentication and authorization logic may be duplicated.
* Mobile performance suffers from high latency.
* Each client may implement different error handling.
* Backend service topology becomes part of the client contract.

An API Gateway reduces this coupling.

```mermaid
sequenceDiagram
    participant Mobile as Mobile App
    participant Gateway as API Gateway
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Shipping as Shipping Service
    participant Catalog as Catalog Service
    participant Support as Support Service

    Mobile->>Gateway: GET /order-details/ord_123

    Gateway->>Orders: Get order
    Gateway->>Payments: Get payment status
    Gateway->>Shipping: Get shipment status
    Gateway->>Catalog: Get product details
    Gateway->>Support: Get support eligibility

    Gateway-->>Mobile: Combined order details response
```

The client sees one API. The gateway manages the backend calls.

---

#### What it solves

The API Gateway solves **client-to-service coupling**.

Without a gateway, clients may depend directly on service locations and contracts:

```mermaid
flowchart TD
    Client[Client]

    Client --> URL1[orders.internal.company.com]
    Client --> URL2[payments.internal.company.com]
    Client --> URL3[inventory.internal.company.com]
    Client --> URL4[shipping.internal.company.com]
```

This is fragile. If the Payment Service moves, splits, changes protocol, or changes version, clients may need to change.

With a gateway:

```mermaid
flowchart TD
    Client[Client]
    Gateway[api.company.com]

    Client --> Gateway

    Gateway --> Orders[Order Service]
    Gateway --> Payments[Payment Service]
    Gateway --> Inventory[Inventory Service]
    Gateway --> Shipping[Shipping Service]
```

The gateway becomes the stable external API boundary.

It can also centralize edge concerns that should not be reimplemented in every service:

* TLS termination,
* authentication,
* authorization enforcement,
* rate limiting,
* request routing,
* request validation,
* API version routing,
* logging,
* tracing,
* metrics,
* request size limits,
* CORS,
* bot protection,
* IP allowlists,
* tenant routing,
* protocol translation.

---

#### Basic responsibilities

An API Gateway usually handles several categories of responsibility.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Auth[Authentication]
    Authz[Authorization]
    Routing[Routing]
    RateLimit[Rate Limiting]
    TLS[TLS Termination]
    Observability[Logging and Metrics]
    Transform[Request or Response Transformation]

    Services[Backend Services]

    Client --> Gateway

    Gateway --> Auth
    Gateway --> Authz
    Gateway --> Routing
    Gateway --> RateLimit
    Gateway --> TLS
    Gateway --> Observability
    Gateway --> Transform

    Routing --> Services
```

However, the gateway should be careful about what it owns.

A good gateway owns **edge concerns**.

A bad gateway starts owning **core business logic**.

| Good gateway responsibility        | Risky gateway responsibility             |
| ---------------------------------- | ---------------------------------------- |
| Authenticate requests              | Decide whether an order can be cancelled |
| Route `/orders/*` to Order Service | Calculate order totals                   |
| Enforce rate limits                | Apply pricing rules                      |
| Terminate TLS                      | Decide fraud risk                        |
| Add correlation IDs                | Manage inventory reservation logic       |
| Normalize simple errors            | Own payment state transitions            |
| Validate request size              | Implement business workflows             |

The gateway should help clients reach backend capabilities. It should not become the place where all business decisions live.

---

#### Request routing

The simplest API Gateway responsibility is routing.

The gateway receives a request and sends it to the correct backend service.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    RouteDecision{Route}

    Orders[Order Service]
    Payments[Payment Service]
    Catalog[Catalog Service]
    Customers[Customer Service]

    Client --> Gateway
    Gateway --> RouteDecision

    RouteDecision -->|/orders/*| Orders
    RouteDecision -->|/payments/*| Payments
    RouteDecision -->|/catalog/*| Catalog
    RouteDecision -->|/customers/*| Customers
```

Example route table:

| Public route       | Backend service  |
| ------------------ | ---------------- |
| `/api/orders/*`    | Order Service    |
| `/api/payments/*`  | Payment Service  |
| `/api/catalog/*`   | Catalog Service  |
| `/api/customers/*` | Customer Service |

Example NGINX-style configuration:

```nginx
location /api/orders/ {
    proxy_pass http://order-service;
}

location /api/payments/ {
    proxy_pass http://payment-service;
}

location /api/catalog/ {
    proxy_pass http://catalog-service;
}

location /api/customers/ {
    proxy_pass http://customer-service;
}
```

Routing can be based on more than path.

It can also use:

* HTTP method,
* host name,
* headers,
* tenant ID,
* region,
* API version,
* client type,
* feature flag,
* percentage rollout.

For example:

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    Version{API Version}

    V1[Legacy Order API]
    V2[New Order API]

    Request --> Gateway
    Gateway --> Version

    Version -->|Accept: v1| V1
    Version -->|Accept: v2| V2
```

This is useful during migrations and API version transitions.

---

#### Authentication

Authentication verifies who the caller is.

The API Gateway is often a good place to authenticate requests before they reach internal services.

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant Identity as Identity Provider
    participant Service as Backend Service

    Client->>Gateway: Request with access token
    Gateway->>Identity: Validate token or fetch keys
    Identity-->>Gateway: Token valid
    Gateway->>Service: Forward authenticated request
    Service-->>Gateway: Response
    Gateway-->>Client: Response
```

For JWT-based authentication, the gateway may verify the token signature and claims.

Example logic:

```ts
type AuthContext = {
  userId: string;
  roles: string[];
  tenantId?: string;
};

function authenticateRequest(req: Request): AuthContext {
  const authHeader = req.header("Authorization");

  if (!authHeader?.startsWith("Bearer ")) {
    throw new Error("Missing bearer token");
  }

  const token = authHeader.slice("Bearer ".length);
  const payload = verifyJwt(token);

  return {
    userId: payload.sub,
    roles: payload.roles ?? [],
    tenantId: payload.tenantId
  };
}
```

After authentication, the gateway can pass identity information downstream.

For example:

```http
X-User-Id: user_123
X-Tenant-Id: tenant_456
X-Request-Id: req_789
```

However, downstream services should not blindly trust headers from the public internet. The gateway must strip incoming spoofed identity headers and add its own trusted headers.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Service[Backend Service]

    Client -->|May include spoofed headers| Gateway
    Gateway -->|Strip and replace trusted identity headers| Service
```

---

#### Authorization

Authorization decides what the caller is allowed to do.

The gateway can enforce coarse-grained authorization, such as:

* user must be authenticated,
* caller must have a required role,
* API key must belong to a valid partner,
* tenant must be allowed to access this API,
* client must have the required scope.

Example:

```ts
function requireScope(auth: AuthContext, requiredScope: string): void {
  if (!auth.scopes.includes(requiredScope)) {
    throw new Error("Forbidden");
  }
}
```

Route-level authorization might look like:

| Route                        | Required scope    |
| ---------------------------- | ----------------- |
| `GET /api/orders`            | `orders:read`     |
| `POST /api/orders`           | `orders:write`    |
| `POST /api/payments/refunds` | `payments:refund` |
| `GET /api/admin/users`       | `admin:read`      |

The gateway can reject unauthorized requests before they hit backend services.

But fine-grained business authorization should usually remain in the domain service.

For example:

| Decision                                          | Best owner      |
| ------------------------------------------------- | --------------- |
| Is the user authenticated?                        | Gateway         |
| Does the token have `orders:write` scope?         | Gateway         |
| Can this user cancel this specific order?         | Order Service   |
| Can this refund be approved under current policy? | Payment Service |
| Can this customer access this invoice?            | Billing Service |

The gateway may know who the user is. The backend service usually knows the business rules.

---

#### Rate limiting

An API Gateway is a natural place to enforce rate limits.

Rate limiting protects backend services from overload and protects public APIs from abuse.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    RateLimiter[Rate Limiter]
    Service[Backend Service]

    Client --> Gateway
    Gateway --> RateLimiter

    RateLimiter -->|Allowed| Service
    RateLimiter -->|Rejected| TooMany[429 Too Many Requests]
```

Common rate limit dimensions include:

* per IP address,
* per API key,
* per user,
* per tenant,
* per route,
* per client application,
* per partner,
* global system limit.

Example response:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1714412400
```

Example token bucket logic:

```ts
type RateLimitResult = {
  allowed: boolean;
  remaining: number;
  retryAfterSeconds?: number;
};

async function checkRateLimit(
  key: string,
  limit: number,
  windowSeconds: number
): Promise<RateLimitResult> {
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, windowSeconds);
  }

  if (current > limit) {
    return {
      allowed: false,
      remaining: 0,
      retryAfterSeconds: await redis.ttl(key)
    };
  }

  return {
    allowed: true,
    remaining: limit - current
  };
}
```

Rate limits should be designed carefully. Too strict, and legitimate clients fail. Too loose, and backend services may be overwhelmed.

---

#### TLS termination

The gateway often terminates TLS.

That means clients connect securely to the gateway over HTTPS, and the gateway handles certificates.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway<br/>TLS Termination]
    Service[Backend Service]

    Client -->|HTTPS| Gateway
    Gateway -->|HTTP or mTLS| Service
```

In production systems, backend communication should still be protected. Common options include:

* private network traffic,
* mutual TLS between services,
* service mesh encryption,
* encrypted load balancer connections.

The gateway is the public edge, but internal traffic still needs security.

---

#### Request and response transformation

A gateway may perform light request or response transformation.

Examples:

* add request IDs,
* add identity headers,
* remove sensitive headers,
* normalize error formats,
* rewrite paths,
* convert public routes to internal routes,
* compress responses,
* handle CORS headers.

Example path rewrite:

```text
Public route:
GET /api/v1/orders/ord_123

Internal route:
GET /orders/ord_123
```

Example:

```ts
function rewriteOrderPath(publicPath: string): string {
  return publicPath.replace("/api/v1/orders", "/orders");
}
```

Response normalization may be useful when exposing a consistent public API:

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "The requested order does not exist."
  }
}
```

But transformation should stay limited. If the gateway starts deeply reshaping domain objects or implementing business rules, it can become a hidden monolith.

---

#### Gateway aggregation

Sometimes the gateway combines data from multiple services into one response.

This is called **gateway aggregation**.

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Shipping as Shipping Service

    Client->>Gateway: GET /order-summary/ord_123

    Gateway->>Orders: GET /orders/ord_123
    Gateway->>Payments: GET /payments?orderId=ord_123
    Gateway->>Shipping: GET /shipments?orderId=ord_123

    Orders-->>Gateway: Order details
    Payments-->>Gateway: Payment status
    Shipping-->>Gateway: Shipment status

    Gateway-->>Client: Combined order summary
```

Example response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "payment": {
    "status": "AUTHORIZED"
  },
  "shipment": {
    "status": "PENDING"
  }
}
```

Gateway aggregation can improve client performance, especially for mobile apps, by reducing round trips.

However, aggregation should be used carefully.

Good uses:

* simple composition for client convenience,
* reducing mobile latency,
* combining read-only data,
* hiding backend topology.

Risky uses:

* implementing checkout workflow in the gateway,
* enforcing complex business rules,
* performing multi-service transactions,
* owning domain state.

If aggregation becomes complex, consider a dedicated **Backend for Frontend**, **query service**, or **composition service** instead.

---

#### Protocol translation

An API Gateway can translate between external and internal protocols.

For example:

```mermaid
flowchart TD
    Client[External Client]
    Gateway[API Gateway]

    Rest[REST Request]
    Grpc[gRPC Service]
    Events[Async Message]

    Client --> Rest
    Rest --> Gateway

    Gateway --> Grpc
    Gateway --> Events
```

A public client may call HTTP/JSON:

```http
POST /api/payments/authorize
Content-Type: application/json
```

The gateway may call an internal gRPC service:

```proto
service PaymentService {
  rpc AuthorizePayment(AuthorizePaymentRequest)
      returns (AuthorizePaymentResponse);
}
```

Protocol translation is useful when you want external APIs to be simple and stable while internal services use protocols optimized for backend communication.

But protocol translation should not become deep domain translation. If business model translation is needed, that may belong in an Anti-Corruption Layer or a dedicated service.

---

#### API versioning

Gateways are often used to route API versions.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    V1[Order API v1]
    V2[Order API v2]

    Client --> Gateway

    Gateway -->|/v1/orders/*| V1
    Gateway -->|/v2/orders/*| V2
```

Versioning strategies include:

| Strategy            | Example                                          |
| ------------------- | ------------------------------------------------ |
| Path versioning     | `/v1/orders`                                     |
| Header versioning   | `Accept: application/vnd.company.orders.v2+json` |
| Query parameter     | `/orders?version=2`                              |
| Hostname versioning | `v2.api.company.com`                             |

The gateway can route older clients to v1 and newer clients to v2.

This is useful for gradual migration, but it does not eliminate the need for API governance. Old versions must eventually be deprecated or they will accumulate forever.

---

#### Gateway and service discovery

In dynamic environments, backend service locations change.

A gateway can integrate with service discovery.

```mermaid
flowchart TD
    Gateway[API Gateway]
    Registry[Service Registry]

    OrdersA[Order Service Instance A]
    OrdersB[Order Service Instance B]
    OrdersC[Order Service Instance C]

    Gateway --> Registry

    Registry --> OrdersA
    Registry --> OrdersB
    Registry --> OrdersC
```

Instead of hardcoding a single backend address, the gateway discovers healthy service instances.

In Kubernetes, the gateway may route to Kubernetes Services:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-service
spec:
  selector:
    app: orders
  ports:
    - port: 80
      targetPort: 3000
```

The gateway routes to `orders-service`, and Kubernetes handles endpoint discovery.

---

#### Gateway and observability

Because the gateway sees all incoming traffic, it is a valuable observability point.

It should capture:

* request ID,
* client ID,
* user or tenant ID when appropriate,
* route,
* backend target,
* status code,
* latency,
* request size,
* response size,
* rate-limit decisions,
* authentication failures,
* authorization failures,
* upstream errors.

Example structured log:

```json
{
  "requestId": "req_123",
  "clientId": "mobile-ios",
  "tenantId": "tenant_456",
  "method": "GET",
  "path": "/api/orders/ord_789",
  "backendService": "order-service",
  "statusCode": 200,
  "latencyMs": 47
}
```

The gateway should also propagate tracing headers downstream.

Example:

```http
X-Request-Id: req_123
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00
```

This lets teams trace a request from client through gateway to backend services.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]

    Client --> Gateway
    Gateway --> Orders
    Orders --> Payments
    Orders --> Inventory

    Trace[Distributed Trace]
    Client -. trace context .-> Gateway
    Gateway -. trace context .-> Orders
    Orders -. trace context .-> Payments
    Orders -. trace context .-> Inventory
```

---

#### Gateway as a security boundary

The API Gateway is often part of the security boundary.

It can enforce:

* TLS,
* authentication,
* authorization scopes,
* rate limits,
* request size limits,
* IP allowlists,
* bot protection,
* API key validation,
* CORS,
* threat detection,
* input schema validation,
* header sanitization.

```mermaid
flowchart TD
    Internet[Internet]
    Gateway[API Gateway]

    Auth[Auth Check]
    RateLimit[Rate Limit]
    Validation[Request Validation]
    Sanitization[Header Sanitization]

    Internal[Internal Services]

    Internet --> Gateway

    Gateway --> Auth
    Auth --> RateLimit
    RateLimit --> Validation
    Validation --> Sanitization
    Sanitization --> Internal
```

However, backend services should not assume the gateway is the only security layer.

Use defense in depth:

* backend services should verify trusted identity context,
* internal traffic should be restricted,
* service-to-service calls should use authentication when appropriate,
* sensitive operations should enforce authorization in the domain service,
* logs should avoid leaking sensitive data.

The gateway protects the edge. It should not be the only place security exists.

---

#### Public API Gateway vs internal gateway

Some organizations use different gateways for different audiences.

```mermaid
flowchart TD
    PublicClients[Public Clients]
    InternalTools[Internal Tools]

    PublicGateway[Public API Gateway]
    InternalGateway[Internal API Gateway]

    Services[Backend Services]

    PublicClients --> PublicGateway
    InternalTools --> InternalGateway

    PublicGateway --> Services
    InternalGateway --> Services
```

A public gateway may prioritize:

* API keys,
* OAuth scopes,
* quotas,
* developer portal integration,
* public documentation,
* strict backward compatibility.

An internal gateway may prioritize:

* service discovery,
* internal identity,
* team-level access controls,
* faster iteration,
* observability,
* lower latency.

Separating public and internal gateways can reduce risk because public APIs usually require stronger governance and compatibility guarantees.

---

#### Gateway vs Backend for Frontend

An API Gateway is a general entry point.

A **Backend for Frontend**, or **BFF**, is a backend tailored to a specific client experience, such as web, iOS, Android, or admin console.

```mermaid
flowchart TD
    Web[Web App]
    Mobile[Mobile App]
    Admin[Admin Console]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]
    AdminBFF[Admin BFF]

    Gateway[Shared Gateway]

    Services[Backend Services]

    Web --> WebBFF
    Mobile --> MobileBFF
    Admin --> AdminBFF

    WebBFF --> Gateway
    MobileBFF --> Gateway
    AdminBFF --> Gateway

    Gateway --> Services
```

Use an API Gateway for common edge concerns.

Use a BFF when each client needs different API shapes, aggregation, or presentation-specific behavior.

For example:

| Need                               | Better fit  |
| ---------------------------------- | ----------- |
| TLS termination                    | API Gateway |
| API key validation                 | API Gateway |
| Global rate limiting               | API Gateway |
| iOS-specific order screen response | Mobile BFF  |
| Admin dashboard aggregation        | Admin BFF   |
| Web-specific view model            | Web BFF     |

A common architecture combines both:

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    BFF[Backend for Frontend]
    Services[Domain Services]

    Client --> Gateway
    Gateway --> BFF
    BFF --> Services
```

The gateway handles edge concerns. The BFF handles client-specific composition.

---

#### Gateway vs service mesh

An API Gateway and a service mesh solve different problems.

```mermaid
flowchart TD
    ExternalClient[External Client]
    Gateway[API Gateway]

    ServiceA[Service A]
    ServiceB[Service B]
    ServiceC[Service C]

    Mesh[Service Mesh]

    ExternalClient --> Gateway
    Gateway --> ServiceA

    ServiceA --> Mesh
    Mesh --> ServiceB
    Mesh --> ServiceC
```

The gateway usually handles **north-south traffic**, meaning traffic entering the system from clients.

The service mesh usually handles **east-west traffic**, meaning service-to-service communication inside the system.

| Concern                               | API Gateway | Service Mesh |
| ------------------------------------- | ----------- | ------------ |
| External client entry point           | Yes         | No           |
| Public API routing                    | Yes         | Usually no   |
| Service-to-service mTLS               | Sometimes   | Yes          |
| Internal traffic policies             | Limited     | Yes          |
| Public rate limiting                  | Yes         | Usually no   |
| Request authentication at edge        | Yes         | Sometimes    |
| Internal retries and circuit breaking | Sometimes   | Yes          |
| Developer API management              | Yes         | No           |

They are complementary, not replacements for each other.

---

#### Example implementation: simple Node gateway

Here is a simplified API Gateway in Node.js using Express and `http-proxy-middleware`.

```ts
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

const app = express();

function requireAuth(req: express.Request, res: express.Response, next: express.NextFunction) {
  const authorization = req.header("Authorization");

  if (!authorization?.startsWith("Bearer ")) {
    res.status(401).json({
      error: "UNAUTHORIZED",
      message: "Missing or invalid access token"
    });
    return;
  }

  // In a real gateway, verify the JWT or call an identity provider.
  next();
}

app.use((req, _res, next) => {
  req.headers["x-request-id"] =
    req.header("X-Request-Id") ?? crypto.randomUUID();
  next();
});

app.use("/api/orders", requireAuth, createProxyMiddleware({
  target: "http://orders-service:3000",
  changeOrigin: true,
  pathRewrite: {
    "^/api/orders": "/orders"
  }
}));

app.use("/api/payments", requireAuth, createProxyMiddleware({
  target: "http://payments-service:3000",
  changeOrigin: true,
  pathRewrite: {
    "^/api/payments": "/payments"
  }
}));

app.use("/api/catalog", createProxyMiddleware({
  target: "http://catalog-service:3000",
  changeOrigin: true,
  pathRewrite: {
    "^/api/catalog": "/catalog"
  }
}));

app.listen(8080, () => {
  console.log("API Gateway listening on port 8080");
});
```

This example shows the basic idea:

* receive public requests,
* apply edge concerns,
* route to backend services,
* rewrite paths.

A production gateway would need more:

* real JWT validation,
* rate limiting,
* structured logging,
* tracing,
* request timeouts,
* circuit breakers,
* retries where safe,
* service discovery,
* secure header handling,
* configuration management,
* metrics,
* deployment automation.

---

#### Example: gateway aggregation endpoint

A gateway may expose a convenience endpoint that aggregates read-only data.

```ts
app.get("/api/order-summary/:orderId", requireAuth, async (req, res) => {
  const { orderId } = req.params;

  const [order, payment, shipment] = await Promise.all([
    ordersClient.getOrder(orderId),
    paymentsClient.getPaymentByOrderId(orderId),
    shippingClient.getShipmentByOrderId(orderId)
  ]);

  res.json({
    orderId: order.id,
    orderStatus: order.status,
    totalAmount: order.totalAmount,
    paymentStatus: payment.status,
    shipmentStatus: shipment.status
  });
});
```

This can be useful, but watch the boundary carefully.

This endpoint is probably acceptable because it composes read data.

This would be risky inside the gateway:

```ts
app.post("/api/checkout", async (req, res) => {
  const order = await ordersClient.createOrder(req.body);
  const payment = await paymentsClient.authorize(order);
  const reservation = await inventoryClient.reserve(order);
  await ordersClient.confirm(order.id);

  res.json({ order, payment, reservation });
});
```

That is no longer just routing or simple composition. It is a business workflow. It likely belongs in a Checkout Service, Saga orchestrator, or domain workflow service.

---

#### Deployment models

An API Gateway can be deployed in different ways.

##### Managed gateway

Examples include cloud-managed API gateways.

```mermaid
flowchart TD
    Client[Client]
    ManagedGateway[Managed API Gateway]
    Services[Backend Services]

    Client --> ManagedGateway
    ManagedGateway --> Services
```

Benefits:

* less infrastructure to manage,
* built-in auth integrations,
* rate limiting,
* monitoring,
* scaling,
* developer portal support.

Trade-offs:

* cloud provider dependency,
* configuration complexity,
* pricing,
* limits on customization.

##### Self-hosted gateway

Examples include NGINX, Envoy, Kong, Traefik, or custom gateway services.

```mermaid
flowchart TD
    Client[Client]
    SelfHosted[Self-Hosted Gateway]
    Services[Backend Services]

    Client --> SelfHosted
    SelfHosted --> Services
```

Benefits:

* more control,
* can run anywhere,
* customizable plugins,
* good for hybrid environments.

Trade-offs:

* team owns operations,
* scaling and patching are your responsibility,
* plugin quality varies.

##### Application-level gateway

A team may build a custom gateway in application code.

```mermaid
flowchart TD
    Client[Client]
    CustomGateway[Custom Gateway App]
    Services[Backend Services]

    Client --> CustomGateway
    CustomGateway --> Services
```

Benefits:

* maximum flexibility,
* easy custom aggregation,
* application-specific behavior.

Trade-offs:

* high risk of becoming a monolith,
* must build operational features yourself,
* may duplicate features available in gateway products.

---

#### When to use it

Use an API Gateway when:

* clients need access to multiple backend services,
* you want one stable public entry point,
* backend services should not be exposed directly,
* clients should not know internal service locations,
* you need centralized authentication,
* you need API-level rate limiting,
* you need request routing by path, version, tenant, or region,
* you need TLS termination at the edge,
* you need public API governance,
* you are exposing APIs to mobile apps, web apps, partners, or external developers.

It is especially useful in microservice systems where client applications would otherwise depend directly on many services.

---

#### When not to use it

An API Gateway may be unnecessary or overkill when:

* the system has only one backend service,
* there are no external clients,
* clients already communicate through a single backend,
* the gateway would only forward traffic without adding value,
* ultra-low latency is more important than centralized edge control,
* the team cannot operate or configure the gateway safely.

Also avoid using a gateway as a substitute for proper service design. A gateway can hide backend complexity from clients, but it cannot fix poor service boundaries by itself.

---

#### Benefits

**1. Hides internal service topology**

Clients do not need to know where every backend service lives.

**2. Centralizes edge concerns**

Authentication, TLS, CORS, rate limiting, and routing can be handled consistently.

**3. Improves client simplicity**

Clients call one API surface instead of many backend services.

**4. Supports API versioning and migration**

The gateway can route old and new versions during transitions.

**5. Improves security**

Backend services do not need to be directly exposed to the internet.

**6. Enables controlled rollout**

Traffic can be routed by version, tenant, region, feature flag, or percentage.

**7. Improves observability at the edge**

The gateway can measure traffic, latency, errors, and client behavior.

---

#### Trade-offs

**1. Can become a bottleneck**

All traffic flows through the gateway, so it must be highly available and scalable.

**2. Can become a hidden monolith**

If business logic accumulates in the gateway, teams lose service autonomy.

**3. Adds operational complexity**

The gateway must be deployed, configured, monitored, secured, and upgraded.

**4. Adds latency**

Every request has at least one extra hop.

**5. Can obscure service ownership**

If too much behavior sits in the gateway, it becomes unclear which team owns what.

**6. Configuration can become complex**

Many routes, versions, tenants, and policies can be hard to manage.

**7. Failure affects many clients**

A gateway outage can impact the entire system.

---

#### Common mistakes

**Mistake 1: Putting business logic in the gateway**

The gateway should not decide how payments work, how inventory is reserved, or whether an order can be cancelled.

**Mistake 2: Building a custom gateway too early**

Many gateway needs can be handled by existing tools. Custom gateways can become expensive to maintain.

**Mistake 3: Exposing internal service contracts directly**

The public API should be stable and intentional, not just a mirror of internal service APIs.

**Mistake 4: Forgetting backend authorization**

The gateway can enforce coarse authorization, but services should still protect sensitive business operations.

**Mistake 5: No timeout strategy**

If backend services hang, gateway requests can pile up and cause cascading failure.

**Mistake 6: No observability**

A gateway without logs, metrics, and traces becomes a blind spot.

**Mistake 7: Making one gateway serve every possible client need**

If web, mobile, admin, and partners need very different APIs, use BFFs or separate gateway configurations.

**Mistake 8: Not stripping untrusted headers**

Clients should not be allowed to spoof identity, tenant, or internal routing headers.

---

#### Practical design checklist

When designing an API Gateway, answer:

* Who are the clients?
* Is this a public, partner, internal, or private gateway?
* What routes should the gateway expose?
* Which backend service owns each route?
* What authentication mechanism is used?
* What authorization checks belong at the gateway?
* What authorization checks remain in backend services?
* What rate limits are needed?
* How are routes versioned?
* How are clients migrated between versions?
* What headers are allowed, removed, or added?
* What request size limits are needed?
* What timeouts should apply to each route?
* Are retries safe for this route?
* How are errors normalized?
* How are request IDs and tracing headers propagated?
* How is the gateway configured and deployed?
* How is gateway configuration tested?
* What happens if a backend service is unavailable?
* What happens if the gateway itself fails?
* Who owns the gateway?

A gateway design is probably healthy if:

* it handles edge concerns consistently,
* it keeps business logic in domain services,
* it exposes a stable public API,
* it hides internal topology,
* it has clear route ownership,
* it has strong observability,
* it can scale horizontally,
* it has a safe configuration process.

A gateway design is probably unhealthy if:

* every team adds business rules to it,
* it contains complex workflows,
* it directly accesses service databases,
* it becomes the only place authorization exists,
* it has unclear ownership,
* it is hard to test changes,
* it is a single point of failure,
* it mirrors every internal service API without design.

---

#### Related patterns

| Pattern                   | Relationship                                                         |
| ------------------------- | -------------------------------------------------------------------- |
| Gateway Routing           | The gateway routes requests to backend services                      |
| Gateway Aggregation       | The gateway combines responses from multiple services                |
| Gateway Offloading        | The gateway handles edge concerns such as TLS, auth, and rate limits |
| Backends for Frontends    | Often used behind or alongside a gateway for client-specific APIs    |
| Service Discovery         | Lets the gateway find backend service instances                      |
| Circuit Breaker           | Protects the gateway from failing backend services                   |
| Retry                     | Can be applied carefully for safe idempotent requests                |
| Rate Limiting             | Common gateway responsibility                                        |
| Strangler Fig Pattern     | Gateway can route traffic between legacy and new systems             |
| Anti-Corruption Layer     | May sit behind a gateway to translate legacy models                  |
| Consumer-Driven Contracts | Helps ensure gateway-facing APIs meet client expectations            |
| Blue-Green Deployment     | Gateway can switch traffic between environments                      |
| Shadow Deployment         | Gateway can duplicate traffic to new services for validation         |

---

#### Summary

An API Gateway is a single entry point that lets clients access backend services without knowing the internal service topology.

The central idea is:

> Clients talk to one stable API boundary; the gateway routes and protects traffic to backend services.

A good API Gateway handles edge concerns such as:

* routing,
* authentication,
* coarse authorization,
* TLS termination,
* rate limiting,
* request validation,
* API versioning,
* observability,
* and controlled traffic management.

The gateway should not become the owner of business logic. Business rules belong in the services that own the domain.

Used well, an API Gateway simplifies clients, improves security, and gives teams a controlled boundary for operating microservice APIs. Used poorly, it becomes a bottleneck, a single point of failure, or a hidden monolith.


---

### 8. Gateway Routing

#### What it is

**Gateway Routing** is the API Gateway pattern where incoming requests are directed to backend services based on request attributes.

The gateway receives the request, evaluates routing rules, and forwards the request to the correct backend service.

Common routing attributes include:

* request path,
* HTTP method,
* host name,
* headers,
* query parameters,
* API version,
* tenant ID,
* region,
* user segment,
* feature flag,
* percentage rollout,
* service health,
* deployment environment.

At its simplest, gateway routing looks like this:

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Orders[Order Service]
    Payments[Payment Service]
    Catalog[Catalog Service]
    Customers[Customer Service]

    Client --> Gateway

    Gateway -->|/orders/*| Orders
    Gateway -->|/payments/*| Payments
    Gateway -->|/catalog/*| Catalog
    Gateway -->|/customers/*| Customers
```

The client sees one stable API surface, such as:

```text
https://api.example.com
```

Internally, the gateway may route to many independently deployed services.

The central idea is:

> The client should know the public API contract, not the internal service topology.

---

#### Why this pattern exists

In a microservice architecture, backend services are split by capability, subdomain, workflow, or ownership.

For example:

```mermaid
flowchart TD
    Backend[Backend System]

    Backend --> Orders[Order Service]
    Backend --> Payments[Payment Service]
    Backend --> Inventory[Inventory Service]
    Backend --> Catalog[Catalog Service]
    Backend --> Shipping[Shipping Service]
    Backend --> Support[Support Service]
```

Without gateway routing, clients may need to know every service address:

```mermaid
flowchart TD
    Client[Client]

    Client --> OrdersURL[orders.internal.example.com]
    Client --> PaymentsURL[payments.internal.example.com]
    Client --> InventoryURL[inventory.internal.example.com]
    Client --> CatalogURL[catalog.internal.example.com]
    Client --> ShippingURL[shipping.internal.example.com]
```

That creates direct coupling between clients and backend topology.

If the Order Service is renamed, moved, split, merged, or versioned, every client that calls it directly may need to change.

Gateway routing avoids this by creating a stable external entry point:

```mermaid
flowchart TD
    Client[Client]
    PublicAPI[api.example.com]
    Gateway[Gateway Routing Layer]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Catalog[Catalog Service]
    Shipping[Shipping Service]

    Client --> PublicAPI
    PublicAPI --> Gateway

    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Inventory
    Gateway --> Catalog
    Gateway --> Shipping
```

The gateway becomes the controlled boundary between the public API and internal services.

---

#### What it solves

Gateway Routing solves the problem of exposing many internal services through one stable external interface.

It helps with:

* hiding internal service names,
* hiding internal network locations,
* routing old and new API versions,
* routing tenants to different backends,
* routing users to regional deployments,
* routing traffic during migrations,
* routing traffic during canary or blue-green releases,
* moving capabilities between services without changing clients,
* centralizing routing policy.

For example, the client may call:

```http
GET /api/orders/ord_123
```

The gateway may route that to:

```text
http://orders-service.internal/orders/ord_123
```

Later, the backend may change to:

```text
http://orders-v2-service.internal/orders/ord_123
```

The client does not need to know. Only the gateway route changes.

---

#### Basic path-based routing

The most common form is **path-based routing**.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    Route{Path Match}

    Orders[Order Service]
    Payments[Payment Service]
    Catalog[Catalog Service]
    Legacy[Legacy System]

    Request --> Gateway
    Gateway --> Route

    Route -->|/api/orders/*| Orders
    Route -->|/api/payments/*| Payments
    Route -->|/api/catalog/*| Catalog
    Route -->|default| Legacy
```

Example route table:

| Public path        | Backend          |
| ------------------ | ---------------- |
| `/api/orders/*`    | Order Service    |
| `/api/payments/*`  | Payment Service  |
| `/api/catalog/*`   | Catalog Service  |
| `/api/customers/*` | Customer Service |
| `/api/reports/*`   | Legacy System    |

Example NGINX-style configuration:

```nginx
location /api/orders/ {
    proxy_pass http://orders-service;
}

location /api/payments/ {
    proxy_pass http://payments-service;
}

location /api/catalog/ {
    proxy_pass http://catalog-service;
}

location /api/customers/ {
    proxy_pass http://customers-service;
}

location / {
    proxy_pass http://legacy-system;
}
```

This is simple, predictable, and easy to understand.

Path-based routing works well when the public API structure maps cleanly to backend service ownership.

---

#### Method-based routing

Sometimes the same path should route differently depending on the HTTP method.

For example:

| Request                    | Backend                    |
| -------------------------- | -------------------------- |
| `GET /api/products/{id}`   | Catalog Query Service      |
| `POST /api/products`       | Catalog Management Service |
| `PATCH /api/products/{id}` | Catalog Management Service |
| `GET /api/products/search` | Search Service             |

Diagram:

```mermaid
flowchart TD
    Request[Incoming Product Request]
    Gateway[API Gateway]

    Method{HTTP Method}

    Query[Catalog Query Service]
    Management[Catalog Management Service]
    Search[Search Service]

    Request --> Gateway
    Gateway --> Method

    Method -->|GET /products/search| Search
    Method -->|GET /products/id| Query
    Method -->|POST or PATCH| Management
```

Example route logic:

```ts
type RouteTarget = {
  serviceName: string;
  baseUrl: string;
};

function routeProductRequest(req: Request): RouteTarget {
  if (req.method === "GET" && req.path === "/api/products/search") {
    return {
      serviceName: "search-service",
      baseUrl: "http://search-service"
    };
  }

  if (req.method === "GET" && req.path.startsWith("/api/products/")) {
    return {
      serviceName: "catalog-query-service",
      baseUrl: "http://catalog-query-service"
    };
  }

  if (
    ["POST", "PUT", "PATCH", "DELETE"].includes(req.method) &&
    req.path.startsWith("/api/products")
  ) {
    return {
      serviceName: "catalog-management-service",
      baseUrl: "http://catalog-management-service"
    };
  }

  throw new Error("No route found");
}
```

This can be useful when read and write workloads are separated.

It is also common in systems using CQRS, where reads and writes are handled by different services or models.

---

#### Host-based routing

With **host-based routing**, the gateway routes based on the domain name.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    Host{Host Header}

    PublicAPI[Public API Services]
    PartnerAPI[Partner API Services]
    AdminAPI[Admin Services]

    Request --> Gateway
    Gateway --> Host

    Host -->|api.example.com| PublicAPI
    Host -->|partners.example.com| PartnerAPI
    Host -->|admin.example.com| AdminAPI
```

Example:

| Host                   | Backend                   |
| ---------------------- | ------------------------- |
| `api.example.com`      | Public API Gateway routes |
| `partners.example.com` | Partner API services      |
| `admin.example.com`    | Admin backend services    |
| `internal.example.com` | Internal tools            |

This is useful when different audiences need different API surfaces.

For example:

* public users use `api.example.com`,
* partners use `partners.example.com`,
* employees use `admin.example.com`,
* internal services use `internal.example.com`.

Host-based routing often pairs well with separate authentication policies, rate limits, and monitoring dashboards.

---

#### Header-based routing

With **header-based routing**, the gateway routes based on request headers.

This is useful for API versions, experiments, client types, regions, or internal testing.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    Header{Header Value}

    V1[Service v1]
    V2[Service v2]
    Beta[Beta Service]

    Request --> Gateway
    Gateway --> Header

    Header -->|X-API-Version: 1| V1
    Header -->|X-API-Version: 2| V2
    Header -->|X-Beta: true| Beta
```

Example:

```http
GET /api/orders/ord_123
X-API-Version: 2
```

Route result:

```text
orders-service-v2
```

Example route logic:

```ts
function routeByVersion(req: Request): RouteTarget {
  const version = req.header("X-API-Version") ?? "1";

  if (version === "2") {
    return {
      serviceName: "orders-v2",
      baseUrl: "http://orders-v2-service"
    };
  }

  return {
    serviceName: "orders-v1",
    baseUrl: "http://orders-v1-service"
  };
}
```

Header-based routing is powerful, but it can become hard to debug if routing decisions are not logged clearly.

Always log the selected route and the header values that influenced routing.

---

#### API version routing

API version routing directs requests to different service versions.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Version{API Version}

    OrdersV1[Order API v1]
    OrdersV2[Order API v2]

    Client --> Gateway
    Gateway --> Version

    Version -->|/v1/orders/*| OrdersV1
    Version -->|/v2/orders/*| OrdersV2
```

Common versioning strategies include:

| Versioning style    | Example                                          |
| ------------------- | ------------------------------------------------ |
| Path versioning     | `/v1/orders`                                     |
| Header versioning   | `X-API-Version: 2`                               |
| Accept header       | `Accept: application/vnd.company.orders.v2+json` |
| Hostname versioning | `v2.api.example.com`                             |

Path versioning is easy to see:

```http
GET /v1/orders/ord_123
GET /v2/orders/ord_123
```

Header versioning keeps URLs cleaner but is less visible:

```http
GET /orders/ord_123
X-API-Version: 2
```

Gateway version routing helps old and new clients coexist:

```mermaid
flowchart TD
    OldClient[Old Mobile App]
    NewClient[New Web App]
    Gateway[API Gateway]

    OrdersV1[Order Service v1]
    OrdersV2[Order Service v2]

    OldClient --> Gateway
    NewClient --> Gateway

    Gateway -->|v1 route| OrdersV1
    Gateway -->|v2 route| OrdersV2
```

This is useful during gradual API migration.

However, version routing should have lifecycle management. Old versions should have owners, monitoring, and deprecation plans.

---

#### Tenant-based routing

In multi-tenant systems, the gateway may route requests based on tenant.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    Tenant{Tenant}

    Shared[Shared Services]
    Enterprise[Enterprise Tenant Cluster]
    Regulated[Regulated Tenant Environment]

    Request --> Gateway
    Gateway --> Tenant

    Tenant -->|standard tenants| Shared
    Tenant -->|enterprise tenant| Enterprise
    Tenant -->|regulated tenant| Regulated
```

Tenant ID may come from:

* subdomain,
* JWT claim,
* request header,
* API key,
* path segment,
* mTLS certificate,
* session context.

Examples:

```http
GET /api/orders
X-Tenant-Id: tenant_123
```

or:

```text
https://tenant-123.api.example.com/orders
```

or JWT claim:

```json
{
  "sub": "user_123",
  "tenantId": "tenant_123",
  "scope": "orders:read"
}
```

Example route logic:

```ts
function routeByTenant(req: Request, auth: AuthContext): RouteTarget {
  const tenantId = auth.tenantId;

  if (tenantId === "enterprise_acme") {
    return {
      serviceName: "orders-acme-dedicated",
      baseUrl: "http://orders-acme-dedicated"
    };
  }

  if (auth.complianceTier === "regulated") {
    return {
      serviceName: "orders-regulated",
      baseUrl: "http://orders-regulated"
    };
  }

  return {
    serviceName: "orders-shared",
    baseUrl: "http://orders-shared"
  };
}
```

Tenant routing is useful when some customers need:

* dedicated infrastructure,
* special compliance controls,
* data residency,
* custom scaling,
* isolated deployments,
* premium reliability.

Be careful not to trust tenant headers directly from clients. Tenant identity should usually come from authenticated context, not from an arbitrary user-provided header.

---

#### Region-based routing

Region-based routing directs users to services in the correct geographic region.

```mermaid
flowchart TD
    Client[Client]
    Gateway[Global Gateway]

    Region{Region}

    US[US Services]
    EU[EU Services]
    APAC[APAC Services]

    Client --> Gateway
    Gateway --> Region

    Region -->|United States| US
    Region -->|European Union| EU
    Region -->|Asia-Pacific| APAC
```

Routing may be based on:

* user profile,
* tenant configuration,
* data residency rules,
* DNS geolocation,
* IP geolocation,
* request header from an upstream edge,
* region encoded in the API key.

Example:

| Tenant            | Required region | Backend       |
| ----------------- | --------------- | ------------- |
| `tenant_us_001`   | US              | `orders-us`   |
| `tenant_eu_001`   | EU              | `orders-eu`   |
| `tenant_apac_001` | APAC            | `orders-apac` |

Region routing is especially important for:

* latency,
* data residency,
* disaster recovery,
* regulatory compliance,
* regional failover.

Example:

```ts
function routeByRegion(tenant: Tenant): RouteTarget {
  switch (tenant.dataRegion) {
    case "US":
      return {
        serviceName: "orders-us",
        baseUrl: "https://orders.us.internal"
      };

    case "EU":
      return {
        serviceName: "orders-eu",
        baseUrl: "https://orders.eu.internal"
      };

    case "APAC":
      return {
        serviceName: "orders-apac",
        baseUrl: "https://orders.apac.internal"
      };
  }
}
```

Region routing must be designed carefully. Accidentally routing EU customer data to a non-EU service may create legal and compliance problems.

---

#### Canary routing

Gateway Routing is commonly used for canary releases.

A **canary release** sends a small percentage of traffic to a new version before rolling it out broadly.

```mermaid
flowchart TD
    Requests[Incoming Requests]
    Gateway[API Gateway]

    Decision{Traffic Split}

    Stable[Orders v1 Stable]
    Canary[Orders v2 Canary]

    Requests --> Gateway
    Gateway --> Decision

    Decision -->|95 percent| Stable
    Decision -->|5 percent| Canary
```

Example traffic split:

| Version   | Traffic |
| --------- | ------: |
| Orders v1 |     95% |
| Orders v2 |      5% |

If metrics look good, increase traffic gradually:

```mermaid
flowchart TD
    Start[Start]
    P1[1 percent]
    P5[5 percent]
    P25[25 percent]
    P50[50 percent]
    P100[100 percent]

    Start --> P1
    P1 --> P5
    P5 --> P25
    P25 --> P50
    P50 --> P100
```

Example pseudo-code:

```ts
function routeCanary(req: Request): RouteTarget {
  const rolloutPercentage = 5;
  const userId = req.header("X-User-Id") ?? "anonymous";

  const bucket = stableHash(userId) % 100;

  if (bucket < rolloutPercentage) {
    return {
      serviceName: "orders-v2",
      baseUrl: "http://orders-v2"
    };
  }

  return {
    serviceName: "orders-v1",
    baseUrl: "http://orders-v1"
  };
}
```

Using a stable hash keeps the same user on the same version during the rollout, which avoids inconsistent behavior across requests.

---

#### Blue-green routing

Gateway Routing can also support blue-green deployments.

In blue-green deployment, two environments exist:

* **Blue**: current production environment,
* **Green**: new candidate environment.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Blue[Blue Environment]
    Green[Green Environment]

    Client --> Gateway

    Gateway -->|Current production traffic| Blue
    Gateway -. standby .-> Green
```

After validation, the gateway switches traffic:

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Blue[Blue Environment]
    Green[Green Environment]

    Client --> Gateway

    Gateway -. standby .-> Blue
    Gateway -->|Production traffic| Green
```

Benefits:

* fast rollback,
* clear environment separation,
* safer release validation,
* minimal downtime.

Rollback is just a routing change back to Blue.

```mermaid
flowchart TD
    Problem[Problem detected]
    Gateway[API Gateway]
    Green[Green Environment]
    Blue[Blue Environment]

    Problem --> Gateway
    Gateway -. stop traffic .-> Green
    Gateway -->|rollback| Blue
```

Blue-green routing is simpler when services are stateless and database migrations are backward compatible.

---

#### Migration routing

Gateway Routing is often used during legacy migration, especially with the Strangler Fig Pattern.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Legacy[Legacy Monolith]
    NewOrders[New Order Service]
    NewCatalog[New Catalog Service]

    Client --> Gateway

    Gateway -->|/orders/*| NewOrders
    Gateway -->|/catalog/*| NewCatalog
    Gateway -->|unmigrated routes| Legacy
```

As each capability is migrated, the route changes.

Example migration route table:

| Route             | Before migration | After migration |
| ----------------- | ---------------- | --------------- |
| `/api/products/*` | Legacy Monolith  | Catalog Service |
| `/api/orders/*`   | Legacy Monolith  | Order Service   |
| `/api/payments/*` | Legacy Monolith  | Payment Service |
| `/api/reports/*`  | Legacy Monolith  | Legacy Monolith |

Gateway routing lets the migration happen slice by slice.

This is safer than replacing the whole system at once.

---

#### Fallback routing

Sometimes the gateway can route to a fallback service when the primary service is unavailable.

```mermaid
flowchart TD
    Request[Request]
    Gateway[API Gateway]

    Health{Primary Healthy?}

    Primary[Primary Service]
    Fallback[Fallback Service or Cached Response]

    Request --> Gateway
    Gateway --> Health

    Health -->|Yes| Primary
    Health -->|No| Fallback
```

Examples:

* route product search to a cached search index if search is degraded,
* return cached catalog data when the catalog service is unavailable,
* route to an older service version if a canary fails,
* send traffic to another region during regional outage.

Fallbacks must be used carefully. They are usually safer for read operations than write operations.

A fallback for `GET /products/{id}` may be acceptable.

A fallback for `POST /payments/authorize` is much riskier.

---

#### Route matching order

Routing rules must have a clear priority order.

For example:

```text
/api/orders/search
/api/orders/{orderId}
/api/orders/*
/api/*
```

If broad routes are evaluated before specific routes, requests may go to the wrong service.

Bad order:

```text
/api/orders/*
/api/orders/search
```

The broader route may catch `/api/orders/search` before the search route gets a chance.

Better order:

```text
/api/orders/search
/api/orders/{orderId}
/api/orders/*
```

Diagram:

```mermaid
flowchart TD
    Request[GET /api/orders/search]
    Rule1{Match /api/orders/search?}
    Rule2{Match /api/orders/id?}
    Rule3{Match /api/orders/*?}

    Search[Search Service]
    Orders[Order Service]
    NotFound[404 Not Found]

    Request --> Rule1

    Rule1 -->|Yes| Search
    Rule1 -->|No| Rule2

    Rule2 -->|Yes| Orders
    Rule2 -->|No| Rule3

    Rule3 -->|Yes| Orders
    Rule3 -->|No| NotFound
```

Route ordering should be documented and tested.

---

#### Route configuration as code

As routing grows, configuration should be versioned, reviewed, and tested.

Route rules should not be changed casually through manual console edits unless there is a strong operational reason.

Example YAML route configuration:

```yaml
routes:
  - name: orders-v1
    match:
      pathPrefix: /api/v1/orders
    target:
      service: orders-v1
      url: http://orders-v1
    policies:
      authRequired: true
      rateLimit:
        requestsPerMinute: 600

  - name: orders-v2
    match:
      pathPrefix: /api/v2/orders
    target:
      service: orders-v2
      url: http://orders-v2
    policies:
      authRequired: true
      rateLimit:
        requestsPerMinute: 600

  - name: catalog
    match:
      pathPrefix: /api/catalog
    target:
      service: catalog
      url: http://catalog-service
    policies:
      authRequired: false
      cache:
        ttlSeconds: 60
```

Configuration as code gives you:

* pull request review,
* version history,
* automated tests,
* rollback,
* ownership metadata,
* auditability,
* environment consistency.

---

#### Testing routing rules

Gateway routing should be tested like application logic.

A simple routing test might look like this:

```ts
describe("gateway routing", () => {
  it("routes order API to the order service", () => {
    const target = routeRequest({
      method: "GET",
      path: "/api/orders/ord_123",
      headers: {}
    });

    expect(target.serviceName).toBe("orders-service");
  });

  it("routes catalog search to the search service", () => {
    const target = routeRequest({
      method: "GET",
      path: "/api/catalog/search",
      headers: {}
    });

    expect(target.serviceName).toBe("search-service");
  });

  it("routes v2 requests to orders-v2", () => {
    const target = routeRequest({
      method: "GET",
      path: "/api/orders/ord_123",
      headers: {
        "X-API-Version": "2"
      }
    });

    expect(target.serviceName).toBe("orders-v2");
  });
});
```

Useful routing tests include:

| Test type         | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| Path match tests  | Verify routes go to the expected backend        |
| Priority tests    | Verify specific routes win over broad routes    |
| Version tests     | Verify API versions route correctly             |
| Tenant tests      | Verify tenants route to the correct environment |
| Region tests      | Verify data residency routing                   |
| Canary tests      | Verify traffic split logic                      |
| Auth policy tests | Verify protected routes require authentication  |
| Fallback tests    | Verify degraded routes behave safely            |
| Negative tests    | Verify unknown routes return 404                |

Routing bugs can be severe because they may send traffic to the wrong service, wrong version, wrong tenant environment, or wrong region.

---

#### Observability for gateway routing

Every routed request should produce useful telemetry.

At minimum, log:

* request ID,
* route name,
* matched rule,
* target service,
* target version,
* tenant ID when appropriate,
* region when appropriate,
* status code,
* latency,
* retry count,
* fallback used or not,
* canary bucket if applicable.

Example structured log:

```json
{
  "requestId": "req_123",
  "method": "GET",
  "path": "/api/orders/ord_456",
  "matchedRoute": "orders-v2",
  "targetService": "orders-service-v2",
  "tenantId": "tenant_789",
  "region": "US",
  "statusCode": 200,
  "latencyMs": 42,
  "canary": false
}
```

This helps answer:

* Which route handled this request?
* Which backend received it?
* Did the request go to the expected version?
* Did a tenant route to the correct environment?
* Are canary users seeing more errors?
* Is one route slower than others?
* Are fallback routes being used too often?

Without this observability, routing problems are difficult to debug.

---

#### Security considerations

Gateway routing is security-sensitive.

Bad routing can expose internal services or send users to the wrong tenant’s data.

Important security rules:

* Do not trust client-provided internal routing headers.
* Strip headers such as `X-User-Id`, `X-Tenant-Id`, and `X-Internal-Role` from external requests.
* Recreate trusted identity headers only after authentication.
* Validate tenant access before tenant routing.
* Keep admin routes separate from public routes.
* Restrict direct access to backend services.
* Use allowlists for sensitive routes.
* Ensure route changes are reviewed.
* Log route decisions for auditability.

Example dangerous request:

```http
GET /api/orders
X-Tenant-Id: enterprise_customer
X-Internal-Role: admin
```

The gateway should not trust those headers from an external client.

A safer flow:

```mermaid
flowchart TD
    Client[Client Request]
    Gateway[API Gateway]

    Strip[Strip untrusted internal headers]
    Auth[Authenticate token]
    Context[Build trusted routing context]
    Route[Route request]

    Backend[Backend Service]

    Client --> Gateway
    Gateway --> Strip
    Strip --> Auth
    Auth --> Context
    Context --> Route
    Route --> Backend
```

The trusted tenant ID should come from a verified token, API key, or identity provider.

---

#### Timeout and retry policy by route

Different routes need different timeout and retry behavior.

For example:

| Route                            | Timeout | Retry?                          | Reason                      |
| -------------------------------- | ------: | ------------------------------- | --------------------------- |
| `GET /api/catalog/products/{id}` |  500 ms | Yes                             | Read-only and safe to retry |
| `GET /api/orders/{id}`           |     1 s | Yes                             | Read-only                   |
| `POST /api/orders`               |     2 s | Only with idempotency key       | Creates state               |
| `POST /api/payments/authorize`   |     3 s | Carefully, with idempotency key | External side effect        |
| `POST /api/refunds`              |     5 s | Carefully, with idempotency key | Financial side effect       |

The gateway should not apply the same retry policy to every route.

Unsafe retries can create duplicate orders, duplicate payments, or duplicate messages.

Example policy:

```yaml
routes:
  - name: catalog-read
    match:
      pathPrefix: /api/catalog
      methods: [GET]
    timeoutMs: 500
    retry:
      attempts: 2

  - name: create-order
    match:
      path: /api/orders
      methods: [POST]
    timeoutMs: 2000
    retry:
      attempts: 0
    requireHeaders:
      - Idempotency-Key
```

Retries are safer for idempotent reads than for state-changing writes.

---

#### Route ownership

As systems grow, every route should have an owner.

A route owner is responsible for:

* backend service health,
* API contract,
* route configuration,
* deprecation,
* monitoring,
* incident response,
* documentation.

Example route ownership table:

| Route                | Backend         | Owner               |
| -------------------- | --------------- | ------------------- |
| `/api/orders/*`      | Order Service   | Orders Team         |
| `/api/payments/*`    | Payment Service | Payments Team       |
| `/api/catalog/*`     | Catalog Service | Catalog Team        |
| `/api/admin/users/*` | Admin Service   | Internal Tools Team |

Without ownership, route configuration becomes a shared dumping ground.

This is one reason gateway routing rules become difficult to manage over time.

---

#### When to use it

Use Gateway Routing when:

* clients need one stable API surface,
* backend services are independently deployed,
* clients should not know internal service locations,
* routes need to be split by path, version, tenant, or region,
* you are migrating from a monolith to services,
* you need canary or blue-green traffic shifting,
* you need public and internal APIs on different hosts,
* you want routing rules to be managed centrally,
* you need to hide backend topology from external clients.

It is especially useful when multiple clients consume many backend services.

---

#### When not to use it

Gateway Routing may be unnecessary when:

* there is only one backend service,
* clients are internal and already use service discovery safely,
* the gateway would only forward traffic without adding value,
* route rules would be more complex than the service topology,
* ultra-low latency is more important than centralized routing,
* backend services are not ready to be independently exposed through contracts.

Also avoid using routing to compensate for unclear service boundaries. If every request needs complex conditional routing, the backend architecture may need review.

---

#### Benefits

**1. Unified client access**

Clients call one API surface instead of many backend services.

**2. Hidden backend topology**

Services can move, split, merge, or change infrastructure without forcing client changes.

**3. Independent deployment**

Backend services remain independently deployable while the gateway provides stable routing.

**4. Controlled migration**

Traffic can be shifted from legacy systems to new services route by route.

**5. Safer releases**

Canary and blue-green routing allow controlled rollout and rollback.

**6. Multi-tenant flexibility**

Tenants can be routed to shared, dedicated, regional, or regulated environments.

**7. API version coexistence**

Old and new API versions can run side by side while clients migrate.

---

#### Trade-offs

**1. Routing rules can become complex**

Path, header, tenant, version, region, and rollout rules can interact in surprising ways.

**2. Configuration becomes critical infrastructure**

A bad route change can cause outages or data exposure.

**3. Debugging can be harder**

When routing is dynamic, teams need strong logs and tracing to understand where a request went.

**4. Gateway can become a bottleneck**

All traffic passes through the gateway, so it must be reliable and scalable.

**5. Route ownership can become unclear**

If many teams modify gateway rules, ownership and review processes are essential.

**6. Security risk increases**

Incorrect routing can expose admin APIs, internal services, or cross-tenant data.

**7. Version sprawl can accumulate**

Gateway routing can make it easy to keep old versions alive forever.

---

#### Common mistakes

**Mistake 1: Using broad routes before specific routes**

A route like `/api/orders/*` may accidentally capture `/api/orders/search` unless rule priority is clear.

**Mistake 2: Trusting client-provided routing headers**

External clients should not be allowed to choose tenant, region, or internal role by sending arbitrary headers.

**Mistake 3: No route ownership**

Every route should have a responsible team.

**Mistake 4: No route tests**

Routing rules should be tested before deployment.

**Mistake 5: Manual route changes without review**

Gateway configuration should usually be versioned and reviewed.

**Mistake 6: Routing all versions forever**

Old routes need deprecation plans.

**Mistake 7: Applying the same timeout and retry policy everywhere**

Read routes and write routes need different behavior.

**Mistake 8: Hiding business logic in routing rules**

Routing should select a backend. It should not become the place where business decisions are made.

---

#### Practical design checklist

When designing gateway routing, answer:

* What public routes does the gateway expose?
* Which backend service owns each route?
* What is the matching rule for each route?
* Are specific routes evaluated before broad routes?
* Are routes based on path, host, header, tenant, region, or version?
* Which headers are trusted?
* Which headers must be stripped?
* How is tenant identity verified?
* How is region selected?
* Are route changes versioned?
* Are route changes reviewed?
* Are routing rules tested automatically?
* What timeout applies to each route?
* Are retries safe for each route?
* What happens if the target service is unavailable?
* Is fallback allowed?
* How are route decisions logged?
* Who owns each route?
* What routes are deprecated?
* How are old routes removed?

A gateway routing design is probably healthy if:

* route rules are clear,
* route ownership is documented,
* route configuration is version-controlled,
* route decisions are observable,
* security-sensitive routing uses trusted identity,
* tests cover important routes,
* old versions have deprecation plans,
* routing stays separate from business logic.

A gateway routing design is probably unhealthy if:

* nobody knows why a route exists,
* rules are edited manually without review,
* broad routes accidentally capture specific routes,
* clients can spoof routing headers,
* old API versions never go away,
* route behavior cannot be reproduced in tests,
* gateway configuration is the only place business behavior is defined.

---

#### Related patterns

| Pattern                | Relationship                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------- |
| API Gateway            | Gateway Routing is one of the core gateway responsibilities                         |
| Gateway Aggregation    | Routing sends requests to services; aggregation combines multiple service responses |
| Gateway Offloading     | Routing is often combined with auth, TLS, rate limiting, and observability          |
| Backends for Frontends | Routing may send different clients to different BFFs                                |
| Strangler Fig Pattern  | Routing gradually shifts traffic from legacy systems to new services                |
| Blue-Green Deployment  | Routing switches traffic between two environments                                   |
| Canary Release         | Routing sends a small percentage of traffic to a new version                        |
| Service Discovery      | Gateway uses discovery to locate backend service instances                          |
| API Versioning         | Gateway can route old and new API versions                                          |
| Circuit Breaker        | Gateway can stop routing to unhealthy backends                                      |
| Rate Limiting          | Route-specific limits protect backend services                                      |
| Anti-Corruption Layer  | Gateway may route to an ACL when integrating with legacy systems                    |

---

#### Summary

Gateway Routing directs requests from a gateway to backend services based on path, host, headers, version, tenant, region, rollout rules, or other request attributes.

The central idea is:

> Clients use one stable API surface while the gateway decides which backend service should handle each request.

Gateway Routing is useful for:

* exposing many services through one API,
* hiding internal topology,
* supporting API versions,
* routing tenants and regions,
* enabling canary and blue-green releases,
* migrating from legacy systems,
* and keeping backend services independently deployable.

The main risk is that routing rules become complex, unsafe, or poorly owned. To use this pattern well, route configuration should be explicit, tested, observable, secure, and version-controlled.


---

### 9. Gateway Aggregation / Aggregator Pattern

#### What it is

**Gateway Aggregation**, also called the **Aggregator Pattern**, combines data from multiple backend services into a single response for a client.

Instead of forcing the client to call several services and assemble the result itself, an aggregator does that work on the server side.

Without aggregation, a client may need to make many calls:

```mermaid
sequenceDiagram
    participant Client
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Shipping as Shipping Service
    participant Catalog as Catalog Service
    participant Support as Support Service

    Client->>Orders: GET /orders/ord_123
    Client->>Payments: GET /payments?orderId=ord_123
    Client->>Shipping: GET /shipments?orderId=ord_123
    Client->>Catalog: GET /products/prod_456
    Client->>Support: GET /support/eligibility?orderId=ord_123
```

With aggregation, the client makes one request:

```mermaid
sequenceDiagram
    participant Client
    participant Aggregator as Gateway Aggregator
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Shipping as Shipping Service
    participant Catalog as Catalog Service
    participant Support as Support Service

    Client->>Aggregator: GET /order-summary/ord_123

    Aggregator->>Orders: Get order
    Aggregator->>Payments: Get payment status
    Aggregator->>Shipping: Get shipment status
    Aggregator->>Catalog: Get product details
    Aggregator->>Support: Get support eligibility

    Orders-->>Aggregator: Order
    Payments-->>Aggregator: Payment status
    Shipping-->>Aggregator: Shipment status
    Catalog-->>Aggregator: Product details
    Support-->>Aggregator: Support eligibility

    Aggregator-->>Client: Combined order summary
```

The central idea is:

> The client asks for the view it needs; the aggregator collects and shapes the backend data required for that view.

This pattern is especially useful for read-heavy screens that need data from several services.

---

#### Why this pattern exists

Microservices often split data by ownership. That is good for service autonomy, but it creates a challenge for clients.

For example, an order detail screen may need data from several services:

| Data needed by screen       | Owning service   |
| --------------------------- | ---------------- |
| Order status and line items | Order Service    |
| Payment status              | Payment Service  |
| Shipment tracking           | Shipping Service |
| Product names and images    | Catalog Service  |
| Return eligibility          | Returns Service  |
| Support options             | Support Service  |

A frontend could call each service directly, but that creates problems:

* many network round trips,
* slower mobile performance,
* duplicated composition logic across clients,
* clients become coupled to internal service boundaries,
* backend service changes can break clients,
* error handling becomes inconsistent,
* authentication and authorization become harder to coordinate,
* clients may need to understand too much domain topology.

Gateway Aggregation moves that composition logic to a backend layer.

```mermaid
flowchart TD
    Client[Client]

    Aggregator[Aggregator]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Catalog[Catalog Service]
    Returns[Returns Service]

    Client --> Aggregator

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping
    Aggregator --> Catalog
    Aggregator --> Returns
```

The client gets a purpose-built response, while backend services continue to own their own data.

---

#### What it solves

Gateway Aggregation solves **client-side composition complexity**.

Without an aggregator, each client may implement the same composition logic:

```mermaid
flowchart TD
    Web[Web App]
    IOS[iOS App]
    Android[Android App]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Catalog[Catalog Service]

    Web --> Orders
    Web --> Payments
    Web --> Shipping
    Web --> Catalog

    IOS --> Orders
    IOS --> Payments
    IOS --> Shipping
    IOS --> Catalog

    Android --> Orders
    Android --> Payments
    Android --> Shipping
    Android --> Catalog
```

This duplicates logic across clients.

For example, each client might need to know:

* which services to call,
* in what order to call them,
* which failures are acceptable,
* how to merge the responses,
* how to handle missing data,
* how to transform service-specific fields into screen-specific fields.

With aggregation, that logic moves to one backend composition point:

```mermaid
flowchart TD
    Web[Web App]
    IOS[iOS App]
    Android[Android App]

    Aggregator[Order Summary Aggregator]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Catalog[Catalog Service]

    Web --> Aggregator
    IOS --> Aggregator
    Android --> Aggregator

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping
    Aggregator --> Catalog
```

The clients can remain simpler.

---

#### Basic aggregation flow

A typical aggregation flow has four steps:

```mermaid
flowchart TD
    Step1[1. Receive client request]
    Step2[2. Call backend services]
    Step3[3. Combine and transform data]
    Step4[4. Return client-shaped response]

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
```

For example:

```http
GET /api/order-summary/ord_123
```

The aggregator may call:

```http
GET /orders/ord_123
GET /payments/by-order/ord_123
GET /shipments/by-order/ord_123
GET /products/prod_456
```

Then it returns:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD",
  "payment": {
    "status": "AUTHORIZED"
  },
  "shipment": {
    "status": "PENDING",
    "estimatedDeliveryDate": "2026-05-02"
  },
  "items": [
    {
      "productId": "prod_456",
      "name": "Trail Running Shoe",
      "imageUrl": "https://cdn.example.com/products/prod_456.jpg",
      "quantity": 1,
      "unitPrice": 129.99
    }
  ]
}
```

The response is designed around what the client needs, not around how backend services are split.

---

#### Aggregation location

Aggregation can live in different places.

##### Option 1: API Gateway aggregation

The API Gateway itself performs the aggregation.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway with Aggregation]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Client --> Gateway

    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Shipping
```

This can be useful for simple read-only aggregation.

However, be careful. If the gateway accumulates many complex aggregations, it can become a hidden monolith.

Use gateway-level aggregation when:

* the aggregation is simple,
* the result is read-only,
* the logic is mostly composition,
* the response shape is broadly useful,
* the gateway team can own the operational risk.

Avoid putting deep business workflows or domain rules in the gateway.

---

##### Option 2: Dedicated aggregator service

A separate service owns the aggregation endpoint.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Aggregator[Order Summary Aggregator]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Catalog[Catalog Service]

    Client --> Gateway
    Gateway --> Aggregator

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping
    Aggregator --> Catalog
```

This is often cleaner when the aggregation is complex or owned by a specific product team.

Benefits:

* clearer ownership,
* easier testing,
* gateway stays simple,
* aggregation can evolve independently,
* domain-specific composition is not mixed with edge infrastructure.

This is often a better choice than putting everything directly inside the API Gateway.

---

##### Option 3: Backend for Frontend

A **Backend for Frontend**, or **BFF**, aggregates data for one specific client experience.

```mermaid
flowchart TD
    Web[Web App]
    Mobile[Mobile App]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]

    Orders[Order Service]
    Payments[Payment Service]
    Catalog[Catalog Service]
    Shipping[Shipping Service]

    Web --> WebBFF
    Mobile --> MobileBFF

    WebBFF --> Orders
    WebBFF --> Payments
    WebBFF --> Catalog

    MobileBFF --> Orders
    MobileBFF --> Payments
    MobileBFF --> Shipping
```

Use a BFF when different clients need different response shapes.

For example:

| Client        | Needs                                                 |
| ------------- | ----------------------------------------------------- |
| Web app       | Rich product details, recommendations, reviews        |
| Mobile app    | Compact payload, fewer fields, image thumbnails       |
| Admin console | Internal metadata, audit status, operational controls |
| Partner API   | Stable contract, fewer internal details               |

Gateway Aggregation and BFF often overlap. The difference is intent:

| Pattern             | Main purpose                                                   |
| ------------------- | -------------------------------------------------------------- |
| Gateway Aggregation | Combine backend service data behind one gateway endpoint       |
| BFF                 | Provide client-specific APIs tailored to a particular frontend |

---

#### Example: product detail page

A product detail page may need data from many services:

```mermaid
flowchart TD
    ProductPage[Product Detail Page]

    Aggregator[Product Detail Aggregator]

    Catalog[Catalog Service]
    Pricing[Pricing Service]
    Inventory[Inventory Service]
    Reviews[Review Service]
    Recommendations[Recommendation Service]
    Shipping[Shipping Service]

    ProductPage --> Aggregator

    Aggregator --> Catalog
    Aggregator --> Pricing
    Aggregator --> Inventory
    Aggregator --> Reviews
    Aggregator --> Recommendations
    Aggregator --> Shipping
```

The backend ownership might look like this:

| Data                          | Source                 |
| ----------------------------- | ---------------------- |
| Product title and description | Catalog Service        |
| Current price                 | Pricing Service        |
| Stock availability            | Inventory Service      |
| Customer reviews              | Review Service         |
| Related products              | Recommendation Service |
| Delivery estimate             | Shipping Service       |

The aggregator returns a view model:

```json
{
  "productId": "prod_123",
  "title": "Trail Running Shoe",
  "description": "Lightweight running shoe for mixed terrain.",
  "price": {
    "amount": 129.99,
    "currency": "USD",
    "discounted": false
  },
  "availability": {
    "status": "IN_STOCK",
    "remainingQuantity": 12
  },
  "rating": {
    "average": 4.6,
    "count": 381
  },
  "delivery": {
    "estimatedDate": "2026-05-03"
  },
  "recommendations": [
    {
      "productId": "prod_999",
      "title": "Running Socks"
    }
  ]
}
```

The client gets one response optimized for the screen.

---

#### Example implementation

Here is a simplified TypeScript example using Express.

```ts
import express, { Request, Response } from "express";

const app = express();

type Order = {
  id: string;
  customerId: string;
  status: string;
  totalAmount: number;
  currency: string;
  items: Array<{
    productId: string;
    quantity: number;
    unitPrice: number;
  }>;
};

type Payment = {
  orderId: string;
  status: string;
};

type Shipment = {
  orderId: string;
  status: string;
  estimatedDeliveryDate?: string;
};

type Product = {
  productId: string;
  title: string;
  imageUrl: string;
};

async function getOrder(orderId: string): Promise<Order> {
  const response = await fetch(`http://orders-service/orders/${orderId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch order");
  }
  return response.json() as Promise<Order>;
}

async function getPayment(orderId: string): Promise<Payment> {
  const response = await fetch(`http://payments-service/payments/by-order/${orderId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch payment");
  }
  return response.json() as Promise<Payment>;
}

async function getShipment(orderId: string): Promise<Shipment> {
  const response = await fetch(`http://shipping-service/shipments/by-order/${orderId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch shipment");
  }
  return response.json() as Promise<Shipment>;
}

async function getProduct(productId: string): Promise<Product> {
  const response = await fetch(`http://catalog-service/products/${productId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch product");
  }
  return response.json() as Promise<Product>;
}

app.get("/api/order-summary/:orderId", async (req: Request, res: Response) => {
  try {
    const order = await getOrder(req.params.orderId);

    const [payment, shipment, products] = await Promise.all([
      getPayment(order.id),
      getShipment(order.id),
      Promise.all(order.items.map((item) => getProduct(item.productId)))
    ]);

    const productsById = new Map(
      products.map((product) => [product.productId, product])
    );

    res.json({
      orderId: order.id,
      status: order.status,
      totalAmount: order.totalAmount,
      currency: order.currency,
      payment: {
        status: payment.status
      },
      shipment: {
        status: shipment.status,
        estimatedDeliveryDate: shipment.estimatedDeliveryDate
      },
      items: order.items.map((item) => {
        const product = productsById.get(item.productId);

        return {
          productId: item.productId,
          name: product?.title ?? "Unknown product",
          imageUrl: product?.imageUrl,
          quantity: item.quantity,
          unitPrice: item.unitPrice
        };
      })
    });
  } catch (error) {
    res.status(500).json({
      error: "ORDER_SUMMARY_FAILED",
      message: "Could not build order summary"
    });
  }
});

app.listen(3000, () => {
  console.log("Aggregator listening on port 3000");
});
```

This example shows the basic flow:

1. Fetch the primary resource.
2. Use data from the primary resource to call supporting services.
3. Combine the results.
4. Return a client-friendly response.

In production, this would also need timeouts, retries, partial failure handling, tracing, caching, and authorization.

---

#### Sequential vs parallel aggregation

Some aggregation calls can run in parallel. Others must run sequentially.

Sequential aggregation:

```mermaid
sequenceDiagram
    participant Aggregator
    participant Orders as Order Service
    participant Catalog as Catalog Service

    Aggregator->>Orders: Get order
    Orders-->>Aggregator: Order with product IDs
    Aggregator->>Catalog: Get products by IDs
    Catalog-->>Aggregator: Product details
```

Parallel aggregation:

```mermaid
sequenceDiagram
    participant Aggregator
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Shipping as Shipping Service

    Aggregator->>Orders: Get order
    Aggregator->>Payments: Get payment
    Aggregator->>Shipping: Get shipment

    Orders-->>Aggregator: Order
    Payments-->>Aggregator: Payment
    Shipping-->>Aggregator: Shipment
```

In practice, many aggregations are mixed.

Example:

```mermaid
flowchart TD
    Start[Request order summary]

    Order[Fetch order]

    Parallel[Fetch related data in parallel]

    Payment[Fetch payment]
    Shipment[Fetch shipment]
    Products[Fetch product details]

    Combine[Combine response]

    Start --> Order
    Order --> Parallel

    Parallel --> Payment
    Parallel --> Shipment
    Parallel --> Products

    Payment --> Combine
    Shipment --> Combine
    Products --> Combine
```

The aggregator should call independent services in parallel when possible to reduce latency.

---

#### Timeout handling

Aggregators depend on multiple services. If one backend is slow, the whole response can become slow.

```mermaid
flowchart TD
    Client[Client]
    Aggregator[Aggregator]

    Fast1[Order Service<br/>40 ms]
    Fast2[Payment Service<br/>50 ms]
    Slow[Shipping Service<br/>3000 ms]

    Client --> Aggregator

    Aggregator --> Fast1
    Aggregator --> Fast2
    Aggregator --> Slow
```

The aggregator should set timeouts for each backend call.

Example helper:

```ts
async function fetchWithTimeout<T>(
  url: string,
  timeoutMs: number
): Promise<T> {
  const controller = new AbortController();

  const timeout = setTimeout(() => {
    controller.abort();
  }, timeoutMs);

  try {
    const response = await fetch(url, {
      signal: controller.signal
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    return response.json() as Promise<T>;
  } finally {
    clearTimeout(timeout);
  }
}
```

Example use:

```ts
const shipment = await fetchWithTimeout<Shipment>(
  `http://shipping-service/shipments/by-order/${orderId}`,
  500
);
```

Timeouts should be chosen by route and dependency. A product image or recommendation call may tolerate a short timeout. A payment status lookup may need a different policy.

---

#### Partial failure handling

Not all backend failures should cause the entire aggregated response to fail.

For example, if the Recommendation Service is unavailable, the product page can still load without recommendations.

```mermaid
flowchart TD
    Aggregator[Product Page Aggregator]

    Catalog[Catalog Service]
    Pricing[Pricing Service]
    Inventory[Inventory Service]
    Reviews[Review Service]
    Recommendations[Recommendation Service<br/>Unavailable]

    Response[Partial response]

    Aggregator --> Catalog
    Aggregator --> Pricing
    Aggregator --> Inventory
    Aggregator --> Reviews
    Aggregator -. failed .-> Recommendations

    Catalog --> Response
    Pricing --> Response
    Inventory --> Response
    Reviews --> Response
```

But if the Catalog Service fails, the product page may not be meaningful at all.

A useful distinction:

| Data type                   | Example                     | Failure behavior        |
| --------------------------- | --------------------------- | ----------------------- |
| Required data               | Order, product, account     | Fail the request        |
| Important but optional data | Shipment estimate, reviews  | Return partial response |
| Nice-to-have data           | Recommendations, promotions | Omit or fallback        |
| Sensitive data              | Payment status, permissions | Fail closed             |

Example partial failure response:

```json
{
  "productId": "prod_123",
  "title": "Trail Running Shoe",
  "price": {
    "amount": 129.99,
    "currency": "USD"
  },
  "availability": {
    "status": "IN_STOCK"
  },
  "recommendations": [],
  "warnings": [
    {
      "code": "RECOMMENDATIONS_UNAVAILABLE",
      "message": "Recommendations are temporarily unavailable."
    }
  ]
}
```

Example implementation using `Promise.allSettled`:

```ts
const [reviewsResult, recommendationsResult] = await Promise.allSettled([
  reviewsClient.getReviews(productId),
  recommendationsClient.getRecommendations(productId)
]);

const reviews =
  reviewsResult.status === "fulfilled" ? reviewsResult.value : [];

const recommendations =
  recommendationsResult.status === "fulfilled"
    ? recommendationsResult.value
    : [];
```

Partial responses should be designed intentionally. The client should understand whether data is missing because it does not exist or because a dependency failed.

---

#### Fallbacks

A fallback is an alternative response when a backend dependency fails.

Common fallbacks include:

* cached data,
* stale data,
* default values,
* empty lists,
* degraded UI sections,
* backup service,
* precomputed read model.

```mermaid
flowchart TD
    Aggregator[Aggregator]
    Dependency[Backend Dependency]
    Cache[(Cache)]
    Response[Response]

    Aggregator --> Dependency
    Dependency -->|success| Response
    Dependency -. failure .-> Cache
    Cache -->|fallback data| Response
```

Example:

```ts
async function getProductRecommendations(productId: string): Promise<Recommendation[]> {
  try {
    return await recommendationsClient.getRecommendations(productId);
  } catch {
    const cached = await cache.get(`recommendations:${productId}`);

    if (cached) {
      return JSON.parse(cached) as Recommendation[];
    }

    return [];
  }
}
```

Fallbacks are most appropriate for non-critical read data.

Be careful with fallback behavior for sensitive or state-changing operations. For example, falling back incorrectly on payment status or authorization checks can create security and financial risk.

---

#### Caching

Aggregators often benefit from caching because they repeatedly assemble similar views.

Caching options include:

| Cache level          | Example                                    |
| -------------------- | ------------------------------------------ |
| CDN cache            | Public product page data                   |
| Gateway cache        | Frequently requested API responses         |
| Aggregator cache     | Product detail view model                  |
| Service-level cache  | Catalog or pricing data                    |
| Per-dependency cache | Cached calls to reviews or recommendations |

```mermaid
flowchart TD
    Client[Client]
    CDN[CDN or Edge Cache]
    Aggregator[Aggregator]
    Cache[(Aggregator Cache)]

    Services[Backend Services]

    Client --> CDN
    CDN --> Aggregator

    Aggregator --> Cache
    Aggregator --> Services
```

Example cache lookup:

```ts
app.get("/api/product-detail/:productId", async (req, res) => {
  const cacheKey = `product-detail:${req.params.productId}`;

  const cached = await cache.get(cacheKey);
  if (cached) {
    res.json(JSON.parse(cached));
    return;
  }

  const response = await buildProductDetail(req.params.productId);

  await cache.set(cacheKey, JSON.stringify(response), {
    ttlSeconds: 60
  });

  res.json(response);
});
```

Caching requires careful thinking:

* How fresh must the data be?
* Can stale data be shown?
* What is the TTL?
* How is cache invalidated?
* Is the response user-specific?
* Does it contain sensitive information?
* Does the cache key include tenant, region, user, language, and currency?
* Can different users accidentally receive each other’s data?

For example, this cache key may be unsafe:

```text
product-detail:prod_123
```

If the price depends on tenant, region, currency, or customer segment, the key should include those dimensions:

```text
product-detail:prod_123:tenant_abc:US:USD:premium
```

---

#### Avoiding the N+1 problem

Aggregators can accidentally create too many backend calls.

For example, this is risky:

```ts
const order = await ordersClient.getOrder(orderId);

const products = [];

for (const item of order.items) {
  const product = await catalogClient.getProduct(item.productId);
  products.push(product);
}
```

If an order has 50 items, this makes 50 calls to Catalog Service.

Better:

```ts
const productIds = order.items.map((item) => item.productId);

const products = await catalogClient.getProductsBatch(productIds);
```

Backend services should provide batch endpoints when aggregators need many related resources.

Example batch API:

```http
POST /products/batch
Content-Type: application/json

{
  "productIds": ["prod_1", "prod_2", "prod_3"]
}
```

Diagram:

```mermaid
flowchart TD
    Aggregator[Aggregator]
    Loop[N individual product calls]
    Batch[One batch product call]
    Catalog[Catalog Service]

    Aggregator --> Loop
    Aggregator --> Batch

    Loop --> Catalog
    Batch --> Catalog
```

Batching reduces latency, network overhead, and backend load.

---

#### Response shaping

An aggregator often returns a response shaped for a specific use case.

Backend service response:

```json
{
  "id": "prod_123",
  "title": "Trail Running Shoe",
  "description": "Lightweight running shoe.",
  "categoryId": "cat_88",
  "createdAt": "2026-01-01T12:00:00Z",
  "updatedAt": "2026-04-20T09:00:00Z",
  "internalStatus": "ACTIVE",
  "merchandisingFlags": ["featured"],
  "taxCategory": "FOOTWEAR"
}
```

Client-specific aggregated response:

```json
{
  "productId": "prod_123",
  "title": "Trail Running Shoe",
  "description": "Lightweight running shoe.",
  "isFeatured": true
}
```

The aggregator should expose what the client needs, not necessarily everything the backend service knows.

This improves:

* payload size,
* client simplicity,
* API stability,
* separation between internal and external models.

But response shaping should not become domain ownership. The Catalog Service should still own what a product means. The aggregator should shape the view.

---

#### Authorization in aggregation

Aggregators often call multiple services on behalf of a user.

They must preserve security context.

```mermaid
flowchart TD
    Client[Client]
    Aggregator[Aggregator]

    Orders[Order Service]
    Billing[Billing Service]
    Support[Support Service]

    Client -->|Authenticated request| Aggregator

    Aggregator -->|User context| Orders
    Aggregator -->|User context| Billing
    Aggregator -->|User context| Support
```

Important questions:

* Who is the user?
* What tenant do they belong to?
* What scopes or roles do they have?
* Should downstream services enforce their own authorization?
* Can the aggregator request data the user should not see?
* Are internal service credentials overprivileged?

A dangerous aggregator uses a powerful service token to fetch everything and then tries to filter later.

A safer design passes user or tenant context downstream so each domain service can enforce its own rules.

Example headers:

```http
X-Request-Id: req_123
X-User-Id: user_456
X-Tenant-Id: tenant_789
X-Scopes: orders:read payments:read
```

These headers should only be created by trusted infrastructure after authentication. External clients should not be allowed to spoof them.

---

#### Aggregation and consistency

Aggregated responses may combine data that changes independently.

For example:

* Order Service says the order is `CONFIRMED`.
* Payment Service says payment is `PENDING`.
* Shipping Service says no shipment exists yet.

That may be valid during an eventually consistent workflow.

```mermaid
flowchart TD
    Aggregator[Order Summary Aggregator]

    Orders[Order Service<br/>Order CONFIRMED]
    Payments[Payment Service<br/>Payment PENDING]
    Shipping[Shipping Service<br/>No shipment yet]

    Response[Combined Response]

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping

    Orders --> Response
    Payments --> Response
    Shipping --> Response
```

The aggregator should not hide all inconsistency. Sometimes the correct response is to show an in-progress state.

Example:

```json
{
  "orderId": "ord_123",
  "orderStatus": "CONFIRMED",
  "paymentStatus": "PENDING",
  "shipmentStatus": "NOT_CREATED",
  "overallStatus": "PROCESSING"
}
```

A common mistake is making the aggregator invent a business state it does not own.

For example, if “overall order status” is a real domain concept, the Order Service or workflow service should own it. The aggregator may display it, but should not be the source of truth for it.

---

#### Aggregation vs read model

Gateway Aggregation builds a response by calling services at request time.

A **read model** precomputes and stores a query-optimized view.

Request-time aggregation:

```mermaid
flowchart TD
    Client[Client]
    Aggregator[Aggregator]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Client --> Aggregator

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping
```

Precomputed read model:

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Bus[(Event Bus)]
    Projector[Read Model Projector]
    ReadDB[(Order Summary Read DB)]

    Client[Client]
    QueryAPI[Query API]

    Orders --> Bus
    Payments --> Bus
    Shipping --> Bus

    Bus --> Projector
    Projector --> ReadDB

    Client --> QueryAPI
    QueryAPI --> ReadDB
```

Comparison:

| Approach            | Best for                                                                  |
| ------------------- | ------------------------------------------------------------------------- |
| Gateway Aggregation | Low to moderate traffic, fresh data, simple composition                   |
| Read model          | High traffic, complex joins, dashboards, analytics, expensive composition |
| Hybrid              | Aggregator uses read model plus a few live calls                          |

If an aggregator becomes slow because it calls too many services, a read model may be a better design.

---

#### Aggregation vs orchestration

Aggregation is for reads. Orchestration is for workflows.

| Pattern       | Purpose                               |
| ------------- | ------------------------------------- |
| Aggregation   | Combine data for a response           |
| Orchestration | Coordinate commands and state changes |

Good aggregation:

```http
GET /api/order-summary/ord_123
```

Risky aggregation misuse:

```http
POST /api/checkout
```

A checkout endpoint that creates an order, authorizes payment, reserves inventory, and confirms the order is not just aggregation. It is workflow orchestration.

That belongs in a Checkout Service, Saga orchestrator, or workflow service.

```mermaid
flowchart TD
    ReadAggregation[Read Aggregation]
    WorkflowOrchestration[Workflow Orchestration]

    ReadAggregation --> Safe[Combines service data]
    ReadAggregation --> Example1[GET order summary]

    WorkflowOrchestration --> Commands[Changes system state]
    WorkflowOrchestration --> Example2[POST checkout]
```

Keeping this distinction clear prevents the gateway or aggregator from becoming a business-process monolith.

---

#### Error handling

Aggregators should return clear errors.

If the primary resource is missing:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "ORDER_NOT_FOUND",
  "message": "The requested order does not exist."
}
```

If a required dependency fails:

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json

{
  "error": "ORDER_SUMMARY_UNAVAILABLE",
  "message": "Order summary is temporarily unavailable."
}
```

If optional data fails:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "shipment": null,
  "warnings": [
    {
      "code": "SHIPMENT_STATUS_UNAVAILABLE",
      "message": "Shipment status is temporarily unavailable."
    }
  ]
}
```

Avoid leaking raw downstream errors to clients.

Bad:

```json
{
  "error": "java.net.SocketTimeoutException: Read timed out at shipping-service"
}
```

Better:

```json
{
  "error": "SHIPMENT_STATUS_UNAVAILABLE",
  "message": "Shipment status is temporarily unavailable."
}
```

Downstream details should be logged internally with request IDs and trace IDs.

---

#### Observability

Aggregation can hide many backend calls behind one client request. Strong observability is essential.

Track:

* aggregator endpoint latency,
* per-dependency latency,
* per-dependency error rate,
* timeout count,
* fallback count,
* partial response count,
* cache hit rate,
* cache staleness,
* downstream status codes,
* response size,
* fan-out count,
* request trace ID.

Example structured log:

```json
{
  "requestId": "req_123",
  "route": "/api/order-summary/ord_456",
  "statusCode": 200,
  "latencyMs": 142,
  "dependencies": {
    "orders": {
      "status": 200,
      "latencyMs": 38
    },
    "payments": {
      "status": 200,
      "latencyMs": 41
    },
    "shipping": {
      "status": "timeout",
      "latencyMs": 500,
      "fallbackUsed": true
    }
  },
  "partialResponse": true
}
```

Distributed tracing is especially useful:

```mermaid
flowchart TD
    Client[Client]
    Aggregator[Aggregator]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Catalog[Catalog Service]

    Trace[One Distributed Trace]

    Client --> Aggregator

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping
    Aggregator --> Catalog

    Trace -. includes .-> Aggregator
    Trace -. includes .-> Orders
    Trace -. includes .-> Payments
    Trace -. includes .-> Shipping
    Trace -. includes .-> Catalog
```

Without tracing, a slow aggregated response can be hard to diagnose.

---

#### Performance considerations

Aggregation can improve perceived client performance, but it can also overload backend services if poorly designed.

Key concerns:

**Fan-out**

One client request may create many backend requests.

```mermaid
flowchart TD
    OneRequest[1 client request]
    Aggregator[Aggregator]

    Call1[Backend call 1]
    Call2[Backend call 2]
    Call3[Backend call 3]
    Call4[Backend call 4]
    Call5[Backend call 5]
    Call6[Backend call 6]

    OneRequest --> Aggregator

    Aggregator --> Call1
    Aggregator --> Call2
    Aggregator --> Call3
    Aggregator --> Call4
    Aggregator --> Call5
    Aggregator --> Call6
```

If the endpoint receives 1,000 requests per second and each request fans out to 6 services, the backend sees up to 6,000 requests per second.

**Tail latency**

The aggregate response is often limited by the slowest required dependency.

```text
Total latency ≈ slowest required backend call + aggregation overhead
```

**Payload size**

Aggregators can accidentally return too much data. Shape responses carefully.

**Concurrency limits**

Aggregators should limit concurrency to avoid overwhelming dependencies.

Example concurrency limit concept:

```ts
import pLimit from "p-limit";

const limit = pLimit(10);

const products = await Promise.all(
  productIds.map((productId) =>
    limit(() => catalogClient.getProduct(productId))
  )
);
```

Batch APIs are often better than many limited concurrent calls.

---

#### When to use it

Use Gateway Aggregation when:

* a screen needs data from multiple services,
* clients are making too many round trips,
* mobile latency matters,
* several clients duplicate composition logic,
* backend topology should be hidden from clients,
* the endpoint is read-heavy,
* data can be combined safely,
* partial failure behavior can be defined,
* the aggregation is not a complex business transaction.

Common use cases include:

* account summaries,
* order detail pages,
* product detail pages,
* checkout review pages,
* customer dashboards,
* admin dashboards,
* mobile home screens,
* notification centers,
* billing summaries,
* support case views,
* search result enrichment.

---

#### When not to use it

Avoid or reconsider Gateway Aggregation when:

* the operation changes state across multiple services,
* the aggregator would own business workflow logic,
* the response requires complex business decisions,
* the fan-out is too large,
* latency requirements are very strict,
* backend dependencies are unreliable,
* a precomputed read model would be more efficient,
* the aggregation is specific to one frontend and belongs in a BFF,
* the gateway would become a dumping ground for presentation logic.

For expensive, high-traffic, multi-service reads, consider CQRS or a materialized read model instead.

---

#### Benefits

**1. Reduces client round trips**

The client makes one request instead of many.

**2. Simplifies clients**

Clients do not need to know which services own which data.

**3. Hides backend topology**

Backend services can change without exposing every change to clients.

**4. Improves perceived performance**

Parallel backend calls from the server side are often faster than multiple client-side calls, especially on mobile networks.

**5. Centralizes composition logic**

Transformation and response shaping happen in one place instead of being duplicated across clients.

**6. Supports client-friendly APIs**

The response can match a screen or use case rather than internal service boundaries.

**7. Enables partial degradation**

Optional sections can fail independently if the aggregator is designed for partial responses.

---

#### Trade-offs

**1. Coupling to many backend APIs**

The aggregator depends on every service it calls.

**2. More failure modes**

Any dependency can be slow, unavailable, inconsistent, or return unexpected data.

**3. Tail latency risk**

The total response time may be dominated by the slowest required dependency.

**4. Fan-out amplification**

One client request can create many backend requests.

**5. Caching becomes harder**

Aggregated responses may include data with different freshness requirements.

**6. Authorization becomes more complex**

The aggregator must preserve user and tenant context across downstream calls.

**7. Risk of becoming a hidden monolith**

If too much business logic is added, the aggregator becomes a centralized business layer.

---

#### Common mistakes

**Mistake 1: Putting workflows in the aggregator**

Aggregation should compose reads. It should not coordinate complex state-changing business processes.

**Mistake 2: Treating all dependencies as required**

Some data can be optional. Define partial failure behavior intentionally.

**Mistake 3: No timeouts**

One slow service can make the whole endpoint slow.

**Mistake 4: No fan-out control**

A single endpoint can overload many backend services.

**Mistake 5: Creating N+1 backend calls**

Use batch endpoints or read models when fetching many related resources.

**Mistake 6: Leaking downstream errors**

Clients should receive stable, client-appropriate errors.

**Mistake 7: Unsafe caching**

Aggregated responses may depend on tenant, user, region, language, currency, permissions, or feature flags.

**Mistake 8: Weak observability**

Without per-dependency metrics and traces, aggregation failures are hard to debug.

---

#### Practical design checklist

Before adding an aggregation endpoint, answer:

* What client or use case needs this aggregated response?
* Which backend services are required?
* Which backend services are optional?
* What is the primary resource?
* Can backend calls run in parallel?
* Are any calls sequentially dependent?
* What is the timeout for each dependency?
* What happens if each dependency fails?
* Which data can be omitted?
* Which failures should fail the entire request?
* Is fallback data available?
* Should the response be cached?
* What is the cache key?
* Does the cache key include tenant, user, region, language, currency, and permissions?
* Are downstream calls authorized with the correct user context?
* Is there a risk of N+1 calls?
* Do backend services need batch APIs?
* What is the expected fan-out?
* What is the expected traffic volume?
* Would a read model be better?
* Who owns this aggregation endpoint?
* How will latency and dependency failures be observed?

A good aggregation design is likely if:

* it is read-focused,
* it has clear ownership,
* it reduces real client complexity,
* it defines required and optional data,
* it has timeouts,
* it handles partial failures,
* it avoids excessive fan-out,
* it preserves authorization context,
* it has strong observability.

A weak aggregation design is likely if:

* it coordinates writes,
* it contains core business rules,
* it calls too many services per request,
* it has no timeout policy,
* it fails completely when optional data is unavailable,
* it has unsafe caching,
* it hides backend failures without logging,
* no team clearly owns it.

---

#### Related patterns

| Pattern                          | Relationship                                                                           |
| -------------------------------- | -------------------------------------------------------------------------------------- |
| API Gateway                      | Gateway Aggregation is often implemented at or behind the gateway                      |
| Gateway Routing                  | Routing sends requests to services; aggregation combines multiple service responses    |
| Gateway Offloading               | Aggregation is often combined with edge concerns, but should not absorb too much logic |
| Backends for Frontends           | BFFs often perform client-specific aggregation                                         |
| CQRS                             | A read model may replace expensive request-time aggregation                            |
| Event-Driven Architecture        | Events can feed materialized views used by aggregators                                 |
| Circuit Breaker                  | Protects aggregators from failing dependencies                                         |
| Retry                            | Useful for safe, idempotent backend calls                                              |
| Cache-Aside                      | Common caching approach for aggregated responses                                       |
| Consumer-Driven Contracts        | Helps ensure backend APIs satisfy aggregator needs                                     |
| Decompose by Business Capability | Aggregators compose data from capability services without owning their data            |

---

#### Summary

Gateway Aggregation combines data from multiple backend services into one client-friendly response.

The central idea is:

> Let backend services own their data, but give clients a response shaped around the screen or use case they need.

This pattern is useful for dashboards, mobile screens, product detail pages, account summaries, order summaries, and other read-heavy views.

A good aggregator:

* reduces client round trips,
* hides backend topology,
* composes read data,
* handles timeouts,
* supports partial failure,
* uses caching carefully,
* preserves authorization context,
* avoids excessive fan-out,
* and remains observable.

The main risk is that the aggregator becomes coupled to many backend APIs or turns into a hidden business-logic layer. Keep aggregation focused on read composition. Put core domain rules and state-changing workflows in the services that own those responsibilities.


---

### 10. Gateway Offloading

#### What it is

**Gateway Offloading** means moving common technical responsibilities out of individual backend services and into the API Gateway.

Instead of every service implementing the same edge concerns, the gateway handles them once at the system boundary.

Common responsibilities that can be offloaded include:

* TLS termination,
* authentication,
* API key validation,
* coarse authorization,
* rate limiting,
* CORS,
* request-size limits,
* request logging,
* tracing headers,
* request IDs,
* IP allowlists,
* bot protection,
* simple schema validation,
* compression,
* response caching,
* protocol translation.

Without gateway offloading, every service may need to repeat the same infrastructure code:

```mermaid
flowchart TD
    Client[Client]

    Orders[Order Service<br/>Auth<br/>TLS<br/>Rate Limit<br/>CORS<br/>Logging]
    Payments[Payment Service<br/>Auth<br/>TLS<br/>Rate Limit<br/>CORS<br/>Logging]
    Catalog[Catalog Service<br/>Auth<br/>TLS<br/>Rate Limit<br/>CORS<br/>Logging]

    Client --> Orders
    Client --> Payments
    Client --> Catalog
```

With gateway offloading, those shared concerns move to the gateway:

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway<br/>Auth<br/>TLS<br/>Rate Limit<br/>CORS<br/>Logging]

    Orders[Order Service]
    Payments[Payment Service]
    Catalog[Catalog Service]

    Client --> Gateway

    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Catalog
```

The central idea is:

> Put common edge responsibilities in one controlled place so backend services can focus on domain behavior.

The gateway handles the repeated technical work. Services handle business capabilities.

---

#### Why this pattern exists

In a microservice system, many services need the same edge behavior.

For example, every public service may need to:

* reject unauthenticated requests,
* verify API keys,
* enforce rate limits,
* block oversized payloads,
* attach request IDs,
* emit access logs,
* expose consistent error responses,
* handle CORS preflight requests,
* terminate HTTPS connections.

If every service implements these concerns independently, the system becomes inconsistent.

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Catalog[Catalog Service]

    Orders --> OrdersAuth[Custom auth logic]
    Payments --> PaymentsAuth[Different auth logic]
    Catalog --> CatalogAuth[Old auth logic]

    Orders --> OrdersRate[Rate limit v1]
    Payments --> PaymentsRate[No rate limit]
    Catalog --> CatalogRate[Rate limit v2]
```

This creates problems:

* duplicated code,
* inconsistent behavior,
* uneven security,
* harder audits,
* more bugs,
* more maintenance,
* slower service development,
* inconsistent logging and tracing.

Gateway Offloading centralizes these concerns.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    TLS[TLS Termination]
    Auth[Authentication]
    RateLimit[Rate Limiting]
    CORS[CORS]
    Logging[Access Logging]
    Limits[Request Size Limits]

    Services[Backend Services]

    Client --> Gateway

    Gateway --> TLS
    TLS --> Auth
    Auth --> RateLimit
    RateLimit --> CORS
    CORS --> Logging
    Logging --> Limits
    Limits --> Services
```

This makes edge behavior easier to standardize, test, monitor, and change.

---

#### What it solves

Gateway Offloading solves **duplicated infrastructure logic**.

Without offloading, backend services often contain repeated middleware:

```ts
app.use(tlsMiddleware);
app.use(authMiddleware);
app.use(apiKeyMiddleware);
app.use(rateLimitMiddleware);
app.use(corsMiddleware);
app.use(loggingMiddleware);
app.use(requestSizeLimitMiddleware);
```

If every service has its own version, small differences appear over time.

For example:

| Concern         | Order Service | Payment Service | Catalog Service |
| --------------- | ------------- | --------------- | --------------- |
| JWT validation  | New library   | Old library     | Custom code     |
| Rate limit      | 100/min       | None            | 500/min         |
| CORS            | Strict        | Too broad       | Missing         |
| Request logging | JSON          | Text logs       | Partial         |
| Max payload     | 1 MB          | 10 MB           | Unlimited       |

This is risky. The Payment Service may accidentally allow unlimited traffic. The Catalog Service may accept oversized requests. One service may validate tokens differently from another.

With offloading, the gateway applies consistent policy before requests reach backend services.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[Gateway Policy Layer]

    Auth{Authenticated?}
    Rate{Within Rate Limit?}
    Size{Request Size OK?}

    Backend[Backend Service]
    Reject[Reject Request]

    Request --> Gateway
    Gateway --> Auth

    Auth -->|No| Reject
    Auth -->|Yes| Rate

    Rate -->|No| Reject
    Rate -->|Yes| Size

    Size -->|No| Reject
    Size -->|Yes| Backend
```

The service receives only requests that passed the shared edge checks.

---

#### What belongs in the gateway

Gateway Offloading works best for **technical edge concerns**.

These are concerns that are common across many APIs and do not require deep domain knowledge.

Good candidates:

| Concern                  | Why it fits the gateway                |
| ------------------------ | -------------------------------------- |
| TLS termination          | Common edge security concern           |
| API key validation       | Public API access control              |
| JWT verification         | Common authentication step             |
| Coarse authorization     | Route-level policy can be centralized  |
| Rate limiting            | Protects services from abusive traffic |
| CORS                     | Browser edge concern                   |
| Request-size limits      | Protects infrastructure                |
| Access logs              | Gateway sees all incoming requests     |
| Request IDs              | Useful for tracing across services     |
| IP allowlists            | Edge security policy                   |
| Bot protection           | Edge concern                           |
| Simple schema validation | Rejects malformed requests early       |
| Compression              | Common transport optimization          |
| Response caching         | Useful for public read-heavy responses |

These responsibilities are usually independent of domain rules.

For example, the gateway can decide:

> Does this request have a valid access token?

But the Order Service should decide:

> Can this specific user cancel this specific order?

That distinction matters.

---

#### What should not be offloaded

The gateway should not own core business decisions.

Bad candidates for gateway offloading:

| Responsibility                          | Better owner                 |
| --------------------------------------- | ---------------------------- |
| Whether an order can be cancelled       | Order Service                |
| Whether inventory can be reserved       | Inventory Service            |
| Whether a payment can be refunded       | Payment Service              |
| Whether a claim should be approved      | Claims Service               |
| Whether a user qualifies for a discount | Pricing or Promotion Service |
| Whether a shipment can be rerouted      | Shipping Service             |
| Whether an account should be suspended  | Account Service              |
| How checkout should be orchestrated     | Checkout or Workflow Service |

A gateway should not become a business rules engine.

```mermaid
flowchart TD
    Gateway[API Gateway]

    Good[Good Offloading]
    Bad[Bad Offloading]

    Good --> Auth[Verify token]
    Good --> RateLimit[Apply rate limit]
    Good --> CORS[Handle CORS]
    Good --> Logging[Emit access logs]

    Bad --> Pricing[Calculate discounts]
    Bad --> Orders[Decide order cancellation]
    Bad --> Payments[Decide refund eligibility]
    Bad --> Inventory[Reserve inventory]
```

The gateway should protect and route traffic. Domain services should own business meaning.

---

#### TLS termination

TLS termination is one of the most common gateway offloading responsibilities.

The client connects to the gateway over HTTPS. The gateway handles certificates and decrypts the request.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway<br/>TLS Termination]
    Service[Backend Service]

    Client -->|HTTPS| Gateway
    Gateway -->|HTTP or mTLS| Service
```

Benefits:

* certificates are managed in one place,
* backend services do not each need public certificates,
* certificate rotation is simpler,
* public HTTPS policy is consistent,
* the gateway can enforce modern TLS settings.

However, internal traffic should still be protected. In many systems, gateway-to-service traffic uses:

* private networking,
* mutual TLS,
* service mesh encryption,
* encrypted load balancer connections.

A safer production design:

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Service[Backend Service]

    Client -->|HTTPS| Gateway
    Gateway -->|mTLS or private encrypted traffic| Service
```

Offloading TLS at the gateway does not mean internal traffic should be ignored.

---

#### Authentication offloading

The gateway can authenticate requests before forwarding them.

For example, the gateway can validate:

* JWT access tokens,
* OAuth2 tokens,
* API keys,
* signed requests,
* mTLS client certificates,
* session cookies.

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant IdP as Identity Provider
    participant Service as Backend Service

    Client->>Gateway: Request with token
    Gateway->>IdP: Validate token or fetch signing keys
    IdP-->>Gateway: Token valid
    Gateway->>Service: Forward request with trusted identity context
    Service-->>Gateway: Response
    Gateway-->>Client: Response
```

The gateway may add trusted headers after authentication:

```http
X-Request-Id: req_123
X-Authenticated-User-Id: user_456
X-Tenant-Id: tenant_789
X-Scopes: orders:read orders:write
```

Backend services can use this identity context, but they should only trust it if it comes from the gateway over a trusted internal path.

The gateway must remove any spoofed headers sent by the client.

```mermaid
flowchart TD
    Client[Client Request]
    Gateway[API Gateway]

    Strip[Strip untrusted identity headers]
    Verify[Verify token]
    Add[Add trusted identity headers]

    Service[Backend Service]

    Client --> Gateway
    Gateway --> Strip
    Strip --> Verify
    Verify --> Add
    Add --> Service
```

This prevents a client from sending fake internal headers such as:

```http
X-Authenticated-User-Id: admin
X-Tenant-Id: another_customer
```

---

#### API key validation

For partner APIs or external developer APIs, the gateway can validate API keys.

```mermaid
flowchart TD
    Partner[Partner Client]
    Gateway[API Gateway]
    KeyStore[(API Key Store)]
    Service[Backend Service]

    Partner -->|API key| Gateway
    Gateway --> KeyStore
    KeyStore --> Gateway
    Gateway --> Service
```

Example request:

```http
GET /api/v1/orders
X-API-Key: key_live_abc123
```

The gateway can check:

* whether the key exists,
* whether the key is active,
* which partner owns it,
* what plan or quota applies,
* which routes it can access,
* whether it is expired or revoked.

Example response for invalid key:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "INVALID_API_KEY",
  "message": "The provided API key is invalid or inactive."
}
```

This prevents every backend service from implementing its own API key validation logic.

---

#### Coarse authorization offloading

The gateway can enforce coarse-grained authorization.

Examples:

| Request                      | Gateway check                    |
| ---------------------------- | -------------------------------- |
| `GET /api/orders`            | Requires `orders:read` scope     |
| `POST /api/orders`           | Requires `orders:write` scope    |
| `GET /api/admin/users`       | Requires `admin:read` scope      |
| `POST /api/payments/refunds` | Requires `payments:refund` scope |

Gateway policy example:

```yaml
routes:
  - path: /api/orders
    methods: [GET]
    requiredScopes:
      - orders:read

  - path: /api/orders
    methods: [POST]
    requiredScopes:
      - orders:write

  - path: /api/admin/users
    methods: [GET]
    requiredScopes:
      - admin:read
```

But fine-grained business authorization should stay in the service.

For example:

| Authorization question                               | Owner           |
| ---------------------------------------------------- | --------------- |
| Does the token have `orders:read`?                   | Gateway         |
| Can user `user_123` view order `ord_456`?            | Order Service   |
| Does this refund exceed the customer’s policy limit? | Payment Service |
| Can this support agent access this tenant?           | Support Service |

The gateway can reject obviously unauthorized traffic early. Services still need to protect business-specific access.

---

#### Rate limiting offloading

Rate limiting is a strong fit for gateway offloading.

The gateway can limit requests by:

* IP address,
* user ID,
* tenant ID,
* API key,
* route,
* partner,
* region,
* plan tier.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]
    RateLimiter[Rate Limiter]
    Backend[Backend Service]
    Rejected[429 Too Many Requests]

    Request --> Gateway
    Gateway --> RateLimiter

    RateLimiter -->|Allowed| Backend
    RateLimiter -->|Limit exceeded| Rejected
```

Example policy:

```yaml
rateLimits:
  - name: free-plan
    match:
      plan: free
    limit:
      requestsPerMinute: 60

  - name: enterprise-plan
    match:
      plan: enterprise
    limit:
      requestsPerMinute: 10000
```

Example response:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1714412400
```

Rate limiting at the gateway helps protect all backend services consistently.

Backend services may still have their own internal limits for expensive operations, but the gateway handles the first line of defense.

---

#### CORS offloading

CORS, or Cross-Origin Resource Sharing, is a browser security mechanism.

If browser-based clients call your API, CORS headers are often required.

Instead of each service implementing CORS differently, the gateway can handle it consistently.

```mermaid
flowchart TD
    Browser[Browser Client]
    Gateway[API Gateway<br/>CORS Handling]
    Service[Backend Service]

    Browser -->|OPTIONS preflight| Gateway
    Gateway -->|CORS response| Browser

    Browser -->|Actual request| Gateway
    Gateway --> Service
```

Example CORS response:

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type, Idempotency-Key
Access-Control-Allow-Credentials: true
```

Gateway-managed CORS helps prevent mistakes such as:

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

That combination can be dangerous for authenticated browser APIs.

---

#### Request-size limits

The gateway can reject requests that are too large before they reach backend services.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    SizeCheck{Payload size OK?}

    Backend[Backend Service]
    Reject[413 Payload Too Large]

    Request --> Gateway
    Gateway --> SizeCheck

    SizeCheck -->|Yes| Backend
    SizeCheck -->|No| Reject
```

Example:

```http
HTTP/1.1 413 Payload Too Large
Content-Type: application/json

{
  "error": "PAYLOAD_TOO_LARGE",
  "message": "Request body exceeds the maximum allowed size."
}
```

Different routes may have different limits.

| Route                          | Max body size |
| ------------------------------ | ------------: |
| `POST /api/orders`             |        256 KB |
| `POST /api/profile/avatar`     |          5 MB |
| `POST /api/documents/upload`   |         25 MB |
| `POST /api/payments/authorize` |         64 KB |

Request-size limits protect services from accidental or malicious large payloads.

---

#### Request logging and request IDs

The gateway is a natural place to create a request ID.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    ServiceA[Order Service]
    ServiceB[Payment Service]

    Client --> Gateway
    Gateway -->|X-Request-Id| ServiceA
    ServiceA -->|X-Request-Id| ServiceB
```

Example headers:

```http
X-Request-Id: req_7f3a9c
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00
```

Example access log:

```json
{
  "requestId": "req_7f3a9c",
  "method": "GET",
  "path": "/api/orders/ord_123",
  "clientIp": "203.0.113.10",
  "userId": "user_456",
  "tenantId": "tenant_789",
  "targetService": "order-service",
  "statusCode": 200,
  "latencyMs": 42
}
```

This gives operators a consistent entry point for tracing requests.

The gateway should avoid logging sensitive data such as:

* passwords,
* access tokens,
* credit card numbers,
* session cookies,
* personal health information,
* full request bodies for sensitive endpoints.

---

#### Protocol translation

The gateway can offload protocol translation.

For example, external clients may use HTTP/JSON, while internal services use gRPC.

```mermaid
flowchart TD
    Client[External Client]
    Gateway[API Gateway]

    Json[HTTP JSON]
    Grpc[gRPC]

    Service[gRPC Backend Service]

    Client --> Json
    Json --> Gateway
    Gateway --> Grpc
    Grpc --> Service
```

Example external request:

```http
POST /api/payments/authorize
Content-Type: application/json

{
  "orderId": "ord_123",
  "amount": 129.99,
  "currency": "USD"
}
```

Internal gRPC request:

```proto
message AuthorizePaymentRequest {
  string order_id = 1;
  int64 amount_cents = 2;
  string currency = 3;
}
```

Protocol translation is useful when internal services use efficient protocols but public APIs need to remain simple and broadly compatible.

However, be careful. Protocol translation is an edge concern. Deep domain translation may belong in an Anti-Corruption Layer, not the gateway.

---

#### Response compression

The gateway can compress responses to reduce bandwidth.

Common compression formats include:

* gzip,
* Brotli,
* deflate.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway<br/>Compression]
    Service[Backend Service]

    Client --> Gateway
    Gateway --> Service
    Service --> Gateway
    Gateway -->|Compressed response| Client
```

This is especially useful for:

* large JSON responses,
* public APIs,
* mobile clients,
* slow networks,
* text-heavy responses.

The gateway can decide compression based on:

```http
Accept-Encoding: gzip, br
```

Backend services do not each need to implement response compression.

---

#### Response caching

The gateway can cache responses for safe, read-heavy endpoints.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Cache[(Gateway Cache)]
    Service[Backend Service]

    Client --> Gateway
    Gateway --> Cache

    Cache -->|Cache hit| Gateway
    Cache -->|Cache miss| Service
    Service --> Gateway
```

Good candidates:

* public catalog data,
* static reference data,
* feature flags for anonymous clients,
* help center content,
* configuration metadata.

Risky candidates:

* user-specific account data,
* payment data,
* private tenant data,
* authorization-dependent responses,
* rapidly changing inventory data.

Cache keys must include any dimension that affects the response.

For example, this may be unsafe:

```text
GET:/api/products/prod_123
```

If response depends on region, language, tenant, or currency, use a richer key:

```text
GET:/api/products/prod_123:tenant_abc:US:en-US:USD
```

Gateway caching is powerful, but incorrect caching can leak data or show stale information.

---

#### Request validation

The gateway can perform simple validation before forwarding requests.

Examples:

* required headers,
* valid content type,
* maximum body size,
* JSON schema shape,
* required query parameters,
* allowed HTTP methods.

```mermaid
flowchart TD
    Request[Incoming Request]
    Gateway[API Gateway]

    Validate{Valid request shape?}

    Backend[Backend Service]
    Reject[400 Bad Request]

    Request --> Gateway
    Gateway --> Validate

    Validate -->|Yes| Backend
    Validate -->|No| Reject
```

Example JSON schema:

```json
{
  "type": "object",
  "required": ["customerId", "items"],
  "properties": {
    "customerId": {
      "type": "string"
    },
    "items": {
      "type": "array",
      "minItems": 1
    }
  }
}
```

This can reduce unnecessary backend traffic.

But domain validation should stay in the service.

For example:

| Validation                           | Owner              |
| ------------------------------------ | ------------------ |
| Is `customerId` present?             | Gateway or service |
| Is request JSON valid?               | Gateway            |
| Does the customer exist?             | Customer Service   |
| Can the customer place this order?   | Order Service      |
| Are the requested products sellable? | Catalog Service    |
| Is the payment method allowed?       | Payment Service    |

The gateway can reject malformed requests. The domain service should reject invalid business requests.

---

#### Example gateway policy configuration

A gateway policy configuration might look like this:

```yaml
routes:
  - name: public-catalog
    match:
      pathPrefix: /api/catalog
      methods: [GET]
    target:
      service: catalog-service
    policies:
      authRequired: false
      cors:
        allowedOrigins:
          - https://app.example.com
      rateLimit:
        requestsPerMinute: 1000
      cache:
        ttlSeconds: 60
      maxRequestBodyBytes: 16384

  - name: create-order
    match:
      path: /api/orders
      methods: [POST]
    target:
      service: order-service
    policies:
      authRequired: true
      requiredScopes:
        - orders:write
      rateLimit:
        requestsPerMinute: 100
      requireHeaders:
        - Idempotency-Key
      maxRequestBodyBytes: 262144

  - name: payment-refund
    match:
      path: /api/payments/refunds
      methods: [POST]
    target:
      service: payment-service
    policies:
      authRequired: true
      requiredScopes:
        - payments:refund
      rateLimit:
        requestsPerMinute: 20
      maxRequestBodyBytes: 65536
```

This makes offloaded behavior explicit and reviewable.

---

#### Example service simplification

Without offloading, a service may need lots of infrastructure middleware:

```ts
app.use(parseTlsClientCertificate);
app.use(validateApiKey);
app.use(validateJwt);
app.use(rateLimit);
app.use(cors);
app.use(createRequestId);
app.use(accessLogger);
app.use(enforceRequestSize);
app.use(compressResponses);
```

With gateway offloading, the service can focus more on domain behavior:

```ts
app.post("/orders", async (req, res) => {
  const user = req.authenticatedUser;
  const command = req.body;

  const order = await orderService.createOrder({
    customerId: user.customerId,
    items: command.items,
    idempotencyKey: req.header("Idempotency-Key")
  });

  res.status(201).json(order);
});
```

The service may still verify trusted identity context and enforce domain rules, but it does not need to reimplement every edge concern.

---

#### Defense in depth

Gateway Offloading does not mean backend services should trust everything blindly.

A common mistake is assuming:

> The gateway checked security, so backend services do not need to.

That is dangerous.

A better mindset is:

> The gateway performs shared edge checks. Backend services still protect their own domain.

```mermaid
flowchart TD
    Gateway[API Gateway]

    EdgeChecks[Edge Checks<br/>Auth token<br/>Rate limit<br/>CORS<br/>Payload size]

    Service[Backend Service]

    DomainChecks[Domain Checks<br/>Resource ownership<br/>Business authorization<br/>State transitions]

    Gateway --> EdgeChecks
    EdgeChecks --> Service
    Service --> DomainChecks
```

Examples:

* The gateway verifies that a token is valid.
* The Order Service verifies that the user can access the requested order.
* The Payment Service verifies that a refund is allowed.
* The Inventory Service verifies that stock can be reserved.

This keeps security layered.

---

#### Gateway offloading and zero trust

In stronger security environments, backend services may still authenticate requests from the gateway or from other services.

This can involve:

* mTLS,
* signed internal headers,
* service identity,
* short-lived internal tokens,
* workload identity,
* service mesh policy.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    Service[Backend Service]

    Client -->|Public token| Gateway
    Gateway -->|mTLS + trusted identity context| Service
```

The gateway authenticates the external caller. The backend service verifies that the request came through trusted infrastructure.

This prevents attackers from bypassing the gateway and calling backend services directly.

---

#### Offloading in Kubernetes

In Kubernetes, gateway offloading may be implemented through:

* Ingress controllers,
* API gateways,
* service mesh ingress gateways,
* sidecars,
* load balancers,
* external gateway products.

Example Ingress-style routing with TLS:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: public-api
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "1m"
    nginx.ingress.kubernetes.io/enable-cors: "true"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls-cert
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /api/orders
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 80
          - path: /api/catalog
            pathType: Prefix
            backend:
              service:
                name: catalog-service
                port:
                  number: 80
```

This offloads TLS, request body limits, CORS, and route selection into the ingress layer.

More advanced API gateways can also handle API keys, OAuth, quotas, transformations, and analytics.

---

#### Operational concerns

The gateway becomes critical infrastructure when it offloads shared responsibilities.

You need to operate it carefully.

Important concerns:

| Concern               | Why it matters                                     |
| --------------------- | -------------------------------------------------- |
| High availability     | Gateway failure can affect all clients             |
| Horizontal scaling    | Gateway must handle peak traffic                   |
| Configuration testing | Bad policies can break many services               |
| Observability         | Gateway is the first place to debug edge issues    |
| Safe rollout          | Policy changes should be staged and reversible     |
| Ownership             | Teams need to know who manages gateway policies    |
| Security review       | Gateway controls public access                     |
| Performance           | Offloaded checks add latency if poorly implemented |

A gateway outage or bad gateway configuration can become a system-wide incident.

---

#### Observability

Gateway Offloading should produce detailed telemetry.

Track:

* total requests,
* requests by route,
* authentication failures,
* authorization failures,
* API key failures,
* rate-limit rejections,
* request-size rejections,
* CORS preflight volume,
* upstream latency,
* gateway latency,
* target service,
* status codes,
* cache hit rate,
* TLS handshake errors,
* policy evaluation failures.

Example log:

```json
{
  "requestId": "req_123",
  "route": "create-order",
  "targetService": "order-service",
  "authenticated": true,
  "userId": "user_456",
  "tenantId": "tenant_789",
  "rateLimited": false,
  "requestBodyBytes": 1824,
  "statusCode": 201,
  "gatewayLatencyMs": 8,
  "upstreamLatencyMs": 63
}
```

Gateway logs should be structured and searchable.

They are often the fastest way to answer:

* Did the request reach the service?
* Was it rejected by authentication?
* Was it rate-limited?
* Was the payload too large?
* Which backend service received it?
* Did the gateway or backend cause the latency?

---

#### When to use it

Use Gateway Offloading when:

* many services need the same edge behavior,
* external clients access multiple backend services,
* you need consistent authentication,
* you need consistent rate limiting,
* services should not each manage TLS certificates,
* browser clients require CORS,
* public APIs need API key validation,
* you need centralized access logs,
* request-size limits should be enforced consistently,
* you want backend services to focus on domain logic.

It is especially useful in systems with many APIs exposed through a common gateway.

---

#### When not to use it

Avoid or limit Gateway Offloading when:

* the concern is domain-specific,
* the logic requires deep business knowledge,
* the gateway would become a workflow engine,
* the offloaded behavior differs significantly per service,
* services are not exposed through a common edge,
* the gateway team cannot safely operate the policy,
* the gateway becomes a single point of organizational bottleneck.

For example, do not put refund eligibility rules in the gateway. That belongs in the Payment Service.

Do not put order cancellation rules in the gateway. That belongs in the Order Service.

Do not put pricing rules in the gateway. That belongs in Pricing or Promotions.

---

#### Benefits

**1. Reduces duplicated code**

Common infrastructure logic does not need to be implemented in every service.

**2. Improves consistency**

Authentication, rate limiting, CORS, logging, and request limits behave the same across services.

**3. Simplifies services**

Backend services can focus more on domain logic.

**4. Improves security at the edge**

The gateway can reject invalid or abusive requests before they reach services.

**5. Centralizes policy management**

Shared policies can be reviewed, versioned, and audited.

**6. Improves observability**

The gateway sees incoming traffic across the system.

**7. Makes operational changes easier**

Changing a rate limit or CORS policy may not require redeploying every service.

---

#### Trade-offs

**1. Gateway becomes critical infrastructure**

If it fails, many services may become unreachable.

**2. Gateway configuration becomes risky**

A bad policy can break many routes at once.

**3. Can become a hidden monolith**

If teams add business logic to the gateway, it becomes tightly coupled to many domains.

**4. Adds latency**

Every offloaded check adds some processing overhead.

**5. Services may over-trust the gateway**

Backend services still need domain authorization and defense in depth.

**6. Policy ownership can become unclear**

If many teams share one gateway, governance matters.

**7. Some concerns still need service-level handling**

Fine-grained authorization, domain validation, and business rules remain in services.

---

#### Common mistakes

**Mistake 1: Offloading business logic**

The gateway should not decide order state transitions, payment refund eligibility, inventory reservation rules, or pricing.

**Mistake 2: Trusting client-supplied internal headers**

The gateway must strip spoofable headers and create trusted context itself.

**Mistake 3: Assuming gateway auth is enough**

Services should still enforce domain-specific authorization.

**Mistake 4: No route-specific policies**

Different routes need different rate limits, payload sizes, timeouts, and auth requirements.

**Mistake 5: Manual policy changes without review**

Gateway policies should usually be version-controlled and reviewed.

**Mistake 6: Logging sensitive data**

Gateway logs can accidentally capture tokens, passwords, or personal information.

**Mistake 7: Making the gateway the only observability point**

Gateway telemetry is important, but backend services still need logs, metrics, and traces.

**Mistake 8: No fallback plan**

A gateway configuration error should be quickly reversible.

---

#### Practical design checklist

When deciding what to offload to the gateway, ask:

* Is this concern common across many services?
* Is it an edge concern or a domain concern?
* Can it be enforced without deep business knowledge?
* Does it need route-specific configuration?
* Who owns the policy?
* How is the policy tested?
* How is the policy deployed?
* How is the policy rolled back?
* What happens if the gateway rejects the request?
* What telemetry will be produced?
* Are sensitive headers stripped?
* Are trusted headers created only after authentication?
* Do backend services still enforce domain authorization?
* Are rate limits different for different plans or tenants?
* Are request-size limits route-specific?
* Are CORS origins explicit?
* Are gateway logs safe and useful?
* Can the gateway scale with peak traffic?

A good offloading design is likely if:

* the gateway handles common technical concerns,
* services retain business ownership,
* policies are explicit and version-controlled,
* route-specific differences are documented,
* requests are observable,
* security-sensitive headers are handled safely,
* backend services still enforce domain rules.

A poor offloading design is likely if:

* domain logic lives in the gateway,
* gateway policies are edited manually without review,
* clients can spoof identity or tenant headers,
* all routes use one generic policy,
* backend services blindly trust all gateway decisions,
* the gateway becomes hard to change because every team depends on it.

---

#### Related patterns

| Pattern                   | Relationship                                                                 |
| ------------------------- | ---------------------------------------------------------------------------- |
| API Gateway               | Gateway Offloading is one of the main reasons to use an API Gateway          |
| Gateway Routing           | Offloaded policies are often applied per route                               |
| Gateway Aggregation       | Aggregation may share gateway infrastructure but should avoid business logic |
| Backends for Frontends    | BFFs may sit behind a gateway that offloads common edge concerns             |
| Rate Limiting             | Commonly offloaded to the gateway                                            |
| Health Check              | Gateway may use health checks to avoid unhealthy services                    |
| Circuit Breaker           | Gateway may stop forwarding requests to failing services                     |
| Service Discovery         | Gateway may discover backend instances dynamically                           |
| External Configuration    | Gateway policies should be externalized and versioned                        |
| Zero Trust / mTLS         | Backend services may still verify trusted gateway-to-service communication   |
| Consumer-Driven Contracts | Helps ensure gateway-facing contracts remain safe for clients                |

---

#### Summary

Gateway Offloading moves common technical responsibilities from backend services into the API Gateway.

The central idea is:

> Offload shared edge concerns, not business decisions.

Good candidates include:

* TLS termination,
* authentication,
* API key validation,
* coarse authorization,
* rate limiting,
* CORS,
* request-size limits,
* logging,
* tracing,
* compression,
* simple validation,
* and response caching.

This improves consistency, reduces duplicated service code, and gives teams one place to manage edge behavior.

The main risk is putting too much into the gateway. A healthy gateway protects, routes, and observes traffic. It does not become the owner of pricing rules, order workflows, payment rules, inventory decisions, or other core domain behavior.


---

### 11. Backends for Frontends

**What it is**

Backends for Frontends creates separate backend services tailored to specific client experiences such as web, mobile, admin, partner, or smart TV.

**What it solves**

It avoids forcing every client to use the same generic backend API.

**Use cases**

Use it when clients need different payload sizes, response shapes, workflows, caching behavior, or release cadences.

**Benefits**

It improves client experience and lets client teams evolve independently.

**Trade-offs**

It increases the number of backend components and can duplicate logic if domain rules are placed in BFFs instead of domain services.

---

### 11. Backends for Frontends

#### What it is

**Backends for Frontends**, often abbreviated as **BFF**, is a pattern where each client experience gets its own backend service tailored to its needs.

Instead of forcing every client to use the same generic backend API, you create client-specific backend layers.

For example:

```mermaid
flowchart TD
    Web[Web App]
    Mobile[Mobile App]
    Admin[Admin Console]
    Partner[Partner API Client]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]
    AdminBFF[Admin BFF]
    PartnerBFF[Partner BFF]

    Services[Domain Services]

    Web --> WebBFF
    Mobile --> MobileBFF
    Admin --> AdminBFF
    Partner --> PartnerBFF

    WebBFF --> Services
    MobileBFF --> Services
    AdminBFF --> Services
    PartnerBFF --> Services
```

Each BFF is optimized for a specific type of client:

| Client        | BFF responsibility                                                   |
| ------------- | -------------------------------------------------------------------- |
| Web app       | Rich page-oriented responses, browser-friendly caching, full UI data |
| Mobile app    | Small payloads, fewer round trips, offline-friendly responses        |
| Admin console | Operational views, internal metadata, audit information              |
| Partner API   | Stable external contracts, strict quotas, partner-specific schemas   |
| Smart TV app  | Minimal interaction model, large-screen optimized data               |
| Wearable app  | Very small payloads, quick summary data                              |

The central idea is:

> Different clients often need different APIs, even when they use the same underlying domain services.

A BFF lets the backend API match the client experience instead of forcing all clients into one generic contract.

---

#### Why this pattern exists

A single generic API often starts simple.

```mermaid
flowchart TD
    Web[Web App]
    Mobile[Mobile App]
    Admin[Admin Console]

    GenericAPI[Generic Backend API]

    Orders[Order Service]
    Catalog[Catalog Service]
    Payments[Payment Service]
    Customers[Customer Service]

    Web --> GenericAPI
    Mobile --> GenericAPI
    Admin --> GenericAPI

    GenericAPI --> Orders
    GenericAPI --> Catalog
    GenericAPI --> Payments
    GenericAPI --> Customers
```

At first, this may work well. But over time, clients begin to need different things.

The web app may want a large response with everything needed to render a page.

The mobile app may want a compact response because mobile networks are slower and data usage matters.

The admin console may need internal fields that should never be exposed to regular customers.

The partner API may need a stable contract that changes slowly, even if internal services change quickly.

If one generic API tries to satisfy all of these needs, it often becomes awkward:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "items": [],
  "payment": {},
  "shipment": {},
  "adminMetadata": {},
  "mobileSummary": {},
  "webDisplayHints": {},
  "partnerFields": {},
  "internalDebugInfo": {}
}
```

The API becomes too broad, too coupled to many clients, and hard to evolve.

A BFF avoids this by giving each client a backend API designed for its own needs.

---

#### What it solves

Backends for Frontends solve the problem of **one-size-fits-all APIs**.

Without BFFs, client teams often face these problems:

* mobile clients receive payloads that are too large,
* web clients make too many calls to assemble one page,
* admin clients need internal fields that public clients should not see,
* partner APIs become coupled to internal service changes,
* each client duplicates aggregation logic,
* clients depend directly on microservice topology,
* API changes become slow because every client might break.

With BFFs, each client gets a tailored backend contract.

```mermaid
flowchart TD
    DomainServices[Domain Services]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]
    AdminBFF[Admin BFF]

    WebResponse[Web page view model]
    MobileResponse[Compact mobile response]
    AdminResponse[Operational admin response]

    DomainServices --> WebBFF
    DomainServices --> MobileBFF
    DomainServices --> AdminBFF

    WebBFF --> WebResponse
    MobileBFF --> MobileResponse
    AdminBFF --> AdminResponse
```

The domain services still own the business capabilities. The BFFs adapt those capabilities to client-specific use cases.

---

#### BFF vs API Gateway

BFFs and API Gateways are related, but they solve different problems.

An **API Gateway** is usually a general entry point for routing, authentication, rate limiting, TLS termination, and other edge concerns.

A **BFF** is a client-specific backend that shapes responses and workflows for a particular frontend.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    BFF[Backend for Frontend]
    Services[Domain Services]

    Client --> Gateway
    Gateway --> BFF
    BFF --> Services
```

A common architecture uses both:

| Responsibility                   | API Gateway   | BFF                                 |
| -------------------------------- | ------------- | ----------------------------------- |
| TLS termination                  | Yes           | Usually no                          |
| Authentication                   | Yes           | Sometimes consumes identity context |
| Rate limiting                    | Yes           | Sometimes client-specific limits    |
| Routing                          | Yes           | Usually behind gateway              |
| Client-specific response shaping | No or limited | Yes                                 |
| Screen-specific aggregation      | Limited       | Yes                                 |
| Domain rules                     | No            | No, should stay in domain services  |
| Client release support           | Limited       | Yes                                 |

The gateway protects and routes traffic. The BFF adapts backend capabilities to a specific client experience.

---

#### BFF vs Gateway Aggregation

Gateway Aggregation and BFFs overlap, but the intent differs.

**Gateway Aggregation** combines data from multiple services into one response.

**BFF** creates a backend tailored to a specific frontend or client type.

A gateway aggregation endpoint may be broadly useful:

```http
GET /api/order-summary/{orderId}
```

A mobile BFF endpoint may be specifically designed for a mobile screen:

```http
GET /mobile/home
```

A web BFF endpoint may return a richer page model:

```http
GET /web/order-detail/{orderId}
```

Comparison:

| Question                                              | Gateway Aggregation | BFF                                                          |
| ----------------------------------------------------- | ------------------- | ------------------------------------------------------------ |
| Is it client-specific?                                | Sometimes           | Yes                                                          |
| Is it usually read-focused?                           | Yes                 | Often, but can also coordinate client-specific command flows |
| Does it belong in shared gateway?                     | Sometimes           | Usually separate from gateway                                |
| Does it shape UI-specific responses?                  | Sometimes           | Yes                                                          |
| Can there be multiple versions for different clients? | Less commonly       | Yes                                                          |

BFFs are especially useful when clients differ significantly.

---

#### Example: web and mobile need different responses

Suppose both the web app and mobile app show order details.

The web app may want a rich response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "createdAt": "2026-04-29T12:00:00Z",
  "items": [
    {
      "productId": "prod_456",
      "title": "Trail Running Shoe",
      "description": "Lightweight running shoe for mixed terrain.",
      "imageUrl": "https://cdn.example.com/full/prod_456.jpg",
      "quantity": 1,
      "unitPrice": 129.99,
      "returnEligible": true,
      "supportArticles": [
        {
          "title": "How to clean trail running shoes",
          "url": "https://help.example.com/articles/cleaning"
        }
      ]
    }
  ],
  "payment": {
    "status": "AUTHORIZED",
    "methodLabel": "Visa ending in 4242"
  },
  "shipment": {
    "status": "PENDING",
    "estimatedDeliveryDate": "2026-05-03",
    "trackingUrl": null
  }
}
```

The mobile app may want a smaller response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "summary": "1 item · $129.99",
  "thumbnailUrl": "https://cdn.example.com/thumb/prod_456.jpg",
  "deliveryText": "Estimated delivery May 3"
}
```

Both responses may use the same underlying services:

```mermaid
flowchart TD
    Web[Web App]
    Mobile[Mobile App]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]

    Orders[Order Service]
    Catalog[Catalog Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Support[Support Service]

    Web --> WebBFF
    Mobile --> MobileBFF

    WebBFF --> Orders
    WebBFF --> Catalog
    WebBFF --> Payments
    WebBFF --> Shipping
    WebBFF --> Support

    MobileBFF --> Orders
    MobileBFF --> Catalog
    MobileBFF --> Shipping
```

The web BFF can return a rich view model. The mobile BFF can return a compact view model.

Neither client needs to know how backend services are split.

---

#### Example: admin client needs different data

An admin console often needs operational fields that regular users should not see.

Customer-facing response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99
}
```

Admin response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "riskScore": 0.17,
  "paymentAuthorizationId": "auth_789",
  "warehouseId": "wh_002",
  "internalNotes": [
    "Manual review not required"
  ],
  "audit": {
    "createdBy": "checkout-service",
    "lastUpdatedAt": "2026-04-29T12:15:00Z"
  }
}
```

A separate Admin BFF can enforce stronger authentication, different authorization, internal-only routing, and admin-specific response shapes.

```mermaid
flowchart TD
    Customer[Customer App]
    Admin[Admin Console]

    CustomerBFF[Customer BFF]
    AdminBFF[Admin BFF]

    Orders[Order Service]
    Risk[Risk Service]
    Warehouse[Warehouse Service]
    Audit[Audit Service]

    Customer --> CustomerBFF
    Admin --> AdminBFF

    CustomerBFF --> Orders

    AdminBFF --> Orders
    AdminBFF --> Risk
    AdminBFF --> Warehouse
    AdminBFF --> Audit
```

This avoids exposing admin-only concerns through the public customer API.

---

#### Basic architecture

A BFF usually sits between the API Gateway and domain services.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    BFF[Client-Specific BFF]

    Orders[Order Service]
    Catalog[Catalog Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Client --> Gateway
    Gateway --> BFF

    BFF --> Orders
    BFF --> Catalog
    BFF --> Payments
    BFF --> Shipping
```

The BFF may handle:

* client-specific endpoints,
* response shaping,
* aggregation,
* lightweight request transformation,
* client-specific caching,
* client-specific error formatting,
* coordinating simple client flows,
* adapting backend APIs to frontend needs.

The BFF should not own:

* core business rules,
* durable business state,
* payment decisions,
* inventory decisions,
* order lifecycle rules,
* pricing logic,
* authorization rules that require domain knowledge.

Those belong in domain services.

---

#### BFF responsibilities

A healthy BFF usually owns **experience composition**, not core domain behavior.

Good BFF responsibilities:

| Responsibility          | Example                                                 |
| ----------------------- | ------------------------------------------------------- |
| Response shaping        | Return compact mobile payloads                          |
| Aggregation             | Combine order, payment, and shipment data               |
| Client-specific caching | Cache mobile home screen summary for 30 seconds         |
| Protocol adaptation     | Convert frontend HTTP request to internal service calls |
| Error adaptation        | Convert backend errors into client-friendly errors      |
| Release compatibility   | Keep old mobile app versions working                    |
| View model construction | Build screen-specific response models                   |
| Feature flag adaptation | Hide or show fields depending on client capability      |

Risky BFF responsibilities:

| Responsibility                   | Why it is risky                                   |
| -------------------------------- | ------------------------------------------------- |
| Calculating order total          | Pricing or Order Service should own this          |
| Deciding refund eligibility      | Payment or Returns Service should own this        |
| Reserving inventory              | Inventory Service should own this                 |
| Managing order state transitions | Order Service should own this                     |
| Applying discount rules          | Pricing or Promotion Service should own this      |
| Storing source-of-truth data     | Domain services should own durable business state |

A useful rule:

> BFFs should compose and adapt; domain services should decide and persist.

---

#### Example implementation: Mobile BFF

Here is a simplified Mobile BFF endpoint in TypeScript using Express.

```ts
import express, { Request, Response } from "express";

const app = express();

type Order = {
  id: string;
  status: string;
  totalAmount: number;
  currency: string;
  items: Array<{
    productId: string;
    quantity: number;
  }>;
};

type Product = {
  productId: string;
  title: string;
  thumbnailUrl: string;
};

type Shipment = {
  orderId: string;
  status: string;
  estimatedDeliveryDate?: string;
};

async function getOrder(orderId: string): Promise<Order> {
  const response = await fetch(`http://orders-service/orders/${orderId}`);
  if (!response.ok) {
    throw new Error("Failed to fetch order");
  }

  return response.json() as Promise<Order>;
}

async function getProducts(productIds: string[]): Promise<Product[]> {
  const response = await fetch("http://catalog-service/products/batch", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ productIds })
  });

  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }

  return response.json() as Promise<Product[]>;
}

async function getShipment(orderId: string): Promise<Shipment | null> {
  const response = await fetch(`http://shipping-service/shipments/by-order/${orderId}`);

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error("Failed to fetch shipment");
  }

  return response.json() as Promise<Shipment>;
}

app.get("/mobile/orders/:orderId/summary", async (req: Request, res: Response) => {
  try {
    const order = await getOrder(req.params.orderId);

    const productIds = order.items.map((item) => item.productId);

    const [products, shipment] = await Promise.all([
      getProducts(productIds),
      getShipment(order.id)
    ]);

    const firstProduct = products[0];

    res.json({
      orderId: order.id,
      status: order.status,
      summary: `${order.items.length} item(s) · ${order.currency} ${order.totalAmount}`,
      thumbnailUrl: firstProduct?.thumbnailUrl,
      deliveryText: shipment?.estimatedDeliveryDate
        ? `Estimated delivery ${shipment.estimatedDeliveryDate}`
        : "Delivery date pending"
    });
  } catch {
    res.status(500).json({
      error: "MOBILE_ORDER_SUMMARY_FAILED",
      message: "Could not load order summary"
    });
  }
});

app.listen(3000, () => {
  console.log("Mobile BFF listening on port 3000");
});
```

This BFF endpoint returns exactly what the mobile screen needs. It does not expose every field from every backend service.

---

#### Example implementation: Web BFF

A Web BFF might return a richer page model.

```ts
app.get("/web/orders/:orderId/detail", async (req: Request, res: Response) => {
  try {
    const order = await ordersClient.getOrder(req.params.orderId);

    const [payment, shipment, products, support] = await Promise.all([
      paymentsClient.getPaymentByOrderId(order.id),
      shippingClient.getShipmentByOrderId(order.id),
      catalogClient.getProductsBatch(order.items.map((item) => item.productId)),
      supportClient.getSupportOptions(order.id)
    ]);

    const productsById = new Map(
      products.map((product) => [product.productId, product])
    );

    res.json({
      orderId: order.id,
      status: order.status,
      createdAt: order.createdAt,
      totalAmount: order.totalAmount,
      currency: order.currency,
      items: order.items.map((item) => {
        const product = productsById.get(item.productId);

        return {
          productId: item.productId,
          title: product?.title,
          imageUrl: product?.imageUrl,
          quantity: item.quantity,
          unitPrice: item.unitPrice
        };
      }),
      payment: {
        status: payment.status,
        methodLabel: payment.methodLabel
      },
      shipment: {
        status: shipment.status,
        trackingUrl: shipment.trackingUrl,
        estimatedDeliveryDate: shipment.estimatedDeliveryDate
      },
      support
    });
  } catch {
    res.status(500).json({
      error: "WEB_ORDER_DETAIL_FAILED",
      message: "Could not load order detail"
    });
  }
});
```

The Web BFF and Mobile BFF may call some of the same services, but they return different response shapes.

---

#### BFF and client release cadence

Different clients are released at different speeds.

| Client       | Release behavior                                           |
| ------------ | ---------------------------------------------------------- |
| Web app      | Can often be deployed many times per day                   |
| iOS app      | Requires App Store review and user updates                 |
| Android app  | May roll out gradually across devices                      |
| Smart TV app | Often slow and fragmented by device platform               |
| Partner API  | Requires long-term contract stability                      |
| Admin app    | Can usually change quickly but may need operational safety |

This matters because backend API changes affect clients differently.

A web app can be updated quickly if an API changes. A mobile app version may remain in use for months or years.

A Mobile BFF can support older app versions while allowing the backend domain services to evolve.

```mermaid
flowchart TD
    MobileV1[Mobile App v1]
    MobileV2[Mobile App v2]

    MobileBFF[Mobile BFF]

    V1Endpoint[/mobile/v1/order-summary]
    V2Endpoint[/mobile/v2/order-summary]

    Services[Domain Services]

    MobileV1 --> V1Endpoint
    MobileV2 --> V2Endpoint

    V1Endpoint --> MobileBFF
    V2Endpoint --> MobileBFF

    MobileBFF --> Services
```

The BFF can maintain compatibility with older clients while exposing improved responses to newer clients.

---

#### BFF and payload optimization

Mobile clients often need smaller payloads than web clients.

Large payloads are costly because they increase:

* network transfer time,
* battery usage,
* memory usage,
* parsing time,
* user-perceived latency.

A generic API might return too much:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "createdAt": "2026-04-29T12:00:00Z",
  "updatedAt": "2026-04-29T12:15:00Z",
  "items": [
    {
      "productId": "prod_456",
      "title": "Trail Running Shoe",
      "description": "Long description...",
      "imageUrl": "https://cdn.example.com/full/prod_456.jpg",
      "thumbnailUrl": "https://cdn.example.com/thumb/prod_456.jpg",
      "category": "Footwear",
      "brand": "SummitRun",
      "attributes": {
        "color": "Black",
        "size": "10",
        "weight": "250g"
      }
    }
  ],
  "payment": {
    "status": "AUTHORIZED",
    "methodType": "CARD",
    "methodLabel": "Visa ending in 4242",
    "authorizationId": "auth_789"
  },
  "shipment": {
    "status": "PENDING",
    "carrier": "UPS",
    "trackingUrl": null,
    "estimatedDeliveryDate": "2026-05-03"
  }
}
```

A mobile BFF can return only what the mobile screen needs:

```json
{
  "orderId": "ord_123",
  "status": "Confirmed",
  "imageUrl": "https://cdn.example.com/thumb/prod_456.jpg",
  "summary": "1 item · Delivery May 3"
}
```

This makes the mobile experience faster and more reliable.

---

#### BFF and caching

Different clients may need different caching strategies.

For example:

| Client       | Caching need                                     |
| ------------ | ------------------------------------------------ |
| Web app      | Cache page data briefly, rely on browser refresh |
| Mobile app   | Cache aggressively for poor networks             |
| Admin app    | Avoid stale operational data                     |
| Partner API  | Cache reference data, not transactional data     |
| Smart TV app | Cache home screen content for fast startup       |

A Mobile BFF might cache a home screen response:

```mermaid
flowchart TD
    Mobile[Mobile App]
    MobileBFF[Mobile BFF]
    Cache[(Mobile BFF Cache)]
    Services[Domain Services]

    Mobile --> MobileBFF
    MobileBFF --> Cache

    Cache -->|hit| MobileBFF
    Cache -->|miss| Services
```

Example:

```ts
app.get("/mobile/home", async (req, res) => {
  const userId = req.authenticatedUser.id;
  const cacheKey = `mobile-home:${userId}`;

  const cached = await cache.get(cacheKey);
  if (cached) {
    res.json(JSON.parse(cached));
    return;
  }

  const home = await buildMobileHome(userId);

  await cache.set(cacheKey, JSON.stringify(home), {
    ttlSeconds: 30
  });

  res.json(home);
});
```

Caching in a BFF must be careful. The cache key should include dimensions that affect the response:

* user,
* tenant,
* region,
* language,
* currency,
* client version,
* permissions,
* feature flags.

A bad cache key can leak user-specific data.

---

#### BFF and feature flags

BFFs are useful places to adapt responses based on client capabilities.

For example, a newer mobile app version may support a new shipment tracking card, while older versions do not.

```mermaid
flowchart TD
    Request[Mobile Request]
    MobileBFF[Mobile BFF]

    Version{Client Version}

    OldResponse[Old Response Shape]
    NewResponse[New Response Shape]

    Request --> MobileBFF
    MobileBFF --> Version

    Version -->|v1| OldResponse
    Version -->|v2| NewResponse
```

Example:

```ts
function supportsTrackingCard(clientVersion: string): boolean {
  return compareVersions(clientVersion, "2.5.0") >= 0;
}

app.get("/mobile/orders/:orderId", async (req, res) => {
  const clientVersion = req.header("X-Client-Version") ?? "1.0.0";

  const order = await ordersClient.getOrder(req.params.orderId);
  const shipment = await shippingClient.getShipmentByOrderId(order.id);

  const response: Record<string, unknown> = {
    orderId: order.id,
    status: order.status
  };

  if (supportsTrackingCard(clientVersion)) {
    response.trackingCard = {
      status: shipment.status,
      estimatedDeliveryDate: shipment.estimatedDeliveryDate
    };
  }

  res.json(response);
});
```

This lets the client and backend evolve safely together.

---

#### BFF and GraphQL

GraphQL is sometimes used as a BFF technology.

A GraphQL BFF lets clients request exactly the fields they need.

```mermaid
flowchart TD
    Web[Web App]
    Mobile[Mobile App]

    GraphQLBFF[GraphQL BFF]

    Orders[Order Service]
    Catalog[Catalog Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Web --> GraphQLBFF
    Mobile --> GraphQLBFF

    GraphQLBFF --> Orders
    GraphQLBFF --> Catalog
    GraphQLBFF --> Payments
    GraphQLBFF --> Shipping
```

Example query:

```graphql
query OrderSummary($orderId: ID!) {
  order(id: $orderId) {
    id
    status
    totalAmount
    shipment {
      status
      estimatedDeliveryDate
    }
  }
}
```

GraphQL can reduce over-fetching and under-fetching, but it does not remove the need for good boundaries.

GraphQL resolvers can still create problems:

* N+1 backend calls,
* weak authorization,
* hidden coupling to many services,
* complex caching,
* expensive queries,
* unclear ownership.

A GraphQL BFF should still be treated as a BFF: a client-facing composition layer, not the owner of core domain rules.

---

#### BFF and authorization

A BFF often receives authenticated user context from an API Gateway or identity provider.

It may enforce client-specific access checks, but domain-specific authorization should remain in the domain services.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    BFF[BFF]
    Service[Domain Service]

    Client --> Gateway
    Gateway -->|Authenticated identity| BFF
    BFF -->|User context| Service
```

Example:

* Gateway validates the token.
* BFF checks that the user is allowed to use the mobile API.
* Order Service checks whether the user can access order `ord_123`.

The BFF should not bypass service-level authorization by using an overpowered service account and returning whatever it fetches.

Bad approach:

```mermaid
flowchart TD
    BFF[BFF with broad service token]
    Orders[Order Service]
    Client[Client]

    Client --> BFF
    BFF -->|Can read all orders| Orders
```

Better approach:

```mermaid
flowchart TD
    Client[Client]
    BFF[BFF]
    Orders[Order Service]

    Client --> BFF
    BFF -->|User context included| Orders
    Orders -->|Checks access to specific order| BFF
```

The domain service should protect its own data.

---

#### BFF and error handling

BFFs can translate backend errors into client-friendly errors.

For example, an Order Service may return:

```json
{
  "error": "ORDER_STATE_TRANSITION_REJECTED",
  "details": {
    "currentState": "SHIPPED",
    "requestedTransition": "CANCELLED"
  }
}
```

A mobile BFF may return:

```json
{
  "error": "ORDER_CANNOT_BE_CANCELLED",
  "message": "This order has already shipped and can no longer be cancelled."
}
```

An admin BFF may return more operational detail:

```json
{
  "error": "ORDER_CANNOT_BE_CANCELLED",
  "message": "Order cannot be cancelled because it is already in SHIPPED state.",
  "currentState": "SHIPPED",
  "allowedActions": ["CREATE_RETURN", "CONTACT_SUPPORT"]
}
```

Different clients may need different error formats.

But the BFF should not hide important domain semantics. It should adapt errors for the client while preserving enough meaning for correct behavior.

---

#### BFF and partial failures

BFFs often aggregate data from multiple services. Some failures may be acceptable.

For example, a mobile home screen may still load even if recommendations are unavailable.

```mermaid
flowchart TD
    MobileBFF[Mobile BFF]

    Profile[Profile Service]
    Orders[Order Service]
    Recommendations[Recommendation Service Unavailable]

    Response[Partial Home Response]

    MobileBFF --> Profile
    MobileBFF --> Orders
    MobileBFF -. failed .-> Recommendations

    Profile --> Response
    Orders --> Response
```

Example response:

```json
{
  "user": {
    "displayName": "Alex"
  },
  "recentOrders": [
    {
      "orderId": "ord_123",
      "status": "Delivered"
    }
  ],
  "recommendations": [],
  "warnings": [
    {
      "code": "RECOMMENDATIONS_UNAVAILABLE",
      "message": "Recommendations are temporarily unavailable."
    }
  ]
}
```

However, some failures should fail the request.

For example:

| Missing data                      | Should response continue? |
| --------------------------------- | ------------------------- |
| User profile on account page      | Usually no                |
| Order itself on order detail page | No                        |
| Recommendations                   | Usually yes               |
| Reviews                           | Often yes                 |
| Authorization decision            | No                        |
| Payment status on payment screen  | Usually no                |

The BFF should define required and optional dependencies clearly.

---

#### BFF and avoiding duplication

The biggest risk with BFFs is duplicate logic.

If Web BFF, Mobile BFF, and Admin BFF all implement the same domain rule, the system becomes inconsistent.

Bad:

```mermaid
flowchart TD
    WebBFF[Web BFF<br/>refund rule]
    MobileBFF[Mobile BFF<br/>refund rule]
    AdminBFF[Admin BFF<br/>refund rule]

    Payments[Payment Service]
```

Better:

```mermaid
flowchart TD
    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]
    AdminBFF[Admin BFF]

    Payments[Payment Service<br/>owns refund rule]

    WebBFF --> Payments
    MobileBFF --> Payments
    AdminBFF --> Payments
```

The BFFs may present refund eligibility differently, but the Payment or Returns Service should decide whether the refund is allowed.

Example:

```ts
// Good BFF behavior:
const eligibility = await returnsClient.getReturnEligibility(orderId);

res.json({
  canReturn: eligibility.allowed,
  message: eligibility.allowed
    ? "This item can be returned."
    : eligibility.reasonMessage
});
```

The BFF displays the decision. It does not own the rule.

---

#### BFF and team ownership

BFFs work best when they align with client teams.

```mermaid
flowchart TD
    WebTeam[Web Team]
    MobileTeam[Mobile Team]
    AdminTeam[Admin Team]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]
    AdminBFF[Admin BFF]

    WebTeam --> WebBFF
    MobileTeam --> MobileBFF
    AdminTeam --> AdminBFF
```

This allows the team building the client experience to evolve its backend contract.

For example:

* The Mobile Team can optimize payloads without waiting for the Web Team.
* The Admin Team can add operational fields without exposing them to customers.
* The Partner API Team can maintain long-term compatibility for external clients.

BFF ownership should be clear. A BFF with no owner becomes a dumping ground.

---

#### BFF and deployment

BFFs may deploy independently from both clients and domain services.

```mermaid
flowchart TD
    ClientRelease[Client Release]
    BFFRelease[BFF Release]
    ServiceRelease[Domain Service Release]

    ClientRelease --> BFFRelease
    BFFRelease --> ServiceRelease
```

This independent deployment can be valuable.

For example:

* A Web BFF can be deployed with a web app release.
* A Mobile BFF can support multiple app versions at once.
* An Admin BFF can ship internal features quickly.
* A Partner BFF can change slowly and preserve public contracts.

However, each BFF adds another deployable component.

That means more:

* CI/CD pipelines,
* monitoring,
* logs,
* alerts,
* security reviews,
* dependencies,
* operational ownership.

Do not create BFFs casually. Use them when client differences justify the extra component.

---

#### BFF and versioning

Mobile and partner clients often need explicit versioning.

Example route structure:

```http
GET /mobile/v1/orders/{orderId}
GET /mobile/v2/orders/{orderId}
```

Or version headers:

```http
GET /mobile/orders/{orderId}
X-Mobile-API-Version: 2
```

A BFF can support older versions while internally calling newer domain services.

```mermaid
flowchart TD
    MobileV1[Mobile App v1]
    MobileV2[Mobile App v2]

    MobileBFF[Mobile BFF]

    AdapterV1[v1 Response Adapter]
    AdapterV2[v2 Response Adapter]

    Services[Domain Services]

    MobileV1 --> MobileBFF
    MobileV2 --> MobileBFF

    MobileBFF --> AdapterV1
    MobileBFF --> AdapterV2

    AdapterV1 --> Services
    AdapterV2 --> Services
```

This is useful because users may not update mobile apps immediately.

A versioning strategy should include:

* supported versions,
* deprecation timelines,
* telemetry by client version,
* compatibility tests,
* app minimum-version policies,
* sunset communication.

---

#### BFF and observability

BFFs should be observable because they sit close to user experience.

Track:

* endpoint latency,
* client version,
* platform,
* user or tenant ID when appropriate,
* downstream service latency,
* downstream errors,
* partial response count,
* cache hit rate,
* response size,
* feature flag decisions,
* dependency timeout count,
* client-specific error rates.

Example structured log:

```json
{
  "requestId": "req_123",
  "bff": "mobile-bff",
  "clientPlatform": "ios",
  "clientVersion": "2.7.1",
  "route": "/mobile/orders/ord_123/summary",
  "statusCode": 200,
  "latencyMs": 84,
  "dependencies": {
    "orders": {
      "status": 200,
      "latencyMs": 31
    },
    "catalog": {
      "status": 200,
      "latencyMs": 27
    },
    "shipping": {
      "status": 200,
      "latencyMs": 40
    }
  },
  "responseBytes": 512
}
```

This helps answer:

* Is the mobile app slow because of the BFF or a downstream service?
* Which client versions are still calling old endpoints?
* Are partial responses increasing?
* Are response payloads too large?
* Which dependency is causing user-visible latency?

Distributed tracing is also important.

```mermaid
flowchart TD
    Client[Client]
    BFF[BFF]

    Orders[Order Service]
    Catalog[Catalog Service]
    Shipping[Shipping Service]

    Trace[Distributed Trace]

    Client --> BFF
    BFF --> Orders
    BFF --> Catalog
    BFF --> Shipping

    Trace -. includes .-> BFF
    Trace -. includes .-> Orders
    Trace -. includes .-> Catalog
    Trace -. includes .-> Shipping
```

---

#### BFF and testing

BFFs need tests because they translate between client expectations and backend service contracts.

Useful tests include:

| Test type             | Purpose                                    |
| --------------------- | ------------------------------------------ |
| Unit tests            | Verify response shaping and mapping logic  |
| Contract tests        | Ensure BFF satisfies frontend expectations |
| Integration tests     | Verify calls to backend services           |
| Snapshot tests        | Detect unexpected response shape changes   |
| Compatibility tests   | Ensure older client versions still work    |
| Authorization tests   | Verify users cannot access forbidden data  |
| Partial failure tests | Verify degraded responses work             |
| Performance tests     | Check latency and payload size             |

Example mapping test:

```ts
describe("buildMobileOrderSummary", () => {
  it("returns compact order summary for mobile", () => {
    const result = buildMobileOrderSummary({
      order: {
        id: "ord_123",
        status: "CONFIRMED",
        totalAmount: 129.99,
        currency: "USD",
        items: [{ productId: "prod_456", quantity: 1 }]
      },
      firstProduct: {
        productId: "prod_456",
        title: "Trail Running Shoe",
        thumbnailUrl: "https://cdn.example.com/thumb/prod_456.jpg"
      },
      shipment: {
        orderId: "ord_123",
        status: "PENDING",
        estimatedDeliveryDate: "2026-05-03"
      }
    });

    expect(result).toEqual({
      orderId: "ord_123",
      status: "CONFIRMED",
      summary: "1 item · USD 129.99",
      thumbnailUrl: "https://cdn.example.com/thumb/prod_456.jpg",
      deliveryText: "Estimated delivery 2026-05-03"
    });
  });
});
```

The BFF contract should be tested from the client’s perspective.

---

#### When to use it

Use Backends for Frontends when:

* different clients need different response shapes,
* mobile needs smaller payloads than web,
* clients have different release cadences,
* clients need different caching behavior,
* clients need different authentication or authorization flows,
* clients duplicate aggregation logic,
* a generic API is becoming bloated,
* admin users need internal fields,
* partner APIs require stable external contracts,
* client teams need more autonomy,
* frontend performance suffers from too many backend calls.

Common examples:

* Web BFF,
* Mobile BFF,
* Admin BFF,
* Partner BFF,
* Smart TV BFF,
* Public API BFF,
* Internal tools BFF.

---

#### When not to use it

Avoid BFFs when:

* there is only one client,
* all clients need the same API shape,
* the generic API is simple and stable,
* the team cannot operate additional backend services,
* the BFF would only pass requests through,
* the main problem is poor domain service design,
* client-specific needs can be solved with query parameters or field selection,
* the organization is likely to duplicate domain logic across BFFs.

For a small system, a single backend API may be better.

For simple differences, you may not need separate BFFs. For example, optional fields or sparse fieldsets may be enough:

```http
GET /orders/ord_123?fields=id,status,totalAmount
```

Do not create extra deployable services unless the client-specific benefits justify the cost.

---

#### Benefits

**1. Better client experience**

Each client gets an API designed for its own screens, workflows, and constraints.

**2. Smaller payloads**

Mobile and constrained clients can receive only the data they need.

**3. Fewer client round trips**

The BFF can aggregate data from multiple backend services.

**4. Client team autonomy**

Frontend teams can evolve their backend contract without waiting for every other client team.

**5. Better compatibility management**

A Mobile BFF can support older app versions while domain services evolve.

**6. Improved security separation**

Admin, partner, public, and customer APIs can have different policies and response shapes.

**7. Cleaner domain services**

Domain services do not need to include presentation-specific response formats for every client.

---

#### Trade-offs

**1. More backend components**

Each BFF needs deployment, monitoring, testing, and ownership.

**2. Risk of duplicated logic**

If domain rules are implemented in multiple BFFs, behavior becomes inconsistent.

**3. More integration points**

BFFs depend on multiple backend services and must handle failures carefully.

**4. Potential for inconsistent client behavior**

Different BFFs may expose different interpretations unless domain services remain authoritative.

**5. Operational overhead**

More services mean more pipelines, logs, alerts, dashboards, and on-call responsibility.

**6. Versioning complexity**

Mobile and partner BFFs may need to support old versions for a long time.

**7. Risk of becoming mini-monoliths**

A BFF can become too large if it absorbs workflows, domain rules, and persistence.

---

#### Common mistakes

**Mistake 1: Putting domain rules in the BFF**

The BFF should not decide refund eligibility, pricing, inventory availability, or order state transitions.

**Mistake 2: Creating a BFF for every screen**

A BFF should usually serve a client experience, not necessarily one service per page.

**Mistake 3: Building pass-through BFFs**

If a BFF only forwards requests without adapting anything, it may not be worth the extra component.

**Mistake 4: Duplicating logic across BFFs**

Shared business decisions should live in domain services.

**Mistake 5: Ignoring old client versions**

Mobile and partner clients may continue using older contracts longer than expected.

**Mistake 6: Weak authorization**

BFFs must not fetch broad data with powerful credentials and filter casually.

**Mistake 7: Poor observability**

BFFs are close to user experience. They need strong latency, error, and dependency telemetry.

**Mistake 8: Letting BFFs own durable business state**

BFFs may cache or store presentation state, but domain services should own source-of-truth business data.

---

#### Practical design checklist

Before creating a BFF, answer:

* Which client is this BFF for?
* What problems does the current generic API create?
* Does this client need a different response shape?
* Does this client need smaller payloads?
* Does this client need different caching behavior?
* Does this client have a different release cadence?
* Which domain services will the BFF call?
* Which data is required?
* Which data is optional?
* What happens when each dependency fails?
* What authorization context will be passed downstream?
* What domain rules must remain in domain services?
* Does this BFF need versioning?
* How long must old client versions be supported?
* Who owns the BFF?
* How will response contracts be tested?
* How will latency and payload size be monitored?
* Is a BFF truly needed, or would query parameters, field selection, or gateway aggregation be enough?

A BFF design is probably healthy if:

* it is clearly tied to a client experience,
* it reduces client complexity,
* it shapes responses without owning domain rules,
* it has clear ownership,
* it preserves user and tenant authorization context,
* it supports client versioning where needed,
* it has strong observability,
* it avoids duplicating business logic.

A BFF design is probably unhealthy if:

* it only passes requests through,
* it owns core business decisions,
* it stores source-of-truth business data,
* every client-specific request creates another service,
* no team owns it,
* it calls too many services without timeouts,
* it hides backend failures without logging,
* it duplicates logic from other BFFs.

---

#### Related patterns

| Pattern                   | Relationship                                                                |
| ------------------------- | --------------------------------------------------------------------------- |
| API Gateway               | BFFs often sit behind a gateway that handles edge concerns                  |
| Gateway Routing           | Gateway may route web, mobile, admin, and partner traffic to different BFFs |
| Gateway Aggregation       | BFFs often perform aggregation tailored to a client                         |
| Gateway Offloading        | Gateway handles shared technical concerns before requests reach BFFs        |
| CQRS                      | BFFs may query read models optimized for client screens                     |
| Consumer-Driven Contracts | Useful for testing BFF contracts against frontend expectations              |
| Anti-Corruption Layer     | BFFs may use ACLs when adapting legacy systems                              |
| Service Discovery         | BFFs need to locate backend services                                        |
| Circuit Breaker           | Protects BFFs from failing downstream dependencies                          |
| Cache-Aside               | BFFs often cache client-specific read models                                |
| API Versioning            | Especially important for mobile and partner BFFs                            |

---

#### Summary

Backends for Frontends create separate backend services tailored to specific client experiences such as web, mobile, admin, partner, smart TV, or wearable clients.

The central idea is:

> Different clients should not be forced to use the same generic backend API when their needs are meaningfully different.

A good BFF:

* returns client-specific response shapes,
* reduces client round trips,
* optimizes payload size,
* supports client release cadence,
* adapts errors for the client,
* handles partial failures carefully,
* preserves authorization context,
* and keeps domain rules in domain services.

The main risk is duplication. If BFFs start owning pricing rules, order rules, refund rules, or inventory decisions, the system becomes inconsistent. BFFs should compose and adapt; domain services should decide and persist.


---

### 13. Client-Side UI Composition / Micro Frontend Composition

#### What it is

**Client-Side UI Composition** is a pattern where the user interface is assembled in the client by combining independently owned UI modules, data sources, or frontend fragments.

In a microservice architecture, backend ownership is often split across services. Micro frontend composition applies a similar idea to the frontend: different teams can own different parts of the user experience.

For example, a product detail page may be composed from several independently owned areas:

```mermaid
flowchart TD
    ProductPage[Product Detail Page]

    Gallery[Product Gallery Module]
    Details[Product Details Module]
    Pricing[Pricing Module]
    Inventory[Availability Module]
    Reviews[Reviews Module]
    Recommendations[Recommendations Module]
    Promotions[Promotions Module]

    ProductPage --> Gallery
    ProductPage --> Details
    ProductPage --> Pricing
    ProductPage --> Inventory
    ProductPage --> Reviews
    ProductPage --> Recommendations
    ProductPage --> Promotions
```

Each module may be owned by a different team:

| UI area                            | Owning team             |
| ---------------------------------- | ----------------------- |
| Product title, description, images | Catalog Team            |
| Price and discounts                | Pricing Team            |
| Inventory availability             | Inventory Team          |
| Reviews                            | Reviews Team            |
| Recommendations                    | Personalization Team    |
| Promotions                         | Marketing Platform Team |

The central idea is:

> The frontend can be composed from independently owned pieces instead of being one large application controlled by one team.

This pattern can be implemented in several ways:

* independent frontend modules inside one shell application,
* micro frontends loaded at runtime,
* client-side calls to different APIs,
* web components,
* module federation,
* iframes,
* independently deployed frontend packages,
* server-provided UI fragments rendered by the client.

---

#### Why this pattern exists

As applications grow, the frontend can become a monolith even if the backend is made of microservices.

```mermaid
flowchart TD
    Frontend[Frontend Monolith]

    CatalogUI[Catalog UI]
    PricingUI[Pricing UI]
    ReviewsUI[Reviews UI]
    CheckoutUI[Checkout UI]
    AccountUI[Account UI]
    AdminUI[Admin UI]

    Frontend --> CatalogUI
    Frontend --> PricingUI
    Frontend --> ReviewsUI
    Frontend --> CheckoutUI
    Frontend --> AccountUI
    Frontend --> AdminUI
```

This can create problems:

* many teams must change the same codebase,
* releases require coordination,
* one broken area can delay the whole frontend release,
* teams cannot choose suitable implementation details,
* ownership boundaries are unclear,
* a small UI change may require a large regression test cycle,
* the frontend becomes a bottleneck even though backend services are independent.

Micro frontend composition tries to make UI ownership match product or domain ownership.

```mermaid
flowchart TD
    Shell[Application Shell]

    CatalogMF[Catalog Micro Frontend]
    PricingMF[Pricing Micro Frontend]
    ReviewsMF[Reviews Micro Frontend]
    CheckoutMF[Checkout Micro Frontend]
    AccountMF[Account Micro Frontend]

    Shell --> CatalogMF
    Shell --> PricingMF
    Shell --> ReviewsMF
    Shell --> CheckoutMF
    Shell --> AccountMF
```

Each area can be built, tested, released, and operated by the team that owns that part of the user experience.

---

#### What it solves

Client-Side UI Composition solves **frontend ownership bottlenecks**.

Without it, several backend-aligned teams may need to work through one frontend team or one frontend release process.

```mermaid
flowchart TD
    CatalogTeam[Catalog Team]
    PricingTeam[Pricing Team]
    ReviewsTeam[Reviews Team]
    RecommendationsTeam[Recommendations Team]

    FrontendTeam[Central Frontend Team]
    FrontendApp[Single Frontend Application]

    CatalogTeam --> FrontendTeam
    PricingTeam --> FrontendTeam
    ReviewsTeam --> FrontendTeam
    RecommendationsTeam --> FrontendTeam

    FrontendTeam --> FrontendApp
```

This can slow down delivery. The central frontend team becomes a queue.

With micro frontend composition, ownership can be distributed:

```mermaid
flowchart TD
    CatalogTeam[Catalog Team]
    PricingTeam[Pricing Team]
    ReviewsTeam[Reviews Team]
    RecommendationsTeam[Recommendations Team]

    CatalogUI[Catalog UI Module]
    PricingUI[Pricing UI Module]
    ReviewsUI[Reviews UI Module]
    RecommendationsUI[Recommendations UI Module]

    Shell[Application Shell]

    CatalogTeam --> CatalogUI
    PricingTeam --> PricingUI
    ReviewsTeam --> ReviewsUI
    RecommendationsTeam --> RecommendationsUI

    Shell --> CatalogUI
    Shell --> PricingUI
    Shell --> ReviewsUI
    Shell --> RecommendationsUI
```

Teams can move independently while still contributing to one user experience.

---

#### Client-side composition vs server-side composition

There are two broad ways to compose a user experience:

1. **Server-side composition**
2. **Client-side composition**

In server-side composition, a backend or server-rendering layer assembles the page or response before sending it to the browser.

```mermaid
flowchart TD
    Browser[Browser]
    CompositionServer[Composition Server]

    Catalog[Catalog Service]
    Pricing[Pricing Service]
    Reviews[Reviews Service]

    Browser --> CompositionServer

    CompositionServer --> Catalog
    CompositionServer --> Pricing
    CompositionServer --> Reviews

    CompositionServer --> Browser
```

In client-side composition, the browser or client app assembles the page by loading modules and data.

```mermaid
flowchart TD
    Browser[Browser]

    Shell[Application Shell]

    CatalogModule[Catalog Module]
    PricingModule[Pricing Module]
    ReviewsModule[Reviews Module]

    CatalogAPI[Catalog API]
    PricingAPI[Pricing API]
    ReviewsAPI[Reviews API]

    Browser --> Shell

    Shell --> CatalogModule
    Shell --> PricingModule
    Shell --> ReviewsModule

    CatalogModule --> CatalogAPI
    PricingModule --> PricingAPI
    ReviewsModule --> ReviewsAPI
```

Comparison:

| Approach                | Strengths                                                | Trade-offs                                         |
| ----------------------- | -------------------------------------------------------- | -------------------------------------------------- |
| Server-side composition | Better first load, centralized rendering, easier SEO     | Composition layer can become bottleneck            |
| Client-side composition | Independent UI ownership, dynamic loading, team autonomy | More frontend complexity and runtime failure modes |
| Hybrid                  | Balanced performance and ownership                       | More architectural complexity                      |

Many real systems use a hybrid approach. For example, the server may render the shell and critical content, while client-side modules load less critical areas such as reviews or recommendations.

---

#### Basic architecture

A typical micro frontend architecture has an **application shell**.

The shell owns common page infrastructure:

* routing,
* layout,
* authentication context,
* navigation,
* design system,
* global error boundaries,
* shared telemetry,
* feature flag context,
* module loading.

Feature teams own individual UI modules.

```mermaid
flowchart TD
    AppShell[Application Shell]

    Routing[Routing]
    Layout[Layout]
    Auth[Auth Context]
    DesignSystem[Design System]
    Telemetry[Telemetry]
    ModuleLoader[Module Loader]

    ProductMF[Product Micro Frontend]
    ReviewsMF[Reviews Micro Frontend]
    RecommendationsMF[Recommendations Micro Frontend]

    AppShell --> Routing
    AppShell --> Layout
    AppShell --> Auth
    AppShell --> DesignSystem
    AppShell --> Telemetry
    AppShell --> ModuleLoader

    ModuleLoader --> ProductMF
    ModuleLoader --> ReviewsMF
    ModuleLoader --> RecommendationsMF
```

The shell should provide shared infrastructure, but it should not become the place where all product logic lives.

---

#### Example: product detail page

A product detail page is a common example.

```mermaid
flowchart TD
    ProductPage[Product Detail Page]

    ProductInfo[Product Info Module]
    PriceBox[Price Box Module]
    Availability[Availability Module]
    Reviews[Reviews Module]
    Recommendations[Recommendations Module]

    ProductAPI[Catalog API]
    PricingAPI[Pricing API]
    InventoryAPI[Inventory API]
    ReviewsAPI[Reviews API]
    RecAPI[Recommendation API]

    ProductPage --> ProductInfo
    ProductPage --> PriceBox
    ProductPage --> Availability
    ProductPage --> Reviews
    ProductPage --> Recommendations

    ProductInfo --> ProductAPI
    PriceBox --> PricingAPI
    Availability --> InventoryAPI
    Reviews --> ReviewsAPI
    Recommendations --> RecAPI
```

Each module can load its own data.

For example:

* Product Info loads product title, images, and description.
* Price Box loads current price, discounts, and tax information.
* Availability loads stock status and delivery estimate.
* Reviews loads ratings and review snippets.
* Recommendations loads related products.

This gives teams independence, but it also creates client-side complexity. The page now has multiple loading states and multiple possible failure modes.

---

#### Example React composition

Here is a simplified React example where a product page composes independently owned modules.

```tsx
import React from "react";

type ProductPageProps = {
  productId: string;
};

export function ProductPage({ productId }: ProductPageProps) {
  return (
    <main>
      <section>
        <ProductInfo productId={productId} />
      </section>

      <aside>
        <PriceBox productId={productId} />
        <Availability productId={productId} />
      </aside>

      <section>
        <Reviews productId={productId} />
      </section>

      <section>
        <Recommendations productId={productId} />
      </section>
    </main>
  );
}
```

Each module owns its own data fetching:

```tsx
import React, { useEffect, useState } from "react";

type Price = {
  amount: number;
  currency: string;
  discounted: boolean;
};

export function PriceBox({ productId }: { productId: string }) {
  const [price, setPrice] = useState<Price | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadPrice() {
      try {
        const response = await fetch(`/api/pricing/products/${productId}`);

        if (!response.ok) {
          throw new Error("Failed to fetch price");
        }

        const data = (await response.json()) as Price;

        if (!cancelled) {
          setPrice(data);
        }
      } catch {
        if (!cancelled) {
          setError(true);
        }
      }
    }

    loadPrice();

    return () => {
      cancelled = true;
    };
  }, [productId]);

  if (error) {
    return <div>Price temporarily unavailable</div>;
  }

  if (!price) {
    return <div>Loading price...</div>;
  }

  return (
    <div>
      <strong>
        {price.currency} {price.amount}
      </strong>
      {price.discounted && <span> Sale</span>}
    </div>
  );
}
```

This module can be developed and released by the Pricing Team, while the Reviews module can be owned by another team.

---

#### Runtime module loading

Some micro frontend systems load modules at runtime.

```mermaid
flowchart TD
    Browser[Browser]
    Shell[Application Shell]

    Manifest[Module Manifest]

    CatalogBundle[Catalog UI Bundle]
    ReviewsBundle[Reviews UI Bundle]
    PricingBundle[Pricing UI Bundle]

    Browser --> Shell
    Shell --> Manifest

    Manifest --> CatalogBundle
    Manifest --> ReviewsBundle
    Manifest --> PricingBundle

    Shell --> CatalogBundle
    Shell --> ReviewsBundle
    Shell --> PricingBundle
```

A manifest might describe which module bundle to load:

```json
{
  "modules": {
    "productInfo": {
      "url": "https://cdn.example.com/catalog-ui/1.8.2/product-info.js",
      "team": "catalog"
    },
    "priceBox": {
      "url": "https://cdn.example.com/pricing-ui/2.3.0/price-box.js",
      "team": "pricing"
    },
    "reviews": {
      "url": "https://cdn.example.com/reviews-ui/1.4.1/reviews.js",
      "team": "reviews"
    }
  }
}
```

Runtime loading allows independent deployments. The Pricing Team can release a new price box without redeploying the whole application shell.

The trade-off is that runtime failures become more likely:

* module bundle fails to load,
* module version is incompatible with shell,
* CDN issue breaks part of page,
* dependency conflict occurs,
* module is slow to initialize.

Because of this, runtime-loaded modules need clear contracts and safe fallbacks.

---

#### Module Federation example

In JavaScript ecosystems, Webpack Module Federation is a common way to load micro frontends.

A shell app may declare remote modules:

```js
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "shell",
      remotes: {
        catalog: "catalog@https://cdn.example.com/catalog/remoteEntry.js",
        pricing: "pricing@https://cdn.example.com/pricing/remoteEntry.js",
        reviews: "reviews@https://cdn.example.com/reviews/remoteEntry.js"
      },
      shared: {
        react: {
          singleton: true,
          requiredVersion: "^18.0.0"
        },
        "react-dom": {
          singleton: true,
          requiredVersion: "^18.0.0"
        }
      }
    })
  ]
};
```

Then the shell can import remote components:

```tsx
import React, { Suspense } from "react";

const ProductInfo = React.lazy(() => import("catalog/ProductInfo"));
const PriceBox = React.lazy(() => import("pricing/PriceBox"));
const Reviews = React.lazy(() => import("reviews/Reviews"));

export function ProductPage({ productId }: { productId: string }) {
  return (
    <main>
      <Suspense fallback={<div>Loading product...</div>}>
        <ProductInfo productId={productId} />
      </Suspense>

      <Suspense fallback={<div>Loading price...</div>}>
        <PriceBox productId={productId} />
      </Suspense>

      <Suspense fallback={<div>Loading reviews...</div>}>
        <Reviews productId={productId} />
      </Suspense>
    </main>
  );
}
```

This allows separate teams to deploy independently. But it also requires careful version management, shared dependency control, and runtime error handling.

---

#### Error boundaries

In micro frontend composition, one module should not crash the entire page.

React error boundaries are commonly used to isolate failures.

```tsx
import React from "react";

type ErrorBoundaryState = {
  hasError: boolean;
};

export class ErrorBoundary extends React.Component<
  { fallback: React.ReactNode; children: React.ReactNode },
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = {
    hasError: false
  };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return {
      hasError: true
    };
  }

  componentDidCatch(error: Error) {
    console.error("Micro frontend failed", error);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}
```

Usage:

```tsx
export function ProductPage({ productId }: { productId: string }) {
  return (
    <main>
      <ErrorBoundary fallback={<div>Product information unavailable</div>}>
        <ProductInfo productId={productId} />
      </ErrorBoundary>

      <ErrorBoundary fallback={<div>Price unavailable</div>}>
        <PriceBox productId={productId} />
      </ErrorBoundary>

      <ErrorBoundary fallback={<div>Reviews unavailable</div>}>
        <Reviews productId={productId} />
      </ErrorBoundary>
    </main>
  );
}
```

This is important because independent modules fail independently. The page should degrade gracefully.

---

#### Loading states

Client-side composition creates multiple loading states.

```mermaid
flowchart TD
    Page[Page Load]

    Product[Product module loading]
    Price[Price module loading]
    Reviews[Reviews module loading]
    Recommendations[Recommendations module loading]

    ProductDone[Product loaded]
    PriceDone[Price loaded]
    ReviewsDone[Reviews loaded]
    RecDone[Recommendations loaded]

    Page --> Product
    Page --> Price
    Page --> Reviews
    Page --> Recommendations

    Product --> ProductDone
    Price --> PriceDone
    Reviews --> ReviewsDone
    Recommendations --> RecDone
```

If unmanaged, this can create a poor user experience where the page jumps around as modules load.

Good practices include:

* skeleton loading states,
* reserved layout space,
* progressive rendering,
* priority loading for critical content,
* lazy loading for below-the-fold modules,
* clear fallback states,
* avoiding layout shift,
* sharing loading indicators where appropriate.

Example:

```tsx
function ProductPageSkeleton() {
  return (
    <main>
      <div className="skeleton product-title" />
      <div className="skeleton product-image" />
      <div className="skeleton price-box" />
      <div className="skeleton reviews" />
    </main>
  );
}
```

Not every module has equal priority. Product title and price may be critical. Recommendations may be deferred.

---

#### Performance considerations

Client-side UI composition can improve team independence but hurt performance if poorly designed.

Important performance risks:

**Too many network calls**

Each module may call its own API.

```mermaid
flowchart TD
    Browser[Browser]

    ProductModule[Product Module]
    PriceModule[Price Module]
    ReviewsModule[Reviews Module]
    RecModule[Recommendations Module]

    ProductAPI[Product API]
    PricingAPI[Pricing API]
    ReviewsAPI[Reviews API]
    RecAPI[Recommendation API]

    Browser --> ProductModule
    Browser --> PriceModule
    Browser --> ReviewsModule
    Browser --> RecModule

    ProductModule --> ProductAPI
    PriceModule --> PricingAPI
    ReviewsModule --> ReviewsAPI
    RecModule --> RecAPI
```

This can be acceptable for some pages, but it can also create a waterfall or too much frontend fan-out.

**Too much JavaScript**

Each micro frontend may bring its own dependencies. If teams do not coordinate, the page can load duplicate libraries.

**Slow module initialization**

Runtime-loaded modules can delay rendering.

**Layout shift**

Modules loading at different times can cause the page to move.

**Inconsistent caching**

Each module may cache data differently.

Mitigations:

* use shared dependencies,
* set bundle size budgets,
* lazy-load noncritical modules,
* use server-side rendering for critical content,
* use BFFs or aggregators for data-heavy views,
* batch API calls when possible,
* preload important modules,
* monitor Core Web Vitals,
* enforce design system consistency.

---

#### Data fetching strategies

There are several ways micro frontends can get data.

##### Strategy 1: Each module fetches its own data

```mermaid
flowchart TD
    ModuleA[Product Module]
    ModuleB[Price Module]
    ModuleC[Reviews Module]

    ProductAPI[Product API]
    PricingAPI[Pricing API]
    ReviewsAPI[Reviews API]

    ModuleA --> ProductAPI
    ModuleB --> PricingAPI
    ModuleC --> ReviewsAPI
```

Benefits:

* strong module independence,
* each team owns its data needs,
* modules can evolve separately.

Trade-offs:

* many network calls,
* inconsistent loading states,
* harder global caching,
* more authorization complexity.

##### Strategy 2: Shell fetches shared page data

```mermaid
flowchart TD
    Shell[Application Shell]

    PageAPI[Page API or BFF]

    ProductModule[Product Module]
    PriceModule[Price Module]
    ReviewsModule[Reviews Module]

    Shell --> PageAPI

    Shell --> ProductModule
    Shell --> PriceModule
    Shell --> ReviewsModule
```

Benefits:

* fewer network calls,
* better initial performance,
* consistent page-level loading.

Trade-offs:

* shell or BFF becomes more coupled to modules,
* changes require coordination,
* less module autonomy.

##### Strategy 3: Hybrid data fetching

```mermaid
flowchart TD
    Shell[Application Shell]
    BFF[Page BFF]

    CriticalData[Critical Page Data]

    ProductModule[Product Module]
    PriceModule[Price Module]
    ReviewsModule[Reviews Module]
    RecommendationsModule[Recommendations Module]

    ReviewsAPI[Reviews API]
    RecAPI[Recommendations API]

    Shell --> BFF
    BFF --> CriticalData

    CriticalData --> ProductModule
    CriticalData --> PriceModule

    ReviewsModule --> ReviewsAPI
    RecommendationsModule --> RecAPI
```

This is often the most practical approach.

The shell or BFF loads critical data needed for the initial render. Less critical modules fetch their own data later.

---

#### Shared design system

Micro frontends need a shared design system to avoid a fragmented user experience.

Without shared UI standards, each team may create inconsistent components:

```mermaid
flowchart TD
    ProductUI[Product UI<br/>Button style A]
    ReviewsUI[Reviews UI<br/>Button style B]
    PricingUI[Pricing UI<br/>Button style C]

    Page[Same Page]

    Page --> ProductUI
    Page --> ReviewsUI
    Page --> PricingUI
```

A shared design system provides:

* typography,
* colors,
* spacing,
* buttons,
* form controls,
* layout primitives,
* accessibility rules,
* icons,
* error states,
* loading states,
* responsive behavior.

```mermaid
flowchart TD
    DesignSystem[Shared Design System]

    ProductMF[Product Micro Frontend]
    PricingMF[Pricing Micro Frontend]
    ReviewsMF[Reviews Micro Frontend]

    DesignSystem --> ProductMF
    DesignSystem --> PricingMF
    DesignSystem --> ReviewsMF
```

The design system should be versioned carefully. Breaking changes can affect many micro frontends.

---

#### Communication between micro frontends

Micro frontends sometimes need to communicate.

For example:

* selecting a product variant changes price and availability,
* adding an item to cart updates the header cart count,
* applying a promotion updates the checkout summary,
* changing location updates delivery estimates.

Avoid tight coupling between modules.

Bad:

```tsx
priceBox.setInventoryModuleState(...);
```

Better approaches include:

* shared application state for small global concerns,
* custom events,
* URL state,
* shell-provided context,
* event bus with strict contracts.

Example using browser custom events:

```ts
type ProductVariantSelectedEvent = CustomEvent<{
  productId: string;
  variantId: string;
}>;

function publishVariantSelected(productId: string, variantId: string) {
  window.dispatchEvent(
    new CustomEvent("product-variant-selected", {
      detail: {
        productId,
        variantId
      }
    })
  );
}
```

Listener:

```ts
window.addEventListener("product-variant-selected", (event) => {
  const typedEvent = event as ProductVariantSelectedEvent;

  reloadPrice({
    productId: typedEvent.detail.productId,
    variantId: typedEvent.detail.variantId
  });
});
```

Communication contracts should be documented. Otherwise, modules become coupled through hidden events.

---

#### Authorization and security

Client-side composition creates security challenges.

Important rule:

> The client can improve user experience, but the server must enforce security.

A micro frontend can hide a button, but it cannot be the only access control.

Bad security model:

```mermaid
flowchart TD
    UI[Micro Frontend]
    HideButton[Hide admin button]
    API[Backend API]

    UI --> HideButton
    HideButton --> API
```

If the backend API does not enforce authorization, a user can still call the API directly.

Better:

```mermaid
flowchart TD
    UI[Micro Frontend]
    API[Backend API]
    Authz[Server-side Authorization]

    UI --> API
    API --> Authz
```

Other security concerns:

* do not expose secrets in frontend modules,
* do not trust client-provided tenant IDs,
* validate authorization on backend APIs,
* avoid loading untrusted remote modules,
* use content security policy,
* use subresource integrity where applicable,
* protect against cross-site scripting,
* validate module manifests,
* restrict who can publish frontend bundles.

Runtime-loaded micro frontends are executable code. Treat module loading as a supply-chain security concern.

---

#### Versioning and compatibility

Micro frontends need compatibility between:

* shell version,
* module version,
* shared design system version,
* shared runtime libraries,
* API versions,
* event contracts.

A shell may load modules through a manifest:

```json
{
  "shellVersion": "4.2.0",
  "modules": {
    "pricing": {
      "version": "2.3.1",
      "url": "https://cdn.example.com/pricing/2.3.1/remoteEntry.js",
      "compatibleShell": ">=4.0.0 <5.0.0"
    },
    "reviews": {
      "version": "1.9.0",
      "url": "https://cdn.example.com/reviews/1.9.0/remoteEntry.js",
      "compatibleShell": ">=4.1.0 <5.0.0"
    }
  }
}
```

Compatibility failures should be handled gracefully.

For example:

```tsx
function MicroFrontendUnavailable({ name }: { name: string }) {
  return (
    <section>
      <p>{name} is temporarily unavailable.</p>
    </section>
  );
}
```

Never assume every remote module will load correctly.

---

#### Deployment models

Micro frontends can be deployed in several ways.

##### Build-time integration

Modules are packaged into the application at build time.

```mermaid
flowchart TD
    ProductPackage[Product UI Package]
    ReviewsPackage[Reviews UI Package]
    PricingPackage[Pricing UI Package]

    Build[Application Build]

    App[Single Deployed Frontend]

    ProductPackage --> Build
    ReviewsPackage --> Build
    PricingPackage --> Build

    Build --> App
```

Benefits:

* simpler runtime,
* fewer loading failures,
* easier performance optimization.

Trade-offs:

* less independent deployment,
* shell must be rebuilt to pick up module changes.

##### Runtime integration

Modules are loaded dynamically at runtime.

```mermaid
flowchart TD
    Shell[Application Shell]
    CDN[CDN]

    ProductBundle[Product Bundle]
    ReviewsBundle[Reviews Bundle]
    PricingBundle[Pricing Bundle]

    Shell --> CDN

    CDN --> ProductBundle
    CDN --> ReviewsBundle
    CDN --> PricingBundle
```

Benefits:

* stronger independent deployment,
* teams can release modules separately.

Trade-offs:

* more runtime complexity,
* version compatibility issues,
* module loading failures,
* harder performance tuning.

##### Route-level integration

Each large section of the app is its own frontend.

```mermaid
flowchart TD
    Router[Frontend Router]

    ProductApp[Product App]
    CheckoutApp[Checkout App]
    AccountApp[Account App]
    AdminApp[Admin App]

    Router -->|/products/*| ProductApp
    Router -->|/checkout/*| CheckoutApp
    Router -->|/account/*| AccountApp
    Router -->|/admin/*| AdminApp
```

This is simpler than composing many modules on one page. It works well when ownership boundaries align with routes.

##### Page-fragment integration

Multiple independently owned fragments appear on the same page.

```mermaid
flowchart TD
    Page[Product Page]

    ProductInfo[Product Info Fragment]
    Price[Price Fragment]
    Reviews[Reviews Fragment]
    Recommendations[Recommendations Fragment]

    Page --> ProductInfo
    Page --> Price
    Page --> Reviews
    Page --> Recommendations
```

This gives fine-grained ownership but adds more coordination complexity.

---

#### Observability

Micro frontends need frontend observability.

Track:

* module load time,
* module render time,
* module load failures,
* JavaScript errors by module,
* API failures by module,
* user interactions,
* client version,
* shell version,
* module version,
* bundle size,
* layout shifts,
* slow renders,
* fallback usage.

Example client-side telemetry event:

```json
{
  "eventType": "MicroFrontendLoadFailed",
  "page": "ProductDetail",
  "module": "Reviews",
  "moduleVersion": "1.9.0",
  "shellVersion": "4.2.0",
  "error": "RemoteEntryLoadFailed",
  "url": "https://cdn.example.com/reviews/1.9.0/remoteEntry.js",
  "occurredAt": "2026-04-29T12:00:00Z"
}
```

Frontend telemetry should include ownership information. When a module fails, the owning team should be able to identify and fix it.

---

#### Testing strategy

Micro frontend testing should happen at several levels.

| Test type               | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| Unit tests              | Test module behavior in isolation                 |
| Contract tests          | Verify module inputs, outputs, and events         |
| Integration tests       | Verify module works inside shell                  |
| Visual regression tests | Catch layout and design regressions               |
| Accessibility tests     | Ensure consistent accessibility                   |
| End-to-end tests        | Verify critical user journeys                     |
| Performance tests       | Track bundle size, load time, and render time     |
| Compatibility tests     | Verify module works with supported shell versions |

Example contract for a module:

```ts
type PriceBoxProps = {
  productId: string;
  selectedVariantId?: string;
  currency: string;
  onPriceLoaded?: (price: {
    amount: number;
    currency: string;
  }) => void;
};
```

This contract should be stable and documented. If the shell depends on it, changing it should require versioning or coordination.

---

#### When to use it

Use Client-Side UI Composition or Micro Frontend Composition when:

* multiple teams own different parts of the UI,
* the frontend has become a monolith,
* teams need independent release cycles,
* different page areas map to different domain ownership,
* route-level ownership is clear,
* client-side performance can be managed,
* the organization has strong frontend platform practices,
* teams can follow shared design system and observability standards.

Common examples include:

* e-commerce product pages,
* marketplace seller and buyer experiences,
* admin platforms with many domain areas,
* SaaS platforms with independently owned modules,
* financial dashboards,
* content platforms,
* customer portals,
* super-apps with many product teams.

---

#### When not to use it

Avoid or delay this pattern when:

* the frontend is small,
* one team owns the whole user experience,
* independent deployment is not needed,
* the organization lacks frontend platform maturity,
* performance is already difficult to manage,
* shared design standards are weak,
* teams are likely to duplicate logic,
* client-side security and observability are immature,
* a simpler modular frontend would solve the problem.

A modular frontend inside one codebase may be enough:

```mermaid
flowchart TD
    FrontendApp[Frontend Application]

    ProductModule[Product Module]
    CheckoutModule[Checkout Module]
    AccountModule[Account Module]

    FrontendApp --> ProductModule
    FrontendApp --> CheckoutModule
    FrontendApp --> AccountModule
```

You do not need independently deployed micro frontends unless the organizational and release benefits justify the complexity.

---

#### Benefits

**1. Independent UI ownership**

Teams can own the frontend parts that correspond to their domain or product area.

**2. Independent release cycles**

A reviews module can ship without redeploying the entire frontend.

**3. Reduced central frontend bottleneck**

Teams do not need to route every UI change through one central frontend team.

**4. Better alignment with domain teams**

The team that owns Pricing can own the pricing UI. The team that owns Reviews can own the reviews UI.

**5. Technology flexibility**

Some teams may use different tools, though this should be governed carefully.

**6. Incremental migration**

A frontend monolith can be gradually split by route or page section.

**7. Fault isolation**

With error boundaries, one module can fail without taking down the whole page.

---

#### Trade-offs

**1. More frontend complexity**

Runtime loading, shared dependencies, versioning, and cross-module communication are difficult.

**2. Performance risk**

Multiple bundles and API calls can hurt load time and user experience.

**3. Inconsistent user experience**

Without a strong design system, modules may look and behave differently.

**4. More failure modes**

A page can partially fail if one module fails to load or one API is slow.

**5. Harder testing**

End-to-end behavior depends on multiple independently deployed pieces.

**6. Dependency duplication**

Different modules may ship duplicate libraries, increasing bundle size.

**7. Security risk**

Loading independently deployed frontend code increases supply-chain and runtime trust concerns.

**8. Coordination does not disappear**

Teams still need shared contracts, design standards, observability, and release compatibility.

---

#### Common mistakes

**Mistake 1: Using micro frontends because microservices exist**

Backend microservices do not automatically require frontend microservices.

**Mistake 2: Splitting too finely**

A separate micro frontend for every small widget creates unnecessary complexity.

**Mistake 3: No shared design system**

The UI becomes inconsistent and unprofessional.

**Mistake 4: No error boundaries**

One broken module can crash the whole page.

**Mistake 5: Too many client-side API calls**

Each module fetching independently can create poor performance.

**Mistake 6: Duplicating domain logic in UI modules**

Business rules should remain in backend domain services.

**Mistake 7: Weak version management**

Shell and module incompatibility can break production.

**Mistake 8: No ownership metadata**

When a module fails, teams must know who owns it.

**Mistake 9: Treating the client as a security boundary**

Authorization must be enforced on the server.

---

#### Practical design checklist

Before adopting micro frontend composition, answer:

* What problem are we solving: ownership, release independence, migration, or performance?
* Which teams own which UI areas?
* Are boundaries route-level or page-fragment-level?
* Does each module have a clear owner?
* Will modules be integrated at build time or runtime?
* How are module versions managed?
* How are shared dependencies managed?
* Is there a shared design system?
* How are accessibility standards enforced?
* How are module failures isolated?
* What loading states are required?
* What fallbacks exist for failed modules?
* How many API calls will the page make?
* Are critical data calls aggregated through a BFF?
* How is authentication context shared?
* How is authorization enforced on backend APIs?
* How do modules communicate?
* Are event contracts documented?
* How are module load times measured?
* How are JavaScript errors attributed to teams?
* What is the rollback plan for a broken module?

A good micro frontend design is likely if:

* ownership boundaries are clear,
* modules are not too small,
* the shell remains thin,
* shared design standards are strong,
* failures are isolated,
* performance is measured,
* contracts are versioned,
* domain rules stay out of UI modules,
* backend APIs enforce authorization.

A weak design is likely if:

* modules are split only by technical preference,
* every widget becomes independently deployed,
* teams duplicate business rules,
* the page makes excessive API calls,
* modules cannot fail safely,
* users see inconsistent design,
* shell and module versions frequently break each other,
* nobody owns frontend platform standards.

---

#### Related patterns

| Pattern                          | Relationship                                                       |
| -------------------------------- | ------------------------------------------------------------------ |
| Backends for Frontends           | Often used to provide client-specific APIs for micro frontends     |
| Gateway Aggregation              | Can reduce frontend fan-out by composing backend data              |
| API Gateway                      | Provides the shared edge for frontend APIs                         |
| Decompose by Business Capability | UI ownership often follows business capability ownership           |
| Decompose by Subdomain           | Frontend modules may align with bounded contexts                   |
| Consumer-Driven Contracts        | Useful for module and API contracts                                |
| Strangler Fig Pattern            | Can be used to gradually migrate a frontend monolith               |
| Anti-Corruption Layer            | May protect new UI modules from legacy frontend or backend models  |
| CQRS                             | Read models can support complex composed UI screens                |
| Event-Driven Architecture        | Can update UI views through event-fed read models or subscriptions |
| Observability Patterns           | Critical for tracking module load failures and frontend errors     |

---

#### Summary

Client-Side UI Composition builds a user interface by combining independently owned frontend modules, UI fragments, or data-driven components in the client.

The central idea is:

> Let different teams own and release different parts of the user experience without forcing everything through one frontend monolith.

This pattern works well when large applications have clear UI ownership boundaries and teams need independent release cycles.

A good implementation has:

* a thin application shell,
* clear module ownership,
* shared design system,
* stable module contracts,
* error boundaries,
* loading and fallback states,
* frontend observability,
* careful performance management,
* server-side authorization,
* and strong version compatibility.

The main risk is complexity. Micro frontends can improve autonomy, but they also introduce runtime loading issues, inconsistent UX, duplicated dependencies, and harder testing. Use them when the organizational benefits are strong enough to justify the frontend complexity.


---

## 4. Service Communication and Workflow Patterns

These patterns define how services coordinate synchronous, asynchronous, and long-running work.

### 14. Smart Endpoints, Dumb Pipes

**What it is**

Smart Endpoints, Dumb Pipes means business logic lives in services, while communication infrastructure stays simple.

**What it solves**

It avoids turning middleware, gateways, brokers, or service buses into hidden monoliths.

**Use cases**

Use this principle when designing event buses, message brokers, API gateways, service meshes, and integration layers.

**Benefits**

It keeps business ownership inside services.

**Trade-offs**

Some complexity moves into services, so teams must avoid duplicating shared rules.

---

### 15. Chained Microservice Pattern

**What it is**

A Chained Microservice Pattern is a synchronous sequence where one service calls another, which calls another, and so on.

**What it solves**

It provides a straightforward way to execute simple workflows where each step depends on the previous step.

**Use cases**

Use it for short, simple, low-latency workflows with reliable dependencies.

**Benefits**

It is conceptually simple.

**Trade-offs**

Latency and failure risk compound through the chain. Long chains are fragile.

---

### 16. Branch Pattern

**What it is**

The Branch Pattern sends a request to multiple services in parallel or conditionally routes it through different paths.

**What it solves**

It supports workflows where multiple independent service calls are needed or where request types require different paths.

**Use cases**

Use it for data enrichment, multi-provider logic, tenant-specific workflows, regional behavior, and conditional processing.

**Benefits**

Parallel branching can reduce latency.

**Trade-offs**

Error handling becomes more complex because branches may succeed or fail independently.

---

### 17. Async Messaging

**What it is**

Async Messaging uses queues, topics, event streams, or brokers so services communicate without requiring immediate responses.

**What it solves**

It removes temporal coupling between services.

**Use cases**

Use it for event-driven workflows, background jobs, notifications, audit pipelines, data replication, long-running processing, and loose coupling.

**Benefits**

It improves resilience and scalability.

**Trade-offs**

Async systems need idempotency, ordering rules, retry policies, dead-letter queues, duplicate handling, observability, and schema governance.

---

### 18. Choreography

**What it is**

Choreography is a workflow style where services react to events and decide independently what to do next.

**What it solves**

It avoids tight coupling to a central orchestrator.

**Use cases**

Use it when multiple services need to react independently to business events.

**Benefits**

It supports loose coupling and autonomy.

**Trade-offs**

The workflow can become difficult to understand because logic is distributed across services.

---

### 19. Saga Pattern

**What it is**

Saga coordinates a distributed business transaction through local transactions and compensating actions.

**What it solves**

It avoids global distributed database transactions while preserving business-level consistency.

**Use cases**

Use it for order placement, travel booking, payments, subscription activation, onboarding, loan approval, and inventory reservation.

**Benefits**

It allows distributed workflows while preserving service autonomy.

**Trade-offs**

Sagas are eventually consistent, and compensation can be difficult when real-world actions cannot be undone perfectly.

---

### 20. Consumer-Driven Contracts

**What it is**

Consumer-Driven Contracts are agreements where consumers define the API or message behavior they require, and providers test against those expectations.

**What it solves**

It prevents accidental breaking changes in provider APIs or message schemas.

**Use cases**

Use it for REST APIs, gRPC APIs, event schemas, message queues, shared internal APIs, and multi-team platforms.

**Benefits**

It supports independent deployment with greater confidence.

**Trade-offs**

Contracts require discipline and should capture real consumer needs rather than every implementation detail.

---

## 5. Data Ownership, Persistence, and Consistency Patterns

These patterns define how services store, own, query, and synchronize data.

### 21. Database per Service

**What it is**

Each service owns its own database or schema, and other services access that data only through APIs, events, or messages.

**What it solves**

It eliminates database-level coupling and gives each service ownership of its schema.

**Use cases**

Use it when services need independent deployment, schema evolution, scaling, and data ownership.

**Benefits**

It enables service autonomy and supports polyglot persistence.

**Trade-offs**

Cross-service queries and transactions become harder.

---

### 22. Shared Database

**What it is**

Shared Database means multiple services use the same physical database or database instance.

**What it solves**

It reduces operational complexity, especially during migration from a monolith or in smaller systems.

**Use cases**

Use it as a transitional pattern or controlled compromise.

**Benefits**

It can simplify reporting, joins, and early migration.

**Trade-offs**

It can recreate monolithic coupling when multiple services depend on the same tables.

---

### 23. CQRS

**What it is**

CQRS separates write operations from read operations. Commands change state; queries read state.

**What it solves**

It avoids forcing one data model to serve both transactional writes and complex reads.

**Use cases**

Use it when reads and writes have different performance, security, scaling, or modeling needs.

**Benefits**

Write models can focus on correctness while read models focus on fast queries.

**Trade-offs**

Read models must be synchronized, often through events, which can introduce eventual consistency.

---

### 24. Event Sourcing

**What it is**

Event Sourcing stores changes as immutable events rather than only storing current state.

**What it solves**

It preserves the full history of how the system reached its current state.

**Use cases**

Use it for banking, payments, insurance, healthcare, compliance-heavy workflows, order lifecycle tracking, and audit-heavy systems.

**Benefits**

It provides complete history, replay, temporal analysis, and strong auditability.

**Trade-offs**

It adds complexity around event versioning, replay, storage, and mental models.

---

### 25. Polyglot Persistence

**What it is**

Polyglot Persistence allows different services to use different storage technologies based on their needs.

**What it solves**

It avoids forcing every service into a single database model.

**Use cases**

Use it when services need different persistence models, such as relational transactions, search, graph traversal, document storage, caching, or time-series metrics.

**Benefits**

Each service can use the best storage model for its job.

**Trade-offs**

It increases operational complexity and requires expertise in multiple data technologies.

---

### 26. Data Sharding

**What it is**

Data Sharding partitions data across multiple database instances or shards.

**What it solves**

It addresses database scale limits when one database cannot handle volume, traffic, or throughput.

**Use cases**

Use it when data volume, read traffic, write throughput, or tenant scale exceeds one database’s capacity.

**Benefits**

It improves scalability and can isolate load.

**Trade-offs**

Cross-shard queries, rebalancing, hotspots, backups, and migrations become harder.

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

## 9. Deployment, Release, and Production Validation Patterns

These patterns reduce release risk and allow safer production validation.

### 37. Blue-Green Deployment

**What it is**

Blue-Green Deployment uses two production-like environments: one active and one inactive. The new version is deployed to the inactive environment, validated, and then traffic is switched.

**What it solves**

It reduces deployment downtime and rollback risk.

**Use cases**

Use it for APIs, backend services, web applications, infrastructure upgrades, and major releases where rollback speed matters.

**Benefits**

It enables near-zero-downtime deployment and fast rollback.

**Trade-offs**

It requires duplicate infrastructure temporarily, and database migrations can be difficult.

---

### 38. Shadow Deployment

**What it is**

Shadow Deployment sends a copy of real production traffic to a new version without affecting users.

**What it solves**

It validates new behavior under real traffic before exposing users to it.

**Use cases**

Use it for rewritten services, new algorithms, new databases, fraud models, recommendation models, performance optimizations, and migration validation.

**Benefits**

It provides high-confidence production validation without user impact.

**Trade-offs**

Shadow traffic increases load and must avoid side effects such as writes, emails, payments, or irreversible actions.

---

## 10. API Design Patterns

API design patterns define endpoint responsibility, representation structure, quality controls, and evolution practices for APIs that expose or compose microservices.

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

