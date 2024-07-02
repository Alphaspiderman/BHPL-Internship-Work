from datetime import datetime, timedelta, timezone
from typing import Literal
from sanic import Sanic
import aiomysql
import jwt

from intranet.models.JWTStatus import JWTStatus


class IntranetApp(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx.entra_public_keys = dict()
        self.ctx.login_states = dict()
        self.ctx.site_checker = {
            "total": 0,
            "checked": 0,
            "online": list(),
            "offline": list(),
            "is_processing": False,
            "last_run": None,
        }

    def run(self, public_key: str, private_key: str, *args, **kwargs):
        self.ctx.signing_keys = {"public_key": public_key, "private_key": private_key}
        super().run(*args, **kwargs)

    @property
    def entra_jwt_keys(self) -> dict:
        return self.ctx.entra_public_keys

    def set_entra_jwt_keys(self, keys: dict):
        self.ctx.entra_public_keys = keys

    @property
    def public_key(self) -> str:
        return self.ctx.signing_keys.get("public_key")

    async def connect_db(self):
        pool = await aiomysql.create_pool(
            host=self.config["DB_HOST"],
            port=self.config["DB_PORT"],
            user=self.config["DB_USERNAME"],
            password=self.config["DB_PASSWORD"],
            db=self.config["DB_NAME"],
        )
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 42;")
                (r,) = await cur.fetchone()
        try:
            assert r == 42
        except AssertionError:
            raise Exception("Database connection failed")
        self.ctx.db_pool = pool

    @property
    def get_db_pool(self):
        return self.ctx.db_pool

    def decode_jwt(self, jwt_token: str) -> dict:
        return jwt.decode(jwt_token, key=self.public_key, algorithms="RS256")

    def check_server_jwt(self, jwt_token: str) -> JWTStatus:
        if not jwt_token or jwt_token == "":
            return JWTStatus(authenticated=False, message="JWT Token not provided")
        try:
            self.decode_jwt(jwt_token)
        except jwt.exceptions.ImmatureSignatureError:
            # Raised when a token’s nbf claim represents a time in the future
            d = JWTStatus(
                authenticated=False, message="JWT Token not allowed to be used at time"
            )
        except jwt.exceptions.InvalidIssuedAtError:
            # Raised when a token’s iat claim is in the future
            d = JWTStatus(authenticated=False, message="JWT Token issued in the future")
        except jwt.exceptions.ExpiredSignatureError:
            # Raised when a token’s exp claim indicates that it has expired
            d = JWTStatus(authenticated=False, message="JWT Token has expired")
        except jwt.exceptions.InvalidTokenError:
            # Generic invalid token
            d = JWTStatus(authenticated=False, message="JWT Token is invalid")
        else:
            # Valid Token
            d = JWTStatus(authenticated=True)

        return d

    async def generate_jwt(
        app: Sanic,
        data: dict,
        validity: int,
        target: Literal["corporate", "outlet", "vendor"],
    ) -> str:
        """Generates JWT with given data"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=validity)

        try:
            # Attempt to get Host from config
            host = app.config["HOST"]
        except KeyError:
            # Unable to get Host from config, Quit app due to required field
            app.stop()

        iss = f"INTRANET_API_{host}"
        data.update(
            {"exp": expire, "iat": now, "nbf": now, "iss": iss, "state": target.lower()}
        )
        return jwt.encode(data, app.config["PRIV_KEY"], algorithm="RS256")

    def add_login_state(self, state: str, nonce: str):
        dic: dict = self.ctx.login_states
        dic[nonce] = state

    def consume_login_state(self, nonce: str) -> str:
        dic: dict = self.ctx.login_states
        return dic.pop(nonce)

    def get_site_check_time(self) -> datetime:
        return self.ctx.site_check_last_run

    def reset_site_checker(self):
        self.ctx.site_checker = {
            "total": 0,
            "checked": 0,
            "online": list(),
            "offline": list(),
            "is_processing": False,
            "last_run": None,
        }

    def set_site_checked_total(self, total: int):
        self.ctx.site_checker["last_run"] = datetime.now(timezone.utc)
        self.ctx.site_checker["total"] = total

    def add_site_checker(self, site: str, is_online: bool):
        self.ctx.site_checker["checked"] += 1
        if is_online:
            self.ctx.site_checker["online"].append(site)
        else:
            self.ctx.site_checker["offline"].append(site)

    def get_site_checker_status(self):
        return self.ctx.site_checker["is_processing"]

    def get_site_checker_info(self):
        return self.ctx.site_checker


appserver = IntranetApp("intranet", strict_slashes=False)
