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

#### What it is

**Smart Endpoints, Dumb Pipes** is a microservice design principle that says business logic should live inside services, while the communication infrastructure between services should stay as simple and generic as possible.

In this phrase:

* **Smart endpoints** are the services. They own business rules, decisions, workflows, validation, state transitions, and domain behavior.
* **Dumb pipes** are the communication mechanisms. They move requests, responses, commands, or events between services without becoming the place where business logic lives.

The principle can be summarized as:

> Services should make business decisions. Infrastructure should move messages.

For example, this is the desired direction:

```mermaid
flowchart TD
    OrderService[Order Service<br/>owns order rules]
    PaymentService[Payment Service<br/>owns payment rules]
    InventoryService[Inventory Service<br/>owns inventory rules]

    Broker[(Message Broker<br/>routes events)]

    OrderService -->|OrderCreated| Broker
    Broker --> PaymentService
    Broker --> InventoryService
```

The broker moves events. It does not decide whether an order is valid, whether payment should be authorized, or whether inventory can be reserved.

A problematic design puts business logic in the infrastructure layer:

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    SmartBus[Enterprise Service Bus<br/>order rules<br/>payment rules<br/>inventory rules<br/>workflow logic]

    OrderService --> SmartBus
    SmartBus --> PaymentService
    SmartBus --> InventoryService
```

In that design, the service bus becomes a hidden monolith. The system may look distributed, but important business behavior is centralized in the middleware.

---

#### Why this pattern exists

Many older service-oriented architectures used powerful middleware such as Enterprise Service Buses, centralized workflow engines, complex integration platforms, or heavy gateway layers.

These tools often started with good intentions:

* route messages,
* transform formats,
* connect systems,
* coordinate workflows,
* apply policies,
* reduce duplicated integration code.

But over time, they sometimes accumulated business logic.

For example, a service bus might start by routing order events:

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[Service Bus]
    Payments[Payment Service]

    Orders -->|OrderCreated| Bus
    Bus --> Payments
```

Then teams add a simple transformation:

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[Service Bus<br/>maps order fields]
    Payments[Payment Service]

    Orders --> Bus
    Bus --> Payments
```

Then they add a business rule:

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[Service Bus<br/>if order total > 1000<br/>send to fraud check]
    Fraud[Fraud Service]
    Payments[Payment Service]

    Orders --> Bus
    Bus --> Fraud
    Bus --> Payments
```

Then they add more workflow logic:

```mermaid
flowchart TD
    Orders[Order Service]
    SmartBus[Service Bus<br/>validates order<br/>checks customer status<br/>calculates route<br/>starts payment<br/>reserves inventory<br/>handles exceptions]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Customer[Customer Service]

    Orders --> SmartBus
    SmartBus --> Customer
    SmartBus --> Payments
    SmartBus --> Inventory
```

At that point, the bus is no longer just infrastructure. It has become a central business application.

This creates many problems:

* business rules are hard to find,
* services no longer own their domain behavior,
* changes require central middleware coordination,
* teams become dependent on a shared integration team,
* testing becomes difficult,
* deployment becomes risky,
* the middleware becomes a bottleneck,
* the architecture becomes a distributed monolith.

Smart Endpoints, Dumb Pipes exists to prevent this.

---

#### What it solves

This principle solves the problem of **business logic migrating into infrastructure**.

In a healthy microservice architecture, business ownership should be clear:

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]
    ShippingService[Shipping Service]

    OrderRules[Order lifecycle rules]
    PaymentRules[Payment authorization rules]
    InventoryRules[Inventory reservation rules]
    ShippingRules[Shipment rules]

    OrderService --> OrderRules
    PaymentService --> PaymentRules
    InventoryService --> InventoryRules
    ShippingService --> ShippingRules
```

Each service owns its own decisions.

The communication layer should help services talk to each other:

```mermaid
flowchart TD
    ServiceA[Service A]
    Pipe[Simple Communication Infrastructure]
    ServiceB[Service B]

    ServiceA --> Pipe
    Pipe --> ServiceB
```

The pipe may provide useful technical features:

* message delivery,
* routing,
* retries,
* buffering,
* backpressure,
* authentication,
* encryption,
* observability,
* dead-letter queues,
* schema validation,
* service discovery.

But it should avoid owning domain rules such as:

* whether an order can be cancelled,
* whether a payment should be refunded,
* whether a customer qualifies for a discount,
* whether inventory should be reserved,
* whether a claim should be approved.

Those decisions belong in the services that own the domain.

---

#### Smart endpoints

A **smart endpoint** is a service that owns meaningful business behavior.

For example, an Order Service should own order-specific rules:

```mermaid
flowchart TD
    OrderService[Order Service]

    Create[Create order]
    Confirm[Confirm order]
    Cancel[Cancel order]
    State[Validate order state transitions]
    Events[Publish order events]
    DB[(Orders DB)]

    OrderService --> Create
    OrderService --> Confirm
    OrderService --> Cancel
    OrderService --> State
    OrderService --> Events
    OrderService --> DB
```

The Order Service should decide whether an order can be cancelled.

Example:

```ts
type OrderStatus =
  | "PENDING_PAYMENT"
  | "CONFIRMED"
  | "SHIPPED"
  | "CANCELLED";

type Order = {
  id: string;
  status: OrderStatus;
};

function cancelOrder(order: Order): Order {
  if (order.status === "SHIPPED") {
    throw new Error("Cannot cancel an order that has already shipped");
  }

  if (order.status === "CANCELLED") {
    return order;
  }

  return {
    ...order,
    status: "CANCELLED"
  };
}
```

This rule belongs in the Order Service because it is part of the order domain.

It should not be hidden in:

* an API gateway,
* a message broker,
* a service mesh,
* an enterprise service bus,
* a shared integration script,
* a database trigger owned by another team.

---

#### Dumb pipes

A **dumb pipe** is communication infrastructure that moves messages without owning domain meaning.

Examples include:

* HTTP,
* REST,
* gRPC,
* message brokers,
* event buses,
* queues,
* pub/sub systems,
* API gateways,
* service meshes,
* reverse proxies,
* load balancers.

“Dumb” does not mean primitive or unreliable. A good pipe can still provide important technical capabilities.

For example, a message broker can provide:

* durable message storage,
* topic routing,
* consumer groups,
* retries,
* dead-letter queues,
* ordering guarantees,
* delivery acknowledgments,
* access control,
* metrics.

```mermaid
flowchart TD
    Producer[Producer Service]
    Broker[(Message Broker)]

    Topic[Topic or Queue]
    DLQ[Dead Letter Queue]
    Consumer[Consumer Service]

    Producer --> Broker
    Broker --> Topic
    Topic --> Consumer
    Topic --> DLQ
```

That is still a dumb pipe if it is not making business decisions.

The broker can decide:

> Which subscribers should receive this event?

But it should not decide:

> Is this customer eligible for a premium discount?

That business decision belongs in a service.

---

#### Example: good event-driven design

Suppose an Order Service publishes an event when an order is created.

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt_123",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "orderId": "ord_456",
    "customerId": "cus_789",
    "totalAmount": 129.99,
    "currency": "USD"
  }
}
```

The event broker routes the event to interested services:

```mermaid
flowchart TD
    Orders[Order Service]
    Broker[(Event Broker)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Notifications[Notification Service]
    Analytics[Analytics Service]

    Orders -->|OrderCreated| Broker

    Broker --> Payments
    Broker --> Inventory
    Broker --> Notifications
    Broker --> Analytics
```

Each service owns its reaction.

Payment Service decides whether and how to authorize payment:

```ts
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  const paymentDecision = await paymentPolicy.evaluate({
    customerId: event.data.customerId,
    orderId: event.data.orderId,
    amount: event.data.totalAmount,
    currency: event.data.currency
  });

  if (paymentDecision.requiresManualReview) {
    await paymentRepository.createPendingReview(event.data.orderId);
    return;
  }

  await paymentGateway.authorize({
    orderId: event.data.orderId,
    amount: event.data.totalAmount,
    currency: event.data.currency
  });
}
```

Inventory Service decides whether inventory can be reserved:

```ts
async function handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
  const reservation = await inventoryService.reserveItems({
    orderId: event.data.orderId,
    items: event.data.items
  });

  await eventBus.publish("InventoryReserved", {
    orderId: event.data.orderId,
    reservationId: reservation.id
  });
}
```

The broker does not know payment policy or inventory policy. It only delivers the event.

---

#### Example: bad event-driven design

A bad design puts business rules inside the broker or integration layer.

```mermaid
flowchart TD
    Orders[Order Service]
    SmartBroker[Smart Broker<br/>if amount > 1000, route to fraud<br/>if customer is VIP, skip review<br/>if stock is low, change priority]

    Payments[Payment Service]
    Fraud[Fraud Service]
    Inventory[Inventory Service]

    Orders --> SmartBroker
    SmartBroker --> Payments
    SmartBroker --> Fraud
    SmartBroker --> Inventory
```

This is risky because the broker now owns business meaning.

The routing rules may look harmless at first:

```yaml
routes:
  - when: order.totalAmount > 1000
    sendTo: fraud-service

  - when: customer.tier == "VIP"
    sendTo: priority-fulfillment

  - when: inventory.stockLevel < 10
    sendTo: replenishment-service
```

But these are not just routing rules. They are business rules.

Questions become difficult to answer:

* Who owns the VIP fulfillment rule?
* Who tests it?
* Who deploys changes to it?
* Does the business know the rule lives in gateway or broker config?
* Does the Order Service know this affects the order lifecycle?
* Does the Fraud Team own the fraud routing criteria?
* What happens when the rule conflicts with service logic?

This is how integration infrastructure becomes a hidden monolith.

---

#### API gateway example

An API Gateway is a common place where this principle matters.

A good gateway handles edge concerns:

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]

    Auth[Authentication]
    RateLimit[Rate Limiting]
    Routing[Routing]
    Logging[Logging]

    Services[Domain Services]

    Client --> Gateway

    Gateway --> Auth
    Auth --> RateLimit
    RateLimit --> Routing
    Routing --> Services
    Routing --> Logging
```

Good gateway responsibilities:

* verify token,
* apply rate limits,
* terminate TLS,
* route requests,
* add request IDs,
* enforce request-size limits,
* handle CORS,
* collect access logs.

Bad gateway responsibilities:

* calculate order total,
* decide refund eligibility,
* approve loan applications,
* determine shipment rerouting rules,
* manage inventory reservations,
* orchestrate complex business workflows,
* apply pricing rules.

For example, this is good:

```ts
function routeRequest(req: Request): RouteTarget {
  if (req.path.startsWith("/api/orders")) {
    return {
      service: "order-service"
    };
  }

  if (req.path.startsWith("/api/payments")) {
    return {
      service: "payment-service"
    };
  }

  throw new Error("No route found");
}
```

This is risky:

```ts
function canCancelOrder(req: Request): boolean {
  return (
    req.body.orderStatus !== "SHIPPED" &&
    req.body.customerTier === "PREMIUM" &&
    req.body.refundAmount < 500
  );
}
```

That cancellation decision belongs in the Order Service or a domain service, not the gateway.

---

#### Message broker example

A message broker should deliver messages and provide infrastructure-level guarantees.

Good broker responsibilities:

* persist messages,
* deliver to subscribers,
* manage consumer groups,
* retry failed delivery,
* send poison messages to a dead-letter queue,
* enforce topic permissions,
* expose lag metrics.

```mermaid
flowchart TD
    Producer[Producer]
    Topic[(Topic)]
    ConsumerA[Consumer A]
    ConsumerB[Consumer B]
    DLQ[(Dead Letter Queue)]

    Producer --> Topic
    Topic --> ConsumerA
    Topic --> ConsumerB
    Topic --> DLQ
```

Risky broker responsibilities:

* deciding customer eligibility,
* modifying order state,
* enriching events with domain data,
* applying pricing rules,
* filtering business events based on domain-specific policies,
* coordinating multi-step business processes.

A broker may filter by topic or event type:

```text
OrderCreated -> order-events topic
PaymentAuthorized -> payment-events topic
```

But be cautious with domain-specific filters:

```text
Only route OrderCreated to Fulfillment if customer is VIP and order margin > 20%
```

That likely belongs in a fulfillment, pricing, or order workflow service.

---

#### Service mesh example

A service mesh can provide powerful infrastructure behavior for service-to-service communication.

Good service mesh responsibilities:

* mTLS,
* traffic routing,
* retries,
* timeouts,
* circuit breaking,
* observability,
* service identity,
* policy enforcement.

```mermaid
flowchart TD
    ServiceA[Service A]
    ProxyA[Sidecar Proxy]

    Mesh[Service Mesh]

    ProxyB[Sidecar Proxy]
    ServiceB[Service B]

    ServiceA --> ProxyA
    ProxyA --> Mesh
    Mesh --> ProxyB
    ProxyB --> ServiceB
```

Bad service mesh responsibilities:

* deciding order workflows,
* applying customer segmentation rules,
* calculating discounts,
* selecting payment strategies based on business policy,
* enforcing domain state transitions.

A service mesh can decide:

> Route 5% of traffic to version 2.

It should not decide:

> Premium customers should bypass fraud checks unless the order contains restricted items.

The first is traffic management. The second is business logic.

---

#### Integration layer example

An integration layer is sometimes needed to connect systems.

For example, it may connect an e-commerce platform to an ERP.

```mermaid
flowchart TD
    Ecommerce[Commerce Services]
    Integration[Integration Layer]
    ERP[ERP System]

    Ecommerce --> Integration
    Integration --> ERP
```

The integration layer may translate protocols and formats:

```mermaid
flowchart TD
    OrderService[Order Service]
    Adapter[ERP Adapter]

    Json[JSON Order Event]
    Soap[SOAP ERP Request]

    ERP[ERP System]

    OrderService --> Json
    Json --> Adapter
    Adapter --> Soap
    Soap --> ERP
```

That is acceptable.

But if the integration layer starts owning core order, pricing, fulfillment, or accounting decisions, it becomes too smart.

A healthy integration layer translates:

```ts
function toErpSalesOrder(order: OrderConfirmedEvent): ErpSalesOrderRequest {
  return {
    salesOrderNumber: order.orderId,
    customerNumber: order.customerId,
    orderDate: order.confirmedAt,
    lines: order.items.map((item) => ({
      sku: item.sku,
      quantity: item.quantity,
      unitPrice: item.unitPrice
    }))
  };
}
```

A risky integration layer decides business policy:

```ts
function shouldSendToErp(order: Order): boolean {
  return order.margin > 0.2 && order.customerTier !== "TRIAL";
}
```

That rule may belong in Order Service, Billing, Finance, or a dedicated fulfillment policy service.

---

#### Smart endpoints and domain ownership

Smart endpoints work because each service owns a bounded business responsibility.

For example:

| Service           | Owns                                                    |
| ----------------- | ------------------------------------------------------- |
| Order Service     | Order lifecycle, order state transitions, order history |
| Payment Service   | Authorization, capture, refunds, payment state          |
| Inventory Service | Stock levels, reservations, availability                |
| Shipping Service  | Shipment creation, carrier integration, tracking        |
| Pricing Service   | Price calculation, discounts, promotions                |
| Customer Service  | Customer profile and preferences                        |

Each service should expose APIs or events that reflect its ownership.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]
    PricingService[Pricing Service]

    OrderService --> OrderAPI[Order API]
    PaymentService --> PaymentAPI[Payment API]
    InventoryService --> InventoryAPI[Inventory API]
    PricingService --> PricingAPI[Pricing API]
```

When another service needs a decision, it should ask the service that owns that decision.

For example, the Checkout Service should not calculate price if Pricing Service owns pricing. It should ask Pricing Service.

```mermaid
sequenceDiagram
    participant Checkout as Checkout Service
    participant Pricing as Pricing Service

    Checkout->>Pricing: Calculate price for cart
    Pricing-->>Checkout: Price quote
```

The pipe between them should not calculate the price.

---

#### Dumb pipes can still be reliable

“Dumb pipes” does not mean the infrastructure should be weak.

A dumb pipe can still be highly engineered.

For example, a message broker may provide:

```mermaid
flowchart TD
    Broker[Message Broker]

    Durability[Durable storage]
    Retry[Retry delivery]
    DLQ[Dead-letter queue]
    Ordering[Ordering guarantees]
    Metrics[Consumer lag metrics]
    Security[Topic permissions]

    Broker --> Durability
    Broker --> Retry
    Broker --> DLQ
    Broker --> Ordering
    Broker --> Metrics
    Broker --> Security
```

These are infrastructure responsibilities.

The distinction is not about sophistication. It is about ownership of business meaning.

Infrastructure should know how to deliver messages. It should not need to understand what those messages mean in business terms.

---

#### Choreography and dumb pipes

This principle fits naturally with event choreography.

In choreography, services publish events and react to events.

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Notifications[Notification Service]

    Orders -->|OrderCreated| Bus

    Bus --> Payments
    Bus --> Inventory
    Bus --> Notifications
```

The event bus does not coordinate the business process. Each service decides how to react.

Payment Service reacts to `OrderCreated` by starting payment authorization.

Inventory Service reacts by reserving stock.

Notification Service reacts by sending confirmation messages.

This keeps business logic distributed to the owning services.

However, choreography can become hard to understand if the workflow is not documented. Smart endpoints do not remove the need for observability and process visibility.

---

#### Orchestration and smart endpoints

Smart Endpoints, Dumb Pipes does not forbid orchestration.

Some workflows need an orchestrator.

For example, checkout may be coordinated by a Checkout Service:

```mermaid
flowchart TD
    Checkout[Checkout Service<br/>workflow coordination]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    Checkout --> Orders
    Checkout --> Payments
    Checkout --> Inventory
    Checkout --> Shipping
```

This can still follow the principle if the orchestrator is a service with clear business ownership, not generic middleware.

A good orchestrator coordinates:

```ts
async function checkout(command: CheckoutCommand): Promise<void> {
  const order = await orders.createPendingOrder(command);
  const payment = await payments.authorize(order.paymentRequest);
  const reservation = await inventory.reserve(order.items);

  await orders.confirm(order.id, {
    paymentId: payment.id,
    reservationId: reservation.id
  });
}
```

But the orchestrator should not steal domain rules from other services.

For example:

* Payment Service decides whether authorization succeeds.
* Inventory Service decides whether stock can be reserved.
* Order Service decides whether the order can be confirmed.

The Checkout Service coordinates the workflow. It does not own every domain rule.

---

#### Business logic vs technical policy

A common difficulty is deciding whether something is business logic or technical policy.

Use this distinction:

| Concern                                               | Usually belongs in                 |
| ----------------------------------------------------- | ---------------------------------- |
| Is the token valid?                                   | Gateway or identity infrastructure |
| Can this user cancel this order?                      | Order Service                      |
| Is request size under 1 MB?                           | Gateway                            |
| Is this payment refundable?                           | Payment Service                    |
| Should this route use canary version?                 | Gateway or service mesh            |
| Is this customer eligible for a discount?             | Pricing or Promotion Service       |
| Should this failed message go to a dead-letter queue? | Broker                             |
| Should this order be sent for manual fraud review?    | Fraud or Risk Service              |
| Should this API key be rate-limited?                  | Gateway                            |
| Can this inventory reservation be created?            | Inventory Service                  |

A useful test:

> Would a product manager, domain expert, or business policy owner care about this rule?

If yes, it probably belongs in a service, not generic infrastructure.

---

#### Example: fraud review

Consider this rule:

> Orders over $1,000 from new customers should be reviewed for fraud.

Bad placement:

```mermaid
flowchart TD
    OrderService[Order Service]
    Broker[Message Broker<br/>if amount > 1000 and customer age < 30 days<br/>route to fraud review]

    Fraud[Fraud Service]
    Payments[Payment Service]

    OrderService --> Broker
    Broker --> Fraud
    Broker --> Payments
```

The broker now owns fraud policy.

Better placement:

```mermaid
flowchart TD
    OrderService[Order Service]
    Broker[(Event Broker)]

    Fraud[Fraud Service<br/>owns fraud policy]
    Payments[Payment Service]

    OrderService -->|OrderCreated| Broker

    Broker --> Fraud
    Broker --> Payments
```

Fraud Service evaluates the rule:

```ts
function requiresFraudReview(order: OrderRiskInput): boolean {
  return order.totalAmount > 1000 && order.customerAgeDays < 30;
}
```

Now fraud policy is owned by the Fraud Service.

If the rule changes, the Fraud Team changes its service. The broker remains generic.

---

#### Example: routing vs business decision

Gateway routing can be technical or business-specific.

Technical routing:

```yaml
routes:
  - pathPrefix: /api/orders
    target: order-service

  - pathPrefix: /api/payments
    target: payment-service
```

This is fine. It maps API routes to services.

Canary routing:

```yaml
routes:
  - pathPrefix: /api/orders
    target:
      stable: order-service-v1
      canary: order-service-v2
      canaryPercent: 5
```

This is also fine. It is deployment policy.

Business routing:

```yaml
routes:
  - when: customer.lifetimeValue > 10000
    target: premium-fulfillment-service

  - when: order.profitMargin < 0.05
    target: low-margin-review-service
```

This is suspicious. These rules use business meaning and likely belong in domain services.

---

#### Example: transformation vs corruption

Some transformation in pipes is acceptable.

For example, a gateway may rewrite a public path to an internal path:

```text
Public:
GET /api/v1/orders/ord_123

Internal:
GET /orders/ord_123
```

That is technical transformation.

An event broker may wrap messages with metadata:

```json
{
  "messageId": "msg_123",
  "topic": "order-events",
  "payload": {
    "eventType": "OrderCreated",
    "orderId": "ord_456"
  }
}
```

That is technical envelope handling.

But this is domain transformation:

```json
{
  "eventType": "PriorityOrderCreated",
  "priority": "HIGH",
  "reason": "Customer is VIP and order total is above threshold"
}
```

If the pipe decides that priority, it is no longer dumb. A domain service should assign business priority.

A useful boundary:

| Transformation type             | Usually okay in pipe? |
| ------------------------------- | --------------------- |
| Path rewrite                    | Yes                   |
| Protocol conversion             | Usually               |
| Header normalization            | Yes                   |
| Message envelope                | Yes                   |
| Schema validation               | Usually               |
| Status code normalization       | Sometimes             |
| Mapping legacy business meaning | Usually better in ACL |
| Calculating business priority   | No                    |
| Applying pricing logic          | No                    |
| Deciding workflow path          | Usually no            |

---

#### Implementation guidance

A good implementation keeps infrastructure configuration declarative and technical.

Example gateway configuration:

```yaml
routes:
  - name: orders
    pathPrefix: /api/orders
    target: order-service
    policies:
      authRequired: true
      rateLimit:
        requestsPerMinute: 500
      timeoutMs: 2000

  - name: catalog
    pathPrefix: /api/catalog
    target: catalog-service
    policies:
      authRequired: false
      cache:
        ttlSeconds: 60
      timeoutMs: 1000
```

This is mostly technical policy.

Example message broker configuration:

```yaml
topics:
  - name: order-events
    retentionDays: 7
    partitions: 12
    allowedProducers:
      - order-service
    allowedConsumers:
      - payment-service
      - inventory-service
      - analytics-service

  - name: payment-events
    retentionDays: 30
    partitions: 8
    allowedProducers:
      - payment-service
    allowedConsumers:
      - order-service
      - accounting-service
```

This is infrastructure ownership.

Business rules remain in service code:

```ts
class PaymentService {
  async authorizePayment(command: AuthorizePaymentCommand): Promise<PaymentAuthorization> {
    const risk = await this.riskPolicy.evaluate(command);

    if (risk.decision === "REJECT") {
      return this.rejectPayment(command, risk.reason);
    }

    if (risk.decision === "REVIEW") {
      return this.markPaymentForReview(command, risk.reason);
    }

    return this.paymentGateway.authorize(command);
  }
}
```

The service owns the decision.

---

#### Shared rules without smart pipes

One trade-off of this principle is that some rules may seem shared across services.

For example:

* tenant access rules,
* data classification rules,
* customer eligibility rules,
* currency formatting,
* validation logic,
* compliance policies.

The wrong solution is to put all shared rules into the gateway, broker, or service bus.

Better options include:

1. **Create a domain service that owns the shared decision**

For example, an Entitlements Service:

```mermaid
flowchart TD
    ServiceA[Service A]
    ServiceB[Service B]
    Entitlements[Entitlements Service<br/>owns entitlement decisions]

    ServiceA --> Entitlements
    ServiceB --> Entitlements
```

2. **Use a shared library only for stable technical utilities**

For example, date parsing, trace propagation, or standard error types.

3. **Use a policy service for cross-cutting authorization**

For example, a centralized authorization service may evaluate access policies, while domain services still enforce resource-specific checks.

4. **Use contracts and schemas**

Keep message formats consistent without putting business behavior in the pipe.

5. **Use platform middleware for technical concerns**

Authentication, rate limiting, and observability can be centralized without moving domain rules.

The goal is not to duplicate everything. The goal is to avoid hiding business behavior in infrastructure.

---

#### When to use it

Use Smart Endpoints, Dumb Pipes when designing:

* microservice communication,
* event-driven systems,
* message brokers,
* API gateways,
* service meshes,
* integration platforms,
* workflow systems,
* legacy migration layers,
* internal platform infrastructure.

It is especially important when multiple teams share the same infrastructure layer. Without this principle, the shared layer can become a bottleneck where every business change must be coordinated.

Use this principle when you want:

* clear domain ownership,
* independently deployable services,
* simple infrastructure contracts,
* decentralized business logic,
* less middleware coupling,
* fewer hidden dependencies.

---

#### When not to apply it blindly

This principle should not be interpreted as:

> Infrastructure must be useless.

A pipe can and should provide strong technical capabilities.

It is reasonable for infrastructure to handle:

* delivery guarantees,
* retries,
* timeouts,
* circuit breaking,
* authentication,
* encryption,
* schema validation,
* observability,
* routing,
* rate limiting,
* dead-letter queues.

It may also be appropriate to use a workflow engine for long-running business processes, as long as the workflow ownership is explicit and domain rules are not hidden in generic middleware.

For example, a dedicated Claims Workflow Service using a workflow engine can still be valid:

```mermaid
flowchart TD
    ClaimsWorkflow[Claims Workflow Service]
    WorkflowEngine[Workflow Engine]

    Policy[Policy Service]
    Fraud[Fraud Service]
    Payments[Payment Service]

    ClaimsWorkflow --> WorkflowEngine
    ClaimsWorkflow --> Policy
    ClaimsWorkflow --> Fraud
    ClaimsWorkflow --> Payments
```

The key is ownership. If the Claims team owns the workflow service and the workflow represents claims domain behavior, that can be acceptable.

The danger is a generic enterprise workflow layer that quietly absorbs business logic from every domain.

---

#### Benefits

**1. Keeps business ownership inside services**

The service responsible for a domain owns that domain’s rules.

**2. Avoids hidden monoliths**

Gateways, brokers, service buses, and meshes do not become centralized business applications.

**3. Improves service autonomy**

Teams can change business behavior in their own services without changing shared middleware.

**4. Makes behavior easier to find**

Order rules live in Order Service. Payment rules live in Payment Service. Inventory rules live in Inventory Service.

**5. Simplifies infrastructure**

Communication layers are easier to operate when they do not contain domain-specific rules.

**6. Improves testability**

Business behavior can be tested in the owning service instead of requiring complex middleware integration tests.

**7. Reduces organizational bottlenecks**

Teams do not need a central integration team for every business rule change.

---

#### Trade-offs

**1. Services become more responsible**

Smart endpoints require teams to own more logic, testing, and operational behavior.

**2. Some rules may be duplicated if ownership is unclear**

Teams must avoid copying the same business rule into multiple services.

**3. Coordination still exists**

Services still need contracts, schemas, observability, and integration testing.

**4. Workflows can be harder to see**

If services react independently to events, the overall process may be less obvious.

**5. Shared policy decisions need careful ownership**

Cross-cutting policies may need dedicated services or libraries.

**6. Infrastructure cannot hide poor service boundaries**

If services are poorly decomposed, simple pipes will not fix the architecture.

---

#### Common mistakes

**Mistake 1: Putting business rules in the gateway**

The gateway should not calculate prices, approve refunds, or decide order transitions.

**Mistake 2: Making the message broker a rules engine**

A broker should route and deliver messages, not own domain decisions.

**Mistake 3: Treating “dumb pipes” as unreliable pipes**

Infrastructure should still be robust, observable, secure, and scalable.

**Mistake 4: Duplicating shared business rules everywhere**

If many services need the same business decision, create a clear owner for that decision.

**Mistake 5: Hiding workflows in event subscriptions**

Event choreography needs documentation, tracing, and operational visibility.

**Mistake 6: Letting an integration layer become the real system**

If most business behavior is in the integration layer, services are no longer autonomous.

**Mistake 7: Confusing technical routing with business routing**

Routing by path or version is technical. Routing by customer value, margin, eligibility, or risk is usually business logic.

---

#### Practical design checklist

When designing communication infrastructure, ask:

* Is this rule technical or business-specific?
* Which service owns the business concept involved?
* Would a domain expert care about this rule?
* Is the gateway only routing and enforcing edge policy?
* Is the broker only delivering messages and managing infrastructure concerns?
* Is the service mesh only managing traffic and security?
* Are business decisions testable inside the owning service?
* Are event contracts clear?
* Are workflows observable?
* Is routing configuration free of hidden business rules?
* Is transformation limited to protocol, envelope, or compatibility concerns?
* Does any shared middleware need frequent business-driven changes?
* If middleware disappeared, would the service still own its domain behavior?
* Is there a clear owner for shared decisions?
* Are teams using infrastructure to avoid fixing service boundaries?

A design is probably healthy if:

* services own business decisions,
* infrastructure owns technical delivery concerns,
* gateway rules are mostly edge policies,
* broker rules are mostly delivery policies,
* domain behavior is easy to find,
* shared business decisions have explicit service ownership,
* communication contracts are simple and documented.

A design is probably unhealthy if:

* business rules live in gateway configuration,
* the broker has domain-specific routing rules,
* service bus changes are required for most product changes,
* no one knows where a business decision is implemented,
* infrastructure teams become blockers for domain changes,
* services mostly forward messages while middleware does the real work.

---

#### Related patterns

| Pattern                          | Relationship                                                        |
| -------------------------------- | ------------------------------------------------------------------- |
| API Gateway                      | Gateway should handle edge concerns, not domain logic               |
| Gateway Routing                  | Routing should remain technical, not become business policy         |
| Gateway Offloading               | Offload technical concerns, not business decisions                  |
| Event-Driven Architecture        | Events should be delivered by pipes and interpreted by services     |
| Choreography                     | Services react to events; the broker stays simple                   |
| Saga                             | Workflow coordination may live in a service, not generic middleware |
| Decompose by Business Capability | Helps decide which endpoint owns which business rules               |
| Decompose by Subdomain           | Bounded contexts should own their own models and decisions          |
| Anti-Corruption Layer            | Translation belongs at boundaries, not hidden inside generic pipes  |
| Service Mesh                     | Mesh handles traffic policy, not domain behavior                    |
| Consumer-Driven Contracts        | Keeps service communication explicit and testable                   |

---

#### Summary

Smart Endpoints, Dumb Pipes means that business logic belongs in services, while communication infrastructure should remain simple, generic, and technical.

The central idea is:

> Let services make business decisions. Let pipes move messages.

A healthy implementation keeps:

* order rules in Order Service,
* payment rules in Payment Service,
* inventory rules in Inventory Service,
* pricing rules in Pricing Service,
* routing, delivery, retries, TLS, rate limits, and observability in infrastructure.

This prevents gateways, brokers, service buses, service meshes, and integration layers from becoming hidden monoliths.

The trade-off is that services must be genuinely capable. They need clear ownership, good contracts, strong tests, and reliable operations. But that is the point of microservices: business capabilities should be owned by services, not by the pipes between them.


---

### 15. Chained Microservice Pattern

#### What it is

The **Chained Microservice Pattern** is a communication pattern where a request flows synchronously through a sequence of services.

One service receives a request, calls another service, that service calls another service, and so on until the workflow completes.

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
```

A simple example:

```mermaid
sequenceDiagram
    participant Client
    participant Checkout as Checkout Service
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service

    Client->>Checkout: Submit checkout
    Checkout->>Orders: Create order
    Orders->>Payments: Authorize payment
    Payments->>Inventory: Reserve inventory
    Inventory-->>Payments: Inventory reserved
    Payments-->>Orders: Payment authorized
    Orders-->>Checkout: Order created
    Checkout-->>Client: Checkout complete
```

The defining feature is that each step waits for the next step to finish before returning.

The central idea is:

> A request is handled by a synchronous chain of service calls, where each service depends on the next service’s response.

This pattern is easy to understand, but it becomes risky when the chain grows long or includes unreliable dependencies.

---

#### Why this pattern exists

Not every workflow needs messaging, sagas, event sourcing, or orchestration.

Some workflows are naturally short and sequential.

For example:

1. API Service receives a request.
2. Customer Service validates the customer.
3. Pricing Service calculates the price.
4. Order Service creates the order.
5. API Service returns the result.

```mermaid
flowchart TD
    Start[Request received]
    Validate[Validate customer]
    Price[Calculate price]
    Create[Create order]
    Return[Return response]

    Start --> Validate
    Validate --> Price
    Price --> Create
    Create --> Return
```

If the workflow is short, low-risk, and requires immediate response, synchronous chaining can be reasonable.

The pattern exists because direct calls are simple:

* the control flow is easy to follow,
* the client receives a response immediately,
* failures are easy to return as errors,
* no message broker is required,
* no eventual consistency model is needed for simple cases.

But that simplicity has limits.

---

#### What it solves

The Chained Microservice Pattern solves the need for **simple sequential coordination**.

It is useful when one step really does need the result of the previous step.

For example:

```mermaid
flowchart TD
    Request[Create order request]

    Customer[Customer Service<br/>validate customer]
    Pricing[Pricing Service<br/>calculate price]
    Orders[Order Service<br/>create order]

    Request --> Customer
    Customer --> Pricing
    Pricing --> Orders
```

The Order Service may need the customer validation result and pricing result before it can create the order.

In this kind of workflow, chaining can be easier than introducing asynchronous messaging.

However, the important limitation is that every service in the chain becomes part of the request’s critical path.

If one service is slow, the whole request is slow.

If one service fails, the whole request may fail.

---

#### Basic structure

A chained request usually has this structure:

```mermaid
sequenceDiagram
    participant Client
    participant A as Service A
    participant B as Service B
    participant C as Service C

    Client->>A: Request
    A->>B: Request
    B->>C: Request
    C-->>B: Response
    B-->>A: Response
    A-->>Client: Response
```

Service A cannot respond to the client until Service B responds.

Service B cannot respond to Service A until Service C responds.

This means total latency accumulates.

If each service takes 100 ms, a three-service chain may take roughly 300 ms, plus network overhead.

```text
Total latency ≈ Service A work + Service B call + Service C call + network overhead
```

For short chains, this can be acceptable. For long chains, it becomes a performance and reliability problem.

---

#### Example: customer lookup and order creation

Suppose an API endpoint creates an order.

The request must:

1. Validate that the customer exists.
2. Calculate the current price.
3. Create the order.

```mermaid
sequenceDiagram
    participant Client
    participant API as API Service
    participant Customers as Customer Service
    participant Pricing as Pricing Service
    participant Orders as Order Service

    Client->>API: POST /orders
    API->>Customers: GET /customers/cus_123
    Customers-->>API: Customer is active

    API->>Pricing: POST /price-quotes
    Pricing-->>API: Price quote

    API->>Orders: POST /orders
    Orders-->>API: Order created

    API-->>Client: 201 Created
```

This is a reasonable use of synchronous calls if:

* the services are reliable,
* the workflow is short,
* the client needs an immediate result,
* all dependencies are low-latency,
* failures can be returned directly to the client.

Example implementation:

```ts
import express, { Request, Response } from "express";

const app = express();
app.use(express.json());

type CreateOrderRequest = {
  customerId: string;
  items: Array<{
    productId: string;
    quantity: number;
  }>;
};

async function getCustomer(customerId: string) {
  const response = await fetch(`http://customer-service/customers/${customerId}`);

  if (response.status === 404) {
    throw new Error("CUSTOMER_NOT_FOUND");
  }

  if (!response.ok) {
    throw new Error("CUSTOMER_SERVICE_UNAVAILABLE");
  }

  return response.json();
}

async function createPriceQuote(request: CreateOrderRequest) {
  const response = await fetch("http://pricing-service/price-quotes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      customerId: request.customerId,
      items: request.items
    })
  });

  if (!response.ok) {
    throw new Error("PRICING_FAILED");
  }

  return response.json();
}

async function createOrder(request: CreateOrderRequest, priceQuoteId: string) {
  const response = await fetch("http://order-service/orders", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      customerId: request.customerId,
      items: request.items,
      priceQuoteId
    })
  });

  if (!response.ok) {
    throw new Error("ORDER_CREATION_FAILED");
  }

  return response.json();
}

app.post("/orders", async (req: Request, res: Response) => {
  try {
    const command = req.body as CreateOrderRequest;

    const customer = await getCustomer(command.customerId);

    if (customer.status !== "ACTIVE") {
      res.status(400).json({
        error: "CUSTOMER_NOT_ACTIVE"
      });
      return;
    }

    const quote = await createPriceQuote(command);
    const order = await createOrder(command, quote.priceQuoteId);

    res.status(201).json(order);
  } catch (error) {
    res.status(500).json({
      error: error instanceof Error ? error.message : "UNKNOWN_ERROR"
    });
  }
});

app.listen(3000);
```

This implementation is simple, but it has an important weakness: every downstream service must respond successfully for the endpoint to succeed.

---

#### Latency accumulation

Latency compounds in a chain.

Suppose a request goes through four services:

```mermaid
flowchart TD
    Client[Client]
    A[Service A<br/>80 ms]
    B[Service B<br/>120 ms]
    C[Service C<br/>150 ms]
    D[Service D<br/>100 ms]

    Client --> A
    A --> B
    B --> C
    C --> D
```

The total latency may be approximately:

```text
80 ms + 120 ms + 150 ms + 100 ms = 450 ms
```

That does not include network overhead, serialization, load balancers, retries, TLS, gateway processing, or queueing.

The longer the chain, the worse tail latency becomes.

For example, even if each service is usually fast, one slow service can slow down the entire request.

```mermaid
flowchart TD
    Request[Request]
    A[Service A<br/>50 ms]
    B[Service B<br/>60 ms]
    C[Service C<br/>2000 ms slow]
    D[Service D<br/>50 ms]
    Response[Slow response]

    Request --> A
    A --> B
    B --> C
    C --> D
    D --> Response
```

A chain is only as fast as its accumulated path.

---

#### Failure accumulation

Failure risk also compounds.

If each service has a 99.9% success rate, a chain of five services has a lower end-to-end success rate than any individual service.

```text
0.999 × 0.999 × 0.999 × 0.999 × 0.999 ≈ 0.995
```

That means a five-service chain with individually reliable services may still have only about 99.5% success end to end.

```mermaid
flowchart TD
    Client[Client]
    A[Service A<br/>99.9 percent]
    B[Service B<br/>99.9 percent]
    C[Service C<br/>99.9 percent]
    D[Service D<br/>99.9 percent]
    E[Service E<br/>99.9 percent]

    Client --> A
    A --> B
    B --> C
    C --> D
    D --> E

    Risk[End-to-end reliability is lower than each individual service]
    E --> Risk
```

The chain fails if any required dependency fails.

This is why long synchronous chains are fragile.

---

#### When chaining is reasonable

A chained design can be reasonable when the chain is short and the dependencies are reliable.

Good conditions:

* only two or three services are involved,
* all calls are low latency,
* all dependencies are within the same trust boundary,
* the workflow needs an immediate response,
* failures can be reported directly to the caller,
* no long-running business process is involved,
* no irreversible side effects happen halfway through,
* there is a clear timeout policy,
* each dependency has strong observability.

Example of a reasonable chain:

```mermaid
sequenceDiagram
    participant API as API Service
    participant Profile as Profile Service
    participant Preferences as Preferences Service

    API->>Profile: Get user profile
    Profile-->>API: Profile
    API->>Preferences: Get user preferences
    Preferences-->>API: Preferences
```

This may be acceptable for a read operation where failure can simply return an error or partial response.

---

#### When chaining becomes dangerous

Chaining becomes dangerous when the workflow is long, state-changing, or business-critical.

Warning signs:

* more than three or four synchronous service calls,
* services call services that call more services,
* the chain crosses many teams,
* the chain includes slow external dependencies,
* the chain performs irreversible side effects,
* timeout behavior is unclear,
* retries can duplicate work,
* partial completion causes inconsistent state,
* no service clearly owns the workflow,
* debugging requires following many nested calls.

A risky chain:

```mermaid
flowchart TD
    Client[Client]
    A[API Service]
    B[Order Service]
    C[Payment Service]
    D[Fraud Service]
    E[Inventory Service]
    F[Warehouse Service]
    G[Shipping Service]
    H[Notification Service]
    I[Analytics Service]

    Client --> A
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
```

This kind of chain has high latency, high failure risk, and poor debuggability.

It may be better as a saga, orchestrated workflow, or event-driven process.

---

#### Chained reads vs chained writes

Chained calls are safer for reads than for writes.

A read chain:

```mermaid
sequenceDiagram
    participant API
    participant Orders
    participant Payments
    participant Shipping

    API->>Orders: Get order
    API->>Payments: Get payment status
    API->>Shipping: Get shipment status
```

If a read dependency fails, the system can often return:

* an error,
* a partial response,
* cached data,
* a fallback,
* a degraded response.

A write chain is riskier:

```mermaid
sequenceDiagram
    participant API
    participant Orders
    participant Payments
    participant Inventory
    participant Shipping

    API->>Orders: Create order
    API->>Payments: Authorize payment
    API->>Inventory: Reserve stock
    API->>Shipping: Create shipment
```

If the chain fails after payment authorization but before inventory reservation, the system is partially complete.

That requires compensation.

```mermaid
flowchart TD
    CreateOrder[Order created]
    Payment[Payment authorized]
    InventoryFail[Inventory reservation failed]

    VoidPayment[Void payment authorization]
    CancelOrder[Cancel order]

    CreateOrder --> Payment
    Payment --> InventoryFail
    InventoryFail --> VoidPayment
    VoidPayment --> CancelOrder
```

At that point, the design is no longer just a simple chain. It is a distributed workflow and likely needs Saga-style handling.

---

#### Hidden chains

One of the most dangerous forms of this pattern is the **hidden chain**.

A service may appear to call only one dependency, but that dependency calls another dependency, which calls another dependency.

```mermaid
flowchart TD
    API[API Service]
    Orders[Order Service]
    Customers[Customer Service]
    Identity[Identity Service]
    Risk[Risk Service]
    Audit[Audit Service]

    API --> Orders
    Orders --> Customers
    Customers --> Identity
    Identity --> Risk
    Risk --> Audit
```

The API Service may only know about Order Service, but the real request path is much longer.

Hidden chains are dangerous because:

* latency surprises callers,
* failures are harder to trace,
* teams do not know their true dependencies,
* capacity planning becomes difficult,
* circular dependencies can appear,
* incident response becomes slower.

To avoid hidden chains, services should document downstream dependencies and expose telemetry showing call graphs.

---

#### Circular chains

A particularly bad failure mode is circular service dependency.

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Customers[Customer Service]

    Orders --> Payments
    Payments --> Customers
    Customers --> Orders
```

This creates tight coupling.

Problems include:

* difficult deployment ordering,
* risk of infinite call loops,
* hard-to-understand ownership,
* fragile startup behavior,
* cascading failures,
* poor testability.

Circular dependencies are usually a sign that service boundaries or workflow ownership need to be revisited.

---

#### Timeouts

Every synchronous call in a chain needs a timeout.

Without timeouts, one slow dependency can consume threads, connections, and memory until the caller also becomes unhealthy.

```mermaid
flowchart TD
    API[API Service]
    Orders[Order Service]
    Slow[Slow Dependency]

    API --> Orders
    Orders --> Slow

    Slow -->|No timeout| Hanging[Request hangs]
```

Example timeout helper:

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

Timeouts should be shorter as calls go deeper into the chain.

For example:

| Layer                             |   Timeout |
| --------------------------------- | --------: |
| Client to API Gateway             | 5 seconds |
| Gateway to API Service            | 4 seconds |
| API Service to downstream service | 2 seconds |
| Downstream service to dependency  |  1 second |

This prevents inner calls from outliving the original request.

---

#### Retries

Retries can help with transient failures, but they are dangerous in chains.

If every service retries three times, the number of attempts can multiply.

```mermaid
flowchart TD
    A[Service A<br/>3 retries]
    B[Service B<br/>3 retries]
    C[Service C<br/>3 retries]

    A --> B
    B --> C

    Risk[Retry amplification]
    C --> Risk
```

A single client request may create many downstream attempts.

Retry only when:

* the operation is idempotent,
* the failure is likely transient,
* there is a timeout,
* there is a retry budget,
* backoff and jitter are used,
* the retry does not overload the dependency.

Example:

```ts
async function retry<T>(
  operation: () => Promise<T>,
  attempts: number
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      if (attempt === attempts) {
        break;
      }

      const delayMs = Math.min(1000, 100 * attempt);
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }

  throw lastError;
}
```

Avoid retries for non-idempotent write operations unless an idempotency key is used.

---

#### Idempotency

If a chained workflow performs writes, idempotency is essential.

For example, this request may be retried:

```http
POST /orders
Idempotency-Key: create-order-req-123
```

The receiving service should store the result for that key:

```ts
async function createOrderWithIdempotency(
  command: CreateOrderCommand,
  idempotencyKey: string
): Promise<Order> {
  const existing = await idempotencyStore.find(idempotencyKey);

  if (existing) {
    return existing.response as Order;
  }

  const order = await orderRepository.create(command);

  await idempotencyStore.save({
    key: idempotencyKey,
    response: order
  });

  return order;
}
```

This prevents duplicate orders if a caller retries after a timeout.

In a chain, every state-changing service should consider idempotency.

Examples:

| Operation         | Idempotency need                          |
| ----------------- | ----------------------------------------- |
| Create order      | Prevent duplicate orders                  |
| Authorize payment | Prevent duplicate authorizations          |
| Reserve inventory | Prevent duplicate reservations            |
| Create shipment   | Prevent duplicate shipments               |
| Send notification | Prevent duplicate messages when necessary |

---

#### Circuit breakers

A circuit breaker prevents repeated calls to a failing dependency.

```mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: Too many failures
    Open --> HalfOpen: After cooldown
    HalfOpen --> Closed: Test call succeeds
    HalfOpen --> Open: Test call fails
```

In a chain, circuit breakers help prevent cascading failure.

```mermaid
flowchart TD
    API[API Service]
    Orders[Order Service]
    Payments[Payment Service<br/>failing]

    Circuit[Circuit Breaker]

    API --> Orders
    Orders --> Circuit
    Circuit --> Payments

    Circuit -->|open| FastFail[Fail fast]
```

Instead of waiting for every request to time out, the caller can fail fast or use a fallback.

Example behavior:

* Payment Service starts timing out.
* Order Service circuit breaker opens.
* Order Service stops calling Payment Service temporarily.
* Requests fail quickly or return a pending state.
* Payment Service gets time to recover.

---

#### Bulkheads

Bulkheads isolate resources so one dependency does not consume everything.

For example, if calls to Inventory Service are slow, they should not exhaust all threads or connections used by other dependencies.

```mermaid
flowchart TD
    API[API Service]

    PoolA[Connection Pool<br/>Orders]
    PoolB[Connection Pool<br/>Payments]
    PoolC[Connection Pool<br/>Inventory]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]

    API --> PoolA
    API --> PoolB
    API --> PoolC

    PoolA --> Orders
    PoolB --> Payments
    PoolC --> Inventory
```

Bulkheads are important in chains because one slow dependency can otherwise cause broad failure.

---

#### Observability

Chained calls require distributed tracing.

Without tracing, it is hard to see where time was spent or where the failure occurred.

```mermaid
flowchart TD
    Client[Client]
    Gateway[API Gateway]
    A[Service A]
    B[Service B]
    C[Service C]

    Trace[Distributed Trace]

    Client --> Gateway
    Gateway --> A
    A --> B
    B --> C

    Trace -. includes .-> Gateway
    Trace -. includes .-> A
    Trace -. includes .-> B
    Trace -. includes .-> C
```

Every service should propagate trace context.

Example headers:

```http
X-Request-Id: req_123
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00
```

Each service should log:

```json
{
  "requestId": "req_123",
  "service": "order-service",
  "operation": "createOrder",
  "downstreamService": "payment-service",
  "downstreamLatencyMs": 87,
  "status": "success"
}
```

Important metrics:

* request latency by service,
* downstream latency,
* timeout count,
* retry count,
* circuit breaker state,
* dependency error rate,
* request fan-out,
* chain depth,
* saturation of connection pools,
* tail latency such as p95 and p99.

---

#### Error handling

In a chain, errors should be translated at service boundaries.

A downstream service may return a technical error:

```json
{
  "error": "PSQL_CONNECTION_TIMEOUT"
}
```

The caller should translate this into an appropriate service-level error:

```json
{
  "error": "ORDER_CREATION_TEMPORARILY_UNAVAILABLE",
  "message": "Order creation is temporarily unavailable. Please try again."
}
```

Do not leak internal dependency errors directly to clients.

Bad response:

```json
{
  "error": "java.net.SocketTimeoutException from inventory-service:8080"
}
```

Better response:

```json
{
  "error": "INVENTORY_UNAVAILABLE",
  "message": "Inventory availability could not be confirmed."
}
```

Internally, logs should preserve detailed failure information with request IDs and trace IDs.

---

#### Chaining and ownership

A common problem with chained workflows is unclear ownership.

For example:

```mermaid
flowchart TD
    Checkout[Checkout Service]
    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]

    Checkout --> Orders
    Orders --> Payments
    Payments --> Inventory
```

Who owns the checkout workflow?

* Checkout Service?
* Order Service?
* Payment Service?
* Inventory Service?

If ownership is unclear, failures become hard to resolve.

A better design makes workflow ownership explicit.

```mermaid
flowchart TD
    Checkout[Checkout Service<br/>owns checkout coordination]

    Orders[Order Service<br/>owns order rules]
    Payments[Payment Service<br/>owns payment rules]
    Inventory[Inventory Service<br/>owns inventory rules]

    Checkout --> Orders
    Checkout --> Payments
    Checkout --> Inventory
```

The Checkout Service coordinates the workflow. Each domain service owns its own decision.

This is often better than deep nested chaining.

---

#### Chain vs orchestration

A deep chain hides the workflow inside nested service calls.

```mermaid
flowchart TD
    A[Service A]
    B[Service B]
    C[Service C]
    D[Service D]

    A --> B
    B --> C
    C --> D
```

An orchestrator makes the workflow explicit.

```mermaid
flowchart TD
    Orchestrator[Workflow Orchestrator]

    A[Service A]
    B[Service B]
    C[Service C]
    D[Service D]

    Orchestrator --> A
    Orchestrator --> B
    Orchestrator --> C
    Orchestrator --> D
```

Comparison:

| Concern             | Chained calls                        | Orchestration                     |
| ------------------- | ------------------------------------ | --------------------------------- |
| Workflow visibility | Hidden across services               | Visible in orchestrator           |
| Service coupling    | Each service depends on next service | Orchestrator depends on services  |
| Failure handling    | Spread across chain                  | Centralized in workflow           |
| Best for            | Short simple sequences               | Longer business workflows         |
| Risk                | Deep dependency chain                | Orchestrator becomes too powerful |

For anything beyond a simple chain, orchestration is often clearer.

---

#### Chain vs event-driven flow

A chain is synchronous. Each service waits.

```mermaid
flowchart TD
    A[Service A]
    B[Service B]
    C[Service C]

    A --> B
    B --> C
```

An event-driven flow is asynchronous. Services publish and react.

```mermaid
flowchart TD
    A[Service A]
    Bus[(Event Bus)]

    B[Service B]
    C[Service C]

    A -->|Event| Bus
    Bus --> B
    Bus --> C
```

Comparison:

| Concern          | Chained microservices            | Event-driven flow                  |
| ---------------- | -------------------------------- | ---------------------------------- |
| Response style   | Immediate response               | Eventually consistent              |
| Coupling         | Direct service dependencies      | Event contract dependencies        |
| Latency          | Accumulates through chain        | Caller may return earlier          |
| Failure handling | Synchronous errors               | Retries, DLQs, compensations       |
| Best for         | Short request/response workflows | Long-running or reactive workflows |

If the client does not need all work completed immediately, async messaging may be better.

---

#### Example: replacing a long chain

Suppose order placement currently does this:

```mermaid
sequenceDiagram
    participant Client
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service
    participant Shipping as Shipping Service
    participant Email as Email Service

    Client->>Orders: Create order
    Orders->>Payments: Authorize payment
    Payments->>Inventory: Reserve inventory
    Inventory->>Shipping: Create shipment
    Shipping->>Email: Send confirmation
    Email-->>Shipping: Sent
    Shipping-->>Inventory: Shipment created
    Inventory-->>Payments: Inventory reserved
    Payments-->>Orders: Payment authorized
    Orders-->>Client: Order created
```

This makes email sending part of the critical path, which is unnecessary.

A better design:

```mermaid
sequenceDiagram
    participant Client
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service
    participant Bus as Event Bus
    participant Shipping as Shipping Service
    participant Email as Email Service

    Client->>Orders: Create order
    Orders->>Payments: Authorize payment
    Payments-->>Orders: Payment authorized

    Orders->>Inventory: Reserve inventory
    Inventory-->>Orders: Inventory reserved

    Orders-->>Client: Order accepted

    Orders->>Bus: OrderConfirmed event
    Bus-->>Shipping: OrderConfirmed
    Bus-->>Email: OrderConfirmed
```

The critical synchronous path is shorter. Shipping and email can happen asynchronously.

---

#### When to use it

Use the Chained Microservice Pattern when:

* the workflow is short,
* each step depends on the previous step,
* the client needs an immediate result,
* dependencies are reliable and low-latency,
* the number of services is small,
* failure can be handled by returning an error,
* there are no complex compensating actions,
* the chain is easy to observe and test.

Good examples:

* API service calls Customer Service to validate a customer,
* Order Service calls Pricing Service to get a price quote,
* Profile Service calls Preferences Service for display settings,
* Search Service calls Ranking Service for a short synchronous ranking step,
* BFF calls two or three services to build a response.

---

#### When not to use it

Avoid or reconsider this pattern when:

* the chain is long,
* the workflow is business-critical,
* the workflow includes many writes,
* the workflow has irreversible side effects,
* services are owned by many teams,
* dependencies are slow or unreliable,
* external third-party services are in the critical path,
* failure requires compensation,
* the client does not need immediate completion,
* tail latency is important,
* the chain is hard to trace.

In these cases, consider:

* orchestration,
* Saga,
* asynchronous messaging,
* event choreography,
* CQRS read models,
* gateway aggregation for reads,
* background jobs.

---

#### Benefits

**1. Simple to understand**

The flow is direct and sequential.

**2. Easy to implement initially**

Synchronous HTTP or gRPC calls are familiar to most teams.

**3. Immediate response**

The client can receive success or failure in the same request.

**4. Natural for dependent steps**

If step two truly needs step one’s result, chaining can be straightforward.

**5. No broker required**

Simple chains do not require message infrastructure.

**6. Easier local reasoning for small flows**

For short workflows, the code path can be easy to follow.

---

#### Trade-offs

**1. Latency accumulates**

Each service call adds time to the total response.

**2. Failure risk compounds**

The request can fail if any required service fails.

**3. Cascading failures are more likely**

A slow or failing downstream service can affect all upstream callers.

**4. Hidden dependencies can grow**

A service may not know the full downstream chain it triggers.

**5. Harder to scale independently**

Upstream traffic can amplify downstream load.

**6. Retries can multiply**

Retries at each layer can overload dependencies.

**7. Long chains are hard to debug**

Without distributed tracing, finding the failure point is difficult.

**8. Partial writes are dangerous**

State-changing chains can leave the system partially complete.

---

#### Common mistakes

**Mistake 1: Making chains too long**

A long chain is fragile and slow.

**Mistake 2: No timeouts**

Every synchronous dependency needs a timeout.

**Mistake 3: Retrying everything**

Retries without idempotency and budgets can cause duplicate work and overload.

**Mistake 4: Putting third-party calls deep in the chain**

External services are often slower and less reliable than internal services.

**Mistake 5: Hiding business workflows in nested calls**

Important workflows should be explicit and observable.

**Mistake 6: No distributed tracing**

You cannot operate chained services safely without tracing.

**Mistake 7: Mixing many writes without compensation**

If step four fails after steps one through three committed, you need a recovery plan.

**Mistake 8: Creating circular dependencies**

Circular chains are a strong sign that boundaries need redesign.

---

#### Practical design checklist

Before using a chained service flow, ask:

* How many services are in the chain?
* Does each step truly need the previous step’s result?
* What is the expected latency of each step?
* What is the total expected latency?
* What is the p95 and p99 latency?
* What happens if each dependency fails?
* Are all calls required, or can some be optional?
* Are timeouts defined for every call?
* Are retries safe?
* Are writes idempotent?
* Is there an idempotency key?
* Are compensating actions needed?
* Is the workflow owner clear?
* Are downstream dependencies visible?
* Is distributed tracing enabled?
* Are circuit breakers needed?
* Are bulkheads needed?
* Could some steps be asynchronous?
* Would orchestration make the workflow clearer?
* Would a read model or aggregator reduce the chain?

A chained design is probably healthy if:

* it is short,
* it has clear ownership,
* every dependency is low-latency,
* every call has a timeout,
* failure behavior is simple,
* writes are idempotent,
* tracing is in place,
* no service is surprised by hidden downstream calls.

A chained design is probably unhealthy if:

* it spans many services,
* no one owns the whole flow,
* the chain includes slow external dependencies,
* failures require manual cleanup,
* retries are uncontrolled,
* tail latency is poor,
* services form circular dependencies,
* the chain is only understood by reading logs in production.

---

#### Related patterns

| Pattern                   | Relationship                                                                |
| ------------------------- | --------------------------------------------------------------------------- |
| API Gateway               | Often starts the chain by routing to the first service                      |
| Gateway Aggregation       | A read-focused alternative where one layer calls multiple services directly |
| Orchestration             | Makes multi-step workflows explicit instead of hiding them in nested calls  |
| Saga                      | Handles long-running workflows with local transactions and compensation     |
| Async Messaging           | Avoids blocking the caller for work that can happen later                   |
| Event-Driven Architecture | Lets services react asynchronously instead of chaining synchronously        |
| Circuit Breaker           | Prevents repeated calls to failing dependencies                             |
| Retry                     | Useful for transient failures, but risky without idempotency                |
| Bulkhead                  | Isolates resources for different downstream dependencies                    |
| Distributed Tracing       | Essential for understanding chained calls                                   |
| Idempotency Key           | Makes retried writes safer                                                  |

---

#### Summary

The Chained Microservice Pattern is a synchronous sequence of service calls where one service calls another, which calls another, and so on.

The central idea is:

> A short synchronous chain can be a simple way to execute dependent steps, but long chains become fragile.

This pattern works best for short, low-latency workflows with reliable dependencies and simple failure behavior.

A healthy chain has:

* few services,
* clear ownership,
* explicit timeouts,
* safe retries,
* idempotency for writes,
* distributed tracing,
* and simple failure handling.

The main risks are compounded latency, compounded failure probability, hidden dependencies, cascading failures, and partial completion. Once a chain becomes long, state-changing, or business-critical, consider orchestration, sagas, asynchronous messaging, or event-driven design instead.


---

### 16. Branch Pattern

#### What it is

The **Branch Pattern** is a microservice communication pattern where a request splits into multiple paths.

Those paths can be:

1. **Parallel branches**
   The service calls several independent services at the same time.

2. **Conditional branches**
   The service chooses one path based on request type, tenant, region, feature flag, customer segment, or business condition.

3. **Hybrid branches**
   The service chooses a path and then performs several calls in parallel within that path.

The simplest parallel branch looks like this:

```mermaid
flowchart TD
    Client[Client]
    API[API or Aggregator Service]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Client --> API

    API --> Orders
    API --> Payments
    API --> Shipping

    Orders --> API
    Payments --> API
    Shipping --> API

    API --> Client
```

A conditional branch looks like this:

```mermaid
flowchart TD
    Request[Incoming Request]
    Router[Routing or Workflow Service]

    Decision{Request Type?}

    Standard[Standard Processing]
    Enterprise[Enterprise Processing]
    Regulated[Regulated Processing]

    Request --> Router
    Router --> Decision

    Decision -->|Standard| Standard
    Decision -->|Enterprise| Enterprise
    Decision -->|Regulated| Regulated
```

The central idea is:

> A request does not always follow one straight line. It may fan out to multiple services or follow different paths depending on context.

---

#### Why this pattern exists

The Chained Microservice Pattern handles sequential workflows, where each step depends on the previous step.

But many workflows are not purely sequential.

Sometimes several calls are independent and can run at the same time.

For example, an account dashboard may need:

* profile data,
* recent orders,
* open support tickets,
* billing status,
* product recommendations.

These calls do not necessarily depend on one another.

A sequential design would be slow:

```mermaid
sequenceDiagram
    participant Client
    participant Dashboard as Dashboard Service
    participant Profile as Profile Service
    participant Orders as Order Service
    participant Billing as Billing Service
    participant Support as Support Service

    Client->>Dashboard: GET /dashboard

    Dashboard->>Profile: Get profile
    Profile-->>Dashboard: Profile

    Dashboard->>Orders: Get recent orders
    Orders-->>Dashboard: Orders

    Dashboard->>Billing: Get billing status
    Billing-->>Dashboard: Billing

    Dashboard->>Support: Get open tickets
    Support-->>Dashboard: Tickets

    Dashboard-->>Client: Dashboard response
```

A branched design can be faster because independent calls run in parallel:

```mermaid
sequenceDiagram
    participant Client
    participant Dashboard as Dashboard Service
    participant Profile as Profile Service
    participant Orders as Order Service
    participant Billing as Billing Service
    participant Support as Support Service

    Client->>Dashboard: GET /dashboard

    par Fetch profile
        Dashboard->>Profile: Get profile
        Profile-->>Dashboard: Profile
    and Fetch orders
        Dashboard->>Orders: Get recent orders
        Orders-->>Dashboard: Orders
    and Fetch billing
        Dashboard->>Billing: Get billing status
        Billing-->>Dashboard: Billing
    and Fetch support
        Dashboard->>Support: Get open tickets
        Support-->>Dashboard: Tickets
    end

    Dashboard-->>Client: Dashboard response
```

The Branch Pattern exists because not every workflow should be modeled as a long chain. When work is independent, branching can reduce latency and make the flow clearer.

---

#### What it solves

The Branch Pattern solves two related problems.

First, it solves **unnecessary sequential latency**.

If three service calls are independent, making them one after another wastes time.

```mermaid
flowchart TD
    Start[Start Request]

    A[Call Service A<br/>100 ms]
    B[Call Service B<br/>150 ms]
    C[Call Service C<br/>120 ms]

    Done[Return Response<br/>Total about 370 ms]

    Start --> A
    A --> B
    B --> C
    C --> Done
```

Parallel branching can reduce total time:

```mermaid
flowchart TD
    Start[Start Request]

    A[Call Service A<br/>100 ms]
    B[Call Service B<br/>150 ms]
    C[Call Service C<br/>120 ms]

    Join[Join Results]
    Done[Return Response<br/>Total about 150 ms plus overhead]

    Start --> A
    Start --> B
    Start --> C

    A --> Join
    B --> Join
    C --> Join

    Join --> Done
```

Second, it solves **conditional workflow variation**.

Different requests may need different processing paths.

For example:

```mermaid
flowchart TD
    Request[Checkout Request]
    Decision{Customer Type}

    Standard[Standard Checkout]
    Premium[Premium Checkout]
    Regulated[Regulated Checkout]

    Request --> Decision

    Decision -->|Standard| Standard
    Decision -->|Premium| Premium
    Decision -->|Regulated| Regulated
```

This is useful when different tenants, products, regions, or customer types need different behavior.

---

#### Branching vs chaining

A chain is linear.

```mermaid
flowchart TD
    A[Service A]
    B[Service B]
    C[Service C]
    D[Service D]

    A --> B
    B --> C
    C --> D
```

A branch splits.

```mermaid
flowchart TD
    A[Service A]

    B[Service B]
    C[Service C]
    D[Service D]

    Join[Join Results]

    A --> B
    A --> C
    A --> D

    B --> Join
    C --> Join
    D --> Join
```

Use a chain when each step depends on the previous step.

Use a branch when multiple steps can happen independently or when a decision determines which path should run.

| Question                       | Chain                                   | Branch                                         |
| ------------------------------ | --------------------------------------- | ---------------------------------------------- |
| Do steps depend on each other? | Yes                                     | Not necessarily                                |
| Can work run in parallel?      | Usually no                              | Often yes                                      |
| Is there conditional routing?  | Sometimes                               | Common                                         |
| Main risk                      | Latency and failure accumulate linearly | Partial failures and join logic become complex |
| Best for                       | Short dependent workflows               | Parallel enrichment or conditional processing  |

---

#### Parallel branching

Parallel branching is common in read-heavy workflows.

Example: a dashboard endpoint.

```mermaid
flowchart TD
    Client[Client]
    Dashboard[Dashboard Service]

    Profile[Profile Service]
    Orders[Order Service]
    Billing[Billing Service]
    Notifications[Notification Service]

    Response[Combined Dashboard Response]

    Client --> Dashboard

    Dashboard --> Profile
    Dashboard --> Orders
    Dashboard --> Billing
    Dashboard --> Notifications

    Profile --> Response
    Orders --> Response
    Billing --> Response
    Notifications --> Response

    Response --> Client
```

The dashboard service calls multiple services at once, then combines the results.

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
  "billing": {
    "status": "Current"
  },
  "notifications": {
    "unreadCount": 3
  }
}
```

This is similar to Gateway Aggregation, but the Branch Pattern is broader. It describes the branching communication shape, whether it happens in a gateway, BFF, workflow service, aggregator, or domain service.

---

#### Parallel branch implementation

Here is a simplified TypeScript example.

```ts
import express, { Request, Response } from "express";

const app = express();

async function getProfile(userId: string) {
  const response = await fetch(`http://profile-service/profiles/${userId}`);
  if (!response.ok) {
    throw new Error("PROFILE_UNAVAILABLE");
  }
  return response.json();
}

async function getRecentOrders(userId: string) {
  const response = await fetch(`http://order-service/users/${userId}/orders/recent`);
  if (!response.ok) {
    throw new Error("ORDERS_UNAVAILABLE");
  }
  return response.json();
}

async function getBillingStatus(userId: string) {
  const response = await fetch(`http://billing-service/users/${userId}/status`);
  if (!response.ok) {
    throw new Error("BILLING_UNAVAILABLE");
  }
  return response.json();
}

async function getNotifications(userId: string) {
  const response = await fetch(`http://notification-service/users/${userId}/summary`);
  if (!response.ok) {
    throw new Error("NOTIFICATIONS_UNAVAILABLE");
  }
  return response.json();
}

app.get("/dashboard", async (req: Request, res: Response) => {
  const userId = req.header("X-User-Id");

  if (!userId) {
    res.status(401).json({
      error: "UNAUTHENTICATED"
    });
    return;
  }

  try {
    const [profile, orders, billing, notifications] = await Promise.all([
      getProfile(userId),
      getRecentOrders(userId),
      getBillingStatus(userId),
      getNotifications(userId)
    ]);

    res.json({
      profile,
      recentOrders: orders,
      billing,
      notifications
    });
  } catch {
    res.status(503).json({
      error: "DASHBOARD_UNAVAILABLE",
      message: "Could not load dashboard."
    });
  }
});

app.listen(3000);
```

This version fails the whole request if any branch fails.

That may be acceptable if all data is required. But in many UI scenarios, some branches are optional.

---

#### Handling partial failures

Branches may succeed or fail independently.

For example, a product page may still be useful if recommendations fail.

```mermaid
flowchart TD
    ProductPage[Product Page Request]

    Product[Product Service]
    Pricing[Pricing Service]
    Inventory[Inventory Service]
    Reviews[Reviews Service]
    Recommendations[Recommendations Service]

    Response[Product Page Response]

    ProductPage --> Product
    ProductPage --> Pricing
    ProductPage --> Inventory
    ProductPage --> Reviews
    ProductPage -. failed .-> Recommendations

    Product --> Response
    Pricing --> Response
    Inventory --> Response
    Reviews --> Response
```

The response can include partial data and warnings:

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
  "reviews": {
    "averageRating": 4.6,
    "count": 381
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

In TypeScript, use `Promise.allSettled` when branches can fail independently.

```ts
const [
  productResult,
  priceResult,
  inventoryResult,
  reviewsResult,
  recommendationsResult
] = await Promise.allSettled([
  productClient.getProduct(productId),
  pricingClient.getPrice(productId),
  inventoryClient.getAvailability(productId),
  reviewsClient.getSummary(productId),
  recommendationsClient.getRecommendations(productId)
]);

if (productResult.status === "rejected") {
  throw new Error("PRODUCT_REQUIRED");
}

if (priceResult.status === "rejected") {
  throw new Error("PRICE_REQUIRED");
}

const warnings: Array<{ code: string; message: string }> = [];

const reviews =
  reviewsResult.status === "fulfilled"
    ? reviewsResult.value
    : null;

if (reviewsResult.status === "rejected") {
  warnings.push({
    code: "REVIEWS_UNAVAILABLE",
    message: "Reviews are temporarily unavailable."
  });
}

const recommendations =
  recommendationsResult.status === "fulfilled"
    ? recommendationsResult.value
    : [];

if (recommendationsResult.status === "rejected") {
  warnings.push({
    code: "RECOMMENDATIONS_UNAVAILABLE",
    message: "Recommendations are temporarily unavailable."
  });
}
```

A key design decision is deciding which branches are required and which are optional.

---

#### Required vs optional branches

Not all branches are equal.

For a product page:

| Branch          | Required?                                  | Failure behavior                               |
| --------------- | ------------------------------------------ | ---------------------------------------------- |
| Product details | Required                                   | Fail the page                                  |
| Price           | Usually required                           | Fail or show unavailable depending on business |
| Inventory       | Usually required for purchase              | Disable purchase if unavailable                |
| Reviews         | Optional                                   | Hide reviews or show fallback                  |
| Recommendations | Optional                                   | Hide section                                   |
| Promotions      | Optional or required depending on business | Varies                                         |

For an account dashboard:

| Branch           | Required?                  | Failure behavior                     |
| ---------------- | -------------------------- | ------------------------------------ |
| Identity/profile | Required                   | Fail dashboard                       |
| Billing status   | Important                  | Show warning or fail billing section |
| Recent orders    | Optional                   | Show empty or unavailable state      |
| Notifications    | Optional                   | Show unavailable count               |
| Security alerts  | Required for security page | Fail closed                          |

The orchestrating service should define this explicitly.

A useful model:

```ts
type BranchRequirement = "REQUIRED" | "OPTIONAL";

type BranchResult<T> = {
  name: string;
  requirement: BranchRequirement;
  value?: T;
  error?: {
    code: string;
    message: string;
  };
};
```

This prevents accidental all-or-nothing behavior.

---

#### Conditional branching

Conditional branching chooses a path based on context.

For example, a payment service may route payments to different providers.

```mermaid
flowchart TD
    PaymentRequest[Payment Request]
    PaymentService[Payment Service]

    Decision{Payment Method}

    Card[Card Processor]
    Bank[Bank Transfer Provider]
    Wallet[Digital Wallet Provider]

    PaymentRequest --> PaymentService
    PaymentService --> Decision

    Decision -->|Card| Card
    Decision -->|Bank transfer| Bank
    Decision -->|Wallet| Wallet
```

Example implementation:

```ts
type PaymentMethodType = "CARD" | "BANK_TRANSFER" | "WALLET";

type PaymentCommand = {
  paymentId: string;
  amount: number;
  currency: string;
  methodType: PaymentMethodType;
  paymentMethodToken: string;
};

interface PaymentProvider {
  authorize(command: PaymentCommand): Promise<PaymentAuthorization>;
}

class PaymentService {
  constructor(
    private readonly cardProvider: PaymentProvider,
    private readonly bankProvider: PaymentProvider,
    private readonly walletProvider: PaymentProvider
  ) {}

  async authorize(command: PaymentCommand): Promise<PaymentAuthorization> {
    switch (command.methodType) {
      case "CARD":
        return this.cardProvider.authorize(command);

      case "BANK_TRANSFER":
        return this.bankProvider.authorize(command);

      case "WALLET":
        return this.walletProvider.authorize(command);
    }
  }
}
```

This is conditional branching inside a domain service. The Payment Service owns the decision because payment provider selection is part of the payment domain.

---

#### Tenant-specific branching

Multi-tenant systems often need tenant-specific paths.

```mermaid
flowchart TD
    Request[Incoming Request]
    TenantResolver[Tenant Resolver]

    Decision{Tenant Type}

    Shared[Shared Service Cluster]
    Dedicated[Dedicated Enterprise Cluster]
    Regulated[Regulated Environment]

    Request --> TenantResolver
    TenantResolver --> Decision

    Decision -->|Standard tenant| Shared
    Decision -->|Enterprise tenant| Dedicated
    Decision -->|Regulated tenant| Regulated
```

Examples:

* standard tenants use shared infrastructure,
* enterprise tenants use dedicated infrastructure,
* regulated tenants use a special compliant environment,
* one tenant has a custom integration.

Example:

```ts
function selectOrderBackend(tenant: Tenant): RouteTarget {
  if (tenant.complianceTier === "REGULATED") {
    return {
      serviceName: "orders-regulated",
      baseUrl: "https://orders.regulated.internal"
    };
  }

  if (tenant.dedicatedClusterUrl) {
    return {
      serviceName: "orders-dedicated",
      baseUrl: tenant.dedicatedClusterUrl
    };
  }

  return {
    serviceName: "orders-shared",
    baseUrl: "https://orders.shared.internal"
  };
}
```

Tenant-specific branching must be secure. Do not trust tenant values supplied directly by the client unless they are verified through authentication or API key context.

---

#### Region-specific branching

Region-specific branching routes requests based on geography, data residency, or latency.

```mermaid
flowchart TD
    Request[Request]
    RegionPolicy[Region Policy]

    Decision{Data Region}

    US[US Services]
    EU[EU Services]
    APAC[APAC Services]

    Request --> RegionPolicy
    RegionPolicy --> Decision

    Decision -->|US| US
    Decision -->|EU| EU
    Decision -->|APAC| APAC
```

Region branching is useful for:

* data residency,
* latency optimization,
* disaster recovery,
* legal compliance,
* regional feature availability.

Example:

```ts
function selectRegionalEndpoint(user: UserContext): string {
  switch (user.dataRegion) {
    case "US":
      return "https://api.us.internal";

    case "EU":
      return "https://api.eu.internal";

    case "APAC":
      return "https://api.apac.internal";
  }
}
```

Region routing must be carefully audited. Incorrect routing can violate data residency requirements.

---

#### Multi-provider branching

The Branch Pattern is common when integrating with multiple providers.

For example, a shipping service may choose among carriers.

```mermaid
flowchart TD
    ShipmentRequest[Shipment Request]
    ShippingService[Shipping Service]

    Decision{Carrier Selection}

    UPS[UPS Adapter]
    FedEx[FedEx Adapter]
    DHL[DHL Adapter]
    Local[Local Courier Adapter]

    ShipmentRequest --> ShippingService
    ShippingService --> Decision

    Decision -->|Domestic standard| UPS
    Decision -->|Domestic express| FedEx
    Decision -->|International| DHL
    Decision -->|Same-day local| Local
```

The decision can be based on:

* destination,
* package size,
* package weight,
* delivery speed,
* carrier cost,
* carrier availability,
* customer preference,
* business rules.

Example:

```ts
function selectCarrier(request: ShipmentRequest): Carrier {
  if (request.destination.country !== "US") {
    return "DHL";
  }

  if (request.deliverySpeed === "EXPRESS") {
    return "FEDEX";
  }

  if (request.deliverySpeed === "SAME_DAY") {
    return "LOCAL_COURIER";
  }

  return "UPS";
}
```

This is business logic and should live in the Shipping Service or a dedicated carrier selection service, not in a generic gateway.

---

#### Data enrichment branching

Data enrichment is a common parallel-branch use case.

For example, a search service may enrich search results with price, availability, and ratings.

```mermaid
flowchart TD
    SearchRequest[Search Request]
    SearchService[Search Service]

    CatalogSearch[Catalog Search Index]
    Pricing[Pricing Service]
    Inventory[Inventory Service]
    Reviews[Reviews Service]

    SearchResponse[Enriched Search Results]

    SearchRequest --> SearchService

    SearchService --> CatalogSearch
    CatalogSearch --> SearchService

    SearchService --> Pricing
    SearchService --> Inventory
    SearchService --> Reviews

    Pricing --> SearchResponse
    Inventory --> SearchResponse
    Reviews --> SearchResponse
```

This is useful, but it can create high fan-out.

If a search result page contains 50 products, calling Pricing, Inventory, and Reviews once per product can create 150 downstream calls.

Better design uses batch APIs:

```mermaid
flowchart TD
    SearchService[Search Service]

    ProductIds[50 Product IDs]

    PricingBatch[Pricing Batch API]
    InventoryBatch[Inventory Batch API]
    ReviewsBatch[Reviews Batch API]

    SearchService --> ProductIds

    ProductIds --> PricingBatch
    ProductIds --> InventoryBatch
    ProductIds --> ReviewsBatch
```

Example:

```http
POST /prices/batch
Content-Type: application/json

{
  "productIds": ["prod_1", "prod_2", "prod_3"],
  "currency": "USD"
}
```

Batching prevents the branch pattern from turning into a fan-out explosion.

---

#### Branch join

A branch usually needs a **join point**.

The join point combines results, handles failures, and decides what to return or do next.

```mermaid
flowchart TD
    Start[Start]

    BranchA[Branch A]
    BranchB[Branch B]
    BranchC[Branch C]

    Join[Join Point]

    Success[Return success]
    Partial[Return partial response]
    Failure[Return failure]

    Start --> BranchA
    Start --> BranchB
    Start --> BranchC

    BranchA --> Join
    BranchB --> Join
    BranchC --> Join

    Join --> Success
    Join --> Partial
    Join --> Failure
```

The join point must answer:

* Which branches are required?
* Which branches are optional?
* How long should we wait?
* What if one branch times out?
* What if a branch returns stale data?
* Should partial results be returned?
* Should failed branches be retried?
* Should failed branches trigger fallback data?
* Should the whole operation fail?

This is where branch pattern complexity usually appears.

---

#### Timeouts

Each branch needs a timeout.

Without branch-specific timeouts, one slow branch can delay the whole response.

```mermaid
flowchart TD
    Request[Request]
    Aggregator[Aggregator]

    FastA[Service A<br/>50 ms]
    FastB[Service B<br/>70 ms]
    SlowC[Service C<br/>3000 ms]

    Response[Response delayed]

    Request --> Aggregator

    Aggregator --> FastA
    Aggregator --> FastB
    Aggregator --> SlowC

    SlowC --> Response
```

Example helper:

```ts
async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  timeoutError: Error
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(timeoutError), timeoutMs)
    )
  ]);
}
```

Example branch call:

```ts
const recommendationsPromise = withTimeout(
  recommendationsClient.getRecommendations(userId),
  300,
  new Error("RECOMMENDATIONS_TIMEOUT")
);
```

Timeouts should reflect importance.

| Branch                     | Example timeout |
| -------------------------- | --------------: |
| Required account data      |         1000 ms |
| Required price data        |          500 ms |
| Optional reviews           |          300 ms |
| Optional recommendations   |          200 ms |
| Optional ads or promotions |          150 ms |

Optional branches should not hold the entire response hostage.

---

#### Fallbacks

A fallback provides alternate data when a branch fails.

```mermaid
flowchart TD
    Branch[Branch Call]
    Dependency[Dependency]
    Cache[(Cache)]
    Default[Default Value]

    Branch --> Dependency

    Dependency -->|success| Result[Use result]
    Dependency -. failure .-> Cache
    Cache -->|hit| Cached[Use cached result]
    Cache -. miss .-> Default
```

Examples:

| Branch                | Fallback                        |
| --------------------- | ------------------------------- |
| Recommendations       | Empty list                      |
| Reviews               | Cached review summary           |
| Product image service | Placeholder image               |
| Promotions            | No promotion shown              |
| Inventory estimate    | “Check availability”            |
| Shipping estimate     | “Delivery estimate unavailable” |

Example:

```ts
async function getRecommendationsOrFallback(userId: string) {
  try {
    return await withTimeout(
      recommendationsClient.getRecommendations(userId),
      250,
      new Error("RECOMMENDATIONS_TIMEOUT")
    );
  } catch {
    return [];
  }
}
```

Fallbacks should be explicit. Hidden fallback behavior can confuse users and operators.

---

#### Branching writes

Parallel branching is safer for reads than writes.

A read branch can usually tolerate partial failure.

A write branch can create inconsistent state if some branches succeed and others fail.

Example risky write branch:

```mermaid
flowchart TD
    Request[Create customer request]

    CRM[Create customer in CRM]
    Billing[Create billing account]
    Marketing[Create marketing profile]
    Support[Create support profile]

    Join[Join]

    Request --> CRM
    Request --> Billing
    Request --> Marketing
    Request --> Support

    CRM --> Join
    Billing --> Join
    Marketing --> Join
    Support --> Join
```

If CRM and Billing succeed but Support fails, what is the state of the customer?

For branching writes, you need a clear recovery strategy:

* retries,
* idempotency,
* compensation,
* eventual consistency,
* workflow state,
* dead-letter queues,
* manual repair tools.

Often, asynchronous messaging is safer:

```mermaid
flowchart TD
    Customer[Customer Service]
    Bus[(Event Bus)]

    Billing[Billing Service]
    Marketing[Marketing Service]
    Support[Support Service]

    Customer -->|CustomerCreated| Bus

    Bus --> Billing
    Bus --> Marketing
    Bus --> Support
```

The Customer Service commits the customer. Other services react independently.

---

#### Idempotency in branches

If branch operations can be retried, they should be idempotent.

For example:

```http
POST /billing/accounts
Idempotency-Key: customer_123_create_billing_account
```

This prevents duplicate accounts if the branch call times out and is retried.

Example:

```ts
async function createBillingAccount(customerId: string) {
  return fetch("http://billing-service/accounts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Idempotency-Key": `customer_${customerId}_billing_account`
    },
    body: JSON.stringify({ customerId })
  });
}
```

For parallel writes, idempotency is not optional. It is a core safety mechanism.

---

#### Concurrency limits

Parallel branching can overload dependencies.

If one request fans out to 10 services, and traffic is 1,000 requests per second, the system may create up to 10,000 downstream requests per second.

```mermaid
flowchart TD
    Incoming[1000 requests per second]
    Brancher[Branching Service]

    Fanout[10 branches per request]
    Downstream[10000 downstream calls per second]

    Incoming --> Brancher
    Brancher --> Fanout
    Fanout --> Downstream
```

Use concurrency limits to protect downstream systems.

Example:

```ts
import pLimit from "p-limit";

const limit = pLimit(10);

const results = await Promise.all(
  productIds.map((productId) =>
    limit(() => inventoryClient.getAvailability(productId))
  )
);
```

Better yet, provide batch APIs when possible.

Concurrency control prevents a branching service from becoming a traffic amplifier.

---

#### Branch explosion

Branch explosion happens when a service accumulates too many conditional paths.

```mermaid
flowchart TD
    Request[Request]

    Tenant{Tenant}
    Region{Region}
    Product{Product Type}
    FeatureFlag{Feature Flag}
    CustomerTier{Customer Tier}

    Path1[Path 1]
    Path2[Path 2]
    Path3[Path 3]
    Path4[Path 4]
    Path5[Path 5]
    Path6[Path 6]

    Request --> Tenant
    Tenant --> Region
    Region --> Product
    Product --> FeatureFlag
    FeatureFlag --> CustomerTier

    CustomerTier --> Path1
    CustomerTier --> Path2
    CustomerTier --> Path3
    CustomerTier --> Path4
    CustomerTier --> Path5
    CustomerTier --> Path6
```

Too many branches make behavior difficult to reason about.

Symptoms:

* nobody can explain which path a request takes,
* tests cover only common paths,
* feature flags interact unpredictably,
* tenant-specific rules pile up,
* debugging requires reconstructing routing decisions,
* small changes break obscure paths.

Mitigation:

* keep branch rules explicit,
* log branch decisions,
* remove old feature flags,
* avoid tenant-specific code when possible,
* extract domain policies into owned services,
* test important path combinations,
* document decision tables.

---

#### Decision tables

For conditional branching, decision tables are often clearer than nested `if` statements.

Example:

| Customer type | Region            | Order amount | Path                   |
| ------------- | ----------------- | -----------: | ---------------------- |
| Standard      | US                |          Any | Standard Checkout      |
| Premium       | US                |    Under 500 | Premium Checkout       |
| Premium       | US                |  500 or more | Premium Review         |
| Any           | EU                |          Any | EU Compliance Checkout |
| Any           | Restricted region |          Any | Blocked                |

Code can then mirror the decision table:

```ts
function selectCheckoutPath(input: CheckoutInput): CheckoutPath {
  if (input.region === "RESTRICTED") {
    return "BLOCKED";
  }

  if (input.region === "EU") {
    return "EU_COMPLIANCE_CHECKOUT";
  }

  if (input.customerType === "PREMIUM" && input.orderAmount >= 500) {
    return "PREMIUM_REVIEW";
  }

  if (input.customerType === "PREMIUM") {
    return "PREMIUM_CHECKOUT";
  }

  return "STANDARD_CHECKOUT";
}
```

Decision tables make branching easier to review with product managers, compliance experts, and domain experts.

---

#### Observability

Branching requires strong observability because different requests may take different paths.

Track:

* branch names,
* selected conditional path,
* branch start time,
* branch latency,
* branch result,
* branch timeout,
* branch fallback usage,
* required vs optional branches,
* partial response count,
* downstream status codes,
* fan-out count,
* decision inputs used for routing.

Example log:

```json
{
  "requestId": "req_123",
  "operation": "BuildProductPage",
  "selectedPath": "STANDARD_PRODUCT_PAGE",
  "branches": {
    "product": {
      "required": true,
      "status": "success",
      "latencyMs": 42
    },
    "pricing": {
      "required": true,
      "status": "success",
      "latencyMs": 58
    },
    "reviews": {
      "required": false,
      "status": "timeout",
      "latencyMs": 300,
      "fallbackUsed": true
    },
    "recommendations": {
      "required": false,
      "status": "success",
      "latencyMs": 91
    }
  },
  "partialResponse": true
}
```

This helps answer:

* Which branches ran?
* Which branch failed?
* Was the failed branch required?
* Did the response use fallback data?
* Why did this request take a different path?
* Are optional branches frequently timing out?
* Is fan-out too high?

Distributed tracing is also important:

```mermaid
flowchart TD
    Request[Request]
    BranchingService[Branching Service]

    A[Service A]
    B[Service B]
    C[Service C]

    Trace[Distributed Trace]

    Request --> BranchingService

    BranchingService --> A
    BranchingService --> B
    BranchingService --> C

    Trace -. includes .-> BranchingService
    Trace -. includes .-> A
    Trace -. includes .-> B
    Trace -. includes .-> C
```

---

#### Testing strategy

Branches increase the number of paths to test.

Useful tests include:

| Test type                     | Purpose                                                 |
| ----------------------------- | ------------------------------------------------------- |
| Branch selection tests        | Verify conditional routing chooses the correct path     |
| Required branch failure tests | Verify required dependency failures fail the request    |
| Optional branch failure tests | Verify partial responses work                           |
| Timeout tests                 | Verify slow branches do not block forever               |
| Fallback tests                | Verify fallback data is used correctly                  |
| Fan-out tests                 | Verify branch count stays within limits                 |
| Authorization tests           | Verify each branch uses correct user and tenant context |
| Load tests                    | Verify parallel branches do not overload dependencies   |
| Decision table tests          | Verify all important path combinations                  |

Example branch selection test:

```ts
describe("selectCheckoutPath", () => {
  it("uses EU compliance checkout for EU region", () => {
    expect(
      selectCheckoutPath({
        customerType: "STANDARD",
        region: "EU",
        orderAmount: 100
      })
    ).toBe("EU_COMPLIANCE_CHECKOUT");
  });

  it("blocks restricted regions", () => {
    expect(
      selectCheckoutPath({
        customerType: "PREMIUM",
        region: "RESTRICTED",
        orderAmount: 1000
      })
    ).toBe("BLOCKED");
  });

  it("uses premium review for high-value premium orders", () => {
    expect(
      selectCheckoutPath({
        customerType: "PREMIUM",
        region: "US",
        orderAmount: 800
      })
    ).toBe("PREMIUM_REVIEW");
  });
});
```

Example partial failure test:

```ts
it("returns product page with warning when recommendations fail", async () => {
  recommendationsClient.getRecommendations.mockRejectedValue(
    new Error("timeout")
  );

  const response = await buildProductPage("prod_123");

  expect(response.productId).toBe("prod_123");
  expect(response.recommendations).toEqual([]);
  expect(response.warnings).toContainEqual({
    code: "RECOMMENDATIONS_UNAVAILABLE",
    message: "Recommendations are temporarily unavailable."
  });
});
```

---

#### Branch Pattern vs Gateway Aggregation

The Branch Pattern and Gateway Aggregation often appear together, but they are not identical.

Gateway Aggregation is a specific read composition pattern.

Branch Pattern is a broader communication shape.

| Concern             | Branch Pattern                          | Gateway Aggregation                         |
| ------------------- | --------------------------------------- | ------------------------------------------- |
| Main idea           | Split request into multiple paths       | Combine service responses into one response |
| Can be conditional? | Yes                                     | Sometimes                                   |
| Can be parallel?    | Yes                                     | Usually                                     |
| Can involve writes? | Yes, but risky                          | Usually read-focused                        |
| Common location     | Services, gateways, BFFs, orchestrators | Gateway, BFF, aggregator service            |
| Main risk           | Partial failure and branch explosion    | Coupling and fan-out                        |

A dashboard aggregator uses the Branch Pattern internally.

A payment provider selector uses conditional branching but is not gateway aggregation.

---

#### Branch Pattern vs Saga

The Branch Pattern describes fan-out or conditional paths.

Saga describes a distributed transaction made of local transactions and compensating actions.

If branches are read-only, you probably do not need a saga.

If branches perform writes and partial success must be repaired, you may need Saga behavior.

```mermaid
flowchart TD
    WriteBranch[Parallel write branches]

    A[Create billing account]
    B[Create marketing profile]
    C[Create support profile]

    Failure[One branch fails]

    Saga[Need retry or compensation]

    WriteBranch --> A
    WriteBranch --> B
    WriteBranch --> C

    C --> Failure
    Failure --> Saga
```

For branching writes, always ask:

> What happens if only some branches commit?

If the answer is complicated, this is probably a Saga or workflow problem.

---

#### When to use it

Use the Branch Pattern when:

* multiple independent service calls are needed,
* parallel calls can reduce latency,
* a request needs enrichment from several services,
* different request types need different paths,
* tenants or regions require different processing,
* provider selection is needed,
* optional data can be loaded independently,
* the workflow needs clear conditional routing,
* the join behavior is well understood.

Common examples:

* dashboard data assembly,
* product page enrichment,
* account summary endpoints,
* search result enrichment,
* payment provider selection,
* shipping carrier selection,
* tenant-specific routing,
* regional service selection,
* feature-flagged workflows,
* multi-provider fallback logic.

---

#### When not to use it

Avoid or reconsider this pattern when:

* branches are not actually independent,
* branch results must be strongly consistent,
* branch failures cannot be tolerated,
* many branches perform writes,
* compensation is required but not designed,
* fan-out would overload dependencies,
* conditional paths are too complex to test,
* the branching service would own too much business logic,
* the client or caller does not need all branch results immediately.

For complex write workflows, consider Saga, orchestration, or asynchronous messaging.

For expensive read branching, consider a CQRS read model or precomputed materialized view.

---

#### Benefits

**1. Reduces latency through parallelism**

Independent calls can run at the same time.

**2. Supports conditional processing**

Different request types, tenants, regions, or providers can follow different paths.

**3. Improves modularity**

Each branch can call the service that owns that piece of data or behavior.

**4. Supports graceful degradation**

Optional branches can fail without failing the whole request.

**5. Works well for enrichment**

Product pages, dashboards, and search results often need data from multiple sources.

**6. Makes variation explicit**

Conditional paths can be documented and tested as decision rules.

---

#### Trade-offs

**1. Error handling becomes more complex**

Each branch can succeed, fail, timeout, or return partial data.

**2. Join logic can become complicated**

The caller must decide how to combine results and handle missing data.

**3. Fan-out can overload services**

One request can generate many downstream calls.

**4. Branch explosion can occur**

Too many conditions create hard-to-understand behavior.

**5. Observability is required**

Without tracing and branch-level logs, debugging is difficult.

**6. Writes are risky**

Parallel writes can leave the system partially complete.

**7. Authorization context must be preserved**

Each branch must call downstream services with the correct identity and tenant context.

---

#### Common mistakes

**Mistake 1: Treating all branches as required**

Optional branches should not fail the whole request unless the business requires it.

**Mistake 2: No timeout per branch**

One slow branch can delay the entire response.

**Mistake 3: No fallback strategy**

Optional data should often have a fallback or degraded response.

**Mistake 4: Fan-out explosion**

Avoid one branch per item when batch APIs or read models would be better.

**Mistake 5: Putting too much business routing in a gateway**

Business-specific branch decisions should live in the owning domain service.

**Mistake 6: Parallel writes without compensation**

If some write branches succeed and others fail, the system needs recovery.

**Mistake 7: No branch observability**

Logs should show which branches ran, which path was selected, and what failed.

**Mistake 8: Leaving old conditional branches forever**

Feature flags, temporary tenant paths, and migration branches should be cleaned up.

---

#### Practical design checklist

Before using the Branch Pattern, ask:

* Is this parallel branching, conditional branching, or both?
* Which branches are required?
* Which branches are optional?
* Can branches run independently?
* Does any branch depend on another branch’s result?
* What is the timeout for each branch?
* What happens if each branch fails?
* What fallback is available for each optional branch?
* Are any branches performing writes?
* If writes are involved, are they idempotent?
* If writes are involved, what compensation is required?
* How many downstream calls can one request create?
* Are batch APIs needed?
* Is fan-out limited?
* Is the branch decision technical or business-specific?
* Which service owns the branch decision?
* Is authorization context passed correctly to every branch?
* How are branch decisions logged?
* How are branch latencies measured?
* Are branch combinations covered by tests?
* How will temporary branches be removed?

A branch design is probably healthy if:

* branches are genuinely independent,
* required and optional branches are explicit,
* timeouts are defined,
* fallbacks are intentional,
* fan-out is controlled,
* branch decisions have clear ownership,
* writes are idempotent or avoided,
* branch behavior is observable and tested.

A branch design is probably unhealthy if:

* every branch is required by accident,
* one slow optional branch delays the whole response,
* a single request creates excessive downstream calls,
* business routing is hidden in gateway rules,
* parallel writes can partially succeed without recovery,
* no one can explain which path a request takes,
* feature flags and temporary paths accumulate permanently.

---

#### Related patterns

| Pattern                      | Relationship                                                                |
| ---------------------------- | --------------------------------------------------------------------------- |
| Gateway Aggregation          | Often uses parallel branching to fetch data from multiple services          |
| Backends for Frontends       | BFFs frequently use branching to build client-specific responses            |
| API Gateway                  | May perform simple technical branching by route, version, tenant, or region |
| Gateway Routing              | Conditional routing is a form of branching                                  |
| Chained Microservice Pattern | Chain is sequential; branch is parallel or conditional                      |
| Saga                         | Needed when branching writes require compensation                           |
| Async Messaging              | Alternative when branches do not need to complete before returning          |
| CQRS                         | Read models can replace expensive runtime branching                         |
| Circuit Breaker              | Protects branches from failing dependencies                                 |
| Bulkhead                     | Isolates resources so one slow branch does not affect others                |
| Retry                        | Can be used carefully for transient branch failures                         |
| Distributed Tracing          | Essential for debugging branched request flows                              |

---

#### Summary

The Branch Pattern sends a request down multiple paths, either in parallel or conditionally.

The central idea is:

> When work is independent, branch it. When request types differ, choose the right path explicitly.

This pattern is useful for dashboards, product pages, enrichment, tenant-specific behavior, regional routing, provider selection, and conditional workflows.

A good branch design clearly defines:

* which branches run,
* which branches are required,
* which branches are optional,
* how results are joined,
* what happens when a branch fails,
* how timeouts and fallbacks work,
* how fan-out is controlled,
* and who owns each branch decision.

The main risks are partial failure, branch explosion, uncontrolled fan-out, and unsafe parallel writes. Use branching for independent work, but switch to orchestration, Saga, async messaging, or read models when the workflow becomes too stateful or complex.


---

### 17. Async Messaging

#### What it is

**Async Messaging** is a communication pattern where services exchange information through queues, topics, event streams, or message brokers instead of waiting for direct, immediate responses from each other.

In synchronous communication, one service calls another and waits:

```mermaid
sequenceDiagram
    participant Orders as Order Service
    participant Payments as Payment Service

    Orders->>Payments: Authorize payment
    Payments-->>Orders: Payment authorized
```

In asynchronous communication, one service sends a message and continues. Another service processes the message later.

```mermaid
sequenceDiagram
    participant Orders as Order Service
    participant Broker as Message Broker
    participant Payments as Payment Service

    Orders->>Broker: Publish OrderCreated event
    Broker-->>Payments: Deliver OrderCreated event
    Payments->>Payments: Process payment authorization
```

The central idea is:

> Services do not need to be online, fast, or immediately available at the same time in order to communicate.

A producer sends a message. A broker stores or routes it. A consumer receives and processes it independently.

```mermaid
flowchart TD
    Producer[Producer Service]
    Broker[(Message Broker)]
    ConsumerA[Consumer Service A]
    ConsumerB[Consumer Service B]
    ConsumerC[Consumer Service C]

    Producer --> Broker

    Broker --> ConsumerA
    Broker --> ConsumerB
    Broker --> ConsumerC
```

Async Messaging is common in microservice systems because it reduces direct runtime dependency between services.

---

#### Why this pattern exists

In synchronous systems, services are **temporally coupled**.

That means both services must be available at the same time for communication to succeed.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]

    OrderService -->|must be online now| PaymentService
```

If Payment Service is down, Order Service may fail immediately.

In async messaging, Order Service can publish a message even if Payment Service is temporarily unavailable, as long as the broker is available.

```mermaid
flowchart TD
    OrderService[Order Service]
    Broker[(Message Broker)]
    PaymentService[Payment Service<br/>temporarily unavailable]

    OrderService -->|publish event| Broker
    Broker -. deliver later .-> PaymentService
```

Payment Service can process the message when it recovers.

This is useful because distributed systems are full of temporary failures:

* services restart,
* deployments happen,
* networks fail,
* dependencies slow down,
* traffic spikes,
* databases become briefly unavailable,
* third-party APIs time out.

Async Messaging allows systems to absorb these disruptions more gracefully.

---

#### What it solves

Async Messaging primarily solves **temporal coupling**.

With synchronous communication, the caller waits for the callee:

```mermaid
sequenceDiagram
    participant A as Service A
    participant B as Service B

    A->>B: Request
    B-->>A: Response
```

If B is slow, A is slow.
If B is unavailable, A may fail.
If many callers depend on B, B can become a bottleneck.

With asynchronous communication, the caller publishes work or facts to a broker:

```mermaid
sequenceDiagram
    participant A as Service A
    participant Broker as Broker
    participant B as Service B

    A->>Broker: Message
    Broker-->>A: Accepted
    Broker-->>B: Deliver message later
```

This lets Service A continue without waiting for Service B to complete its work.

Async Messaging helps with:

* long-running work,
* background processing,
* retryable tasks,
* event-driven workflows,
* data replication,
* audit pipelines,
* notifications,
* integration with slow systems,
* smoothing traffic spikes,
* decoupling producers from consumers.

---

#### Queue vs topic vs event stream

Async Messaging has several common forms.

##### Queue

A **queue** delivers each message to one consumer.

```mermaid
flowchart TD
    Producer[Producer]
    Queue[(Queue)]

    WorkerA[Worker A]
    WorkerB[Worker B]
    WorkerC[Worker C]

    Producer --> Queue

    Queue --> WorkerA
    Queue --> WorkerB
    Queue --> WorkerC
```

If there are multiple workers, they share the work. Each message is processed by one worker.

Use queues for:

* background jobs,
* task processing,
* email sending,
* image processing,
* report generation,
* payment retries,
* one-time commands.

Example message:

```json
{
  "messageType": "SendEmail",
  "messageId": "msg_123",
  "data": {
    "to": "customer@example.com",
    "template": "order-confirmation",
    "orderId": "ord_456"
  }
}
```

---

##### Topic / publish-subscribe

A **topic** broadcasts messages to multiple subscribers.

```mermaid
flowchart TD
    Publisher[Publisher]
    Topic[(Topic)]

    Billing[Billing Service]
    Analytics[Analytics Service]
    Notifications[Notification Service]
    Search[Search Indexer]

    Publisher --> Topic

    Topic --> Billing
    Topic --> Analytics
    Topic --> Notifications
    Topic --> Search
```

Each subscriber receives its own copy.

Use topics for:

* domain events,
* event-driven workflows,
* audit events,
* notifications,
* data replication,
* analytics pipelines,
* cache invalidation.

Example event:

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt_123",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "orderId": "ord_456",
    "customerId": "cus_789",
    "totalAmount": 129.99,
    "currency": "USD"
  }
}
```

---

##### Event stream

An **event stream** stores an ordered log of events that consumers can read from.

```mermaid
flowchart TD
    Producer[Producer]
    Stream[(Event Stream)]

    ConsumerA[Consumer A]
    ConsumerB[Consumer B]

    OffsetA[Consumer A Offset]
    OffsetB[Consumer B Offset]

    Producer --> Stream

    Stream --> ConsumerA
    Stream --> ConsumerB

    ConsumerA --> OffsetA
    ConsumerB --> OffsetB
```

Consumers track their own position, often called an offset.

Use event streams for:

* high-volume event processing,
* event replay,
* analytics,
* data pipelines,
* change data capture,
* materialized views,
* audit trails.

Unlike a simple queue, a stream often keeps messages for a retention period, allowing consumers to replay historical events.

---

#### Commands vs events

Async messages usually fall into two major categories:

1. **Commands**
2. **Events**

A **command** asks another service to do something.

```json
{
  "messageType": "AuthorizePayment",
  "messageId": "msg_123",
  "data": {
    "orderId": "ord_456",
    "amount": 129.99,
    "currency": "USD"
  }
}
```

A command is imperative:

> Please authorize this payment.

An **event** says something already happened.

```json
{
  "eventType": "PaymentAuthorized",
  "eventId": "evt_789",
  "occurredAt": "2026-04-29T12:01:00Z",
  "data": {
    "orderId": "ord_456",
    "paymentId": "pay_123"
  }
}
```

An event is factual:

> Payment was authorized.

The difference matters.

| Message type | Meaning          | Typical recipient           |
| ------------ | ---------------- | --------------------------- |
| Command      | “Please do this” | One logical handler         |
| Event        | “This happened”  | Many interested subscribers |

Commands often go through queues. Events often go through topics or streams.

---

#### Example: async order workflow

Suppose an Order Service creates an order.

Instead of directly calling Payment Service, Inventory Service, Notification Service, and Analytics Service synchronously, it publishes an event.

```mermaid
flowchart TD
    Orders[Order Service]
    Broker[(Event Broker)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Notifications[Notification Service]
    Analytics[Analytics Service]

    Orders -->|OrderCreated| Broker

    Broker --> Payments
    Broker --> Inventory
    Broker --> Notifications
    Broker --> Analytics
```

Each service reacts independently.

Payment Service may authorize payment.

Inventory Service may reserve stock.

Notification Service may send an email.

Analytics Service may update dashboards.

The Order Service does not need to wait for all of them before responding to the user.

---

#### Example sequence

```mermaid
sequenceDiagram
    participant Client
    participant Orders as Order Service
    participant Broker as Event Broker
    participant Payments as Payment Service
    participant Inventory as Inventory Service
    participant Notifications as Notification Service

    Client->>Orders: POST /orders
    Orders->>Orders: Create pending order
    Orders->>Broker: Publish OrderCreated
    Orders-->>Client: 202 Accepted

    Broker-->>Payments: OrderCreated
    Payments->>Payments: Authorize payment
    Payments->>Broker: Publish PaymentAuthorized

    Broker-->>Inventory: OrderCreated
    Inventory->>Inventory: Reserve stock
    Inventory->>Broker: Publish InventoryReserved

    Broker-->>Notifications: OrderCreated
    Notifications->>Notifications: Send confirmation email
```

The client receives an accepted response quickly. The rest of the workflow continues asynchronously.

This improves responsiveness, but it also means the workflow is eventually consistent. The order may not be fully confirmed immediately.

---

#### Immediate response vs eventual completion

Async systems often return a response before all processing is complete.

Example:

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{
  "orderId": "ord_456",
  "status": "PENDING_PROCESSING"
}
```

The user can later check status:

```http
GET /orders/ord_456
```

Response:

```json
{
  "orderId": "ord_456",
  "status": "CONFIRMED",
  "paymentStatus": "AUTHORIZED",
  "inventoryStatus": "RESERVED"
}
```

This is different from synchronous systems, where the caller usually expects all work to complete before the response returns.

Async Messaging works best when the business can tolerate intermediate states such as:

* pending,
* processing,
* awaiting payment,
* awaiting inventory,
* queued,
* retrying,
* failed,
* completed.

---

#### Example implementation: publishing a message

Here is a simplified TypeScript example that creates an order and publishes an event.

```ts
import crypto from "crypto";

type CreateOrderCommand = {
  customerId: string;
  items: Array<{
    productId: string;
    quantity: number;
    unitPrice: number;
  }>;
};

type Order = {
  id: string;
  customerId: string;
  status: "PENDING_PROCESSING" | "CONFIRMED" | "FAILED";
  totalAmount: number;
};

type EventBus = {
  publish(topic: string, event: unknown): Promise<void>;
};

type OrderRepository = {
  create(order: Order): Promise<Order>;
};

function calculateTotal(items: CreateOrderCommand["items"]): number {
  return items.reduce(
    (sum, item) => sum + item.quantity * item.unitPrice,
    0
  );
}

async function createOrder(
  command: CreateOrderCommand,
  orderRepository: OrderRepository,
  eventBus: EventBus
): Promise<Order> {
  const order: Order = {
    id: `ord_${crypto.randomUUID()}`,
    customerId: command.customerId,
    status: "PENDING_PROCESSING",
    totalAmount: calculateTotal(command.items)
  };

  const savedOrder = await orderRepository.create(order);

  await eventBus.publish("order-events", {
    eventType: "OrderCreated",
    eventId: `evt_${crypto.randomUUID()}`,
    occurredAt: new Date().toISOString(),
    data: {
      orderId: savedOrder.id,
      customerId: savedOrder.customerId,
      totalAmount: savedOrder.totalAmount,
      items: command.items
    }
  });

  return savedOrder;
}
```

This is simple, but there is a hidden problem: the database write and event publish are not atomic. If the order is saved but event publishing fails, the system may lose the event.

That is why async systems often need the Outbox Pattern.

---

#### Outbox Pattern

The **Outbox Pattern** solves the problem of updating local state and publishing a message reliably.

Bad version:

```ts
await orderRepository.create(order);
await eventBus.publish("order-events", event);
```

If the database write succeeds but event publishing fails, the event is lost.

Better version:

```mermaid
flowchart TD
    Service[Order Service]
    DB[(Orders DB)]
    Outbox[(Outbox Table)]
    Publisher[Outbox Publisher]
    Broker[(Message Broker)]

    Service -->|same DB transaction| DB
    Service -->|same DB transaction| Outbox

    Publisher --> Outbox
    Publisher --> Broker
```

The service writes both the order and the event record in the same database transaction.

```ts
async function createOrderWithOutbox(
  command: CreateOrderCommand,
  db: Database
): Promise<Order> {
  return db.transaction(async (tx) => {
    const order = await tx.orders.insert({
      id: `ord_${crypto.randomUUID()}`,
      customerId: command.customerId,
      status: "PENDING_PROCESSING",
      totalAmount: calculateTotal(command.items)
    });

    await tx.outbox.insert({
      eventId: `evt_${crypto.randomUUID()}`,
      topic: "order-events",
      eventType: "OrderCreated",
      payload: JSON.stringify({
        orderId: order.id,
        customerId: order.customerId,
        totalAmount: order.totalAmount,
        items: command.items
      }),
      published: false,
      createdAt: new Date()
    });

    return order;
  });
}
```

A separate publisher process reads unpublished outbox records and sends them to the broker.

```ts
async function publishOutboxEvents(db: Database, eventBus: EventBus) {
  const events = await db.outbox.findUnpublished({
    limit: 100
  });

  for (const event of events) {
    await eventBus.publish(event.topic, JSON.parse(event.payload));

    await db.outbox.markPublished(event.eventId, {
      publishedAt: new Date()
    });
  }
}
```

The Outbox Pattern is one of the most important reliability patterns for Async Messaging.

---

#### Example implementation: consuming a message

A consumer receives a message and processes it.

```ts
type OrderCreatedEvent = {
  eventType: "OrderCreated";
  eventId: string;
  occurredAt: string;
  data: {
    orderId: string;
    customerId: string;
    totalAmount: number;
    items: Array<{
      productId: string;
      quantity: number;
    }>;
  };
};

async function handleOrderCreated(event: OrderCreatedEvent) {
  await paymentService.authorizePayment({
    orderId: event.data.orderId,
    customerId: event.data.customerId,
    amount: event.data.totalAmount
  });
}
```

This looks simple, but real consumers need idempotency.

The same message may be delivered more than once.

---

#### Duplicate messages

Most messaging systems provide **at-least-once delivery**.

That means the broker will try hard to deliver the message, but consumers may receive the same message multiple times.

Duplicates can happen when:

* a consumer processes a message but crashes before acknowledging it,
* the broker retries delivery,
* network issues hide a successful acknowledgment,
* a publisher sends the same event twice,
* a consumer restarts during processing.

```mermaid
sequenceDiagram
    participant Broker
    participant Consumer

    Broker->>Consumer: Deliver message
    Consumer->>Consumer: Process message successfully
    Consumer--xBroker: Ack lost due to crash/network issue
    Broker->>Consumer: Redeliver same message
```

Therefore, consumers must be idempotent.

---

#### Idempotent consumers

An idempotent consumer can process the same message more than once without causing duplicate side effects.

Bad consumer:

```ts
async function handlePaymentAuthorized(event: PaymentAuthorizedEvent) {
  await orderRepository.markAsPaid(event.data.orderId);
  await emailClient.sendPaymentConfirmation(event.data.orderId);
}
```

If the message is processed twice, the email may be sent twice.

Better consumer:

```ts
async function handlePaymentAuthorized(event: PaymentAuthorizedEvent) {
  const alreadyProcessed = await processedEventRepository.exists(event.eventId);

  if (alreadyProcessed) {
    return;
  }

  await db.transaction(async (tx) => {
    await tx.orders.markAsPaid(event.data.orderId);

    await tx.processedEvents.insert({
      eventId: event.eventId,
      processedAt: new Date()
    });
  });
}
```

The consumer records that it processed the event.

For side effects like email, use a durable record:

```ts
async function sendPaymentConfirmationOnce(event: PaymentAuthorizedEvent) {
  const notificationId = `payment-confirmation:${event.data.orderId}`;

  const created = await notificationRepository.createIfNotExists({
    notificationId,
    type: "PAYMENT_CONFIRMATION",
    orderId: event.data.orderId,
    status: "PENDING"
  });

  if (!created) {
    return;
  }

  await emailClient.sendPaymentConfirmation(event.data.orderId);

  await notificationRepository.markSent(notificationId);
}
```

Idempotency is not optional in async systems. It is a basic correctness requirement.

---

#### Retry policies

Async Messaging often uses retries for transient failures.

Example:

```mermaid
flowchart TD
    Message[Message]
    Consumer[Consumer]

    Success[Processed Successfully]
    Retry[Retry Later]
    DLQ[Dead Letter Queue]

    Message --> Consumer

    Consumer -->|success| Success
    Consumer -->|temporary failure| Retry
    Consumer -->|too many failures| DLQ
```

A retry policy should define:

* which errors are retryable,
* how many attempts are allowed,
* delay between attempts,
* whether exponential backoff is used,
* whether jitter is used,
* when to move to a dead-letter queue.

Example retry configuration:

```yaml
consumer:
  topic: order-events
  maxAttempts: 5
  backoff:
    type: exponential
    initialDelayMs: 1000
    maxDelayMs: 60000
    jitter: true
  deadLetterQueue: order-events-dlq
```

Not every error should be retried.

| Error type                      | Retry?      |
| ------------------------------- | ----------- |
| Temporary database timeout      | Usually yes |
| Network timeout                 | Usually yes |
| Third-party service unavailable | Usually yes |
| Invalid message schema          | No          |
| Missing required field          | No          |
| Unknown event type              | Usually no  |
| Business rule rejection         | Usually no  |

Retrying invalid messages wastes capacity and can block good messages.

---

#### Dead-letter queues

A **dead-letter queue**, often abbreviated as **DLQ**, stores messages that could not be processed successfully.

```mermaid
flowchart TD
    MainQueue[(Main Queue)]
    Consumer[Consumer]

    Processed[Processed]
    DLQ[(Dead Letter Queue)]

    MainQueue --> Consumer

    Consumer -->|success| Processed
    Consumer -->|permanent failure or max retries exceeded| DLQ
```

A DLQ is not a trash can. It is an operational tool.

Teams should monitor DLQs and investigate messages there.

A DLQ message should include enough context to debug:

```json
{
  "originalTopic": "order-events",
  "eventId": "evt_123",
  "eventType": "OrderCreated",
  "failedAt": "2026-04-29T12:05:00Z",
  "attempts": 5,
  "failureReason": "Missing required field: customerId",
  "payload": {
    "orderId": "ord_456"
  }
}
```

Operational questions:

* Who owns the DLQ?
* What alert fires when messages enter it?
* Can messages be replayed?
* Can messages be repaired?
* How long are DLQ messages retained?
* What data is safe to store in DLQ payloads?

A DLQ with no owner becomes a graveyard of broken workflows.

---

#### Ordering

Async systems must be explicit about ordering.

Some workflows need messages processed in order.

For example, these order events should be processed in sequence:

```text
OrderCreated
PaymentAuthorized
OrderConfirmed
OrderShipped
OrderDelivered
```

If consumers see them out of order, they may produce incorrect state.

```mermaid
flowchart TD
    Event1[OrderCreated]
    Event2[OrderConfirmed]
    Event3[OrderCancelled]

    Consumer[Consumer]

    Event2 --> Consumer
    Event1 --> Consumer
    Event3 --> Consumer

    Problem[Consumer receives events out of order]
    Consumer --> Problem
```

Not all messaging systems guarantee global ordering. Some provide ordering only within a partition or message group.

A common approach is to partition by entity ID.

```mermaid
flowchart TD
    Events[Order Events]

    Partition1[Partition 1<br/>orderId ord_1]
    Partition2[Partition 2<br/>orderId ord_2]
    Partition3[Partition 3<br/>orderId ord_3]

    Events --> Partition1
    Events --> Partition2
    Events --> Partition3
```

For order events, use `orderId` as the partition key so events for the same order are processed in order.

Example:

```ts
await eventBus.publish("order-events", event, {
  partitionKey: event.data.orderId
});
```

Ordering design questions:

* Do messages need global ordering?
* Or only per entity, such as per order or customer?
* What is the partition key?
* What happens when a message is delayed?
* Can the consumer handle out-of-order events?
* Does the consumer store event version numbers?

For many systems, per-entity ordering is enough. Global ordering is expensive and often unnecessary.

---

#### Event versioning and schema governance

Async messages are contracts.

Once multiple consumers depend on an event, changing it can break them.

Bad event evolution:

```json
{
  "eventType": "OrderCreated",
  "data": {
    "id": "ord_123"
  }
}
```

Old consumers expected `orderId`, but the publisher renamed it to `id`. They may fail.

Better approach: evolve additively.

Version 1:

```json
{
  "eventType": "OrderCreated",
  "schemaVersion": 1,
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456"
  }
}
```

Version 2 adds a field without removing old fields:

```json
{
  "eventType": "OrderCreated",
  "schemaVersion": 2,
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456",
    "currency": "USD"
  }
}
```

Safe changes usually include:

* adding optional fields,
* adding new event types,
* adding metadata,
* widening enum handling carefully.

Risky changes include:

* removing fields,
* renaming fields,
* changing field types,
* changing meaning,
* changing event timing,
* changing ordering guarantees.

Use schema governance tools or practices:

* schema registry,
* event contract tests,
* consumer-driven contracts,
* compatibility checks,
* event documentation,
* ownership metadata,
* deprecation policies.

---

#### Event envelope

A consistent event envelope helps consumers process messages reliably.

Example:

```json
{
  "eventId": "evt_123",
  "eventType": "OrderCreated",
  "schemaVersion": 1,
  "source": "order-service",
  "occurredAt": "2026-04-29T12:00:00Z",
  "correlationId": "corr_456",
  "causationId": "cmd_789",
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456"
  }
}
```

Common envelope fields:

| Field           | Purpose                                   |
| --------------- | ----------------------------------------- |
| `eventId`       | Unique identifier for idempotency         |
| `eventType`     | Describes what happened                   |
| `schemaVersion` | Supports evolution                        |
| `source`        | Publisher service                         |
| `occurredAt`    | Business event time                       |
| `publishedAt`   | Time event was published                  |
| `correlationId` | Connects related messages in one workflow |
| `causationId`   | Identifies what caused this event         |
| `data`          | Event-specific payload                    |

A consistent envelope improves observability, debugging, replay, and schema management.

---

#### Correlation and causation IDs

Async workflows can be hard to trace because work happens over time and across services.

Correlation IDs connect related messages.

```mermaid
flowchart TD
    Command[Create Order Command<br/>correlationId corr_123]
    Event1[OrderCreated<br/>correlationId corr_123]
    Event2[PaymentAuthorized<br/>correlationId corr_123]
    Event3[InventoryReserved<br/>correlationId corr_123]
    Event4[OrderConfirmed<br/>correlationId corr_123]

    Command --> Event1
    Event1 --> Event2
    Event1 --> Event3
    Event2 --> Event4
    Event3 --> Event4
```

Causation IDs show which message caused another message.

Example:

```json
{
  "eventId": "evt_payment_authorized",
  "eventType": "PaymentAuthorized",
  "correlationId": "corr_checkout_123",
  "causationId": "evt_order_created",
  "data": {
    "orderId": "ord_456",
    "paymentId": "pay_789"
  }
}
```

This helps answer:

* Which user action started this workflow?
* Which message caused this event?
* What messages belong to the same business process?
* Where did the workflow get stuck?

---

#### Backpressure

Async Messaging can absorb traffic spikes, but queues can grow.

```mermaid
flowchart TD
    Producers[Producers]
    Queue[(Queue)]
    Consumers[Consumers]

    Producers -->|high rate| Queue
    Queue -->|lower rate| Consumers

    Queue --> Backlog[Backlog grows]
```

Backpressure means the system responds when producers are faster than consumers.

Possible responses:

* scale consumers,
* slow producers,
* reject new work,
* prioritize messages,
* shed low-priority work,
* increase broker capacity,
* alert operators,
* move old messages to DLQ if appropriate.

Important metrics:

* queue depth,
* consumer lag,
* oldest message age,
* processing rate,
* failure rate,
* retry count,
* DLQ count.

A growing queue is not automatically bad. It may be normal during a spike. But an unbounded or aging backlog means consumers cannot keep up.

---

#### Consumer scaling

Consumers can usually scale horizontally.

```mermaid
flowchart TD
    Queue[(Queue)]

    Worker1[Worker 1]
    Worker2[Worker 2]
    Worker3[Worker 3]
    Worker4[Worker 4]

    Queue --> Worker1
    Queue --> Worker2
    Queue --> Worker3
    Queue --> Worker4
```

Adding more workers can increase throughput.

But scaling consumers has limits:

* database capacity,
* external API rate limits,
* partition count,
* ordering constraints,
* lock contention,
* downstream service capacity.

For example, if messages must be processed in order per customer, you cannot process all messages for the same customer in parallel without care.

Consumer scaling should consider both broker capacity and downstream dependency capacity.

---

#### Async request-reply

Sometimes a caller sends a message asynchronously but still expects a later response.

This is called async request-reply.

```mermaid
sequenceDiagram
    participant Client
    participant API as API Service
    participant Broker as Broker
    participant Worker as Worker Service

    Client->>API: Start report generation
    API->>Broker: GenerateReport command
    API-->>Client: 202 Accepted with jobId

    Broker-->>Worker: GenerateReport
    Worker->>Worker: Generate report
    Worker->>Broker: ReportGenerated event

    Client->>API: GET /jobs/job_123
    API-->>Client: Completed with report URL
```

This is useful for:

* report generation,
* video processing,
* document conversion,
* machine learning jobs,
* large exports,
* fraud review,
* onboarding workflows.

The API should expose job status:

```json
{
  "jobId": "job_123",
  "status": "PROCESSING"
}
```

Later:

```json
{
  "jobId": "job_123",
  "status": "COMPLETED",
  "resultUrl": "https://storage.example.com/reports/job_123.pdf"
}
```

This avoids blocking an HTTP request for a long-running process.

---

#### Async Messaging and Saga

Async Messaging is often used with the Saga pattern.

A saga coordinates a multi-step workflow through local transactions and events.

```mermaid
flowchart TD
    Orders[Order Service]
    Broker[(Event Broker)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    Orders -->|OrderCreated| Broker

    Broker --> Payments
    Payments -->|PaymentAuthorized| Broker

    Broker --> Inventory
    Inventory -->|InventoryReserved| Broker

    Broker --> Orders
    Orders -->|OrderConfirmed| Broker

    Broker --> Shipping
```

If a step fails, another event can trigger compensation.

```mermaid
flowchart TD
    Inventory[Inventory Service]
    Broker[(Event Broker)]
    Payments[Payment Service]
    Orders[Order Service]

    Inventory -->|InventoryReservationFailed| Broker

    Broker --> Payments
    Payments -->|VoidPaymentAuthorization| Payments

    Broker --> Orders
    Orders -->|CancelOrder| Orders
```

Async Messaging provides the communication style. Saga provides the workflow consistency pattern.

---

#### Async Messaging and CQRS

Async Messaging is also common with CQRS.

A write service publishes events. A read model consumes those events and builds query-optimized views.

```mermaid
flowchart TD
    OrderService[Order Service]
    Broker[(Event Broker)]

    Projector[Order Summary Projector]
    ReadDB[(Order Summary Read DB)]

    QueryAPI[Query API]
    Client[Client]

    OrderService -->|OrderCreated<br/>OrderConfirmed<br/>OrderShipped| Broker

    Broker --> Projector
    Projector --> ReadDB

    Client --> QueryAPI
    QueryAPI --> ReadDB
```

This is useful when clients need fast reads across data owned by multiple services.

The trade-off is eventual consistency. The read model may lag behind the write model.

---

#### Async Messaging and notifications

Notifications are a classic async use case.

Order Service should not block order creation while waiting for an email provider.

```mermaid
flowchart TD
    Orders[Order Service]
    Broker[(Event Broker)]
    Notifications[Notification Service]
    EmailProvider[Email Provider]

    Orders -->|OrderCreated| Broker
    Broker --> Notifications
    Notifications --> EmailProvider
```

If the email provider is slow or down, the order can still be created.

Notification Service can retry later.

This decouples business-critical order creation from non-critical notification delivery.

---

#### Async Messaging and audit pipelines

Audit logging is another common use case.

```mermaid
flowchart TD
    Services[Business Services]
    Broker[(Audit Event Stream)]
    AuditProcessor[Audit Processor]
    AuditStore[(Audit Store)]

    Services --> Broker
    Broker --> AuditProcessor
    AuditProcessor --> AuditStore
```

Services publish audit events such as:

```json
{
  "eventType": "UserPermissionChanged",
  "eventId": "evt_999",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "actorUserId": "user_admin",
    "targetUserId": "user_123",
    "permission": "billing:read",
    "action": "GRANTED"
  }
}
```

The audit pipeline can process, store, index, and export audit records independently from the main business request path.

---

#### Observability

Async systems need strong observability because work is no longer contained in one request-response call.

Track:

* messages published,
* messages consumed,
* queue depth,
* consumer lag,
* processing latency,
* end-to-end latency,
* retry count,
* DLQ count,
* message age,
* failure rate by consumer,
* schema validation failures,
* duplicate detection count,
* poison message count,
* consumer restart count.

Example structured log:

```json
{
  "service": "payment-service",
  "eventId": "evt_123",
  "eventType": "OrderCreated",
  "correlationId": "corr_456",
  "consumer": "payment-authorization-consumer",
  "status": "processed",
  "processingLatencyMs": 83,
  "attempt": 1
}
```

Important dashboards:

* broker health,
* queue depth by queue,
* consumer lag by consumer group,
* DLQ messages by topic,
* processing errors by event type,
* oldest unprocessed message age,
* event publish rate,
* event consume rate.

Async failures may not be visible to users immediately. That makes monitoring essential.

---

#### Replay

Some event streaming systems allow consumers to replay old messages.

Replay is useful for:

* rebuilding read models,
* fixing projection bugs,
* backfilling new consumers,
* recovering from data loss,
* testing new consumers,
* auditing historical changes.

```mermaid
flowchart TD
    Stream[(Event Stream)]
    OldConsumer[Existing Consumer]
    NewConsumer[New Consumer]

    Stream --> OldConsumer
    Stream -->|replay from beginning or offset| NewConsumer
```

Replay is powerful but dangerous.

Consumers must be idempotent. Otherwise replay can duplicate side effects such as emails, payments, or shipments.

Good replay candidates:

* updating a read model,
* rebuilding a search index,
* recalculating analytics,
* generating reports.

Risky replay candidates:

* sending emails,
* charging cards,
* creating shipments,
* calling external systems with side effects.

For side-effecting consumers, store processing records and design replay carefully.

---

#### Poison messages

A **poison message** is a message that repeatedly fails processing.

Example:

```json
{
  "eventType": "OrderCreated",
  "data": {
    "orderId": null
  }
}
```

If a consumer requires `orderId`, this message will fail every time.

Poison messages can block queues if not handled properly.

```mermaid
flowchart TD
    Queue[(Queue)]
    Poison[Poison Message]
    Consumer[Consumer]
    DLQ[(Dead Letter Queue)]

    Queue --> Poison
    Poison --> Consumer
    Consumer -->|fails repeatedly| Poison
    Poison -->|after max attempts| DLQ
```

Use DLQs, schema validation, and max retry limits to prevent poison messages from blocking progress.

---

#### Message size

Messages should usually be small.

Avoid putting large files or huge payloads directly into messages.

Bad:

```json
{
  "eventType": "DocumentUploaded",
  "data": {
    "fileBytesBase64": "very-large-base64-string..."
  }
}
```

Better:

```json
{
  "eventType": "DocumentUploaded",
  "data": {
    "documentId": "doc_123",
    "storageUrl": "s3://documents/doc_123.pdf",
    "contentType": "application/pdf",
    "sizeBytes": 10485760
  }
}
```

Use object storage for large payloads and send references in messages.

Large messages can hurt broker performance, increase latency, and complicate retries.

---

#### Security

Async Messaging needs security controls.

Important concerns:

* producer authorization,
* consumer authorization,
* topic or queue permissions,
* encryption in transit,
* encryption at rest,
* sensitive data in messages,
* retention period,
* PII handling,
* auditability,
* tenant isolation,
* replay permissions.

Example topic permissions:

```yaml
topics:
  order-events:
    producers:
      - order-service
    consumers:
      - payment-service
      - inventory-service
      - analytics-service

  payment-events:
    producers:
      - payment-service
    consumers:
      - order-service
      - accounting-service
```

Avoid putting unnecessary sensitive data in messages.

For example, do not include full payment card details in an event. Publish a payment token or payment ID instead.

---

#### When to use it

Use Async Messaging when:

* the caller does not need an immediate result,
* work can happen in the background,
* services should be loosely coupled,
* temporary failures should be absorbed,
* a process is long-running,
* multiple services need to react to the same event,
* traffic spikes should be smoothed,
* data needs to be replicated between services,
* read models need to be updated,
* audit or analytics pipelines need event data,
* external integrations are slow or unreliable.

Common use cases include:

* notifications,
* order processing,
* payment retries,
* inventory updates,
* search indexing,
* analytics pipelines,
* audit logging,
* data synchronization,
* report generation,
* image or video processing,
* machine learning jobs,
* onboarding workflows,
* background cleanup tasks.

---

#### When not to use it

Avoid Async Messaging when:

* the caller needs an immediate answer,
* the operation is simple and local,
* strong immediate consistency is required,
* users cannot tolerate intermediate states,
* the team cannot operate message infrastructure,
* message ordering and idempotency are not understood,
* debugging and observability are immature,
* the process would be simpler as a direct call.

For example, checking whether a password is valid during login usually needs a synchronous response.

Calculating a quick price quote may also be better as a synchronous call if the user is waiting for it.

Async Messaging is powerful, but it adds complexity. Do not use it just because it seems more “microservice-like.”

---

#### Benefits

**1. Reduces temporal coupling**

Producers and consumers do not need to be available at the same time.

**2. Improves resilience**

Temporary consumer failures can be absorbed by queues or streams.

**3. Smooths traffic spikes**

Queues buffer work when producers are faster than consumers.

**4. Supports loose coupling**

Publishers do not need to know every consumer.

**5. Enables background processing**

Long-running work can happen outside the request path.

**6. Supports fan-out**

Many consumers can react to the same event.

**7. Improves scalability**

Consumers can often scale horizontally.

**8. Supports event-driven architecture**

Services can publish facts and react independently.

---

#### Trade-offs

**1. Eventual consistency**

State changes may not be visible everywhere immediately.

**2. More operational complexity**

Brokers, queues, topics, consumers, retries, and DLQs must be operated.

**3. Duplicate handling is required**

Messages may be delivered more than once.

**4. Ordering is not automatic**

Ordering guarantees must be understood and designed.

**5. Debugging is harder**

Work happens across time and services.

**6. Schema governance is required**

Message changes can break consumers.

**7. Failures may be delayed**

A user may see success while downstream processing later fails.

**8. Backlogs can build**

Consumers may fall behind producers.

**9. Poison messages can block processing**

Invalid messages need safe handling.

---

#### Common mistakes

**Mistake 1: Assuming exactly-once processing**

Most systems require consumers to handle duplicates.

**Mistake 2: No idempotency**

Duplicate messages can create duplicate payments, emails, shipments, or records.

**Mistake 3: No DLQ**

Bad messages retry forever and block progress.

**Mistake 4: No schema governance**

Publishers change messages and break consumers.

**Mistake 5: No observability**

Teams cannot see queue depth, lag, retries, or failed messages.

**Mistake 6: Treating events as commands**

An event says something happened. A command asks someone to do something.

**Mistake 7: Publishing events outside the database transaction**

The system can save state but lose the event.

**Mistake 8: Putting too much data in messages**

Large or sensitive payloads create performance and security problems.

**Mistake 9: Ignoring ordering**

Consumers may process events in the wrong order.

**Mistake 10: Retrying permanent failures**

Invalid messages should go to a DLQ, not retry forever.

---

#### Practical design checklist

Before using Async Messaging, answer:

* Is this a command or an event?
* Who owns the message schema?
* Which service publishes the message?
* Which services consume it?
* Does the producer need to know the consumers?
* Does the caller need an immediate response?
* What is the expected delivery guarantee?
* Can messages be delivered more than once?
* Are consumers idempotent?
* Is ordering required?
* If ordering is required, what is the partition key?
* What is the retry policy?
* What errors are retryable?
* What errors are permanent?
* Is there a dead-letter queue?
* Who owns the DLQ?
* Can messages be replayed?
* Is replay safe for this consumer?
* How are schemas versioned?
* Are breaking changes prevented?
* How are correlation IDs propagated?
* How is message processing observed?
* What alerts are needed for lag and DLQ growth?
* How long are messages retained?
* Does the message contain sensitive data?
* How is access to topics and queues controlled?
* Is the Outbox Pattern needed?

A good async design is likely if:

* producers and consumers are loosely coupled,
* messages have clear ownership,
* consumers are idempotent,
* retries and DLQs are defined,
* schemas are versioned,
* queue lag is monitored,
* ordering assumptions are explicit,
* message payloads are small and safe,
* correlation IDs connect workflows,
* operators can replay or repair messages when needed.

A poor async design is likely if:

* messages are undocumented,
* consumers assume no duplicates,
* retries happen forever,
* no one monitors the DLQ,
* event schemas break without warning,
* business workflows get stuck invisibly,
* messages contain sensitive data unnecessarily,
* ordering is assumed but not guaranteed,
* publishing can fail after local state commits.

---

#### Related patterns

| Pattern                      | Relationship                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------- |
| Event-Driven Architecture    | Async Messaging is the communication foundation for event-driven systems     |
| Choreography                 | Services react to events without a central coordinator                       |
| Saga                         | Uses async messages to coordinate distributed transactions and compensations |
| Outbox Pattern               | Publishes messages reliably with local database changes                      |
| CQRS                         | Uses events to update read models                                            |
| Event Sourcing               | Stores state changes as events                                               |
| Branch Pattern               | Async fan-out can replace synchronous branches                               |
| Chained Microservice Pattern | Async messaging can reduce long synchronous chains                           |
| Circuit Breaker              | Protects consumers or producers from failing dependencies                    |
| Retry                        | Handles transient processing failures                                        |
| Dead Letter Queue            | Captures messages that cannot be processed                                   |
| Consumer-Driven Contracts    | Helps protect consumers from breaking schema changes                         |
| Distributed Tracing          | Correlates async workflows across services                                   |

---

#### Summary

Async Messaging lets services communicate through queues, topics, event streams, or brokers without requiring immediate responses.

The central idea is:

> Producers publish messages now; consumers process them independently, possibly later.

This reduces temporal coupling, improves resilience, supports background work, and enables event-driven workflows.

A good async system has:

* clear command and event semantics,
* reliable publishing,
* idempotent consumers,
* retry policies,
* dead-letter queues,
* ordering rules,
* schema governance,
* correlation IDs,
* observability,
* and operational ownership.

The trade-off is complexity. Async systems are not automatically simpler than synchronous systems. They shift complexity from request handling into message delivery, retries, duplicate handling, ordering, monitoring, and eventual consistency. Done well, they make microservice systems more resilient and scalable. Done poorly, they create invisible failures and hard-to-debug workflows.


---

### 18. Choreography

#### What it is

**Choreography** is a workflow style where services collaborate by publishing and reacting to events, without a central service explicitly telling every participant what to do.

Each service listens for events it cares about. When it receives an event, it decides what action to take based on its own rules.

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Notifications[Notification Service]
    Analytics[Analytics Service]

    Orders -->|OrderCreated| Bus

    Bus --> Payments
    Bus --> Inventory
    Bus --> Notifications
    Bus --> Analytics
```

The central idea is:

> Services publish facts about what happened, and other services independently decide how to react.

For example, when an order is created:

* Payment Service may authorize payment.
* Inventory Service may reserve stock.
* Notification Service may send a confirmation email.
* Analytics Service may record the order for reporting.
* Fraud Service may evaluate risk.

The Order Service does not need to know every downstream reaction. It publishes `OrderCreated`, and interested services respond.

---

#### Why this pattern exists

In distributed systems, business workflows often involve many services.

A traditional approach is to use a central orchestrator:

```mermaid
flowchart TD
    Orchestrator[Workflow Orchestrator]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Notifications[Notification Service]

    Orchestrator --> Orders
    Orchestrator --> Payments
    Orchestrator --> Inventory
    Orchestrator --> Shipping
    Orchestrator --> Notifications
```

This can be useful when the workflow needs strict central control. But it can also create coupling. Every time a new service needs to participate, the orchestrator may need to change.

Choreography avoids that by letting services subscribe to events.

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Notifications[Notification Service]
    Fraud[Fraud Service]

    Orders -->|OrderCreated| Bus

    Bus --> Payments
    Bus --> Inventory
    Bus --> Fraud

    Payments -->|PaymentAuthorized| Bus
    Inventory -->|InventoryReserved| Bus
    Fraud -->|FraudCheckPassed| Bus

    Bus --> Shipping
    Bus --> Notifications
```

New behavior can often be added by subscribing a new service to an existing event. The publisher does not necessarily need to change.

For example, if the business wants to add loyalty points after every completed order, the Loyalty Service can subscribe to `OrderConfirmed`:

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]
    Loyalty[Loyalty Service]

    Orders -->|OrderConfirmed| Bus
    Bus --> Loyalty
```

The Order Service does not need to call Loyalty Service directly.

---

#### What it solves

Choreography solves the problem of **central workflow coupling**.

In an orchestrated workflow, one central component may know every step:

```mermaid
flowchart TD
    Checkout[Checkout Orchestrator]

    Checkout --> CreateOrder[Create Order]
    Checkout --> AuthorizePayment[Authorize Payment]
    Checkout --> ReserveInventory[Reserve Inventory]
    Checkout --> SendEmail[Send Email]
    Checkout --> UpdateAnalytics[Update Analytics]
    Checkout --> AwardLoyalty[Award Loyalty Points]
```

As the workflow grows, the orchestrator may become responsible for too much.

Choreography distributes the reactions:

```mermaid
flowchart TD
    Bus[(Event Bus)]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Notifications[Notification Service]
    Analytics[Analytics Service]
    Loyalty[Loyalty Service]

    Orders -->|OrderCreated| Bus
    Orders -->|OrderConfirmed| Bus

    Bus --> Payments
    Bus --> Inventory
    Bus --> Notifications
    Bus --> Analytics
    Bus --> Loyalty
```

Each service owns its own behavior:

| Service              | Event it reacts to               | Responsibility       |
| -------------------- | -------------------------------- | -------------------- |
| Payment Service      | `OrderCreated`                   | Authorize payment    |
| Inventory Service    | `OrderCreated`                   | Reserve stock        |
| Notification Service | `OrderConfirmed`                 | Send confirmation    |
| Analytics Service    | `OrderCreated`, `OrderConfirmed` | Update reporting     |
| Loyalty Service      | `OrderConfirmed`                 | Award loyalty points |

This reduces direct coupling between the original publisher and every downstream service.

---

#### Choreography vs orchestration

Choreography and orchestration are two different ways to coordinate distributed workflows.

**Orchestration** uses a central coordinator.

```mermaid
flowchart TD
    Orchestrator[Orchestrator]

    A[Service A]
    B[Service B]
    C[Service C]

    Orchestrator --> A
    Orchestrator --> B
    Orchestrator --> C
```

**Choreography** uses events and local reactions.

```mermaid
flowchart TD
    A[Service A]
    Bus[(Event Bus)]

    B[Service B]
    C[Service C]

    A -->|EventPublished| Bus
    Bus --> B
    Bus --> C
```

Comparison:

| Question                   | Choreography                               | Orchestration                        |
| -------------------------- | ------------------------------------------ | ------------------------------------ |
| Who controls the workflow? | Participating services react independently | A central coordinator directs steps  |
| Coupling style             | Event contracts                            | Command/API contracts                |
| Workflow visibility        | Distributed across services                | Centralized in orchestrator          |
| Adding new reactions       | Often easy: add a subscriber               | Usually requires orchestrator change |
| Failure handling           | Distributed                                | Centralized                          |
| Best for                   | Independent reactions to events            | Strict sequential business processes |
| Main risk                  | Workflow becomes hard to understand        | Orchestrator becomes too powerful    |

Neither is always better. Choreography works best when reactions are naturally independent. Orchestration works better when the business process needs clear central control.

---

#### Basic choreography flow

A choreographed workflow usually follows this pattern:

```mermaid
flowchart TD
    Step1[Service changes local state]
    Step2[Service publishes event]
    Step3[Other services receive event]
    Step4[Each service decides what to do]
    Step5[Some services publish new events]

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
```

Example:

```mermaid
sequenceDiagram
    participant Orders as Order Service
    participant Bus as Event Bus
    participant Payments as Payment Service
    participant Inventory as Inventory Service
    participant Shipping as Shipping Service

    Orders->>Orders: Create order
    Orders->>Bus: Publish OrderCreated

    Bus-->>Payments: OrderCreated
    Payments->>Payments: Authorize payment
    Payments->>Bus: Publish PaymentAuthorized

    Bus-->>Inventory: OrderCreated
    Inventory->>Inventory: Reserve stock
    Inventory->>Bus: Publish InventoryReserved

    Bus-->>Orders: PaymentAuthorized
    Bus-->>Orders: InventoryReserved

    Orders->>Orders: Confirm order
    Orders->>Bus: Publish OrderConfirmed

    Bus-->>Shipping: OrderConfirmed
    Shipping->>Shipping: Create shipment
```

No central orchestrator calls each participant. Services react to events and publish new events.

---

#### Example: order processing choreography

Consider a simplified e-commerce order workflow.

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]
    Notifications[Notification Service]

    Orders -->|OrderCreated| Bus

    Bus --> Payments
    Bus --> Inventory

    Payments -->|PaymentAuthorized| Bus
    Inventory -->|InventoryReserved| Bus

    Bus --> Orders

    Orders -->|OrderConfirmed| Bus

    Bus --> Shipping
    Bus --> Notifications
```

The behavior might be:

1. Order Service creates an order with status `PENDING`.
2. Order Service publishes `OrderCreated`.
3. Payment Service receives `OrderCreated` and authorizes payment.
4. Payment Service publishes `PaymentAuthorized`.
5. Inventory Service receives `OrderCreated` and reserves inventory.
6. Inventory Service publishes `InventoryReserved`.
7. Order Service receives both `PaymentAuthorized` and `InventoryReserved`.
8. Order Service confirms the order and publishes `OrderConfirmed`.
9. Shipping Service receives `OrderConfirmed` and creates a shipment.
10. Notification Service receives `OrderConfirmed` and sends a confirmation message.

Each service owns its local transaction and its own rules.

---

#### Event design

Choreography depends on well-designed events.

An event should represent something that happened in the business.

Good event names:

* `OrderCreated`
* `PaymentAuthorized`
* `PaymentAuthorizationFailed`
* `InventoryReserved`
* `InventoryReservationFailed`
* `OrderConfirmed`
* `ShipmentCreated`
* `RefundIssued`
* `CustomerSuspended`

Poor event names:

* `DoPayment`
* `CallInventory`
* `ProcessNextStep`
* `UpdateDatabase`
* `HandleOrderStuff`

Events should be facts, not instructions.

Good:

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt_123",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "orderId": "ord_456",
    "customerId": "cus_789",
    "totalAmount": 129.99,
    "currency": "USD"
  }
}
```

Less ideal:

```json
{
  "eventType": "AuthorizePaymentNow",
  "data": {
    "orderId": "ord_456"
  }
}
```

The first event says what happened. The second looks like a command.

Choreography is usually event-driven. Events should describe facts. Consumers decide what to do with those facts.

---

#### Event envelope

A consistent event envelope makes choreographed workflows easier to trace and operate.

```json
{
  "eventId": "evt_123",
  "eventType": "OrderCreated",
  "schemaVersion": 1,
  "source": "order-service",
  "occurredAt": "2026-04-29T12:00:00Z",
  "correlationId": "corr_checkout_001",
  "causationId": "cmd_create_order_001",
  "data": {
    "orderId": "ord_456",
    "customerId": "cus_789",
    "totalAmount": 129.99,
    "currency": "USD"
  }
}
```

Important fields:

| Field           | Purpose                            |
| --------------- | ---------------------------------- |
| `eventId`       | Unique ID for idempotency          |
| `eventType`     | The business fact that occurred    |
| `schemaVersion` | Supports event evolution           |
| `source`        | Service that published the event   |
| `occurredAt`    | When the business event happened   |
| `correlationId` | Groups events in the same workflow |
| `causationId`   | Identifies what caused this event  |
| `data`          | Event-specific payload             |

Without correlation and causation IDs, choreographed workflows are much harder to debug.

---

#### Local state and event publishing

In choreography, services often update local state and then publish an event.

For example, Order Service creates an order and publishes `OrderCreated`.

Bad version:

```ts
await orderRepository.create(order);
await eventBus.publish("order-events", orderCreatedEvent);
```

If the database write succeeds but publishing fails, the order exists but other services never receive `OrderCreated`.

A safer approach is the Outbox Pattern:

```mermaid
flowchart TD
    Service[Order Service]
    DB[(Orders DB)]
    Outbox[(Outbox Table)]
    Publisher[Outbox Publisher]
    Bus[(Event Bus)]

    Service -->|same transaction| DB
    Service -->|same transaction| Outbox

    Publisher --> Outbox
    Publisher --> Bus
```

Example:

```ts
async function createOrder(command: CreateOrderCommand, db: Database) {
  return db.transaction(async (tx) => {
    const order = await tx.orders.insert({
      customerId: command.customerId,
      status: "PENDING",
      totalAmount: command.totalAmount
    });

    await tx.outbox.insert({
      eventId: crypto.randomUUID(),
      eventType: "OrderCreated",
      topic: "order-events",
      payload: JSON.stringify({
        orderId: order.id,
        customerId: order.customerId,
        totalAmount: order.totalAmount
      }),
      published: false,
      createdAt: new Date()
    });

    return order;
  });
}
```

A background publisher sends outbox events to the broker.

This is critical for reliable choreography.

---

#### Example implementation: event handler

Payment Service may handle `OrderCreated`.

```ts
type OrderCreatedEvent = {
  eventId: string;
  eventType: "OrderCreated";
  occurredAt: string;
  correlationId: string;
  data: {
    orderId: string;
    customerId: string;
    totalAmount: number;
    currency: string;
  };
};

async function handleOrderCreated(event: OrderCreatedEvent) {
  const alreadyProcessed = await processedEventRepository.exists(event.eventId);

  if (alreadyProcessed) {
    return;
  }

  await db.transaction(async (tx) => {
    const authorization = await paymentGateway.authorize({
      orderId: event.data.orderId,
      customerId: event.data.customerId,
      amount: event.data.totalAmount,
      currency: event.data.currency
    });

    await tx.payments.insert({
      paymentId: authorization.paymentId,
      orderId: event.data.orderId,
      status: "AUTHORIZED",
      amount: event.data.totalAmount,
      currency: event.data.currency
    });

    await tx.outbox.insert({
      eventId: crypto.randomUUID(),
      eventType: "PaymentAuthorized",
      topic: "payment-events",
      correlationId: event.correlationId,
      causationId: event.eventId,
      payload: JSON.stringify({
        orderId: event.data.orderId,
        paymentId: authorization.paymentId
      }),
      published: false,
      createdAt: new Date()
    });

    await tx.processedEvents.insert({
      eventId: event.eventId,
      processedAt: new Date()
    });
  });
}
```

This handler does several important things:

* checks idempotency,
* performs a local transaction,
* records state,
* writes a new event to the outbox,
* records that the incoming event was processed.

That is the level of care choreographed systems need.

---

#### Idempotency

Choreographed systems must assume duplicate events can happen.

A consumer may receive the same event more than once because most brokers provide at-least-once delivery.

```mermaid
sequenceDiagram
    participant Broker
    participant Consumer

    Broker->>Consumer: OrderCreated evt_123
    Consumer->>Consumer: Processes successfully
    Consumer--xBroker: Ack lost
    Broker->>Consumer: OrderCreated evt_123 again
```

If the consumer is not idempotent, it may duplicate side effects.

Bad:

```ts
async function handleOrderConfirmed(event: OrderConfirmedEvent) {
  await emailClient.sendOrderConfirmation(event.data.orderId);
}
```

If the event is delivered twice, the customer may receive two emails.

Better:

```ts
async function handleOrderConfirmed(event: OrderConfirmedEvent) {
  const notificationId = `order-confirmation:${event.data.orderId}`;

  const created = await notificationRepository.createIfNotExists({
    notificationId,
    orderId: event.data.orderId,
    type: "ORDER_CONFIRMATION",
    status: "PENDING"
  });

  if (!created) {
    return;
  }

  await emailClient.sendOrderConfirmation(event.data.orderId);

  await notificationRepository.markSent(notificationId);
}
```

Every event handler should be safe to run more than once.

---

#### Ordering

Choreography often requires careful ordering.

For example:

```text
OrderCreated
PaymentAuthorized
InventoryReserved
OrderConfirmed
OrderCancelled
```

If a consumer receives `OrderConfirmed` before `OrderCreated`, it may fail.

Ordering can be handled in several ways:

1. **Partition by entity ID**

For order events, use `orderId` as the partition key.

```ts
await eventBus.publish("order-events", event, {
  partitionKey: event.data.orderId
});
```

This keeps events for the same order in the same ordered partition, assuming the broker supports partition ordering.

2. **Use version numbers**

```json
{
  "eventType": "OrderConfirmed",
  "aggregateId": "ord_123",
  "aggregateVersion": 3
}
```

Consumers can detect missing or out-of-order versions.

3. **Make consumers tolerant**

A consumer can store unknown future events temporarily, or fetch current state from the owning service when needed.

4. **Avoid unnecessary ordering assumptions**

Not every consumer needs strict ordering. Analytics may tolerate out-of-order events. Order state projection may not.

Ordering should be explicit. Do not assume global ordering unless the messaging system actually provides it.

---

#### Failure handling

In choreography, failures are handled locally by the service that encounters the failure.

For example, Payment Service may fail to authorize payment:

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]
    Payments[Payment Service]

    Orders -->|OrderCreated| Bus
    Bus --> Payments

    Payments -->|PaymentAuthorizationFailed| Bus
```

Order Service can react to `PaymentAuthorizationFailed`:

```mermaid
flowchart TD
    Bus[(Event Bus)]
    Orders[Order Service]
    Notifications[Notification Service]

    Bus -->|PaymentAuthorizationFailed| Orders
    Orders -->|OrderCancelled| Bus
    Bus --> Notifications
```

Example handler:

```ts
async function handlePaymentAuthorizationFailed(
  event: PaymentAuthorizationFailedEvent
) {
  await db.transaction(async (tx) => {
    const order = await tx.orders.findById(event.data.orderId);

    if (!order || order.status === "CANCELLED") {
      return;
    }

    await tx.orders.update(order.id, {
      status: "CANCELLED",
      cancellationReason: "PAYMENT_FAILED"
    });

    await tx.outbox.insert({
      eventId: crypto.randomUUID(),
      eventType: "OrderCancelled",
      topic: "order-events",
      correlationId: event.correlationId,
      causationId: event.eventId,
      payload: JSON.stringify({
        orderId: order.id,
        reason: "PAYMENT_FAILED"
      }),
      published: false,
      createdAt: new Date()
    });
  });
}
```

No central orchestrator tells Order Service what to do. Order Service reacts to a failure event and applies its own rules.

---

#### Compensation

Choreographed workflows often need compensating actions.

Suppose payment is authorized, but inventory reservation fails.

```mermaid
sequenceDiagram
    participant Orders as Order Service
    participant Bus as Event Bus
    participant Payments as Payment Service
    participant Inventory as Inventory Service

    Orders->>Bus: OrderCreated
    Bus-->>Payments: OrderCreated
    Payments->>Bus: PaymentAuthorized

    Bus-->>Inventory: OrderCreated
    Inventory->>Bus: InventoryReservationFailed

    Bus-->>Payments: InventoryReservationFailed
    Payments->>Bus: PaymentAuthorizationVoided

    Bus-->>Orders: InventoryReservationFailed
    Orders->>Bus: OrderCancelled
```

Payment Service may react to `InventoryReservationFailed` by voiding payment authorization.

This is a choreographed saga: each service reacts to events and performs local transactions or compensation.

The challenge is visibility. The workflow is distributed across event handlers.

---

#### Avoiding event loops

Choreography can accidentally create event loops.

```mermaid
flowchart TD
    ServiceA[Service A]
    Bus[(Event Bus)]
    ServiceB[Service B]

    ServiceA -->|EventA| Bus
    Bus --> ServiceB
    ServiceB -->|EventB| Bus
    Bus --> ServiceA
```

This is not automatically wrong, but it can be dangerous if each event triggers another indefinitely.

Example bad loop:

1. Customer Service publishes `CustomerUpdated`.
2. Marketing Service reacts and updates customer segment.
3. Customer Service reacts to segment update and publishes `CustomerUpdated`.
4. Marketing Service reacts again.

To avoid loops:

* use causation IDs,
* make handlers idempotent,
* avoid publishing events when nothing changed,
* distinguish command intent from state-change events,
* define ownership clearly,
* monitor event rates,
* detect repeated causation chains.

Example guard:

```ts
async function updateCustomerProfile(command: UpdateCustomerCommand) {
  const existing = await customerRepository.findById(command.customerId);

  const updated = applyUpdate(existing, command);

  if (deepEqual(existing, updated)) {
    return;
  }

  await customerRepository.save(updated);
  await publishCustomerUpdated(updated);
}
```

Do not publish an event if no meaningful state changed.

---

#### Workflow visibility

The biggest challenge with choreography is that the workflow is not in one place.

The “order workflow” may be spread across:

* Order Service event handlers,
* Payment Service event handlers,
* Inventory Service event handlers,
* Shipping Service event handlers,
* Notification Service event handlers,
* retry policies,
* DLQs,
* monitoring dashboards.

```mermaid
flowchart TD
    Workflow[Order Workflow]

    Orders[Order Service Handlers]
    Payments[Payment Service Handlers]
    Inventory[Inventory Service Handlers]
    Shipping[Shipping Service Handlers]
    Notifications[Notification Service Handlers]

    Workflow --> Orders
    Workflow --> Payments
    Workflow --> Inventory
    Workflow --> Shipping
    Workflow --> Notifications
```

This makes documentation and observability essential.

Useful artifacts include:

* event catalog,
* workflow diagrams,
* event ownership table,
* consumer ownership table,
* correlation ID tracing,
* dashboards by workflow,
* DLQ dashboards,
* message replay procedures,
* runbooks for stuck workflows.

Without these, choreography becomes “event soup.”

---

#### Event catalog

An event catalog documents events and their consumers.

Example:

| Event                        | Published by      | Consumed by                      | Meaning                         |
| ---------------------------- | ----------------- | -------------------------------- | ------------------------------- |
| `OrderCreated`               | Order Service     | Payment, Inventory, Analytics    | A new order was created         |
| `PaymentAuthorized`          | Payment Service   | Order Service, Accounting        | Payment authorization succeeded |
| `PaymentAuthorizationFailed` | Payment Service   | Order Service, Notifications     | Payment authorization failed    |
| `InventoryReserved`          | Inventory Service | Order Service                    | Stock was reserved              |
| `InventoryReservationFailed` | Inventory Service | Order Service, Payment Service   | Stock could not be reserved     |
| `OrderConfirmed`             | Order Service     | Shipping, Notifications, Loyalty | Order is ready for fulfillment  |

This should be treated as part of the architecture, not an afterthought.

---

#### Choreography and eventual consistency

Choreographed systems are usually eventually consistent.

For example, immediately after `OrderCreated`, the system may look like this:

```json
{
  "orderStatus": "PENDING",
  "paymentStatus": "UNKNOWN",
  "inventoryStatus": "UNKNOWN"
}
```

Later:

```json
{
  "orderStatus": "CONFIRMED",
  "paymentStatus": "AUTHORIZED",
  "inventoryStatus": "RESERVED"
}
```

The user experience must account for intermediate states.

Common states:

* `PENDING_PAYMENT`
* `PENDING_INVENTORY`
* `PROCESSING`
* `CONFIRMED`
* `FAILED`
* `CANCELLED`
* `RETRYING`

Do not pretend async workflows are instantly complete. Make progress visible.

---

#### Choreography and read models

Because choreography spreads state across services, clients often need a read model to see workflow status.

```mermaid
flowchart TD
    OrderEvents[Order Events]
    PaymentEvents[Payment Events]
    InventoryEvents[Inventory Events]

    Bus[(Event Bus)]

    Projector[Order Status Projector]
    ReadDB[(Order Status Read Model)]

    Client[Client]
    API[Query API]

    OrderEvents --> Bus
    PaymentEvents --> Bus
    InventoryEvents --> Bus

    Bus --> Projector
    Projector --> ReadDB

    Client --> API
    API --> ReadDB
```

The read model can show:

```json
{
  "orderId": "ord_456",
  "overallStatus": "CONFIRMED",
  "steps": {
    "orderCreated": "COMPLETED",
    "paymentAuthorized": "COMPLETED",
    "inventoryReserved": "COMPLETED",
    "shipmentCreated": "PENDING"
  }
}
```

This helps users and operators understand where the workflow stands.

---

#### Observability

Choreography needs stronger observability than simple synchronous flows.

Track:

* event publish rate,
* event consume rate,
* consumer lag,
* retry counts,
* DLQ counts,
* event processing latency,
* end-to-end workflow duration,
* stuck workflow count,
* event schema failures,
* duplicate detection count,
* out-of-order event count,
* compensation count,
* correlation ID traces.

Example log:

```json
{
  "service": "inventory-service",
  "handler": "handleOrderCreated",
  "eventId": "evt_123",
  "eventType": "OrderCreated",
  "correlationId": "corr_checkout_001",
  "orderId": "ord_456",
  "status": "processed",
  "latencyMs": 73
}
```

A good distributed trace should connect the original request to later async events.

```mermaid
flowchart TD
    Client[Client Request]
    Orders[Order Service]
    Bus[(Event Bus)]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    Client --> Orders
    Orders -->|OrderCreated corr_001| Bus
    Bus --> Payments
    Bus --> Inventory
    Payments -->|PaymentAuthorized corr_001| Bus
    Inventory -->|InventoryReserved corr_001| Bus
    Bus --> Shipping
```

Correlation IDs are essential.

---

#### Testing choreography

Testing choreographed workflows is harder than testing a single function call.

Useful test types include:

| Test type                 | Purpose                                             |
| ------------------------- | --------------------------------------------------- |
| Unit tests                | Test each event handler’s local behavior            |
| Contract tests            | Verify event schemas remain compatible              |
| Integration tests         | Verify services publish and consume expected events |
| End-to-end workflow tests | Verify full business process across services        |
| Idempotency tests         | Verify duplicate events are safe                    |
| Out-of-order tests        | Verify consumers handle unexpected order            |
| Failure tests             | Verify compensation events are produced             |
| DLQ tests                 | Verify poison messages are handled                  |
| Replay tests              | Verify event replay is safe where needed            |

Example event handler test:

```ts
describe("handlePaymentAuthorized", () => {
  it("marks order as payment authorized and emits event", async () => {
    const event = {
      eventId: "evt_payment_123",
      eventType: "PaymentAuthorized",
      correlationId: "corr_001",
      data: {
        orderId: "ord_456",
        paymentId: "pay_789"
      }
    };

    await handlePaymentAuthorized(event);

    const order = await orderRepository.findById("ord_456");

    expect(order.paymentStatus).toBe("AUTHORIZED");

    expect(outboxRepository).toContainEvent("OrderPaymentRecorded");
  });

  it("ignores duplicate events", async () => {
    const event = makePaymentAuthorizedEvent();

    await handlePaymentAuthorized(event);
    await handlePaymentAuthorized(event);

    const processed = await processedEventRepository.count(event.eventId);

    expect(processed).toBe(1);
  });
});
```

Test duplicate handling explicitly.

---

#### When to use it

Use choreography when:

* multiple services need to react to the same business event,
* reactions are mostly independent,
* the publisher should not know all consumers,
* new consumers may be added over time,
* loose coupling is more important than central workflow visibility,
* eventual consistency is acceptable,
* each service can own its own local reaction,
* event contracts are well governed,
* observability is mature.

Common examples:

* notifications after business events,
* analytics pipelines,
* search indexing,
* loyalty points after purchases,
* audit logging,
* cache invalidation,
* inventory updates after orders,
* payment and inventory reactions to order creation,
* data synchronization across bounded contexts.

---

#### When not to use it

Avoid choreography when:

* the workflow requires strict central control,
* the business process must be easy to see in one place,
* the steps are strongly sequential,
* failure handling is complex,
* compensation must be carefully coordinated,
* event ownership is unclear,
* the team lacks observability and DLQ practices,
* consumers are likely to depend on undocumented event behavior,
* eventual consistency is unacceptable.

For example, a complex loan approval workflow with many conditional steps, manual review, deadlines, and strict audit requirements may be better with orchestration or a workflow engine.

Choreography works best for independent reactions. It becomes difficult when used for highly stateful, tightly controlled processes.

---

#### Benefits

**1. Loose coupling**

Publishers do not need to know every consumer.

**2. Service autonomy**

Each service owns its own reaction to events.

**3. Easy to add new consumers**

New services can subscribe to existing events without changing the publisher.

**4. Scalable fan-out**

Many consumers can react to one event.

**5. Good for side effects**

Notifications, analytics, search indexing, and audit logging work well.

**6. Supports event-driven architecture**

Services communicate through business facts rather than direct commands.

**7. Reduces central bottlenecks**

There is no single orchestrator that must be changed for every reaction.

---

#### Trade-offs

**1. Workflow visibility is weaker**

The business process is distributed across many event handlers.

**2. Debugging is harder**

Failures may happen later and in different services.

**3. Eventual consistency is normal**

The system may pass through intermediate states.

**4. Event contracts require governance**

Publishers must not break consumers.

**5. Idempotency is required**

Consumers must handle duplicate events.

**6. Ordering can be difficult**

Consumers must understand ordering guarantees and limitations.

**7. Failure handling is distributed**

Retries, DLQs, and compensations may be spread across services.

**8. Event loops are possible**

Services can accidentally trigger each other repeatedly.

---

#### Common mistakes

**Mistake 1: No event catalog**

If no one knows which events exist or who consumes them, the system becomes event soup.

**Mistake 2: Treating events like commands**

Events should describe facts. Commands tell a service to do something.

**Mistake 3: No idempotency**

Duplicate events will eventually happen.

**Mistake 4: No correlation IDs**

Without correlation IDs, workflows are hard to trace.

**Mistake 5: Assuming ordering without guarantees**

Ordering must be designed, usually by partition key or aggregate version.

**Mistake 6: No DLQ ownership**

Dead-letter queues need owners, alerts, and replay or repair procedures.

**Mistake 7: Hiding critical workflows in event handlers**

Highly controlled workflows may need orchestration instead.

**Mistake 8: Publishing events unreliably**

Use the Outbox Pattern or equivalent reliability mechanism.

**Mistake 9: Letting temporary consumers become permanent dependencies**

Consumers should be documented and owned.

---

#### Practical design checklist

Before using choreography, ask:

* What business event starts the workflow?
* Which service owns and publishes that event?
* Which services consume the event?
* Are the consumers independent?
* Does the publisher need to know the consumers?
* Is eventual consistency acceptable?
* What events are produced by each reaction?
* Are events facts rather than commands?
* Is there an event catalog?
* Who owns each event schema?
* How are schema changes governed?
* Are consumers idempotent?
* Can events be delivered out of order?
* What ordering guarantees are needed?
* What is the partition key?
* What happens when a consumer fails?
* What is the retry policy?
* What is the DLQ policy?
* Who owns DLQ monitoring?
* How are correlation IDs propagated?
* How will operators see workflow progress?
* Are compensating actions needed?
* Would orchestration be clearer?

A choreography design is probably healthy if:

* events represent real business facts,
* publishers do not know all consumers,
* each consumer owns its local reaction,
* event contracts are documented,
* consumers are idempotent,
* retries and DLQs are defined,
* workflow progress is observable,
* eventual consistency is acceptable,
* no central middleware owns business logic.

A choreography design is probably unhealthy if:

* no one can explain the full workflow,
* events are named like commands,
* duplicate events cause duplicate side effects,
* DLQs are ignored,
* event schemas change without review,
* critical business processes are hidden in many handlers,
* consumers depend on undocumented event timing,
* event loops occur,
* operators cannot tell where a workflow is stuck.

---

#### Related patterns

| Pattern                     | Relationship                                                            |
| --------------------------- | ----------------------------------------------------------------------- |
| Async Messaging             | Choreography usually relies on async messages, topics, or event streams |
| Event-Driven Architecture   | Choreography is one major event-driven workflow style                   |
| Saga                        | A saga can be implemented through choreography and compensating events  |
| Outbox Pattern              | Ensures events are published reliably after local state changes         |
| CQRS                        | Choreographed events often feed read models                             |
| Event Sourcing              | Event-sourced systems naturally publish domain events                   |
| Smart Endpoints, Dumb Pipes | Services react intelligently; broker stays simple                       |
| Orchestration               | Alternative workflow style with central coordination                    |
| Dead Letter Queue           | Captures events that consumers cannot process                           |
| Consumer-Driven Contracts   | Helps protect event consumers from breaking schema changes              |
| Distributed Tracing         | Critical for understanding event-driven workflows                       |

---

#### Summary

Choreography is a workflow style where services react to events and independently decide what to do next.

The central idea is:

> No central coordinator controls the whole workflow. Services publish facts, and other services react.

Choreography is useful when multiple services need to respond independently to business events, especially for notifications, analytics, search indexing, audit logging, loyalty, and loosely coupled workflow steps.

A good choreographed system has:

* well-named business events,
* clear event ownership,
* idempotent consumers,
* reliable publishing,
* schema governance,
* retries and DLQs,
* correlation IDs,
* workflow observability,
* and documented event flows.

The main risk is that the workflow becomes hard to understand because logic is distributed across services. Choreography gives autonomy, but it requires discipline. Without event catalogs, tracing, and ownership, it can turn into an invisible network of side effects.

---

### 19. Saga Pattern

#### What it is

The **Saga Pattern** coordinates a distributed business transaction across multiple services by breaking the transaction into a sequence of **local transactions**.

Each service performs its own local transaction against its own database. If a later step fails, the saga executes **compensating actions** to undo, reverse, or neutralize the earlier successful steps.

The central idea is:

> Instead of one global transaction across many services, use a sequence of local transactions plus compensation.

For example, placing an order may involve several services:

```mermaid
flowchart TD
    Start[Start Order Placement]

    Order[Create Order]
    Payment[Authorize Payment]
    Inventory[Reserve Inventory]
    Shipping[Create Shipment Request]

    Done[Order Confirmed]

    Start --> Order
    Order --> Payment
    Payment --> Inventory
    Inventory --> Shipping
    Shipping --> Done
```

Each step is owned by a different service:

| Step              | Owning service    | Local transaction                  |
| ----------------- | ----------------- | ---------------------------------- |
| Create order      | Order Service     | Insert order with status `PENDING` |
| Authorize payment | Payment Service   | Create payment authorization       |
| Reserve inventory | Inventory Service | Create inventory reservation       |
| Create shipment   | Shipping Service  | Create shipment request            |
| Confirm order     | Order Service     | Update order status to `CONFIRMED` |

If everything succeeds, the saga completes.

If something fails, the saga runs compensation:

```mermaid
flowchart TD
    Start[Start Order Placement]

    Order[Create Order]
    Payment[Authorize Payment]
    Inventory[Reserve Inventory]
    InventoryFail[Inventory Reservation Failed]

    VoidPayment[Void Payment Authorization]
    CancelOrder[Cancel Order]

    Start --> Order
    Order --> Payment
    Payment --> Inventory
    Inventory --> InventoryFail

    InventoryFail --> VoidPayment
    VoidPayment --> CancelOrder
```

The system does not roll back one global database transaction. Instead, it performs business-level recovery actions.

---

#### Why this pattern exists

In a monolith, a business operation can often use one database transaction.

For example:

```sql
BEGIN;

INSERT INTO orders (...);
INSERT INTO payment_authorizations (...);
UPDATE inventory SET available_quantity = available_quantity - 1;
INSERT INTO shipment_requests (...);

COMMIT;
```

If anything fails, the database can roll back all changes.

That works when all data is in one database.

In microservices, each service usually owns its own database:

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]
    ShippingService[Shipping Service]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]
    InventoryDB[(Inventory DB)]
    ShippingDB[(Shipping DB)]

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    InventoryService --> InventoryDB
    ShippingService --> ShippingDB
```

There is no simple single transaction that safely commits across all databases.

A global distributed transaction, such as a two-phase commit, can be used in some systems, but it is often avoided in microservice architectures because it can:

* tightly couple services,
* reduce availability,
* require all participants to coordinate at the same time,
* hold locks across service boundaries,
* make failure recovery difficult,
* limit independent deployment,
* make scaling harder.

The Saga Pattern exists because business workflows still need consistency, even when data is distributed.

It gives you a way to say:

> Each service commits its own local state. If the overall workflow cannot complete, execute compensating actions to bring the business process to an acceptable final state.

---

#### What it solves

The Saga Pattern solves the problem of **distributed business consistency without distributed database transactions**.

Suppose order placement requires:

1. Creating an order.
2. Authorizing payment.
3. Reserving inventory.
4. Creating a shipment.
5. Confirming the order.

If step 3 fails after step 2 succeeds, the system cannot simply roll back the Payment Service’s database from the Order Service.

The Payment Service already committed its local transaction.

So the system needs a compensating action:

```mermaid
flowchart TD
    PaymentAuthorized[Payment Authorized]
    InventoryFailed[Inventory Reservation Failed]

    Compensation[Void Payment Authorization]

    PaymentAuthorized --> InventoryFailed
    InventoryFailed --> Compensation
```

A saga makes this explicit.

It defines:

* the forward steps,
* the local transaction for each step,
* the failure conditions,
* the compensating action for each completed step,
* the final success state,
* the final failure state.

A saga is not about pretending distributed systems are atomic. It is about designing the recovery path clearly.

---

#### Local transactions

A **local transaction** is a normal transaction inside one service boundary.

For example, Inventory Service may reserve stock using a local database transaction:

```ts
type InventoryReservation = {
  reservationId: string;
  orderId: string;
  productId: string;
  quantity: number;
  status: "ACTIVE" | "RELEASED" | "COMMITTED";
};

async function reserveInventory(
  db: Database,
  command: {
    orderId: string;
    productId: string;
    quantity: number;
  }
): Promise<InventoryReservation> {
  return db.transaction(async (tx) => {
    const item = await tx.inventory.findByProductIdForUpdate(
      command.productId
    );

    if (!item) {
      throw new Error("INVENTORY_ITEM_NOT_FOUND");
    }

    if (item.availableQuantity < command.quantity) {
      throw new Error("INSUFFICIENT_INVENTORY");
    }

    await tx.inventory.update(command.productId, {
      availableQuantity: item.availableQuantity - command.quantity
    });

    const reservation = await tx.reservations.insert({
      reservationId: crypto.randomUUID(),
      orderId: command.orderId,
      productId: command.productId,
      quantity: command.quantity,
      status: "ACTIVE"
    });

    return reservation;
  });
}
```

This transaction is local to Inventory Service. It does not update the Order database, Payment database, or Shipping database.

That is the point.

Each service owns its own data and commits its own changes.

---

#### Compensating actions

A **compensating action** is a business operation that reverses, offsets, or neutralizes a previous local transaction.

For example:

| Completed action        | Compensation                      |
| ----------------------- | --------------------------------- |
| Create pending order    | Cancel order                      |
| Authorize payment       | Void authorization                |
| Capture payment         | Refund payment                    |
| Reserve inventory       | Release inventory reservation     |
| Create shipment request | Cancel shipment request           |
| Activate subscription   | Deactivate subscription           |
| Book hotel room         | Cancel hotel booking              |
| Book flight             | Cancel flight booking, if allowed |

Compensation is not always a perfect undo.

For example, refunding a captured payment is not the same as the payment never happening. It may create fees, delays, audit records, or customer-visible activity.

That is why saga design is a business design problem, not just a technical pattern.

```mermaid
flowchart TD
    Forward[Forward Transaction]
    Compensation[Compensating Action]

    Forward -->|does work| BusinessState[Business State Changed]
    Compensation -->|attempts to reverse or offset| RecoveredState[Acceptable Recovery State]
```

The goal is not always to return the world to exactly the previous state. The goal is to reach a valid business state.

---

#### Example: order placement saga

A typical order placement saga may look like this:

```mermaid
flowchart TD
    Start[Start Saga]

    CreateOrder[Create Pending Order]
    AuthorizePayment[Authorize Payment]
    ReserveInventory[Reserve Inventory]
    ConfirmOrder[Confirm Order]

    Success[Order Confirmed]

    CreateOrderFail[Order Creation Failed]
    PaymentFail[Payment Authorization Failed]
    InventoryFail[Inventory Reservation Failed]

    CancelOrder[Cancel Order]
    VoidPayment[Void Payment]

    Start --> CreateOrder
    CreateOrder --> AuthorizePayment
    AuthorizePayment --> ReserveInventory
    ReserveInventory --> ConfirmOrder
    ConfirmOrder --> Success

    CreateOrder -->|fails| CreateOrderFail

    AuthorizePayment -->|fails| PaymentFail
    PaymentFail --> CancelOrder

    ReserveInventory -->|fails| InventoryFail
    InventoryFail --> VoidPayment
    VoidPayment --> CancelOrder
```

The forward flow is:

1. Create pending order.
2. Authorize payment.
3. Reserve inventory.
4. Confirm order.

The compensation flow is:

* If payment authorization fails, cancel the pending order.
* If inventory reservation fails after payment succeeds, void the payment authorization and cancel the order.
* If confirmation fails, decide whether to retry, cancel, or escalate.

This flow should be explicit and documented.

---

#### Saga state

A saga should usually store its own state.

For example:

```ts
type OrderSagaStatus =
  | "STARTED"
  | "ORDER_CREATED"
  | "PAYMENT_AUTHORIZED"
  | "INVENTORY_RESERVED"
  | "ORDER_CONFIRMED"
  | "COMPENSATING"
  | "COMPENSATED"
  | "FAILED";

type OrderSaga = {
  sagaId: string;
  orderId?: string;
  paymentId?: string;
  reservationId?: string;
  status: OrderSagaStatus;
  failureReason?: string;
  createdAt: string;
  updatedAt: string;
};
```

Saga state helps answer:

* What step is the workflow on?
* Which steps have completed?
* Which compensations are needed?
* Has compensation already started?
* Is the saga stuck?
* Can the saga be retried?
* Does an operator need to intervene?

A saga without state is difficult to debug and recover.

```mermaid
stateDiagram-v2
    [*] --> STARTED
    STARTED --> ORDER_CREATED
    ORDER_CREATED --> PAYMENT_AUTHORIZED
    PAYMENT_AUTHORIZED --> INVENTORY_RESERVED
    INVENTORY_RESERVED --> ORDER_CONFIRMED
    ORDER_CONFIRMED --> [*]

    ORDER_CREATED --> COMPENSATING
    PAYMENT_AUTHORIZED --> COMPENSATING
    INVENTORY_RESERVED --> COMPENSATING

    COMPENSATING --> COMPENSATED
    COMPENSATING --> FAILED
```

---

#### Orchestrated saga

In an **orchestrated saga**, a central saga orchestrator tells each participant what to do.

```mermaid
flowchart TD
    Orchestrator[Order Saga Orchestrator]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    SagaState[(Saga State)]

    Orchestrator --> Orders
    Orchestrator --> Payments
    Orchestrator --> Inventory
    Orchestrator --> Shipping

    Orchestrator --> SagaState
```

The orchestrator owns the workflow sequence.

It sends commands such as:

* `CreateOrder`
* `AuthorizePayment`
* `ReserveInventory`
* `ConfirmOrder`
* `CancelOrder`
* `VoidPayment`
* `ReleaseInventory`

Example sequence:

```mermaid
sequenceDiagram
    participant Client
    participant Saga as Order Saga Orchestrator
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service

    Client->>Saga: Place order

    Saga->>Orders: Create pending order
    Orders-->>Saga: Order created

    Saga->>Payments: Authorize payment
    Payments-->>Saga: Payment authorized

    Saga->>Inventory: Reserve inventory
    Inventory-->>Saga: Inventory reserved

    Saga->>Orders: Confirm order
    Orders-->>Saga: Order confirmed

    Saga-->>Client: Order confirmed
```

If inventory fails:

```mermaid
sequenceDiagram
    participant Saga as Order Saga Orchestrator
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service

    Saga->>Orders: Create pending order
    Orders-->>Saga: Order created

    Saga->>Payments: Authorize payment
    Payments-->>Saga: Payment authorized

    Saga->>Inventory: Reserve inventory
    Inventory-->>Saga: Inventory unavailable

    Saga->>Payments: Void payment authorization
    Payments-->>Saga: Payment voided

    Saga->>Orders: Cancel order
    Orders-->>Saga: Order cancelled
```

Orchestrated sagas are easier to understand because the workflow is visible in one place.

The main risk is that the orchestrator can become too powerful if it starts owning business rules that belong inside domain services.

---

#### Orchestrated saga implementation

A simplified orchestrated saga might look like this:

```ts
class OrderSagaOrchestrator {
  constructor(
    private readonly sagaStore: SagaStore,
    private readonly orderClient: OrderClient,
    private readonly paymentClient: PaymentClient,
    private readonly inventoryClient: InventoryClient
  ) {}

  async placeOrder(command: PlaceOrderCommand): Promise<void> {
    const saga = await this.sagaStore.create({
      sagaId: crypto.randomUUID(),
      status: "STARTED"
    });

    try {
      const order = await this.orderClient.createPendingOrder({
        customerId: command.customerId,
        items: command.items
      });

      await this.sagaStore.update(saga.sagaId, {
        orderId: order.orderId,
        status: "ORDER_CREATED"
      });

      const payment = await this.paymentClient.authorizePayment({
        orderId: order.orderId,
        amount: order.totalAmount,
        paymentMethodId: command.paymentMethodId
      });

      await this.sagaStore.update(saga.sagaId, {
        paymentId: payment.paymentId,
        status: "PAYMENT_AUTHORIZED"
      });

      const reservation = await this.inventoryClient.reserveInventory({
        orderId: order.orderId,
        items: command.items
      });

      await this.sagaStore.update(saga.sagaId, {
        reservationId: reservation.reservationId,
        status: "INVENTORY_RESERVED"
      });

      await this.orderClient.confirmOrder(order.orderId);

      await this.sagaStore.update(saga.sagaId, {
        status: "ORDER_CONFIRMED"
      });
    } catch (error) {
      await this.compensate(saga.sagaId, error);
      throw error;
    }
  }

  private async compensate(sagaId: string, error: unknown): Promise<void> {
    const saga = await this.sagaStore.findById(sagaId);

    await this.sagaStore.update(sagaId, {
      status: "COMPENSATING",
      failureReason: error instanceof Error ? error.message : "UNKNOWN"
    });

    if (saga.paymentId) {
      await this.paymentClient.voidAuthorization(saga.paymentId);
    }

    if (saga.orderId) {
      await this.orderClient.cancelOrder(saga.orderId);
    }

    await this.sagaStore.update(sagaId, {
      status: "COMPENSATED"
    });
  }
}
```

This example is intentionally simplified.

A production saga needs:

* idempotency,
* retries,
* timeouts,
* compensation retries,
* observability,
* safe persistence,
* recovery after orchestrator crash,
* manual intervention for stuck states.

---

#### Choreographed saga

In a **choreographed saga**, there is no central orchestrator. Services publish events and react to events.

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Payments[Payment Service]
    Inventory[Inventory Service]
    Shipping[Shipping Service]

    Orders -->|OrderCreated| Bus

    Bus --> Payments
    Payments -->|PaymentAuthorized| Bus

    Bus --> Inventory
    Inventory -->|InventoryReserved| Bus

    Bus --> Orders
    Orders -->|OrderConfirmed| Bus

    Bus --> Shipping
```

Each service owns its local transaction and publishes events when something happens.

Example:

1. Order Service creates order and publishes `OrderCreated`.
2. Payment Service reacts and publishes `PaymentAuthorized` or `PaymentFailed`.
3. Inventory Service reacts and publishes `InventoryReserved` or `InventoryReservationFailed`.
4. Order Service reacts to the outcomes and confirms or cancels the order.

Failure flow:

```mermaid
flowchart TD
    Orders[Order Service]
    Bus[(Event Bus)]

    Payments[Payment Service]
    Inventory[Inventory Service]

    Orders -->|OrderCreated| Bus
    Bus --> Payments
    Payments -->|PaymentAuthorized| Bus

    Bus --> Inventory
    Inventory -->|InventoryReservationFailed| Bus

    Bus --> Payments
    Payments -->|PaymentAuthorizationVoided| Bus

    Bus --> Orders
    Orders -->|OrderCancelled| Bus
```

Choreographed sagas support loose coupling, but the workflow is distributed across services. That makes visibility and debugging harder.

---

#### Orchestration vs choreography for sagas

| Question                 | Orchestrated saga                  | Choreographed saga                         |
| ------------------------ | ---------------------------------- | ------------------------------------------ |
| Where is workflow logic? | In an orchestrator                 | Spread across event handlers               |
| Easier to understand?    | Usually yes                        | Often harder                               |
| Coupling style           | Orchestrator depends on services   | Services depend on events                  |
| Adding side effects      | May require orchestrator change    | Add new event subscriber                   |
| Failure handling         | Centralized                        | Distributed                                |
| Risk                     | Orchestrator becomes a god service | Workflow becomes invisible                 |
| Best for                 | Complex, sequential workflows      | Independent reactions and looser workflows |

Use orchestration when the business process needs clear control and visibility.

Use choreography when services can react independently to events and the workflow does not require one central decision-maker.

Many systems use both.

For example:

* Checkout may use an orchestrated saga.
* Notifications, analytics, loyalty, and search indexing may use choreography after the order is confirmed.

---

#### Saga participants

A saga participant is a service that performs a local transaction as part of the saga.

A participant should expose operations that are:

* well-defined,
* idempotent,
* locally transactional,
* compensatable when needed,
* observable,
* owned by that service.

For example, Payment Service may expose:

```http
POST /payment-authorizations
POST /payment-authorizations/{paymentId}/void
```

Inventory Service may expose:

```http
POST /inventory-reservations
POST /inventory-reservations/{reservationId}/release
POST /inventory-reservations/{reservationId}/commit
```

Order Service may expose:

```http
POST /orders
POST /orders/{orderId}/confirm
POST /orders/{orderId}/cancel
```

Each service owns its own business rules.

The saga coordinates the workflow, but the participant decides whether its local operation is valid.

---

#### Idempotency

Sagas must be idempotent because steps may be retried.

For example, the orchestrator may send `AuthorizePayment`, but the response times out. The payment may have succeeded, but the orchestrator does not know.

If the orchestrator retries, Payment Service must not create duplicate authorizations.

Use idempotency keys:

```http
POST /payment-authorizations
Idempotency-Key: saga_123_authorize_payment
Content-Type: application/json

{
  "orderId": "ord_456",
  "amount": 129.99,
  "currency": "USD"
}
```

Payment Service should return the original result if the same idempotency key is seen again.

```ts
async function authorizePayment(
  command: AuthorizePaymentCommand,
  idempotencyKey: string
): Promise<PaymentAuthorization> {
  const existing = await idempotencyStore.find(idempotencyKey);

  if (existing) {
    return existing.response as PaymentAuthorization;
  }

  const authorization = await paymentGateway.authorize(command);

  await idempotencyStore.save({
    key: idempotencyKey,
    response: authorization,
    createdAt: new Date()
  });

  return authorization;
}
```

Every saga command that changes state should be designed for safe retries.

---

#### Compensation must also be idempotent

Compensating actions can also be retried.

For example, if `VoidPaymentAuthorization` times out, the saga may send it again.

That must be safe.

```ts
async function voidAuthorization(paymentId: string): Promise<void> {
  const payment = await paymentRepository.findById(paymentId);

  if (!payment) {
    throw new Error("PAYMENT_NOT_FOUND");
  }

  if (payment.status === "VOIDED") {
    return;
  }

  if (payment.status !== "AUTHORIZED") {
    throw new Error("PAYMENT_CANNOT_BE_VOIDED");
  }

  await paymentGateway.voidAuthorization(payment.gatewayAuthorizationId);

  await paymentRepository.update(paymentId, {
    status: "VOIDED"
  });
}
```

The compensation checks current state before acting.

That makes repeated compensation safe.

---

#### Timeouts

Sagas need timeouts because some steps may never respond.

Examples:

* payment authorization request times out,
* inventory reservation event is delayed,
* shipping provider is unavailable,
* external verification takes too long,
* a consumer crashes before publishing the next event.

A saga timeout policy defines what happens if the workflow gets stuck.

```mermaid
flowchart TD
    SagaStep[Waiting for PaymentAuthorized]
    Timer[Timeout Timer]

    Received[Event Received]
    Timeout[Timeout Expired]

    Continue[Continue Saga]
    Compensate[Start Compensation]

    SagaStep --> Timer

    Timer --> Received
    Timer --> Timeout

    Received --> Continue
    Timeout --> Compensate
```

Example timeout states:

```ts
type SagaTimeoutPolicy = {
  step: "PAYMENT_AUTHORIZATION";
  timeoutMs: number;
  onTimeout: "RETRY" | "COMPENSATE" | "ESCALATE";
};
```

Timeouts should be business-aware.

For example:

* Payment authorization might time out after seconds.
* Manual identity verification might time out after days.
* Loan approval might have a multi-day review period.
* Hotel booking might need immediate compensation if another booking fails.

---

#### Retries

Sagas need retries for transient failures.

Retryable failures:

* network timeout,
* temporary database error,
* broker unavailable,
* external provider temporarily down,
* rate limit that can be retried later.

Non-retryable failures:

* invalid request,
* insufficient inventory,
* card declined,
* customer not eligible,
* schema validation failure,
* forbidden operation.

A retry policy might look like this:

```yaml
saga:
  steps:
    authorizePayment:
      maxAttempts: 3
      backoff:
        type: exponential
        initialDelayMs: 500
        maxDelayMs: 5000

    reserveInventory:
      maxAttempts: 2
      backoff:
        type: fixed
        delayMs: 1000
```

Retries should have limits. Infinite retries can create stuck workflows and overload dependencies.

If retries are exhausted, the saga should compensate or escalate.

---

#### Compensation ordering

Compensation usually happens in reverse order.

Forward flow:

```mermaid
flowchart LR
    A[Create Order] --> B[Authorize Payment] --> C[Reserve Inventory] --> D[Create Shipment]
```

Compensation flow:

```mermaid
flowchart LR
    D2[Cancel Shipment] --> C2[Release Inventory] --> B2[Void Payment] --> A2[Cancel Order]
```

Why reverse order?

Because later steps often depend on earlier steps.

If shipment was created after inventory was reserved, cancel shipment before releasing inventory. If inventory was reserved after payment authorization, release inventory before voiding payment may or may not be correct depending on the business. The key is to define the right recovery sequence.

Example table:

| Forward step      | Compensation        | Compensation order               |
| ----------------- | ------------------- | -------------------------------- |
| Create order      | Cancel order        | Last                             |
| Authorize payment | Void authorization  | After inventory/shipping cleanup |
| Reserve inventory | Release reservation | Before cancelling order          |
| Create shipment   | Cancel shipment     | First                            |

Compensation order is a business decision.

---

#### Compensation is not always possible

Some actions cannot be perfectly undone.

Examples:

| Action                  | Why compensation is hard                |
| ----------------------- | --------------------------------------- |
| Send email              | Customer may have already read it       |
| Capture payment         | Refund may take days and fees may apply |
| Book flight             | Cancellation may have penalties         |
| Ship package            | Package may already be in transit       |
| Issue gift card         | Customer may have used it               |
| Create legal document   | Audit and compliance records remain     |
| Notify external partner | Partner may have acted on it            |

For these cases, compensation may mean:

* issue refund,
* create correction event,
* notify customer,
* open manual review,
* reverse accounting entry,
* mark record as cancelled,
* create audit trail,
* perform operational repair.

A saga must model the real business world, not just database state.

---

#### Pivot transaction

Some saga designs identify a **pivot transaction**.

A pivot transaction is the point after which the saga should usually move forward rather than compensate backward.

For example:

```mermaid
flowchart TD
    Start[Start]
    Reserve[Reserve Inventory]
    Authorize[Authorize Payment]
    Capture[Capture Payment]
    Ship[Ship Order]

    Start --> Reserve
    Reserve --> Authorize
    Authorize --> Capture
    Capture --> Ship

    Capture --> Pivot[Pivot Point]
```

Before capturing payment, compensation might be easy:

* release inventory,
* void authorization,
* cancel order.

After capturing payment or shipping, compensation may become more expensive:

* refund payment,
* process return,
* contact customer,
* reconcile accounting.

Identifying the pivot helps design recovery rules.

---

#### Saga state machine

A saga can be modeled as a state machine.

```mermaid
stateDiagram-v2
    [*] --> Pending

    Pending --> PaymentAuthorized
    Pending --> Failed: payment failed

    PaymentAuthorized --> InventoryReserved
    PaymentAuthorized --> Compensating: inventory failed

    InventoryReserved --> Confirmed
    InventoryReserved --> Compensating: confirmation failed

    Confirmed --> [*]

    Compensating --> Compensated
    Compensating --> CompensationFailed

    Compensated --> [*]
    CompensationFailed --> ManualReview
```

State machines are useful because they make allowed transitions explicit.

Example:

```ts
type SagaStatus =
  | "PENDING"
  | "PAYMENT_AUTHORIZED"
  | "INVENTORY_RESERVED"
  | "CONFIRMED"
  | "COMPENSATING"
  | "COMPENSATED"
  | "COMPENSATION_FAILED"
  | "MANUAL_REVIEW";

function transition(
  current: SagaStatus,
  event: SagaEvent
): SagaStatus {
  switch (current) {
    case "PENDING":
      if (event.type === "PAYMENT_AUTHORIZED") {
        return "PAYMENT_AUTHORIZED";
      }
      if (event.type === "PAYMENT_FAILED") {
        return "COMPENSATED";
      }
      break;

    case "PAYMENT_AUTHORIZED":
      if (event.type === "INVENTORY_RESERVED") {
        return "INVENTORY_RESERVED";
      }
      if (event.type === "INVENTORY_FAILED") {
        return "COMPENSATING";
      }
      break;

    case "INVENTORY_RESERVED":
      if (event.type === "ORDER_CONFIRMED") {
        return "CONFIRMED";
      }
      if (event.type === "CONFIRMATION_FAILED") {
        return "COMPENSATING";
      }
      break;
  }

  throw new Error(`Invalid transition from ${current} on ${event.type}`);
}
```

A state machine prevents impossible workflow states.

---

#### Saga with async messaging

Sagas often use async messaging.

```mermaid
flowchart TD
    Saga[Order Saga]
    Broker[(Message Broker)]

    Orders[Order Service]
    Payments[Payment Service]
    Inventory[Inventory Service]

    Saga -->|CreateOrder command| Broker
    Broker --> Orders

    Orders -->|OrderCreated event| Broker
    Broker --> Saga

    Saga -->|AuthorizePayment command| Broker
    Broker --> Payments

    Payments -->|PaymentAuthorized event| Broker
    Broker --> Saga

    Saga -->|ReserveInventory command| Broker
    Broker --> Inventory

    Inventory -->|InventoryReserved event| Broker
    Broker --> Saga
```

This makes the saga resilient to temporary service outages, but it also adds complexity:

* duplicate messages,
* out-of-order messages,
* retries,
* DLQs,
* idempotency,
* message schema evolution,
* stuck workflow detection.

Async sagas need strong observability and durable saga state.

---

#### Saga with synchronous calls

A saga can also use synchronous calls.

```mermaid
sequenceDiagram
    participant Saga as Saga Orchestrator
    participant Orders as Order Service
    participant Payments as Payment Service
    participant Inventory as Inventory Service

    Saga->>Orders: Create order
    Orders-->>Saga: Created

    Saga->>Payments: Authorize payment
    Payments-->>Saga: Authorized

    Saga->>Inventory: Reserve inventory
    Inventory-->>Saga: Reserved

    Saga->>Orders: Confirm order
    Orders-->>Saga: Confirmed
```

This is simpler to implement, but the saga is more sensitive to runtime availability and latency.

If Inventory Service is down, the saga fails immediately or waits for retries.

A synchronous saga works best when:

* steps are short,
* dependencies are reliable,
* response time matters,
* there are few participants,
* failure behavior is simple.

An async saga works better for longer-running workflows.

---

#### Example: travel booking saga

Travel booking is a classic saga example.

A trip booking may require:

1. Reserve flight.
2. Reserve hotel.
3. Reserve rental car.
4. Charge customer.
5. Confirm booking.

```mermaid
flowchart TD
    Start[Start Trip Booking]

    Flight[Reserve Flight]
    Hotel[Reserve Hotel]
    Car[Reserve Rental Car]
    Payment[Charge Customer]
    Confirm[Confirm Trip]

    Success[Trip Booked]

    Start --> Flight
    Flight --> Hotel
    Hotel --> Car
    Car --> Payment
    Payment --> Confirm
    Confirm --> Success
```

If hotel reservation fails after flight reservation succeeds:

```mermaid
flowchart TD
    Flight[Flight Reserved]
    HotelFail[Hotel Reservation Failed]

    CancelFlight[Cancel Flight Reservation]
    CancelTrip[Cancel Trip Booking]

    Flight --> HotelFail
    HotelFail --> CancelFlight
    CancelFlight --> CancelTrip
```

If payment fails after flight, hotel, and car are reserved:

```mermaid
flowchart TD
    Flight[Flight Reserved]
    Hotel[Hotel Reserved]
    Car[Car Reserved]
    PaymentFail[Payment Failed]

    CancelCar[Cancel Car]
    CancelHotel[Cancel Hotel]
    CancelFlight[Cancel Flight]

    Flight --> Hotel
    Hotel --> Car
    Car --> PaymentFail

    PaymentFail --> CancelCar
    CancelCar --> CancelHotel
    CancelHotel --> CancelFlight
```

This example shows why compensation order matters.

It also shows why compensation may not be perfect. Airlines, hotels, and rental car providers may have different cancellation policies.

---

#### Example: subscription activation saga

A subscription activation workflow may involve:

1. Create subscription.
2. Charge payment.
3. Provision account.
4. Enable entitlements.
5. Send welcome email.

```mermaid
flowchart TD
    Start[Start Activation]

    Subscription[Create Subscription]
    Payment[Charge Payment]
    Provision[Provision Account]
    Entitlements[Enable Entitlements]
    Email[Send Welcome Email]

    Active[Subscription Active]

    Start --> Subscription
    Subscription --> Payment
    Payment --> Provision
    Provision --> Entitlements
    Entitlements --> Email
    Email --> Active
```

Failure cases:

| Failure                      | Compensation                                        |
| ---------------------------- | --------------------------------------------------- |
| Payment fails                | Cancel subscription                                 |
| Provisioning fails           | Refund or void payment, cancel subscription         |
| Entitlement activation fails | Disable provisioned account, refund or escalate     |
| Email fails                  | Retry email, do not necessarily cancel subscription |

Notice that not every failure requires cancelling everything.

If welcome email fails, the subscription may still be active. The correct action may be to retry email later.

A good saga distinguishes critical steps from non-critical side effects.

---

#### Critical vs non-critical steps

Not every step belongs inside the saga’s consistency boundary.

For example, in order placement:

Critical:

* create order,
* authorize payment,
* reserve inventory,
* confirm order.

Non-critical:

* send confirmation email,
* update analytics,
* award loyalty points,
* index order for search.

Non-critical side effects can often happen after the saga completes through events.

```mermaid
flowchart TD
    Saga[Order Placement Saga]
    Confirmed[Order Confirmed]
    Bus[(Event Bus)]

    Email[Notification Service]
    Analytics[Analytics Service]
    Loyalty[Loyalty Service]

    Saga --> Confirmed
    Confirmed -->|OrderConfirmed event| Bus

    Bus --> Email
    Bus --> Analytics
    Bus --> Loyalty
```

This keeps the saga focused.

Do not make the saga fail just because analytics or email failed, unless the business truly requires it.

---

#### Observability

Sagas need strong observability because workflows can span many services and time periods.

Track:

* saga ID,
* current saga state,
* completed steps,
* failed steps,
* compensation status,
* retry count,
* timeout count,
* participant latency,
* stuck saga count,
* compensation failure count,
* manual intervention count,
* business outcome.

Example saga log:

```json
{
  "sagaId": "saga_123",
  "sagaType": "OrderPlacement",
  "orderId": "ord_456",
  "status": "PAYMENT_AUTHORIZED",
  "step": "ReserveInventory",
  "attempt": 1,
  "correlationId": "corr_789",
  "timestamp": "2026-04-29T12:00:00Z"
}
```

Example compensation log:

```json
{
  "sagaId": "saga_123",
  "sagaType": "OrderPlacement",
  "status": "COMPENSATING",
  "compensationStep": "VoidPaymentAuthorization",
  "paymentId": "pay_456",
  "attempt": 2,
  "result": "SUCCESS"
}
```

Operators should be able to answer:

* Which sagas are currently running?
* Which sagas are stuck?
* Which step failed?
* Which compensations have run?
* Which compensations failed?
* Which sagas require manual intervention?

---

#### Manual intervention

Some saga failures cannot be fully automated.

Examples:

* payment was captured but refund failed,
* shipment was created but carrier cancellation failed,
* hotel booking cannot be cancelled automatically,
* external partner accepted a request but returned no confirmation,
* compensation repeatedly fails,
* data inconsistency is detected after completion.

For these cases, design a manual review state.

```mermaid
stateDiagram-v2
    [*] --> Running
    Running --> Compensating
    Compensating --> Compensated
    Compensating --> ManualReview: compensation failed repeatedly
    ManualReview --> Resolved
    Resolved --> [*]
```

Manual review should include:

* complete saga history,
* completed steps,
* failed steps,
* attempted compensations,
* external reference IDs,
* recommended operator actions,
* audit trail.

A saga is not production-ready if there is no plan for stuck or partially compensated workflows.

---

#### Testing sagas

Saga testing must cover both success and failure paths.

Useful tests include:

| Test type                  | Purpose                                          |
| -------------------------- | ------------------------------------------------ |
| Happy path tests           | Verify all steps complete                        |
| Step failure tests         | Verify compensation starts                       |
| Compensation tests         | Verify completed steps are compensated correctly |
| Compensation failure tests | Verify manual review or retry behavior           |
| Timeout tests              | Verify stuck steps are handled                   |
| Idempotency tests          | Verify duplicate commands/events are safe        |
| Retry tests                | Verify transient failures are retried            |
| State transition tests     | Verify invalid transitions are rejected          |
| Recovery tests             | Verify saga can resume after orchestrator crash  |

Example test:

```ts
describe("OrderPlacementSaga", () => {
  it("voids payment and cancels order when inventory reservation fails", async () => {
    orderClient.createPendingOrder.mockResolvedValue({
      orderId: "ord_123",
      totalAmount: 129.99
    });

    paymentClient.authorizePayment.mockResolvedValue({
      paymentId: "pay_123"
    });

    inventoryClient.reserveInventory.mockRejectedValue(
      new Error("INSUFFICIENT_INVENTORY")
    );

    await expect(
      saga.placeOrder(makePlaceOrderCommand())
    ).rejects.toThrow("INSUFFICIENT_INVENTORY");

    expect(paymentClient.voidAuthorization).toHaveBeenCalledWith("pay_123");
    expect(orderClient.cancelOrder).toHaveBeenCalledWith("ord_123");
  });
});
```

Do not test only the happy path. Most saga complexity is in failure handling.

---

#### When to use it

Use the Saga Pattern when:

* a business workflow spans multiple services,
* each service owns its own database,
* a global distributed transaction is undesirable,
* each step can be committed locally,
* failure requires business-level recovery,
* compensation is possible or at least manageable,
* eventual consistency is acceptable,
* workflow progress needs to be tracked,
* services need to remain autonomous.

Common use cases:

* order placement,
* payment authorization,
* inventory reservation,
* shipment creation,
* travel booking,
* subscription activation,
* customer onboarding,
* loan approval,
* insurance claims,
* refund processing,
* identity verification,
* account provisioning.

---

#### When not to use it

Avoid or reconsider sagas when:

* the operation is simple and local to one service,
* one service can own the whole transaction safely,
* immediate strong consistency is required,
* compensation is impossible and failure cannot be tolerated,
* the team cannot operate distributed workflows,
* the business does not accept intermediate states,
* a modular monolith would be simpler,
* the workflow is mostly read-only,
* the process does not need coordinated recovery.

For example, updating a user’s display name probably does not need a saga.

It should be a local transaction inside the service that owns user profile data.

---

#### Benefits

**1. Avoids global distributed transactions**

Each service commits its own local transaction.

**2. Preserves service autonomy**

Services keep ownership of their data and business rules.

**3. Supports distributed workflows**

Business processes can span multiple services without sharing databases.

**4. Enables failure recovery**

Compensating actions provide a structured recovery path.

**5. Improves workflow visibility**

Saga state can show where a business process is in progress.

**6. Works with async messaging**

Sagas fit naturally with event-driven systems and queues.

**7. Models real business processes**

Many real-world workflows are not perfectly atomic. Sagas make that explicit.

---

#### Trade-offs

**1. Eventual consistency**

The system may pass through intermediate states before reaching a final state.

**2. Compensation is hard**

Some actions cannot be perfectly undone.

**3. More complex error handling**

Every step needs failure and compensation behavior.

**4. More operational complexity**

Sagas need monitoring, retries, timeouts, and manual recovery.

**5. More state to manage**

The saga itself usually needs durable state.

**6. Business logic can become scattered**

In choreographed sagas, logic may be spread across many event handlers.

**7. Testing is harder**

You must test success, failure, retry, timeout, and compensation paths.

**8. User experience is more complex**

Users may see pending or processing states.

---

#### Common mistakes

**Mistake 1: Treating a saga like an ACID transaction**

A saga is not atomic in the database sense. It is eventually consistent.

**Mistake 2: Ignoring compensation**

Every completed step needs a recovery plan if later steps fail.

**Mistake 3: Assuming compensation is perfect**

Refunding a payment or cancelling a shipment may not fully undo the action.

**Mistake 4: No saga state**

Without durable saga state, debugging and recovery become difficult.

**Mistake 5: No idempotency**

Retries and duplicate messages can create duplicate side effects.

**Mistake 6: No timeout policy**

A saga can wait forever for a response that will never come.

**Mistake 7: No manual recovery path**

Some failures need human intervention.

**Mistake 8: Putting non-critical side effects inside the saga**

Email, analytics, and search indexing often do not belong in the core saga.

**Mistake 9: Letting the orchestrator own domain rules**

The orchestrator coordinates. Domain services should still own their own decisions.

---

#### Practical design checklist

Before designing a saga, answer:

* What business process does the saga represent?
* What is the final success state?
* What are the possible failure states?
* Which services participate?
* What local transaction does each service perform?
* What compensating action exists for each completed step?
* Are compensations idempotent?
* Are forward steps idempotent?
* What is the pivot point, if any?
* Which steps are critical?
* Which side effects can happen after the saga completes?
* Is the saga orchestrated or choreographed?
* Where is saga state stored?
* What events or commands connect the steps?
* What timeout applies to each step?
* What retry policy applies?
* What happens when retries are exhausted?
* What happens if compensation fails?
* What manual intervention process exists?
* How will operators see saga progress?
* How will stuck sagas be detected?
* How will duplicate messages be handled?
* How will event schemas be versioned?
* What should the user see while the saga is pending?

A saga design is probably healthy if:

* every step has a clear owner,
* every local transaction is well defined,
* every failure path has a response,
* compensations are explicit,
* idempotency is designed,
* saga state is durable,
* timeouts and retries are defined,
* observability is strong,
* manual recovery is possible,
* eventual consistency is acceptable.

A saga design is probably unhealthy if:

* compensation is hand-waved,
* no one owns the full workflow,
* services share databases to avoid coordination,
* the user expects instant consistency,
* duplicate messages cause duplicate side effects,
* failures leave workflows stuck forever,
* the orchestrator contains all domain rules,
* operators cannot tell what step failed.

---

#### Related patterns

| Pattern              | Relationship                                                                   |
| -------------------- | ------------------------------------------------------------------------------ |
| Async Messaging      | Often used to carry saga commands and events                                   |
| Choreography         | A saga can be implemented through event choreography                           |
| Orchestration        | A saga can be implemented with a central orchestrator                          |
| Outbox Pattern       | Helps publish saga events reliably after local transactions                    |
| Idempotency Key      | Makes saga commands safe to retry                                              |
| Dead Letter Queue    | Captures saga messages that cannot be processed                                |
| CQRS                 | Read models can expose saga progress to users                                  |
| Event Sourcing       | Can record saga state transitions as events                                    |
| Circuit Breaker      | Protects saga steps from failing dependencies                                  |
| Retry                | Handles transient failures in saga steps                                       |
| Transactional Outbox | Prevents local state changes from being committed without corresponding events |
| Process Manager      | Another name often used for a component that manages long-running workflows    |

---

#### Summary

The Saga Pattern coordinates a distributed business transaction through a sequence of local transactions and compensating actions.

The central idea is:

> Each service commits its own work. If the overall workflow cannot complete, the system performs business-level compensation.

Sagas are useful when a workflow spans multiple services that each own their own data, such as order placement, travel booking, subscription activation, onboarding, payment processing, and inventory reservation.

A good saga has:

* clear workflow ownership,
* durable saga state,
* local transactions,
* explicit compensation,
* idempotent steps,
* retries,
* timeouts,
* observability,
* manual recovery,
* and a user experience that accepts pending states.

The trade-off is eventual consistency. A saga does not make distributed work magically atomic. It makes distributed failure and recovery explicit.


---

### 20. Consumer-Driven Contracts

#### What it is

**Consumer-Driven Contracts**, often abbreviated as **CDC**, are agreements between a service provider and its consumers that describe the behavior the consumers depend on.

A **consumer** is any application, service, frontend, job, or integration that uses an API, event, or message.

A **provider** is the service that exposes that API, event, or message.

The key idea is:

> Consumers define the behavior they require, and providers continuously verify that they still satisfy those expectations.

For example, suppose a Mobile BFF calls the Order Service.

```mermaid
flowchart TD
    Consumer[Mobile BFF<br/>Consumer]
    Provider[Order Service<br/>Provider]

    Consumer -->|GET /orders/{orderId}| Provider
```

The Mobile BFF may depend on the Order Service returning:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD"
}
```

A consumer-driven contract captures that expectation.

The provider then runs tests to prove it still satisfies that contract.

```mermaid
flowchart TD
    Consumer[Consumer]
    Contract[Consumer Contract]
    Provider[Provider]

    Consumer -->|publishes expectations| Contract
    Provider -->|verifies behavior| Contract
```

This prevents the provider from accidentally making a breaking change, such as renaming `orderId` to `id` or removing `currency`.

---

#### Why this pattern exists

In microservice systems, teams deploy independently.

That independence is valuable, but it creates risk.

A provider team may change an API without realizing that a consumer depends on a specific field, status code, error format, enum value, or message shape.

For example, the Order Service team might change this response:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD"
}
```

to this:

```json
{
  "id": "ord_123",
  "state": "CONFIRMED",
  "amount": 129.99
}
```

From the provider team’s perspective, this may look like a cleanup.

From the consumer’s perspective, it is a breaking change.

```mermaid
flowchart TD
    ProviderChange[Provider changes API]
    Consumer[Consumer expects old response]
    Failure[Consumer breaks in production]

    ProviderChange --> Consumer
    Consumer --> Failure
```

Consumer-Driven Contracts prevent this by making consumer expectations executable and testable before deployment.

---

#### What it solves

Consumer-Driven Contracts solve the problem of **accidental contract breakage**.

Without contracts, teams often rely on:

* documentation,
* manual testing,
* integration environments,
* informal Slack messages,
* hope that consumers will not break.

That is fragile.

```mermaid
flowchart TD
    Provider[Provider Team]
    Change[API Change]
    Deploy[Deploy]
    Consumer[Consumer Breaks]
    Incident[Production Incident]

    Provider --> Change
    Change --> Deploy
    Deploy --> Consumer
    Consumer --> Incident
```

With consumer-driven contracts, provider changes are checked against known consumer expectations before release.

```mermaid
flowchart TD
    Provider[Provider Team]
    Change[API Change]
    ContractTests[Run Contract Tests]
    Result{Contracts Pass?}

    Deploy[Deploy]
    Fix[Fix Breaking Change]

    Provider --> Change
    Change --> ContractTests
    ContractTests --> Result

    Result -->|Yes| Deploy
    Result -->|No| Fix
```

The provider can deploy with more confidence because it knows it still satisfies its consumers.

---

#### Provider contract vs consumer-driven contract

A traditional provider-driven API contract says:

> Here is what the provider offers.

For example, an OpenAPI document may define the full Order API.

A consumer-driven contract says:

> Here is what this specific consumer actually needs from the provider.

Both are useful, but they serve different purposes.

| Contract type            | Defined by                | Focus                                    |
| ------------------------ | ------------------------- | ---------------------------------------- |
| Provider contract        | Provider team             | Complete public API surface              |
| Consumer-driven contract | Consumer team             | Behavior required by a specific consumer |
| Shared schema            | Platform or provider team | Common message or data format            |
| Consumer test            | Consumer team             | “This is what I need to keep working”    |

A provider contract may say the API supports many fields:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD",
  "createdAt": "2026-04-29T12:00:00Z",
  "updatedAt": "2026-04-29T12:15:00Z",
  "customerId": "cus_456",
  "internalRiskScore": 0.13
}
```

A mobile consumer contract may only care about:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD"
}
```

Consumer-driven contracts help providers understand what is truly depended on.

---

#### Basic workflow

A typical Consumer-Driven Contract workflow looks like this:

```mermaid
flowchart TD
    Step1[Consumer defines expected interaction]
    Step2[Consumer tests against mock provider]
    Step3[Contract is published]
    Step4[Provider verifies contract]
    Step5[Provider deploys only if contracts pass]

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
```

In more detail:

1. The consumer writes a contract describing the request it will make and the response it requires.
2. The consumer uses the contract to test its own code against a mock provider.
3. The contract is published to a shared location, often called a contract broker.
4. The provider pulls the contract and runs it against the real provider implementation.
5. If the provider passes all relevant consumer contracts, it can deploy with more confidence.

```mermaid
flowchart TD
    ConsumerTests[Consumer Tests]
    Contract[Generated Contract]
    Broker[Contract Broker]
    ProviderVerification[Provider Verification Tests]
    Provider[Provider Service]

    ConsumerTests --> Contract
    Contract --> Broker
    Broker --> ProviderVerification
    ProviderVerification --> Provider
```

---

#### Example: REST API contract

Suppose a Web BFF calls the Order Service:

```http
GET /orders/ord_123
```

The BFF expects:

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD"
}
```

A contract describes that interaction:

```ts
const orderSummaryContract = {
  consumer: "web-bff",
  provider: "order-service",
  interaction: {
    description: "get confirmed order summary",
    request: {
      method: "GET",
      path: "/orders/ord_123"
    },
    response: {
      status: 200,
      body: {
        orderId: "ord_123",
        status: "CONFIRMED",
        totalAmount: 129.99,
        currency: "USD"
      }
    }
  }
};
```

The important part is not the exact syntax. Different tools use different formats.

The important part is the contract captures a real consumer expectation.

---

#### Example: consumer test

A consumer test verifies that the consumer can work with the expected provider response.

For example:

```ts
type OrderSummary = {
  orderId: string;
  status: "PENDING" | "CONFIRMED" | "CANCELLED";
  totalAmount: number;
  currency: string;
};

async function getOrderSummary(orderId: string): Promise<OrderSummary> {
  const response = await fetch(`http://order-service/orders/${orderId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch order");
  }

  return response.json() as Promise<OrderSummary>;
}
```

Consumer-side test:

```ts
describe("Order Service contract", () => {
  it("returns order summary needed by Web BFF", async () => {
    mockProvider.given("order ord_123 exists and is confirmed")
      .uponReceiving("a request for order summary")
      .withRequest({
        method: "GET",
        path: "/orders/ord_123"
      })
      .willRespondWith({
        status: 200,
        headers: {
          "Content-Type": "application/json"
        },
        body: {
          orderId: "ord_123",
          status: "CONFIRMED",
          totalAmount: 129.99,
          currency: "USD"
        }
      });

    const order = await getOrderSummary("ord_123");

    expect(order).toEqual({
      orderId: "ord_123",
      status: "CONFIRMED",
      totalAmount: 129.99,
      currency: "USD"
    });
  });
});
```

This test proves the consumer can handle the expected response.

It also produces a contract that the provider can later verify.

---

#### Example: provider verification

The provider runs the consumer contract against the real provider implementation.

```mermaid
flowchart TD
    Contract[Consumer Contract]
    ProviderTest[Provider Verification Test]
    Provider[Real Provider API]
    Result[Pass or Fail]

    Contract --> ProviderTest
    ProviderTest --> Provider
    Provider --> Result
```

Provider verification checks:

* Does the provider accept the expected request?
* Does it return the expected status code?
* Does it include required fields?
* Are field types compatible?
* Are expected headers present?
* Are error responses compatible?
* Does provider state setup support the scenario?

Example provider verification setup:

```ts
describe("Order Service provider verification", () => {
  beforeEach(async () => {
    await testDatabase.orders.insert({
      orderId: "ord_123",
      status: "CONFIRMED",
      totalAmount: 129.99,
      currency: "USD"
    });
  });

  it("satisfies Web BFF order summary contract", async () => {
    const response = await request(orderServiceApp)
      .get("/orders/ord_123")
      .expect(200);

    expect(response.body).toMatchObject({
      orderId: "ord_123",
      status: "CONFIRMED",
      totalAmount: 129.99,
      currency: "USD"
    });
  });
});
```

If the provider removes `currency`, the provider verification fails before deployment.

---

#### Provider states

Consumer contracts often need provider states.

A provider state describes the setup required before verifying an interaction.

Examples:

| Provider state                     | Meaning                                      |
| ---------------------------------- | -------------------------------------------- |
| `order ord_123 exists`             | Provider should create test order `ord_123`  |
| `order ord_123 is cancelled`       | Provider should prepare a cancelled order    |
| `customer cus_123 has no invoices` | Provider should prepare empty invoice state  |
| `payment pay_123 failed`           | Provider should prepare failed payment state |

Example:

```ts
mockProvider.given("order ord_123 exists and is confirmed")
  .uponReceiving("a request for order summary")
  .withRequest({
    method: "GET",
    path: "/orders/ord_123"
  })
  .willRespondWith({
    status: 200,
    body: {
      orderId: "ord_123",
      status: "CONFIRMED",
      totalAmount: 129.99,
      currency: "USD"
    }
  });
```

The provider verification test must know how to create that state.

```ts
const providerStates = {
  "order ord_123 exists and is confirmed": async () => {
    await testDatabase.orders.insert({
      orderId: "ord_123",
      status: "CONFIRMED",
      totalAmount: 129.99,
      currency: "USD"
    });
  }
};
```

Provider states make contracts executable instead of relying on fragile shared test environments.

---

#### Contracts for error responses

Contracts should cover important error cases, not only happy paths.

For example, a consumer may depend on this error when an order is missing:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json
```

```json
{
  "error": "ORDER_NOT_FOUND",
  "message": "The requested order does not exist."
}
```

Contract:

```ts
const orderNotFoundContract = {
  consumer: "mobile-bff",
  provider: "order-service",
  interaction: {
    description: "get missing order",
    request: {
      method: "GET",
      path: "/orders/missing_order"
    },
    response: {
      status: 404,
      body: {
        error: "ORDER_NOT_FOUND",
        message: "The requested order does not exist."
      }
    }
  }
};
```

This prevents providers from accidentally changing error behavior.

For example, changing the response to this may break the consumer:

```json
{
  "code": "NOT_FOUND"
}
```

If the mobile app expects `error: "ORDER_NOT_FOUND"`, that is a breaking change.

---

#### Contracts for events

Consumer-Driven Contracts are not only for REST APIs.

They are also useful for events and messages.

Suppose the Order Service publishes `OrderCreated`.

The Inventory Service consumes the event and requires:

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt_123",
  "schemaVersion": 1,
  "data": {
    "orderId": "ord_456",
    "items": [
      {
        "productId": "prod_123",
        "quantity": 2
      }
    ]
  }
}
```

The Inventory Service does not care about payment method, marketing campaign, or UI source. It cares about order ID and item quantities.

A consumer-driven event contract captures that requirement.

```ts
const inventoryOrderCreatedContract = {
  consumer: "inventory-service",
  provider: "order-service",
  message: {
    description: "OrderCreated event contains inventory reservation data",
    eventType: "OrderCreated",
    body: {
      eventId: "evt_123",
      eventType: "OrderCreated",
      schemaVersion: 1,
      data: {
        orderId: "ord_456",
        items: [
          {
            productId: "prod_123",
            quantity: 2
          }
        ]
      }
    }
  }
};
```

The Order Service provider test verifies that when an order is created, it publishes an event compatible with this contract.

---

#### Event contract testing

Event provider verification checks the event emitted by the provider.

```mermaid
flowchart TD
    Provider[Order Service]
    Action[Create Order]
    PublishedEvent[Published OrderCreated Event]
    Contract[Inventory Service Contract]
    Verification[Verify Event Shape]

    Provider --> Action
    Action --> PublishedEvent
    PublishedEvent --> Verification
    Contract --> Verification
```

Example:

```ts
it("publishes OrderCreated event required by Inventory Service", async () => {
  await orderService.createOrder({
    orderId: "ord_456",
    items: [
      {
        productId: "prod_123",
        quantity: 2
      }
    ]
  });

  const publishedEvent = await testEventBus.findEvent("OrderCreated");

  expect(publishedEvent).toMatchObject({
    eventType: "OrderCreated",
    schemaVersion: 1,
    data: {
      orderId: "ord_456",
      items: [
        {
          productId: "prod_123",
          quantity: 2
        }
      ]
    }
  });
});
```

This catches breaking event schema changes before they reach consumers.

---

#### Contracts for gRPC APIs

Consumer-Driven Contracts can also apply to gRPC.

A provider may expose:

```proto
service OrderService {
  rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
}

message GetOrderRequest {
  string order_id = 1;
}

message GetOrderResponse {
  string order_id = 1;
  string status = 2;
  double total_amount = 3;
  string currency = 4;
}
```

A consumer contract may say:

> When I call `GetOrder` with `order_id = "ord_123"`, I require `order_id`, `status`, `total_amount`, and `currency`.

Even though protobuf gives you schema compatibility rules, consumer-driven contracts still help verify actual provider behavior.

They test examples, states, errors, and real consumer expectations.

---

#### Contract broker

In larger systems, contracts are usually stored in a shared contract broker.

```mermaid
flowchart TD
    ConsumerA[Web BFF]
    ConsumerB[Mobile BFF]
    ConsumerC[Inventory Service]

    Broker[Contract Broker]

    Provider[Order Service]

    ConsumerA --> Broker
    ConsumerB --> Broker
    ConsumerC --> Broker

    Provider --> Broker
```

The contract broker stores:

* contracts,
* provider verification results,
* consumer versions,
* provider versions,
* compatibility status,
* deployment safety information.

A contract broker helps answer:

* Which consumers depend on this provider?
* Which contracts must this provider satisfy?
* Has provider version `2.4.1` passed all contracts?
* Is it safe to deploy this provider to production?
* Which consumers still rely on an old field?
* Which contracts are stale?

This is especially useful in multi-team environments.

---

#### Deployment safety

Consumer-driven contracts support independent deployment.

Before deploying a provider, check whether it satisfies all relevant consumer contracts.

```mermaid
flowchart TD
    ProviderBuild[Provider Build]
    ContractTests[Verify Consumer Contracts]
    Decision{Safe to Deploy?}

    Deploy[Deploy Provider]
    Block[Block Deployment]

    ProviderBuild --> ContractTests
    ContractTests --> Decision

    Decision -->|Yes| Deploy
    Decision -->|No| Block
```

Before deploying a consumer, check whether the provider version in the target environment supports the consumer’s contract.

```mermaid
flowchart TD
    ConsumerBuild[Consumer Build]
    ContractPublished[Publish Consumer Contract]
    ProviderStatus[Check Provider Verification]
    Decision{Compatible?}

    Deploy[Deploy Consumer]
    Wait[Wait for Provider Support]

    ConsumerBuild --> ContractPublished
    ContractPublished --> ProviderStatus
    ProviderStatus --> Decision

    Decision -->|Yes| Deploy
    Decision -->|No| Wait
```

This prevents deploying a consumer that expects behavior the provider does not yet support.

---

#### Backward-compatible changes

Consumer-driven contracts help teams understand which changes are safe.

Usually safe:

* adding optional response fields,
* adding new endpoints,
* adding new event types,
* adding optional event fields,
* supporting additional enum values if consumers handle unknowns,
* making validation less restrictive,
* adding headers consumers do not depend on.

Usually breaking:

* removing fields,
* renaming fields,
* changing field types,
* changing status codes consumers depend on,
* removing enum values,
* changing error response shape,
* changing event meaning,
* changing required request fields,
* changing ordering or timing semantics,
* removing an endpoint.

Example safe change:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD",
  "estimatedDeliveryDate": "2026-05-03"
}
```

If consumers ignore unknown fields, adding `estimatedDeliveryDate` is usually safe.

Example breaking change:

```json
{
  "id": "ord_123",
  "state": "CONFIRMED",
  "amount": 129.99
}
```

If consumers expect `orderId`, `status`, and `totalAmount`, this breaks them.

---

#### Consumer contracts should capture real needs

A good consumer contract captures what the consumer actually depends on.

It should not capture every implementation detail.

Bad contract:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD",
  "createdAt": "2026-04-29T12:00:00.000Z",
  "updatedAt": "2026-04-29T12:15:00.000Z",
  "internalVersion": 17,
  "databaseShard": "shard-3",
  "debugTrace": "abc123"
}
```

If the consumer only displays the order total and status, this contract is too strict.

Better:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "currency": "USD"
}
```

Contracts that are too strict create false failures and slow down provider evolution.

The contract should represent meaningful consumer requirements, not a snapshot of the entire response.

---

#### Flexible matching

Contract tests should often use flexible matchers rather than exact values.

For example, this is too rigid:

```ts
expect(response.body).toEqual({
  orderId: "ord_123",
  status: "CONFIRMED",
  totalAmount: 129.99,
  currency: "USD",
  createdAt: "2026-04-29T12:00:00Z"
});
```

If the consumer only needs `createdAt` to be a valid ISO timestamp, use a type or pattern matcher:

```ts
expect(response.body).toMatchObject({
  orderId: expect.any(String),
  status: expect.stringMatching(/PENDING|CONFIRMED|CANCELLED/),
  totalAmount: expect.any(Number),
  currency: expect.stringMatching(/USD|EUR|GBP/),
  createdAt: expect.stringMatching(
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/
  )
});
```

This makes the contract stable while still protecting real consumer needs.

---

#### Contracts and schema validation

Consumer-driven contracts are related to schema validation, but they are not the same thing.

A schema might define the full event shape:

```json
{
  "type": "object",
  "required": ["eventId", "eventType", "data"],
  "properties": {
    "eventId": {
      "type": "string"
    },
    "eventType": {
      "type": "string"
    },
    "data": {
      "type": "object"
    }
  }
}
```

A consumer contract defines a specific interaction or expectation:

```json
{
  "eventType": "OrderCreated",
  "data": {
    "orderId": "ord_456",
    "items": [
      {
        "productId": "prod_123",
        "quantity": 2
      }
    ]
  }
}
```

Schema validation answers:

> Is this message structurally valid?

Consumer-driven contracts answer:

> Does this provider still satisfy what this consumer actually needs?

Both are useful.

---

#### Contracts and integration tests

Consumer-driven contracts do not replace all integration tests.

They reduce the need for expensive end-to-end testing by catching many compatibility problems earlier.

Comparison:

| Test type               | Purpose                                                |
| ----------------------- | ------------------------------------------------------ |
| Unit tests              | Test internal logic                                    |
| Consumer contract tests | Verify consumer expectations against provider behavior |
| Provider contract tests | Verify provider satisfies consumer contracts           |
| Integration tests       | Test real components working together                  |
| End-to-end tests        | Test full user journey                                 |

Consumer-driven contracts are especially useful because they are faster and more targeted than full end-to-end tests.

They answer a narrow but important question:

> Will this provider change break known consumers?

---

#### Contracts for frontend clients

Frontend clients can also use consumer-driven contracts.

For example:

```mermaid
flowchart TD
    WebApp[Web App]
    MobileApp[Mobile App]
    BFF[Backend for Frontend]

    WebApp --> BFF
    MobileApp --> BFF
```

The web app may require:

```json
{
  "displayName": "Alex",
  "cartItemCount": 3,
  "notifications": {
    "unreadCount": 2
  }
}
```

The mobile app may require:

```json
{
  "displayName": "Alex",
  "cartItemCount": 3
}
```

Separate contracts let the BFF evolve safely.

This is especially useful for mobile apps because old app versions may remain in use for a long time.

---

#### Contracts for shared internal APIs

Consumer-driven contracts are valuable for shared internal platforms.

Examples:

* Identity Service,
* Entitlements Service,
* Pricing Service,
* Customer Service,
* Notification Service,
* Payment Service,
* Search Service.

These providers often have many consumers.

```mermaid
flowchart TD
    Identity[Identity Service]

    WebBFF[Web BFF]
    MobileBFF[Mobile BFF]
    Admin[Admin Console]
    Billing[Billing Service]
    Support[Support Service]

    WebBFF --> Identity
    MobileBFF --> Identity
    Admin --> Identity
    Billing --> Identity
    Support --> Identity
```

Without contracts, the provider team may not know which consumers rely on which behavior.

Contracts make dependencies visible.

---

#### Contract ownership

Consumer-driven contracts require clear ownership.

The consumer owns the contract because it describes the consumer’s needs.

The provider owns satisfying the contract or negotiating a change.

```mermaid
flowchart TD
    ConsumerTeam[Consumer Team]
    Contract[Consumer Contract]
    ProviderTeam[Provider Team]

    ConsumerTeam -->|defines need| Contract
    ProviderTeam -->|verifies support| Contract
```

If a provider wants to remove a field, it should check which contracts depend on that field.

If a consumer no longer needs a field, it should remove that expectation from its contract.

Contracts should not live forever without ownership.

---

#### Contract lifecycle

Contracts have a lifecycle.

```mermaid
flowchart TD
    Create[Create Contract]
    Publish[Publish Contract]
    Verify[Provider Verifies]
    Use[Used in Deployment Checks]
    Update[Update as Consumer Changes]
    Deprecate[Deprecate when Consumer No Longer Needs It]
    Remove[Remove Stale Contract]

    Create --> Publish
    Publish --> Verify
    Verify --> Use
    Use --> Update
    Update --> Deprecate
    Deprecate --> Remove
```

A stale contract can block useful provider changes.

For example, a contract from an old service that no longer exists should not prevent provider deployment.

Good contract hygiene includes:

* owner metadata,
* last verified date,
* consumer version,
* provider version,
* production usage signal,
* deprecation process,
* removal of unused contracts.

---

#### Example contract metadata

A contract should include enough metadata to understand who owns it.

```json
{
  "consumer": "mobile-bff",
  "consumerTeam": "Mobile Platform Team",
  "provider": "order-service",
  "providerTeam": "Orders Team",
  "description": "Mobile order summary contract",
  "lastUpdated": "2026-04-29",
  "contact": "#team-mobile-platform",
  "interactions": []
}
```

This helps during breaking-change review.

If a provider change fails a contract, the provider team knows whom to contact.

---

#### Versioning contracts

Contracts should be version-aware.

For example, Mobile App v1 and Mobile App v2 may have different expectations.

```mermaid
flowchart TD
    MobileV1[Mobile App v1]
    MobileV2[Mobile App v2]

    ContractV1[Mobile v1 Contract]
    ContractV2[Mobile v2 Contract]

    Provider[Order Service]

    MobileV1 --> ContractV1
    MobileV2 --> ContractV2

    Provider --> ContractV1
    Provider --> ContractV2
```

This matters when old clients remain in production.

Example:

| Consumer version | Required fields                                                         |
| ---------------- | ----------------------------------------------------------------------- |
| Mobile v1        | `orderId`, `status`, `totalAmount`                                      |
| Mobile v2        | `orderId`, `status`, `totalAmount`, `currency`, `estimatedDeliveryDate` |

The provider must satisfy all active consumer versions.

---

#### Contract testing in CI/CD

Consumer-driven contracts are most valuable when integrated into CI/CD.

Consumer pipeline:

```mermaid
flowchart TD
    ConsumerCode[Consumer Code Change]
    ConsumerTests[Run Consumer Contract Tests]
    PublishContract[Publish Contract]
    Build[Build Consumer Artifact]

    ConsumerCode --> ConsumerTests
    ConsumerTests --> PublishContract
    PublishContract --> Build
```

Provider pipeline:

```mermaid
flowchart TD
    ProviderCode[Provider Code Change]
    UnitTests[Run Unit Tests]
    ContractTests[Verify Consumer Contracts]
    Decision{All Pass?}

    Deploy[Deploy]
    Block[Block Release]

    ProviderCode --> UnitTests
    UnitTests --> ContractTests
    ContractTests --> Decision

    Decision -->|Yes| Deploy
    Decision -->|No| Block
```

This shifts compatibility testing earlier.

Instead of discovering breakage in a shared staging environment or production, teams discover it during provider build verification.

---

#### Example breaking change caught by contract

Suppose Mobile BFF has a contract requiring:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "currency": "USD"
}
```

The Order Service team changes its response to:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED"
}
```

Provider verification fails:

```text
Contract verification failed:
Expected field $.currency to be present
Consumer: mobile-bff
Provider: order-service
Interaction: get confirmed order summary
```

This tells the provider exactly what broke and who depends on it.

The provider team can then choose to:

* keep `currency`,
* add a new version,
* coordinate migration with Mobile BFF,
* deprecate the field later after consumers stop using it.

---

#### Consumer-driven contracts and provider evolution

Consumer-driven contracts do not mean providers can never change.

They make change safer.

A provider can still evolve by:

* adding fields,
* adding endpoints,
* adding new event types,
* creating a new API version,
* deprecating old behavior with migration plans,
* coordinating breaking changes with affected consumers,
* removing stale contracts after consumers migrate.

The contracts reveal impact.

Without contracts, a provider team may not know who will break.

With contracts, the provider can see the consumers that depend on the old behavior.

---

#### Contract granularity

Contracts should be specific enough to be useful but not so detailed that they become brittle.

Too broad:

```text
The Order Service must behave exactly as it does today.
```

This is impossible to verify meaningfully.

Too narrow:

```text
The response timestamp must always equal 2026-04-29T12:00:00Z.
```

This is too brittle.

Good:

```text
When an existing confirmed order is requested, the provider returns 200 with orderId, status, totalAmount, and currency.
```

Good contracts describe meaningful interactions.

---

#### What to include in a contract

For REST APIs, contracts commonly include:

* HTTP method,
* path,
* query parameters,
* required headers,
* request body,
* response status,
* response headers,
* response body fields,
* error responses,
* provider state.

For gRPC APIs:

* service method,
* request message,
* response message,
* error status,
* metadata,
* provider state.

For events:

* event type,
* schema version,
* required fields,
* field types,
* example payload,
* event metadata,
* publishing scenario.

For message queues:

* message type,
* command or event semantics,
* required payload fields,
* headers,
* routing key,
* expected acknowledgement behavior when relevant.

---

#### What not to include in a contract

Avoid including details the consumer does not truly depend on.

Usually avoid:

* database IDs not exposed to consumer behavior,
* internal debug fields,
* exact timestamps unless needed,
* full response snapshots,
* field order in JSON,
* incidental headers,
* provider implementation details,
* fields the consumer ignores,
* overly specific generated values,
* every optional field.

A contract should protect useful compatibility, not freeze the provider implementation.

---

#### Handling multiple consumers

A provider may have many consumers.

```mermaid
flowchart TD
    Provider[Order Service]

    Web[Web BFF Contract]
    Mobile[Mobile BFF Contract]
    Admin[Admin Contract]
    Analytics[Analytics Consumer Contract]
    Inventory[Inventory Event Contract]

    Provider --> Web
    Provider --> Mobile
    Provider --> Admin
    Provider --> Analytics
    Provider --> Inventory
```

The provider must satisfy all active contracts.

This can reveal conflicting expectations.

For example:

| Consumer   | Expectation                                          |
| ---------- | ---------------------------------------------------- |
| Web BFF    | `status` values include `CONFIRMED`                  |
| Admin Tool | `status` values include `CONFIRMED`, `MANUAL_REVIEW` |
| Mobile App | Unknown statuses should be mapped to `PROCESSING`    |

If consumers have incompatible needs, the provider may need:

* versioned APIs,
* different endpoints,
* BFF-specific shaping,
* additive schema evolution,
* better enum handling,
* deprecation plan.

Contracts make these issues visible before production.

---

#### Consumer-driven contracts and event evolution

Event contracts are especially important because events often have many consumers.

```mermaid
flowchart TD
    OrderService[Order Service]
    OrderCreated[OrderCreated Event]

    Inventory[Inventory Service]
    Analytics[Analytics Service]
    Notifications[Notification Service]
    Search[Search Indexer]

    OrderService --> OrderCreated

    OrderCreated --> Inventory
    OrderCreated --> Analytics
    OrderCreated --> Notifications
    OrderCreated --> Search
```

A change to `OrderCreated` can break many consumers.

Safe event evolution usually means:

* add optional fields,
* keep existing fields,
* avoid changing field meaning,
* support old schema versions during migration,
* publish new event types when meaning changes significantly,
* give consumers time to migrate.

Bad event change:

```json
{
  "eventType": "OrderCreated",
  "data": {
    "id": "ord_123"
  }
}
```

If consumers expect `data.orderId`, this breaks them.

Better:

```json
{
  "eventType": "OrderCreated",
  "data": {
    "orderId": "ord_123",
    "id": "ord_123"
  }
}
```

Then deprecate `orderId` only after consumers stop using it.

Even better, avoid renaming stable event fields unless there is a strong reason.

---

#### Consumer-driven contracts vs shared test environments

Many organizations rely on shared staging environments for integration testing.

Shared environments are useful, but they have problems:

* slow feedback,
* environment instability,
* test data conflicts,
* unclear ownership,
* late discovery of breakage,
* hard-to-reproduce failures,
* many services must be deployed together.

Consumer-driven contracts catch many compatibility issues earlier.

```mermaid
flowchart TD
    CodeChange[Code Change]
    ContractTest[Fast Contract Test]
    SharedStaging[Shared Staging Test]
    Production[Production]

    CodeChange --> ContractTest
    ContractTest --> SharedStaging
    SharedStaging --> Production
```

Contracts do not eliminate staging, but they reduce reliance on it for basic compatibility.

---

#### Consumer-driven contracts and independent deployment

Independent deployment is one of the major benefits.

Without contracts, teams may coordinate deployments manually:

```mermaid
flowchart TD
    ProviderChange[Provider Change]
    Meeting[Coordinate with Consumers]
    DeployTogether[Deploy Together]
    Risk[Still Risky]

    ProviderChange --> Meeting
    Meeting --> DeployTogether
    DeployTogether --> Risk
```

With contracts, a provider can test against active consumer expectations.

```mermaid
flowchart TD
    ProviderChange[Provider Change]
    Verify[Verify Consumer Contracts]
    Deploy[Deploy Independently]

    ProviderChange --> Verify
    Verify --> Deploy
```

This does not remove communication. It makes communication evidence-based.

Instead of asking, “Will this break anyone?” teams can see which contracts pass or fail.

---

#### When to use it

Use Consumer-Driven Contracts when:

* multiple teams own consumers and providers,
* services deploy independently,
* APIs change frequently,
* event schemas are shared across services,
* provider changes have broken consumers before,
* shared staging tests are too slow or unreliable,
* mobile or partner clients need compatibility guarantees,
* internal platform services have many consumers,
* async messages have multiple subscribers,
* teams need confidence before deploying.

Common targets:

* REST APIs,
* gRPC APIs,
* GraphQL APIs,
* event schemas,
* Kafka topics,
* queues,
* webhooks,
* BFF APIs,
* internal platform APIs,
* partner APIs.

---

#### When not to use it

Consumer-driven contracts may be unnecessary or too heavy when:

* there is only one consumer and one provider owned by the same team,
* the API is very stable and rarely changes,
* the integration is trivial,
* consumers and providers are deployed together as one unit,
* simple schema validation is enough,
* the organization will not maintain contracts,
* contracts would duplicate better existing tests without adding value.

For small systems, a provider-owned OpenAPI spec and a few integration tests may be enough.

Consumer-driven contracts are most valuable when independent teams and independent deployments create compatibility risk.

---

#### Benefits

**1. Prevents accidental breaking changes**

Provider changes are tested against real consumer expectations.

**2. Supports independent deployment**

Teams can deploy with more confidence without coordinating every release manually.

**3. Makes dependencies visible**

Providers can see which consumers depend on which behavior.

**4. Reduces reliance on slow end-to-end tests**

Contract tests catch compatibility issues earlier and faster.

**5. Improves collaboration**

Consumers express their needs explicitly.

**6. Helps API evolution**

Providers can identify who is affected by breaking changes.

**7. Works for APIs and messages**

The pattern applies to REST, gRPC, events, queues, and schemas.

---

#### Trade-offs

**1. Requires discipline**

Contracts must be written, published, verified, and maintained.

**2. Can become too brittle**

Overly specific contracts can block harmless provider changes.

**3. Can become stale**

Contracts from retired consumers may continue blocking provider evolution.

**4. Does not test everything**

Contracts verify compatibility, not full business correctness or performance.

**5. Requires ownership**

Consumer and provider teams must agree on lifecycle and responsibility.

**6. Adds CI/CD complexity**

Provider pipelines need contract verification steps.

**7. May create false confidence**

Passing contracts does not guarantee the whole system works, only that known expectations are satisfied.

---

#### Common mistakes

**Mistake 1: Capturing entire responses**

Consumers should contract only on fields they actually need.

**Mistake 2: Ignoring error cases**

Important error responses should be covered.

**Mistake 3: Treating contracts as provider-owned only**

The consumer should define what it requires.

**Mistake 4: Letting contracts go stale**

Remove or deprecate contracts for consumers that no longer exist.

**Mistake 5: Making contracts too strict**

Exact timestamps, generated IDs, and ignored fields create brittle tests.

**Mistake 6: Not running provider verification in CI**

Contracts are only useful if they block unsafe changes before deployment.

**Mistake 7: Using contracts instead of communication**

Breaking changes still require coordination and migration planning.

**Mistake 8: Assuming contracts replace all tests**

You still need unit, integration, and end-to-end tests where appropriate.

**Mistake 9: Ignoring event contracts**

Async message schemas are just as important as synchronous APIs.

---

#### Practical design checklist

Before adopting Consumer-Driven Contracts, ask:

* Who are the consumers?
* Who owns each consumer?
* Who owns the provider?
* Which APIs or messages are risky to change?
* What behavior does each consumer actually require?
* Are contracts capturing real needs or full implementation snapshots?
* Are important error cases covered?
* Are event schemas covered?
* How are contracts published?
* Where are contracts stored?
* Does the provider verify contracts in CI?
* Are contract verification results visible?
* How are provider states created for tests?
* How are old contracts deprecated?
* How are consumer versions tracked?
* How are breaking changes coordinated?
* How are schema versions handled?
* Are flexible matchers used where appropriate?
* Are contracts blocking deployment only when they represent active consumers?

A contract strategy is probably healthy if:

* consumers define real expectations,
* providers verify contracts automatically,
* contracts are versioned,
* stale contracts are removed,
* contracts cover important success and error cases,
* event schemas are included,
* CI/CD uses contract verification,
* contract failures identify the affected consumer,
* teams still communicate about intentional breaking changes.

A contract strategy is probably unhealthy if:

* contracts are just full response snapshots,
* nobody owns them,
* provider verification is optional,
* stale contracts block changes,
* consumers do not update contracts when their needs change,
* event schemas change without contract checks,
* teams treat contract passing as proof that all business behavior works.

---

#### Related patterns

| Pattern                   | Relationship                                                 |
| ------------------------- | ------------------------------------------------------------ |
| API Gateway               | Gateway-facing APIs can be protected with consumer contracts |
| Backends for Frontends    | Frontend clients can define contracts against BFF APIs       |
| Async Messaging           | Events and messages need contracts just like APIs            |
| Choreography              | Event-driven workflows rely on stable event contracts        |
| Saga                      | Saga participants depend on command and event contracts      |
| CQRS                      | Read model consumers may define contracts for query APIs     |
| Anti-Corruption Layer     | Contracts clarify the boundary between systems               |
| Versioned APIs            | Contracts help manage API evolution across versions          |
| Schema Registry           | Complements CDC for event and message schema governance      |
| Strangler Fig Pattern     | Contracts reduce risk while replacing legacy APIs            |
| Consumer-Provider Testing | The testing practice behind this pattern                     |

---

#### Summary

Consumer-Driven Contracts are agreements where consumers define the API or message behavior they require, and providers verify that they still satisfy those expectations.

The central idea is:

> Consumers describe what they depend on. Providers test against those expectations before deploying changes.

This pattern is useful for REST APIs, gRPC APIs, event schemas, queues, shared internal APIs, BFFs, partner APIs, and multi-team platforms.

A good contract strategy:

* captures real consumer needs,
* avoids unnecessary implementation details,
* covers important success and error cases,
* supports events and messages,
* runs provider verification in CI/CD,
* tracks active consumer versions,
* removes stale contracts,
* and makes breaking changes visible before production.

The main trade-off is maintenance. Contracts require discipline. If they are too strict, stale, or poorly owned, they become friction. If they are focused and actively maintained, they allow teams to deploy independently with much greater confidence.


---

## 5. Data Ownership, Persistence, and Consistency Patterns

These patterns define how services store, own, query, synchronize, and protect data in a distributed system.

In a monolithic application, many features often share one database. In a microservice architecture, that usually becomes dangerous because services can become coupled through tables instead of through well-defined APIs and events.

Data patterns answer questions such as:

* Which service owns this data?
* Can another service read this table directly?
* How do services query data across boundaries?
* How do services keep data consistent without one global transaction?
* How are changes published to other services?
* How do we handle duplicates, stale reads, retries, and eventual consistency?

The most important principle in this group is:

> A service should own the data it is responsible for, and other services should interact with that data through contracts, not direct database access.

---

### 21. Database per Service

#### What it is

**Database per Service** is a microservice data ownership pattern where each service owns its own database, schema, or set of tables.

Other services do not directly read or write that database. They access the owning service’s data through:

* APIs,
* events,
* commands,
* messages,
* replicated read models,
* published data products.

The basic structure looks like this:

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]
    CustomerService[Customer Service]

    OrderDB[(Order Database)]
    PaymentDB[(Payment Database)]
    InventoryDB[(Inventory Database)]
    CustomerDB[(Customer Database)]

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    InventoryService --> InventoryDB
    CustomerService --> CustomerDB
```

Each service owns its own persistence model.

For example:

| Service           | Owns                                        |
| ----------------- | ------------------------------------------- |
| Order Service     | Orders, order status, order history         |
| Payment Service   | Payments, authorizations, captures, refunds |
| Inventory Service | Stock levels, reservations, availability    |
| Customer Service  | Customer profiles, customer preferences     |
| Shipping Service  | Shipments, tracking, carrier references     |

The central idea is:

> A service owns its data. Other services must not bypass the service and directly manipulate its database.

This is one of the most important foundations of microservice autonomy.

---

#### Why this pattern exists

A common early mistake in microservices is to split the application code into services while keeping one shared database.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]
    ReportingService[Reporting Service]

    SharedDB[(Shared Database)]

    OrderService --> SharedDB
    PaymentService --> SharedDB
    InventoryService --> SharedDB
    ReportingService --> SharedDB
```

This may look convenient because all services can query the same data. But it creates hidden coupling.

For example, suppose the Payment Service directly reads the `orders` table:

```sql
SELECT id, status, total_amount
FROM orders
WHERE id = 'ord_123';
```

Now the Payment Service depends on the Order Service’s table structure.

If the Order Service team wants to rename `total_amount` to `amount_cents`, split the table, change status values, or move storage technologies, the Payment Service may break.

The database has become a shared contract, even if nobody intended it to be.

Database per Service avoids this by making ownership explicit.

```mermaid
flowchart TD
    PaymentService[Payment Service]
    OrderService[Order Service]
    OrderDB[(Order Database)]

    PaymentService -->|API or event contract| OrderService
    OrderService --> OrderDB
```

The Payment Service depends on the Order Service’s API or events, not its internal tables.

---

#### What it solves

Database per Service solves **database-level coupling**.

Database-level coupling happens when multiple services depend directly on the same database structures.

Symptoms include:

* one service queries another service’s tables,
* several services write to the same table,
* database migrations require many teams to coordinate,
* table schemas become shared public contracts,
* one service cannot change its schema without breaking others,
* business rules are enforced inconsistently across services,
* ownership of tables is unclear,
* services are independently deployed in name only.

For example, this is database-level coupling:

```mermaid
flowchart TD
    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Analytics[Analytics Service]

    OrdersTable[(orders table)]

    Orders --> OrdersTable
    Payments --> OrdersTable
    Shipping --> OrdersTable
    Analytics --> OrdersTable
```

Every service depends on the `orders` table.

A safer design:

```mermaid
flowchart TD
    Orders[Order Service]
    OrderDB[(Order Database)]

    Payments[Payment Service]
    Shipping[Shipping Service]
    Analytics[Analytics Service]

    Orders --> OrderDB

    Payments -->|Order API or events| Orders
    Shipping -->|Order events| Orders
    Analytics -->|Order event stream| Orders
```

Now the Order Service owns the database. Other services depend on contracts.

---

#### Service ownership and data ownership

Database per Service is not just a storage pattern. It is an ownership pattern.

A service owns:

* the schema,
* the data model,
* the database migrations,
* the constraints,
* the storage technology,
* the read and write access rules,
* the lifecycle of the data,
* the business rules around that data.

For example, the Inventory Service owns inventory reservations.

```mermaid
flowchart TD
    InventoryService[Inventory Service]

    Reserve[Reserve Inventory]
    Release[Release Reservation]
    Commit[Commit Reservation]
    Query[Check Availability]

    InventoryDB[(Inventory Database)]

    InventoryService --> Reserve
    InventoryService --> Release
    InventoryService --> Commit
    InventoryService --> Query

    Reserve --> InventoryDB
    Release --> InventoryDB
    Commit --> InventoryDB
    Query --> InventoryDB
```

Other services should not directly update inventory tables.

Bad:

```sql
UPDATE inventory
SET available_quantity = available_quantity - 1
WHERE product_id = 'prod_123';
```

If the Order Service runs this SQL directly, it bypasses the Inventory Service’s rules.

Better:

```http
POST /inventory-reservations
Content-Type: application/json

{
  "orderId": "ord_123",
  "items": [
    {
      "productId": "prod_123",
      "quantity": 1
    }
  ]
}
```

The Inventory Service can then enforce its own rules:

* is the product tracked?
* is inventory available?
* is the warehouse active?
* is the item sellable?
* is the reservation duplicate?
* should inventory be reserved from one location or many?

Data ownership keeps those rules in the right place.

---

#### Database per Service does not always mean one physical database server

The phrase “database per service” can be misunderstood.

It does not always mean every service must have its own physical database server.

It means each service has exclusive ownership over its persistence boundary.

Possible implementations include:

##### Separate physical databases

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]

    OrderDB[(Order PostgreSQL Cluster)]
    PaymentDB[(Payment PostgreSQL Cluster)]

    OrderService --> OrderDB
    PaymentService --> PaymentDB
```

This gives strong isolation.

##### Separate schemas in the same database server

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]

    SharedServer[(Shared PostgreSQL Server)]

    OrderSchema[(orders schema)]
    PaymentSchema[(payments schema)]

    OrderService --> OrderSchema
    PaymentService --> PaymentSchema

    SharedServer --> OrderSchema
    SharedServer --> PaymentSchema
```

This can be acceptable if access controls prevent cross-service access.

##### Separate tables with strict ownership

```mermaid
flowchart TD
    SharedDB[(Shared Database)]

    OrderTables[(Order-owned tables)]
    PaymentTables[(Payment-owned tables)]

    OrderService[Order Service]
    PaymentService[Payment Service]

    OrderService --> OrderTables
    PaymentService --> PaymentTables

    SharedDB --> OrderTables
    SharedDB --> PaymentTables
```

This is weaker isolation, but it can be a transitional step.

The key rule is:

> Ownership matters more than physical deployment. A service’s data should not be directly accessed by other services.

In mature microservice systems, physical separation is often preferred because it enforces ownership more strongly.

---

#### Basic architecture

A service exposes behavior through APIs or messages. The database remains private.

```mermaid
flowchart TD
    ClientService[Other Service]
    OwnerService[Owning Service]
    PrivateDB[(Private Database)]

    ClientService -->|API call, command, or event subscription| OwnerService
    OwnerService --> PrivateDB
```

For example:

```mermaid
flowchart TD
    CheckoutService[Checkout Service]
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]
    InventoryDB[(Inventory DB)]

    CheckoutService --> OrderService
    CheckoutService --> PaymentService
    CheckoutService --> InventoryService

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    InventoryService --> InventoryDB
```

Checkout Service coordinates the workflow, but it does not directly write to the Order, Payment, or Inventory databases.

Each service protects its own data.

---

#### Example: Order Service owns orders

The Order Service might own this internal table:

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

It exposes an API:

```http
GET /orders/ord_123
```

Response:

```json
{
  "orderId": "ord_123",
  "customerId": "cus_456",
  "status": "CONFIRMED",
  "totalAmount": {
    "amount": 129.99,
    "currency": "USD"
  }
}
```

Notice that the API response does not have to match the database schema exactly.

Internally, the database stores `total_amount_cents`.

Externally, the API exposes:

```json
{
  "amount": 129.99,
  "currency": "USD"
}
```

This is good. The service can change its database schema without forcing consumers to change.

---

#### Example: service repository layer

Inside a service, the database is accessed through local persistence code.

```ts
type OrderStatus =
  | "PENDING"
  | "CONFIRMED"
  | "CANCELLED"
  | "SHIPPED";

type Order = {
  orderId: string;
  customerId: string;
  status: OrderStatus;
  totalAmountCents: number;
  currency: string;
};

class OrderRepository {
  constructor(private readonly db: Database) {}

  async findById(orderId: string): Promise<Order | null> {
    const row = await this.db.queryOne(
      `
      SELECT order_id, customer_id, status, total_amount_cents, currency
      FROM orders
      WHERE order_id = $1
      `,
      [orderId]
    );

    if (!row) {
      return null;
    }

    return {
      orderId: row.order_id,
      customerId: row.customer_id,
      status: row.status,
      totalAmountCents: row.total_amount_cents,
      currency: row.currency
    };
  }

  async save(order: Order): Promise<void> {
    await this.db.execute(
      `
      INSERT INTO orders (
        order_id,
        customer_id,
        status,
        total_amount_cents,
        currency
      )
      VALUES ($1, $2, $3, $4, $5)
      ON CONFLICT (order_id)
      DO UPDATE SET
        status = EXCLUDED.status,
        total_amount_cents = EXCLUDED.total_amount_cents
      `,
      [
        order.orderId,
        order.customerId,
        order.status,
        order.totalAmountCents,
        order.currency
      ]
    );
  }
}
```

Only the Order Service uses this repository.

No other service imports it, queries the table, or depends on the table shape.

---

#### Example: API instead of direct database access

Suppose Payment Service needs to know whether an order exists before authorizing payment.

Bad design:

```ts
async function authorizePayment(orderId: string) {
  const order = await sharedDatabase.queryOne(
    "SELECT * FROM orders WHERE order_id = $1",
    [orderId]
  );

  if (!order) {
    throw new Error("Order not found");
  }

  return paymentGateway.authorize(order.total_amount_cents);
}
```

Payment Service is now coupled to the Order database.

Better design:

```ts
async function authorizePayment(orderId: string) {
  const order = await orderClient.getOrder(orderId);

  if (order.status === "CANCELLED") {
    throw new Error("Cannot authorize payment for cancelled order");
  }

  return paymentGateway.authorize({
    orderId: order.orderId,
    amount: order.totalAmount.amount,
    currency: order.totalAmount.currency
  });
}
```

The Payment Service depends on the Order API contract, not the Order database schema.

---

#### Data access rules

A healthy Database per Service design has clear access rules.

| Action                                       | Allowed?    | Why                                   |
| -------------------------------------------- | ----------- | ------------------------------------- |
| Service reads its own tables                 | Yes         | It owns them                          |
| Service writes its own tables                | Yes         | It owns them                          |
| Other service reads owner’s tables directly  | No          | Creates schema coupling               |
| Other service writes owner’s tables directly | Strong no   | Bypasses business rules               |
| Reporting system reads replicated data       | Usually yes | If replicated intentionally           |
| DBA runs emergency query                     | Sometimes   | Operational exception, not app design |
| Data platform ingests change events          | Yes         | If governed as published data         |

The most dangerous violation is cross-service writes.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    OrderDB[(Order DB)]

    OrderService --> OrderDB
    PaymentService -. direct write: bad .-> OrderDB
```

A direct write bypasses invariants and can corrupt business state.

---

#### Polyglot persistence

Database per Service allows each service to choose the storage technology that fits its needs.

```mermaid
flowchart TD
    CatalogService[Catalog Service]
    OrderService[Order Service]
    SearchService[Search Service]
    RecommendationService[Recommendation Service]
    SessionService[Session Service]

    DocumentDB[(Document Database)]
    RelationalDB[(Relational Database)]
    SearchIndex[(Search Index)]
    GraphDB[(Graph Database)]
    Cache[(Key-Value Store)]

    CatalogService --> DocumentDB
    OrderService --> RelationalDB
    SearchService --> SearchIndex
    RecommendationService --> GraphDB
    SessionService --> Cache
```

Examples:

| Service                | Possible storage                                  |
| ---------------------- | ------------------------------------------------- |
| Order Service          | Relational database for transactions              |
| Catalog Service        | Document database for flexible product attributes |
| Search Service         | Search index for full-text search                 |
| Recommendation Service | Graph or vector database                          |
| Session Service        | Key-value store                                   |
| Audit Service          | Append-only event store                           |
| Analytics Service      | Columnar warehouse                                |

This is called **polyglot persistence**.

The benefit is that each service can use the right tool.

The trade-off is operational complexity. More database technologies mean more skills, monitoring, backups, security, and failure modes.

---

#### Schema evolution

One major benefit of Database per Service is independent schema evolution.

The Order Service can change its internal schema without requiring every other service to migrate at the same time.

For example, it might split one table:

Before:

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    shipping_address TEXT,
    billing_address TEXT,
    status TEXT
);
```

After:

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    status TEXT
);

CREATE TABLE order_addresses (
    order_id TEXT,
    address_type TEXT,
    address_json JSONB
);
```

If no other service directly queries these tables, the change is internal to the Order Service.

The public API can remain stable:

```json
{
  "orderId": "ord_123",
  "customerId": "cus_456",
  "status": "CONFIRMED",
  "shippingAddress": {
    "line1": "100 Market Street",
    "city": "San Francisco"
  }
}
```

This is exactly the kind of autonomy microservices are supposed to provide.

---

#### Cross-service queries

The biggest challenge with Database per Service is that cross-service queries become harder.

In a shared database, this is easy:

```sql
SELECT
    o.order_id,
    o.status,
    p.status AS payment_status,
    s.status AS shipment_status
FROM orders o
JOIN payments p ON p.order_id = o.order_id
JOIN shipments s ON s.order_id = o.order_id
WHERE o.customer_id = 'cus_123';
```

In Database per Service, those tables live behind different services.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    ShippingService[Shipping Service]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]
    ShippingDB[(Shipping DB)]

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    ShippingService --> ShippingDB
```

You should not perform a direct database join across service databases.

Instead, use one of these patterns:

1. API composition
2. Gateway aggregation
3. BFF aggregation
4. CQRS read model
5. Event-fed materialized view
6. Data warehouse or analytics platform

---

#### Option 1: API composition

A service or aggregator calls multiple services and combines results.

```mermaid
flowchart TD
    Client[Client]
    Aggregator[Order Summary API]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]

    Client --> Aggregator

    Aggregator --> Orders
    Aggregator --> Payments
    Aggregator --> Shipping
```

Example:

```ts
async function getOrderSummary(orderId: string): Promise<OrderSummary> {
  const [order, payment, shipment] = await Promise.all([
    orderClient.getOrder(orderId),
    paymentClient.getPaymentByOrderId(orderId),
    shippingClient.getShipmentByOrderId(orderId)
  ]);

  return {
    orderId: order.orderId,
    orderStatus: order.status,
    paymentStatus: payment.status,
    shipmentStatus: shipment.status
  };
}
```

This works well for simple, low-volume reads.

But it can become slow or expensive if the query needs many services or many records.

---

#### Option 2: CQRS read model

For high-volume or complex queries, build a read model.

Services publish events. A projector consumes them and updates a query-optimized database.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    ShippingService[Shipping Service]

    Bus[(Event Bus)]

    Projector[Order Summary Projector]
    ReadDB[(Order Summary Read DB)]

    QueryAPI[Order Summary Query API]
    Client[Client]

    OrderService -->|OrderCreated, OrderConfirmed| Bus
    PaymentService -->|PaymentAuthorized, PaymentCaptured| Bus
    ShippingService -->|ShipmentCreated, ShipmentDelivered| Bus

    Bus --> Projector
    Projector --> ReadDB

    Client --> QueryAPI
    QueryAPI --> ReadDB
```

The read model might store:

```json
{
  "orderId": "ord_123",
  "customerId": "cus_456",
  "orderStatus": "CONFIRMED",
  "paymentStatus": "AUTHORIZED",
  "shipmentStatus": "PENDING",
  "totalAmount": 129.99,
  "currency": "USD"
}
```

This avoids runtime joins across service databases.

The trade-off is eventual consistency. The read model may lag behind the source services.

---

#### Cross-service transactions

Database per Service also makes cross-service transactions harder.

For example, placing an order may require:

* create order,
* authorize payment,
* reserve inventory.

In a shared database, you might use one transaction.

In microservices, each service commits locally.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]
    InventoryDB[(Inventory DB)]

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    InventoryService --> InventoryDB
```

You cannot safely wrap all of these in one ordinary database transaction.

Instead, use patterns such as:

* Saga,
* Async Messaging,
* Outbox Pattern,
* Try-confirm-cancel,
* idempotent commands,
* compensating actions.

Example saga:

```mermaid
flowchart TD
    Start[Place Order]

    CreateOrder[Create Pending Order]
    AuthorizePayment[Authorize Payment]
    ReserveInventory[Reserve Inventory]
    ConfirmOrder[Confirm Order]

    VoidPayment[Void Payment]
    CancelOrder[Cancel Order]

    Start --> CreateOrder
    CreateOrder --> AuthorizePayment
    AuthorizePayment --> ReserveInventory
    ReserveInventory --> ConfirmOrder

    ReserveInventory -->|fails| VoidPayment
    VoidPayment --> CancelOrder
```

The price of service autonomy is that consistency must be designed explicitly.

---

#### Eventual consistency

Database per Service often leads to eventual consistency.

For example:

1. Order Service creates an order.
2. It publishes `OrderCreated`.
3. Payment Service later authorizes payment.
4. Inventory Service later reserves stock.
5. Order status eventually becomes `CONFIRMED`.

During the workflow, the system may temporarily show:

```json
{
  "orderId": "ord_123",
  "status": "PENDING_PAYMENT"
}
```

Then later:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED"
}
```

This is not a bug if the business process is designed for it.

User interfaces and APIs should expose meaningful intermediate states:

* `PENDING`
* `PROCESSING`
* `PENDING_PAYMENT`
* `PENDING_INVENTORY`
* `CONFIRMED`
* `FAILED`
* `CANCELLED`

Do not promise immediate consistency if the architecture cannot provide it.

---

#### Data duplication

Database per Service often requires controlled data duplication.

For example, the Order Service may store a snapshot of customer information at the time of order:

```json
{
  "orderId": "ord_123",
  "customerId": "cus_456",
  "customerSnapshot": {
    "displayName": "Alex Morgan",
    "email": "alex@example.com"
  }
}
```

This is not necessarily bad.

It may be required because an order needs to preserve historical facts.

If the customer later changes their email address, the old order may still need to show the email used at purchase time.

Types of acceptable duplication:

| Duplication type    | Example                       | Why useful                   |
| ------------------- | ----------------------------- | ---------------------------- |
| Historical snapshot | Customer name on order        | Preserves past business fact |
| Read model copy     | Order summary view            | Supports efficient queries   |
| Search index        | Product data in search engine | Supports full-text search    |
| Cache               | Recently viewed product       | Improves performance         |
| Analytics copy      | Event data in warehouse       | Supports reporting           |

The key is to know which copy is authoritative.

---

#### Source of truth

With duplicated data, every field should have a clear source of truth.

For example:

| Data                     | Source of truth                                  |
| ------------------------ | ------------------------------------------------ |
| Current customer profile | Customer Service                                 |
| Order status             | Order Service                                    |
| Payment status           | Payment Service                                  |
| Inventory availability   | Inventory Service                                |
| Shipment tracking        | Shipping Service                                 |
| Product search index     | Derived from Catalog Service                     |
| Order summary read model | Derived from Order, Payment, and Shipping events |

A read model is not usually the source of truth. It is a derived projection.

```mermaid
flowchart TD
    Source[Source of Truth Service]
    Events[Events]
    Projection[Derived Read Model]

    Source --> Events
    Events --> Projection
```

If the projection is wrong, rebuild it from source events or source services.

Do not let derived copies become accidental sources of truth.

---

#### Reporting and analytics

Reporting is a common reason teams violate Database per Service.

A reporting tool may want to query every service database directly.

```mermaid
flowchart TD
    Reporting[Reporting Tool]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]
    CustomerDB[(Customer DB)]
    InventoryDB[(Inventory DB)]

    Reporting -. direct queries .-> OrderDB
    Reporting -. direct queries .-> PaymentDB
    Reporting -. direct queries .-> CustomerDB
    Reporting -. direct queries .-> InventoryDB
```

This is tempting, but dangerous.

Problems:

* reporting queries can overload operational databases,
* schema changes break reports,
* sensitive data may leak,
* ownership becomes unclear,
* operational databases become integration points.

A better design publishes data into an analytics platform.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    CustomerService[Customer Service]

    Events[(Event Stream)]
    ETL[ETL or Stream Processor]
    Warehouse[(Data Warehouse)]
    BI[BI and Reporting]

    OrderService --> Events
    PaymentService --> Events
    CustomerService --> Events

    Events --> ETL
    ETL --> Warehouse
    Warehouse --> BI
```

Reporting can then query the warehouse instead of service databases.

---

#### Access control

Database per Service should be enforced with access control.

Each service should have database credentials only for its own database or schema.

Bad:

```text
All services use the same database username and password.
```

Better:

```text
order-service can access order_db only.
payment-service can access payment_db only.
inventory-service can access inventory_db only.
```

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]

    OrderService -->|order_db credentials| OrderDB
    PaymentService -->|payment_db credentials| PaymentDB

    OrderService -. no access .-> PaymentDB
    PaymentService -. no access .-> OrderDB
```

If teams can bypass the service boundary easily, they eventually will.

Technical enforcement matters.

---

#### Database migrations

Each service should own its own migrations.

For example, Order Service owns:

```text
order-service/migrations
```

Payment Service owns:

```text
payment-service/migrations
```

A service deployment may include database migration steps.

```mermaid
flowchart TD
    CodeChange[Service Code Change]
    Migration[Database Migration]
    Deploy[Deploy Service]

    CodeChange --> Migration
    Migration --> Deploy
```

Migration safety is important because services are deployed independently.

Use backward-compatible migration practices:

1. Add new nullable column.
2. Deploy code that writes both old and new fields.
3. Backfill data.
4. Deploy code that reads new field.
5. Remove old field later.

Example:

```sql
ALTER TABLE orders ADD COLUMN total_amount_cents INTEGER;
```

Do not immediately remove old fields if old code versions might still be running.

Database per Service reduces cross-team migration coupling, but it does not eliminate migration discipline.

---

#### Shared reference data

Some data is shared across many services, such as:

* country codes,
* currency codes,
* tax categories,
* product categories,
* compliance classifications,
* tenant metadata,
* feature flags.

There are several ways to handle this.

##### Option 1: Dedicated reference data service

```mermaid
flowchart TD
    ReferenceService[Reference Data Service]
    Services[Other Services]

    Services --> ReferenceService
```

Good when the data changes and needs governance.

##### Option 2: Replicated reference data

```mermaid
flowchart TD
    ReferenceService[Reference Data Service]
    Bus[(Event Bus)]

    OrderService[Order Service]
    PaymentService[Payment Service]
    CatalogService[Catalog Service]

    ReferenceService -->|ReferenceDataChanged| Bus

    Bus --> OrderService
    Bus --> PaymentService
    Bus --> CatalogService
```

Good when services need local fast reads.

##### Option 3: Shared library or static config

Good for stable standards, such as ISO currency codes.

Be careful with shared libraries. They should not become a way to distribute frequently changing business rules into every service.

---

#### Shared database as a migration step

Sometimes teams cannot immediately move from a shared database to fully isolated databases.

A transitional architecture may look like this:

```mermaid
flowchart TD
    LegacyDB[(Legacy Shared Database)]

    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    OrderTables[(Order-owned tables)]
    PaymentTables[(Payment-owned tables)]
    InventoryTables[(Inventory-owned tables)]

    LegacyDB --> OrderTables
    LegacyDB --> PaymentTables
    LegacyDB --> InventoryTables

    OrderService --> OrderTables
    PaymentService --> PaymentTables
    InventoryService --> InventoryTables
```

This is not ideal, but it may be a practical intermediate stage.

Rules for a transitional shared database:

* define table ownership,
* prevent cross-service writes,
* restrict credentials by schema or table,
* publish APIs for owned data,
* gradually remove direct reads,
* build read models for reporting,
* migrate high-change services first,
* track violations.

The goal should be movement toward clear ownership, not permanent shared-database coupling.

---

#### Anti-pattern: shared database integration

The worst version is when services integrate through database tables.

```mermaid
flowchart TD
    ServiceA[Service A]
    SharedDB[(Shared Database)]
    ServiceB[Service B]

    ServiceA -->|writes table| SharedDB
    ServiceB -->|polls or reads table| SharedDB
```

This is sometimes called database integration.

Problems:

* no clear API contract,
* schema changes break consumers,
* consumers may read partial or invalid state,
* business rules are bypassed,
* ownership is unclear,
* database becomes the integration layer,
* services are not truly independent.

If services need to communicate, use APIs, events, or messages.

---

#### Anti-pattern: one service updates another service’s tables

This is even worse than direct reads.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentDB[(Payment DB)]

    OrderService -. direct update: bad .-> PaymentDB
```

Example:

```sql
UPDATE payments
SET status = 'VOIDED'
WHERE order_id = 'ord_123';
```

This bypasses Payment Service.

Payment Service may need to:

* call a payment gateway,
* create audit records,
* enforce valid state transitions,
* publish `PaymentVoided`,
* update reconciliation records,
* prevent duplicate voids.

A direct database update skips all of that.

Correct approach:

```http
POST /payment-authorizations/pay_123/void
```

Let the Payment Service own payment behavior.

---

#### Handling joins inside a service

Database per Service does not mean a service cannot use joins internally.

Inside one service boundary, joins are fine.

For example, Order Service can join its own order tables:

```sql
SELECT
    o.order_id,
    o.status,
    oi.product_id,
    oi.quantity
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_id = 'ord_123';
```

That is internal to the Order Service.

The rule is:

> Join freely within your service’s data boundary. Do not join across service ownership boundaries.

---

#### Data consistency models

Database per Service requires choosing the right consistency model.

Common models:

| Model                    | Description                          | Example                                       |
| ------------------------ | ------------------------------------ | --------------------------------------------- |
| Strong local consistency | Within one service database          | Order state transition                        |
| Eventual consistency     | Across services                      | Payment status appears after event processing |
| Read-your-writes         | User sees their own submitted update | Profile update confirmation                   |
| Snapshot consistency     | Read model shows a known version     | Dashboard projection                          |
| Best-effort consistency  | Non-critical derived data            | Recommendations                               |

Not all data needs the same consistency.

For example:

* Payment capture should be strongly controlled by Payment Service.
* Search index can be eventually consistent.
* Analytics can lag by minutes.
* Inventory availability may need near-real-time consistency.
* Recommendations can tolerate stale data.

Design consistency based on business needs, not technical preference.

---

#### Example: eventual consistency with events

Suppose Catalog Service owns product data and Search Service owns a search index.

```mermaid
flowchart TD
    CatalogService[Catalog Service]
    CatalogDB[(Catalog DB)]

    Bus[(Event Bus)]

    SearchIndexer[Search Indexer]
    SearchIndex[(Search Index)]

    CatalogService --> CatalogDB
    CatalogService -->|ProductUpdated| Bus

    Bus --> SearchIndexer
    SearchIndexer --> SearchIndex
```

When a product is updated:

1. Catalog Service updates Catalog DB.
2. Catalog Service publishes `ProductUpdated`.
3. Search Indexer consumes the event.
4. Search Index is updated.

For a short time, search results may show old data.

That is eventual consistency.

This is usually acceptable for search.

It may not be acceptable for payment authorization.

---

#### Handling stale reads

Because derived data can be stale, APIs should sometimes expose freshness metadata.

Example:

```json
{
  "orderId": "ord_123",
  "orderStatus": "CONFIRMED",
  "paymentStatus": "AUTHORIZED",
  "shipmentStatus": "PENDING",
  "lastUpdatedAt": "2026-04-29T12:00:00Z",
  "projectionLagMs": 450
}
```

For operational dashboards, freshness matters.

For user-facing screens, you might show:

```text
Updated a few seconds ago
```

or:

```text
Your order is still processing. Check back shortly.
```

A good user experience acknowledges eventual consistency instead of hiding it.

---

#### Data ownership and APIs

When another service needs data, ask:

> Does it need current data, historical data, or a local copy?

Different answers imply different designs.

| Need                       | Better approach                  |
| -------------------------- | -------------------------------- |
| Current authoritative data | Call owning service API          |
| Historical fact            | Store snapshot when event occurs |
| High-volume read           | Build read model                 |
| Search                     | Maintain search index            |
| Analytics                  | Publish to warehouse             |
| Workflow reaction          | Subscribe to event               |
| Local validation           | Replicate small reference data   |

Do not default to direct database reads.

---

#### Example decision: should Payment Service store order amount?

Payment Service needs to authorize a payment for an order amount.

Should it query the Order database every time?

No.

Better options:

1. Order Service sends amount in a payment command.
2. Payment Service stores payment amount locally.
3. Payment Service treats that amount as the payment transaction’s own record.

```json
{
  "commandType": "AuthorizePayment",
  "data": {
    "orderId": "ord_123",
    "amount": 129.99,
    "currency": "USD"
  }
}
```

Payment Service can store:

```sql
CREATE TABLE payment_authorizations (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL
);
```

This is not bad duplication. It is Payment Service recording the amount it was asked to authorize.

---

#### Data privacy and compliance

Database per Service can improve privacy boundaries.

For example, Payment Service may own sensitive payment data.

```mermaid
flowchart TD
    PaymentService[Payment Service]
    PaymentDB[(Payment DB with Sensitive Data)]

    OrderService[Order Service]
    AnalyticsService[Analytics Service]

    PaymentService --> PaymentDB

    OrderService -->|Payment status only| PaymentService
    AnalyticsService -->|Aggregated events only| PaymentService
```

Other services should not directly query payment tables.

This helps enforce:

* least privilege,
* data minimization,
* auditability,
* access control,
* compliance boundaries.

A service can expose only what others need.

For example, Order Service may need:

```json
{
  "paymentStatus": "AUTHORIZED"
}
```

It does not need card tokens, gateway references, fraud details, or bank response payloads.

---

#### Operational implications

Database per Service creates operational responsibilities.

Each service team may need to own:

* database migrations,
* backups,
* restore testing,
* monitoring,
* indexes,
* query performance,
* capacity planning,
* security permissions,
* encryption settings,
* retention policies,
* data deletion workflows,
* schema documentation.

This is a trade-off.

In a monolith, a central database team may handle much of this.

In microservices, teams need enough database ownership maturity to operate their own persistence safely.

---

#### Backup and restore

Each service database needs backup and restore planning.

Questions:

* How often are backups taken?
* How long are backups retained?
* Can the service restore independently?
* What is the recovery point objective?
* What is the recovery time objective?
* Are events needed to rebuild derived data?
* Are read models rebuildable?
* Is sensitive data encrypted in backups?

A derived read model may not need the same backup strategy as a source-of-truth database if it can be rebuilt from events.

```mermaid
flowchart TD
    Events[(Event Stream)]
    Projector[Projector]
    ReadModel[(Read Model)]

    Events --> Projector
    Projector --> ReadModel

    Rebuild[Rebuild if lost]
    Events --> Rebuild
    Rebuild --> ReadModel
```

Source-of-truth databases need stronger backup and recovery guarantees.

---

#### When to use it

Use Database per Service when:

* services need independent deployment,
* services need independent schema evolution,
* teams own different business capabilities,
* services have different scaling needs,
* data ownership boundaries are clear,
* direct database sharing is slowing change,
* services require different storage technologies,
* security or compliance requires data isolation,
* you want to avoid hidden coupling through tables.

It is especially important when services are owned by different teams and expected to evolve independently.

---

#### When not to use it

Avoid or delay Database per Service when:

* the system is small and one team owns everything,
* service boundaries are unclear,
* most operations require strong consistency across all data,
* the team cannot handle distributed consistency,
* reporting depends heavily on ad hoc joins and no data platform exists,
* operational maturity is low,
* a modular monolith would provide enough separation,
* splitting the database would add complexity without real autonomy.

For many systems, a modular monolith with clear module boundaries is a better first step than prematurely splitting databases.

```mermaid
flowchart TD
    ModularMonolith[Modular Monolith]

    OrderModule[Order Module]
    PaymentModule[Payment Module]
    InventoryModule[Inventory Module]

    SharedDB[(Single Database with Module-Owned Tables)]

    ModularMonolith --> OrderModule
    ModularMonolith --> PaymentModule
    ModularMonolith --> InventoryModule

    OrderModule --> SharedDB
    PaymentModule --> SharedDB
    InventoryModule --> SharedDB
```

The important thing is clear ownership. Physical separation can come later if needed.

---

#### Benefits

**1. Service autonomy**

Each service can evolve its schema without coordinating with every other service.

**2. Clear ownership**

Teams know which service owns which data.

**3. Independent deployment**

Database migrations are scoped to the owning service.

**4. Better encapsulation**

Internal tables are not public contracts.

**5. Polyglot persistence**

Services can choose storage technologies that fit their needs.

**6. Improved fault isolation**

A database issue in one service may be contained better than in a shared database.

**7. Stronger security boundaries**

Sensitive data can be isolated behind the owning service.

**8. Reduced accidental coupling**

Services communicate through APIs and events instead of shared tables.

---

#### Trade-offs

**1. Cross-service queries are harder**

You cannot simply join tables across services.

**2. Distributed transactions are harder**

Workflows across services need sagas, compensation, or eventual consistency.

**3. More operational overhead**

More databases mean more migrations, backups, monitoring, and security policies.

**4. Data duplication increases**

Read models, caches, indexes, and snapshots often duplicate data intentionally.

**5. Eventual consistency becomes common**

Derived data may lag behind source-of-truth data.

**6. Reporting requires new architecture**

Analytics usually needs event pipelines, ETL, or a warehouse.

**7. Debugging can be harder**

A business entity may be represented across multiple services.

**8. Boundary mistakes are expensive**

If services are split poorly, data ownership becomes awkward and chatty.

---

#### Common mistakes

**Mistake 1: Splitting services but keeping a shared database**

This creates distributed code with monolithic data coupling.

**Mistake 2: Allowing cross-service writes**

Other services should not update tables they do not own.

**Mistake 3: Treating database tables as integration contracts**

Use APIs, events, or published data products instead.

**Mistake 4: Ignoring cross-service query needs**

Plan read models, aggregation, or analytics pipelines.

**Mistake 5: Expecting ACID transactions across services**

Use Saga or other consistency patterns when workflows span services.

**Mistake 6: Duplicating data without defining source of truth**

Every duplicated field needs an owner.

**Mistake 7: Choosing too many database technologies too early**

Polyglot persistence is useful, but operational complexity grows quickly.

**Mistake 8: No access control enforcement**

If every service can still connect to every database, the boundary is only theoretical.

**Mistake 9: Reporting directly from operational databases**

Use replicated data, events, or a warehouse for reporting.

---

#### Practical design checklist

Before applying Database per Service, ask:

* Which service owns this data?
* Who owns the schema?
* Who owns migrations?
* Which service is allowed to write this data?
* Which service is allowed to read this data directly?
* What API exposes this data?
* What events publish changes to this data?
* Which consumers need a copy?
* Is that copy authoritative or derived?
* How will cross-service queries be handled?
* Is a read model needed?
* Is a search index needed?
* Is an analytics pipeline needed?
* What consistency does the business require?
* Is eventual consistency acceptable?
* What happens if a downstream projection lags?
* Are cross-service transactions needed?
* Should a saga be used?
* Are database credentials scoped correctly?
* How are backups handled?
* How are data retention and deletion handled?
* Does this split improve autonomy enough to justify the complexity?

A Database per Service design is probably healthy if:

* ownership is clear,
* direct cross-service database access is blocked,
* APIs and events are well defined,
* duplicated data has clear source of truth,
* cross-service queries are handled deliberately,
* consistency expectations are explicit,
* service teams can operate their databases,
* schema changes can happen independently.

A design is probably unhealthy if:

* services share tables freely,
* multiple services write the same records,
* reporting depends on direct operational joins,
* no one knows which service owns a field,
* cross-service workflows expect one global transaction,
* data is duplicated without ownership,
* every query requires many synchronous service calls,
* database permissions do not enforce boundaries.

---

#### Related patterns

| Pattern                   | Relationship                                                      |
| ------------------------- | ----------------------------------------------------------------- |
| Saga Pattern              | Coordinates workflows across services with separate databases     |
| Async Messaging           | Publishes changes between services without direct database access |
| Outbox Pattern            | Reliably publishes events after local database transactions       |
| CQRS                      | Builds read models for cross-service queries                      |
| Event Sourcing            | Stores state as events owned by a service                         |
| API Composition           | Combines data from multiple services at request time              |
| Gateway Aggregation       | Client-facing form of API composition                             |
| Choreography              | Services react to events from other services                      |
| Consumer-Driven Contracts | Protects APIs and event schemas between services                  |
| Anti-Corruption Layer     | Protects a service model from external data models                |
| Strangler Fig Pattern     | Helps migrate from shared legacy databases to service-owned data  |

---

#### Summary

Database per Service means each service owns its own database, schema, or persistence boundary. Other services access that data through APIs, events, messages, or derived read models rather than direct database queries.

The central idea is:

> Services should not be coupled through tables. They should communicate through explicit contracts.

This pattern enables service autonomy, independent schema evolution, clearer ownership, better encapsulation, and polyglot persistence.

The trade-off is that cross-service queries and transactions become harder. You need patterns such as API composition, CQRS, read models, Saga, Async Messaging, and Outbox to handle distributed data correctly.

Used well, Database per Service is one of the core patterns that makes microservices truly independent. Used poorly, it can create scattered data, inconsistent copies, and difficult reporting. The difference is disciplined ownership, explicit contracts, and intentional consistency design.


---

### 22. Shared Database

#### What it is

**Shared Database** is a persistence pattern where multiple services use the same physical database, database instance, or database cluster.

In the simplest form, several services connect to one database:

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]
    ReportingService[Reporting Service]

    SharedDB[(Shared Database)]

    OrderService --> SharedDB
    PaymentService --> SharedDB
    InventoryService --> SharedDB
    ReportingService --> SharedDB
```

This is different from **Database per Service**, where every service owns a private persistence boundary.

A shared database can appear in several forms:

| Form                                      | Description                                                                  |
| ----------------------------------------- | ---------------------------------------------------------------------------- |
| Same database, same tables                | Multiple services read and write the same tables                             |
| Same database, separate schemas           | Services share the same database instance but own different schemas          |
| Same database cluster, separate databases | Services use the same database server or cluster but have separate databases |
| Shared legacy database                    | New services connect to a database originally created for a monolith         |
| Shared reporting database                 | Multiple services publish or replicate data into one shared read store       |

The most dangerous version is when multiple services freely read and write the same tables.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    ShippingService[Shipping Service]

    OrdersTable[(orders table)]

    OrderService --> OrdersTable
    PaymentService --> OrdersTable
    ShippingService --> OrdersTable
```

The safer version is when services share infrastructure but ownership is still separated.

```mermaid
flowchart TD
    SharedDatabaseInstance[(Shared Database Instance)]

    OrderSchema[(order_service schema)]
    PaymentSchema[(payment_service schema)]
    InventorySchema[(inventory_service schema)]

    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    SharedDatabaseInstance --> OrderSchema
    SharedDatabaseInstance --> PaymentSchema
    SharedDatabaseInstance --> InventorySchema

    OrderService --> OrderSchema
    PaymentService --> PaymentSchema
    InventoryService --> InventorySchema
```

The central idea is:

> Sharing database infrastructure can be useful, but sharing data ownership is dangerous.

A shared database is sometimes a practical compromise. It should be used deliberately, with clear ownership rules.

---

#### Why this pattern exists

Shared Database exists because real systems often cannot move directly from a monolith to perfect service-owned databases.

A legacy monolith may already have one large database:

```mermaid
flowchart TD
    Monolith[Legacy Monolith]
    LegacyDB[(Legacy Database)]

    Monolith --> LegacyDB
```

During migration, teams may start extracting services while the old database still contains the business data.

```mermaid
flowchart TD
    Monolith[Legacy Monolith]
    OrderService[New Order Service]
    CustomerService[New Customer Service]

    LegacyDB[(Legacy Database)]

    Monolith --> LegacyDB
    OrderService --> LegacyDB
    CustomerService --> LegacyDB
```

This can be a useful intermediate step because it lets teams extract behavior before fully separating data.

Shared databases also appear in smaller systems where the cost of operating many databases is not justified yet.

For example, one team may own all services, the system is small, and all services are deployed together.

```mermaid
flowchart TD
    APIService[API Service]
    WorkerService[Worker Service]
    AdminService[Admin Service]

    SharedDB[(Application Database)]

    APIService --> SharedDB
    WorkerService --> SharedDB
    AdminService --> SharedDB
```

This can be reasonable if the services are not truly independent yet.

The danger is when the shared database remains after services are expected to evolve independently.

---

#### What it solves

Shared Database solves several short-term problems.

**1. It reduces operational complexity**

One database is easier to operate than many databases.

There may be fewer:

* database clusters,
* backups,
* monitoring dashboards,
* replication setups,
* credentials,
* migrations,
* restore procedures,
* database technologies.

**2. It simplifies cross-data queries**

Joining data is easy when all tables are in one database:

```sql
SELECT
    o.order_id,
    o.status AS order_status,
    p.status AS payment_status,
    s.status AS shipment_status
FROM orders o
JOIN payments p ON p.order_id = o.order_id
JOIN shipments s ON s.order_id = o.order_id
WHERE o.customer_id = 'cus_123';
```

This is much harder when Order, Payment, and Shipping data are owned by separate services.

**3. It supports gradual migration**

During monolith extraction, direct database access may allow a new service to work before full ownership boundaries are established.

**4. It can reduce duplication**

A shared database can avoid creating read models, event projections, and duplicated snapshots early in a system’s life.

**5. It can make reporting easier**

Reporting tools can query one database instead of combining data from many services.

These are real benefits. The pattern exists because it is sometimes practical.

But the trade-off is coupling.

---

#### The main risk: database-level coupling

The biggest problem with a shared database is that services can become coupled through tables instead of explicit contracts.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    SharedDB[(Shared Database)]

    OrdersTable[(orders)]
    PaymentsTable[(payments)]
    InventoryTable[(inventory)]

    SharedDB --> OrdersTable
    SharedDB --> PaymentsTable
    SharedDB --> InventoryTable

    OrderService --> OrdersTable
    PaymentService --> OrdersTable
    PaymentService --> PaymentsTable
    InventoryService --> OrdersTable
    InventoryService --> InventoryTable
```

In this design, the `orders` table is effectively a public API.

If Order Service changes the table, it may break Payment Service or Inventory Service.

For example, this change may seem internal:

```sql
ALTER TABLE orders RENAME COLUMN total_amount TO total_amount_cents;
```

But if another service has this query:

```sql
SELECT total_amount
FROM orders
WHERE order_id = 'ord_123';
```

that service breaks.

The problem is not just the physical database. The problem is that services now depend on each other’s internal data structures.

---

#### Shared database vs shared schema ownership

A shared database is not always equally dangerous.

There is a spectrum.

##### High-risk shared ownership

Multiple services read and write the same tables.

```mermaid
flowchart TD
    ServiceA[Service A]
    ServiceB[Service B]
    ServiceC[Service C]

    SharedTable[(shared table)]

    ServiceA --> SharedTable
    ServiceB --> SharedTable
    ServiceC --> SharedTable
```

This creates strong coupling and unclear ownership.

##### Medium-risk shared database with table ownership

Services share one database, but each table has an owner.

```mermaid
flowchart TD
    SharedDB[(Shared Database)]

    OrderTables[(Order-owned tables)]
    PaymentTables[(Payment-owned tables)]
    InventoryTables[(Inventory-owned tables)]

    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    SharedDB --> OrderTables
    SharedDB --> PaymentTables
    SharedDB --> InventoryTables

    OrderService --> OrderTables
    PaymentService --> PaymentTables
    InventoryService --> InventoryTables
```

This is better, but still risky if access control is not enforced.

##### Lower-risk shared infrastructure

Services share a database server or cluster, but each service owns a separate database or schema.

```mermaid
flowchart TD
    DatabaseCluster[(Database Cluster)]

    OrderDB[(Order Database)]
    PaymentDB[(Payment Database)]
    InventoryDB[(Inventory Database)]

    OrderService[Order Service]
    PaymentService[Payment Service]
    InventoryService[Inventory Service]

    DatabaseCluster --> OrderDB
    DatabaseCluster --> PaymentDB
    DatabaseCluster --> InventoryDB

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    InventoryService --> InventoryDB
```

This reduces operational overhead while preserving stronger ownership boundaries.

When people say “shared database,” always clarify which version they mean.

---

#### When a shared database is a reasonable compromise

A shared database can be reasonable when it is used intentionally and temporarily.

Good situations include:

* early-stage systems,
* small teams,
* modular monoliths,
* monolith migration,
* reporting databases,
* transitional Strangler Fig migration,
* low-risk internal tools,
* services that are deployed together,
* services owned by one team with no need for independent schema evolution.

For example, during monolith migration:

```mermaid
flowchart TD
    Client[Client]
    Router[Router or API Gateway]

    Monolith[Legacy Monolith]
    NewCatalog[New Catalog Service]

    LegacyDB[(Legacy Database)]

    Client --> Router

    Router -->|unmigrated routes| Monolith
    Router -->|catalog routes| NewCatalog

    Monolith --> LegacyDB
    NewCatalog --> LegacyDB
```

This may be acceptable as a migration step.

But the target state should be clearer ownership:

```mermaid
flowchart TD
    Client[Client]
    Router[Router or API Gateway]

    Monolith[Legacy Monolith]
    CatalogService[Catalog Service]

    LegacyDB[(Legacy Database)]
    CatalogDB[(Catalog Database)]

    Client --> Router

    Router --> Monolith
    Router --> CatalogService

    Monolith --> LegacyDB
    CatalogService --> CatalogDB
```

The shared database is the bridge, not the destination.

---

#### When a shared database becomes an anti-pattern

A shared database becomes an anti-pattern when services are supposed to be independent but remain coupled through database tables.

Warning signs:

* multiple services write the same table,
* no one knows which service owns a table,
* schema changes require many teams to coordinate,
* business rules are implemented in stored procedures used by several services,
* one service bypasses another service’s validation logic by writing directly to its tables,
* services cannot be deployed independently because of database dependencies,
* table columns become de facto public API fields,
* reporting queries overload production tables,
* teams are afraid to change schemas,
* the database becomes the integration layer.

This design may look like microservices, but the shared database acts like a monolithic core.

```mermaid
flowchart TD
    ServiceA[Service A]
    ServiceB[Service B]
    ServiceC[Service C]
    ServiceD[Service D]

    SharedDB[(Shared Database<br/>hidden monolith)]

    ServiceA --> SharedDB
    ServiceB --> SharedDB
    ServiceC --> SharedDB
    ServiceD --> SharedDB
```

The services are physically separate, but logically coupled.

---

#### Example: dangerous shared write access

Suppose Order Service owns order lifecycle.

Order Service expects valid transitions:

```text
PENDING -> CONFIRMED -> SHIPPED -> DELIVERED
PENDING -> CANCELLED
CONFIRMED -> CANCELLED
```

But Payment Service directly updates the `orders` table:

```sql
UPDATE orders
SET status = 'CONFIRMED'
WHERE order_id = 'ord_123';
```

This bypasses Order Service.

Order Service may normally do additional work when confirming an order:

* validate current state,
* record an audit entry,
* publish `OrderConfirmed`,
* update order history,
* enforce fraud checks,
* verify inventory reservation,
* notify downstream services.

A direct table update skips all of that.

Better:

```http
POST /orders/ord_123/confirm
Content-Type: application/json

{
  "paymentId": "pay_456",
  "inventoryReservationId": "res_789"
}
```

Then Order Service owns the transition.

The database table should not be the command interface.

---

#### Example: acceptable read-only reporting copy

A shared database can be acceptable when it is a derived reporting database, not an operational database.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    ShippingService[Shipping Service]

    EventBus[(Event Bus)]

    ReportingProjector[Reporting Projector]
    ReportingDB[(Shared Reporting Database)]

    BI[BI Tool]
    FinanceReports[Finance Reports]
    OpsDashboard[Ops Dashboard]

    OrderService -->|Order events| EventBus
    PaymentService -->|Payment events| EventBus
    ShippingService -->|Shipping events| EventBus

    EventBus --> ReportingProjector
    ReportingProjector --> ReportingDB

    BI --> ReportingDB
    FinanceReports --> ReportingDB
    OpsDashboard --> ReportingDB
```

In this design:

* service databases remain private,
* reporting queries do not hit operational databases,
* the reporting database is derived,
* the source of truth remains with the owning services.

This is different from multiple services directly sharing operational tables.

---

#### Example: shared database with schema ownership

A controlled compromise is to share one database instance but separate schemas by service.

```sql
CREATE SCHEMA order_service;
CREATE SCHEMA payment_service;
CREATE SCHEMA inventory_service;
```

Order Service tables:

```sql
CREATE TABLE order_service.orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL
);
```

Payment Service tables:

```sql
CREATE TABLE payment_service.payment_authorizations (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL
);
```

Inventory Service tables:

```sql
CREATE TABLE inventory_service.inventory_reservations (
    reservation_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL
);
```

Then enforce credentials:

```text
order_service_user can access order_service schema only.
payment_service_user can access payment_service schema only.
inventory_service_user can access inventory_service schema only.
```

This allows shared database infrastructure while still enforcing data ownership.

The important part is not just naming schemas. It is preventing cross-service access.

---

#### Access control is critical

If a shared database is used, access control must enforce ownership.

Bad:

```text
Every service uses the same database username and password.
```

Better:

```text
Order Service uses order_service_user.
Payment Service uses payment_service_user.
Inventory Service uses inventory_service_user.
```

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]

    OrderSchema[(order_service schema)]
    PaymentSchema[(payment_service schema)]

    OrderService -->|allowed| OrderSchema
    PaymentService -->|allowed| PaymentSchema

    OrderService -. denied .-> PaymentSchema
    PaymentService -. denied .-> OrderSchema
```

Database permissions can prevent accidental boundary violations.

Example:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA order_service
TO order_service_user;

REVOKE ALL
ON ALL TABLES IN SCHEMA order_service
FROM payment_service_user;
```

A boundary that exists only in documentation is weak. A boundary enforced by credentials is much stronger.

---

#### Stored procedures and triggers

Shared databases often accumulate stored procedures, triggers, and database-level business logic.

For example:

```sql
CREATE TRIGGER update_order_status_after_payment
AFTER INSERT ON payments
FOR EACH ROW
EXECUTE FUNCTION confirm_order_if_paid();
```

This may seem convenient, but it can hide business behavior inside the database.

Problems:

* business rules are no longer owned by a service,
* behavior is harder to test with service code,
* deployments require database coordination,
* multiple services may depend on hidden side effects,
* debugging becomes harder,
* local development environments become harder to reproduce.

This does not mean stored procedures are always bad. They can be useful for local data integrity or performance-sensitive operations inside a service boundary.

But be careful when database logic coordinates behavior across service boundaries.

```mermaid
flowchart TD
    PaymentService[Payment Service]
    SharedDB[(Shared Database)]

    Trigger[Database Trigger<br/>updates order status]
    OrderService[Order Service]

    PaymentService --> SharedDB
    SharedDB --> Trigger
    Trigger -. hidden behavior .-> OrderService
```

If the business behavior belongs to Order Service, put it in Order Service.

---

#### Reporting and joins

One of the biggest benefits of a shared database is easy reporting.

For example:

```sql
SELECT
    c.customer_id,
    c.email,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount_cents) AS lifetime_value_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.email;
```

This is simple and powerful.

But using the operational shared database for reporting has risks:

* long queries can slow down production traffic,
* reports depend on internal schemas,
* schema changes break reports,
* sensitive data may be exposed,
* reporting teams may create unofficial business definitions,
* indexes added for reports may affect write performance.

A better long-term approach is often a separate reporting store:

```mermaid
flowchart TD
    OperationalDB[(Operational Shared DB)]
    CDC[Change Data Capture]
    ReportingDB[(Reporting DB)]
    BI[BI Tool]

    OperationalDB --> CDC
    CDC --> ReportingDB
    BI --> ReportingDB
```

Or event-based reporting:

```mermaid
flowchart TD
    Services[Services]
    EventStream[(Event Stream)]
    Warehouse[(Data Warehouse)]
    Reports[Reports]

    Services --> EventStream
    EventStream --> Warehouse
    Reports --> Warehouse
```

This keeps heavy reporting away from operational workloads.

---

#### Shared database during Strangler Fig migration

Shared Database is common during Strangler Fig migrations.

At first, the monolith owns everything:

```mermaid
flowchart TD
    Client[Client]
    Monolith[Monolith]
    DB[(Monolith Database)]

    Client --> Monolith
    Monolith --> DB
```

Then a new service is extracted but still reads the old database:

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway]

    Monolith[Monolith]
    CatalogService[Catalog Service]

    DB[(Monolith Database)]

    Client --> Gateway

    Gateway --> Monolith
    Gateway --> CatalogService

    Monolith --> DB
    CatalogService --> DB
```

Then the service starts owning its own database:

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway]

    Monolith[Monolith]
    CatalogService[Catalog Service]

    LegacyDB[(Legacy Database)]
    CatalogDB[(Catalog Database)]

    Client --> Gateway

    Gateway --> Monolith
    Gateway --> CatalogService

    Monolith --> LegacyDB
    CatalogService --> CatalogDB
```

Finally, the monolith stops owning that capability:

```mermaid
flowchart TD
    Client[Client]
    Gateway[Gateway]

    CatalogService[Catalog Service]
    CatalogDB[(Catalog Database)]

    Client --> Gateway
    Gateway --> CatalogService
    CatalogService --> CatalogDB
```

The shared database helped the migration start, but the end state removed the coupling.

---

#### Transitional ownership rules

If you use a shared database as a transition, define rules.

A practical rule set might be:

| Rule                                                    | Reason                           |
| ------------------------------------------------------- | -------------------------------- |
| Every table has one owning service                      | Avoid unclear ownership          |
| Only the owner writes the table                         | Prevent bypassing business rules |
| Non-owners may read only through approved views or APIs | Limit schema coupling            |
| New cross-service reads require review                  | Prevent coupling from growing    |
| Cross-service writes are forbidden                      | Preserve data integrity          |
| Migrations are owned by the table owner                 | Keep accountability clear        |
| Reporting uses replicas or views                        | Protect operational workloads    |
| Violations are tracked as migration debt                | Keep transition temporary        |

You can document ownership like this:

```yaml
tables:
  orders:
    owner: order-service
    allowedWriters:
      - order-service
    allowedReaders:
      - reporting-readonly-user

  payment_authorizations:
    owner: payment-service
    allowedWriters:
      - payment-service
    allowedReaders:
      - reporting-readonly-user

  inventory_reservations:
    owner: inventory-service
    allowedWriters:
      - inventory-service
    allowedReaders: []
```

This makes the compromise explicit.

---

#### Database views as a compromise

Sometimes you can reduce coupling by exposing database views instead of raw tables.

For example, Order Service owns internal order tables, but exposes a stable read-only view:

```sql
CREATE VIEW reporting.order_summary AS
SELECT
    order_id,
    customer_id,
    status,
    total_amount_cents,
    currency,
    created_at
FROM order_service.orders;
```

Reporting tools read:

```sql
SELECT *
FROM reporting.order_summary
WHERE customer_id = 'cus_123';
```

This is better than exposing every internal table.

But views still create database-level contracts. If many services depend on them, they must be versioned and governed.

A view can be a useful transitional tool, but it should not become a substitute for proper APIs, events, or read models when services need independence.

---

#### Change Data Capture

Change Data Capture, or CDC, can help move away from direct shared database access.

CDC reads database changes and publishes them to a stream.

```mermaid
flowchart TD
    SharedDB[(Shared Database)]
    CDC[Change Data Capture]
    EventStream[(Event Stream)]

    SearchIndexer[Search Indexer]
    ReportingProjector[Reporting Projector]
    NewService[New Service]

    SharedDB --> CDC
    CDC --> EventStream

    EventStream --> SearchIndexer
    EventStream --> ReportingProjector
    EventStream --> NewService
```

This lets consumers stop querying the database directly.

For example, instead of Reporting Service querying `orders` directly, it consumes order changes and builds its own reporting store.

CDC can be useful during migration, but it has its own challenges:

* schema changes affect CDC consumers,
* delete handling must be designed,
* events may be low-level database changes rather than business events,
* consumers may become coupled to table structure,
* sensitive data must be filtered,
* ordering and replay need attention.

CDC is powerful, but it should be governed carefully.

---

#### Shared database and transactions

A shared database can make transactions across tables easy.

For example:

```sql
BEGIN;

INSERT INTO orders (...);
INSERT INTO payment_authorizations (...);
UPDATE inventory
SET available_quantity = available_quantity - 1
WHERE product_id = 'prod_123';

COMMIT;
```

This is one of the reasons shared databases are appealing.

But it can also hide poor service boundaries.

If Order Service, Payment Service, and Inventory Service are supposed to be independent, one database transaction across their tables means they are not truly autonomous.

```mermaid
flowchart TD
    Transaction[Single Database Transaction]

    OrdersTable[(orders)]
    PaymentsTable[(payments)]
    InventoryTable[(inventory)]

    Transaction --> OrdersTable
    Transaction --> PaymentsTable
    Transaction --> InventoryTable
```

This may be fine inside a modular monolith.

It is less appropriate if each table is owned by a different independently deployed service.

In microservices, cross-service consistency is usually handled with Saga, Outbox, events, or other distributed consistency patterns.

---

#### Shared database vs modular monolith

A shared database is often a good fit for a modular monolith.

In a modular monolith, modules are part of one deployable application, but internal boundaries are still clear.

```mermaid
flowchart TD
    ModularMonolith[Modular Monolith]

    OrderModule[Order Module]
    PaymentModule[Payment Module]
    InventoryModule[Inventory Module]

    SharedDB[(Shared Database)]

    ModularMonolith --> OrderModule
    ModularMonolith --> PaymentModule
    ModularMonolith --> InventoryModule

    OrderModule --> SharedDB
    PaymentModule --> SharedDB
    InventoryModule --> SharedDB
```

This can be a strong architecture when:

* one team owns the system,
* deployment is unified,
* transactions are important,
* operational simplicity matters,
* service boundaries are still evolving.

A modular monolith can still enforce table ownership in code.

The problem comes when teams split deployment and ownership but keep the database coupled.

```mermaid
flowchart TD
    OrderService[Independently deployed Order Service]
    PaymentService[Independently deployed Payment Service]
    InventoryService[Independently deployed Inventory Service]

    SharedDB[(Shared Database)]

    OrderService --> SharedDB
    PaymentService --> SharedDB
    InventoryService --> SharedDB
```

This can create the worst of both worlds: distributed services with monolithic data coupling.

---

#### How to migrate away from a shared database

A common migration path looks like this:

```mermaid
flowchart TD
    Step1[1. Identify table ownership]
    Step2[2. Stop cross-service writes]
    Step3[3. Replace direct reads with APIs or views]
    Step4[4. Publish events from owners]
    Step5[5. Build read models for consumers]
    Step6[6. Move owned tables to service database]
    Step7[7. Remove legacy access]

    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
    Step5 --> Step6
    Step6 --> Step7
```

A practical sequence:

1. Inventory all tables.
2. Assign each table an owning service.
3. Find all services reading and writing each table.
4. Remove cross-service writes first.
5. Replace cross-service reads with APIs or events.
6. Create read models for reporting and dashboards.
7. Add database credentials that enforce ownership.
8. Move tables to service-owned databases.
9. Delete old direct access paths.

This migration can take time. The important thing is to reduce coupling intentionally.

---

#### Example migration: remove direct payment read from Order Service

Initial state:

```mermaid
flowchart TD
    OrderService[Order Service]
    SharedDB[(Shared Database)]
    PaymentsTable[(payments table)]

    OrderService --> SharedDB
    SharedDB --> PaymentsTable
```

Order Service queries payment status:

```sql
SELECT status
FROM payments
WHERE order_id = 'ord_123';
```

Step 1: Payment Service exposes an API:

```http
GET /payments/by-order/ord_123
```

Step 2: Order Service uses the API:

```ts
async function getPaymentStatus(orderId: string): Promise<PaymentStatus> {
  const response = await fetch(
    `http://payment-service/payments/by-order/${orderId}`
  );

  if (!response.ok) {
    throw new Error("Payment status unavailable");
  }

  const payment = await response.json();

  return payment.status;
}
```

Step 3: Remove Order Service’s database permission to `payments`.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    PaymentDB[(Payment-owned tables)]

    OrderService -->|Payment API| PaymentService
    PaymentService --> PaymentDB
```

Now Payment Service owns payment data.

---

#### Performance considerations

A shared database can become a performance bottleneck.

Problems include:

* too many services compete for the same connection pool,
* one service’s expensive query slows others,
* reporting queries lock or overload tables,
* indexing choices conflict between workloads,
* write-heavy services affect read-heavy services,
* database scaling becomes all-or-nothing.

```mermaid
flowchart TD
    APIService[API Service]
    WorkerService[Worker Service]
    ReportingService[Reporting Service]
    AdminService[Admin Service]

    SharedDB[(Shared Database)]

    APIService --> SharedDB
    WorkerService --> SharedDB
    ReportingService --> SharedDB
    AdminService --> SharedDB

    SharedDB --> Bottleneck[Shared bottleneck]
```

Mitigations:

* use read replicas for reporting,
* separate schemas or databases,
* enforce query timeouts,
* limit service credentials,
* monitor query patterns by service,
* isolate high-volume workloads,
* use materialized views or read models,
* move hot services to their own database.

A shared database that works at low scale may become a bottleneck at higher scale.

---

#### Security considerations

Shared databases increase the blast radius of credential leaks and access mistakes.

If every service uses broad database credentials, one compromised service may expose all data.

Bad:

```text
service_user has access to all tables.
```

Better:

```text
order_service_user has access only to order-owned tables.
payment_service_user has access only to payment-owned tables.
reporting_user has read-only access to reporting views.
```

Also consider:

* encryption at rest,
* audit logs by database user,
* least privilege,
* row-level security where appropriate,
* masking sensitive data in reporting views,
* separating regulated data,
* restricting production console access,
* rotating credentials,
* avoiding shared passwords.

Shared infrastructure does not mean shared unrestricted access.

---

#### Schema migration risk

In a shared database, migrations can affect many services.

Example migration:

```sql
ALTER TABLE customers DROP COLUMN phone_number;
```

If five services read `customers.phone_number`, this breaks them.

To reduce risk:

* use expand-and-contract migrations,
* avoid destructive changes until consumers migrate,
* track column usage,
* use views as stable compatibility layers,
* run database migration tests,
* communicate ownership,
* apply consumer-driven contracts for database-facing views or APIs,
* monitor query logs for deprecated columns.

An expand-and-contract migration:

```mermaid
flowchart TD
    Add[Add new column]
    DualWrite[Write old and new]
    MigrateReaders[Move readers to new column]
    Backfill[Backfill data]
    StopOldReads[Stop old reads]
    Remove[Remove old column]

    Add --> DualWrite
    DualWrite --> MigrateReaders
    MigrateReaders --> Backfill
    Backfill --> StopOldReads
    StopOldReads --> Remove
```

Never assume a column is unused just because one team does not use it.

---

#### How to keep a shared database controlled

If you must use a shared database, keep it controlled.

Recommended practices:

**1. Define ownership**

Every table, view, and schema should have an owner.

**2. Enforce access controls**

Do not use one shared database user for all services.

**3. Ban cross-service writes**

Only the owner writes owned data.

**4. Limit cross-service reads**

Prefer APIs, events, or read models.

**5. Use views for transitional read access**

Expose stable read-only views instead of internal tables.

**6. Monitor queries by service**

Know which services access which tables.

**7. Version database contracts**

If a view is consumed by multiple services, version it.

**8. Separate reporting from operations**

Use replicas, warehouses, or projections.

**9. Treat violations as migration debt**

Track them and remove them over time.

**10. Have an exit plan**

A transitional shared database should have a path toward stronger ownership.

---

#### When to use it

Use Shared Database when:

* the system is small,
* one team owns all services,
* services are not independently deployed,
* operational simplicity matters more than autonomy,
* you are migrating from a monolith,
* service boundaries are still being discovered,
* cross-service transactions are temporarily required,
* reporting needs are not yet served by a data platform,
* the shared database is a deliberate transitional compromise.

It is often reasonable as an intermediate step during migration.

It is less ideal as the target architecture for independently owned microservices.

---

#### When not to use it

Avoid Shared Database when:

* services are owned by different teams,
* services need independent deployment,
* schemas change frequently,
* each service needs independent scaling,
* teams need different storage technologies,
* security boundaries matter,
* services directly write each other’s tables,
* database migrations are blocking releases,
* the shared database is becoming the integration layer,
* cross-service coupling is already painful.

In those cases, prefer Database per Service, APIs, events, read models, and data pipelines.

---

#### Benefits

**1. Lower operational complexity**

One database is easier to manage than many.

**2. Easier joins**

Cross-domain queries are simpler when data is in one database.

**3. Easier reporting at first**

BI tools and reports can query one place.

**4. Faster early migration**

New services can be extracted before full data separation.

**5. Simpler transactions**

A single database can provide local ACID transactions across tables.

**6. Lower infrastructure cost**

Fewer database clusters may reduce cost and operational overhead.

**7. Familiar development model**

Teams can use traditional relational database techniques.

---

#### Trade-offs

**1. Database-level coupling**

Services become coupled through schemas and tables.

**2. Reduced service autonomy**

Schema changes require coordination across services.

**3. Unclear ownership**

Multiple services may depend on the same tables.

**4. Business rules can be bypassed**

Direct writes skip the owning service’s validation and events.

**5. Shared performance bottleneck**

One service’s workload can affect others.

**6. Security blast radius**

Broad database access can expose too much data.

**7. Harder independent deployment**

Database changes can block service releases.

**8. Migration debt**

Temporary shared access often becomes permanent unless actively managed.

---

#### Common mistakes

**Mistake 1: Calling it microservices while sharing all tables**

If services depend on the same tables, they are not truly autonomous.

**Mistake 2: Allowing multiple services to write the same table**

This creates unclear business ownership and data corruption risk.

**Mistake 3: Using one database user for all services**

This makes boundaries unenforceable.

**Mistake 4: Treating table schemas as public APIs**

Use APIs, events, views, or read models instead.

**Mistake 5: Letting reporting query production tables directly**

Heavy reporting can degrade operational workloads.

**Mistake 6: No table ownership map**

If no one owns a table, everyone and no one owns it.

**Mistake 7: No migration plan**

A transitional shared database becomes permanent coupling.

**Mistake 8: Hiding workflows in triggers and stored procedures**

Business behavior becomes invisible to service owners.

**Mistake 9: Ignoring schema change impact**

A small table change can break many services.

---

#### Practical design checklist

Before using a shared database, ask:

* Why are we sharing the database?
* Is this a target architecture or a transition?
* Which services use the database?
* Which tables does each service own?
* Which service is allowed to write each table?
* Are any tables written by multiple services?
* Are cross-service writes forbidden?
* Are database credentials scoped by service?
* Are reporting queries isolated from production workloads?
* Are direct reads temporary or permanent?
* Can direct reads be replaced with APIs or events?
* Are views needed as compatibility boundaries?
* Who owns each migration?
* How are schema changes reviewed?
* Which services depend on each table or column?
* How are sensitive data permissions enforced?
* What is the plan to move toward stronger ownership?
* What monitoring shows query load by service?
* What happens if one service overloads the database?
* Is a modular monolith more honest than distributed services with shared data?

A shared database design is probably healthy if:

* it is intentional,
* ownership is documented,
* access control is enforced,
* cross-service writes are blocked,
* reporting is isolated,
* schema changes are governed,
* migration debt is tracked,
* there is an exit plan where needed.

A shared database design is probably unhealthy if:

* every service can read and write everything,
* no one owns tables,
* services break when another team changes a column,
* business rules live in triggers used by many services,
* reporting queries slow production,
* database access replaces APIs and events,
* the shared database is the only integration mechanism.

---

#### Related patterns

| Pattern                   | Relationship                                                                  |
| ------------------------- | ----------------------------------------------------------------------------- |
| Database per Service      | Preferred target when services need autonomy                                  |
| Strangler Fig Pattern     | Shared databases often appear during gradual migration                        |
| Anti-Corruption Layer     | Can protect new services from legacy database models                          |
| Outbox Pattern            | Helps publish changes reliably from service-owned data                        |
| Change Data Capture       | Can replicate shared database changes into streams or read models             |
| CQRS                      | Replaces cross-service joins with query-optimized read models                 |
| Gateway Aggregation       | Alternative to direct joins for client-facing reads                           |
| Saga Pattern              | Replaces single shared-database transactions across service boundaries        |
| Consumer-Driven Contracts | Helps protect API or view contracts during migration                          |
| Modular Monolith          | Often a better fit when one shared database and one deployment are acceptable |

---

#### Summary

Shared Database means multiple services use the same physical database, database instance, or database cluster.

The central idea is:

> Sharing database infrastructure can reduce complexity, but sharing data ownership can recreate monolithic coupling.

This pattern can be useful for small systems, modular monoliths, reporting databases, and transitional migrations from legacy systems.

The danger is that services become coupled through tables. If multiple services read and write the same schema freely, the database becomes the real integration layer and the services lose autonomy.

A healthy shared database approach has:

* clear table ownership,
* scoped credentials,
* no cross-service writes,
* controlled read access,
* isolated reporting,
* governed schema changes,
* and a migration plan if service autonomy is the goal.

Used carefully, Shared Database can be a practical compromise. Used casually, it becomes a distributed monolith with a shared data core.


---

### 23. CQRS

#### What it is

**CQRS**, or **Command Query Responsibility Segregation**, is a pattern that separates operations that **change state** from operations that **read state**.

In CQRS:

* **Commands** perform writes.
* **Queries** perform reads.
* The write side focuses on correctness and business rules.
* The read side focuses on fast, convenient queries.

The simplest idea is:

> Do not force the same model to handle both complex business writes and complex application reads.

A basic CQRS structure looks like this:

```mermaid
flowchart TD
    Client[Client]

    CommandAPI[Command API]
    QueryAPI[Query API]

    WriteModel[Write Model]
    ReadModel[Read Model]

    WriteDB[(Write Database)]
    ReadDB[(Read Database)]

    Client -->|Commands| CommandAPI
    Client -->|Queries| QueryAPI

    CommandAPI --> WriteModel
    WriteModel --> WriteDB

    QueryAPI --> ReadModel
    ReadModel --> ReadDB
```

A command changes the system:

```http
POST /orders
Content-Type: application/json

{
  "customerId": "cus_123",
  "items": [
    {
      "productId": "prod_456",
      "quantity": 1
    }
  ]
}
```

A query reads from the system:

```http
GET /orders/ord_123/summary
```

The command side may store normalized, rule-focused data. The query side may store denormalized, screen-friendly data.

---

#### Why this pattern exists

In many applications, the model needed for writes is not the same as the model needed for reads.

A write model often needs to enforce business rules.

For example, an Order Service write model may need to answer:

* Can this order be created?
* Is the customer allowed to order?
* Are the items valid?
* Can this order be cancelled?
* Is this state transition allowed?
* Should this command be rejected?
* What events should be emitted?

A read model often needs to answer different questions:

* Show the customer’s order history.
* Show order, payment, shipment, and refund status together.
* Show a dashboard of recent activity.
* Show a product page with price, availability, reviews, and recommendations.
* Show a support agent everything needed to help a customer.

Trying to satisfy both needs with one model can make the system awkward.

```mermaid
flowchart TD
    OneModel[One Shared Model]

    Writes[Complex Writes<br/>business rules<br/>state transitions<br/>validation]
    Reads[Complex Reads<br/>dashboards<br/>joins<br/>search<br/>summaries]

    OneModel --> Writes
    OneModel --> Reads

    Problem[Model becomes overloaded]
    Writes --> Problem
    Reads --> Problem
```

CQRS separates these concerns.

```mermaid
flowchart TD
    WriteModel[Write Model<br/>correctness and rules]
    ReadModel[Read Model<br/>fast queries and views]

    Commands[Commands] --> WriteModel
    Queries[Queries] --> ReadModel
```

This lets each side be designed for its own job.

---

#### What it solves

CQRS solves the problem of **one model trying to serve two different purposes**.

Without CQRS, an application may use one database schema for everything:

```mermaid
flowchart TD
    App[Application]
    DB[(Single Database Model)]

    CreateOrder[Create Order]
    CancelOrder[Cancel Order]
    OrderSummary[Order Summary Page]
    CustomerDashboard[Customer Dashboard]
    AdminReport[Admin Report]

    App --> DB

    CreateOrder --> DB
    CancelOrder --> DB
    OrderSummary --> DB
    CustomerDashboard --> DB
    AdminReport --> DB
```

That can work for simple systems. But as complexity grows, the single model may struggle.

Problems appear when:

* write transactions need normalized consistency,
* reads need large joins,
* dashboards need denormalized data,
* search needs indexed documents,
* reads are much more frequent than writes,
* different teams need different query shapes,
* read permissions differ from write permissions,
* query performance requirements differ from write performance requirements.

CQRS allows separate models:

```mermaid
flowchart TD
    Commands[Commands]
    Queries[Queries]

    WriteSide[Write Side<br/>normalized<br/>transactional<br/>rule-focused]
    ReadSide[Read Side<br/>denormalized<br/>query-focused<br/>fast]

    Commands --> WriteSide
    Queries --> ReadSide
```

The write side protects correctness. The read side optimizes retrieval.

---

#### Commands

A **command** is a request to change state.

Commands are usually named with imperative verbs:

* `CreateOrder`
* `CancelOrder`
* `AuthorizePayment`
* `ReserveInventory`
* `UpdateCustomerAddress`
* `ActivateSubscription`
* `ApproveLoanApplication`
* `IssueRefund`

A command expresses intent.

Example:

```json
{
  "commandType": "CancelOrder",
  "commandId": "cmd_123",
  "data": {
    "orderId": "ord_456",
    "reason": "CUSTOMER_REQUESTED"
  }
}
```

A command may succeed or fail.

For example, `CancelOrder` may fail if the order has already shipped.

```ts
type OrderStatus =
  | "PENDING"
  | "CONFIRMED"
  | "SHIPPED"
  | "CANCELLED";

type Order = {
  orderId: string;
  status: OrderStatus;
};

function cancelOrder(order: Order): Order {
  if (order.status === "SHIPPED") {
    throw new Error("Cannot cancel an order that has already shipped");
  }

  if (order.status === "CANCELLED") {
    return order;
  }

  return {
    ...order,
    status: "CANCELLED"
  };
}
```

The command side owns this business rule.

---

#### Queries

A **query** reads data without changing state.

Queries are usually named around what they return:

* `GetOrderSummary`
* `ListCustomerOrders`
* `SearchProducts`
* `GetAccountDashboard`
* `GetShipmentTracking`
* `GetInvoiceHistory`
* `GetAdminCustomerView`

A query should not change the system.

Example:

```http
GET /customers/cus_123/orders
```

Response:

```json
{
  "customerId": "cus_123",
  "orders": [
    {
      "orderId": "ord_456",
      "status": "CONFIRMED",
      "totalAmount": 129.99,
      "currency": "USD",
      "estimatedDeliveryDate": "2026-05-03"
    }
  ]
}
```

The query side can be optimized for exactly this response shape.

It does not need to enforce order cancellation rules or payment authorization rules. It needs to answer read requests efficiently.

---

#### Basic CQRS without separate databases

CQRS does not always require separate physical databases.

At its simplest, CQRS can mean separating command code from query code while using the same database.

```mermaid
flowchart TD
    Client[Client]

    CommandHandler[Command Handlers]
    QueryHandler[Query Handlers]

    DB[(Same Database)]

    Client -->|Commands| CommandHandler
    Client -->|Queries| QueryHandler

    CommandHandler --> DB
    QueryHandler --> DB
```

Example:

```ts
class CreateOrderHandler {
  constructor(private readonly orderRepository: OrderRepository) {}

  async handle(command: CreateOrderCommand): Promise<void> {
    const order = Order.create({
      customerId: command.customerId,
      items: command.items
    });

    await this.orderRepository.save(order);
  }
}

class GetOrderSummaryHandler {
  constructor(private readonly db: Database) {}

  async handle(query: GetOrderSummaryQuery): Promise<OrderSummary> {
    return this.db.queryOne(
      `
      SELECT
        order_id,
        status,
        total_amount_cents,
        currency
      FROM orders
      WHERE order_id = $1
      `,
      [query.orderId]
    );
  }
}
```

This is a lightweight form of CQRS.

It gives code-level separation without event-driven projections or separate storage.

This is often a good first step.

---

#### CQRS with separate read and write models

More advanced CQRS uses separate models and often separate storage.

```mermaid
flowchart TD
    CommandAPI[Command API]
    WriteDB[(Write DB)]

    EventBus[(Event Bus)]
    Projector[Read Model Projector]
    ReadDB[(Read DB)]
    QueryAPI[Query API]

    CommandAPI --> WriteDB
    CommandAPI -->|publishes events| EventBus

    EventBus --> Projector
    Projector --> ReadDB

    QueryAPI --> ReadDB
```

The write side stores the authoritative transactional state.

The read side stores query-optimized projections.

For example, the write database may have normalized tables:

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL
);

CREATE TABLE order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price_cents INTEGER NOT NULL
);
```

The read database may have a denormalized order summary table:

```sql
CREATE TABLE order_summaries (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_status TEXT NOT NULL,
    payment_status TEXT,
    shipment_status TEXT,
    total_amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL,
    item_count INTEGER NOT NULL,
    estimated_delivery_date DATE,
    last_updated_at TIMESTAMP NOT NULL
);
```

The read model is designed for queries, not for enforcing business invariants.

---

#### Example: order write model

The write model focuses on correctness.

```ts
type OrderStatus =
  | "PENDING_PAYMENT"
  | "CONFIRMED"
  | "SHIPPED"
  | "CANCELLED";

type OrderItem = {
  productId: string;
  quantity: number;
  unitPriceCents: number;
};

class Order {
  constructor(
    public readonly orderId: string,
    public readonly customerId: string,
    public status: OrderStatus,
    public readonly items: OrderItem[]
  ) {}

  confirmPayment(): void {
    if (this.status !== "PENDING_PAYMENT") {
      throw new Error("Order is not waiting for payment");
    }

    this.status = "CONFIRMED";
  }

  cancel(reason: string): void {
    if (this.status === "SHIPPED") {
      throw new Error("Cannot cancel shipped order");
    }

    if (this.status === "CANCELLED") {
      return;
    }

    this.status = "CANCELLED";
  }

  get totalAmountCents(): number {
    return this.items.reduce(
      (sum, item) => sum + item.quantity * item.unitPriceCents,
      0
    );
  }
}
```

The write model is allowed to be rich and rule-heavy.

It protects valid state transitions.

---

#### Example: order read model

The read model focuses on convenient reads.

```ts
type OrderSummary = {
  orderId: string;
  customerId: string;
  orderStatus: string;
  paymentStatus: string;
  shipmentStatus: string;
  totalAmount: number;
  currency: string;
  itemCount: number;
  estimatedDeliveryDate?: string;
};

class OrderSummaryQueryHandler {
  constructor(private readonly db: Database) {}

  async getOrderSummary(orderId: string): Promise<OrderSummary | null> {
    const row = await this.db.queryOne(
      `
      SELECT
        order_id,
        customer_id,
        order_status,
        payment_status,
        shipment_status,
        total_amount_cents,
        currency,
        item_count,
        estimated_delivery_date
      FROM order_summaries
      WHERE order_id = $1
      `,
      [orderId]
    );

    if (!row) {
      return null;
    }

    return {
      orderId: row.order_id,
      customerId: row.customer_id,
      orderStatus: row.order_status,
      paymentStatus: row.payment_status,
      shipmentStatus: row.shipment_status,
      totalAmount: row.total_amount_cents / 100,
      currency: row.currency,
      itemCount: row.item_count,
      estimatedDeliveryDate: row.estimated_delivery_date
    };
  }
}
```

This read model may be denormalized, duplicated, and optimized for one or more query use cases.

That is acceptable because it is not the source of truth for business decisions.

---

#### Synchronizing read models

When the write side changes, the read side must be updated.

A common approach is event-driven projection.

```mermaid
flowchart TD
    WriteSide[Write Side]
    WriteDB[(Write DB)]

    Events[Domain Events]
    Bus[(Event Bus)]

    Projector[Read Model Projector]
    ReadDB[(Read DB)]

    WriteSide --> WriteDB
    WriteSide --> Events
    Events --> Bus
    Bus --> Projector
    Projector --> ReadDB
```

Example events:

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt_001",
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456",
    "totalAmountCents": 12999,
    "currency": "USD",
    "itemCount": 1
  }
}
```

```json
{
  "eventType": "PaymentAuthorized",
  "eventId": "evt_002",
  "occurredAt": "2026-04-29T12:01:00Z",
  "data": {
    "orderId": "ord_123",
    "paymentStatus": "AUTHORIZED"
  }
}
```

```json
{
  "eventType": "ShipmentCreated",
  "eventId": "evt_003",
  "occurredAt": "2026-04-29T12:03:00Z",
  "data": {
    "orderId": "ord_123",
    "shipmentStatus": "PENDING",
    "estimatedDeliveryDate": "2026-05-03"
  }
}
```

The projector consumes these events and updates the read model.

---

#### Projector example

A projector updates a read database from events.

```ts
type Event =
  | OrderCreatedEvent
  | PaymentAuthorizedEvent
  | ShipmentCreatedEvent;

class OrderSummaryProjector {
  constructor(private readonly db: Database) {}

  async handle(event: Event): Promise<void> {
    switch (event.eventType) {
      case "OrderCreated":
        await this.handleOrderCreated(event);
        return;

      case "PaymentAuthorized":
        await this.handlePaymentAuthorized(event);
        return;

      case "ShipmentCreated":
        await this.handleShipmentCreated(event);
        return;
    }
  }

  private async handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
    await this.db.execute(
      `
      INSERT INTO order_summaries (
        order_id,
        customer_id,
        order_status,
        total_amount_cents,
        currency,
        item_count,
        last_updated_at
      )
      VALUES ($1, $2, $3, $4, $5, $6, NOW())
      ON CONFLICT (order_id)
      DO UPDATE SET
        order_status = EXCLUDED.order_status,
        total_amount_cents = EXCLUDED.total_amount_cents,
        currency = EXCLUDED.currency,
        item_count = EXCLUDED.item_count,
        last_updated_at = NOW()
      `,
      [
        event.data.orderId,
        event.data.customerId,
        "PENDING_PAYMENT",
        event.data.totalAmountCents,
        event.data.currency,
        event.data.itemCount
      ]
    );
  }

  private async handlePaymentAuthorized(
    event: PaymentAuthorizedEvent
  ): Promise<void> {
    await this.db.execute(
      `
      UPDATE order_summaries
      SET
        payment_status = $2,
        last_updated_at = NOW()
      WHERE order_id = $1
      `,
      [event.data.orderId, "AUTHORIZED"]
    );
  }

  private async handleShipmentCreated(
    event: ShipmentCreatedEvent
  ): Promise<void> {
    await this.db.execute(
      `
      UPDATE order_summaries
      SET
        shipment_status = $2,
        estimated_delivery_date = $3,
        last_updated_at = NOW()
      WHERE order_id = $1
      `,
      [
        event.data.orderId,
        event.data.shipmentStatus,
        event.data.estimatedDeliveryDate
      ]
    );
  }
}
```

Projectors must be idempotent because events may be delivered more than once.

---

#### CQRS and eventual consistency

When the read model is updated asynchronously, the query side may lag behind the write side.

```mermaid
sequenceDiagram
    participant Client
    participant CommandAPI as Command API
    participant WriteDB as Write DB
    participant Bus as Event Bus
    participant Projector
    participant ReadDB as Read DB
    participant QueryAPI as Query API

    Client->>CommandAPI: Create order
    CommandAPI->>WriteDB: Save order
    CommandAPI->>Bus: Publish OrderCreated
    CommandAPI-->>Client: Order accepted

    Client->>QueryAPI: Get order summary
    QueryAPI->>ReadDB: Query summary
    ReadDB-->>QueryAPI: Not updated yet
    QueryAPI-->>Client: Still processing

    Bus-->>Projector: OrderCreated
    Projector->>ReadDB: Update summary
```

For a short time, the read model may not show the latest write.

This is eventual consistency.

The user experience should handle it.

Example response:

```json
{
  "orderId": "ord_123",
  "status": "PROCESSING",
  "message": "Your order was received and is being prepared."
}
```

Or expose freshness information:

```json
{
  "orderId": "ord_123",
  "orderStatus": "CONFIRMED",
  "lastUpdatedAt": "2026-04-29T12:00:02Z",
  "projectionLagMs": 850
}
```

CQRS works best when this lag is acceptable or can be hidden behind good UX.

---

#### Read-your-writes problem

A common issue in CQRS is the user writes something and then immediately reads it, but the read model has not caught up.

Example:

1. User changes address.
2. Command succeeds.
3. User refreshes profile page.
4. Query reads old address from read model.

```mermaid
flowchart TD
    Command[Update Address Command]
    WriteDB[(Write DB)]
    Event[AddressUpdated Event]
    ReadDB[(Read DB)]
    Query[Profile Query]

    Command --> WriteDB
    WriteDB --> Event
    Event -. delayed .-> ReadDB
    Query --> ReadDB
    ReadDB --> OldData[Old address still visible]
```

Ways to handle this:

**1. Return the updated value from the command**

```json
{
  "customerId": "cus_123",
  "address": {
    "line1": "100 Market Street",
    "city": "San Francisco"
  }
}
```

**2. Read from the write side for immediate confirmation**

Use this carefully. Do not turn every query into a write-side query.

**3. Use session consistency**

Track the version the user just wrote and wait until the read model reaches that version.

**4. Show a pending state**

```text
Your address update is being applied.
```

**5. Make projection very fast for user-facing data**

Some systems update critical read models synchronously or near-synchronously.

Read-your-writes behavior should be designed deliberately.

---

#### CQRS with multiple read models

One write model can feed many read models.

```mermaid
flowchart TD
    OrderWriteModel[Order Write Model]
    Bus[(Event Bus)]

    CustomerOrderReadModel[Customer Order History]
    AdminOrderReadModel[Admin Order Dashboard]
    SearchIndex[Order Search Index]
    AnalyticsModel[Analytics Model]

    OrderWriteModel -->|Order events| Bus

    Bus --> CustomerOrderReadModel
    Bus --> AdminOrderReadModel
    Bus --> SearchIndex
    Bus --> AnalyticsModel
```

Each read model is optimized for a different use case.

| Read model             | Optimized for                         |
| ---------------------- | ------------------------------------- |
| Customer order history | Customer-facing list of orders        |
| Admin order dashboard  | Support and operations                |
| Search index           | Search by order ID, customer, product |
| Analytics model        | Reporting and metrics                 |
| Mobile order summary   | Small payload for mobile app          |
| Fraud review queue     | Risk team workflow                    |

This is one of CQRS’s biggest strengths.

You can avoid forcing one generic query model to satisfy every consumer.

---

#### CQRS and Database per Service

CQRS fits naturally with Database per Service.

Each service owns its write model.

Other services or query APIs can build read models from events.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    ShippingService[Shipping Service]

    OrderDB[(Order DB)]
    PaymentDB[(Payment DB)]
    ShippingDB[(Shipping DB)]

    EventBus[(Event Bus)]

    OrderSummaryProjector[Order Summary Projector]
    OrderSummaryDB[(Order Summary Read DB)]

    OrderService --> OrderDB
    PaymentService --> PaymentDB
    ShippingService --> ShippingDB

    OrderService -->|Order events| EventBus
    PaymentService -->|Payment events| EventBus
    ShippingService -->|Shipping events| EventBus

    EventBus --> OrderSummaryProjector
    OrderSummaryProjector --> OrderSummaryDB
```

This solves a common problem:

> How do we query across service-owned databases without directly joining them?

Answer:

> Build a read model that subscribes to the relevant events.

The read model is derived. The source of truth remains with the owning services.

---

#### CQRS vs simple CRUD

Not every system needs CQRS.

Simple CRUD uses the same model for reads and writes.

```mermaid
flowchart TD
    API[API]
    DB[(Database)]

    Create[Create]
    Read[Read]
    Update[Update]
    Delete[Delete]

    API --> DB

    Create --> DB
    Read --> DB
    Update --> DB
    Delete --> DB
```

This is often enough for straightforward applications.

Use simple CRUD when:

* read and write needs are similar,
* the model is simple,
* scaling requirements are modest,
* consistency needs are immediate,
* the team does not need separate read projections,
* the extra CQRS complexity is not justified.

CQRS is most useful when reads and writes are meaningfully different.

---

#### CQRS vs Event Sourcing

CQRS and Event Sourcing are related but not the same.

CQRS separates commands and queries.

Event Sourcing stores state changes as events.

You can use CQRS without Event Sourcing.

```mermaid
flowchart TD
    CommandSide[Command Side]
    WriteDB[(Traditional Write Database)]

    Events[Events]
    ReadModel[Read Model]

    CommandSide --> WriteDB
    CommandSide --> Events
    Events --> ReadModel
```

You can also combine CQRS with Event Sourcing.

```mermaid
flowchart TD
    Commands[Commands]
    Aggregate[Aggregate]
    EventStore[(Event Store)]
    Projector[Projector]
    ReadDB[(Read DB)]
    Queries[Queries]

    Commands --> Aggregate
    Aggregate --> EventStore
    EventStore --> Projector
    Projector --> ReadDB
    Queries --> ReadDB
```

Comparison:

| Pattern               | Main idea                                         |
| --------------------- | ------------------------------------------------- |
| CQRS                  | Separate write operations from read operations    |
| Event Sourcing        | Store state as a sequence of events               |
| CQRS + Event Sourcing | Commands produce events, queries read projections |

Event Sourcing often uses CQRS because event streams are not usually convenient for direct queries.

But CQRS does not require Event Sourcing.

---

#### CQRS and commands that return data

A strict interpretation says commands change state and queries return data.

In practice, commands often return some data.

For example, `CreateOrder` may return:

```json
{
  "orderId": "ord_123",
  "status": "PENDING_PAYMENT"
}
```

This is fine.

The important rule is:

> Queries should not change state. Commands may return enough information to confirm the result.

A command should not become a general-purpose query.

Bad:

```http
POST /orders/search
```

Better:

```http
GET /orders?status=CONFIRMED
```

Use commands for intent to change state. Use queries for reading.

---

#### CQRS and security

Reads and writes often have different security needs.

For example:

| Operation                  | Permission          |
| -------------------------- | ------------------- |
| View order                 | `orders:read`       |
| Create order               | `orders:write`      |
| Cancel order               | `orders:cancel`     |
| View admin order dashboard | `orders:admin_read` |
| Export order report        | `orders:export`     |

CQRS can make this cleaner by separating command and query endpoints.

```mermaid
flowchart TD
    User[User]

    CommandAPI[Command API<br/>write permissions]
    QueryAPI[Query API<br/>read permissions]

    User --> CommandAPI
    User --> QueryAPI
```

Admin read models may contain fields that customer-facing read models should not expose.

Example customer read model:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99
}
```

Example admin read model:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED",
  "totalAmount": 129.99,
  "riskScore": 0.18,
  "paymentAuthorizationId": "auth_456",
  "warehouseId": "wh_001"
}
```

Separate read models help enforce separate access policies.

---

#### CQRS and scaling

Reads and writes often scale differently.

Many systems have far more reads than writes.

```mermaid
flowchart TD
    Reads[High read traffic]
    Writes[Lower write traffic]

    QuerySide[Query Side<br/>scaled horizontally]
    CommandSide[Command Side<br/>protected for consistency]

    Reads --> QuerySide
    Writes --> CommandSide
```

CQRS lets you scale the query side independently.

Examples:

* add read replicas,
* use a search index,
* use a cache,
* use a denormalized read database,
* use a document store for read views,
* use a columnar store for analytics.

The write side can remain focused on transactions and business invariants.

---

#### CQRS and performance

CQRS improves performance when query needs are expensive for the write model.

For example, this query may be expensive against normalized service databases:

```sql
SELECT
    o.order_id,
    o.status,
    p.status AS payment_status,
    s.status AS shipment_status,
    COUNT(oi.order_item_id) AS item_count
FROM orders o
JOIN payments p ON p.order_id = o.order_id
JOIN shipments s ON s.order_id = o.order_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.customer_id = 'cus_123'
GROUP BY o.order_id, o.status, p.status, s.status;
```

A read model can precompute this:

```sql
SELECT *
FROM customer_order_history
WHERE customer_id = 'cus_123'
ORDER BY created_at DESC;
```

The read model trades write-time or projection-time work for faster reads.

This is especially useful for:

* dashboards,
* search,
* reports,
* feed pages,
* account summaries,
* admin consoles,
* customer support views.

---

#### Rebuilding read models

A good CQRS design should allow read models to be rebuilt.

```mermaid
flowchart TD
    EventStream[(Event Stream)]
    Projector[Projector]
    ReadDB[(Read Model)]

    EventStream --> Projector
    Projector --> ReadDB

    Rebuild[Rebuild Read Model]
    EventStream --> Rebuild
    Rebuild --> ReadDB
```

Rebuilds are useful when:

* read model schema changes,
* projector bug is fixed,
* data corruption is detected,
* new read model is introduced,
* historical backfill is needed.

If events are retained, rebuilding is easier.

If events are not retained, rebuild may require reading from source services or databases.

Projection rebuilds should be planned. Large rebuilds can be expensive and may affect production systems.

---

#### Idempotent projectors

Projectors should be idempotent because events may be delivered more than once.

Bad:

```ts
async function handleOrderCreated(event: OrderCreatedEvent) {
  await db.execute(
    `
    INSERT INTO order_counts (customer_id, count)
    VALUES ($1, 1)
    ON CONFLICT (customer_id)
    DO UPDATE SET count = order_counts.count + 1
    `,
    [event.data.customerId]
  );
}
```

If the same event is delivered twice, the count increments twice.

Better:

```ts
async function handleOrderCreated(event: OrderCreatedEvent) {
  const alreadyProcessed = await db.queryOne(
    `
    SELECT event_id
    FROM processed_events
    WHERE event_id = $1
    `,
    [event.eventId]
  );

  if (alreadyProcessed) {
    return;
  }

  await db.transaction(async (tx) => {
    await tx.execute(
      `
      INSERT INTO customer_orders (customer_id, order_id)
      VALUES ($1, $2)
      ON CONFLICT (order_id) DO NOTHING
      `,
      [event.data.customerId, event.data.orderId]
    );

    await tx.execute(
      `
      INSERT INTO processed_events (event_id, processed_at)
      VALUES ($1, NOW())
      `,
      [event.eventId]
    );
  });
}
```

Idempotency prevents duplicate event delivery from corrupting projections.

---

#### Handling out-of-order events

Events may arrive out of order.

For example:

```text
PaymentAuthorized arrives before OrderCreated
```

A projector must decide what to do.

Options:

**1. Use partitioning**

Publish events for the same aggregate using the same partition key, such as `orderId`.

```ts
await eventBus.publish("order-events", event, {
  partitionKey: event.data.orderId
});
```

**2. Use upserts**

Allow projection rows to be created or updated in any order.

```sql
INSERT INTO order_summaries (order_id, payment_status)
VALUES ($1, $2)
ON CONFLICT (order_id)
DO UPDATE SET payment_status = EXCLUDED.payment_status;
```

**3. Store pending fragments**

If the base record does not exist yet, store the event and retry later.

**4. Use versions**

Ignore older events if the projection already has a newer version.

Example:

```json
{
  "eventType": "OrderStatusChanged",
  "aggregateId": "ord_123",
  "aggregateVersion": 4,
  "data": {
    "status": "CONFIRMED"
  }
}
```

Ordering assumptions should be explicit.

---

#### Projection lag

Projection lag is the delay between the write-side change and the read model update.

```mermaid
flowchart TD
    Write[Write occurs]
    Event[Event published]
    Projector[Projector processes event]
    ReadModel[Read model updated]

    Write --> Event
    Event --> Projector
    Projector --> ReadModel

    Lag[Projection lag]
    Event --> Lag
    Lag --> ReadModel
```

Track projection lag as a metric.

Important measurements:

* time from event occurrence to projection update,
* consumer lag,
* oldest unprocessed event age,
* projection update failure rate,
* read model freshness.

Example metric log:

```json
{
  "projector": "order-summary-projector",
  "eventType": "PaymentAuthorized",
  "eventId": "evt_123",
  "eventOccurredAt": "2026-04-29T12:00:00Z",
  "projectedAt": "2026-04-29T12:00:02Z",
  "projectionLagMs": 2000
}
```

Projection lag should be visible to operators.

---

#### CQRS with search

Search is a common CQRS use case.

The write side owns product data. The search side owns a search index.

```mermaid
flowchart TD
    CatalogService[Catalog Service]
    CatalogDB[(Catalog DB)]

    EventBus[(Event Bus)]

    SearchIndexer[Search Indexer]
    SearchIndex[(Search Index)]

    SearchAPI[Search API]
    Client[Client]

    CatalogService --> CatalogDB
    CatalogService -->|ProductCreated, ProductUpdated| EventBus

    EventBus --> SearchIndexer
    SearchIndexer --> SearchIndex

    Client --> SearchAPI
    SearchAPI --> SearchIndex
```

The Catalog Service may store normalized product data.

The Search Index may store denormalized search documents:

```json
{
  "productId": "prod_123",
  "title": "Trail Running Shoe",
  "description": "Lightweight running shoe for mixed terrain.",
  "brand": "SummitRun",
  "category": "Footwear",
  "tags": ["running", "trail", "outdoor"],
  "price": 129.99,
  "currency": "USD",
  "inStock": true
}
```

The search model is optimized for search queries, not for product lifecycle rules.

---

#### CQRS with dashboards

Dashboards often need data from many services.

Without CQRS, the dashboard may call many APIs at request time.

```mermaid
flowchart TD
    Dashboard[Dashboard API]

    Orders[Order Service]
    Payments[Payment Service]
    Shipping[Shipping Service]
    Support[Support Service]

    Dashboard --> Orders
    Dashboard --> Payments
    Dashboard --> Shipping
    Dashboard --> Support
```

With CQRS, events update a dashboard read model.

```mermaid
flowchart TD
    Orders[Order Events]
    Payments[Payment Events]
    Shipping[Shipping Events]
    Support[Support Events]

    Bus[(Event Bus)]

    DashboardProjector[Dashboard Projector]
    DashboardDB[(Dashboard Read DB)]

    DashboardAPI[Dashboard Query API]

    Orders --> Bus
    Payments --> Bus
    Shipping --> Bus
    Support --> Bus

    Bus --> DashboardProjector
    DashboardProjector --> DashboardDB

    DashboardAPI --> DashboardDB
```

The dashboard query becomes fast and simple.

The trade-off is eventual consistency.

---

#### CQRS and writes that need read data

Commands often need to read some data before writing.

For example, `CancelOrder` must load the order before deciding whether cancellation is allowed.

That is still part of the command side.

```mermaid
flowchart TD
    CancelCommand[CancelOrder Command]
    CommandHandler[Command Handler]
    WriteDB[(Write DB)]

    CancelCommand --> CommandHandler
    CommandHandler -->|load order| WriteDB
    CommandHandler -->|save updated order| WriteDB
```

CQRS does not mean the write side never reads.

It means reads that support writes are different from queries that serve clients.

The command side can read its own write model to enforce business rules.

---

#### CQRS and validation

Validation may happen on both sides, but for different reasons.

Command validation:

* Is the command well-formed?
* Is the user allowed to perform this action?
* Does the aggregate exist?
* Is the state transition valid?
* Are business rules satisfied?

Query validation:

* Is the query well-formed?
* Is the user allowed to see this data?
* Are pagination parameters valid?
* Is the filter allowed?
* Is the requested view available?

Do not put write business rules in query models.

For example, a read model may show `canCancel: true`, but the command side must still enforce cancellation rules when the user actually sends `CancelOrder`.

```mermaid
flowchart TD
    ReadModel[Read Model<br/>canCancel hint]
    User[User]
    CommandSide[Command Side<br/>actual rule enforcement]

    ReadModel --> User
    User -->|CancelOrder| CommandSide
```

Read-side hints improve UX. They are not a security or consistency boundary.

---

#### CQRS and permissions

Read and write permissions can differ.

For example:

```mermaid
flowchart TD
    User[User]

    QueryAPI[Query API]
    CommandAPI[Command API]

    ReadPermission[orders:read]
    WritePermission[orders:cancel]

    User --> QueryAPI
    User --> CommandAPI

    QueryAPI --> ReadPermission
    CommandAPI --> WritePermission
```

A user may be allowed to view an order but not cancel it.

A support agent may be allowed to view many customer orders but not issue refunds.

An admin may be allowed to query audit logs but not modify orders.

CQRS makes these separations explicit.

---

#### CQRS in a single service

CQRS can be applied inside one service.

```mermaid
flowchart TD
    OrderService[Order Service]

    CommandHandlers[Command Handlers]
    QueryHandlers[Query Handlers]

    WriteTables[(Write Tables)]
    ReadTables[(Read Tables)]

    OrderService --> CommandHandlers
    OrderService --> QueryHandlers

    CommandHandlers --> WriteTables
    CommandHandlers --> ReadTables
    QueryHandlers --> ReadTables
```

This is common when a service has complex writes and high-volume reads.

For example, Order Service may maintain:

* normalized order tables for writes,
* denormalized order summary tables for reads.

Both live inside the same service boundary.

This is simpler than cross-service CQRS and can still be valuable.

---

#### CQRS across services

CQRS can also create read models across multiple services.

```mermaid
flowchart TD
    OrderService[Order Service]
    PaymentService[Payment Service]
    ShippingService[Shipping Service]

    EventBus[(Event Bus)]

    CustomerOrderView[Customer Order View Projector]
    ReadDB[(Customer Order View DB)]

    OrderService -->|Order events| EventBus
    PaymentService -->|Payment events| EventBus
    ShippingService -->|Shipping events| EventBus

    EventBus --> CustomerOrderView
    CustomerOrderView --> ReadDB
```

This is useful when no single service owns the full read view.

The read model is derived from multiple sources.

Ownership must be clear. Someone must own the read model, projector, schema, freshness, and query API.

---

#### CQRS and ownership

Every read model needs an owner.

A read model is not “free data.” It is a product with responsibilities.

Read model owner responsibilities:

* schema design,
* projection logic,
* freshness expectations,
* rebuild process,
* access control,
* monitoring,
* query performance,
* event compatibility,
* data retention,
* backfill,
* user-facing semantics.

Example ownership table:

| Read model               | Owner                  | Sources                                  |
| ------------------------ | ---------------------- | ---------------------------------------- |
| Customer order history   | Orders Experience Team | Order, Payment, Shipping events          |
| Product search index     | Search Team            | Catalog, Pricing, Inventory events       |
| Admin customer dashboard | Support Platform Team  | Customer, Order, Payment, Support events |
| Finance reporting model  | Finance Data Team      | Payment, Refund, Invoice events          |

Without ownership, read models become stale, inconsistent, or untrusted.

---

#### CQRS and deleting data

Data deletion is more complex with CQRS because copies may exist in read models.

If a customer requests deletion, the system must delete or anonymize data in:

* source-of-truth write models,
* read models,
* search indexes,
* caches,
* analytics stores,
* projections,
* backups according to policy.

```mermaid
flowchart TD
    DeleteRequest[Delete Customer Request]

    CustomerService[Customer Service]
    EventBus[(Event Bus)]

    SearchIndex[Search Index]
    ReadModel[Read Model]
    Analytics[Analytics Store]

    DeleteRequest --> CustomerService
    CustomerService -->|CustomerDeleted or CustomerAnonymized| EventBus

    EventBus --> SearchIndex
    EventBus --> ReadModel
    EventBus --> Analytics
```

CQRS designs should include deletion and retention policies.

Do not forget derived copies.

---

#### Testing CQRS

CQRS needs tests for both sides.

Useful command-side tests:

| Test               | Purpose                            |
| ------------------ | ---------------------------------- |
| Command validation | Reject invalid commands            |
| Business rules     | Enforce state transitions          |
| Authorization      | Reject unauthorized commands       |
| Event emission     | Verify correct events are produced |
| Idempotency        | Verify duplicate commands are safe |

Useful query-side tests:

| Test               | Purpose                                           |
| ------------------ | ------------------------------------------------- |
| Projection tests   | Verify events update read model correctly         |
| Query tests        | Verify query API returns expected views           |
| Idempotency tests  | Verify duplicate events do not corrupt read model |
| Out-of-order tests | Verify ordering assumptions                       |
| Rebuild tests      | Verify read model can be rebuilt                  |

Example projector test:

```ts
describe("OrderSummaryProjector", () => {
  it("creates order summary from OrderCreated", async () => {
    await projector.handle({
      eventId: "evt_1",
      eventType: "OrderCreated",
      data: {
        orderId: "ord_123",
        customerId: "cus_456",
        totalAmountCents: 12999,
        currency: "USD",
        itemCount: 1
      }
    });

    const summary = await readDb.orderSummaries.findById("ord_123");

    expect(summary).toMatchObject({
      orderId: "ord_123",
      customerId: "cus_456",
      orderStatus: "PENDING_PAYMENT",
      totalAmountCents: 12999,
      currency: "USD",
      itemCount: 1
    });
  });

  it("does not duplicate work when event is processed twice", async () => {
    const event = makeOrderCreatedEvent("evt_1");

    await projector.handle(event);
    await projector.handle(event);

    const summaries = await readDb.orderSummaries.findAll();

    expect(summaries).toHaveLength(1);
  });
});
```

---

#### Observability

CQRS needs observability for command and query paths.

Command-side metrics:

* command rate,
* command success rate,
* command failure rate,
* validation failures,
* business rule rejections,
* write latency,
* event publish latency,
* outbox lag.

Query-side metrics:

* query rate,
* query latency,
* read model freshness,
* projection lag,
* projection error rate,
* stale read count,
* rebuild duration,
* read database performance.

Example log:

```json
{
  "component": "order-summary-projector",
  "eventId": "evt_123",
  "eventType": "PaymentAuthorized",
  "orderId": "ord_456",
  "status": "projected",
  "projectionLagMs": 742,
  "readModel": "order_summaries"
}
```

Important dashboards:

* command success and failure,
* query latency,
* projector lag,
* dead-letter queue count,
* read model freshness,
* event processing failures.

Without observability, CQRS failures can be hard to detect because writes may succeed while reads silently become stale.

---

#### When to use it

Use CQRS when:

* reads and writes have different models,
* read traffic is much higher than write traffic,
* queries require expensive joins,
* reads need denormalized views,
* writes need strong business rule enforcement,
* different read models are needed for different clients,
* read and write permissions differ,
* cross-service queries are difficult,
* search, dashboards, or reporting need optimized data,
* read models can tolerate eventual consistency.

Common use cases:

* order summaries,
* customer dashboards,
* admin consoles,
* product search,
* account activity feeds,
* financial reporting views,
* support agent views,
* analytics projections,
* inventory availability views,
* shipment tracking summaries.

---

#### When not to use it

Avoid CQRS when:

* the application is simple CRUD,
* reads and writes use the same model comfortably,
* immediate consistency is required for all reads,
* the team cannot operate event-driven projections,
* eventual consistency would confuse users,
* read models would duplicate data without clear benefit,
* query volume is low,
* the extra complexity is not justified.

CQRS is not a default requirement for microservices.

It is a tool for cases where separating reads and writes provides enough value to justify the complexity.

---

#### Benefits

**1. Separate models for separate needs**

The write model can focus on correctness while the read model focuses on queries.

**2. Better read performance**

Read models can be denormalized and optimized for specific views.

**3. Better write correctness**

Command models can enforce business rules without being polluted by query concerns.

**4. Independent scaling**

Read and write sides can scale differently.

**5. Supports multiple views**

One write model can feed many read models.

**6. Helps with cross-service queries**

Read models can combine events from multiple services without direct database joins.

**7. Improves security separation**

Read and write permissions can be handled separately.

**8. Works well with event-driven systems**

Events naturally update projections and read models.

---

#### Trade-offs

**1. Eventual consistency**

Read models may lag behind writes.

**2. More moving parts**

Commands, events, projectors, read databases, and query APIs all need ownership.

**3. Synchronization complexity**

Read models must be kept up to date.

**4. Duplicate data**

Data appears in both write and read models.

**5. More testing**

You must test commands, projections, and queries.

**6. More operational overhead**

Projection lag, rebuilds, and read model failures must be monitored.

**7. Harder debugging**

A user may see stale data even though the write succeeded.

**8. Schema evolution is more involved**

Write events and read models need versioning and migration.

---

#### Common mistakes

**Mistake 1: Using CQRS everywhere**

Most simple CRUD features do not need CQRS.

**Mistake 2: Confusing CQRS with Event Sourcing**

CQRS separates reads and writes. Event Sourcing stores state as events. They can be used together, but they are different patterns.

**Mistake 3: No projection monitoring**

If read models stop updating, users see stale data.

**Mistake 4: Ignoring read-your-writes**

Users may be confused when a successful write is not immediately visible.

**Mistake 5: Treating read models as sources of truth**

Read models are usually derived. The write model owns authoritative state.

**Mistake 6: No idempotency in projectors**

Duplicate events can corrupt read models.

**Mistake 7: No rebuild strategy**

Read models should be rebuildable when projections change or bugs are fixed.

**Mistake 8: Overcomplicating small systems**

CQRS adds architecture overhead. Use it when there is a real read/write mismatch.

**Mistake 9: No owner for read models**

Every projection and query model needs an owning team.

---

#### Practical design checklist

Before applying CQRS, ask:

* Are reads and writes truly different?
* What business rules does the write side enforce?
* What queries need optimization?
* Can a simpler CRUD model work?
* Is eventual consistency acceptable?
* What read models are needed?
* Who owns each read model?
* What events update each read model?
* Are those events reliable?
* Is the Outbox Pattern needed?
* How much projection lag is acceptable?
* How will projection lag be monitored?
* How will users experience stale data?
* Do users need read-your-writes consistency?
* Are projectors idempotent?
* Can read models be rebuilt?
* How are event schemas versioned?
* What happens if projection fails?
* Is there a dead-letter queue?
* What permissions apply to commands?
* What permissions apply to queries?
* What data deletion rules apply to derived models?

A CQRS design is probably healthy if:

* the read/write split solves a real problem,
* the write model owns business correctness,
* read models are query-focused,
* events are reliable,
* projectors are idempotent,
* projection lag is monitored,
* read models have clear owners,
* eventual consistency is acceptable,
* rebuild procedures exist.

A CQRS design is probably unhealthy if:

* it is used for simple CRUD without need,
* no one owns projections,
* read models silently go stale,
* users are surprised by stale reads,
* duplicate events corrupt read data,
* read models become accidental sources of truth,
* every small feature requires events, projections, and new databases.

---

#### Related patterns

| Pattern                   | Relationship                                                         |
| ------------------------- | -------------------------------------------------------------------- |
| Database per Service      | CQRS helps query across service-owned databases without direct joins |
| Async Messaging           | Often used to update read models asynchronously                      |
| Outbox Pattern            | Reliably publishes events after write-side transactions              |
| Event Sourcing            | Often paired with CQRS, but not required                             |
| Gateway Aggregation       | Alternative to read models for request-time composition              |
| Backends for Frontends    | BFFs may query CQRS read models tailored to client needs             |
| Saga Pattern              | Sagas may update read models to show workflow progress               |
| Choreography              | Events from choreographed workflows can feed read models             |
| Materialized View         | A common CQRS read model implementation                              |
| Consumer-Driven Contracts | Protects command APIs, query APIs, and event schemas                 |

---

#### Summary

CQRS separates commands that change state from queries that read state.

The central idea is:

> Use a write model for correctness and business rules. Use read models for fast, convenient queries.

CQRS is useful when reads and writes have different performance, scaling, security, or modeling needs. It works especially well for dashboards, search, admin views, order summaries, and cross-service query models.

A good CQRS design has:

* clear command and query boundaries,
* a write model that owns business rules,
* read models optimized for specific queries,
* reliable event publishing,
* idempotent projectors,
* projection lag monitoring,
* rebuild procedures,
* and clear ownership.

The main trade-off is eventual consistency. Read models must be synchronized, and users may temporarily see stale data. CQRS is powerful when the read/write split solves a real problem, but it is unnecessary complexity for simple CRUD systems.


---

### 24. Event Sourcing

#### What it is

**Event Sourcing** is a persistence pattern where a service stores the history of state changes as a sequence of immutable events instead of storing only the latest state.

In a traditional state-based model, a database row stores the current state:

```sql
orders
------------------------------------------------
order_id   status      total_amount   updated_at
ord_123    CONFIRMED   129.99         2026-04-29
```

This tells you what the order looks like now, but not exactly how it got there.

In Event Sourcing, the system stores the events that happened:

```text
OrderCreated
PaymentAuthorized
InventoryReserved
OrderConfirmed
ShipmentCreated
OrderDelivered
```

The current state is rebuilt by replaying those events in order.

```mermaid
flowchart TD
    Events[Event Stream]

    E1[OrderCreated]
    E2[PaymentAuthorized]
    E3[InventoryReserved]
    E4[OrderConfirmed]

    Aggregate[Order Aggregate<br/>Current state]

    Events --> E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> Aggregate
```

The central idea is:

> Store what happened, not just what things look like now.

For example, instead of storing only this:

```json
{
  "orderId": "ord_123",
  "status": "CONFIRMED"
}
```

Event Sourcing stores this:

```json
[
  {
    "eventType": "OrderCreated",
    "orderId": "ord_123"
  },
  {
    "eventType": "PaymentAuthorized",
    "orderId": "ord_123"
  },
  {
    "eventType": "InventoryReserved",
    "orderId": "ord_123"
  },
  {
    "eventType": "OrderConfirmed",
    "orderId": "ord_123"
  }
]
```

The state is derived from the event history.

---

#### Why this pattern exists

Many systems care not only about current state, but also about the sequence of events that produced that state.

For example, in a payment system, knowing that a payment is currently `REFUNDED` is useful.

But it may not be enough.

You may need to know:

* when the payment was authorized,
* when it was captured,
* who initiated the refund,
* whether the refund was partial or full,
* which gateway response was received,
* whether there were failed retry attempts,
* whether a manual override happened,
* what the state looked like at a specific time.

A current-state table may show:

```sql
payment_id   status     amount
pay_123      REFUNDED   129.99
```

An event stream can show the full story:

```text
PaymentAuthorizationRequested
PaymentAuthorized
PaymentCaptured
RefundRequested
RefundApproved
PaymentRefunded
```

That history is valuable for:

* auditing,
* debugging,
* compliance,
* dispute resolution,
* analytics,
* replay,
* temporal queries,
* reconstructing state,
* understanding business behavior.

Event Sourcing exists because some domains need the complete timeline, not just the final value.

---

#### What it solves

Event Sourcing solves the problem of **lost history**.

In a normal CRUD model, updates overwrite old state.

```mermaid
flowchart TD
    State1[Order status: PENDING]
    State2[Order status: CONFIRMED]
    State3[Order status: SHIPPED]

    State1 -->|UPDATE row| State2
    State2 -->|UPDATE row| State3

    Lost[Earlier states may be lost unless separately audited]

    State3 --> Lost
```

After several updates, the database may only show:

```json
{
  "orderId": "ord_123",
  "status": "SHIPPED"
}
```

Event Sourcing keeps the full transition history:

```mermaid
flowchart TD
    Event1[OrderCreated]
    Event2[PaymentAuthorized]
    Event3[OrderConfirmed]
    Event4[ShipmentCreated]
    Event5[OrderShipped]

    Current[Current order state: SHIPPED]

    Event1 --> Event2
    Event2 --> Event3
    Event3 --> Event4
    Event4 --> Event5
    Event5 --> Current
```

This lets you answer questions such as:

* What happened first?
* What changed?
* Who or what caused the change?
* When did the change happen?
* What did the system know at that time?
* Can we rebuild the current state?
* Can we rebuild a previous state?
* Can we create a new projection from historical events?

Event Sourcing turns history into the primary source of truth.

---

#### Traditional persistence vs Event Sourcing

In traditional persistence, the database stores current state.

```mermaid
flowchart TD
    Command[Command]
    Service[Service]
    StateDB[(Current State DB)]

    Command --> Service
    Service -->|insert/update row| StateDB
```

Example:

```sql
UPDATE orders
SET status = 'CONFIRMED'
WHERE order_id = 'ord_123';
```

In Event Sourcing, the database stores events.

```mermaid
flowchart TD
    Command[Command]
    Aggregate[Aggregate]
    EventStore[(Event Store)]

    Command --> Aggregate
    Aggregate -->|append event| EventStore
```

Example:

```json
{
  "eventType": "OrderConfirmed",
  "eventId": "evt_123",
  "aggregateId": "ord_123",
  "aggregateVersion": 4,
  "occurredAt": "2026-04-29T12:00:00Z"
}
```

The event is appended. Existing events are not updated or deleted.

| Traditional persistence                   | Event Sourcing                 |
| ----------------------------------------- | ------------------------------ |
| Stores current state                      | Stores sequence of events      |
| Updates rows in place                     | Appends immutable events       |
| History may require separate audit tables | History is the source of truth |
| Current state is primary                  | Current state is derived       |
| Easier mental model                       | More powerful but more complex |
| Good for CRUD                             | Good for history-heavy domains |

---

#### Events as facts

An event should represent a fact that happened in the past.

Good event names:

* `OrderCreated`
* `PaymentAuthorized`
* `PaymentCaptured`
* `RefundIssued`
* `InventoryReserved`
* `ShipmentDispatched`
* `PolicyApproved`
* `ClaimSubmitted`
* `PatientRecordUpdated`

Poor event names:

* `CreateOrder`
* `AuthorizePayment`
* `DoRefund`
* `UpdateInventory`
* `ProcessNextStep`

The difference is tense and meaning.

A command asks for something to happen:

```json
{
  "commandType": "CancelOrder",
  "orderId": "ord_123"
}
```

An event records that something happened:

```json
{
  "eventType": "OrderCancelled",
  "orderId": "ord_123"
}
```

A command can be rejected. An event is a fact.

The write model validates commands and emits events only when the requested change is allowed.

---

#### Event stream

An **event stream** is the ordered list of events for a particular aggregate or entity.

For example, the event stream for order `ord_123` might be:

```text
Stream: order-ord_123

1. OrderCreated
2. PaymentAuthorized
3. InventoryReserved
4. OrderConfirmed
5. ShipmentCreated
6. OrderDelivered
```

```mermaid
flowchart TD
    Stream[Order Event Stream<br/>order-ord_123]

    E1[1. OrderCreated]
    E2[2. PaymentAuthorized]
    E3[3. InventoryReserved]
    E4[4. OrderConfirmed]
    E5[5. ShipmentCreated]
    E6[6. OrderDelivered]

    Stream --> E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> E5
    E5 --> E6
```

Each event is appended with a sequence number or version.

Example event:

```json
{
  "eventId": "evt_001",
  "eventType": "OrderCreated",
  "aggregateType": "Order",
  "aggregateId": "ord_123",
  "aggregateVersion": 1,
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "customerId": "cus_456",
    "items": [
      {
        "productId": "prod_789",
        "quantity": 1,
        "unitPriceCents": 12999
      }
    ],
    "currency": "USD"
  }
}
```

The aggregate version is important because it preserves ordering and helps with concurrency control.

---

#### Rebuilding state from events

To get current state, load the event stream and apply each event in order.

```mermaid
flowchart TD
    Events[Events]

    Apply1[Apply OrderCreated]
    Apply2[Apply PaymentAuthorized]
    Apply3[Apply InventoryReserved]
    Apply4[Apply OrderConfirmed]

    State[Current Order State]

    Events --> Apply1
    Apply1 --> Apply2
    Apply2 --> Apply3
    Apply3 --> Apply4
    Apply4 --> State
```

Example TypeScript model:

```ts
type OrderStatus =
  | "NEW"
  | "PENDING_PAYMENT"
  | "PAYMENT_AUTHORIZED"
  | "INVENTORY_RESERVED"
  | "CONFIRMED"
  | "CANCELLED";

type OrderState = {
  orderId: string;
  customerId?: string;
  status: OrderStatus;
  totalAmountCents: number;
  currency?: string;
};

type OrderEvent =
  | {
      eventType: "OrderCreated";
      data: {
        orderId: string;
        customerId: string;
        totalAmountCents: number;
        currency: string;
      };
    }
  | {
      eventType: "PaymentAuthorized";
      data: {
        paymentId: string;
      };
    }
  | {
      eventType: "InventoryReserved";
      data: {
        reservationId: string;
      };
    }
  | {
      eventType: "OrderConfirmed";
      data: Record<string, never>;
    }
  | {
      eventType: "OrderCancelled";
      data: {
        reason: string;
      };
    };

function initialOrderState(orderId: string): OrderState {
  return {
    orderId,
    status: "NEW",
    totalAmountCents: 0
  };
}

function applyOrderEvent(
  state: OrderState,
  event: OrderEvent
): OrderState {
  switch (event.eventType) {
    case "OrderCreated":
      return {
        orderId: event.data.orderId,
        customerId: event.data.customerId,
        status: "PENDING_PAYMENT",
        totalAmountCents: event.data.totalAmountCents,
        currency: event.data.currency
      };

    case "PaymentAuthorized":
      return {
        ...state,
        status: "PAYMENT_AUTHORIZED"
      };

    case "InventoryReserved":
      return {
        ...state,
        status: "INVENTORY_RESERVED"
      };

    case "OrderConfirmed":
      return {
        ...state,
        status: "CONFIRMED"
      };

    case "OrderCancelled":
      return {
        ...state,
        status: "CANCELLED"
      };
  }
}
```

Rebuild function:

```ts
function rebuildOrderState(
  orderId: string,
  events: OrderEvent[]
): OrderState {
  return events.reduce(
    applyOrderEvent,
    initialOrderState(orderId)
  );
}
```

This is the core mechanics of Event Sourcing.

---

#### Commands produce events

In Event Sourcing, commands do not directly update current-state rows.

Instead, a command handler:

1. Loads past events.
2. Rebuilds current state.
3. Validates the command.
4. Produces new events.
5. Appends those events to the event store.

```mermaid
flowchart TD
    Command[Command]
    LoadEvents[Load event stream]
    Rebuild[Rebuild aggregate state]
    Validate[Validate business rules]
    NewEvents[Produce new events]
    Append[Append events to event store]

    Command --> LoadEvents
    LoadEvents --> Rebuild
    Rebuild --> Validate
    Validate --> NewEvents
    NewEvents --> Append
```

Example command:

```json
{
  "commandType": "ConfirmOrder",
  "orderId": "ord_123"
}
```

Command handler:

```ts
type ConfirmOrderCommand = {
  orderId: string;
};

function confirmOrder(
  state: OrderState,
  command: ConfirmOrderCommand
): OrderEvent[] {
  if (state.status !== "INVENTORY_RESERVED") {
    throw new Error("Order cannot be confirmed until inventory is reserved");
  }

  return [
    {
      eventType: "OrderConfirmed",
      data: {}
    }
  ];
}
```

The event is then appended to the event stream.

The aggregate does not say “set status to confirmed.”
It says “OrderConfirmed happened.”

---

#### Event store

An **event store** is the database where events are persisted.

A simplified relational event store table might look like this:

```sql
CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    aggregate_version INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB NOT NULL,
    occurred_at TIMESTAMP NOT NULL,

    UNIQUE (aggregate_type, aggregate_id, aggregate_version)
);
```

Example row:

```json
{
  "eventId": "evt_123",
  "aggregateType": "Order",
  "aggregateId": "ord_456",
  "aggregateVersion": 4,
  "eventType": "OrderConfirmed",
  "eventData": {
    "confirmedBy": "system"
  },
  "metadata": {
    "correlationId": "corr_789",
    "causationId": "evt_122",
    "userId": "user_123"
  },
  "occurredAt": "2026-04-29T12:00:00Z"
}
```

The event store is append-only.

You generally do not update old events. You append new events that represent new facts.

---

#### Optimistic concurrency

Event-sourced systems commonly use optimistic concurrency.

Suppose two commands try to update the same order at the same time.

```mermaid
sequenceDiagram
    participant A as Command Handler A
    participant B as Command Handler B
    participant Store as Event Store

    A->>Store: Load order stream at version 3
    B->>Store: Load order stream at version 3

    A->>Store: Append event expecting version 3
    Store-->>A: Success, stream now version 4

    B->>Store: Append event expecting version 3
    Store-->>B: Conflict, stream already version 4
```

The event store rejects the second write because the expected version is stale.

Example append API:

```ts
type AppendToStreamOptions = {
  aggregateType: string;
  aggregateId: string;
  expectedVersion: number;
  events: OrderEvent[];
};

async function appendToStream(options: AppendToStreamOptions): Promise<void> {
  // Event store inserts events only if the stream is still at expectedVersion.
}
```

This prevents lost updates.

The failed command can reload the latest stream, rebuild state, and retry if appropriate.

---

#### Projections

Event streams are great for preserving history, but they are not always convenient for queries.

For example, a customer order history page should not rebuild every order from events on every request.

Instead, Event Sourcing usually uses **projections**.

A projection consumes events and builds a read model.

```mermaid
flowchart TD
    EventStore[(Event Store)]

    Projector[Projection Handler]

    OrderSummaryDB[(Order Summary Read DB)]
    CustomerHistoryDB[(Customer Order History Read DB)]
    AdminDashboardDB[(Admin Dashboard Read DB)]

    EventStore --> Projector

    Projector --> OrderSummaryDB
    Projector --> CustomerHistoryDB
    Projector --> AdminDashboardDB
```

Example projection table:

```sql
CREATE TABLE order_summaries (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount_cents INTEGER NOT NULL,
    currency TEXT NOT NULL,
    last_updated_at TIMESTAMP NOT NULL
);
```

Projection handler:

```ts
async function projectOrderEvent(event: StoredEvent): Promise<void> {
  switch (event.eventType) {
    case "OrderCreated":
      await db.execute(
        `
        INSERT INTO order_summaries (
          order_id,
          customer_id,
          status,
          total_amount_cents,
          currency,
          last_updated_at
        )
        VALUES ($1, $2, $3, $4, $5, NOW())
        `,
        [
          event.aggregateId,
          event.eventData.customerId,
          "PENDING_PAYMENT",
          event.eventData.totalAmountCents,
          event.eventData.currency
        ]
      );
      return;

    case "OrderConfirmed":
      await db.execute(
        `
        UPDATE order_summaries
        SET status = 'CONFIRMED',
            last_updated_at = NOW()
        WHERE order_id = $1
        `,
        [event.aggregateId]
      );
      return;

    case "OrderCancelled":
      await db.execute(
        `
        UPDATE order_summaries
        SET status = 'CANCELLED',
            last_updated_at = NOW()
        WHERE order_id = $1
        `,
        [event.aggregateId]
      );
      return;
  }
}
```

This is why Event Sourcing is often paired with CQRS.

The event store is the write-side source of truth. Projections serve read-side queries.

---

#### Event Sourcing and CQRS

Event Sourcing and CQRS are related, but they are not the same pattern.

**Event Sourcing** says:

> Store state changes as events.

**CQRS** says:

> Separate commands from queries.

They are commonly used together:

```mermaid
flowchart TD
    Commands[Commands]
    CommandHandler[Command Handler]
    Aggregate[Aggregate]
    EventStore[(Event Store)]

    Projector[Projector]
    ReadModel[(Read Model)]
    QueryAPI[Query API]
    Queries[Queries]

    Commands --> CommandHandler
    CommandHandler --> Aggregate
    Aggregate --> EventStore

    EventStore --> Projector
    Projector --> ReadModel

    Queries --> QueryAPI
    QueryAPI --> ReadModel
```

You can use CQRS without Event Sourcing.

You can also use Event Sourcing without many separate read models, although that is less common in real systems.

Most practical Event Sourcing systems need projections because event streams are not efficient for every query.

---

#### Replay

One major benefit of Event Sourcing is replay.

Because the system stores historical events, you can replay them to rebuild state or create new views.

```mermaid
flowchart TD
    EventStore[(Event Store)]

    ExistingProjection[Existing Projection]
    NewProjection[New Projection]
    RebuildProjection[Rebuilt Projection]

    EventStore --> ExistingProjection
    EventStore --> NewProjection
    EventStore --> RebuildProjection
```

Replay can be used to:

* rebuild a corrupted read model,
* create a new projection,
* backfill analytics,
* test new business logic,
* reconstruct state at a point in time,
* investigate bugs,
* migrate read model schemas.

Example replay loop:

```ts
async function rebuildOrderSummaries(eventStore: EventStore): Promise<void> {
  await readDb.orderSummaries.truncate();

  let cursor: string | null = null;

  while (true) {
    const batch = await eventStore.readAllEvents({
      cursor,
      limit: 1000
    });

    for (const event of batch.events) {
      await projectOrderEvent(event);
    }

    if (!batch.nextCursor) {
      break;
    }

    cursor = batch.nextCursor;
  }
}
```

Replay is powerful, but it requires event handlers to be deterministic and idempotent.

---

#### Temporal queries

Event Sourcing can answer questions about the past.

For example:

> What was the order state at 10:00 AM?

To answer this, replay only events that occurred before that time.

```ts
function rebuildOrderStateAt(
  orderId: string,
  events: OrderEvent[],
  timestamp: Date
): OrderState {
  const historicalEvents = events.filter(
    (event) => new Date(event.occurredAt) <= timestamp
  );

  return rebuildOrderState(orderId, historicalEvents);
}
```

This is useful for:

* audits,
* compliance,
* customer disputes,
* financial reconciliation,
* debugging,
* “as of” reporting,
* regulatory investigations.

A current-state database usually cannot answer this unless it has a separate audit mechanism.

In Event Sourcing, this is natural because history is preserved.

---

#### Auditability

Event Sourcing provides strong auditability because every state change is recorded as an event.

A good event includes metadata:

```json
{
  "eventId": "evt_123",
  "eventType": "RefundIssued",
  "aggregateType": "Payment",
  "aggregateId": "pay_456",
  "aggregateVersion": 8,
  "occurredAt": "2026-04-29T12:00:00Z",
  "data": {
    "refundId": "ref_789",
    "amountCents": 5000,
    "currency": "USD",
    "reason": "CUSTOMER_REQUEST"
  },
  "metadata": {
    "userId": "agent_123",
    "source": "support-admin",
    "correlationId": "corr_456",
    "ipAddress": "203.0.113.10"
  }
}
```

This helps answer:

* who initiated the change,
* what command caused it,
* when it happened,
* what aggregate changed,
* what version it became,
* what workflow it belonged to,
* what external request caused it.

For compliance-heavy systems, this can be a major advantage.

---

#### Snapshots

Rebuilding state from events can become expensive if an aggregate has many events.

For example, a bank account may have thousands of transactions.

A **snapshot** stores the aggregate state at a certain version.

```mermaid
flowchart TD
    E1[Events 1 to 1000]
    Snapshot[Snapshot at version 1000]
    E2[Events 1001 to 1010]
    Current[Current State]

    E1 --> Snapshot
    Snapshot --> E2
    E2 --> Current
```

Instead of replaying all events from the beginning, load the latest snapshot and replay only events after it.

Example snapshot:

```json
{
  "aggregateType": "Order",
  "aggregateId": "ord_123",
  "aggregateVersion": 100,
  "state": {
    "orderId": "ord_123",
    "status": "CONFIRMED",
    "totalAmountCents": 12999,
    "currency": "USD"
  },
  "createdAt": "2026-04-29T12:00:00Z"
}
```

Snapshot rebuild:

```ts
async function loadOrder(orderId: string): Promise<OrderState> {
  const snapshot = await snapshotStore.getLatestSnapshot("Order", orderId);

  const startingState = snapshot
    ? snapshot.state
    : initialOrderState(orderId);

  const startingVersion = snapshot?.aggregateVersion ?? 0;

  const events = await eventStore.readStream({
    aggregateType: "Order",
    aggregateId: orderId,
    fromVersion: startingVersion + 1
  });

  return events.reduce(applyOrderEvent, startingState);
}
```

Snapshots are an optimization. The source of truth remains the event stream.

---

#### Event versioning

Events live for a long time. Once stored, they may be replayed years later.

That means event schemas must be versioned carefully.

Version 1:

```json
{
  "eventType": "OrderCreated",
  "schemaVersion": 1,
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456",
    "totalAmountCents": 12999
  }
}
```

Version 2 adds currency:

```json
{
  "eventType": "OrderCreated",
  "schemaVersion": 2,
  "data": {
    "orderId": "ord_123",
    "customerId": "cus_456",
    "totalAmountCents": 12999,
    "currency": "USD"
  }
}
```

Event handlers must handle old versions.

```ts
function applyOrderCreated(
  state: OrderState,
  event: StoredEvent
): OrderState {
  if (event.schemaVersion === 1) {
    return {
      orderId: event.data.orderId,
      customerId: event.data.customerId,
      status: "PENDING_PAYMENT",
      totalAmountCents: event.data.totalAmountCents,
      currency: "USD"
    };
  }

  if (event.schemaVersion === 2) {
    return {
      orderId: event.data.orderId,
      customerId: event.data.customerId,
      status: "PENDING_PAYMENT",
      totalAmountCents: event.data.totalAmountCents,
      currency: event.data.currency
    };
  }

  throw new Error(`Unsupported OrderCreated version ${event.schemaVersion}`);
}
```

Event versioning is one of the hardest parts of Event Sourcing.

Unlike normal database rows, old events remain important because they may be replayed.

---

#### Upcasting

**Upcasting** transforms old event versions into newer shapes before application code handles them.

```mermaid
flowchart TD
    OldEvent[OrderCreated v1]
    Upcaster[Upcaster]
    NewShape[OrderCreated v2 shape]
    Handler[Current Event Handler]

    OldEvent --> Upcaster
    Upcaster --> NewShape
    NewShape --> Handler
```

Example:

```ts
function upcastOrderCreated(event: StoredEvent): StoredEvent {
  if (
    event.eventType === "OrderCreated" &&
    event.schemaVersion === 1
  ) {
    return {
      ...event,
      schemaVersion: 2,
      data: {
        ...event.data,
        currency: "USD"
      }
    };
  }

  return event;
}
```

This lets the rest of the application handle a consistent event shape.

Upcasting is useful, but too many upcasters can become difficult to manage. Event schema design still matters.

---

#### Immutability

Events are usually immutable.

Once an event is written, it represents something that happened.

You generally do not update it.

Bad:

```sql
UPDATE events
SET event_data = ...
WHERE event_id = 'evt_123';
```

Better:

```text
Append a correcting event.
```

For example, if a customer’s address was recorded incorrectly:

```text
CustomerAddressRecorded
CustomerAddressCorrected
```

If an order was wrongly cancelled:

```text
OrderCancelled
OrderCancellationReversed
```

This preserves the truth that the mistaken event happened, and also records the correction.

This is important for auditability.

---

#### Handling sensitive data

Event immutability creates challenges for sensitive data.

If events are permanent, you must be careful about what you put in them.

Avoid storing unnecessary sensitive data in events.

Bad:

```json
{
  "eventType": "PaymentMethodAdded",
  "data": {
    "cardNumber": "4111111111111111",
    "cvv": "123"
  }
}
```

Better:

```json
{
  "eventType": "PaymentMethodAdded",
  "data": {
    "paymentMethodId": "pm_123",
    "cardBrand": "Visa",
    "last4": "1111"
  }
}
```

Consider:

* data minimization,
* encryption,
* tokenization,
* retention policies,
* key destruction,
* redaction events,
* separate secure stores for sensitive data,
* legal requirements such as deletion or anonymization.

Event Sourcing and privacy regulations require careful design.

Do not treat the event store as a place to dump every detail forever.

---

#### Deletion and retention

Event Sourcing complicates deletion because history is the source of truth.

For some domains, events must be retained for compliance.

For others, personal data must be deleted or anonymized.

Common strategies:

| Strategy                       | Description                                   |
| ------------------------------ | --------------------------------------------- |
| Avoid sensitive data in events | Store references or tokens instead            |
| Encrypt sensitive fields       | Destroy keys when data must become unreadable |
| Append redaction events        | Preserve history while marking data removed   |
| Separate PII store             | Events reference PII by ID                    |
| Retention windows              | Delete old events after policy allows         |
| Aggregate archival             | Move old streams to cold storage              |

Example redaction event:

```json
{
  "eventType": "CustomerPersonalDataRedacted",
  "aggregateId": "cus_123",
  "data": {
    "redactedFields": ["email", "phoneNumber"],
    "reason": "DATA_DELETION_REQUEST"
  }
}
```

The right strategy depends on legal, compliance, and business requirements.

---

#### Event Sourcing and domain modeling

Event Sourcing works best when events are meaningful domain facts.

For example, in an insurance claims system:

```text
ClaimSubmitted
DocumentsUploaded
ClaimAssignedToAdjuster
DamageAssessmentCompleted
ClaimApproved
PaymentIssued
ClaimClosed
```

These events describe the business process.

Poor event modeling would look like this:

```text
ClaimRowInserted
ClaimStatusColumnUpdated
ClaimJsonChanged
```

Those events describe database operations, not domain meaning.

Good event sourcing requires good domain modeling.

Ask domain experts:

* What happened?
* What does this event mean?
* Who caused it?
* What business process does it belong to?
* What should be true after this event?
* What event would the business recognize?

Event names should be part of the ubiquitous language of the domain.

---

#### Event Sourcing in banking example

A bank account is a classic example.

Events:

```text
AccountOpened
MoneyDeposited
MoneyWithdrawn
TransferSent
TransferReceived
AccountFrozen
AccountClosed
```

Current balance is derived from events.

```ts
type BankAccountEvent =
  | {
      eventType: "AccountOpened";
      data: {
        accountId: string;
        openingBalanceCents: number;
      };
    }
  | {
      eventType: "MoneyDeposited";
      data: {
        amountCents: number;
      };
    }
  | {
      eventType: "MoneyWithdrawn";
      data: {
        amountCents: number;
      };
    };

type BankAccountState = {
  accountId: string;
  balanceCents: number;
  opened: boolean;
};

function applyBankAccountEvent(
  state: BankAccountState,
  event: BankAccountEvent
): BankAccountState {
  switch (event.eventType) {
    case "AccountOpened":
      return {
        accountId: event.data.accountId,
        balanceCents: event.data.openingBalanceCents,
        opened: true
      };

    case "MoneyDeposited":
      return {
        ...state,
        balanceCents: state.balanceCents + event.data.amountCents
      };

    case "MoneyWithdrawn":
      return {
        ...state,
        balanceCents: state.balanceCents - event.data.amountCents
      };
  }
}
```

The balance is not the primary record. It is derived from the ledger of events.

This is why Event Sourcing is common in financial domains.

---

#### Event Sourcing for order lifecycle

Order lifecycle tracking is another good fit.

Events:

```text
OrderCreated
PaymentAuthorized
InventoryReserved
OrderConfirmed
ShipmentCreated
ShipmentDispatched
OrderDelivered
ReturnRequested
ReturnApproved
RefundIssued
```

This event history can answer:

* how long orders spend in each state,
* which step failed most often,
* whether payment or inventory came first,
* when customers request returns,
* why orders were cancelled,
* whether a shipment was created before order confirmation,
* what happened in a support dispute.

A current-state database can show that the order is delivered.

An event-sourced system can show the whole lifecycle.

---

#### Event Sourcing and debugging

Event Sourcing can make debugging easier because you can inspect the exact event sequence.

For example, an order unexpectedly ended in `CANCELLED`.

The event stream shows:

```text
OrderCreated
PaymentAuthorized
InventoryReservationFailed
PaymentAuthorizationVoided
OrderCancelled
```

This explains the cancellation.

Without events, you might only see:

```json
{
  "orderId": "ord_123",
  "status": "CANCELLED"
}
```

and need to search logs to reconstruct what happened.

Events become a durable debugging record.

However, this only works if events are well designed and metadata is complete.

---

#### Event Sourcing and analytics

Event history can feed analytics naturally.

For example, you can measure:

* time from order created to order confirmed,
* percentage of payments that fail,
* average time to approve a claim,
* number of retries before success,
* common cancellation reasons,
* state transition frequencies,
* customer behavior over time.

```mermaid
flowchart TD
    EventStore[(Event Store)]
    AnalyticsPipeline[Analytics Pipeline]
    Warehouse[(Data Warehouse)]
    Reports[Reports and Analysis]

    EventStore --> AnalyticsPipeline
    AnalyticsPipeline --> Warehouse
    Warehouse --> Reports
```

The event stream captures business activity in a rich form.

But be careful: event-sourced domain events are not automatically analytics-ready. You may still need transformation, privacy filtering, and schema governance.

---

#### Event Sourcing and integration events

There is an important distinction between internal domain events and external integration events.

Internal event:

```json
{
  "eventType": "PaymentAuthorizationRiskCheckPassed",
  "aggregateId": "pay_123",
  "data": {
    "riskScore": 0.12
  }
}
```

External integration event:

```json
{
  "eventType": "PaymentAuthorized",
  "paymentId": "pay_123",
  "orderId": "ord_456",
  "amountCents": 12999,
  "currency": "USD"
}
```

Internal events may be detailed and service-specific.

External events should be stable contracts for other services.

```mermaid
flowchart TD
    EventStore[(Internal Event Store)]
    Translator[Integration Event Publisher]
    EventBus[(External Event Bus)]

    EventStore --> Translator
    Translator --> EventBus
```

Do not automatically expose every internal event to the rest of the organization.

Use integration events as stable published contracts.

---

#### Event Sourcing and snapshots vs projections

Snapshots and projections are different.

| Concept     | Purpose                       |
| ----------- | ----------------------------- |
| Snapshot    | Speeds up aggregate loading   |
| Projection  | Supports queries              |
| Event store | Source of truth               |
| Read model  | Query-optimized derived state |

A snapshot is used internally when rebuilding an aggregate.

A projection is used externally for reads.

```mermaid
flowchart TD
    EventStore[(Event Store)]

    Snapshot[(Snapshot Store)]
    Aggregate[Aggregate Load]

    Projector[Projector]
    ReadModel[(Read Model)]

    EventStore --> Snapshot
    Snapshot --> Aggregate
    EventStore --> Aggregate

    EventStore --> Projector
    Projector --> ReadModel
```

Do not confuse the two.

Snapshots optimize writes and command handling. Projections optimize reads.

---

#### Event Sourcing and failure recovery

Because events are the source of truth, many failures can be recovered by replay.

If a read model is corrupted:

```mermaid
flowchart TD
    EventStore[(Event Store)]
    BrokenReadModel[(Broken Read Model)]
    Rebuild[Rebuild Projection]
    NewReadModel[(Rebuilt Read Model)]

    BrokenReadModel --> Rebuild
    EventStore --> Rebuild
    Rebuild --> NewReadModel
```

If a projection bug is fixed, replay events into a new projection.

If a report needs new fields, build a new projector.

If a workflow bug occurred, inspect the event sequence.

This recovery power is one of the biggest benefits of Event Sourcing.

---

#### Event Sourcing and external side effects

Be careful when replaying events that trigger side effects.

Safe replay:

* rebuild read model,
* rebuild search index,
* recalculate analytics,
* reconstruct aggregate state.

Risky replay:

* send emails,
* charge cards,
* create shipments,
* notify external partners,
* issue refunds.

A projection that sends emails should not send emails again during replay.

Separate side-effect handlers from replayable projections.

```mermaid
flowchart TD
    EventStore[(Event Store)]

    ReplayableProjection[Replayable Projection<br/>updates read model]
    SideEffectHandler[Side Effect Handler<br/>sends email or calls provider]

    ReadDB[(Read DB)]
    ExternalSystem[External System]

    EventStore --> ReplayableProjection
    ReplayableProjection --> ReadDB

    EventStore --> SideEffectHandler
    SideEffectHandler --> ExternalSystem
```

Side-effect handlers need idempotency and replay controls.

---

#### Example: prevent duplicate side effects

Suppose `OrderConfirmed` sends an email.

Bad handler:

```ts
async function handleOrderConfirmed(event: OrderConfirmedEvent): Promise<void> {
  await emailClient.sendOrderConfirmation(event.data.orderId);
}
```

If events are replayed, emails are sent again.

Better:

```ts
async function handleOrderConfirmed(event: OrderConfirmedEvent): Promise<void> {
  const notificationId = `order-confirmation:${event.data.orderId}`;

  const created = await notificationRepository.createIfNotExists({
    notificationId,
    orderId: event.data.orderId,
    eventId: event.eventId,
    status: "PENDING"
  });

  if (!created) {
    return;
  }

  await emailClient.sendOrderConfirmation(event.data.orderId);

  await notificationRepository.markSent(notificationId);
}
```

The handler records that the side effect already happened.

Replay safety must be designed explicitly.

---

#### Testing Event Sourcing

Event-sourced systems are often tested with a “given, when, then” style.

* **Given** past events
* **When** a command is handled
* **Then** new events should be produced

Example:

```ts
describe("ConfirmOrder", () => {
  it("emits OrderConfirmed when payment and inventory are ready", () => {
    const pastEvents: OrderEvent[] = [
      {
        eventType: "OrderCreated",
        data: {
          orderId: "ord_123",
          customerId: "cus_456",
          totalAmountCents: 12999,
          currency: "USD"
        }
      },
      {
        eventType: "PaymentAuthorized",
        data: {
          paymentId: "pay_123"
        }
      },
      {
        eventType: "InventoryReserved",
        data: {
          reservationId: "res_123"
        }
      }
    ];

    const state = rebuildOrderState("ord_123", pastEvents);

    const newEvents = confirmOrder(state, {
      orderId: "ord_123"
    });

    expect(newEvents).toEqual([
      {
        eventType: "OrderConfirmed",
        data: {}
      }
    ]);
  });

  it("rejects confirmation before inventory is reserved", () => {
    const pastEvents: OrderEvent[] = [
      {
        eventType: "OrderCreated",
        data: {
          orderId: "ord_123",
          customerId: "cus_456",
          totalAmountCents: 12999,
          currency: "USD"
        }
      }
    ];

    const state = rebuildOrderState("ord_123", pastEvents);

    expect(() =>
      confirmOrder(state, {
        orderId: "ord_123"
      })
    ).toThrow("Order cannot be confirmed until inventory is reserved");
  });
});
```

This testing style is powerful because it directly tests business behavior through event history.

---

#### Observability

Event-sourced systems need observability around event streams and projections.

Track:

* events appended per aggregate type,
* append failures,
* optimistic concurrency conflicts,
* event store latency,
* stream length,
* projection lag,
* projection failures,
* replay progress,
* snapshot creation,
* snapshot load time,
* event version distribution,
* upcaster failures,
* poison events,
* side-effect handler duplicates,
* read model freshness.

Example structured log:

```json
{
  "component": "event-store",
  "operation": "append",
  "aggregateType": "Order",
  "aggregateId": "ord_123",
  "expectedVersion": 3,
  "newVersion": 4,
  "eventType": "OrderConfirmed",
  "eventId": "evt_456",
  "correlationId": "corr_789",
  "latencyMs": 12
}
```

Projection log:

```json
{
  "component": "order-summary-projector",
  "eventId": "evt_456",
  "eventType": "OrderConfirmed",
  "aggregateId": "ord_123",
  "projectedAt": "2026-04-29T12:00:02Z",
  "projectionLagMs": 700
}
```

Without projection monitoring, read models can silently fall behind.

---

#### When to use it

Use Event Sourcing when the history of changes is as important as the current state.

Good use cases include:

* banking ledgers,
* payment lifecycle tracking,
* insurance claims,
* healthcare workflows,
* compliance-heavy systems,
* audit-heavy systems,
* order lifecycle tracking,
* subscription lifecycle tracking,
* financial reconciliation,
* trading systems,
* workflow systems with important state transitions,
* systems that need replay and temporal analysis.

Event Sourcing is especially useful when you need to answer:

* What exactly happened?
* When did it happen?
* Who caused it?
* What was the state at a previous time?
* Can we rebuild the state?
* Can we create new projections from old history?
* Can we prove the sequence of business events?

---

#### When not to use it

Avoid Event Sourcing when:

* the system is simple CRUD,
* history is not important,
* audit requirements are modest,
* the team is unfamiliar with event-based modeling,
* event versioning would be too costly,
* the domain has poorly understood events,
* data deletion requirements conflict with event retention,
* current-state queries are all you need,
* replay is not valuable,
* operational maturity is low.

For example, a simple product category admin screen probably does not need Event Sourcing.

A normal current-state table plus an audit log may be enough.

Event Sourcing is powerful, but it is not a default persistence choice.

---

#### Benefits

**1. Complete history**

Every state change is preserved as an event.

**2. Strong auditability**

Events can show who did what, when, and why.

**3. Replay**

Read models can be rebuilt from the event stream.

**4. Temporal analysis**

The system can reconstruct state at a previous point in time.

**5. Better debugging**

The exact sequence of events can explain unexpected state.

**6. Natural fit for event-driven systems**

Domain events are already the source of truth.

**7. Supports multiple projections**

One event stream can feed many read models.

**8. Avoids losing business meaning**

Events describe business facts, not just final state.

---

#### Trade-offs

**1. More complex mental model**

Developers must think in events, streams, aggregates, projections, and replay.

**2. Event versioning is hard**

Old events may need to be supported forever.

**3. Querying requires projections**

Event streams are not convenient for most user-facing queries.

**4. Replay can be risky**

Side effects must not repeat during replay.

**5. Storage grows over time**

Events are append-only and may accumulate indefinitely.

**6. Privacy and deletion are harder**

Immutable history can conflict with data deletion requirements.

**7. Debugging projections can be complex**

Current read state may depend on many historical events.

**8. Bad event design is costly**

Poorly named or overly technical events become long-term baggage.

---

#### Common mistakes

**Mistake 1: Using Event Sourcing for simple CRUD**

If history and replay are not valuable, the complexity is probably not worth it.

**Mistake 2: Treating events like database change logs**

Good events represent business facts, not table mutations.

**Mistake 3: Exposing every internal event externally**

Internal domain events and integration events have different audiences and stability requirements.

**Mistake 4: Ignoring event versioning**

Events live a long time. Schema evolution must be planned.

**Mistake 5: No projection monitoring**

Read models can silently become stale or broken.

**Mistake 6: Replaying side effects**

Rebuilding a read model should not resend emails or recharge cards.

**Mistake 7: Storing too much sensitive data in events**

Immutable event stores require careful privacy design.

**Mistake 8: No snapshot strategy for long streams**

Very long streams can become expensive to load.

**Mistake 9: Assuming replay fixes everything**

Replay helps if events are correct and handlers are deterministic. It does not fix poorly modeled events.

---

#### Practical design checklist

Before using Event Sourcing, ask:

* Is history truly important?
* Do we need to reconstruct past state?
* Do we need replay?
* Do we need strong auditability?
* What are the domain events?
* Are events meaningful to domain experts?
* What is the aggregate boundary?
* What is the event stream boundary?
* What metadata must every event include?
* How are events versioned?
* How will old event versions be handled?
* Are upcasters needed?
* What read models are required?
* Who owns each projection?
* How will projection lag be monitored?
* Are projections rebuildable?
* What side effects are triggered by events?
* Are side effects idempotent?
* How do we prevent replay from repeating side effects?
* Are snapshots needed?
* What is the retention policy?
* Does the event store contain sensitive data?
* How will privacy and deletion requirements be handled?
* How will concurrency conflicts be handled?
* What operational tools are needed to inspect streams?

A good Event Sourcing design is likely if:

* events are meaningful business facts,
* history and auditability are real requirements,
* event schemas are governed,
* projections are owned and monitored,
* replay is safe,
* side effects are idempotent,
* privacy is designed carefully,
* snapshots are used where needed,
* the team understands the event-based model.

A poor Event Sourcing design is likely if:

* it is used only because it sounds advanced,
* events mirror table updates,
* no one owns event schemas,
* projections silently fail,
* replay resends external side effects,
* old events cannot be read by new code,
* sensitive data is stored forever without a plan,
* simple CRUD operations become unnecessarily complex.

---

#### Related patterns

| Pattern                   | Relationship                                                               |
| ------------------------- | -------------------------------------------------------------------------- |
| CQRS                      | Event Sourcing is often paired with CQRS because events feed read models   |
| Async Messaging           | Events can be published to other services or projectors                    |
| Choreography              | Event-sourced domain events can trigger choreographed workflows            |
| Saga Pattern              | Sagas may consume and emit events as workflow state changes                |
| Outbox Pattern            | Helps publish events reliably from state changes                           |
| Database per Service      | Each service can own its own event store                                   |
| Materialized View         | Projections from events often become materialized views                    |
| Consumer-Driven Contracts | Protects event schemas used by consumers                                   |
| Audit Log                 | Event Sourcing can provide a stronger audit trail than separate audit logs |
| Snapshotting              | Optimizes loading aggregates with long event streams                       |

---

#### Summary

Event Sourcing stores state changes as immutable events rather than storing only the latest state.

The central idea is:

> The event history is the source of truth. Current state is derived by replaying events.

This pattern is valuable for banking, payments, insurance, healthcare, order lifecycle tracking, compliance-heavy workflows, and systems where auditability and history matter deeply.

A good Event Sourcing design has:

* meaningful domain events,
* append-only event streams,
* reliable event storage,
* optimistic concurrency,
* versioned event schemas,
* projections for queries,
* replay-safe handlers,
* idempotent side effects,
* snapshotting where needed,
* and strong observability.

The trade-off is complexity. Event Sourcing changes how teams think about persistence. It adds challenges around event versioning, projections, replay, storage growth, privacy, and operational tooling. Use it when the history is valuable enough to justify that complexity.


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

