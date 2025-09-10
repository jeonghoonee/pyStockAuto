"""
Test Hello Controller

Tests for hello controller functionality.
"""

import pytest
from fastapi.testclient import TestClient

def test_hello_endpoint(test_client: TestClient):
    """Test hello endpoint"""
    response = test_client.get("/api/hello")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "Hello! PyStockAuto Start!" in data["message"]
    assert "timestamp" in data
    assert "service" in data
    assert data["service"] == "PyStockAuto"

def test_root_endpoint(test_client: TestClient):
    """Test root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "PyStockAuto" in data["message"]

def test_health_endpoint(test_client: TestClient):
    """Test health check endpoint"""
    response = test_client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "PyStockAuto"
