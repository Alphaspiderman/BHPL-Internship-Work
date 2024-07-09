from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.contract_payment import ContractPayment


class Vendor_Payment(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        vendor_code = request.args.get("id")

        payment_info = list()

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                if vendor_code in [None, ""]:
                    await cur.execute(
                        "SELECT DISTINCT Vendor_Code FROM contract_payment"
                    )
                    vendor_payment = await cur.fetchall()
                    return json(vendor_payment)
                elif vendor_code in ["all", "null"]:
                    await cur.execute(
                        "SELECT * FROM contract_payment ORDER BY Due_Date DESC"
                    )
                    vendor_payment = await cur.fetchall()
                    payment_info = [ContractPayment(entry) for entry in vendor_payment]
                else:
                    await cur.execute(
                        "SELECT * FROM contract_payment WHERE Vendor_Code = %s ORDER BY Due_Date DESC",
                        (vendor_code,),
                    )
                    vendor_payment = await cur.fetchall()
                    payment_info = [ContractPayment(entry) for entry in vendor_payment]
        data = [list(entry.get_data().values()) for entry in payment_info]
        return json({"data": data, "schema": payment_info[0].get_schema()})
