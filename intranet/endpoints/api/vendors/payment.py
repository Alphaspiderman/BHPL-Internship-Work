from datetime import datetime
from json import loads
import uuid
import aiocsv
import aiofiles
from sanic.request import Request
from sanic.log import logger
from sanic.response import json, file
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.contract_payment import ContractPayment


class Vendor_Payment(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        refernece_id = request.args.get("id")
        export = request.args.get("export")
        if export:
            export = export.lower() == "true"
        else:
            export = False

        payment_info = list()

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                if refernece_id in [None, ""]:
                    await cur.execute(
                        "SELECT Contract_Id, Vendor_Code, Department_Code, AMC_Start_Date FROM contract_payment NATURAL JOIN vendor_contract"  # noqa: E501
                    )
                    vendor_payment = await cur.fetchall()
                    vendor_payment = [list(entry) for entry in vendor_payment]
                    for entry in vendor_payment:
                        entry[-1] = entry[-1].strftime("%Y-%m-%d")
                    return json(vendor_payment)
                elif refernece_id in ["all", "null"]:
                    await cur.execute(
                        "SELECT Contract_Id, Vendor_Code, Department_Code, Invoice_Status, Due_Date, Due_Amount, Payment_Date, Payment_Amount, Invoice_Frequency FROM contract_payment NATURAL JOIN vendor_contract ORDER BY Due_Date DESC"  # noqa: E501
                    )
                    vendor_payment = await cur.fetchall()
                    payment_info = [ContractPayment(entry) for entry in vendor_payment]
                else:
                    await cur.execute(
                        "SELECT Contract_Id, Vendor_Code, Department_Code, Invoice_Status, Due_Date, Due_Amount, Payment_Date, Payment_Amount, Invoice_Frequency FROM contract_payment NATURAL JOIN vendor_contract WHERE Contract_Id = %s ORDER BY Due_Date DESC",  # noqa: E501
                        (refernece_id,),
                    )
                    vendor_payment = await cur.fetchall()
                    payment_info = [ContractPayment(entry) for entry in vendor_payment]
        data = [list(entry.get_data().values()) for entry in payment_info]
        temp_name = f"temp/{uuid.uuid4().hex}.csv"
        if export:
            async with aiofiles.open(temp_name, "w", newline="") as f:
                writer = aiocsv.AsyncWriter(f)
                await writer.writerow(payment_info[0].get_schema())
                await writer.writerows(data)
            resp = await file(temp_name, filename="vendor_payment.csv")
            await request.respond(resp)
            await aiofiles.os.remove(temp_name)
        else:
            return json({"data": data, "schema": payment_info[0].get_schema()})

    @require_login(is_api=True)
    async def put(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        form_data = request.form
        update_data = loads(form_data["data"][0])
        print(update_data)
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                        "UPDATE contract_payment SET Payment_Date = %s, Payment_Amount = %s, Invoice_Status = %s WHERE Contract_Id = %s",  # noqa: E501
                        (
                            datetime.strptime(
                                update_data["payment_date"], "%Y-%m-%d"
                            ).strftime("%Y-%m-%d"),
                            update_data["payment_amount"],
                            update_data["status"],
                            form_data["id"],
                        ),
                    )
                except Exception as e:
                    logger.error(f"Failed to Update: {e}")
                    return json({"status": "failure", "message": "Failed to Update"})
        return json({"status": "success"})
