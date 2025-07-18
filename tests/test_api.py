
from chatapp.main import app
from fastapi.testclient import TestClient

def test_health_check():
    client = TestClient(app)
    response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401

def test_chat_response():
    token = "Bearer invalid_token"
    payload = {
        "session_id": "testsession123",
        "message": "What is the return policy?"
    }

    client = TestClient(app)
    response = client.post("/chat", json=payload, headers={"Authorization": token})
    assert response.status_code in [401, 500]