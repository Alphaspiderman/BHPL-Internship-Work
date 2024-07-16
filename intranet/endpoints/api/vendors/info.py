from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Vendor_Info(HTTPMethodView):
    schema = [
        "Vendor_Code",
        "Vendor_Name",
        "Vendor_Address",
        "Vendor_Phone",
        "Vendor_Email",
        "PAN_Number",
        "GST_Number",
        "Account_Number",
    ]

    @require_login()
    async def get(self, request: Request):
        app: IntranetApp = request.app
        vendor_id = request.args.get("id")
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                if vendor_id in [None, ""]:
                    await cur.execute(
                        "SELECT Vendor_Code, Vendor_Name FROM vendor_info"
                    )
                    vendor_info = await cur.fetchall()
                    return json(vendor_info)
                elif vendor_id in ["all", "null"]:
                    await cur.execute("SELECT * FROM vendor_info")
                    vendor_info = await cur.fetchall()
                else:
                    await cur.execute(
                        "SELECT * FROM vendor_info WHERE Vendor_Code = %s", (vendor_id,)
                    )
                    vendor_info = await cur.fetchall()
                if vendor_info is None:
                    return json(
                        {"status": "failure", "message": "Vendor not found"}, status=404
                    )
                return json({"data": vendor_info, "schema": self.schema})

    async def post(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        data = request.json
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO vendor_info (Vendor_Code, Vendor_Name, Vendor_Address, Vendor_Phone, Vendor_Email, PAN_Number, GST_Number, Account_Number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",  # noqa: E501
                    (
                        data["vendorCode"],
                        data["vendorName"],
                        data["vendorAddress"],
                        data["vendorPhone"],
                        data["vendorEmail"],
                        data["panNumber"],
                        data["gstNumber"],
                        data["accountNumber"],
                    ),
                )
                await conn.commit()
        return json({"status": "success"})

    async def patch(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        data = request.form
        vendor_id = data.get("id")
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                        "UPDATE vendor_info SET Vendor_Name = %s, Vendor_Address = %s, Vendor_Phone = %s, Vendor_Email = %s, PAN_Number = %s, GST_Number = %s, Account_Number = %s WHERE Vendor_Code = %s",  # noqa: E501
                        (
                            data["Vendor_Name"],
                            data["Vendor_Address"],
                            data["Vendor_Phone"],
                            data["Vendor_Email"],
                            data["PAN_Number"],
                            data["GST_Number"],
                            data["Account_Number"],
                            vendor_id,
                        ),
                    )
                    await conn.commit()
                except Exception:
                    return json({"status": "failure", "message": "An Error Occoured"})
        return json({"status": "success"})
