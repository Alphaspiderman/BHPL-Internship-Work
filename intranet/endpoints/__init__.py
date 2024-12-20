import intranet.endpoints.api  # noqa: F401
from intranet.app import appserver
from intranet.endpoints.announcements.create import Create_Announcement
from intranet.endpoints.announcements.render import Announcements
from intranet.endpoints.connectivity import Connectivity
from intranet.endpoints.expenses.expense_report import Expense_Report
from intranet.endpoints.expenses.expenses import Expenses
from intranet.endpoints.home import Home
from intranet.endpoints.HTTP_404 import HTTP_404
from intranet.endpoints.locations.master import Location_Master
from intranet.endpoints.login import Login
from intranet.endpoints.rewards.reward_bells import Reward_Bells
from intranet.endpoints.rewards.rewards import Rewards
from intranet.endpoints.sales.missing import Missing_Site_Sales
from intranet.endpoints.sales.overview import Sales_Overview
from intranet.endpoints.sales.stats import Sales_Stats
from intranet.endpoints.sales.submit import Sales_Input
from intranet.endpoints.sites.create import Create_Site
from intranet.endpoints.sites.downtime import Site_Downtime
from intranet.endpoints.sites.edit import Edit_Site
from intranet.endpoints.vendors.create.contracts import Contracts_Create
from intranet.endpoints.vendors.create.vendors import Vendors_Create
from intranet.endpoints.vendors.edit.contracts import Contracts_Edit
from intranet.endpoints.vendors.edit.payments import Payments_Edit
from intranet.endpoints.vendors.edit.vendors import Vendors_Edit
from intranet.endpoints.vendors.view.contracts import Contracts_View
from intranet.endpoints.vendors.view.payments import Payments_View
from intranet.endpoints.vendors.view.vendors import Vendors_View

appserver.add_route(Home.as_view(), "/home")
appserver.add_route(Login.as_view(), "/login")
appserver.add_route(Location_Master.as_view(), "/locations")
appserver.add_route(Create_Site.as_view(), "/locations/create")
appserver.add_route(Edit_Site.as_view(), "/locations/edit/<uuid:str>")
appserver.add_route(Sales_Input.as_view(), "/sales/submit")
appserver.add_route(Sales_Stats.as_view(), "/sales/stats")
appserver.add_route(Connectivity.as_view(), "/connectivity")
appserver.add_route(Vendors_View.as_view(), "/vendors/vendors")
appserver.add_route(Contracts_View.as_view(), "/vendors/contracts")
appserver.add_route(Payments_View.as_view(), "/vendors/payments")
appserver.add_route(Vendors_Create.as_view(), "/vendors/vendors/create")
appserver.add_route(Contracts_Create.as_view(), "/vendors/contracts/create")
appserver.add_route(Vendors_Edit.as_view(), "/vendors/vendors/edit/<uuid:str>")
appserver.add_route(Contracts_Edit.as_view(), "/vendors/contracts/edit/<uuid:str>")
appserver.add_route(Payments_Edit.as_view(), "/vendors/payments/edit/<uuid:str>")
appserver.add_route(Create_Announcement.as_view(), "/create_announcement")
appserver.add_route(Announcements.as_view(), "/announcement/<uuid:str>")
appserver.add_route(Reward_Bells.as_view(), "/rewards/bells")
appserver.add_route(HTTP_404.as_view(), "/404")
appserver.add_route(Rewards.as_view(), "/rewards/view")
appserver.add_route(Expenses.as_view(), "/expenses/submit")
appserver.add_route(Expense_Report.as_view(), "/expenses/report")
appserver.add_route(Site_Downtime.as_view(), "/sites/downtime")
appserver.add_route(Missing_Site_Sales.as_view(), "/sales/missing")
appserver.add_route(Sales_Overview.as_view(), "/sales/overview")
