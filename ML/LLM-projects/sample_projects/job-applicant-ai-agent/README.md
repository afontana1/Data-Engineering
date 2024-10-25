# AI Agents and GPTs Base Cloud Native Microservice Template - Event Driven Architecture

### Overview
This project implements a cloud-native ai microservice template with an event-driven architecture. 

Think of it as a starter kit to develop Multi Agents API's and Custom GPTs. It comes packed with:

- Cloud Native Development Environment Setup
- Authentication and User Management Microservice
- Crew AI Multi Agent Microservice 
- Kafka for Asynchronous Communication Across Microservices
- Kong as API Management Layer 

There are a lot of exciting add-ons like Postgres, PgAdmin, Kafka-UI, Protobuf, Schema Registry base config and Central Management. The Goal here is to keep it a minimal starter kit without any closed source package or tools. The Authentication is managed fully by oauth-users microservice.

Best part you just need Docker and VS Code to Run it - Nothing else on your Machine. Before Going to TOC head's on:

What's Missing here is particularly Deployment and Testing Tools:
- Kubernetes: Container orchestration system for automating deployment, scaling, and management.
- Terraform: Infrastructure as Code (IaC) tool.
- testcontainers: Provides lightweight, disposable instances of common databases.
- GitHub Actions: CI/CD tool that automates workflows, including testing and deployment.
- F.E: A Super Simple NextJS 15 F.E Client

### Table of Contents
- [Overview](#overview)
- [Core Features](#core-features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Microservices](#microservices)
  - [Auth Microservice](#auth-microservice)
  - [Todo Microservice](#todo-microservice)
  - [Recommendation Engine Microservice](#recommendation-engine-microservice)
- [Event Service](#event-service)
- [Frontend Client](#frontend-client)
- [Contributing](#contributing)
- [License](#license)

### Core-Features
- **Auth Microservice:** Handles user authentication using OAuth2, produces and consumes authentication events.
- **Recommendation Engine:** AI Agent that Generates recommendations and perform actions - we have used Crew AI as base Multi Agent model, to sends recommendations via email, and produces events for saving recommendations.
- **Event Service:** Uses Kafka for managing and routing events between microservices.
- **Scalability and Resilience:** Designed for horizontal scaling and includes circuit breaker patterns.
- **Advanced Analytics and Logging:** Centralized logging and monitoring with tools like Prometheus.

### Architecture
![Architecture Diagram](path_to_architecture_diagram.png)

### Prerequisites
- [VSCode](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Ready to Make Some Cool AI Agents

### Getting Started
1. **Clone the Repository:**
   ```bash
   git clone ...
   cd cloud-native-microservice-template
    ```

2. **Set Up Environment:**
Ensure you have Docker Desktop installed.

3. **Start Services with Docker Compose:**

```bash
docker-compose up --build
```

4. **Access Services:**

- Auth Server: http://localhost:9000
- Todo Server: http://localhost:9002/
- Recommendation Server: http://localhost:9001
- PGAdmin: http://localhost:8010
- Kafka UI: http://localhost:8080
- Kong GUI: http://localhost:8002
- Kong Reverse Proxy Base Route: http://localhost:8000

### Microservices

#### Auth Microservice
**Purpose:** Handles user authentication and authorization.

**Features:**
- User registration
- User login
- Token management (OAuth2)

**Events Produced:**
- UserRegistered
- UserLoggedIn
- TokenIssued

#### Recommendation Engine Microservice
**Purpose:** Generates and sends task recommendations in MailBox.

**Features:**
- Generate recommendations using CrewAI Agent
- Send recommendations via email

<!-- **Events Produced:**
- RecommendationGenerated
- RecommendationSaved -->

**Events Consumed:**
- Todo Created


## Contributing
We welcome contributions from the community. Please read our Contributing Guidelines before submitting a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

This project is part of the PanaCloud Assignment. For more details, visit the Assignment Documentation.

