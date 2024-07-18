$(document).ready(function () {
  // Listen to form submission
  $("#form").submit(function (e) {
    e.preventDefault();
    handle_form_submit.call();
  });
  // Set Store Open Date to today's date
  const today = new Date();
  const formattedDate = today.toISOString().slice(0, 10);
  document.getElementById("storeOpenDate").value = formattedDate;
  // Set Posist Live Date to today's date
  document.getElementById("posistLiveDate").value = formattedDate;
});
function handle_form_submit() {
  var formData = new FormData(document.getElementById("form"));
  var newFormData = new FormData();
  // Drop all empty values
  formData.forEach(function (value, key) {
    console.log(key + " : " + value);
    if (value != "" && value != null) {
      newFormData.append(key, value);
    }
  });
  $.ajax({
    url: "/api/sites/info",
    type: "POST",
    data: newFormData,
    success: function (response) {
      if (response.status === "success") {
        alert("Location created successfully");
        window.location.href = "/locations";
      } else {
        alert("Failed to create location");
      }
    },
    error: function (xhr, status, error) {
      alert("Failed to create location");
    },
    contentType: false,
    processData: false,
  });
}
