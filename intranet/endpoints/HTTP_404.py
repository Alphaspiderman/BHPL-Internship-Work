from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render


class HTTP_404(HTTPMethodView):
    async def get(self, request: Request):
        return await render("404.html")
