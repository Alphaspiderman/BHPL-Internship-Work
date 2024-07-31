from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from datetime import datetime


class Missing_Sales(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        # Check for location
        location = request.args.get("loc")
        # Check for date range
        date_from = request.args.get("from")
        if not date_from:
            return json({"status": "error", "message": "Date not provided"})

        # Transform date to string
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_from = date_from.strftime("%Y-%m-%d")

        # print(f"Location: {location}, Date: {date_from}")

        if location == "all" or not location:
            store_filter = ""
            args = date_from
        else:
            store_filter = "AND s.Store_Code = %s"
            args = (location, date_from)

        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get list of store ids
                await cur.execute(
                    f"""SELECT
                            s.Store_Code,
                            s.Champs_Number,
                            s.Store_Name,
                            d.Date
                        FROM
                            sites s
                        CROSS JOIN
                            (SELECT DISTINCT Date FROM order_source_data WHERE Date > %s) d
                        LEFT JOIN
                            order_source_data osd
                            ON s.Store_Code = osd.Store_Id
                            AND d.Date = osd.Date
                        WHERE
                            osd.Store_Id IS NULL AND
                            s.Status = 'Operational'
                            {store_filter}
                        ORDER BY
                            d.Date,
                            s.Store_Code;
                        """,
                    args,
                )
                result = await cur.fetchall()
                # Transform the result
                result = [
                    {
                        "store_code": row[0],
                        "store_id": row[1],
                        "store_name": row[2],
                        "date": row[3].strftime("%Y-%m-%d"),
                    }
                    for row in result
                ]
                return json({"status": "success", "data": result})
