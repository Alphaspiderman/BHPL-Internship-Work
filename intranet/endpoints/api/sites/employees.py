from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp


class Location_Employees(HTTPMethodView):
    async def get(self, request: Request):
        location = request.args.get("loc")
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM people where Store_Code = %s", (location,)
                )
                result = await cur.fetchall()

        # Only return the Employee Code and Name
        employees = []
        for employee in result:
            employees.append([employee[0], employee[1] + " " + employee[2]])
        return json(employees)