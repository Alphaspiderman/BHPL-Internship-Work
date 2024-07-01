from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from datetime import datetime

from intranet.app import IntranetApp


class Announcements(HTTPMethodView):
    async def get(self, request: Request):
        ...

    async def post(self, request: Request):
        try:
            body = request.form["body"][0]
            date_from = datetime.strptime(
                request.form["date_from"][0], "%Y-%m-%d"
            ).strftime("%Y-%m-%d")
            date_to = datetime.strptime(
                request.form["date_to"][0], "%Y-%m-%d"
            ).strftime("%Y-%m-%d")
            title = request.form["title"][0]
        except KeyError:
            return json({"status": "failure"}, status=400)

        app: IntranetApp = request.app
        db_pool = app.get_db_pool

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO announcements (title, body, date_from, date_to) VALUES (%s, %s, %s, %s)",
                    (
                        title,
                        body,
                        date_from,
                        date_to,
                    ),
                )
                lrid = cur.lastrowid
            await conn.commit()

        print(lrid)
        return json({"status": "success", "id": lrid})

    async def patch(self, request: Request):
        ...
