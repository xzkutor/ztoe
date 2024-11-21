from aiohttp import ClientSession
import ztoe.schedule as schedule


class Client:
    DATA_URL = "https://www.ztoe.com.ua/unhooking-search.php"
    REQUEST_TIMEOUT = 30

    def __init__(self, session: ClientSession, url: str = ""):
        self.DATA_URL = url or self.DATA_URL
        self.session = session

    async def __request(self, method: str) -> str:
        headers = {"accept": "text/html"}

        async with self.session.request(method, self.DATA_URL, headers=headers, timeout=self.REQUEST_TIMEOUT) as r:
            r.raise_for_status()
            return await r.text()

    async def get_schedule(self) -> schedule.Schedule:
        return schedule.Schedule(await self.__request("GET"))
