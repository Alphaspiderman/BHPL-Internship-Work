from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render


class Login(HTTPMethodView):
    async def get(self, request: Request):
        return await render("login.html", status=400)
