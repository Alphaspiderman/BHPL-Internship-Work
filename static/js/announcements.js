window.onload = function () {
  $.ajax({
    url: "/api/announcements/",
    type: "GET",
    success: function (data) {
      load_announcements(data["announcements"]);
    },
  });
};

/* Announcement card format
 <div class="card">
    <img/>
    <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <a href="LINK" class="btn btn-primary">Go somewhere</a>
    </div>
</div> */

function load_announcements(data) {
  container = document.getElementById("announcements-container");
  container.style = "display: flex; flex-wrap: wrap; padding: 20px;";
  data.forEach((element) => {
    image = element["2"];
    title = element["1"];
    id = element["0"];
    div = document.createElement("div");
    div.className = "col-sm-6 col-lg-4 mb-4";
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
