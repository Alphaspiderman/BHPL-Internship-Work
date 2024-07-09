$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "/api/bells/info/",
    data: {
      show: "home",
    },
    success: function (data) {
      var dataPoint1 = [];
      store_bell_map = data.store_bell_map;
      for (var key in store_bell_map) {
        dataPoint1.push({
          label: key,
          y: store_bell_map[key],
        });
      }
      load_chart(
        "chartContainer1",
        dataPoint1,
        "Bells (by Location) Handed out this month",
      );
      var dataPoint2 = [];
      employee_bell_map = data.employee_bell_map;
      employee_name_id_map = data.employee_name_id_map;
      for (var key in employee_bell_map) {
        dataPoint2.push({
          label: employee_name_id_map[key],
          y: employee_bell_map[key],
        });
      }
      load_chart(
        "chartContainer2",
        dataPoint2,
        "Bells (by Person) Handed out this month",
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
