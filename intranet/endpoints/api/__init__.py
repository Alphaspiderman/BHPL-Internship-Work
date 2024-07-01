from .login.callback import Callback
from .login.root import Login_Root
from .logout import Logout
from .sites.checker import Site_Checker
from .sites.status import Site_Status
from .announcements import Announcements

from intranet.app import appserver

# Register the login endpoints
appserver.add_route(Login_Root.as_view(), "/api/login")

# Register the callback endpoint
appserver.add_route(Callback.as_view(), "/api/login/callback")

# Register the logout endpoint
appserver.add_route(Logout.as_view(), "/api/logout")

# Register the site checker endpoint
appserver.add_route(Site_Checker.as_view(), "/api/sites/checker")

# Register the site status endpoint
appserver.add_route(Site_Status.as_view(), "/api/sites/status")

# Register the announcements endpoint
appserver.add_route(Announcements.as_view(), "/api/announcements")
