from datetime import datetime, timedelta, timezone

import aiomysql
import jwt
from sanic import Sanic

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

    def get_entra_jwt_keys(self) -> dict:
        return self.ctx.entra_public_keys

    def set_entra_jwt_keys(self, keys: dict):
        self.ctx.entra_public_keys = keys

    def get_public_key(self) -> str:
        return self.config["PRIV_KEY"]

    async def connect_db(self):
        pool = await aiomysql.create_pool(
            host=self.config["DB_HOST"],
            port=self.config["DB_PORT"],
            user=self.config["DB_USERNAME"],
            password=self.config["DB_PASSWORD"],
            db=self.config["DB_NAME"],
            autocommit=True,
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

    def get_db_pool(self):
        return self.ctx.db_pool

    def decode_jwt(self, jwt_token: str) -> dict:
        return jwt.decode(jwt_token, key=self.config["PUB_KEY"], algorithms="RS256")

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
        self,
        data: dict,
        validity: int,
    ) -> str:
        """Generates JWT with given data"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=validity)

        try:
            # Attempt to get Host from config
            host = self.config["HOST"]
        except KeyError:
            # Unable to get Host from config, Quit app due to required field
            self.stop()

        iss = f"INTRANET_API_{host}"
        data.update({"exp": expire, "iat": now, "nbf": now, "iss": iss})
        return jwt.encode(data, self.config["PRIV_KEY"], algorithm="RS256")

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
