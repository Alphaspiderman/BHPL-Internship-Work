from datetime import datetime, timedelta, timezone
from sanic.request import Request
from sanic.response import redirect
from sanic.views import HTTPMethodView


class Logout(HTTPMethodView):
    async def get(self, request: Request):
        rsp = redirect("/login")
        # Force a deletion even if either server or client time has drifted
        expire_time = datetime.now(tz=timezone.utc) - timedelta(minutes=30)
        rsp.add_cookie("JWT_TOKEN", "", expires=expire_time, secure=False)
        rsp.add_cookie("JWT_TOKEN", "", expires=expire_time, secure=True)
        return rsp
