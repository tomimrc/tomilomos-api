"""Tests for the health check endpoint."""

from fastapi.testclient import TestClient


def test_health_check_status_ok(test_client: TestClient):
    """Test that health check endpoint returns 200 and correct JSON."""
    response = test_client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data
    assert data["version"] == "1.0.0"


def test_health_check_timestamp_format(test_client: TestClient):
    """Test that health check returns ISO format timestamp."""
    response = test_client.get("/api/v1/health")
    data = response.json()
    
    # Should be valid ISO format (can be parsed)
    from datetime import datetime
    try:
        datetime.fromisoformat(data["timestamp"])
        assert True
    except ValueError:
        assert False, "Timestamp is not valid ISO format"
