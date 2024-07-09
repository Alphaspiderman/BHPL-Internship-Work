$(document).ready(function () {
  $.ajax({
    url: "/api/announcements/",
    type: "GET",
    success: function (data) {
      load_announcements(data["announcements"]);
    },
  });
});

function load_announcements(data) {
  container = document.getElementById("announcements-container");
  container.style =
    "position: relative; display: flex; flex-wrap: wrap; justify-content: center; align-items: center;";
  data.forEach((element) => {
    image = element["2"];
    title = element["1"];
    id = element["0"];
    div = document.createElement("div");
    div.style = "width: 500px; padding: 10px; margin: 10px;";
    announcement = document.createElement("div");
    announcement.className = "card";
    img = document.createElement("img");
    img.src = `/files/${image}`;
    img.class = "rounded mx-auto d-block";
    announcement.appendChild(img);
    body = document.createElement("div");
    body.className = "card-body";
    titleElement = document.createElement("h5");
    titleElement.innerHTML = title;
    body.appendChild(titleElement);
    link = document.createElement("a");
    link.href = `/announcement/${id}`;
    link.className = "btn btn-primary";
    link.innerHTML = "Read More";
    body.appendChild(link);
    announcement.appendChild(body);
    div.appendChild(announcement);
    container.appendChild(div);
  });
}
