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
    const emails = document.getElementById("emailList");
    const emailElement = document.createElement("div");
    emailElement.classList.add("email");
    emailElement.innerHTML = `<div class="input-group"><input class="form-control" name="emails[]" value="${email}" readonly>
    <button class="btn btn-danger" onclick="removeEmail(this)">Remove</button></div>`;
    emails.appendChild(emailElement);
    document.getElementById("emailUser").value = "";
    document.getElementById("emailDomain").value = "burmanhospitality.com";
  });
  load_dropdowns();
});

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

  // Add the file
  newFormData.append("file", document.getElementById("formFile").files[0]);
  newFormData.append("data", JSON.stringify(data));
  $.ajax({
    url: "/api/vendors/contract",
    type: "POST",
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

function load_dropdowns() {
  const vendorDrop = document.getElementById("vendor");
  const departmentDrop = document.getElementById("department");
  // Get all vendors
  $.ajax({
    url: "/api/vendors/info",
    type: "GET",
    success: function (response) {
      response.forEach((vendor) => {
        const option = document.createElement("option");
        option.value = vendor[0];
        option.text = vendor[1];
        vendorDrop.appendChild(option);
      });
    },
  });
  // Get all Departments
  $.ajax({
    url: "/api/departments",
    type: "GET",
    success: function (response) {
      const departments = response.data;
      departments.forEach((department) => {
        const option = document.createElement("option");
        option.value = department[0];
        option.text = department[1];
        departmentDrop.appendChild(option);
      });
    },
  });
}

function removeEmail(element) {
  element.parentElement.remove();
}
