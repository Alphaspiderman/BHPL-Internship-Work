$(document).ready(function () {
  $("#form").parsley();
  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
    handle_form_submit();
  });
  load_info();
});

function load_info() {
  var path = window.location.href.split("/");
  var contract_id = path[path.length - 1];
  $.ajax({
    url: "/api/vendors/payment",
    type: "GET",
    data: { id: contract_id },
    success: function (response) {
      console.log(response);
      const schema = response.schema;
      const data = response.data;
      document.getElementById("vendor").value =
        data[0][schema.indexOf("Vendor_Code")];
      document.getElementById("department").value =
        data[0][schema.indexOf("Department_Code")];
      document.getElementById("frequency").value =
        data[0][schema.indexOf("Invoice_Frequency")];
      document.getElementById("due_amount").value =
        data[0][schema.indexOf("Due_Amount")];
      document.getElementById("status").value =
        data[0][schema.indexOf("Invoice_Status")];
      document.getElementById("payment_date").value =
        data[0][schema.indexOf("Payment_Date")];
      document.getElementById("payment_amount").value =
        data[0][schema.indexOf("Payment_Amount")];
      data.forEach((row) => {
        // Add dates to dropdown
        const date = row[schema.indexOf("Due_Date")];
        const option = document.createElement("option");
        option.value = date;
        option.text = date;
        document.getElementById("due_date").appendChild(option);
      });
    },
  });
}

function handle_form_submit() {
  const form = document.getElementById("form");
  const formData = new FormData(form);
  const data = {};
  const valid = ["status", "payment_date", "payment_amount"];
  formData.forEach((value, key) => {
    if (valid.includes(key)) {
      data[key] = value;
    }
  });

  const path = window.location.href.split("/");
  const contract_id = path[path.length - 1];
  const newFormData = {
    id: contract_id,
    data: JSON.stringify(data),
  };

  console.log(newFormData);

  console.log(data);
  $.ajax({
    url: "/api/vendors/payment",
    type: "PUT",
    data: newFormData,
    success: function (response) {
      console.log(response);
      if (response.status === "success") {
        alert("Payment updated successfully");
        window.location.href = "/vendors/payments";
      } else {
        alert("Error updating payment");
      }
    },
  });
}
