$(document).ready(function () {
  $("#form").parsley();
  // Listen to form submission
  $("#form").submit(function (e) {
    e.preventDefault();
    handle_form_submit();
  });
  // Listen to Kiosk Total Sales change and set it to Kiosk Total Sales Source
  $("#kiosk_sales").change(function () {
    $("#kiosk_sales_source").val($("#kiosk_sales").val());
  });
  // Listen to Kiosk Bill Count change and set it to Kiosk Bill Count Source
  $("#kiosk_bill_count").change(function () {
    $("#kiosk_bill_count_source").val($("#kiosk_bill_count").val());
  });
  // Default date to today
  $("#date").val(new Date().toISOString().split("T")[0]);
});

function handle_form_submit() {
  var form = $("#form");
  // Check if form is valid
  if (!form.parsley().isValid()) {
    return;
  }

  var data = {
    Store_Id: $("#store_id").val(),
    Date: $("#date").val(),
  };

  // Add Order_Type_Data to data
  var order_type_data = {};
  order_type_data["Delivery_Total_Sales"] = $("#delivery_sales").val();
  order_type_data["Delivery_Bill_Count"] = $("#delivery_bill_count").val();
  order_type_data["Takeaway_Total_Sales"] = $("#takeaway_sales").val();
  order_type_data["Takeaway_Bill_Count"] = $("#takeaway_bill_count").val();
  order_type_data["Dinein_Total_Sales"] = $("#dinein_sales").val();
  order_type_data["Dinein_Bill_Count"] = $("#dinein_bill_count").val();
  order_type_data["Kiosk_Total_Sales"] = $("#kiosk_sales").val();
  order_type_data["Kiosk_Bill_Count"] = $("#kiosk_bill_count").val();

  console.log(order_type_data);

  // Add order_source_data to data
  var order_source_data = {};
  order_source_data["Zomato_Total_Sales"] = $("#zomato_sales").val();
  order_source_data["Zomato_Bill_Count"] = $("#zomato_bill_count").val();
  order_source_data["Swiggy_Total_Sales"] = $("#swiggy_sales").val();
  order_source_data["Swiggy_Bill_Count"] = $("#swiggy_bill_count").val();
  order_source_data["POS_Total_Sales"] = $("#pos_sales").val();
  order_source_data["POS_Bill_Count"] = $("#pos_bill_count").val();
  order_source_data["Kiosk_Total_Sales"] = $("#kiosk_sales").val();
  order_source_data["Kiosk_Bill_Count"] = $("#kiosk_bill_count").val();
  order_source_data["Magicpin_Total_Sales"] = $("#magicpin_sales").val();
  order_source_data["Magicpin_Bill_Count"] = $("#magicpin_bill_count").val();

  console.log(order_source_data);

  data["Order_Type_Data"] = order_type_data;
  data["Order_Source_Data"] = order_source_data;

  console.log(data);

  var form_data = new FormData();
  form_data.append("data", JSON.stringify(data));

  $.ajax({
    url: "/api/sites/sales",
    method: "POST",
    data: form_data,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response["status"] == "success") {
        // Show success message
        show_message(true, response["message"]);
        // Clear form
        form.trigger("reset");
      } else {
        // Show error message
        show_message(false, response["message"]);
      }
    },
    error: function (response) {
      show_message(false, "An error occurred");
    },
  });
}
function show_message(success, message) {
  prefix = success ? "Success!" : "Error!";
  // Show an alert
  window.alert(prefix + " " + message);
}
