from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.log import logger
import aiohttp
from intranet.utils import tasks

from intranet.app import IntranetApp, appserver


class Site_Checker(HTTPMethodView):
    running = False
    total_count = 0
    count_checked = 0
    count_online = 0
    count_offline = 0

    def __init__(self):
        super().__init__()
        self.check_site_connection.start(appserver)

    async def get(self, request: Request):
        if self.running:
            return json(
                {
                    "message": "Site check is currently running",
                    "total_count": self.total_count,
                    "checked": self.count_checked,
                    "online": self.count_online,
                    "offline": self.count_offline,
                }
            )

    async def post(self, request: Request):
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

        self.total_count = len(sites)
        self.count_checked = 0
        self.count_online = 0
        self.count_offline = 0

        online_sites = []
        offline_sites = []

        # Check if the site is up
        for site in sites:
            name, ip = site
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(ip) as resp:
                        if resp.status == 200:
                            online_sites.append(name)
                            self.count_online += 1
                        else:
                            offline_sites.append(name)
                            self.count_offline += 1
                except Exception:
                    offline_sites.append(name)
                    self.count_offline += 1
                finally:
                    self.checked += 1

        # Update on app
        app.set_site_status(online_sites=online_sites, offline_sites=offline_sites)
