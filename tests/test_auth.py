"""
Tests de autenticación — /auth/register y /auth/login.

Cubre:
- Registro exitoso devuelve 201 + access_token
- Email duplicado devuelve 409
- Username duplicado devuelve 409
- Login correcto devuelve 200 + access_token
- Login con contraseña incorrecta devuelve 401
- Ruta protegida sin token devuelve 403
- Token inválido devuelve 401
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


class TestRegister:

    async def test_register_returns_201_and_token(self, client: AsyncClient):
        resp = await client.post("/auth/register", json=_user())
        assert resp.status_code == 201
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert "user" in body
        assert body["user"]["is_active"] is True

    async def test_register_duplicate_email_returns_400(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)
        # Cambiar username pero mismo email
        data2 = {**data, "username": data["username"] + "_bis"}
        resp = await client.post("/auth/register", json=data2)
        assert resp.status_code == 400

    async def test_register_duplicate_username_returns_400(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)
        # Cambiar email pero mismo username
        data2 = {**data, "email": f"other_{uuid.uuid4().hex[:6]}@test.com"}
        resp = await client.post("/auth/register", json=data2)
        assert resp.status_code == 400

    async def test_register_short_password_returns_422(self, client: AsyncClient):
        data = {**_user(), "password": "abc"}
        resp = await client.post("/auth/register", json=data)
        assert resp.status_code == 422

    async def test_register_invalid_email_returns_422(self, client: AsyncClient):
        data = {**_user(), "email": "not-an-email"}
        resp = await client.post("/auth/register", json=data)
        assert resp.status_code == 422


class TestLogin:

    async def test_login_success_returns_token(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)
        resp = await client.post("/auth/login", json={
            "email": data["email"],
            "password": data["password"],
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_login_wrong_password_returns_401(self, client: AsyncClient):
        data = _user()
        await client.post("/auth/register", json=data)
        resp = await client.post("/auth/login", json={
            "email": data["email"],
            "password": "WrongPass!",
        })
        assert resp.status_code == 401

    async def test_login_unknown_email_returns_401(self, client: AsyncClient):
        resp = await client.post("/auth/login", json={
            "email": "noexiste@test.com",
            "password": "Passw0rd!",
        })
        assert resp.status_code == 401


class TestProtectedRoutes:

    async def test_no_token_returns_401(self, client: AsyncClient):
        resp = await client.get("/characters/")
        assert resp.status_code == 401

    async def test_invalid_token_returns_401(self, client: AsyncClient):
        resp = await client.get(
            "/characters/",
            headers={"Authorization": "Bearer token.invalido.aqui"},
        )
        assert resp.status_code == 401

    async def test_valid_token_reaches_endpoint(self, client: AsyncClient, auth):
        headers, _ = auth
        resp = await client.get("/characters/", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
