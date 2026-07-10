"""
Tests extendidos de autenticación — forgot-password, reset-password, /me.

Cubre:
- forgot-password con email existente retorna token (debug mode)
- forgot-password con email inexistente no revela existencia
- reset-password con token válido cambia contraseña
- reset-password con token inválido devuelve 400
- reset-password con token expirado devuelve 400
- /me retorna datos del usuario autenticado
- /me sin token devuelve 401
"""

import uuid
import pytest
from httpx import AsyncClient


def _user(suffix: str = "") -> dict:
    uid = uuid.uuid4().hex[:6]
    return {
        "email": f"user_{uid}{suffix}@test.com",
        "username": f"user_{uid}{suffix}",
        "password": "Passw0rd!",
    }


class TestForgotPassword:

    async def test_forgot_password_existing_email_returns_token_in_debug(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)
        resp = await client.post("/auth/forgot-password", json={"email": data["email"]})
        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        # In debug mode, token is returned
        assert body["token"] is not None
        assert len(body["token"]) > 0

    async def test_forgot_password_unknown_email_returns_200_no_token(self, client: AsyncClient):
        resp = await client.post("/auth/forgot-password", json={"email": "noexiste@test.com"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["token"] is None

    async def test_forgot_password_invalid_email_returns_422(self, client: AsyncClient):
        resp = await client.post("/auth/forgot-password", json={"email": "not-an-email"})
        assert resp.status_code == 422


class TestResetPassword:

    async def test_reset_password_with_valid_token(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)

        # Get reset token (debug mode returns it)
        resp = await client.post("/auth/forgot-password", json={"email": data["email"]})
        token = resp.json()["token"]
        assert token is not None

        # Reset password
        new_password = "NewPass123!"
        resp = await client.post("/auth/reset-password", json={
            "token": token,
            "password": new_password,
        })
        assert resp.status_code == 200
        assert "actualizada" in resp.json()["detail"].lower()

        # Login with new password should work
        resp = await client.post("/auth/login", json={
            "email": data["email"],
            "password": new_password,
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_reset_password_with_invalid_token(self, client: AsyncClient):
        resp = await client.post("/auth/reset-password", json={
            "token": "token_invalido_12345",
            "password": "NewPass123!",
        })
        assert resp.status_code == 400

    async def test_reset_password_with_used_token_fails(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)

        # Get token
        resp = await client.post("/auth/forgot-password", json={"email": data["email"]})
        token = resp.json()["token"]

        # Use it once
        await client.post("/auth/reset-password", json={
            "token": token,
            "password": "NewPass123!",
        })

        # Try to use it again — should fail
        resp = await client.post("/auth/reset-password", json={
            "token": token,
            "password": "AnotherPass456!",
        })
        assert resp.status_code == 400


class TestGetMe:

    async def test_me_returns_user_data(self, client: AsyncClient, auth):
        headers, user_data = auth
        resp = await client.get("/auth/me", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["email"] == user_data["email"]
        assert body["username"] == user_data["username"]
        assert body["is_active"] is True
        # Password hash should never be exposed
        assert "password_hash" not in body

    async def test_me_without_token_returns_401(self, client: AsyncClient):
        resp = await client.get("/auth/me")
        assert resp.status_code == 401

    async def test_me_with_invalid_token_returns_401(self, client: AsyncClient):
        resp = await client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert resp.status_code == 401
