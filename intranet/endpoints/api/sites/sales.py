from json import loads
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.log import logger
from intranet.app import IntranetApp
from intranet.decorators.require_login import require_login
from datetime import datetime
from pymysql.err import IntegrityError


class Location_Sales(HTTPMethodView):
    @require_login(is_api=True)
    async def get(self, request: Request):
        # Check for location
        location = request.args.get("loc")
        if not location:
            return json({"status": "error", "message": "Location not provided"})

        # Check for date range
        date_from = request.args.get("dateFrom")
        date_to = request.args.get("dateTo")

        # Check if display is for graph
        graph = request.args.get("graph")
        if graph:
            graph = graph.lower() == "true"

        if location == "all":
            store_filter = ""
            args = (date_from, date_to)
        else:
            store_filter = "Store_Id = %s AND"
            args = (location, date_from, date_to)

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
            assert d_from <= d_to
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
                    f"SELECT * FROM order_source_data WHERE {store_filter} Date BETWEEN %s AND %s",
                    args,
                )
                source_data = await cur.fetchall()
                # Get the data related to Type
                await cur.execute(
                    f"SELECT * FROM order_type_data WHERE {store_filter} Date BETWEEN %s AND %s",
                    args,
                )
                type_data = await cur.fetchall()
        # Convert data types
        source_data = [
            {
                "Store_Id": row[0],
                "Date": row[1].strftime("%Y-%m-%d"),
                "Zomato_Total_Sales": float(row[2]),
                "Zomato_Bill_Count": row[3],
                "Swiggy_Total_Sales": float(row[4]),
                "Swiggy_Bill_Count": row[5],
                "POS_Total_Sales": float(row[6]),
                "POS_Bill_Count": row[7],
                "Kiosk_Total_Sales": float(row[8]),
                "Kiosk_Bill_Count": row[9],
                "Magicpin_Total_Sales": float(row[10]),
                "Magicpin_Bill_Count": row[11],
            }
            for row in source_data
        ]

        type_data = [
            {
                "Store_Id": row[0],
                "Date": row[1].strftime("%Y-%m-%d"),
                "Delivery_Total_Sales": float(row[2]),
                "Delivery_Bill_Count": row[3],
                "Takeaway_Total_Sales": float(row[4]),
                "Takeaway_Bill_Count": row[5],
                "Dinein_Total_Sales": float(row[6]),
                "Dinein_Bill_Count": row[7],
                "Kiosk_Total_Sales": float(row[8]),
                "Kiosk_Bill_Count": row[9],
            }
            for row in type_data
        ]

        # If the data is for graph, return the raw data
        if graph:
            return json(
                {
                    "status": "success",
                    "data": {"source": source_data, "type": type_data},
                }
            )
        # Sum up the values
        source_totals = {
            "Zomato_Total_Sales": sum(row["Zomato_Total_Sales"] for row in source_data),
            "Swiggy_Total_Sales": sum(row["Swiggy_Total_Sales"] for row in source_data),
            "POS_Total_Sales": sum(row["POS_Total_Sales"] for row in source_data),
            "Kiosk_Total_Sales": sum(row["Kiosk_Total_Sales"] for row in source_data),
            "Magicpin_Total_Sales": sum(
                row["Magicpin_Total_Sales"] for row in source_data
            ),
            "Zomato_Bill_Count": sum(row["Zomato_Bill_Count"] for row in source_data),
            "Swiggy_Bill_Count": sum(row["Swiggy_Bill_Count"] for row in source_data),
            "POS_Bill_Count": sum(row["POS_Bill_Count"] for row in source_data),
            "Kiosk_Bill_Count": sum(row["Kiosk_Bill_Count"] for row in source_data),
            "Magicpin_Bill_Count": sum(
                row["Magicpin_Bill_Count"] for row in source_data
            ),
        }

        type_totals = {
            "Delivery_Total_Sales": sum(
                row["Delivery_Total_Sales"] for row in type_data
            ),
            "Takeaway_Total_Sales": sum(
                row["Takeaway_Total_Sales"] for row in type_data
            ),
            "Dinein_Total_Sales": sum(row["Dinein_Total_Sales"] for row in type_data),
            "Kiosk_Total_Sales": sum(row["Kiosk_Total_Sales"] for row in type_data),
            "Delivery_Bill_Count": sum(row["Delivery_Bill_Count"] for row in type_data),
            "Takeaway_Bill_Count": sum(row["Takeaway_Bill_Count"] for row in type_data),
            "Dinein_Bill_Count": sum(row["Dinein_Bill_Count"] for row in type_data),
            "Kiosk_Bill_Count": sum(row["Kiosk_Bill_Count"] for row in type_data),
        }

        return json(
            {
                "status": "success",
                "data": {"source": source_totals, "type": type_totals},
            }
        )

    @require_login(is_api=True)
    async def post(self, request: Request):
        app: IntranetApp = request.app
        db_pool = app.get_db_pool()
        data = loads(request.form.get("data"))
        store_code = data["Store_Id"]
        date = data["Date"]
        order_type_data = data["Order_Type_Data"].copy()
        order_source_data = data["Order_Source_Data"].copy()

        # Convert the date to the correct format
        date = datetime.strptime(date, "%Y-%m-%d")

        for key in order_type_data.keys():
            order_type_data[key] = float(order_type_data[key])
        for key in order_source_data.keys():
            order_source_data[key] = float(order_source_data[key])

        try:
            # Ensure that all the keys are present
            assert order_type_data.keys() == set(
                [
                    "Delivery_Total_Sales",
                    "Delivery_Bill_Count",
                    "Takeaway_Total_Sales",
                    "Takeaway_Bill_Count",
                    "Dinein_Total_Sales",
                    "Dinein_Bill_Count",
                    "Kiosk_Total_Sales",
                    "Kiosk_Bill_Count",
                ]
            )
            assert order_source_data.keys() == set(
                [
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
                ]
            )

            # Ensure that all the values are of the correct type
            assert isinstance(order_type_data["Delivery_Total_Sales"], float)
            assert isinstance(order_type_data["Delivery_Bill_Count"], float)
            assert isinstance(order_type_data["Takeaway_Total_Sales"], float)
            assert isinstance(order_type_data["Takeaway_Bill_Count"], float)
            assert isinstance(order_type_data["Dinein_Total_Sales"], float)
            assert isinstance(order_type_data["Dinein_Bill_Count"], float)
            assert isinstance(order_type_data["Kiosk_Total_Sales"], float)
            assert isinstance(order_type_data["Kiosk_Bill_Count"], float)

            assert isinstance(order_source_data["Zomato_Total_Sales"], float)
            assert isinstance(order_source_data["Zomato_Bill_Count"], float)
            assert isinstance(order_source_data["Swiggy_Total_Sales"], float)
            assert isinstance(order_source_data["Swiggy_Bill_Count"], float)
            assert isinstance(order_source_data["POS_Total_Sales"], float)
            assert isinstance(order_source_data["POS_Bill_Count"], float)
            assert isinstance(order_source_data["Kiosk_Total_Sales"], float)
            assert isinstance(order_source_data["Kiosk_Bill_Count"], float)
            assert isinstance(order_source_data["Magicpin_Total_Sales"], float)
            assert isinstance(order_source_data["Magicpin_Bill_Count"], float)

            # Check that Store_Id is a string and non-empty
            assert isinstance(store_code, str)
            assert store_code != ""

            # Check that Date not in the future
            assert date <= datetime.now()
        except AssertionError as e:
            logger.error("API Failed to Validate the data", exc_info=e)
            return json(
                {"status": "error", "message": "Backend Failed to Validate the data"}
            )

        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
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
                except IntegrityError as e:
                    logger.error("Integrity Erroe", exc_info=e)
                    return json(
                        {
                            "status": "error",
                            "message": "Data already exists for the given date",
                        }
                    )

        return json({"status": "success"})
