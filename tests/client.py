import aiohttp
import pytest
from aiohttp import ClientSession
from ztoe.client import Client
from ztoe.schedule import Schedule

@pytest.fixture
async def client():
    async with ClientSession() as session:
        yield Client(session)

@pytest.mark.asyncio
async def client_initialization(client):
    assert client.DATA_URL == "https://www.ztoe.com.ua/unhooking-search.php"
    assert client.REQUEST_TIMEOUT == 30

@pytest.mark.asyncio
async def request_get_method(client, aiohttp_mock):
    aiohttp_mock.get(client.DATA_URL, status=200, body="response")
    response = await client._Client__request("GET")
    assert response == "response"

@pytest.mark.asyncio
async def request_raises_for_status(client, aiohttp_mock):
    aiohttp_mock.get(client.DATA_URL, status=404)
    with pytest.raises(aiohttp.ClientResponseError):
        await client._Client__request("GET")

@pytest.mark.asyncio
async def get_schedule_returns_schedule_instance(client, aiohttp_mock):
    aiohttp_mock.get(client.DATA_URL, status=200, body="<html></html>")
    schedule = await client.get_schedule()
    assert isinstance(schedule, Schedule)