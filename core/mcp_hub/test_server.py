import pytest
from fastapi.testclient import TestClient
from server import app
import db
import sqlite3
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Initialize a clean in-memory database or use the test setup
    db.init_db()
    
    # Clear out all tasks for a clean slate
    with sqlite3.connect(db.DB_PATH) as conn:
        conn.execute("DELETE FROM tasks")
        conn.commit()
    yield

def test_recommendations_pdf():
    response = client.post("/api/recommendations", json={
        "category": "financial_reports",
        "file_format": ".pdf",
        "asset_count": 15
    })
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["service_id"] == "pdf-ingestion"

def test_recommendations_hr():
    response = client.post("/api/recommendations", json={
        "category": "internal_memo",
        "file_format": ".docx",
        "asset_count": 55
    })
    assert response.status_code == 200
    data = response.json()
    assert data["recommendations"][0]["service_id"] == "hr-analytics"

def test_recommendations_fallback():
    response = client.post("/api/recommendations", json={
        "category": "unknown",
        "file_format": ".txt",
        "asset_count": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["recommendations"][0]["service_id"] == "generic-classifier"

@patch("server.trigger_npu_fine_tune")
def test_opt_in_task(mock_trigger):
    mock_trigger.return_value = {
        "status": "success",
        "task_id": "test_npu_id",
        "job_status": "queued"
    }
    
    response = client.post("/api/tasks/opt-in?service_id=hr-analytics")
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "STARTING"
    assert "npu_relay" in data
    assert data["npu_relay"]["status"] == "success"

def test_list_tasks():
    # Create a task
    client.post("/api/tasks/opt-in?service_id=pdf-ingestion")
    
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert len(data["tasks"]) == 1
    task = list(data["tasks"].values())[0]
    assert task["service_id"] == "pdf-ingestion"
    assert task["status"] == "STARTING"

@patch("server.fetch_npu_system_health")
def test_npu_health(mock_health):
    mock_health.return_value = {"status": "online", "version": "1.0.0"}
    response = client.get("/api/npu/status")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
