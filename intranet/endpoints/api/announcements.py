import base64
import uuid
from datetime import datetime
from typing import List

from sanic.request import Request
from sanic.request.form import File
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Announcements_API(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request, id: str = None):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        # Return list of announcements that can be viewed now
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT Announcement_Id, Title FROM announcements WHERE Date = CURDATE()"  # noqa: E501
                )
                announcements = await cur.fetchall()
        return json({"announcements": announcements})

    @require_login(is_api=True)
    async def post(self, request: Request, id: str = None):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        files: List[File] = request.files.getlist("file")
        announcement_id = uuid.uuid4().hex

        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))
        emp_id = jwt_data["emp_id"]
        emp_name = jwt_data["name"]

        try:
            body = base64.b64encode(request.form["body"][0].encode("ascii"))
            date = datetime.strptime(request.form["date"][0], "%Y-%m-%d").strftime(
                "%Y-%m-%d"
            )
            title = request.form["title"][0]
            as_admin = request.form.get("as_admin", "").lower() == "true"
            if as_admin:
                posted_by = "Admin"
            else:
                posted_by = request.form.get("posted_by", emp_name)
        except KeyError:
            return json({"status": "failure", "message": "Missing Required Fields"})
        except ValueError:
            return json({"status": "failure", "message": "Date not Provided"})

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Insert announcement into the database
                await cur.execute(
                    "INSERT INTO announcements (Announcement_Id, Title, Body, Date, Posted_By, Log_Posted_By) VALUES (%s, %s, %s, %s, %s, %s)",  # noqa: E501
                    (
                        announcement_id,
                        title,
                        body,
                        date,
                        posted_by,
                        emp_name,
                    ),
                )
                # Insert files into the database
                if files is None:
                    pass
                elif len(files) > 0:
                    file = files[0]
                    ext = file.name.split(".")[-1]
                    new_name = uuid.uuid4().hex + "." + ext
                    await cur.execute(
                        "INSERT INTO files(File_Id, File_Name, File_Type, File_Data, Uploaded_By) VALUES (%s, %s, %s, %s, %s)",  # noqa: E501
                        (
                            new_name,
                            file.name,
                            file.type,
                            file.body,
                            emp_id,
                        ),
                    )
                    # Insert announcement into the database
                    await cur.execute(
                        "INSERT INTO announcement_files (Announcement_Id, File_Id) VALUES (%s, %s)",  # noqa: E501
                        (announcement_id, new_name),
                    )
                # Save the data
                await conn.commit()

        return json({"status": "success", "id": announcement_id})

    @require_login(is_api=True)
    async def patch(self, request: Request):
        return json({"status": "failure", "message": "Not implemented"})
