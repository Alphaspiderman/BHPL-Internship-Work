import aiohttp
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.decorators.require_login import require_login


class Site_Status(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        # Get the site checker info from localhost:1234
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:1234") as resp:
                stats = await resp.json()
        last_run = stats["last_run"]
        if last_run is None:
            return json({"message": "no data available"})
        return json(stats)
