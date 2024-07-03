from sanic.views import HTTPMethodView
from sanic import Request, response
from intranet.app import IntranetApp
from typing import Literal, Optional


def require_type(
    require: Optional[
        Literal[
            "STORE",
            "CORP",
        ]
    ] = None,
    is_api: bool = True,
):
    def decorator(f):
        async def decorated_function(*args, **kwargs):
            # Check if the first argument is a view or a request
            if isinstance(args[0], HTTPMethodView):
                request: Request = args[1]
            else:
                request: Request = args[0]

            app: IntranetApp = request.app

            if require is not None:
                # Get the JWT data
                jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN", ""))
                if jwt_data["emp_type"] != require:
                    if is_api:
                        return response.json({"error": "Unauthorized"}, status=401)
                    else:
                        return response.redirect("/home")
            return await f(*args, **kwargs)

        return decorated_function

    return decorator
