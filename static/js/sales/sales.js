$(document).ready(function () {
  // Listen to the change of the dropdown
  document.getElementById("loc-select").addEventListener("change", function () {
    load_data();
  });
  // Listen to the Get Stats button click
  document.getElementById("get-stats").addEventListener("click", function () {
    load_data();
  });
  // Dates for the date picker as start of month and today
  var today = new Date();
  var firstDay = new Date();
  firstDay.setDate(1);
  // Set the date picker values
  document.getElementById("dateFrom").valueAsDate = firstDay;
  document.getElementById("dateTo").valueAsDate = today;
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
}

function load_data() {
  var loc = document.getElementById("loc-select").value;
  if (loc == "All") {
    loc = "all";
  }
  var dateFrom = document.getElementById("dateFrom").value;
  var dateTo = document.getElementById("dateTo").value;
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
  document.getElementById("total_orders").value = data["total_orders"];
}
