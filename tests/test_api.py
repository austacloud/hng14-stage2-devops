from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# ---------------- HEALTH CHECK ----------------


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ---------------- CREATE JOB ----------------
@patch("api.main.get_redis")
def test_create_job(mock_redis):
    mock_redis.lpush.return_value = 1

    response = client.post("/jobs", json={})
    assert response.status_code == 200

    data = response.json()
    assert "job_id" in data


# ---------------- GET JOB STATUS ----------------
@patch("api.main.get_redis")
def test_get_job_status(mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.get.return_value = "completed"

    # create job
    create = client.post("/jobs", json={})
    job_id = create.json()["job_id"]

    # check status
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert "status" in response.json()
