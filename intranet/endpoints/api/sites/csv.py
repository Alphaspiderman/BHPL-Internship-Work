import uuid

import aiocsv
import aiofiles
from sanic.request import Request
from sanic.response import file
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.location import Location


class Location_CSV(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        location = request.args.get("location")
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        # There is a location specified
        location_data = list()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                if location:
                    await cur.execute(
                        "SELECT * FROM sites WHERE Champs_Number = %s", (location,)
                    )
                else:
                    await cur.execute(
                        "SELECT * FROM sites WHERE Champs_Number IS NOT NULL"
                    )
                locations = await cur.fetchall()
                location_data = [Location(entry) for entry in locations]

        # Check for IT Department in JWT
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))
        # Remove IT specific fields if the user is not from IT department
        if jwt_data["department"] != "IT":
            data = [
                list(entry.get_data(is_IT=False).values()) for entry in location_data
            ]
            schema = Location.get_schema(is_IT=False)
        else:
            data = [
                list(entry.get_data(is_IT=True).values()) for entry in location_data
            ]
            schema = Location.get_schema(is_IT=True)
        temp_file_name = f"temp/{uuid.uuid4().hex}.csv"
        async with aiofiles.open(temp_file_name, "w", newline="") as f:
            writer = aiocsv.AsyncWriter(f)
            await writer.writerow(schema)
            await writer.writerows(data)

        resp = await file(temp_file_name, filename="location_data.csv")
        await request.respond(resp)
        await aiofiles.os.remove(temp_file_name)
