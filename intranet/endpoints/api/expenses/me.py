from datetime import datetime
from typing import List
import uuid
from json import loads

from sanic.response import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.request.form import File

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.expense import Expense


class Employee_Expenses(HTTPMethodView):
    cost_per_km_4 = 13
    cost_per_km_2 = 8

    @require_login(is_api=True)
    async def get(self, request: Request):
        by_doc_date = request.args.get("by_doc_date")
        if by_doc_date is not None and by_doc_date.lower() == "true":
            return await self.get_by_doc_date(request)

        app: IntranetApp = request.app
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        employee_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]

        if date_from is None:
            date_from = datetime.now().strftime("%Y-%m-01")
        if date_to is None:
            date_to = datetime.now().strftime("%Y-%m-%d")
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM expenses WHERE Employee_Id = %s AND Date_Of_Expense >= %s AND Date_Of_Expense <= %s ORDER BY Date_Of_Expense",  # noqa: E501
                    (employee_id, date_from, date_to),
                )
                result = await cur.fetchall()
                expense_data = [
                    Expense(
                        entry,
                        cost_per_km_four_wheeler=self.cost_per_km_4,
                        cost_per_km_two_wheeler=self.cost_per_km_2,
                    )
                    for entry in result
                ]
        return json(
            {
                "data": [
                    list(expense.get_data(show_id=True, show_file_names=True).values())
                    for expense in expense_data
                ],
                "schema": expense_data[0].get_schema(show_id=True),
                "total": sum([expense.get_total() for expense in expense_data]),
            }
        )

    @require_login(is_api=True)
    async def post(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        data = loads(request.form["data"][0])
        employee_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
        date_of_expense = datetime.strptime(
            data["Date_Of_Expense"], "%Y-%m-%d"
        ).strftime("%Y-%m-%d")
        location = data.get("Location")
        stationary = float(data.get("Stationary")) if data.get("Stationary") else 0
        welfare_meal = (
            float(data.get("Welfare_Meal")) if data.get("Welfare_Meal") else 0
        )
        promotion_meal = (
            float(data.get("Promotion_Meal")) if data.get("Promotion_Meal") else 0
        )
        hotel_rent = float(data.get("Hotel_Rent")) if data.get("Hotel_Rent") else 0
        connectivity_charges = (
            float(data.get("Connectivity_Charges"))
            if data.get("Connectivity_Charges")
            else 0
        )
        travel_charge = (
            float(data.get("Travel_Charge")) if data.get("Travel_Charge") else 0
        )
        others = float(data.get("Others")) if data.get("Others") else 0

        personal_vehicle_dist = (
            float(data["Personal_Vehicle_Dist"])
            if data.get("Personal_Vehicle_Dist")
            else 0
        )
        if personal_vehicle_dist != 0:
            vehicle_type = data["Vehicle_Type"]
        else:
            vehicle_type = None
        reason = data["Reason"]
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                files: List[File] = request.files.getlist("file")
                if files:
                    if len(files) == 1:
                        file = files[0]
                        ext = file.name.split(".")[-1]
                        new_name = uuid.uuid4().hex + "." + ext
                        await cur.execute(
                            "INSERT INTO files(File_Id, File_Name, File_Type, File_Data, Uploaded_By) VALUES (%s, %s, %s, %s, %s)",  # noqa: E501
                            (new_name, file.name, file.type, file.body, employee_id),
                        )
                        bill_attached = new_name
                    elif len(files) > 1:
                        return json(
                            {
                                "status": "failure",
                                "message": "Only one file can be attached",
                            }
                        )
                else:
                    bill_attached = None
                await cur.execute(
                    "INSERT INTO expenses (Employee_Id, Date_Of_Expense, Location, Stationary, Welfare_Meal, Promotion_Meal, Hotel_Rent, Connectivity_Charges, Travel_Charge, Others, Bill_Attached, Personal_Vehicle_Dist, Vehicle_Type, Reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  # noqa: E501
                    (
                        employee_id,
                        date_of_expense,
                        location,
                        stationary,
                        welfare_meal,
                        promotion_meal,
                        hotel_rent,
                        connectivity_charges,
                        travel_charge,
                        others,
                        bill_attached,
                        personal_vehicle_dist,
                        vehicle_type,
                        reason,
                    ),
                )
            await conn.commit()
        return json({"status": "success"})

    @require_login(is_api=True)
    async def delete(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        emp_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
        expense_id = request.form.get("expense_id")

        # Ensure we have an expense_id
        if expense_id and len(expense_id) != 0:
            pass
        else:
            return json({"status": "failure", "message": "No Expense ID given"})

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    # Get attached file name
                    await cur.execute(
                        "SELECT Bill_Attached FROM expenses WHERE Id = %s AND Employee_Id = %s",
                        (
                            expense_id,
                            emp_id,
                        ),
                    )
                    result = await cur.fetchone()
                    if result:
                        file_name = result[0]
                        if file_name:
                            await cur.execute(
                                "DELETE FROM files WHERE File_Id = %s",
                                (file_name,),
                            )
                    await cur.execute(
                        "DELETE FROM expenses WHERE Id = %s AND Employee_Id = %s",
                        (
                            expense_id,
                            emp_id,
                        ),
                    )
                except Exception:
                    return json({"status": "failure", "message": "Expense not found"})
            await conn.commit()
        return json({"status": "success"})

    async def get_by_doc_date(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        employee_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM expenses WHERE Employee_Id = %s AND Document_Date >= CURDATE() AND Document_Date < CURDATE() + INTERVAL 1 DAY ORDER BY Document_Date DESC",  # noqa: E501
                    (employee_id),
                )
                result = await cur.fetchall()
                expense_data = [
                    Expense(
                        entry,
                        cost_per_km_four_wheeler=self.cost_per_km_4,
                        cost_per_km_two_wheeler=self.cost_per_km_2,
                    )
                    for entry in result
                ]
        if len(expense_data) > 0:
            return json(
                {
                    "data": [
                        list(expense.get_data().values()) for expense in expense_data
                    ],
                    "schema": expense_data[0].get_schema(),
                    "total": sum([expense.get_total() for expense in expense_data]),
                }
            )
        else:
            return json({"data": [], "total": "0"})
