window.onload = function () {
  // Get location from query string
  var loc = new URLSearchParams(window.location.search).get("loc");
  // Listen to the submit event of the button to get the selected location

  // Get list of locations for the dropdown
  $.ajax({
    type: "GET",
    url: "/api/lm/",
    success: function (data) {
      load_options(data["locations"]);
    },
    error: function (data) {
      console.log(data);
    },
  });

  if (loc != null) {
    // If location is not null, get location details
    process_location(loc);
  } else {
    process_location("all");
  }
};

function process_location(loc) {
  $.ajax({
    type: "GET",
    url: "/api/lm/",
    data: {
      location: loc,
    },
    success: function (data) {
      load_data_table(data);
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_options(data) {
  var select = document.getElementById("loc-select");
  data.forEach((element) => {
    select.appendChild(new Option(element[0] + " - " + element[1], element[0]));
  });
}

function load_data_table(data) {
  var tableHead = document.getElementById("table-head");
  var tableBody = document.getElementById("table-body");

  tableHead.innerHTML = "";
  tableBody.innerHTML = "";

  headerData = data["schema"];
  tableData = data["data"];

  console.log(headerData);
  console.log(tableData);

  headerData.forEach((element) => {
    var th = document.createElement("th");
    th.setAttribute("scope", "col");
    th.setAttribute("style", "width=80px");
    th.innerHTML = element.replaceAll("_", " ");
    tableHead.appendChild(th);
  });

  tableData.forEach((element) => {
    var tr = document.createElement("tr");
    element.forEach((data, index) => {
      if (index == 0) {
        var elem = document.createElement("th");
        elem.setAttribute("scope", "row");
      } else {
        var elem = document.createElement("td");
      }
      elem.innerHTML = data;
      tr.appendChild(elem);
    });
    tableBody.appendChild(tr);
  });
}
