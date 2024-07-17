from datetime import datetime

from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import render

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.employee import Employee
from intranet.models.expense import Expense


class Expenses_PDF(HTTPMethodView):
    cost_per_km_4 = 13
    cost_per_km_2 = 8

    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        JWT_Data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))
        employee_id = JWT_Data["emp_id"]
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
                await cur.execute(
                    "SELECT * FROM people WHERE Employee_Id = %s",
                    (employee_id,),
                )
                data = await cur.fetchone()
                employee = Employee(data)
        tot_without_bill = 0.0
        master_total = 0.0
        # Category wise totals
        Stationary_Total = 0.0
        Welfare_Meal_Total = 0.0
        Promotion_Meal_Total = 0.0
        Hotel_Rent_Total = 0.0
        Connectivity_Charges_Total = 0.0
        Travel_Charge_Total = 0.0
        Personal_Vehicle_Dist_Total = 0.0
        Personal_Vehicle_Cost_Total = 0.0
        Other_Total = 0.0
        for entry in expense_data:
            Stationary_Total += float(entry.Stationary)
            Welfare_Meal_Total += float(entry.Welfare_Meal)
            Promotion_Meal_Total += float(entry.Promotion_Meal)
            Hotel_Rent_Total += float(entry.Hotel_Rent)
            Connectivity_Charges_Total += float(entry.Connectivity_Charges)
            Travel_Charge_Total += float(entry.Travel_Charge)
            Personal_Vehicle_Dist_Total += float(entry.Personal_Vehicle_Dist)
            Personal_Vehicle_Cost_Total += entry.get_personal_vehicle_comp()
            Other_Total += float(entry.Others)
            master_total += entry.get_total()
            if entry.is_bill_attached() == "No":
                tot_without_bill += entry.get_total()
        return await render(
            "expense_claim_template.html",
            context={
                "employee_name": employee.get_full_name(),
                "department": employee.Department,
                "employee_id": employee_id,
                "date_from": date_from,
                "date_to": date_to,
                "total_without_bill": tot_without_bill,
                "employee_grade": employee.Grade,
                "expenses": expense_data,
                "master_total": master_total,
                "Stationary_Total": Stationary_Total,
                "Welfare_Meal_Total": Welfare_Meal_Total,
                "Promotion_Meal_Total": Promotion_Meal_Total,
                "Hotel_Rent_Total": Hotel_Rent_Total,
                "Connectivity_Charges_Total": Connectivity_Charges_Total,
                "Travel_Charge_Total": Travel_Charge_Total,
                "Personal_Vehicle_Cost_Total": Personal_Vehicle_Cost_Total,
                "Personal_Vehicle_Dist_Total": Personal_Vehicle_Dist_Total,
                "Other_Total": Other_Total,
                "adv_adjustment": 0,
            },
        )
