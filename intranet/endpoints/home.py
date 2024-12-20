from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.decorators.require_login import require_login


class Home(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        return await render("home.html")
