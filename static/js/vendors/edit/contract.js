$(document).ready(function () {
  $("#form").parsley();
  document.getElementById("form").addEventListener("submit", function (e) {
    // Log the form data
    e.preventDefault();
    handle_form_submit();
  });
  document.getElementById("addEmail").addEventListener("click", function (e) {
    const email =
      document.getElementById("emailUser").value +
      "@" +
      document.getElementById("emailDomain").value;
    addEmailToList(email);
    document.getElementById("emailUser").value = "";
    document.getElementById("emailDomain").value = "burmanhospitality.com";
  });
  document.getElementById("contract").addEventListener("change", function (e) {
    contract_id = document.getElementById("contract").value;
    load_contract_data(contract_id);
  });
  load_contracts();
});

function addEmailToList(email) {
  const emails = document.getElementById("emailList");
  const emailElement = document.createElement("div");
  emailElement.classList.add("email");
  emailElement.innerHTML = `<div class="input-group"><input class="form-control" name="emails[]" value="${email}" readonly>
      <button class="btn btn-danger" onclick="removeEmail(this)">Remove</button></div>`;
  emails.appendChild(emailElement);
}

function handle_form_submit() {
  const form = document.getElementById("form");
  const formData = new FormData(form);
  const newFormData = new FormData();
  var data = {};
  var incomplete = false;
  formData.forEach((value, key) => {
    // Ensure data is not empty
    if (!value) {
      incomplete = true;
    }
    // Check if the key is an array
    if (key.includes("[]")) {
      // Check if the key already exists in the data object
      if (data[key.replace("[]", "")]) {
        // If it does, push the value to the array
        data[key.replace("[]", "")].push(value);
      } else {
        // If it doesn't, create a new array with the value
        data[key.replace("[]", "")] = [value];
      }
    } else {
      data[key] = value;
    }
  });

  if (incomplete) {
    alert("Please fill out all fields");
    return;
  }
  // Set contractStatus based on the radio buttons
  data["contractStatus"] = document.getElementById("contractActive").checked
    ? "Active"
    : "Inactive";

  data["contractId"] = document.getElementById("contract").value;

  // Add the file
  newFormData.append("data", JSON.stringify(data));
  $.ajax({
    url: "/api/vendors/contract",
    type: "PUT",
    data: newFormData,
    contentType: false,
    processData: false,
    success: function (response) {
      console.log(response);
      if (response.status === "success") {
        window.location.href = "/vendors/contracts";
      } else {
        alert("Failed to create contract");
      }
    },
  });
}

function load_contracts() {
  var path = window.location.href.split("/");
  var vendorId = path[path.length - 1];
  document.getElementById("vendor").value = vendorId;
  $.ajax({
    url: "/api/vendors/contract",
    type: "GET",
    data: { id: vendorId, all: "true" },
    success: function (response) {
      dropdown = document.getElementById("contract");
      const schema = response.schema;
      response.data.forEach((contract) => {
        var option = document.createElement("option");
        option.value = contract[schema.indexOf("Contract_Id")];
        option.text =
          contract[schema.indexOf("Department_Code")] +
          " - " +
          contract[schema.indexOf("AMC_Start_Date")];
        dropdown.appendChild(option);
      });
      dropdown.selectedIndex = -1;
    },
  });
}

function removeEmail(element) {
  element.parentElement.remove();
}

function load_contract_data(contract_id) {
  $.ajax({
    url: "/api/vendors/contract",
    type: "GET",
    data: { id: contract_id, lookup: "contract", all: "true" },
    success: function (response) {
      console.log(response);
      // Set the form data
      const schema = response.schema;
      const data = response.data[0];
      document.getElementById("department").value =
        data[schema.indexOf("Department_Code")];
      document.getElementById("startDate").value =
        data[schema.indexOf("AMC_Start_Date")];
      document.getElementById("endDate").value =
        data[schema.indexOf("AMC_End_Date")];
      document.getElementById("contractActive").checked =
        data[schema.indexOf("Contract_Active")] === "Yes";
      document.getElementById("contractInActive").checked =
        data[schema.indexOf("Contract_Active")] != "Yes";
      document.getElementById("contractDesc").value =
        data[schema.indexOf("Contract_Description")];
      document.getElementById("frequency").value =
        data[schema.indexOf("Invoice_Frequency")];
      document.getElementById("baseCost").value =
        data[schema.indexOf("Invoice_Base_Cost")];
      document.getElementById("emailList").innerHTML = "";
      data[schema.indexOf("Reminder_Addresses")].split(",").forEach((email) => {
        addEmailToList(email);
      });
    },
  });
}
