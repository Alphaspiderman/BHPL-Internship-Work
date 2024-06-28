from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp


class Site_Status(HTTPMethodView):
    async def get(self, request: Request):
        app: IntranetApp = request.app
        last_run = app.get_site_check_time()
        if last_run is None:
            return json({"message": "Site check has not been run yet"})
        online, offline = app.get_site_status()
        return json(
            {
                "online_count": len(online),
                "offline_count": len(offline),
                offline: offline,
                last_run: last_run,
            }
        )
