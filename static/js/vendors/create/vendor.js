$(document).ready(function () {
  $("#form").parsley();
  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
    handle_form_submit();
  });
});

function handle_form_submit() {
  const form = document.getElementById("form");
  const formData = new FormData(form);
  const data = {};
  formData.forEach((value, key) => {
    data[key] = value;
  });

  $.ajax({
    url: "/api/vendors/info",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function (data) {
      if (data.error) {
        alert(data.error);
      } else {
        alert("Vendor created successfully");
        window.location.href = "/vendors/vendors";
      }
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
}
