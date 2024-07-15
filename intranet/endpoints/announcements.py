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
        if len(announcements) != 1:
            return redirect("/404")
        announcement_title = announcements[0][1]
        announcement_body = base64.b64decode(announcements[0][2]).decode("ascii")
        announcement_header = f"/api/files?file_id={announcements[0][5]}"

        return await render(
            "announcement_template.html",
            context={
                "header_image": announcement_header,
                "title": announcement_title,
                "content": announcement_body,
            },
        )
