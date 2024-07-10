import asyncio

import aioping
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp


class Site_Checker(HTTPMethodView):
    def __init__(self):
        super().__init__()

    async def get(self, request: Request):
        response = await request.respond(json({"message": "Site check triggered"}))
        app: IntranetApp = request.app
        await response.send()

        # Get IPs from DB
        db_pool = app.get_db_pool()

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT Store_Name, Static_Ip FROM sites WHERE Status = 'Operational'"
                )
                sites = await cur.fetchall()

        app.reset_site_checker()

        total_count = len(sites)
        app.set_site_checked_total(total_count)

        # Check if the site is up
        tasks = []
        for site in sites:
            name, ip = site
            tasks.append(self.check_site(app, ip, name))
        await asyncio.gather(*tasks)

    async def check_site(self, app: IntranetApp, ip: str, name: str):
        try:
            await aioping.ping(ip, 2)
            app.add_site_checker(name, True)
        except Exception:
            app.add_site_checker(name, False)
