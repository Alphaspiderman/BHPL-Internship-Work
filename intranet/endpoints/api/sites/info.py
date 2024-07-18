from datetime import datetime
import json

from sanic.request import Request
from sanic.response import json as json_resp
from sanic.views import HTTPMethodView
from sanic.log import logger

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.location import Location


class Location_Master(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        location = request.args.get("location")
        show_all = request.args.get("show_all")
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        if not location:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT Champs_Number, Store_Name FROM sites WHERE Champs_Number IS NOT NULL"
                    )
                    locations = await cur.fetchall()
            return json_resp({"locations": locations})
        # There is a location specified
        location_data = list()
        # Get the data from the database
        if location == "all":
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT * FROM sites WHERE Champs_Number IS NOT NULL"
                    )
                    data = await cur.fetchall()
                    location_data = [Location(entry) for entry in data]
        else:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        "SELECT * FROM sites WHERE Champs_Number = %s", (location,)
                    )
                    data = await cur.fetchone()
                    if data:
                        location_data = [Location(data)]
                    else:
                        return json_resp(
                            {"status": "failure", "message": "Location not found"}
                        )
        # Check for IT Department in JWT
        jwt_data = app.decode_jwt(request.cookies.get("JWT_TOKEN"))
        # Remove IT specific fields if the user is not from IT department
        if jwt_data["department"] != "IT":
            data = [
                list(entry.get_data(is_IT=False, show_all=show_all).values())
                for entry in location_data
            ]
            schema = location_data[0].get_schema(is_IT=False, show_all=show_all)
        else:
            data = [
                list(entry.get_data(is_IT=True, show_all=show_all).values())
                for entry in location_data
            ]
            schema = location_data[0].get_schema(is_IT=True, show_all=show_all)

        # Return the data using custom JSON serializer
        return json_resp(
            {
                "data": data,
                "schema": schema,
            },
            dumps=lambda x: json.dumps(x, default=str),
        )

    @require_login(is_api=True)
    async def post(self, request: Request):
        data = request.form
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    storeOpenDate = data.get("storeOpenDate", None)
                    posistLiveDate = data.get("posistLiveDate", None)
                    if storeOpenDate:
                        storeOpenDate = datetime.strptime(
                            storeOpenDate, "%Y-%m-%d"
                        ).strftime("%Y-%m-%d")
                    if posistLiveDate:
                        posistLiveDate = datetime.strptime(
                            posistLiveDate, "%Y-%m-%d"
                        ).strftime("%Y-%m-%d")
                    await cur.execute(
                        """INSERT INTO sites (Champs_Number, Store_Code, Store_Name, Posist_Store_Name,
                        Ownership_Type, Local_Address, City, State_Name, Region_Internal, Postal_Code,
                        Primary_Brand_Channel, Facility_Type, Ordering_Methods, Store_Type, Store_Phone,
                        Store_Email, Status, Latitude, Longitude, Store_Open_Date, Posist_Live_Date,
                        Seat_Count, Local_Org_Name, Franchisee_id, Temp_Close_Date, Reopen_Date,
                        Store_Closure_Date, Sunday_Open, Sunday_Close, Monday_Open, Monday_Close,
                        Tuesday_Open, Tuesday_Close, Wednesday_Open, Wednesday_Close, Thursday_Open,
                        Thursday_Close, Friday_Open, Friday_Close, Saturday_Open, Saturday_Close,
                        Market_Name, Area_Name, Coach_ID, Ip_Range_Start, Ip_Range_End, Subnet,
                        Static_Ip, Link_ISP, Link_Type)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s)""",
                        (
                            data.get("champsNumber", None),
                            data.get("storeCode", None),
                            data.get("storeName", None),
                            data.get("posistStoreName", None),
                            data.get("ownershipType", None),
                            data.get("localAddress", None),
                            data.get("city", None),
                            data.get("stateName", None),
                            data.get("regionInternal", None),
                            data.get("postalCode", None),
                            data.get("primaryBrandChannel", None),
                            data.get("facilityType", None),
                            data.get("orderingMethods", None),
                            data.get("storeType", None),
                            data.get("storePhone", None),
                            data.get("storeEmail", None),
                            data.get("status", None),
                            data.get("latitude", None),
                            data.get("longitude", None),
                            storeOpenDate,
                            posistLiveDate,
                            data.get("seatCount", None),
                            data.get("localOrgName", None),
                            data.get("franchiseeId", None),
                            data.get("tempCloseDate", None),
                            data.get("reopenDate", None),
                            data.get("storeClosureDate", None),
                            data.get("sundayOpen", None),
                            data.get("sundayClose", None),
                            data.get("mondayOpen", None),
                            data.get("mondayClose", None),
                            data.get("tuesdayOpen", None),
                            data.get("tuesdayClose", None),
                            data.get("wednesdayOpen", None),
                            data.get("wednesdayClose", None),
                            data.get("thursdayOpen", None),
                            data.get("thursdayClose", None),
                            data.get("fridayOpen", None),
                            data.get("fridayClose", None),
                            data.get("saturdayOpen", None),
                            data.get("saturdayClose", None),
                            data.get("marketName", None),
                            data.get("areaName", None),
                            data.get("coachId", None),
                            data.get("ipRangeStart", None),
                            data.get("ipRangeEnd", None),
                            data.get("subnet", None),
                            data.get("staticIp", None),
                            data.get("linkISP", None),
                            data.get("linkType", None),
                        ),
                    )
                except Exception as e:
                    logger.error(f"Failed to insert data: {e}")
                    return json_resp(
                        {"status": "failure", "message": "Failed to Insert"}, status=400
                    )
                await conn.commit()
        return json_resp({"status": "success", "message": "Data Inserted"})

    @require_login(is_api=True)
    async def put(self, request: Request):
        data = request.form
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                        """UPDATE sites SET Store_Name = %s, Posist_Store_Name = %s,
                        Ownership_Type = %s, Local_Address = %s, City = %s, State_Name = %s,
                        Region_Internal = %s, Postal_Code = %s, Primary_Brand_Channel = %s,
                        Facility_Type = %s, Ordering_Methods = %s, Store_Type = %s, Store_Phone = %s,
                        Store_Email = %s, Status = %s, Latitude = %s, Longitude = %s, Store_Open_Date = %s,
                        posist_Live_Date = %s, Seat_Count = %s, Local_Org_Name = %s, Franchisee_id = %s,
                        Temp_Close_Date = %s, Reopen_Date = %s, Store_Closure_Date = %s, Sunday_Open = %s,
                        Sunday_Close = %s, Monday_Open = %s, Monday_Close = %s, Tuesday_Open = %s,
                        Tuesday_Close = %s, Wednesday_Open = %s, Wednesday_Close = %s, Thursday_Open = %s,
                        Thursday_Close = %s, Friday_Open = %s, Friday_Close = %s, Saturday_Open = %s,
                        Saturday_Close = %s, Market_Name = %s, Area_Name = %s, Coach_ID = %s,
                        Ip_Range_Start = %s, Ip_Range_End = %s, Subnet = %s, Static_Ip = %s, Link_ISP = %s,
                        Link_Type = %s WHERE Store_Code = %s AND Champs_Number = %s""",
                        (
                            data.get("storeName", None),
                            data.get("posistStoreName", None),
                            data.get("ownershipType", None),
                            data.get("localAddress", None),
                            data.get("city", None),
                            data.get("stateName", None),
                            data.get("regionInternal", None),
                            data.get("postalCode", None),
                            data.get("primaryBrandChannel", None),
                            data.get("facilityType", None),
                            data.get("orderingMethods", None),
                            data.get("storeType", None),
                            data.get("storePhone", None),
                            data.get("storeEmail", None),
                            data.get("status", None),
                            data.get("latitude", None),
                            data.get("longitude", None),
                            data.get("storeOpenDate", None),
                            data.get("posistLiveDate", None),
                            data.get("seatCount", None),
                            data.get("localOrgName", None),
                            data.get("franchiseeId", None),
                            data.get("tempCloseDate", None),
                            data.get("reopenDate", None),
                            data.get("storeClosureDate", None),
                            data.get("sundayOpen", None),
                            data.get("sundayClose", None),
                            data.get("mondayOpen", None),
                            data.get("mondayClose", None),
                            data.get("tuesdayOpen", None),
                            data.get("tuesdayClose", None),
                            data.get("wednesdayOpen", None),
                            data.get("wednesdayClose", None),
                            data.get("thursdayOpen", None),
                            data.get("thursdayClose", None),
                            data.get("fridayOpen", None),
                            data.get("fridayClose", None),
                            data.get("saturdayOpen", None),
                            data.get("saturdayClose", None),
                            data.get("marketName", None),
                            data.get("areaName", None),
                            data.get("coachId", None),
                            data.get("ipRangeStart", None),
                            data.get("ipRangeEnd", None),
                            data.get("subnet", None),
                            data.get("staticIp", None),
                            data.get("linkISP", None),
                            data.get("linkType", None),
                            data.get("storeCode", None),
                            data.get("champsNumber", None),
                        ),
                    )
                except Exception as e:
                    logger.error(f"Failed to update data: {e}")
                    return json_resp(
                        {"status": "failure", "message": "Failed to Update"}, status=400
                    )
                await conn.commit()
        return json_resp({"status": "success", "message": "Data Updated"})
