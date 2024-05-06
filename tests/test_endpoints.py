import hashlib

import pytest
from aiohttp import web

from api.router import setup_routes


def setup_app_for_tests():
    app = web.Application()
    setup_routes(app)
    return app


HEALTHCHECK_ROUTE = "/healthcheck"


@pytest.mark.asyncio
async def test_healthcheck_regular(aiohttp_client):
    client = await aiohttp_client(setup_app_for_tests())
    response = await client.get(HEALTHCHECK_ROUTE)
    assert response.status == 200
    json = await response.json()
    assert json == {}


@pytest.mark.asyncio
async def test_healthcheck_wrong_methods(aiohttp_client):
    client = await aiohttp_client(setup_app_for_tests())
    responses = []
    for method in ("post", "put", "patch"):
        responses.append(await getattr(client, method)(HEALTHCHECK_ROUTE))

    for response in responses:
        assert response.status == 405


HASH_ROUTE = "/hash"
HASH_TEST_TEST_STRING = "test_string"
HASH_TEST_HASH_FIELD = "hash_string"


@pytest.mark.asyncio
async def test_hash_regular(aiohttp_client):
    client = await aiohttp_client(setup_app_for_tests())
    response = await client.post(
        HASH_ROUTE, json={"string": HASH_TEST_TEST_STRING}
    )
    assert response.status == 200
    json = await response.json()
    test_string_hash = hashlib.sha256(
        HASH_TEST_TEST_STRING.encode("utf-8")
    ).hexdigest()
    assert HASH_TEST_HASH_FIELD in json
    assert json[HASH_TEST_HASH_FIELD] == test_string_hash


@pytest.mark.asyncio
async def test_hash_wrong_methods(aiohttp_client):
    client = await aiohttp_client(setup_app_for_tests())
    responses = []
    for method in ("get", "put", "patch"):
        responses.append(
            await getattr(client, method)(HASH_ROUTE, json={"string": None})
        )

    for response in responses:
        assert response.status == 405


@pytest.mark.asyncio
async def test_hash_no_string_field(aiohttp_client):
    client = await aiohttp_client(setup_app_for_tests())
    response = await client.post(HASH_ROUTE, json={})
    assert response.status == 400


@pytest.mark.asyncio
async def test_hash_emtpy_field(aiohttp_client):
    client = await aiohttp_client(setup_app_for_tests())
    response = await client.post(HASH_ROUTE, json={"string": None})
    assert response.status == 400
