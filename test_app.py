from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_list_todo():
    response = client.post("/todos", json={"title": "test todo"})
    assert response.status_code == 200
    todo = response.json()
    assert todo["title"] == "test todo"
    assert todo["done"] is False

    response = client.get("/todos")
    assert response.status_code == 200
    titles = [t["title"] for t in response.json()]
    assert "test todo" in titles

def test_config():
    response = client.get("/config")
    assert response.status_code == 200
    assert "APP_GREETING" in response.json()
