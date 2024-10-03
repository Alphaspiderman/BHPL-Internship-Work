from datetime import datetime
import uuid

from sanic.request import Request
from sanic.response import json, file
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login

import aiocsv
import aiofiles


class Bell_Info(HTTPMethodView):
    bell_value_map = {
        3: 100,
        4: 200,
        5: 300,
    }

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

    @require_login(is_api=True)
    async def get(self, request: Request):
        """Stats about Bells awarded to the employee this month"""
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        display = request.args.get("show")

        year = request.args.get("year")
        month = request.args.get("month")

        export = request.args.get("export")
        if year is None or month is None:
            # Get date to calculate against
            now = datetime.now()
            month_start = now.strftime("%Y-%m-01")
            month_end = now.replace(month=now.month + 1).strftime("%Y-%m-01")

        else:
            date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-01")
            month_start = date.strftime("%Y-%m-01")
            month_end = date.replace(month=date.month + 1).strftime("%Y-%m-01")

        can_export = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["department"] in [
            "IT",
            "HR",
        ]

        if export == "true" and can_export:
            return await self.export(request, month_start, month_end)

        if display == "home":
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT Bells_Awarded, s.Store_Code, Store_Name, Employee_Code, Employee_Name FROM bells_awarded b NATURAL JOIN sites s JOIN people p ON Employee_Code = p.Employee_Id WHERE Award_Date >= %s AND Award_Date < %s",  # noqa: E501
                        (month_start, month_end),
                    )
                    bells_awarded = await cur.fetchall()
            # Calculate the stats of bells awarded
            total_bells_awarded = 0
            store_bell_cnt_map = {}
            store_bell_val_map = {}
            employee_bell_cnt_map = {}
            employee_bell_val_map = {}
            employee_id_name_map = {}
            employee_id_store_map = {}

            # Map value includes bell count and bell value
            for award in bells_awarded:
                Store_Name = award[2]
                Bells_Awarded = self.convert_bells(award[0])
                Bell_Value = self.bell_value_map[Bells_Awarded]
                Employee_Id = award[3]
                name = award[4]
                total_bells_awarded += Bells_Awarded
                store_bell_cnt_map[Store_Name] = (
                    store_bell_cnt_map.get(Store_Name, 0) + Bells_Awarded
                )
                store_bell_val_map[Store_Name] = (
                    store_bell_val_map.get(Store_Name, 0) + Bell_Value
                )

                employee_bell_cnt_map[Employee_Id] = (
                    employee_bell_cnt_map.get(Employee_Id, 0) + Bells_Awarded
                )
                employee_bell_val_map[Employee_Id] = (
                    employee_bell_val_map.get(Employee_Id, 0) + Bell_Value
                )

                employee_id_name_map[Employee_Id] = name
                employee_id_store_map[Employee_Id] = Store_Name

            # Sort the stores and employees by bell count
            stores_bells_by_cnt = sorted(
                store_bell_cnt_map.keys(),
                key=lambda x: store_bell_cnt_map[x],
                reverse=True,
            )
            employee_bells_by_cnt = sorted(
                employee_bell_cnt_map.keys(),
                key=lambda x: employee_bell_cnt_map[x],
                reverse=True,
            )
            employee_bells_by_val = sorted(
                employee_bell_val_map.keys(),
                key=lambda x: employee_bell_val_map[x],
                reverse=True,
            )

            return json(
                {
                    "total_bells_awarded": total_bells_awarded,
                    "by_count": {
                        "store": stores_bells_by_cnt,
                        "employee": employee_bells_by_cnt,
                    },
                    "by_value": {
                        "employee": employee_bells_by_val,
                    },
                    "employee_id_bell_count_map": employee_bell_cnt_map,
                    "employee_id_bell_value_map": employee_bell_val_map,
                    "store_bell_count_map": store_bell_cnt_map,
                    "employee_id_name_map": employee_id_name_map,
                    "employee_id_store_map": employee_id_store_map,
                    "can_export": can_export,
                }
            )
        else:
            return json({"error": "Invalid display type"})

    async def export(self, request: Request, month_start, month_end):
        """Trigger download of bells awarded for provided month"""
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()

        year = month_start.split("-")[0]
        month = month_start.split("-")[1]

        # Get the bells awarded for the month
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM bells_awarded WHERE Award_Date >= %s AND Award_Date < %s",
                    (
                        month_start,
                        month_end,
                    ),
                )
                bells_awarded = await cur.fetchall()

        # Write the bells awarded to a file
        # Random string to avoid conflicts
        random = str(uuid.uuid4().hex)
        file_name = f"temp/{random}.csv"
        async with aiofiles.open(
            file_name, mode="w", encoding="utf-8", newline=""
        ) as afp:
            writer = aiocsv.AsyncWriter(afp)
            await writer.writerow(
                [
                    "ID",
                    "Employee_Code",
                    "Store_Code",
                    "Bells_Awarded",
                    "Award_Date",
                    "Awarded_By_Id",
                    "Reason",
                    "File_Id",
                ]
            )
            await writer.writerows(bells_awarded)
        # Return the file
        resp = await file(
            file_name,
            filename=f"bells_awarded_{month}_{year}.csv",
            mime_type="text/csv",
        )
        # Send the response
        await request.respond(resp)
        # Remove the file after sending
        await aiofiles.os.remove(file_name)
