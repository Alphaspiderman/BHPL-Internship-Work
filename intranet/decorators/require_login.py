from sanic import Request, response
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.models.JWTStatus import JWTStatus


def require_login(is_api: bool = False):
    def decorator(f):
        async def decorated_function(*args, **kwargs):
            # Check if the first argument is a view or a request
            if isinstance(args[0], HTTPMethodView):
                request: Request = args[1]
            else:
                request: Request = args[0]

            app: IntranetApp = request.app

            # Check if the request is authorized
            is_jwt_valid: JWTStatus = app.check_server_jwt(
                request.cookies.get("JWT_TOKEN", "")
            )

            if is_jwt_valid.authenticated:
                # Call the function if the request is authorized
                return await f(*args, **kwargs)
            else:
                if is_api:
                    return response.json({"error": "Unauthorized access"}, status=401)
                else:
                    return response.redirect("/login")

        return decorated_function

    return decorator
