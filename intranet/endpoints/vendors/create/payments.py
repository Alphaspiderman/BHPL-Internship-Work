from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.decorators.require_login import require_login


class Payments_Create(HTTPMethodView):
    @require_login()
    # TODO - Add Role Check
    async def get(self, request: Request):
        return await render("./vendors/create_payments.html")
