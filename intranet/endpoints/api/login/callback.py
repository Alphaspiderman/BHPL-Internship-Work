import jwt
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.log import logger
from sanic.response import redirect

from intranet.app import IntranetApp


class Callback(HTTPMethodView):
    async def post(self, request: Request):
        # Get the token from the request.
        form = request.form
        token = form["id_token"][0]
        app: IntranetApp = request.app

        # Get the ID of the key used to sign the token.
        kid = jwt.get_unverified_header(token)["kid"]

        # Get the public key to verify the token.
        key = app.entra_jwt_keys.get(kid, "")

        try:
            # Decode the token.
            decoded = jwt.decode(
                token,
                key=key,
                algorithms=["RS256"],
                audience=request.app.config["AZURE_AD_CLIENT_ID"],
            )
        except jwt.exceptions.InvalidAudienceError:
            logger.warning("Invalid audience for JWT")
            # Invalid token
            return redirect("login?error=invalid_token")
        except jwt.exceptions.InvalidIssuedAtError:
            logger.warning("JWT issued in future")
            # Invalid token
            return redirect("login?error=invalid_token")
        except jwt.exceptions.ImmatureSignatureError:
            logger.warning("JWT issued in future")
            # Invalid token
            return redirect("login?error=invalid_token")
        except jwt.exceptions.ExpiredSignatureError:
            logger.warning("JWT has expired")
            # Invalid token
            return redirect("login?error=invalid_token")
        except jwt.exceptions.DecodeError:
            logger.warning("JWT decode error")
            # Invalid token
            return redirect("login?error=invalid_token")

        # Get email from decoded token
        email = decoded["email"]

        # Get domain from email
        domain = email.split("@")[1]

        # Check Domain
        if domain != "burmanhospitality.com":
            return redirect("login?error=invalid_domain")

        # Get the user from the database
        async with app.get_db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = await cur.fetchall()

        # Check if user exists
        if user is None or len(user) == 0:
            return redirect("login?error=user_not_found")
        if len(user) > 1:
            return redirect("login?error=too_many_users")

        # TODO - Extract data for adding to JWT

        # TODO - Generate Token
        token = app.generate_jwt(
            {
                "email": email,
                "name": decoded["name"],
            },
            60,
        )

        # Redirect to home with JWT set in cookie
        rsp = redirect("home")
        rsp.add_cookie("JWT_TOKEN", token)

        # Redirect to home
        return rsp
