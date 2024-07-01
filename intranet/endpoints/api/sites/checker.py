import asyncio
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.log import logger
import aioping
from intranet.utils import tasks

from intranet.app import IntranetApp


class Site_Checker(HTTPMethodView):
    def __init__(self):
        super().__init__()
        # asyncio.ensure_future(self.check_site_connection(appserver))

    async def get(self, request: Request):
        app: IntranetApp = request.app
        stats = app.get_site_checker_info()
        if stats["is_processing"]:
            return json(
                {
                    "message": "Site check is currently processing",
                    "total_count": stats["total"],
                    "checked": stats["checked"],
                    "online": stats["online"],
                    "offline": stats["offline"],
                }
            )
        else:
            return json(
                {
                    "message": "Site check is not currently processing",
                    "total_count": stats["total"],
                    "checked": stats["checked"],
                    "online": stats["online"],
                    "offline": stats["offline"],
                }
            )

    async def post(self, request: Request):
        response = await request.respond(json({"message": "Site check triggered"}))
        await response.send()
        await self.check_sites(request.app)

    @tasks.loop(minutes=5)
    async def check_site_connection(self, app: IntranetApp):
        await self.check_sites(app)

    async def check_sites(self, app: IntranetApp):
        logger.info("Checking site connection")

        # Get IPs from DB
        db_pool = app.get_db_pool

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT name, ip FROM sites")
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
            logger.info(f"Online - {name}")
        except Exception:
            app.add_site_checker(name, False)
            logger.info(f"Offline - {name}")
