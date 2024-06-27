from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render


class Home(HTTPMethodView):
    async def get(self, request: Request):
        return await render("home.html", status=400)
