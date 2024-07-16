$(document).ready(function () {
  var active_tab = window.location.pathname
    .replace("/vendors", "")
    .replace("/", "")
    .split("?")[0];
  switch (active_tab) {
    case "vendors":
      // Load the dropdown
      load_dropdown("vendors");
      show_vendors(null);
      break;
    case "contracts":
      // Load the dropdown
      load_dropdown("contracts");
      show_contracts(null);
      break;
    case "payments":
      // Load the dropdown
      load_dropdown("payments");
      show_payments(null);
      break;
    default:
      return;
  }
  document.getElementById("edit-btn").addEventListener("click", function () {
    window.location.href =
      window.location.pathname +
      "/edit/" +
      document.getElementById("item-select").value;
  });
  document
    .getElementById("item-select")
    .addEventListener("change", function () {
      var active_tab = window.location.pathname
        .replace("/vendors", "")
        .replace("/", "")
        .split("?")[0];
      query = document.getElementById("item-select").value;
      switch (active_tab) {
        case "vendors":
          show_vendors(query);
          break;
        case "contracts":
          show_contracts(query);
          break;
        case "payments":
          show_payments(query);
          break;
        default:
          show_vendors(null);
          break;
      }
    });
});

function load_dropdown(type) {
  btn = document.getElementById("export-btn");
  switch (type) {
    case "vendors":
      url = "/api/vendors/info";
      text_val = "Select a Vendor";
      btn.setAttribute(
        "onclick",
        "export_csv('vendors', document.getElementById('item-select').value)",
      );
      break;
    case "contracts":
      url = "/api/vendors/contract";
      text_val = "Select a Vendor Contract";
      btn.setAttribute(
        "onclick",
        "export_csv('contracts', document.getElementById('item-select').value)",
      );
      break;
    case "payments":
      url = "/api/vendors/payment";
      text_val = "Select a Vendor Payment";
      btn.setAttribute(
        "onclick",
        "export_csv('payments', document.getElementById('item-select').value)",
      );
      break;
    default:
      url = "/api/vendors/info";
      text_val = "Select a Vendor";
      btn.setAttribute(
        "onclick",
        "export_csv('vendors', document.getElementById('item-select').value)",
      );
      break;
  }
  $.ajax({
    url: url,
    type: "GET",
    success: function (response) {
      elem = document.getElementById("item-select");
      elem.innerHTML = "";
      elem.appendChild(new Option("Show All", "all"));
      response.forEach((element) => {
        if (element.length > 1) {
          elem.appendChild(
            new Option(element[0] + " - " + element[1], element[0]),
          );
        } else {
          elem.appendChild(new Option(element[0], element[0]));
        }
      });
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function render_table(data) {
  var tableHead = document.getElementById("table-head");
  var tableBody = document.getElementById("table-body");

  tableHead.innerHTML = "";
  tableBody.innerHTML = "";

  headerData = data["schema"];
  tableData = data["data"];

  headerData.forEach((element) => {
    var th = document.createElement("th");
    th.innerHTML = element.replaceAll("_", " ");
    tableHead.appendChild(th);
  });

  if (document.getElementById("item-select").value == "all") {
    document.getElementById("edit-btn").setAttribute("hidden", "");
  } else {
    document.getElementById("edit-btn").removeAttribute("hidden");
  }

  tableData.forEach((element) => {
    var tr = document.createElement("tr");
    element.forEach((ele) => {
      var td = document.createElement("td");
      td.innerHTML = ele;
      tr.appendChild(td);
    });
    tableBody.appendChild(tr);
  });
}

function show_vendors(selected_id) {
  selected_id = selected_id == null ? "all" : selected_id;
  // Get the vendor details
  $.ajax({
    url: "/api/vendors/info",
    type: "GET",
    data: {
      id: selected_id,
    },
    success: function (response) {
      render_table(response);
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function show_contracts(selected_id) {
  selected_id = selected_id == null ? "all" : selected_id;
  // Get the contract details
  $.ajax({
    url: "/api/vendors/contract",
    type: "GET",
    data: {
      id: selected_id,
    },
    success: function (response) {
      render_table(response);
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function show_payments(selected_id) {
  selected_id = selected_id == null ? "all" : selected_id;
  // Get the payment details
  $.ajax({
    url: "/api/vendors/payment",
    type: "GET",
    data: {
      id: selected_id,
    },
    success: function (response) {
      render_table(response);
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function export_csv(type, selected_id) {
  selected_id = selected_id == null ? "all" : selected_id;
  switch (type) {
    case "vendors":
      url = "/api/vendors/info";
      break;
    case "contracts":
      url = "/api/vendors/contract";
      break;
    case "payments":
      url = "/api/vendors/payment";
      break;
    default:
      url = "/api/vendors/info";
      break;
  }
  url += "?id=" + selected_id;
  url += "&export=true";
  window.open(url, "_blank");
}
