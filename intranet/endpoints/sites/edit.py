from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.decorators.require_login import require_login


class Edit_Site(HTTPMethodView):
    @require_login()
    # TODO - Add Role Check
    async def get(self, request: Request, uuid: str):
        return await render("sites/edit.html")
