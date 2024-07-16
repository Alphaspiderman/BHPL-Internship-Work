from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.decorators.require_login import require_login


class Expense_Report(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        return await render("expense_report.html")