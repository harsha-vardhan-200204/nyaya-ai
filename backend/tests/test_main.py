import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Verify that the API root endpoint returns the online status details."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert "NyayaAI" in response.json()["system"]

def test_user_registration_and_login():
    """Verify registration, duplicate block, and token generation flows."""
    import random
    unique_id = random.randint(1000, 9999)
    username = f"tester_{unique_id}"
    email = f"tester_{unique_id}@nyaya.ai"
    
    # 1. Register
    reg_payload = {
        "username": username,
        "email": email,
        "password": "securepassword123",
        "role": "Client"
      }
    response = client.post("/api/auth/register", json=reg_payload)
    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["role"] == "Client"
    
    # 2. Duplicate Check
    response_dup = client.post("/api/auth/register", json=reg_payload)
    assert response_dup.status_code == 400
    
    # 3. Login
    login_payload = {
        "username": username,
        "password": "securepassword123"
    }
    response_login = client.post("/api/auth/login", json=login_payload)
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()
    assert response_login.json()["role"] == "Client"
    assert response_login.json()["token_type"] == "bearer"

def test_legal_acts_index():
    """Verify that seeded legal acts can be successfully retrieved."""
    response = client.get("/api/legal/acts")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "Indian Contract Act" in [act["name"] for act in response.json()]
