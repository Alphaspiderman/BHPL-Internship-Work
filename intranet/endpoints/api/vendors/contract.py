import uuid
import aiocsv
import aiofiles
from json import loads, dumps
from sanic.request import Request
from sanic.response import json, file
from sanic.views import HTTPMethodView

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from intranet.models.vendor_contract import VendorContract


class Vendor_Contract(HTTPMethodView):
    @require_login()
    async def get(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        reference_id = request.args.get("id")
        export = request.args.get("export")
        if request.args.get("lookup"):
            lookup = request.args.get("lookup").lower() == "contract"
        else:
            lookup = False
        if request.args.get("all"):
            show_all = request.args.get("all").lower() == "true"
        else:
            show_all = False
        if export:
            export = export.lower() == "true"
        else:
            export = False

        contact_info = list()

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                if reference_id in [None, ""]:
                    await cur.execute(
                        "SELECT DISTINCT Vendor_Code FROM vendor_contract"
                    )
                    vendor_contract = await cur.fetchall()
                    return json(vendor_contract)
                elif reference_id in ["all", "null"]:
                    await cur.execute(
                        "SELECT * FROM vendor_contract ORDER BY AMC_Start_Date DESC"
                    )
                    vendor_contract = await cur.fetchall()
                    contact_info = [VendorContract(entry) for entry in vendor_contract]
                else:
                    if lookup:
                        await cur.execute(
                            "SELECT * FROM vendor_contract WHERE Contract_Id = %s",
                            (reference_id,),
                        )
                    else:
                        await cur.execute(
                            "SELECT * FROM vendor_contract WHERE Vendor_Code = %s ORDER BY AMC_Start_Date DESC",  # noqa: E501
                            (reference_id,),
                        )
                    vendor_contract = await cur.fetchall()
                    contact_info = [VendorContract(entry) for entry in vendor_contract]
        data = [
            list(entry.get_data(show_all=show_all).values()) for entry in contact_info
        ]
        temp_name = f"temp/{uuid.uuid4().hex}.csv"
        if export:
            async with aiofiles.open(temp_name, "w", newline="") as f:
                writer = aiocsv.AsyncWriter(f)
                await writer.writerow(contact_info[0].get_schema(show_all=show_all))
                await writer.writerows(data)
            resp = await file(temp_name, filename="vendor_contract.csv")
            await request.respond(resp)
            await aiofiles.os.remove(temp_name)
        else:
            return json(
                {
                    "data": data,
                    "schema": contact_info[0].get_schema(show_all=show_all),
                }
            )

    async def post(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()

        emp_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
        # Extract the data from the request
        data = loads(request.form.get("data"))
        file = request.files.get("file")
        # Extract the data form the form
        Vendor_Code = data.get("vendor")
        Department = data.get("department")
        contract_status = data.get("contractStatus")
        AMC_Start_Date = data.get("startDate")
        AMC_End_Date = data.get("endDate")
        AMC_Amount = data.get("baseCost")
        Frequency = data.get("frequency")
        Contract_Desc = data.get("contractDesc")
        Emails = data.get("emails")

        # Transform Contract Status
        if not contract_status or len(contract_status) == 0:
            contract_status = None
        else:
            contract_status = 1

        # Save the data
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    # Insert file
                    file_name = f"{uuid.uuid4().hex}.{file.name.split('.')[-1]}"
                    await cur.execute(
                        "INSERT INTO files (File_Id, File_Name, File_Type, File_Data, Uploaded_By, File_Flag) VALUES (%s, %s, %s, %s, %s, %s)",  # noqa: E501
                        (file_name, file.name, file.type, file.body, emp_id, "Public"),
                    )

                    await cur.execute(
                        "INSERT INTO vendor_contract (Contract_Id, Vendor_Code, Department_Code, Contract_Active, Contract_Description, AMC_Start_Date, AMC_End_Date, File_Name, Invoice_Frequency, Invoice_Base_Cost, Reminder_Addresses) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",  # noqa: E501
                        (
                            str(uuid.uuid4().hex),
                            Vendor_Code,
                            Department,
                            contract_status,
                            Contract_Desc,
                            AMC_Start_Date,
                            AMC_End_Date,
                            file_name,
                            Frequency,
                            AMC_Amount,
                            dumps(Emails),
                        ),
                    )
                    await conn.commit()
                except Exception:
                    await conn.rollback()
                    return json({"status": "failed"})
        return json({"status": "success"})

    async def patch(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        # Extract the data from the request
        data = loads(request.form.get("data"))
        # Extract the data form the form
        contract_id = data.get("contractId")
        Vendor_Code = data.get("vendor")
        Department = data.get("department")
        contract_status = data.get("contractStatus")
        AMC_Start_Date = data.get("startDate")
        AMC_End_Date = data.get("endDate")
        AMC_Amount = data.get("baseCost")
        Frequency = data.get("frequency")
        Contract_Desc = data.get("contractDesc")
        Emails = data.get("emails")

        # Transform Contract Status
        if not contract_status or len(contract_status) == 0:
            contract_status = None
        else:
            contract_status = 1

        # Save the data
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(
                        "UPDATE vendor_contract SET Vendor_Code = %s, Department_Code = %s, Contract_Active = %s, Contract_Description = %s, AMC_Start_Date = %s, AMC_End_Date = %s, Invoice_Frequency = %s, Invoice_Base_Cost = %s, Reminder_Addresses = %s WHERE Contract_Id = %s",  # noqa: E501
                        (
                            Vendor_Code,
                            Department,
                            contract_status,
                            Contract_Desc,
                            AMC_Start_Date,
                            AMC_End_Date,
                            Frequency,
                            AMC_Amount,
                            dumps(Emails),
                            contract_id,
                        ),
                    )
                    await conn.commit()
                except Exception:
                    await conn.rollback()
                    return json({"status": "failed"})
        return json({"status": "success"})
