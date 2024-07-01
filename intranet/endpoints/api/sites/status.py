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
        stats = app.get_site_checker_info()
        return json(
            {
                "total_count": stats["total"],
                "checked": stats["checked"],
                "online": stats["online"],
                "offline": stats["offline"],
                "last_run": str(last_run),
            }
        )
