# RAG Gateway Service

A FastAPI-based gateway service that automatically routes queries to topic-specific RAG agents using AI-powered topic detection.

## Features

- Automatic topic detection using OpenAI embeddings
- Configurable routing to topic-specific agents
- Fallback agent for unknown topics
- Environment variable configuration
- Docker support
- Comprehensive test coverage

## Project Structure

```
rag-gateway/
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── router.py              # /query endpoint
│   ├── config.py              # YAML config loader
│   ├── schema.py              # Request/response models
│   ├── client.py              # HTTP client to call agents
│   └── utils.py               # Helper functions
├── config.yaml                # Routing config
├── tests/
│   └── test_routing.py        # Unit + integration tests
├── scripts/
│   ├── start.sh              # Script to start the service
│   └── test.sh               # Script to run tests
├── Dockerfile                 # For containerizing the gateway
├── docker-compose.yml         # For local testing with mock agents
├── requirements.txt
└── README.md
```

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the tests:
   ```bash
   ./scripts/test.sh
   ```

4. Start the services using Docker Compose:
   ```bash
   ./scripts/start.sh
   ```

## API Usage

Send a POST request to `/api/v1/query` with the following JSON payload:

```json
{
  "message": "How do I reset my password?"
}
```

The service will:
1. Detect the topic using AI embeddings
2. Route the query to the appropriate agent
3. Return a response with the detected topic and confidence score

Example response:
```json
{
  "response": "To reset your password, click the 'Forgot Password' link.",
  "detected_topic": "password_reset",
  "metadata": {
    "confidence": 0.95,
    "agent_metadata": {
      "source": "password_reset_guide"
    }
  }
}
```

## Configuration

The service uses a YAML configuration file (`config.yaml`) to define topics and their corresponding agent URLs. Each topic includes:
- Route: The URL of the agent service
- Descriptions: Example queries and descriptions for topic detection

Example configuration:
```yaml
topics:
  password_reset:
    route: ${AGENT_PASSWORD_RESET_URL}/query
    descriptions:
      - "How to reset password"
      - "Forgot password"
      - "Change password"
  billing:
    route: ${AGENT_BILLING_URL}/query
    descriptions:
      - "Billing questions"
      - "Payment issues"
      - "Invoice problems"

default_agent: ${AGENT_FALLBACK_URL}/query
```

## Environment Variables

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `AGENT_PASSWORD_RESET_URL`: URL for password reset agent
- `AGENT_BILLING_URL`: URL for billing agent
- `AGENT_FALLBACK_URL`: URL for fallback agent

Optional environment variables:
- `ENVIRONMENT`: Deployment environment (default: "development")
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: 30.0)
- `CORS_ORIGINS`: Allowed CORS origins (default: ["*"])
- `CORS_METHODS`: Allowed CORS methods (default: ["*"])
- `CORS_HEADERS`: Allowed CORS headers (default: ["*"])

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest tests/ -v
```

4. Start the service:
```bash
uvicorn app.main:app --reload
```

## Docker Deployment

1. Build the image:
```bash
docker build -t rag-gateway .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env rag-gateway
```

## Testing

The service includes comprehensive tests for:
- Health check endpoint
- Configuration loading
- Topic detection
- Query routing
- Error handling

Run tests with:
```bash
pytest tests/ -v
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 