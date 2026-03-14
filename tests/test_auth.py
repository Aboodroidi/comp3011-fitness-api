def test_register_user(client):
    payload = {
        "username": "abdullah",
        "email": "abdullah@example.com",
        "password": "StrongPass123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "abdullah"
    assert data["email"] == "abdullah@example.com"
    assert "id" in data


def test_register_duplicate_user_fails(client):
    payload = {
        "username": "abdullah",
        "email": "abdullah@example.com",
        "password": "StrongPass123"
    }

    first = client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 400
    assert second.json()["detail"] == "Username or email already exists"


def test_login_user(client):
    register_payload = {
        "username": "abdullah",
        "email": "abdullah@example.com",
        "password": "StrongPass123"
    }
    client.post("/auth/register", json=register_payload)

    login_payload = {
        "username": "abdullah",
        "password": "StrongPass123"
    }

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    payload = {
        "username": "unknown",
        "password": "wrongpass"
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"