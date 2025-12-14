from fastapi.testclient import TestClient

from collatz.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sequence_endpoint():
    response = client.post("/collatz/sequence", json={"start": 7})
    assert response.status_code == 200
    data = response.json()
    assert data["iterations"] == 16
    assert data["reached_one"] is True
    assert data["sequence"][0] == 7
    assert data["sequence"][-1] == 1


def test_sequence_endpoint_validation():
    response = client.post("/collatz/sequence", json={"start": 0})
    assert response.status_code == 422


def test_scan_endpoint():
    response = client.post("/collatz/scan", json={"start": 1, "count": 3})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 3
    assert data["data"][0]["start"] == 1
