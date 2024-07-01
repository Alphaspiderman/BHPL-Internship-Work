from intranet.app import appserver

# flake8: noqa
import intranet.endpoints.api
from intranet.endpoints.connectivity import Connectivity
from intranet.endpoints.home import Home
from intranet.endpoints.locations import Locations
from intranet.endpoints.login import Login
from intranet.endpoints.sales import Sales
from intranet.endpoints.vendors import Vendors
from intranet.endpoints.create_annoucement import Create_Announcement

appserver.add_route(Home.as_view(), "/home")
appserver.add_route(Login.as_view(), "/login")
appserver.add_route(Locations.as_view(), "/locations")
appserver.add_route(Sales.as_view(), "/sales")
appserver.add_route(Connectivity.as_view(), "/connectivity")
appserver.add_route(Vendors.as_view(), "/vendors")
appserver.add_route(Create_Announcement.as_view(), "/create_announcement")
