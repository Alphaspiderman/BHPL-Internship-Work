from sanic.request import Request
from sanic.response import redirect
from sanic.views import HTTPMethodView


class Logout(HTTPMethodView):
    async def get(self, request: Request):
        rsp = redirect("/login")
        rsp.delete_cookie("JWT_TOKEN")
        return rsp
