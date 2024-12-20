from intranet.app import appserver

from .announcements import Announcements_API
from .bells.award import Award_Bells
from .bells.info import Bell_Info
from .departments import Departments
from .expenses.me import Employee_Expenses
from .expenses.pdf import Expenses_PDF
from .files import Files
from .login.callback import Callback
from .login.root import Login_Root
from .logout import Logout
from .navbar import NavBar
from .sites.checker import Site_Checker
from .sites.csv import Location_CSV
from .sites.downtime import Site_Downtime_Stats
from .sites.employees import Location_Employees
from .sites.info import Location_Master_API
from .sites.missing_sales import Missing_Sales
from .sites.sales import Location_Sales
from .sites.status import Site_Status
from .vendors.contract import Vendor_Contract
from .vendors.info import Vendor_Info
from .vendors.payment import Vendor_Payment

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

# Register the location master endpoint
appserver.add_route(Location_Master_API.as_view(), "/api/sites/info")

# Register the location employees endpoint
appserver.add_route(Location_Employees.as_view(), "/api/sites/employees")

# Register the announcements endpoint
appserver.add_route(Announcements_API.as_view(), "/api/announcements/<id:strorempty>")

# Register the vendor payment endpoint
appserver.add_route(Vendor_Payment.as_view(), "/api/vendors/payment")

# Register the vendor info endpoint
appserver.add_route(Vendor_Info.as_view(), "/api/vendors/info")

# Register the vendor contract endpoint
appserver.add_route(Vendor_Contract.as_view(), "/api/vendors/contract")

# Register the award bells endpoint
appserver.add_route(Award_Bells.as_view(), "/api/bells/award")

# Register the bell info endpoint
appserver.add_route(Bell_Info.as_view(), "/api/bells/info")

# Register the employee expenses endpoint
appserver.add_route(Employee_Expenses.as_view(), "/api/expenses/me")

# Register the expenses pdf endpoint
appserver.add_route(Expenses_PDF.as_view(), "/api/expenses/pdf")

# Register the files endpoint
appserver.add_route(Files.as_view(), "/api/files")

# Register the location csv endpoint
appserver.add_route(Location_CSV.as_view(), "/api/sites/csv")

# Register the departments endpoint
appserver.add_route(Departments.as_view(), "/api/departments")

# Register the navbar endpoint
appserver.add_route(NavBar.as_view(), "/api/navbar")

# Register the location sales endpoint
appserver.add_route(Location_Sales.as_view(), "/api/sites/sales")

# Register the missing sales endpoint
appserver.add_route(Missing_Sales.as_view(), "/api/sites/missing")

# Register the site downtime endpoint
appserver.add_route(Site_Downtime_Stats.as_view(), "/api/sites/downtime")
