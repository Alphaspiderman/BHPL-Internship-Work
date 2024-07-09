$(document).ready(function () {
  $.ajax({
    type: "GET",
    url: "/api/bells/info/",
    data: {
      show: "home",
    },
    success: function (data) {
      load_chart(data);
    },
    error: function (data) {
      console.log(data);
    },
  });
});

function load_chart(data) {
  var dataPoints = [];
  store_bell_map = data.store_bell_map;
  for (var key in store_bell_map) {
    dataPoints.push({
      label: key,
      y: store_bell_map[key],
    });
  }
  var chart = new CanvasJS.Chart("chartContainer", {
    theme: "light1",
    exportEnabled: true,
    animationEnabled: true,
    title: {
      text: "Bells Handed out this month",
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
