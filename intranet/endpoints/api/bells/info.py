from datetime import datetime
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Bell_Info(HTTPMethodView):
    def convert_bells(self, card_type):
        """Converts the bells to the integer value"""
        if card_type == "Card_3":
            return 3
        elif card_type == "Card_4":
            return 4
        elif card_type == "Card_5":
            return 5
        else:
            raise ValueError("Invalid card type")

    @require_login()
    async def get(self, request: Request):
        """Stats about Bells awarded to the employee this month"""
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        display = request.args.get("show")

        # Get date to calculate against
        now = datetime.now()
        month_start = now.strftime("%Y-%m-01")

        if display == "home":
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT Bells_Awarded, s.Store_Code, Store_Name, Employee_Code, First_Name, Last_Name FROM bells_awarded b NATURAL JOIN sites s JOIN people p ON Employee_Code = p.Employee_Id  WHERE Award_Date >= %s",  # noqa: E501
                        (month_start,),
                    )
                    bells_awarded = await cur.fetchall()
            # Calculate the stats of bells awarded
            total_bells_awarded = 0
            store_bell_map = {}
            employee_bell_map = {}
            employee_name_id_map = {}
            for award in bells_awarded:
                Store_Name = award[2]
                Bells_Awarded = self.convert_bells(award[0])
                Employee_Id = award[3]
                name = f"{award[4]} {award[5]}"
                total_bells_awarded += Bells_Awarded
                store_bell_map[Store_Name] = (
                    store_bell_map.get(Store_Name, 0) + Bells_Awarded
                )
                employee_bell_map[Employee_Id] = (
                    employee_bell_map.get(Employee_Id, 0) + Bells_Awarded
                )
                employee_name_id_map[Employee_Id] = name

            top_10_stores = sorted(
                store_bell_map.keys(), key=lambda x: store_bell_map[x], reverse=True
            )[:10]
            top_10_employees = sorted(
                employee_bell_map.keys(),
                key=lambda x: employee_bell_map[x],
                reverse=True,
            )[:10]

            bells_other_stores = total_bells_awarded - sum(
                store_bell_map[store] for store in top_10_stores
            )

            bells_other_employees = total_bells_awarded - sum(
                employee_bell_map[employee] for employee in top_10_employees
            )

            return json(
                {
                    "total_bells_awarded": total_bells_awarded,
                    "top_10": {"store": top_10_stores, "employee": top_10_employees},
                    "others": {
                        "store": bells_other_stores,
                        "employee": bells_other_employees,
                    },
                    "bell_map": {
                        "store": store_bell_map,
                        "employee": employee_bell_map,
                    },
                    "employee_name_id_map": employee_name_id_map,
                }
            )
        else:
            return json({"error": "Invalid display type"})
