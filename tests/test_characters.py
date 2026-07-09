"""Tests del CRUD de personajes."""

import uuid
import pytest
from httpx import AsyncClient

from tests.conftest import CHARACTER_PAYLOAD


class TestCreateCharacter:

    async def test_create_valid(self, client: AsyncClient, auth):
        headers, _ = auth
        resp = await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == CHARACTER_PAYLOAD["name"]
        assert data["world"] == "fantasia"
        assert "id" in data

    async def test_create_missing_name(self, client: AsyncClient, auth):
        headers, _ = auth
        payload = CHARACTER_PAYLOAD.copy()
        del payload["name"]
        resp = await client.post("/characters/", json=payload, headers=headers)
        assert resp.status_code == 422

    async def test_create_requires_auth(self, client: AsyncClient):
        resp = await client.post("/characters/", json=CHARACTER_PAYLOAD)
        assert resp.status_code == 401


class TestListCharacters:

    async def test_list_empty(self, client: AsyncClient, auth):
        headers, _ = auth
        resp = await client.get("/characters/", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_after_create(self, client: AsyncClient, auth):
        headers, _ = auth
        await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)
        resp = await client.get("/characters/", headers=headers)
        assert len(resp.json()) >= 1

    async def test_list_isolation(self, client: AsyncClient, auth):
        headers_a, _ = auth
        await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)

        uid = uuid.uuid4().hex[:8]
        resp_b = await client.post("/auth/register", json={
            "email": f"iso_{uid}@test.com", "username": f"iso_{uid}", "password": "Passw0rd!",
        })
        headers_b = {"Authorization": f"Bearer {resp_b.json()['access_token']}"}

        resp = await client.get("/characters/", headers=headers_b)
        assert resp.json() == []


class TestUpdateCharacter:

    async def test_update_name(self, client: AsyncClient, auth):
        headers, _ = auth
        created = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)).json()
        resp = await client.put(f"/characters/{created['id']}", json={"name": "NuevoNombre"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "NuevoNombre"

    async def test_update_other_user_returns_404(self, client: AsyncClient, auth):
        headers_a, _ = auth
        created = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)).json()

        uid = uuid.uuid4().hex[:8]
        resp_b = await client.post("/auth/register", json={
            "email": f"up_{uid}@test.com", "username": f"up_{uid}", "password": "Passw0rd!",
        })
        headers_b = {"Authorization": f"Bearer {resp_b.json()['access_token']}"}

        resp = await client.put(f"/characters/{created['id']}", json={"name": "Hacker"}, headers=headers_b)
        assert resp.status_code == 404


class TestDeleteCharacter:

    async def test_delete_own(self, client: AsyncClient, auth):
        headers, _ = auth
        created = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers)).json()
        resp = await client.delete(f"/characters/{created['id']}", headers=headers)
        assert resp.status_code == 204

        resp = await client.get("/characters/", headers=headers)
        ids = [c["id"] for c in resp.json()]
        assert created["id"] not in ids

    async def test_delete_other_user_returns_404(self, client: AsyncClient, auth):
        headers_a, _ = auth
        created = (await client.post("/characters/", json=CHARACTER_PAYLOAD, headers=headers_a)).json()

        uid = uuid.uuid4().hex[:8]
        resp_b = await client.post("/auth/register", json={
            "email": f"del_{uid}@test.com", "username": f"del_{uid}", "password": "Passw0rd!",
        })
        headers_b = {"Authorization": f"Bearer {resp_b.json()['access_token']}"}

        resp = await client.delete(f"/characters/{created['id']}", headers=headers_b)
        assert resp.status_code == 404
