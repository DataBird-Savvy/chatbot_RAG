from chatapp.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_login_with_invalid_credentials():
    response = client.post("/token", data={
        "username": "invaliduser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_users_me_with_invalid_token():
    response = client.get("/users/me", headers={
        "Authorization": "Bearer invalid_token"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_login_with_valid_credentials():
    response = client.post("/token", data={
        "username": "Username",
        "password": "password"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

    # Use the token to call protected endpoint
    user_response = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert user_response.status_code == 200
    assert user_response.json()["username"] == "Username"
