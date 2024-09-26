from sanic import redirect
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Create_Announcement(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        app: IntranetApp = request.app
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN", ""))
        if jwt_data["department"] not in ["IT", "HR"]:
            return redirect("/home")
        return await render("announcements/create.html")
