from sanic import Sanic
import aiomysql


class IntranetApp(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx.entra_public_keys = dict()

    def run(self, public_key: str, private_key: str, *args, **kwargs):
        self.ctx.signing_keys = {"public_key": public_key, "private_key": private_key}
        super().run(*args, **kwargs)

    @property
    def get_entra_jwt_keys(self) -> dict:
        return self.ctx.entra_public_keys

    def set_entra_jwt_keys(self, keys: dict):
        self.ctx.entra_public_keys = keys

    @property
    def get_public_key(self) -> str:
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
                print(cur.description)
                (r,) = await cur.fetchone()
        try:
            assert r == 42
        except AssertionError:
            raise Exception("Database connection failed")
        self.ctx.db_pool = pool

    @property
    def get_db_pool(self):
        return self.ctx.db_pool


appserver = IntranetApp("intranet", strict_slashes=False)
