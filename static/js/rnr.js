$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "/api/bells/info/",
    data: {
      show: "home",
    },
    success: function (data) {
      var dataPoint1 = [];
      data.top_10.store.forEach((store) => {
        dataPoint1.push({
          label: store,
          y: data.bell_map.store[store],
        });
      });
      dataPoint1.push({ label: "Others", y: data.others.store });
      load_chart(
        "chartContainer1",
        dataPoint1,
        "Most Bells Earned by Stores out this month",
      );
      var dataPoint2 = [];
      data.top_10.employee.forEach((employee) => {
        dataPoint2.push({
          label: employee,
          y: data.bell_map.employee[employee],
        });
      });
      dataPoint2.push({ label: "Others", y: data.others.employee });
      load_chart(
        "chartContainer2",
        dataPoint2,
        "Most Bells Earned by Employees out this month",
      );
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
