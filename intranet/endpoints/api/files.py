import aiofiles
from sanic.request import Request
from sanic.response import json, file
from sanic.views import HTTPMethodView
from sanic.log import logger

from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login


class Files(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        file_id = request.args.get("file_id")
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM files WHERE File_Id = %s", (file_id,))
                file_info = await cur.fetchall()

        if len(file_info) == 0:
            return json({"status": "failure", "message": "File not found"})
        else:
            file_to_send = file_info[0]
            file_name = file_to_send[2]
            file_mime_type = file_to_send[3]
            file_data = file_to_send[4]
            file_uploader = file_to_send[5]
            file_flag = file_to_send[6]
            # Check File's Flag
            if file_flag == "public":
                pass
            elif file_flag == "private":
                try:
                    emp_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
                except Exception:
                    return json(
                        {
                            "status": "failure",
                            "message": "You are not authorized to view this file",
                            "error": "No JWT Token",
                        }
                    )
                if emp_id != file_uploader:
                    return json(
                        {
                            "status": "failure",
                            "message": "You are not authorized to view this file",
                            "error": "Not the owner",
                        }
                    )
            elif file_flag == "dept":
                try:
                    emp_id = app.decode_jwt(request.cookies.get("JWT_TOKEN"))["emp_id"]
                except Exception:
                    return json(
                        {
                            "status": "failure",
                            "message": "You are not authorized to view this file",
                            "error": "No JWT Token",
                        }
                    )
                # Make sure both the employee and the file owner are in the same department
                async with db_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(
                            "SELECT Department FROM people WHERE Employee_Id = %s INTERSECT SELECT Department FROM people WHERE Employee_Id = %s",  # noqa: E501
                            (emp_id, file_uploader),
                        )
                        dept = await cur.fetchall()
                if len(dept) == 0:
                    return json(
                        {
                            "status": "failure",
                            "message": "You are not authorized to view this file",
                            "error": "Department Mismatch",
                        }
                    )
            # Write file to disk
            logger.debug(f"Writing file to disk: {file_name}")
            path = f"temp/{file_name}"
            async with aiofiles.open(path, "wb") as f:
                await f.write(file_data)
            logger.debug(f"File written to disk: {path}")
            resp = await file(path, filename=file_name, mime_type=file_mime_type)
            await request.respond(resp)

            # Delete file from disk
            logger.debug(f"Deleting file from disk: {path}")
            await aiofiles.os.remove(path)
