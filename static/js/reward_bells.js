$(document).ready(function () {
  // Load the available bells
  load_bells();
  // Load the location dropdown
  load_loc();
  // Listen to the change of the location dropdown
  $("#loc-select").on(
    "changed.bs.select",
    function (e, clickedIndex, isSelected, previousValue) {
      load_emp(e.target.value);
    },
  );
  // Listen to the form submission
  $("#awardBellsForm").submit(function (e) {
    e.preventDefault();
    process_submission();
  });
});

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
      // Re-render the selectpickers
      $("#loc-select").val(null);
      $("#loc-select").selectpicker("refresh");
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_emp(loc) {
  if (loc == "") {
    var select = document.getElementById("emp-select");
    select.innerHTML = "";
    select.setAttribute("disabled", "");
    return;
  }
  $.ajax({
    type: "GET",
    url: "/api/sites/employees/",
    data: {
      loc: loc,
    },
    success: function (data) {
      var select = document.getElementById("emp-select");
      select.innerHTML = "";
      data.forEach((element) => {
        select.appendChild(
          new Option(element[0] + " - " + element[1], element[0]),
        );
      });
      select.removeAttribute("disabled");
      // Destroy and re-render the selectpickers to update the options
      // Its required due to a bug in the Beta release
      // but we need the Beta for the feature to render properly
      $("#emp-select").selectpicker("destroy");
      $("#emp-select").selectpicker();
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
      if (data.Card_5_Left < 1) {
        document.getElementById("cardFive").setAttribute("disabled", "");
      }

      card_4 = document.createElement("tr");
      card_4.innerHTML =
        "<th scope='row'>4 Bells</th><td>" + data.Card_4_Left + "</td>";
      if (data.Card_4_Left < 1) {
        document.getElementById("cardFour").setAttribute("disabled", "");
      }

      card_3 = document.createElement("tr");
      card_3.innerHTML =
        "<th scope='row'>3 Bells</th><td>" + data.Card_3_Left + "</td>";
      if (data.Card_3_Left < 1) {
        document.getElementById("cardThree").setAttribute("disabled", "");
      }

      table.appendChild(card_5);
      table.appendChild(card_4);
      table.appendChild(card_3);
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function process_submission() {
  store_code = document.getElementById("loc-select").value;
  emp_code = document.getElementById("emp-select").value;
  is_5_bells = document.getElementById("cardFive").checked;
  is_4_bells = document.getElementById("cardFour").checked;
  is_3_bells = document.getElementById("cardThree").checked;
  reason = document.getElementById("reasonInput").value;

  if (store_code == "") {
    alert("Please select a location");
    return;
  }
  if (emp_code == "") {
    alert("Please select an employee");
    return;
  }
  if (reason == "") {
    alert("Please enter a reason");
    return;
  }
  if (reason.length > 250) {
    alert("Reason is too long (" + reason.length + " characters)");
    return;
  }

  let formData = new FormData();

  // Append additional data to formData
  formData.append("Store_Code", store_code);
  formData.append("Employee_Code", emp_code);
  formData.append("Award_Date", new Date().toISOString().split("T")[0]);
  formData.append("Reason", reason);
  formData.append("file", $("#fileUpload")[0].files[0]);

  if (is_5_bells) {
    formData.append("Bells_Awarded", "Card_5");
  } else if (is_4_bells) {
    formData.append("Bells_Awarded", "Card_4");
  } else if (is_3_bells) {
    formData.append("Bells_Awarded", "Card_3");
  } else {
    alert("Please select the number of bells to award");
    return;
  }

  $.ajax({
    type: "POST",
    url: "/api/bells/award",
    data: formData,
    processData: false,
    contentType: false,
    success: function (data) {
      if (data.status == "success") {
        alert(
          "Bells awarded successfully! Chart may take a few minutes to update.",
        );
        location.reload();
      } else {
        alert(data.message);
      }
    },
    error: function (data) {
      console.log(data);
    },
  });
}
