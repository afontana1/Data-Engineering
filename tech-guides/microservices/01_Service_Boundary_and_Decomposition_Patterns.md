# Table of Contents

- [1. Service Boundary and Decomposition Patterns](#1-service-boundary-and-decomposition-patterns)
  - [1. Decompose by Business Capability](#1-decompose-by-business-capability)
  - [2. Decompose by Subdomain](#2-decompose-by-subdomain)
  - [3. Decompose by Transaction or Workflow Boundary](#3-decompose-by-transaction-or-workflow-boundary)
  - [4. Stateless Services](#4-stateless-services)

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
