$(document).ready(function () {
  load_location();
  $("#form").parsley();
  // Listen to the click event of edit button
  $("#form").submit(function (e) {
    e.preventDefault();
    var formData = new FormData(document.getElementById("form"));
    $.ajax({
      url: "/api/sites/info",
      type: "PUT",
      data: formData,
      success: function (response) {
        if (response.status === "success") {
          alert("Location updated successfully");
          window.location.href = "/locations";
        } else {
          alert("Failed to update location");
        }
      },
      error: function (xhr, status, error) {
        alert("Failed to update location");
      },
      contentType: false,
      processData: false,
    });
  });
});

function load_location() {
  // Get the location id from the URL
  var path = window.location.href.split("/");
  var loc_id = path[path.length - 1];
  $.ajax({
    url: "/api/sites/info",
    type: "GET",
    data: { location: loc_id, show_all: true },
    success: function (response) {
      if (response.status === "failure") {
        alert("Location not found");
        window.location.href = "/locations";
        return;
      }
      var location = response.data[0];
      var schema = response.schema;
      location.forEach((elem, idx) => {
        console.log(schema[idx] + " : " + elem);
      });
      document.getElementById("champsNumber").value =
        location[schema.indexOf("Champs_Number")];
      document.getElementById("storeCode").value =
        location[schema.indexOf("Store_Code")];
      document.getElementById("storeName").value =
        location[schema.indexOf("Store_Name")];
      document.getElementById("posistStoreName").value =
        location[schema.indexOf("Posist_Store_Name")];
      document.getElementById("posistLiveDate").value =
        location[schema.indexOf("Posist_Live_Date")];
      document.getElementById("localAddress").value =
        location[schema.indexOf("Local_Address")];
      document.getElementById("city").value = location[schema.indexOf("City")];
      document.getElementById("stateName").value =
        location[schema.indexOf("State_Name")];
      document.getElementById("regionInternal").value =
        location[schema.indexOf("Region_Internal")];
      document.getElementById("postalCode").value =
        location[schema.indexOf("Postal_Code")];
      document.getElementById("latitude").value =
        location[schema.indexOf("Latitude")];
      document.getElementById("longitude").value =
        location[schema.indexOf("Longitude")];
      document.getElementById("ownershipType").value =
        location[schema.indexOf("Ownership_Type")];
      document.getElementById("primaryBrandChannel").value =
        location[schema.indexOf("Primary_Brand_Channel")];
      document.getElementById("facilityType").value =
        location[schema.indexOf("Facility_Type")];
      document.getElementById("storeType").value =
        location[schema.indexOf("Store_Type")];
      document.getElementById("localOrgName").value =
        location[schema.indexOf("Local_Org_Name")];
      document.getElementById("franchiseeId").value =
        location[schema.indexOf("Franchisee_Id")];
      document.getElementById("marketName").value =
        location[schema.indexOf("Market_Name")];
      document.getElementById("areaName").value =
        location[schema.indexOf("Area_Name")];
      document.getElementById("coachId").value =
        location[schema.indexOf("Coach_Id")];
      document.getElementById("storePhone").value =
        location[schema.indexOf("Store_Phone")];
      document.getElementById("storeEmail").value =
        location[schema.indexOf("Store_Email")];
      document.getElementById("status").value =
        location[schema.indexOf("Status")];
      document.getElementById("storeOpenDate").value =
        location[schema.indexOf("Store_Open_Date")];
      document.getElementById("seatCount").value =
        location[schema.indexOf("Seat_Count")];
      document.getElementById("tempCloseDate").value =
        location[schema.indexOf("Temp_Close_Date")];
      document.getElementById("reopenDate").value =
        location[schema.indexOf("Reopen_Date")];
      document.getElementById("storeClosureDate").value =
        location[schema.indexOf("Store_Closure_Date")];
      document.getElementById("sundayOpen").value =
        location[schema.indexOf("Sunday_Open")];
      document.getElementById("sundayClose").value =
        location[schema.indexOf("Sunday_Close")];
      document.getElementById("mondayOpen").value =
        location[schema.indexOf("Monday_Open")];
      document.getElementById("mondayClose").value =
        location[schema.indexOf("Monday_Close")];
      document.getElementById("tuesdayOpen").value =
        location[schema.indexOf("Tuesday_Open")];
      document.getElementById("tuesdayClose").value =
        location[schema.indexOf("Tuesday_Close")];
      document.getElementById("wednesdayOpen").value =
        location[schema.indexOf("Wednesday_Open")];
      document.getElementById("wednesdayClose").value =
        location[schema.indexOf("Wednesday_Close")];
      document.getElementById("thursdayOpen").value =
        location[schema.indexOf("Thursday_Open")];
      document.getElementById("thursdayClose").value =
        location[schema.indexOf("Thursday_Close")];
      document.getElementById("fridayOpen").value =
        location[schema.indexOf("Friday_Open")];
      document.getElementById("fridayClose").value =
        location[schema.indexOf("Friday_Close")];
      document.getElementById("saturdayOpen").value =
        location[schema.indexOf("Saturday_Open")];
      document.getElementById("saturdayClose").value =
        location[schema.indexOf("Saturday_Close")];
      // Check if Ip_Range_Start is present in the schema as a check for IT Fields
      if (schema.indexOf("Ip_Range_Start") == -1) {
        // Hide the IT Fields
        document.getElementById("itFields").setAttribute("hidden", "");
        document.getElementById("itHeader").setAttribute("hidden", "");
      } else {
        document.getElementById("ipRangeStart").value =
          location[schema.indexOf("Ip_Range_Start")];
        document.getElementById("ipRangeEnd").value =
          location[schema.indexOf("Ip_Range_End")];
        document.getElementById("subnet").value =
          location[schema.indexOf("Subnet")];
        document.getElementById("staticIp").value =
          location[schema.indexOf("Static_Ip")];
        document.getElementById("linkISP").value =
          location[schema.indexOf("Link_ISP")];
        document.getElementById("linkType").value =
          location[schema.indexOf("Link_Type")];
      }
    },
  });
}

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
    type: "PUT",
    data: newFormData,
    success: function (response) {
      if (response.status === "success") {
        alert("Location updated successfully");
        window.location.href = "/locations";
      } else {
        alert("Failed to update location");
      }
    },
    error: function (xhr, status, error) {
      alert("Failed to update location");
    },
    contentType: false,
    processData: false,
  });
}
