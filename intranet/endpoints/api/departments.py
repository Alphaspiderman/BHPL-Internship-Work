from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Departments(HTTPMethodView):
    schema = [
        "Department_Code",
        "Department_Name",
        "Department_Head_Name",
        "Department_Email",
    ]

    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        show_all = request.args.get("show")
        if show_all:
            show_all = show_all.lower() == "true"
        else:
            show_all = False
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM departments")
                departments = await cur.fetchall()
                if show_all:
                    return json({"data": departments, "schema": self.schema})
                else:
                    return json(
                        {
                            "data": [
                                [
                                    entry[0],
                                    entry[1],
                                ]
                                for entry in departments
                            ],
                            "schema": ["Department_Code", "Department_Name"],
                        }
                    )
