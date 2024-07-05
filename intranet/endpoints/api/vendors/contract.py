from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.vendor_contract import VendorContract

class Vendor_Contract(HTTPMethodView):

    @require_login()
    async def get(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        contract_id = request.args.get("id")

        contact_info = list()

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                if contract_id in [None, ""]:
                    await cur.execute(
                        "SELECT DISTINCT Vendor_Code FROM vendor_contract"
                    )
                    vendor_contract = await cur.fetchall()
                    return json(vendor_contract)
                elif contract_id in ["all", "null"]:
                    await cur.execute("SELECT * FROM vendor_contract ORDER BY AMC_Start_Date DESC")
                    vendor_contract = await cur.fetchall()
                    contact_info = [VendorContract(entry) for entry in vendor_contract]
                else:
                    await cur.execute(
                        "SELECT * FROM vendor_contract WHERE Vendor_Code = %s ORDER BY AMC_Start_Date DESC",
                        (contract_id,),
                    )
                    vendor_contract = await cur.fetchall()
                    contact_info = [VendorContract(entry) for entry in vendor_contract]
        data = [list(entry.get_data().values()) for entry in contact_info]
        return json({"data": data, "schema": contact_info[0].get_schema()})
