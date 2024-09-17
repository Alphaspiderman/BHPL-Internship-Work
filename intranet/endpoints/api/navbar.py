from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class NavBar(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        # Decode the JWT token
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))

        # Create an empty navbar
        navbar = []

        # Add the Home section to the navbar
        navbar.append(["/home", "Home"])

        # Check if emp_type is CORP
        if jwt_data["emp_type"] in ["CORP", "REGI"]:
            emp_id = jwt_data["emp_id"]
            async with app.get_db_pool().acquire() as conn:
                async with conn.cursor() as cur:
                    # Check if emp_id exists in the bells_info table
                    await cur.execute(
                        "SELECT * FROM bells_info WHERE Employee_Id = %s", (emp_id,)
                    )
                    bells_info = await cur.fetchall()
                    if len(bells_info) != 0:
                        navbar.append(
                            {
                                "Rewards": [
                                    ["/rewards/view", "Reward & Recognition"],
                                    ["/rewards/bells", "Award Bells"],
                                ],
                            }
                        )
                    else:
                        navbar.append(
                            {
                                "Rewards": [
                                    ["/rewards/view", "Reward & Recognition"],
                                ],
                            }
                        )

            # Add the Vendor section to the navbar
            navbar.append(
                {
                    "Vendors": [
                        ["/vendors/vendors", "Vendor Management"],
                        ["/vendors/contracts", "Vendor Contracts"],
                        ["/vendors/payments", "Vendor Payments"],
                    ],
                }
            )

            # Add the Location section to the navbar
            navbar.append(
                ["/locations", "Location Master"],
            )

            # Add the Connectivity section to the navbar
            navbar.append(
                {
                    "Connectivity": [
                        ["/connectivity", "Network Status"],
                        ["/sites/downtime", "Network Downtime"],
                    ],
                }
            )

            # Add the Expenses section to the navbar
            navbar.append(
                {
                    "Expenses": [
                        ["/expenses/submit", "Submit Expense"],
                        ["/expenses/report", "View Report"],
                    ],
                }
            )

            # Add the Sales Dashboard section to the navbar
            navbar.append(
                {
                    "Sales": [
                        ["/sales/overview", "Sales Overview"],
                        ["/sales/stats", "Sales Dashboard"],
                        ["/sales/missing", "View Missing Entries"],
                    ]
                }
            )
        else:
            # Add Reward and Recognition section to the navbar
            navbar.append(
                {
                    "Rewards": [
                        ["/rewards/view", "Reward & Recognition"],
                    ],
                }
            )

            # Add the sales submit section to the navbar
            navbar.append(["/sales/submit", "Submit Data"])

        return json(navbar)
