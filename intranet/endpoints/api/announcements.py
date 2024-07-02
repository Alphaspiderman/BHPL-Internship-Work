import uuid
from datetime import datetime
from typing import List

import aiofiles
from sanic.request import Request
from sanic.request.form import File
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp


class Announcements(HTTPMethodView):
    async def get(self, request: Request):
        ...

    async def post(self, request: Request):
        files: List[File] = request.files.getlist("file")
        announcement_id = uuid.uuid4().hex

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

        names = []
        path = "./dynamic"
        for file in files:
            name = ".".join(file.name.split(".")[:-1])
            ext = file.name.split(".")[-1]
            new_name = uuid.uuid4().hex + "." + ext
            names.append(new_name)
            async with aiofiles.open(path + "/" + new_name, "wb") as f:
                await f.write(file.body)

        app: IntranetApp = request.app
        db_pool = app.get_db_pool

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO Announcements (Announcement_Id, Title, Body, Date_From, Date_To) VALUES (%s, %s, %s, %s)",  # noqa: E501
                    (
                        announcement_id,
                        title,
                        body,
                        date_from,
                        date_to,
                    ),
                )
                # Insert Files
                for name in names:
                    await cur.execute(
                        "INSERT INTO Announcement_Files (Announcement_Id, File_Name) VALUES (%s, %s)",
                        (announcement_id, name),
                    )
            await conn.commit()

        print(announcement_id)
        return json({"status": "success", "id": announcement_id})

    async def patch(self, request: Request):
        ...
