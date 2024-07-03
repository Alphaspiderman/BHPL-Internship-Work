from sanic.request import Request
from sanic.response import json as json_resp
from sanic.views import HTTPMethodView
import json
from intranet.models.location import Location

from intranet.app import IntranetApp


class Location_Master(HTTPMethodView):
    async def get(self, request: Request):
        location = request.args.get("location")
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        if not location:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT Store_Code, Store_Name FROM sites")
                    locations = await cur.fetchall()
            return json_resp({"locations": locations})
        # There is a location specified
        location_data = list()
        # Get the data from the database
        if location == "all":
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM sites")
                    data = await cur.fetchall()
                    location_data = [Location(entry) for entry in data]
        else:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT * FROM sites WHERE Store_Code = %s", (location,)
                    )
                    data = await cur.fetchone()
                    location_data = [Location(data)]
        # Check for IT Department in JWT
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))
        # Remove IT specific fields if the user is not from IT department
        if jwt_data["department"] != "IT":
            data = [
                list(entry.get_data(is_IT=False).values()) for entry in location_data
            ]
            schema = location_data[0].get_schema(is_IT=False)
        else:
            data = [
                list(entry.get_data(is_IT=True).values()) for entry in location_data
            ]
            schema = location_data[0].get_schema(is_IT=True)

        # Return the data using custom JSON serializer
        return json_resp(
            {
                "data": data,
                "schema": schema,
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
