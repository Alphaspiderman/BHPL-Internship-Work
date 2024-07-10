from sanic.request import Request
from sanic.response import redirect
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.app import IntranetApp


class Login(HTTPMethodView):
    async def get(self, request: Request):
        cookie = request.cookies.get("JWT_TOKEN")
        app: IntranetApp = request.app
        status = app.check_server_jwt(cookie)
        if status.authenticated:
            return redirect("/home")
        else:
            return await render("login.html", status=400)
