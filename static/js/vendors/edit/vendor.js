const mapping = {
  Vendor_Code: "vendorCode",
  Vendor_Name: "vendorName",
  Vendor_Email: "vendorEmail",
  Vendor_Phone: "vendorPhone",
  Vendor_Address: "vendorAddress",
  PAN_Number: "panNumber",
  GST_Number: "gstNumber",
  Account_Number: "accountNumber",
};

$(document).ready(function () {
  $("#form").parsley();
  vendor_id = window.location.href.split("/").pop();
  $.ajax({
    url: "/api/vendors/info",
    type: "GET",
    data: {
      id: vendor_id,
    },
    success: function (data) {
      if (data.data.length == 0) {
        alert("Vendor not found");
        window.location.href = "/vendors/vendors";
        return;
      }
      document.getElementById("vendorCode").value =
        data.data[0][data.schema.indexOf("Vendor_Code")];
      document.getElementById("vendorName").value =
        data.data[0][data.schema.indexOf("Vendor_Name")];
      document.getElementById("vendorEmail").value =
        data.data[0][data.schema.indexOf("Vendor_Email")];
      document.getElementById("vendorPhone").value =
        data.data[0][data.schema.indexOf("Vendor_Phone")];
      document.getElementById("vendorAddress").value =
        data.data[0][data.schema.indexOf("Vendor_Address")];
      document.getElementById("panNumber").value =
        data.data[0][data.schema.indexOf("PAN_Number")];
      document.getElementById("gstNumber").value =
        data.data[0][data.schema.indexOf("GST_Number")];
      document.getElementById("accountNumber").value =
        data.data[0][data.schema.indexOf("Account_Number")];
    },
  });
  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
    handle_form_submit();
  });
});

function handle_form_submit() {
  // Get form data
  vendorCode = document.getElementById("vendorCode").value;
  vendorName = document.getElementById("vendorName").value;
  vendorEmail = document.getElementById("vendorEmail").value;
  vendorPhone = document.getElementById("vendorPhone").value;
  vendorAddress = document.getElementById("vendorAddress").value;
  panNumber = document.getElementById("panNumber").value;
  gstNumber = document.getElementById("gstNumber").value;
  accountNumber = document.getElementById("accountNumber").value;

  // Get data from DB
  vendor_id = window.location.href.split("/").pop();
  $.ajax({
    url: "/api/vendors/info",
    type: "GET",
    data: {
      id: vendor_id,
    },
    success: function (respData) {
      // Check which fields are modified
      modified_fields = [];
      schema = respData.schema;
      respData = respData.data[0];
      if (respData[schema.indexOf("Vendor_Name")] != vendorName) {
        modified_fields.push("Vendor_Name");
      }
      if (respData[schema.indexOf("Vendor_Email")] != vendorEmail) {
        modified_fields.push("Vendor_Email");
      }
      if (respData[schema.indexOf("Vendor_Phone")] != vendorPhone) {
        modified_fields.push("Vendor_Phone");
      }
      if (respData[schema.indexOf("Vendor_Address")] != vendorAddress) {
        modified_fields.push("Vendor_Address");
      }
      if (respData[schema.indexOf("PAN_Number")] != panNumber) {
        modified_fields.push("PAN_Number");
      }
      if (respData[schema.indexOf("GST_Number")] != gstNumber) {
        modified_fields.push("GST_Number");
      }
      if (respData[schema.indexOf("Account_Number")] != accountNumber) {
        modified_fields.push("Account_Number");
      }
      // Check if any field is modified
      if (modified_fields.length == 0) {
        alert("No fields modified");
        return;
      }

      // Update data in DB
      $.ajax({
        url: "/api/vendors/info",
        type: "PUT",
        data: {
          id: vendor_id,
          modified_fields: modified_fields,
          Vendor_Name: vendorName,
          Vendor_Email: vendorEmail,
          Vendor_Phone: vendorPhone,
          Vendor_Address: vendorAddress,
          PAN_Number: panNumber,
          GST_Number: gstNumber,
          Account_Number: accountNumber,
        },
        success: function (data) {
          alert("Vendor updated successfully");
          window.location.href = "/vendors/vendors";
        },
      });
    },
  });
}
