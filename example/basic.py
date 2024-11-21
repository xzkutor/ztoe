import asyncio
import aiohttp
from ztoe.client import Client
import logging

logger = logging.getLogger(__name__)

async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session)
        schedule = await (await client.get_schedule()).get_queue(1)

        for item in schedule:
            print(f"sector={item['sector']} queue={item['queue']} schedule_data={item['data']}")

logging.basicConfig(level=logging.INFO)
asyncio.run(main())