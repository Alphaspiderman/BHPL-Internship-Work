import jwt
from jwt import algorithms

from dotenv import dotenv_values
from sanic import Request, Sanic, response
from sanic.log import logger
import aiohttp
import json

from .app import appserver

# noinspection PyUnresolvedReferences
# flake8: noqa
import intranet.endpoints


logger.debug("Loading ENV")
config = dotenv_values(".env")

# Read the public and private keys and add them to the config.
with open("public-key.pem") as public_key_file:
    config["PUB_KEY"] = public_key_file.read()

with open("private-key.pem") as private_key_file:
    config["PRIV_KEY"] = private_key_file.read()

# Try to get state from the ENV, defaults to being dev.
is_prod: str = config.get("IS_PROD", "false")

# Convert the string to a bool and update the config with the bool.
config.update({"IS_PROD": is_prod.lower() == "true"})

app: Sanic = appserver
app.config.update(config)
app.config.PROXIES_COUNT = int(config.get("PROXIES_COUNT", 0))


@app.listener("before_server_start")
async def setup_app(app: Sanic):

    logger.info("Fetching OpenID Configuration of Entra")

    # Fetch OpenID Configuration of Entra from https://login.microsoftonline.com/common/.well-known/openid-configuration
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://login.microsoftonline.com/common/.well-known/openid-configuration"
        ) as resp:
            config = await resp.json()
            jwks_uri = config["jwks_uri"]

    logger.info(
        "Fetching JSON Web Key Set (JWKS) from the OpenID Configuration of Entra"
    )

    # Fetch the JSON Web Key Set (JWKS) from the OpenID Configuration of Entra
    async with aiohttp.ClientSession() as session:
        async with session.get(jwks_uri) as resp:
            jwks = await resp.json()

    logger.info("Saving public keys from the JWKS")

    # Create a dictionary of public keys from the JWKS
    public_keys = {}
    for jwk in jwks["keys"]:
        kid = jwk["kid"]
        public_keys[kid] = algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    logger.info("Saving public keys to the app context")
    app.ctx.public_keys = public_keys


@app.get("/ping")
async def ping_test(request: Request):
    return response.text("Pong")


@app.get("/jwt")
async def jwt_status(request: Request):
    if not request.token:
        d = {"authenticated": False, "message": "No token"}
        return response.json(d)

    try:
        jwt.decode(request.token, key=request.app.config["PUB_KEY"], algorithms="RS256")
    except jwt.exceptions.ImmatureSignatureError:
        # Raised when a token’s nbf claim represents a time in the future
        d = {
            "authenticated": False,
            "message": "JWT Token not allowed to be used at time",
        }
        status = 401
    except jwt.exceptions.InvalidIssuedAtError:
        # Raised when a token’s iat claim is in the future
        d = {"authenticated": False, "message": "JWT issues in future"}
        status = 401
    except jwt.exceptions.ExpiredSignatureError:
        # Raised when a token’s exp claim indicates that it has expired
        d = {"authenticated": False, "message": "JWT has expired"}
        status = 401
    except jwt.exceptions.InvalidTokenError:
        # Generic invalid token
        d = {"authenticated": False, "message": "JWT invalid"}
        status = 401
    else:
        # Valid Token
        d = {"authenticated": True, "message": "JWT is valid"}
        status = 200

    return response.json(d, status=status)


if __name__ == "__main__":
    # Check for Production environment
    is_prod = app.config["IS_PROD"]

    # Use a KWARGS dict to pass to app.run dynamically
    kwargs = {"access_log": True, "host": "0.0.0.0"}

    if is_prod:
        # If prod, check for HOST (internally required for JWTs).
        if app.config.get("HOST") is None:
            logger.error("MISSING HOST")
            quit(1)

    else:
        # If DEV, set HOST to DEV.
        app.config["HOST"] = "DEV"
        kwargs["debug"] = True
        kwargs["auto_reload"] = True

    # Run the API Server
    app.run(**kwargs)
