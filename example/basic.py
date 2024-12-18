import asyncio
import aiohttp
from ztoe.client import Client
import logging

logger = logging.getLogger(__name__)

async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session)
        schedule = await (await client.get_schedule()).get_all()

        for item in schedule:
            #print(f"date={item['date']}")
            print(f"queue={item['queue']} sub_queue={item['sub_queue']} schedule_data={item['data']}")

logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())