from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Site_Status(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        stats = app.get_site_checker_info()
        last_run = stats["last_run"]
        if last_run is None:
            return json({"message": "no data available"})
        return json(
            {
                "message": "success",
                "total_count": stats["total"],
                "checked": stats["checked"],
                "online": stats["online"],
                "offline": stats["offline"],
                "last_run": str(last_run),
            }
        )
