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
        print(f"Vendor ID: {vendor_id} Type: {type(vendor_id)}")
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
