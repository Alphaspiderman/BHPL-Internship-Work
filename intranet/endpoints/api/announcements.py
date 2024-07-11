import base64
import uuid
from datetime import datetime
from typing import List

import aiofiles
from sanic.request import Request
from sanic.request.form import File
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp


class Announcements_API(HTTPMethodView):
    async def get(self, request: Request, id: str = None):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        if id is None or len(id) == 0:
            # Return list of announcements that can be viewed now
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT Announcement_Id, Title, Header_Image FROM announcements WHERE Date_From <= NOW() AND Date_To >= NOW()"  # noqa: E501
                    )
                    announcements = await cur.fetchall()
            return json({"announcements": announcements})
        else:
            # Return announcement with the given id
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT Title, Body, Header_Image FROM announcements WHERE Announcement_Id = %s AND Date_From <= NOW() AND Date_To >= NOW()",  # noqa: E501
                        (id,),
                    )
                    announcement = await cur.fetchone()
            # If the announcement is not found, return a 404
            if announcement is None:
                return json({"status": "failure"}, status=404)
            # If the announcement is found, return the announcement
            body = base64.b64decode(announcement[1]).decode("ascii")
            announcement = {
                "title": announcement[0],
                "body": body,
                "header_image": announcement[2],
            }
            return json({"status": "success", "announcement": announcement})

    async def post(self, request: Request, id: str = None):
        has_header_img = False
        files: List[File] = request.files.getlist("file")
        announcement_id = uuid.uuid4().hex

        try:
            body = base64.b64encode(request.form["body"][0].encode("ascii"))
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
        for idx, file in enumerate(files):
            if idx == 0:
                # Check if the file is an image
                if file.type.startswith("image"):
                    has_header_img = True
            name = ".".join(file.name.split(".")[:-1])
            ext = file.name.split(".")[-1]
            new_name = uuid.uuid4().hex + "." + ext
            names.append(new_name)
            async with aiofiles.open(path + "/" + new_name, "wb") as f:
                await f.write(file.body)

        app: IntranetApp = request.app
        db_pool = app.get_db_pool()

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO announcements (Announcement_Id, Title, Body, Date_From, Date_To) VALUES (%s, %s, %s, %s, %s)",  # noqa: E501
                    (
                        announcement_id,
                        title,
                        body,
                        date_from,
                        date_to,
                    ),
                )
                # Insert Files
                for idx, name in enumerate(names):
                    if idx == 0 and has_header_img:
                        await cur.execute(
                            "UPDATE announcements SET Header_Image = %s WHERE Announcement_Id = %s",  # noqa: E501
                            (name, announcement_id),
                        )
                    await cur.execute(
                        "INSERT INTO announcement_files (Announcement_Id, File_Name) VALUES (%s, %s)",
                        (announcement_id, name),
                    )
            await conn.commit()

        return json({"status": "success", "id": announcement_id})

    async def patch(self, request: Request):
        ...
