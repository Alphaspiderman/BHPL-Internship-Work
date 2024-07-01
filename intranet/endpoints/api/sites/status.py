from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.log import logger

from intranet.app import IntranetApp


class Site_Status(HTTPMethodView):
    async def get(self, request: Request):
        logger.info("Getting site status")
        app: IntranetApp = request.app
        stats = app.get_site_checker_info()
        last_run = stats["last_run"]
        if last_run is None:
            return json({"message": "no data available"})
        logger.info(f"Last run: {last_run}")
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
