from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.log import logger
from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from datetime import datetime


class Location_Sales(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        # Check for location
        location = request.args.get("loc")
        if not location:
            return json({"status": "error", "message": "Location not provided"})

        # Check for date range
        date_from = request.args.get("from")
        date_to = request.args.get("to")

        # Default date range
        if not date_from:
            # Start of Month
            date_from = datetime.now().replace(day=1).strftime("%Y-%m-%d")

        if not date_to:
            # End of Month
            date_to = (
                datetime.now()
                .replace(day=1, month=datetime.now().month + 1)
                .strftime("%Y-%m-%d")
            )

        # Check if the date range is valid
        try:
            d_from = datetime.strptime(date_from, "%Y-%m-%d")
            d_to = datetime.strptime(date_to, "%Y-%m-%d")
            assert d_from < d_to
        except ValueError:
            return json({"status": "error", "message": "Invalid Date Range (Parse)"})
        except AssertionError:
            return json(
                {"status": "error", "message": "Invalid Date Range (from > to)"}
            )

        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Get the data related to Source
                await cur.execute(
                    "SELECT * FROM order_source_data WHERE Store_Id = %s AND Date BETWEEN %s AND %s",
                    (location, date_from, date_to),
                )
                source_data = await cur.fetchall()
                # Get the data related to Type
                await cur.execute(
                    "SELECT * FROM order_type_data WHERE Store_Id = %s AND Date BETWEEN %s AND %s",
                    (location, date_from, date_to),
                )
                type_data = await cur.fetchall()
        return json(
            {"status": "success", "data": {"source": source_data, "type": type_data}}
        )

    @require_login(is_api=True)
    async def post(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        data = request.json

        store_code = data["Store_Id"]
        date = data["Date"]
        order_type_data = data["Order_Type_Data"]
        order_source_data = data["Order_Source_Data"]

        try:
            # Ensure that all the keys are present
            assert set(order_type_data.keys()) == {
                "Delivery_Total_Sales",
                "Delivery_Bill_Count",
                "Takeaway_Total_Sales",
                "Takeaway_Bill_Count",
                "Dinein_Total_Sales",
                "Dinein_Bill_Count",
                "Kiosk_Total_Sales",
                "Kiosk_Bill_Count",
            }
            assert set(order_source_data.keys()) == {
                "Zomato_Total_Sales",
                "Zomato_Bill_Count",
                "Swiggy_Total_Sales",
                "Swiggy_Bill_Count",
                "POS_Total_Sales",
                "POS_Bill_Count",
                "Kiosk_Total_Sales",
                "Kiosk_Bill_Count",
                "Magicpin_Total_Sales",
                "Magicpin_Bill_Count",
            }

            # Ensure that all the values are of the correct type
            assert isinstance(order_type_data["Delivery_Total_Sales"], float)
            assert isinstance(order_type_data["Delivery_Bill_Count"], int)
            assert isinstance(order_type_data["Takeaway_Total_Sales"], float)
            assert isinstance(order_type_data["Takeaway_Bill_Count"], int)
            assert isinstance(order_type_data["Dinein_Total_Sales"], float)
            assert isinstance(order_type_data["Dinein_Bill_Count"], int)
            assert isinstance(order_type_data["Kiosk_Total_Sales"], float)
            assert isinstance(order_type_data["Kiosk_Bill_Count"], int)

            assert isinstance(order_source_data["Zomato_Total_Sales"], float)
            assert isinstance(order_source_data["Zomato_Bill_Count"], int)
            assert isinstance(order_source_data["Swiggy_Total_Sales"], float)
            assert isinstance(order_source_data["Swiggy_Bill_Count"], int)
            assert isinstance(order_source_data["POS_Total_Sales"], float)
            assert isinstance(order_source_data["POS_Bill_Count"], int)
            assert isinstance(order_source_data["Kiosk_Total_Sales"], float)
            assert isinstance(order_source_data["Kiosk_Bill_Count"], int)
            assert isinstance(order_source_data["Magicpin_Total_Sales"], float)
            assert isinstance(order_source_data["Magicpin_Bill_Count"], int)

        except AssertionError as e:
            logger.error("API Failed to Validate the data", exc_info=e)
            return json(
                {"status": "error", "message": "API Failed to Validate the data"}
            )

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO order_type_data (Store_Id, Date, Delivery_Total_Sales, Delivery_Bill_Count, Takeaway_Total_Sales, Takeaway_Bill_Count, Dinein_Total_Sales, Dinein_Bill_Count, Kiosk_Total_Sales, Kiosk_Bill_Count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  # noqa: E501
                    (
                        store_code,
                        date,
                        order_type_data["Delivery_Total_Sales"],
                        order_type_data["Delivery_Bill_Count"],
                        order_type_data["Takeaway_Total_Sales"],
                        order_type_data["Takeaway_Bill_Count"],
                        order_type_data["Dinein_Total_Sales"],
                        order_type_data["Dinein_Bill_Count"],
                        order_type_data["Kiosk_Total_Sales"],
                        order_type_data["Kiosk_Bill_Count"],
                    ),
                )
                await cur.execute(
                    "INSERT INTO order_source_data (Store_Id, Date, Zomato_Total_Sales, Zomato_Bill_Count, Swiggy_Total_Sales, Swiggy_Bill_Count, POS_Total_Sales, POS_Bill_Count, Kiosk_Total_Sales, Kiosk_Bill_Count, Magicpin_Total_Sales, Magicpin_Bill_Count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  # noqa: E501
                    (
                        store_code,
                        date,
                        order_source_data["Zomato_Total_Sales"],
                        order_source_data["Zomato_Bill_Count"],
                        order_source_data["Swiggy_Total_Sales"],
                        order_source_data["Swiggy_Bill_Count"],
                        order_source_data["POS_Total_Sales"],
                        order_source_data["POS_Bill_Count"],
                        order_source_data["Kiosk_Total_Sales"],
                        order_source_data["Kiosk_Bill_Count"],
                        order_source_data["Magicpin_Total_Sales"],
                        order_source_data["Magicpin_Bill_Count"],
                    ),
                )

        return json({"status": "success"})
