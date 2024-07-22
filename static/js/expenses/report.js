$(document).ready(function () {
  start_of_month = new Date();
  start_of_month.setDate(1);
  document.getElementById("dateFrom").valueAsDate = start_of_month;
  document.getElementById("dateTo").valueAsDate = new Date();
  document.getElementById("search").addEventListener("click", function () {
    load_data();
  });
  document.getElementById("exportPDF").addEventListener("click", function () {
    // Open a new tab
    date_from = document.getElementById("dateFrom").value;
    date_to = document.getElementById("dateTo").value;
    url = "/api/expenses/pdf?from=" + date_from + "&to=" + date_to;
    window.open(url, "_blank").focus();
  });
  load_data();
});

function load_data() {
  date_from = document.getElementById("dateFrom").value;
  date_to = document.getElementById("dateTo").value;
  $.ajax({
    url: "/api/expenses/me",
    type: "GET",
    data: {
      from: date_from,
      to: date_to,
    },
    success: function (data) {
      document.getElementById("exportPDF").removeAttribute("disabled");
      // Set entry count and total expense
      document.getElementById("entryCount").value = data.data.length;
      document.getElementById("totalExpense").value = "₹ " + data.total;
      // Load data into quick view table
      table = document.getElementById("quickViewBody");
      table.innerHTML = "";
      const dateIDX = data.schema.indexOf("Date_Of_Expense");
      const locIDX = data.schema.indexOf("Location");
      const fileIDX = data.schema.indexOf("Bill_Attached");
      const descIDX = data.schema.indexOf("Reason");
      data.data.forEach((element) => {
        row = table.insertRow();
        var file_link = element[fileIDX];
        var file_info = "No File";
        if (file_link != "No") {
          file_link = "/api/files?file_id=" + file_link;
          file_info = "<a href=" + file_link + ">Get File</a>";
        }
        var delete_btn =
          '<button class="btn btn-danger" onclick=deleteExpense(' +
          element[0] +
          ")>Delete</button>";
        row.insertCell(0).innerHTML = element[dateIDX];
        row.insertCell(1).innerHTML = element[locIDX];
        row.insertCell(2).innerHTML = file_info;
        row.insertCell(3).innerHTML = element[descIDX];
        row.insertCell(4).innerHTML = delete_btn;
      });
    },
  });
}

function deleteExpense(id) {
  // Send a DELETE Request
  $.ajax({
    url: "/api/expenses/me",
    type: "DELETE",
    data: {
      expense_id: id,
    },
    success: function (data) {
      if (data.status == "success") {
        alert("Entry Deleted");
        // Reload page
        load_data();
      } else {
        alert("An error occoured while removing the entry");
      }
    },
  });
}
