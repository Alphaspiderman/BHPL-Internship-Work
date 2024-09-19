from datetime import datetime
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Site_Downtime_Stats(HTTPMethodView):
    def __init__(self):
        super().__init__()

    @require_login(is_api=True)
    async def get(self, request: Request):
        # Check for location
        location = request.args.get("loc")
        if not location:
            return json({"status": "error", "message": "Location not provided"})

        # Check for date range
        date_from = request.args.get("dateFrom")
        date_to = request.args.get("dateTo")

        if not date_from or not date_to:
            return json({"status": "error", "message": "Date range not provided"})

        # Transform date to timestamp string
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_from = date_from.isoformat()
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        date_to = date_to.isoformat()

        if location == "all":
            filter = ""
            args = (date_from, date_to)
        else:
            filter = "s.Champs_Number = %s AND"
            args = (location, date_from, date_to)

        # Get downtime data
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    f"""SELECT
                        s.Champs_Number,
                        s.Store_Code,
                        s.Store_Name,
                        n.Start_Time,
                        n.End_Time
                    FROM
                        network_uptime n
                    JOIN
                        sites s
                    ON
                        s.Store_Code = n.Store_Code
                    WHERE
                        {filter}
                        n.Start_Time >= %s AND (n.End_Time <= %s OR n.End_Time IS NULL)
                    ORDER BY
                        n.Start_Time;
                    """,
                    args,
                )
                data = await cursor.fetchall()

        # Transform data to JSON
        data = [
            {
                "champsNumber": row[0],
                "storeCode": row[1],
                "storeName": row[2],
                "startTime": row[3].isoformat(),
                "endTime": row[4].isoformat() if row[4] is not None else None,
            }
            for row in data
        ]

        result = {
            "status": "success",
            "data": data,
        }
        return json(result)
