from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Expenses(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        app: IntranetApp = request.app
        emp_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM people WHERE Employee_Id = %s", (emp_id,)
                )
                employee = await cur.fetchall()

        if len(employee) == 1:
            emp_name = f"{employee[0][1]} {employee[0][2]}"
            emp_dept = employee[0][5]
            emp_grade = employee[0][7]
            return await render(
                "expenses.html",
                context={
                    "emp_name": emp_name,
                    "emp_id": emp_id,
                    "emp_dept": emp_dept,
                    "emp_grade": emp_grade,
                },
            )
        else:
            return json({"status": "error", "message": "Employee not found"})
