from datetime import timedelta
from urllib.parse import parse_qs, urlparse


def register(client, email="Carla@Example.COM"):
    return client.post(
        "/api/auth/register",
        json={"display_name": "  Carla  ", "email": email, "password": "password123"},
    )


def login(client, email="carla@example.com", password="password123"):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def test_register_normalizes_email_and_rejects_duplicate(client):
    created = register(client)
    assert created.status_code == 201
    assert created.json()["display_name"] == "Carla"
    assert created.json()["email"] == "carla@example.com"
    assert "password" not in created.text

    duplicate = register(client, "carla@example.com")
    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == "email_already_registered"


def test_login_me_logout_cookie_lifecycle(client):
    register(client)
    invalid = login(client, password="incorrect")
    assert invalid.status_code == 401
    assert invalid.json()["code"] == "invalid_credentials"

    authenticated = login(client)
    assert authenticated.status_code == 204
    cookie = authenticated.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "samesite=lax" in cookie

    current = client.get("/api/auth/me")
    assert current.status_code == 200
    assert current.json()["email"] == "carla@example.com"

    assert client.post("/api/auth/logout").status_code == 204
    assert client.get("/api/auth/me").status_code == 401


def test_recovery_is_enumeration_safe_and_reset_is_one_time(
    client, email_sender, mutable_clock
):
    register(client)
    login(client)
    existing = client.post("/api/auth/password-recovery", json={"email": "carla@example.com"})
    unknown = client.post("/api/auth/password-recovery", json={"email": "nobody@example.com"})

    assert existing.status_code == unknown.status_code == 202
    assert existing.json() == unknown.json()
    assert len(email_sender.outbox) == 1
    token = parse_qs(urlparse(email_sender.outbox[0].reset_url).query)["token"][0]

    reset = client.post(
        "/api/auth/password-reset",
        json={"token": token, "new_password": "new-password-123"},
    )
    assert reset.status_code == 204
    assert client.get("/api/auth/me").status_code == 401
    assert login(client, password="password123").status_code == 401
    assert login(client, password="new-password-123").status_code == 204

    reused = client.post(
        "/api/auth/password-reset",
        json={"token": token, "new_password": "another-password"},
    )
    assert reused.status_code == 400
    assert reused.json()["code"] == "invalid_reset_token"


def test_reset_token_expires_at_30_minutes(client, email_sender, mutable_clock):
    register(client)
    client.post("/api/auth/password-recovery", json={"email": "carla@example.com"})
    token = parse_qs(urlparse(email_sender.outbox[0].reset_url).query)["token"][0]
    mutable_clock.advance(minutes=30)

    response = client.post(
        "/api/auth/password-reset",
        json={"token": token, "new_password": "new-password-123"},
    )

    assert response.status_code == 400
    assert response.json()["code"] == "invalid_reset_token"


def test_validation_errors_follow_contract(client):
    response = client.post(
        "/api/auth/register",
        json={"display_name": "", "email": "bad", "password": "short"},
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert {"display_name", "email", "password"}.issubset(payload["field_errors"])
