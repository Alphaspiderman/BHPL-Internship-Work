import base64

from sanic.request import Request
from sanic.response import redirect
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Announcements(HTTPMethodView):
    @require_login()
    async def get(self, request: Request, uuid: str = None):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM announcements WHERE Announcement_Id = %s", (uuid,)
                )
                announcements = await cur.fetchall()
                # Get related files
                if len(announcements) != 1:
                    return redirect("/404")
                await cur.execute(
                    "SELECT * FROM files where File_Id IN (SELECT File_Id from announcement_files WHERE Announcement_Id = %s)",  # noqa: E501
                    (uuid,),
                )
                announcement_files = await cur.fetchall()

        title = announcements[0][1]
        body = base64.b64decode(announcements[0][2]).decode("ascii")
        date_posted = announcements[0][3]
        posted_by = announcements[0][5]
        images = []
        attachments = []
        for entry in announcement_files:
            if entry[3].startswith("image"):
                images.append(f"/api/files?file_id={entry[0]}")
            else:
                attachments.append([entry[2], f"/api/files?file_id={entry[0]}"])

        print(images)
        print(attachments)

        return await render(
            "announcements/template.html",
            context={
                "title": title,
                "body": body,
                "date_posted": date_posted,
                "posted_by": posted_by,
                "images": images,
                "attachments": attachments,
            },
        )
