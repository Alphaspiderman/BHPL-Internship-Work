$(document).ready(function () {
  // Listen to the change of the dropdown
  document.getElementById("loc-select").addEventListener("change", function () {
    load_data();
  });
  // Listen to the Get Stats button click
  document.getElementById("get-stats").addEventListener("click", function () {
    load_data();
  });
  // Listen to the date picker change
  document.getElementById("dateFrom").addEventListener("change", function () {
    load_data();
  });
  document.getElementById("dateTo").addEventListener("change", function () {
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
  // Load the data for the first time
  load_data();
});
function load_options(data) {
  var select = document.getElementById("loc-select");
  data.forEach((element) => {
    select.appendChild(new Option(element[0] + " - " + element[1], element[0]));
  });
}

function load_data() {
  var loc = document.getElementById("loc-select").value;
  var dateFrom = document.getElementById("dateFrom").value;
  var dateTo = document.getElementById("dateTo").value;
  $.ajax({
    type: "GET",
    url: "/api/sites/downtime/",
    data: {
      loc: loc,
      dateFrom: dateFrom,
      dateTo: dateTo,
    },
    success: function (data) {
      load_table(data);
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_table(data) {
  table_body = document.getElementById("downtime-stats");
  // Clear the table
  table_body.innerHTML = "";
  // Add the new data
  entries = data.data;
  var now = new Date();
  entries.forEach((element) => {
    var startTime = new Date(element["startTime"]);
    // var endTime = new Date(element["endTime"]);
    var endTime = element["endTime"] ? new Date(element["endTime"]) : "Ongoing";
    var duration =
      (element["endTime"] ? new Date(element["endTime"]) : now) -
      new Date(element["startTime"]);
    var row = table_body.insertRow();
    var cell = row.insertCell();
    cell.innerHTML = element["champsNumber"];
    var cell = row.insertCell();
    cell.innerHTML = startTime;
    var cell = row.insertCell();
    cell.innerHTML = endTime;
    var cell = row.insertCell();
    cell.innerHTML = convert_duration(duration);
  });
}

function convert_duration(duration) {
  var hours = Math.floor(duration / 3600000);
  var minutes = Math.floor((duration % 3600000) / 60000);
  var seconds = Math.floor((duration % 60000) / 1000);
  return hours + "h " + minutes + "m " + seconds + "s";
}
