$(document).ready(function () {
  // Link the buttons
  $("#trigger-load").click(load_data);
  $("#trigger-export").click(function () { window.open("/api/bells/info/?month=" + $("#month").val() + "&year=" + $("#year").val() + "&export=true", "_blank"); });
  // Put in the current month and year in the form
  var today = new Date();
  var month = today.getMonth() + 1;
  var year = today.getFullYear();
  // Pad the month with a 0 if it is less than 10
  if (month < 10) {
    month = "0" + month;
  }
  $("#month").val(month);
  $("#year").val(year);
  // Trigger the button click
  $("#trigger-load").click();
});

function load_data() {
  $.ajax({
    type: "GET",
    url: "/api/bells/info/",
    data: {
      show: "home",
      month: $("#month").val(),
      year: $("#year").val(),
    },
    success: function (data) {
      if (data.can_export) {
        $("#export").removeAttr("hidden");
      }
      var dataPoint1 = [];
      var sum_other_stores = 0;
      store_lb_by_cnt = data.by_count.store;
      emp_lb_by_cnt = data.by_count.employee;
      store_lb_by_cnt.forEach((entry, idx) => {
        if (idx < 10) {
          dataPoint1.push({
            label: entry,
            y: data.store_bell_count_map[entry],
          });
        } else {
          sum_other_stores += data.store_bell_count_map[entry];
        }
      });

      if (sum_other_stores > 0) {
        dataPoint1.push({ label: "Others", y: sum_other_stores });
      }


      load_chart(
        "chartContainer1",
        dataPoint1,
        "Most Bells Earned by Stores out this month",
      );

      var dataPoint2 = [];
      var sum_other_employees = 0;

      emp_lb_by_cnt.forEach((entry, idx) => {
        if (idx < 10) {
          dataPoint2.push({
            label: data.employee_id_name_map[entry],
            y: data.employee_id_bell_count_map[entry],
          });
        } else {
          sum_other_employees += data.employee_id_bell_count_map[entry];
        }
      });
      if (sum_other_employees > 0) {
        dataPoint2.push({ label: "Others", y: sum_other_employees });
      }
      load_chart(
        "chartContainer2",
        dataPoint2,
        "Most Bells Earned by Employees out this month",
      );

      load_lb(data);
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function load_chart(container, dataPoints, title) {
  var chart = new CanvasJS.Chart(container, {
    theme: "light1",
    exportEnabled: true,
    animationEnabled: true,
    title: {
      text: title,
    },
    data: [
      {
        type: "pie",
        toolTipContent: "<b>{label}</b>: {y} Bells",
        showInLegend: "true",
        legendText: "{label}",
        indexLabelFontSize: 16,
        indexLabel: "{label} - {y} Bells",
        dataPoints: dataPoints,
      },
    ],
  });
  chart.render();
}

function load_lb(data) {
  table = document.getElementById("leaderboard");
  body = document.getElementById("table-body");
  // Clear the table body
  body.innerHTML = "";
  employees = data.by_value.employee;
  employees.forEach((entry) => {
    var row = body.insertRow();
    row.insertCell(0).innerHTML = data.employee_id_name_map[entry];
    row.insertCell(1).innerHTML = data.employee_id_store_map[entry];
    row.insertCell(2).innerHTML = data.employee_id_bell_value_map[entry];
    row.insertCell(3).innerHTML = data.employee_id_bell_count_map[entry];
  });
}
