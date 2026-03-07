from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_exercises_endpoint_exists():
    r = client.get("/exercises?limit=5")
    assert r.status_code == 200
    assert isinstance(r.json(), list)