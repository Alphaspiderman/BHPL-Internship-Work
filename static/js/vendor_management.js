window.onload = function () {
  var urlParams = new URLSearchParams(window.location.search);
  var active_tab = urlParams.get("show");
  var id = urlParams.get("id");
  console.log(active_tab);
  if (active_tab == "vendors") {
    show_vendors(id);
  } else if (active_tab == "contracts") {
    show_contracts(id);
  } else if (active_tab == "payments") {
    show_payments(id);
  } else {
    // Change the URL
    history.pushState("", "", "/vendors?show=vendors&id=" + id);
    // Navigate to the vendors tab
    show_vendors(id);
  }
  document
    .getElementById("show-vendors")
    .addEventListener("click", function () {
      // Change the URL
      history.pushState("", "", "/vendors?show=vendors&id=" + id);
      // Navigate to the tab
      show_vendors(id);
    });
  document
    .getElementById("show-contracts")
    .addEventListener("click", function () {
      // Change the URL
      history.pushState("", "", "/vendors?show=contracts&id=" + id);
      // Navigate to the tab
      show_contracts(id);
    });
  document
    .getElementById("contract-payments")
    .addEventListener("click", function () {
      // Change the URL
      history.pushState("", "", "/vendors?show=payments&id=" + id);
      // Navigate to the tab
      show_payments(id);
    });
};

function show_vendors(id) {
  // Clear the working body
  body = document.getElementById("working-Body");
  body.innerHTML = "";
  // Get the vendor details
  $.ajax({
    url: "/api/vendor/info",
    type: "GET",
    data: {
      id: id,
    },
    success: function (response) {
      render_vendor(response);
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function show_contracts(id) {
  // Clear the working body
  body = document.getElementById("working-Body");
  body.innerHTML = "";
  // Get the contract details
  $.ajax({
    url: "/api/vendor/contract",
    type: "GET",
    data: {
      id: id,
    },
    success: function (response) {
      render_contarct(response);
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function show_payments(id) {
  // Clear the working body
  body = document.getElementById("working-Body");
  body.innerHTML = "";
  // Get the payment details
  $.ajax({
    url: "/api/vendor/payment",
    type: "GET",
    data: {
      id: id,
    },
    success: function (response) {
      render_payment(response);
    },
    error: function (response) {
      console.log(response);
    },
  });
}

function render_contarct(data) {}

function render_payment(data) {}

function render_vendor(data) {}
