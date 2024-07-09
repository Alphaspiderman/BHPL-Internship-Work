var api_data = "/api/sites/status";
var api_refresh = "/api/sites/checker";
var refresh_interval = 300000;
var refresh_set = false;

$(document).ready(function () {
  var btn = document.getElementById("recheck-btn");
  btn.onclick = function () {
    recheck_sites();
  };
  get_data();
});

function get_data() {
  $.ajax({
    type: "GET",
    url: api_data,
    success: function (data) {
      if (data.message == "no data available") {
        recheck_sites();
      } else {
        process_data(data);
      }
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function process_data(api_response) {
  // Last run time
  var last_run = document.getElementById("last-run");
  var date = new Date(api_response.last_run);

  var now = new Date();
  var diff = now - date;

  if (!refresh_set) {
    // Start refresh with next refresh
    refresh_set = true;
    setTimeout(function () {
      setInterval(recheck_sites, refresh_interval);
    }, refresh_interval - diff);
  }

  // If the last run was more than 5 minutes ago, recheck
  if (diff > refresh_interval + 5000) {
    recheck_sites();
    return;
  }

  var data = {
    labels: ["Online", "Offline", "Processing"],
    datasets: [
      {
        data: [0, 0, 0],
        backgroundColor: ["green", "red", "grey"],
      },
    ],
  };
  var online_cnt = api_response.online.length;
  var offline_cnt = api_response.offline.length;
  var to_process = api_response.total_count - api_response.checked;

  data.datasets[0].data[0] = online_cnt;
  data.datasets[0].data[1] = offline_cnt;
  data.datasets[0].data[2] = to_process;

  build_chart(data);

  // Set last run
  last_run.innerHTML = "Last Run at - " + date.toLocaleString();

  // Update Counts
  var onlcount = document.getElementById("online-count");
  onlcount.innerHTML = "Online - " + online_cnt;
  var offcount = document.getElementById("offline-count");
  offcount.innerHTML = "Offline - " + offline_cnt;

  var offline_list_1 = document.getElementById("offline-list-1");
  var offline_list_2 = document.getElementById("offline-list-2");
  offline_list_1.innerHTML = "";
  offline_list_2.innerHTML = "";

  if (api_response.offline.length > 0) {
    // Update message
    var msg = document.getElementById("checkMsg");
    msg.innerHTML = "The following sites are offline:";

    if (api_response.offline.length > 5) {
      api_response.offline.forEach(function (site, index) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(site));
        index % 2 == 0
          ? offline_list_1.appendChild(li)
          : offline_list_2.appendChild(li);
      });
    } else {
      api_response.offline.forEach(function (site) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(site));
        offline_list_1.appendChild(li);
      });
    }
  } else {
    // Update message
    var msg = document.getElementById("checkMsg");
    msg.innerHTML = "All Sites are Online";
  }
}

function build_chart(data) {
  var ctx = document.getElementById("connectivityChart").getContext("2d");
  var chart = Chart.getChart(ctx);
  if (chart) {
    chart.data = data;
    chart.update();
    return;
  }

  var myChart = new Chart(ctx, {
    type: "pie",
    data: data,
    options: {
      layout: {
        padding: 20,
      },
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: true,
        position: "bottom",
      },
    },
  });
  myChart.render();
}

function recheck_sites() {
  // Update message
  var msg = document.getElementById("checkMsg");
  msg.innerHTML = "Checking sites... Please wait";
  var onlcount = document.getElementById("online-count");
  onlcount.innerHTML = "Online - Processing...";
  var offcount = document.getElementById("offline-count");
  offcount.innerHTML = "Offline - Processing...";
  // Empty offline list
  var offline_list_1 = document.getElementById("offline-list-1");
  var offline_list_2 = document.getElementById("offline-list-2");
  offline_list_1.innerHTML = "";
  offline_list_2.innerHTML = "";
  // Trigger the recheck
  $.ajax({
    type: "GET",
    url: api_refresh,
    success: function (data) {
      get_data();
    },
    error: function (data) {
      console.log(data);
    },
  });
}
