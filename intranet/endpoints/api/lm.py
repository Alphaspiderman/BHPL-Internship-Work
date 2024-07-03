from sanic.request import Request
from sanic.response import json as json_resp
from sanic.views import HTTPMethodView
import json

from intranet.app import IntranetApp


class Location_Master(HTTPMethodView):
    table_schema = [
        "Store_Code",
        "Store_Name",
        "Posist_Store_Name",
        "Ownership_Type",
        "Local_Address",
        "City",
        "State_Name",
        "Region_Internal",
        "Postal_Code",
        "Champs_Number",
        "Primary_Brand_Channel",
        "Facility_Type",
        "Ordering_Methods",
        "Store_Type",
        "Store_Phone",
        "Store_Email",
        "Status",
        "Latitude",
        "Longitude",
        "Store_Open_Date",
        "Posit_Live_Date",
        "Seat_Count",
        "Local_Org_Name",
        "Franchisee_id",
        "Temp_Close_Date",
        "Reopen_Date",
        "Store_Closure_Date",
        "Sunday_Open",
        "Sunday_Close",
        "Monday_Open",
        "Monday_Close",
        "Tuesday_Open",
        "Tuesday_Close",
        "Wednesday_Open",
        "Wednesday_Close",
        "Thursday_Open",
        "Thursday_Close",
        "Friday_Open",
        "Friday_Close",
        "Saturday_Open",
        "Saturday_Close",
        "Market_Name",
        "Area_Name",
        "Coach_ID",
        "Ip_Range_Start",
        "Ip_Range_End",
        "Subnet",
        "Static_Ip",
        "Link_ISP",
        "Link_Type",
    ]

    async def get(self, request: Request):
        location = request.args.get("location")
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        if not location:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT Store_Code, Store_Name FROM sites")
                    locations = await cur.fetchall()
            return json({"locations": locations})
        else:
            if location == "all":
                async with db_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT * FROM sites")
                        data = await cur.fetchall()
            else:
                async with db_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(
                            "SELECT * FROM sites WHERE Store_Code = %s", (location,)
                        )
                        data = await cur.fetchone()
        # Check for IT Department in JWT
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))
        modified_schema = self.table_schema.copy()
        if jwt_data["department"] != "IT":
            # drop data
            pass
        return json_resp(
            {
                "data": data,
                "schema": modified_schema,
            },
            dumps=lambda x: json.dumps(x, default=str),
        )

    async def post(self, request: Request):
        return json_resp({"message": "To be implemented"})
        # data = request.json
        # app: IntranetApp = request.app
        # db_pool = app.get_db_pool()
        # async with db_pool.acquire() as conn:
        #     async with conn.cursor() as cur:
        #         await cur.execute(
        #             "INSERT INTO sites (name, ip) VALUES (%s, %s)",
        #             (data["name"], data["ip"]),
        #         )
        # return json_resp({"message": "Location added"})

    async def patch(self, request: Request):
        return json_resp({"message": "To be implemented"})
        # data = request.json
        # app: IntranetApp = request.app
        # db_pool = app.get_db_pool()
        # async with db_pool.acquire() as conn:
        #     async with conn.cursor() as cur:
        #         await cur.execute(
        #             "UPDATE sites SET ip = %s WHERE name = %s",
        #             (data["ip"], data["name"]),
        #         )
        # return json_resp({"message": "Location updated"})
