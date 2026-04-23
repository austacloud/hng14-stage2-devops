from fastapi.testclient import TestClient
from api.main import app   # adjust if your file name is different

client = TestClient(app)

# ---------------- HEALTH CHECK ----------------
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ---------------- CREATE JOB ----------------
def test_create_job():
    response = client.post("/jobs", json={})
    assert response.status_code == 200

    data = response.json()
    assert "job_id" in data


# ---------------- GET JOB STATUS ----------------
def test_get_job_status():
    # create job first
    create = client.post("/jobs", json={})
    job_id = create.json()["job_id"]

    # check status
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert "status" in response.json()