$(document).ready(function () {
  $("#form").parsley();
  load_expenses();
  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
    handle_submit();
  });
});

function handle_submit() {
  // Ensure there is a date
  if (document.getElementById("date").value == "") {
    alert("Please enter a date");
    return;
  }

  // Ensure there is a location
  if (document.getElementById("location").value == "") {
    alert("Please enter a location");
    return;
  }

  // Ensure there is a reason
  if (document.getElementById("reason").value == "") {
    alert("Please enter a reason");
    return;
  }

  var data = {
    Date_Of_Expense: document.getElementById("date").value,
    Location: document.getElementById("location").value,
    Stationary: document.getElementById("office_stationary").value,
    Hotel_Rent: document.getElementById("hotel_rent").value,
    Connectivity_Charges: document.getElementById("connectivity_charges").value,
    Travel_Charge: document.getElementById("cab_cost").value,
    Others: document.getElementById("misc_expenses").value,
    Reason: document.getElementById("reason").value,
  };
  meal_cost = document.getElementById("meal_cost").value;
  meal_type = document.getElementById("meal_type").value;
  switch (meal_type) {
    case "welfare":
      data.Welfare_Meal = meal_cost;
      data.Promotion_Meal = 0.0;
    case "promotion":
      data.Welfare_Meal = 0.0;
      data.Promotion_Meal = meal_cost;
  }

  distance_travelled = document.getElementById("distance_travelled").value;
  vehicle_type = document.getElementById("vehicle_type").value;
  switch (vehicle_type) {
    case "car":
      data.Vehicle_Type = "Car";
    case "bike":
      data.Vehicle_Type = "Bike";
  }

  formdata = new FormData();

  // Remove empty fields
  for (var key in data) {
    if (data[key] == "" || data[key] == "0.00" || data[key] == "0") {
      delete data[key];
    }
  }

  // Get file
  var file = document.getElementById("formFile").files[0];

  // Add file to formdata
  formdata.append("file", file);

  // Add data to formdata
  formdata.append("data", JSON.stringify(data));

  // Send data to server
  $.ajax({
    type: "POST",
    url: "/api/expenses/me",
    data: formdata,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response.status == "success") {
        alert("Expense added successfully");
        window.location.reload();
      } else {
        alert("Failed to add expense");
      }
    },
  });
}

function load_expenses() {
  $.ajax({
    type: "GET",
    url: "/api/expenses/me?by_doc_date=true",
    success: function (response) {
      const data = response.data;
      const table = document.getElementById("loggedTodayTableBody");

      if (data.length == 0) {
        document.getElementById("loggedTodayTitle").setAttribute("hidden", "");
        document.getElementById("loggedTodayTable").setAttribute("hidden", "");
        return;
      }
      data.forEach((element) => {
        row = table.insertRow();
        row.insertCell().textContent = element[0];
        row.insertCell().textContent = element[1];
        row.insertCell().textContent = element[2];
        row.insertCell().textContent = element[3];
        row.insertCell().textContent = element[4];
        row.insertCell().textContent = element[5];
        row.insertCell().textContent = element[6];
        row.insertCell().textContent = element[7];
        row.insertCell().textContent = element[8];
        row.insertCell().textContent = element[11];
        row.insertCell().textContent = element[10];
        row.insertCell().textContent = element[12];
        row.insertCell().textContent = element[9];
      });
    },
  });
}