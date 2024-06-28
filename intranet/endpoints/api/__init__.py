from .login.callback import Callback
from .login.root import Login_Root

from intranet.app import appserver

# Register the login endpoints
appserver.add_route(Login_Root.as_view(), "/api/login")

# Register the callback endpoint
appserver.add_route(Callback.as_view(), "/api/login/callback")
