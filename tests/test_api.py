""" ML API Tests 
Tests functionality, not ML accuracy
CI-safe: runs without GPU, cloud resources, or real data
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import numpy as np

@pytest.fixture(scope="module")
def client():
    """Create a test client that persists across all tests in this module"""
    with TestClient(app) as test_client:
        yield test_client

def test_health_check(client):
    """ Test: Health endpoint returns 200 and correct structure
        Why: Kubernetes needs this to know if pod is alive
    """

    response = client.get("/health")

    #check status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    #check response structure 
    data = response.json()
    assert "status" in data, "Missing 'status' in response"
    assert "model_loaded" in data, "Missing 'model_loaded' in response"

    assert "model_loaded" in data, "Model should be loaded"

    print("✅ Health check passed")

def test_prediction_endpoint_success(client):
    """
    Test: Valid input returns prediction with correct structure
    Why: Core functionality - if this fails, app is broken
    """
    payload = { "features": [5.1, 3.5, 1.4, 0.2] }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    required_fields = ["prediction", "prediction_index", "confidence", "all_probabilities"]
    for field in required_fields:
        assert field in data, f"Missing '{field}' in response"

    assert isinstance(data["prediction"], str), "'prediction' should be a string"
    assert isinstance(data["prediction_index"], int), "'prediction_index' should be an integer"
    assert isinstance(data["confidence"], float), "'confidence' should be a float"
    assert isinstance(data["all_probabilities"], dict), "'all_probabilities' should be a dictionary"

    assert 0 <= data["confidence"] <= 1, "'confidence' should be between 0 and 1"
    assert 0.0 <= data["prediction_index"] < 2.0, "'prediction_index' should be a valid class index"

    assert data["prediction"] in ["setosa", "versicolor", "virginica"], f"Unexpected prediction: {data['prediction']}"
    
    prob_sum = sum(data["all_probabilities"].values())

    assert 0.99 <= prob_sum <= 1.01, f"Probabilities should sum to 1, got {prob_sum}"

    print(f"✅ Prediction endpoint success test passed: {data['prediction']} ({data['confidence']:.2f} confidence)")


def test_prediction_wrong_feature_count(client):
    """
    Test: Wrong number of features returns 400 error
    Why: Input validation prevents crashes
    """
    payload = { "features": [5.1, 3.5, 1.4] }

    response = client.post("/predict", json=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    print("✅ Error handling test passed (wrong feature count)")

def test_prediction_invalid_data_type(client):
    """
    Test: Invalid data type returns 422 error
    Why: Pydantic validation catches type errors
    """

    payload = {"features": ['a', 'b', 'c', 'd']}

    response = client.post("/predict", json=payload)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    print("✅ Error handling test passed (invalid data type)")

def test_prediction_missing_features(client):
    """
    Test: Missing features key returns 422 error
    Why: Required field validation
    """

    payload = {}

    response = client.post("/predict", json=payload)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    print("✅ Error handling test passed (missing features)")

def test_root_endpoint(client):
    """
    Test: Root endpoint returns API info
    Why: Useful for API discovery and health monitoring
    """
    
    response = client.get("/")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert "message" in data, "Missing 'message' in response"
    assert "endpoints" in data, "Missing 'endpoints' in response"

    print("✅ Root endpoint test passed")
    