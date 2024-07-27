from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class NavBar(HTTPMethodView):
    navbar_entries = [
        ["/home", "Home"],
        {
            "Rewards": [
                ["/rewards/view", "Reward & Recognition"],
                # ["/rewards/bells", "Award Bells"],
            ],
        },
        # {
        #     "Vendors": [
        #         ["/vendors/vendors", "Vendor Management"],
        #         ["/vendors/contracts", "Vendor Contracts"],
        #         ["/vendors/payments", "Vendor Payments"],
        #     ],
        # },
        # ["/locations", "Location Master"],
        ["/connectivity", "Connectivity Status"],
        # {
        #     "Expenses": [
        #         ["/expenses/submit", "Submit Expense"],
        #         ["/expenses/report", "View Report"],
        #     ],
        # },
    ]

    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        # Decode the JWT token
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))

        # Copy the navbar entries
        navbar = [entry.copy() for entry in self.navbar_entries]

        # Check if emp_type is not CORP
        if jwt_data["emp_type"] == "CORP":
            # Add the Vendor section to the navbar
            navbar.insert(
                2,
                {
                    "Vendors": [
                        ["/vendors/vendors", "Vendor Management"],
                        ["/vendors/contracts", "Vendor Contracts"],
                        ["/vendors/payments", "Vendor Payments"],
                    ],
                },
            )

            # Add the Location Master section to the navbar
            navbar.insert(3, ["/locations", "Location Master"])

            # Add the Sales Dashboard section to the navbar
            navbar.insert(5, ["/sales/stats", "Sales Dashboard"])

            # Add the Expenses section to the navbar
            navbar.insert(
                5,
                {
                    "Expenses": [
                        ["/expenses/submit", "Submit Expense"],
                        ["/expenses/report", "View Report"],
                    ],
                },
            )

        else:
            # Add the Sales Dashboard section to the navbar
            navbar.insert(2, ["/sales/submit", "Sales Dashboard"])

        emp_id = jwt_data["emp_id"]
        async with app.get_db_pool().acquire() as conn:
            async with conn.cursor() as cur:
                # Check if emp_id exists in the bells_info table
                await cur.execute(
                    "SELECT * FROM bells_info WHERE Employee_Id = %s", (emp_id,)
                )
                bells_info = await cur.fetchall()
                if len(bells_info) != 0:
                    # Add the Award Bells section to the navbar
                    copy = navbar[1]["Rewards"].copy()
                    copy.append(["/rewards/bells", "Award Bells"])
                    navbar[1]["Rewards"] = copy

        return json(navbar)
