from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Award_Bells(HTTPMethodView):

    @require_login
    async def get(self, request: Request):
        """Shows the bells the employee can award."""
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        employee_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM bell_info WHERE Employee_ID = %s", (employee_id,)
                )
                bell_info = await cur.fetchall()
        if bell_info is None:
            return json(
                {"status": "failure", "message": "You can't award bells"}, status=404
            )
        return json(
            {
                "Card_5_Total": int(bell_info[1]),
                "Card_4_Total": int(bell_info[2]),
                "Card_3_Total": int(bell_info[3]),
                "Card_5_Left": int(bell_info[4]),
                "Card_4_Left": int(bell_info[5]),
                "Card_3_Left": int(bell_info[6]),
            }
        )

    @require_login
    async def post(self, request: Request):
        form_data = request.form
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        Awarded_By_Id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]

        # Extract the information from the form data
        Store_Code = form_data.get("Store_Code")
        Employee_Code = form_data.get("Employee_Code")
        Bells_Awarded = form_data.get("Bells_Awarded")
        Award_Date = form_data.get("Award_Date")
        Reason = form_data.get("Reason")

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Check if the employee has the bells to award
                await cur.execute(
                    "SELECT * FROM bell_info WHERE Employee_ID = %s", (Awarded_By_Id,)
                )
                bell_info = await cur.fetchall()
                if bell_info is None:
                    return json(
                        {"status": "failure", "message": "You can't award bells"},
                        status=404,
                    )
                card_5_left = int(bell_info[4])
                card_4_left = int(bell_info[5])
                card_3_left = int(bell_info[6])

                if Bells_Awarded == "Card_5":
                    if card_5_left == 0:
                        return json(
                            {
                                "status": "failure",
                                "message": "You can't award more 5 Bell Cards",
                            },
                            status=404,
                        )
                    else:
                        await cur.execute(
                            "INSERT INTO bells_awarded (Store_Code, Employee_Code, Bells_Awarded, Award_Date, Awarded_By_Id, Reason) VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                Store_Code,
                                Employee_Code,
                                "Card_5",
                                Award_Date,
                                Awarded_By_Id,
                                Reason,
                            ),
                        )
                        await cur.execute(
                            "UPDATE bell_info SET Card_5_Left = %s WHERE Employee_ID = %s",
                            (card_5_left - 1, Awarded_By_Id),
                        )
                elif Bells_Awarded == "Card_4":
                    if card_4_left == 0:
                        return json(
                            {
                                "status": "failure",
                                "message": "You can't award more 4 Bell Cards",
                            },
                            status=404,
                        )
                    else:
                        await cur.execute(
                            "INSERT INTO bells_awarded (Store_Code, Employee_Code, Bells_Awarded, Award_Date, Awarded_By_Id, Reason) VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                Store_Code,
                                Employee_Code,
                                "Card_4",
                                Award_Date,
                                Awarded_By_Id,
                                Reason,
                            ),
                        )
                        await cur.execute(
                            "UPDATE bell_info SET Card_4_Left = %s WHERE Employee_ID = %s",
                            (card_4_left - 1, Awarded_By_Id),
                        )
                elif Bells_Awarded == "Card_3":
                    if card_3_left == 0:
                        return json(
                            {
                                "status": "failure",
                                "message": "You can't award more 3 Bell Cards",
                            },
                            status=404,
                        )
                    else:
                        await cur.execute(
                            "INSERT INTO bells_awarded (Store_Code, Employee_Code, Bells_Awarded, Award_Date, Awarded_By_Id, Reason) VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                Store_Code,
                                Employee_Code,
                                "Card_3",
                                Award_Date,
                                Awarded_By_Id,
                                Reason,
                            ),
                        )
                        await cur.execute(
                            "UPDATE bell_info SET Card_3_Left = %s WHERE Employee_ID = %s",
                            (card_3_left - 1, Awarded_By_Id),
                        )
                else:
                    return json(
                        {"status": "failure", "message": "Invalid bell card"},
                        status=404,
                    )