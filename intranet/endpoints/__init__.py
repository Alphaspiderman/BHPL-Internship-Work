from intranet.endpoints.home import Home
from intranet.endpoints.login import Login
from intranet.app import appserver

# flake8: noqa
import intranet.endpoints.api

appserver.add_route(Home.as_view(), "/home")
appserver.add_route(Login.as_view(), "/login")
