from aiohttp import ClientSession
from typing import Any, Literal, Optional


class HolodexHttpClient:
    BASE_URL = "https://holodex.net/api/v2/"

    def __init__(self, session: Optional[ClientSession] = None) -> None:
        self.session = session

    async def close(self):
        if self.session:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
    ) -> Any:
        if not self.session:
            self.session = ClientSession()

        async with self.session.request(
            method, self.BASE_URL + endpoint, json=json
        ) as r:
            return await r.json()

    async def channels(self, channel_id: str) -> Any:
        return await self.request("GET", f"/channels/{channel_id}")
