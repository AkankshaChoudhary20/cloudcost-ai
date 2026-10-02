from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analysis():
    response = client.get("/api/v1/analysis")
    assert response.status_code == 200
    body = response.json()
    assert body["monthly_spend"] == 1240.5
    assert body["potential_monthly_savings"] > 0
    assert len(body["recommendations"]) == 4

def test_explain_without_bedrock():
    analysis = client.get("/api/v1/analysis").json()
    response = client.post("/api/v1/explain", json={"analysis": analysis})
    assert response.status_code == 200
    assert response.json()["provider"] == "deterministic"
