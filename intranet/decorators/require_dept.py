from typing import List, Literal, Optional

from sanic import Request, response
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp


def require_dept(
    require: Optional[
        List[
            Literal[
                "IT",
                "OPERATIONS",
                "HR",
                "MARKETING",
            ]
        ]
    ] = None,
    is_api: bool = True,
):
    if require is None:
        require = []

    def decorator(f):
        async def decorated_function(*args, **kwargs):
            # Check if the first argument is a view or a request
            if isinstance(args[0], HTTPMethodView):
                request: Request = args[1]
            else:
                request: Request = args[0]

            app: IntranetApp = request.app

            if len(require) > 0:
                # Get the JWT data
                jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN", ""))
                if jwt_data["dept"] not in require:
                    if is_api:
                        return response.json({"error": "Unauthorized"}, status=401)
                    else:
                        return response.redirect("/home")
            return await f(*args, **kwargs)

        return decorated_function

    return decorator
