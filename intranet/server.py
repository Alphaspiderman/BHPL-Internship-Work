import json

import aiohttp
from dotenv import dotenv_values
from jwt import algorithms
from sanic import NotFound, Request, response
from sanic.log import logger
from sanic_ext import render

from .app import IntranetApp, appserver

# noinspection PyUnresolvedReferences
import intranet.endpoints  # noqa: F401

logger.debug("Loading ENV")
config = dotenv_values(".env")

# Read the public and private keys and add them to the config.
with open("public-key.pem") as public_key_file:
    config["PUB_KEY"] = public_key_file.read()

with open("private-key.pem") as private_key_file:
    config["PRIV_KEY"] = private_key_file.read()

# Try to get state from the ENV, defaults to being dev.
is_prod: str = config.get("IS_PROD", "false")

# Load default values for the database connection
config.update(
    {
        "DB_HOST": config.get("DB_HOST", "localhost"),
        "DB_PORT": int(config.get("DB_PORT", 3306)),
        "DB_USERNAME": config.get("DB_USERNAME", "root"),
        "DB_PASSWORD": config.get("DB_PASSWORD", "password"),
        "DB_NAME": config.get("DB_NAME", "intranet"),
    },
)

# Check if AZURE_AD env variables are set
if (
    config.get("AZURE_AD_TENANT_ID") is None
    or config.get("AZURE_AD_CLIENT_ID") is None
    or config.get("AZURE_AD_REDIRECT_URI") is None
):
    logger.error("MISSING AZURE AD ENV VARIABLES")
    quit(1)

# Convert the string to a bool and update the config with the bool.
config.update({"IS_PROD": is_prod.lower() == "true"})

# Disable OpenAPI docs
config["OAS"] = False
config["OAS_UI_DEFAULT"] = None
config["OAS_UI_REDOC"] = False
config["OAS_UI_SWAGGER"] = False


app: IntranetApp = appserver
app.config.update(config)
app.config.PROXIES_COUNT = int(config.get("PROXIES_COUNT", 0))

# Static files
app.static("/static/", "./static/", name="static")


@app.listener("before_server_start")
async def setup_app(app: IntranetApp):
    try:
        await app.connect_db()
    except Exception as e:
        logger.error(e)
        logger.error("Error connecting to DB")
        app.stop()

    logger.info("Fetching OpenID Configuration of Entra")

    # Fetch OpenID Configuration of Entra
    # https://login.microsoftonline.com/common/.well-known/openid-configuration
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

    logger.info("Saving public keys to the app")
    app.set_entra_jwt_keys(public_keys)


@app.listener("after_server_stop")
async def close_connection(app: IntranetApp, loop):
    pool = app.get_db_pool()
    pool.close()
    await pool.wait_closed()


@app.get("/ping")
async def ping_test(request: Request):
    return response.text("Pong")


@app.get("/")
async def route_to_login_or_home(request: Request):
    # Get the Authorization cookie
    auth = request.cookies.get("JWT_TOKEN")
    if auth is None:
        return response.redirect("login")
    else:
        return response.redirect("home")


@app.exception(NotFound)
def ignore_404s(request, exception):
    return render("404.html")


# Check for Production environment
is_prod = app.config["IS_PROD"]

# Use a KWARGS dict to pass to app.run dynamically
kwargs = {"host": "0.0.0.0"}

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

if __name__ == "__main__":
    # Run the API Server
    app.run(**kwargs)
