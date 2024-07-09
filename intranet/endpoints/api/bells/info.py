from datetime import datetime
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Bell_Info(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        """Stats about Bells awarded to the employee this month"""
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        employee_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]

        # Get date to calculate against
        now = datetime.now()
        month_start = now.strftime("%Y-%m-01")

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM bells_awarded WHERE Award_Date >= %s", (month_start,)
                )
                bells_awarded = await cur.fetchall()
        # Calculate the stats of bells awarded
        total_bells_awarded = 0
        employee_bell_map = {}
        store_bell_map = {}
        for award in bells_awarded:
            total_bells_awarded += award["Bells_Awarded"]
            if award["Awarded_To"] == employee_id:
                employee_bell_map[award["Awarded_By"]] = (
                    employee_bell_map.get(award["Awarded_By"], 0)
                    + award["Bells_Awarded"]
                )
            store_bell_map[award["Store_Code"]] = (
                store_bell_map.get(award["Store_Code"], 0) + award["Bells_Awarded"]
            )

        return json(
            {
                "total_bells_awarded": total_bells_awarded,
                "employee_bell_map": employee_bell_map,
                "store_bell_map": store_bell_map,
            }
        )
