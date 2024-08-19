$(document).ready(function () {
  // Listen to the change of the dropdown
  document.getElementById("loc-select").addEventListener("change", function () {
    load_data();
  });
  // Listen to the Get Stats button click
  document
    .getElementById("date-select")
    .addEventListener("change", function () {
      load_data();
    });
  // Get list of locations for the dropdown
  $.ajax({
    type: "GET",
    url: "/api/sites/info/",
    success: function (data) {
      load_options(data["locations"]);
    },
    error: function (data) {
      console.log(data);
    },
  });
});
function load_options(data) {
  var select = document.getElementById("loc-select");
  data.forEach((element) => {
    select.appendChild(new Option(element[0] + " - " + element[1], element[0]));
  });
  load_data();
}

function load_data() {
  var loc = document.getElementById("loc-select").value;
  if (loc == "All") {
    loc = "all";
  }
  var selected = document.getElementById("date-select").value;
  var now = new Date();
  // Switch case to get the dates based on the selected option
  switch (selected) {
    case "today":
      dateFrom = now.toISOString().split("T")[0];
      dateTo = now.toISOString().split("T")[0];
      break;
    case "yesterday":
      dateFrom = new Date(now.setDate(now.getDate() - 1))
        .toISOString()
        .split("T")[0];
      dateTo = dateFrom;
    case "this_week":
      dateFrom = new Date(now.setDate(now.getDate() - now.getDay()))
        .toISOString()
        .split("T")[0];
      dateTo = now.toISOString().split("T")[0];
    case "last_week":
      dateFrom = new Date(now.setDate(now.getDate() - now.getDay() - 7))
        .toISOString()
        .split("T")[0];
      dateTo = new Date(now.setDate(now.getDate() - now.getDay() - 1))
        .toISOString()
        .split("T")[0];
    case "this_month":
      dateFrom = new Date(now.getFullYear(), now.getMonth(), 1)
        .toISOString()
        .split("T")[0];
      dateTo = now.toISOString().split("T")[0];
    case "last_month":
      dateFrom = new Date(now.getFullYear(), now.getMonth() - 1, 1)
        .toISOString()
        .split("T")[0];
      dateTo = new Date(now.getFullYear(), now.getMonth(), 0)
        .toISOString()
        .split("T")[0];
  }

  // Send a GET request to the API with the location and dates as parameters
  $.ajax({
    type: "GET",
    url: "/api/sites/sales",
    data: {
      loc: loc,
      dateFrom: dateFrom,
      dateTo: dateTo,
    },
    success: function (data) {
      load_fields(data);
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_fields(data) {
  // Check status of the response
  if (data["status"] == "error") {
    alert(data["message"]);
    return;
  }
  order_type_data = data["data"]["type"];
  order_source_data = data["data"]["source"];
  // Check if the data is empty
  if (order_type_data.length == 0) {
    alert("No data found for the selected location and dates.");
    return;
  }
  // Set values in the fields
  $("#delivery_sales").val(order_type_data["Delivery_Total_Sales"]);
  $("#delivery_bill_count").val(order_type_data["Delivery_Bill_Count"]);
  $("#takeaway_sales").val(order_type_data["Takeaway_Total_Sales"]);
  $("#takeaway_bill_count").val(order_type_data["Takeaway_Bill_Count"]);
  $("#dinein_sales").val(order_type_data["Dinein_Total_Sales"]);
  $("#dinein_bill_count").val(order_type_data["Dinein_Bill_Count"]);
  $("#kiosk_sales").val(order_type_data["Kiosk_Total_Sales"]);
  $("#kiosk_bill_count").val(order_type_data["Kiosk_Bill_Count"]);

  $("#zomato_sales").val(order_source_data["Zomato_Total_Sales"]);
  $("#zomato_bill_count").val(order_source_data["Zomato_Bill_Count"]);
  $("#swiggy_sales").val(order_source_data["Swiggy_Total_Sales"]);
  $("#swiggy_bill_count").val(order_source_data["Swiggy_Bill_Count"]);
  $("#pos_sales").val(order_source_data["POS_Total_Sales"]);
  $("#pos_bill_count").val(order_source_data["POS_Bill_Count"]);
  $("#kiosk_sales_source").val(order_source_data["Kiosk_Total_Sales"]);
  $("#kiosk_bill_count_source").val(order_source_data["Kiosk_Bill_Count"]);
  $("#magicpin_sales").val(order_source_data["Magicpin_Total_Sales"]);
  $("#magicpin_bill_count").val(order_source_data["Magicpin_Bill_Count"]);
}
