$(document).ready(function () {
  // Listen to the change of the dropdown
  document.getElementById("loc-select").addEventListener("change", function () {
    load_data();
  });
  // Listen to the Get Stats button click
  document.getElementById("get-stats").addEventListener("click", function () {
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
}

function load_data() {
  var loc = document.getElementById("loc-select").value;
  if (loc == "All") {
    loc = "all";
  }
  var dateFrom = document.getElementById("dateFrom").value;
  // Send a GET request to the API with the location and dates as parameters
  $.ajax({
    type: "GET",
    url: "/api/sites/missing",
    data: {
      loc: loc,
      from: dateFrom,
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
  if (data["status"] == "error") {
    alert(data["message"]);
    return;
  }
  // Clear the table
  $("#table-body").empty();
  // Add the rows
  data["data"].forEach((element) => {
    console.log(element);
    $("#table-body").append(
      "<tr><td>" +
        element["store_id"] +
        "</td><td>" +
        element["store_code"] +
        "</td><td>" +
        element["store_name"] +
        "</td><td>" +
        element["date"] +
        "</td></tr>",
    );
  });
}
