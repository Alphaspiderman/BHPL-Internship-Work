from .login.callback import Callback
from .login.root import Login_Root
from .logout import Logout
from .sites.checker import Site_Checker
from .sites.status import Site_Status
from .announcements import Announcements
from .lm import Location_Master
from .vendors.payment import Vendor_Payment
from .vendors.info import Vendor_Info
from .vendors.amc import Contract_AMC
from .vendors.contract import Vendor_Contract

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
appserver.add_route(Announcements.as_view(), "/api/announcements/<id:strorempty>")

# Register the location master endpoint
appserver.add_route(Location_Master.as_view(), "/api/lm")

# Register the vendor payment endpoint
appserver.add_route(Vendor_Payment.as_view(), "/api/vendors/payment")

# Register the vendor info endpoint
appserver.add_route(Vendor_Info.as_view(), "/api/vendors/info")

# Register the vendor contract endpoint
appserver.add_route(Vendor_Contract.as_view(), "/api/vendors/contract")

# Register the vendor amc endpoint
appserver.add_route(Contract_AMC.as_view(), "/api/vendors/amc")
