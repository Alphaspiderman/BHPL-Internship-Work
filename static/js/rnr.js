$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "/api/bells/info/",
    data: {
      show: "home",
    },
    success: function (data) {
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
      dataPoint1.push({ label: "Others", y: sum_other_stores });

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
      dataPoint2.push({ label: "Others", y: sum_other_employees });
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
});

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
  employees = data.by_value.employee;
  employees.forEach((entry) => {
    var row = table.insertRow();
    row.insertCell(0).innerHTML = data.employee_id_name_map[entry];
    row.insertCell(1).innerHTML = data.employee_id_store_map[entry];
    row.insertCell(2).innerHTML = data.employee_id_bell_value_map[entry];
    row.insertCell(3).innerHTML = data.employee_id_bell_count_map[entry];
  });
}
