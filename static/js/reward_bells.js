window.onload = function () {
  // Load the available bells
  load_bells();
  // Load the location dropdown
  load_loc();
  // Listen to the change of the location dropdown
  document.getElementById("loc-select").addEventListener("change", function () {
    var loc = document.getElementById("loc-select").value;
    load_emp(loc);
  });
};

function load_loc() {
  $.ajax({
    type: "GET",
    url: "/api/sites/info/",
    success: function (data) {
      var select = document.getElementById("loc-select");
      data.locations.forEach((element) => {
        select.appendChild(
          new Option(element[0] + " - " + element[1], element[0]),
        );
      });
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_emp() {
  var loc = document.getElementById("loc-select").value;
  if (loc == "") {
    var select = document.getElementById("emp-select");
    select.innerHTML = "";
    select.appendChild(new Option("Please select a location", ""));
    select.setAttribute("disabled");
    return;
  }
  $.ajax({
    type: "GET",
    url: "/api/sites/employees/",
    data: {
      loc: loc,
    },
    success: function (data) {
      console.log(data);
      var select = document.getElementById("emp-select");
      select.innerHTML = "";
      data.forEach((element) => {
        select.appendChild(
          new Option(element[0] + " - " + element[1], element[0]),
        );
      });
      select.removeAttribute("disabled");
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_bells() {
  $.ajax({
    type: "GET",
    url: "/api/bells/award",
    success: function (data) {
      if (data.status == "failure") {
        alert(data.message);
        window.location.href = "/home";
        return;
      }
      var table = document.getElementById("bell-table");
      card_5 = document.createElement("tr");
      card_5.innerHTML =
        "<th scope='row'>5 Bells</th><td>" + data.Card_5_Left + "</td>";

      card_4 = document.createElement("tr");
      card_4.innerHTML =
        "<th scope='row'>4 Bells</th><td>" + data.Card_4_Left + "</td>";

      card_3 = document.createElement("tr");
      card_3.innerHTML =
        "<th scope='row'>3 Bells</th><td>" + data.Card_3_Left + "</td>";

      table.appendChild(card_5);
      table.appendChild(card_4);
      table.appendChild(card_3);
    },
    error: function (data) {
      console.log(data);
    },
  });
}
