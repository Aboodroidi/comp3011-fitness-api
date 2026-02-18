from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_and_get_workout():
    payload = {
        "date": "2026-02-17",
        "workout_type": "Push",
        "duration_min": 45,
        "notes": "Test session"
    }
    r = client.post("/workouts", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    workout_id = data["id"]

    r2 = client.get(f"/workouts/{workout_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["workout_type"] == "Push"

def test_get_missing_workout_returns_404():
    r = client.get("/workouts/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Workout not found"

def test_analytics_streak_endpoint():
    r = client.get("/analytics/streak")
    assert r.status_code == 200
    body = r.json()
    assert "current_streak" in body
    assert "longest_streak" in body