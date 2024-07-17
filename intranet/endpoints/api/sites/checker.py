from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.decorators.require_login import require_login


class Site_Checker(HTTPMethodView):
    def __init__(self):
        super().__init__()

    @require_login(is_api=True)
    async def get(self, request: Request):
        await request.app.dispatch("intranet.network_checker.trigger")
        return json({"message": "Site check triggered"})
