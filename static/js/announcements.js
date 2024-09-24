$(document).ready(function () {
  $.ajax({
    url: "/api/announcements/",
    type: "GET",
    success: function (data) {
      show_banner(data["announcements"]);
    },
  });
});

function show_banner(announcements) {
  if (announcements.length > 0) {
    banner = document.getElementById("announcement-info");
    banner.innerHTML =
      "New Announcement! View here: <a href='/announcement/" +
      announcements[0][0] +
      "'>" +
      announcements[0][1] +
      "</a>";
    banner.removeAttribute("hidden");
  }
}
