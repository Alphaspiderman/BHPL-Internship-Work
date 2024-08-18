import asyncio
from datetime import datetime, timezone

import aiomysql
import aioping
from dotenv import dotenv_values
from sanic import Sanic, json
from sanic.log import logger

from intranet.utils import tasks


class CheckerApp(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx.site_checker = {
            "total": 0,
            "checked": 0,
            "online": list(),
            "offline": list(),
            "last_run": None,
        }
        self.ctx.site_checker_running = False

    def get_site_check_time(self) -> datetime:
        return self.ctx.site_check_last_run

    async def connect_db(self):
        pool = await aiomysql.create_pool(
            host=self.config["DB_HOST"],
            port=self.config["DB_PORT"],
            user=self.config["DB_USERNAME"],
            password=self.config["DB_PASSWORD"],
            db=self.config["DB_NAME"],
            autocommit=True,
        )
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 42;")
                (r,) = await cur.fetchone()
        try:
            assert r == 42
        except AssertionError:
            raise Exception("Database connection failed")
        self.ctx.db_pool = pool

    def get_db_pool(self):
        return self.ctx.db_pool

    def reset_site_checker(self):
        self.ctx.site_checker = {
            "total": 0,
            "checked": 0,
            "online": list(),
            "offline": list(),
            "last_run": None,
        }

    def set_site_checked_total(self, total: int):
        self.ctx.site_checker["last_run"] = datetime.now(timezone.utc)
        self.ctx.site_checker["total"] = total

    async def add_site_checker(self, site: str, is_online: bool, store_code: str):
        logger.info(
            f"Site {site} ({store_code}) is {'online' if is_online else 'offline'}"
        )
        self.ctx.site_checker["checked"] += 1
        async with self.get_db_pool().acquire() as conn:
            async with conn.cursor() as cur:
                if is_online:
                    self.ctx.site_checker["online"].append(site)
                    await cur.execute(
                        "UPDATE network_uptime SET End_Time = NOW() WHERE Store_Code = %s AND End_Time IS NULL",  # noqa: E501
                        (store_code,),
                    )
                else:
                    self.ctx.site_checker["offline"].append(site)
                    # Make sure the site is not already in the DB
                    await cur.execute(
                        "SELECT * FROM network_uptime WHERE Store_Code = %s AND End_Time IS NULL",  # noqa: E501
                        (store_code,),
                    )
                    if not await cur.fetchone():
                        await cur.execute(
                            "INSERT INTO network_uptime (Store_Code, Start_Time) VALUES (%s, NOW())",  # noqa: E501
                            (store_code,),
                        )

    def get_site_checker_info(self):
        return self.ctx.site_checker

    def set_checker_running(self, is_running: bool):
        self.ctx.site_checker_running = is_running

    def is_checker_running(self) -> bool:
        return self.ctx.site_checker_running


app = CheckerApp("Site_Checker")


@app.listener("before_server_start")
async def setup_db(app: CheckerApp):
    await app.connect_db()
    site_checker.start()


@app.get("/")
async def index(request):
    data = app.get_site_checker_info().copy()
    # Convert the datetime to a string
    data["last_run"] = data["last_run"].isoformat()
    return json(data)


@tasks.loop(seconds=300)
async def site_checker():
    await app.dispatch("intranet.network_checker.trigger")


@app.signal("intranet.network_checker.trigger")
async def network_checker():
    logger.info("Checking sites")
    # Get IPs from DB
    db_pool = app.get_db_pool()

    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT Store_Name, Static_Ip, Store_Code FROM sites WHERE Status = 'Operational' AND Static_Ip IS NOT NULL"  # noqa: E501
            )
            sites = await cur.fetchall()

    app.reset_site_checker()

    total_count = len(sites)
    app.set_site_checked_total(total_count)

    # Check if the site is up
    tasks = []
    for site in sites:
        name, ip, store_code = site
        tasks.append(check_site(app, ip, name, store_code))
    await asyncio.gather(*tasks)
    logger.info("Site Check Finished")


async def check_site(app: CheckerApp, ip: str, name: str, store_code: str):
    try:
        await aioping.ping(ip, 4)
        await app.add_site_checker(name, True, store_code)
    except Exception:
        await app.add_site_checker(name, False, store_code)


kwargs = {"host": "127.0.0.1", "port": 1234}

# Load ENV
config = dotenv_values(".env")

# Load default values for the database connection
config.update(
    {
        "DB_HOST": config.get("DB_HOST", "localhost"),
        "DB_PORT": int(config.get("DB_PORT", 3306)),
        "DB_USERNAME": config.get("DB_USERNAME", "root"),
        "DB_PASSWORD": config.get("DB_PASSWORD", "password"),
        "DB_NAME": config.get("DB_NAME", "intranet"),
    },
)
app.config.update(config)


if __name__ == "__main__":
    # Run the API Server
    app.run(**kwargs)
