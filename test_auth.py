import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "test123",
            "name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_login_user():
    # First register
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "test123",
            "name": "Login Test"
        }
    )
    
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "test123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_profile():
    # First register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "profile@example.com",
            "password": "test123",
            "name": "Profile Test"
        }
    )
    
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "profile@example.com",
            "password": "test123"
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Get profile
    response = client.get(
        "/api/v1/auth/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "profile@example.com"
    assert "password" not in data
