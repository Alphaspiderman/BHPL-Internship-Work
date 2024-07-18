from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.decorators.require_login import require_login


class Edit_Location(HTTPMethodView):
    @require_login()
    # TODO - Add Role Check
    async def get(self, request: Request, uuid: str):
        return await render("edit_site.html")
