from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render


class Index(HTTPMethodView):
    async def get(self, request: Request):
        return await render("index.html", status=400)
