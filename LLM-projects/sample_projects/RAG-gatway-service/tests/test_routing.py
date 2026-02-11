import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import Config
from app.schema import QueryRequest, QueryResponse
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "development"
    }

@pytest.mark.asyncio
async def test_config_loading():
    config = Config()
    assert config.default_agent is not None
    assert "password_reset" in config.topics
    assert "billing" in config.topics
    assert len(config.topic_descriptions["password_reset"]) > 0
    assert len(config.topic_descriptions["billing"]) > 0

@patch('app.router.topic_detector.detect_topic')
@patch('httpx.AsyncClient.post')
def test_query_endpoint(mock_post, mock_detect_topic):
    # Mock topic detection
    mock_detect_topic.return_value = ("password_reset", 0.95)
    
    # Mock agent response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": "To reset your password, click the 'Forgot Password' link.",
        "metadata": {"source": "password_reset_guide"}
    }
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    request_data = {
        "message": "How do I reset my password?"
    }
    response = client.post("/api/v1/query", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "detected_topic" in data
    assert data["detected_topic"] == "password_reset"
    assert "confidence" in data["metadata"]

@patch('app.router.topic_detector.detect_topic')
@patch('httpx.AsyncClient.post')
def test_query_with_unknown_topic(mock_post, mock_detect_topic):
    # Mock topic detection with low confidence
    mock_detect_topic.return_value = ("unknown", 0.3)
    
    # Mock fallback agent response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": "I'm not sure about that. Please contact support.",
        "metadata": {"source": "fallback_agent"}
    }
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    request_data = {
        "message": "What is the meaning of life?"
    }
    response = client.post("/api/v1/query", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "detected_topic" in data
    assert data["detected_topic"] == "unknown"
    assert "confidence" in data["metadata"] 