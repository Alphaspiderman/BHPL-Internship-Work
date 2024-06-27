from sanic import Sanic

class IntranetApp(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx.entra_public_keys = dict()
    
    def run(self, public_key:str, private_key:str, *args, **kwargs):
        self.ctx.signing_keys = {"public_key": public_key, "private_key": private_key}
        super().run(*args, **kwargs)

    @property
    def get_entra_jwt_keys(self) -> dict:
        return self.ctx.entra_public_keys

    def set_entra_jwt_keys(self, keys:dict):
        self.ctx.entra_public_keys = keys
    
    @property
    def get_public_key(self) -> str:
        return self.ctx.signing_keys.get("public_key")

appserver = IntranetApp("intranet", strict_slashes=False)