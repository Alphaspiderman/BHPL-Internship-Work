$(document).ready(function () {
  console.log("Page loaded");
  load_navbar();
});

// Load the navbar
function load_navbar() {
  path = window.location.pathname;
  navbar = document.getElementById("navbarContent");
  // Add an unordered list
  ul = document.createElement("ul");
  ul.className = "navbar-nav me-auto mb-2 mb-lg-0";
  navbar.appendChild(ul);

  // Refresh the navbar entries if required or get the entries from server and store them in localStorage
  checkNavbarEntries();

  // Get the navbar entries from localStorage
  data = localStorage.getItem("navbar_entries");
  // Reload the page if the entries are not available
  if (data === null) {
    console.error("Navbar entries not available");
    // Wait for 1 second and reload the page
    setTimeout(function () {
      location.reload();
    }, 500);
  }
  navbar_entries = JSON.parse(data);
  // Add the entries
  navbar_entries.forEach((entry) => {
    // Check if the entry is an array or an dict
    if (Array.isArray(entry)) {
      // Add the entry
      li = document.createElement("li");
      li.className = "nav-item";
      ul.appendChild(li);
      a = document.createElement("a");
      a.className = "nav-link";
      a.href = entry[0];
      a.innerHTML = entry[1];
      if (entry[0] == path) {
        a.className += " active";
      }
      li.appendChild(a);
    } else {
      // Add the dropdown
      li = document.createElement("li");
      li.className = "nav-item dropdown";
      ul.appendChild(li);
      a = document.createElement("a");
      a.className = "nav-link dropdown-toggle";
      a.href = "#";
      a.id = "navbarDropdown";
      a.role = "button";
      a.setAttribute("data-bs-toggle", "dropdown");
      a.setAttribute("aria-haspopup", "true");
      a.setAttribute("aria-expanded", "false");
      a.innerHTML = Object.keys(entry)[0];
      li.appendChild(a);
      // Add the dropdown menu
      div = document.createElement("div");
      div.className = "dropdown-menu";
      div.setAttribute("aria-labelledby", "navbarDropdown");
      li.appendChild(div);
      entry[Object.keys(entry)[0]].forEach((subentry) => {
        a = document.createElement("a");
        a.className = "dropdown-item";
        a.href = subentry[0];
        a.innerHTML = subentry[1];
        div.appendChild(a);
      });
    }
  });
  // Add the logout button
  div = document.createElement("div");
  div.className = "d-lg-flex col-lg-3 justify-content-lg-end";
  navbar.appendChild(div);
  a = document.createElement("a");
  a.className = "btn btn-outline-danger";
  a.href = "/api/logout";
  a.innerHTML = "Logout";
  div.appendChild(a);
}
function fetchNavbarEntries() {
  $.ajax({
    url: "/api/navbar",
    type: "GET",
    success: function (data) {
      // Set expiration time to 6 hour
      var now = new Date();
      var time = now.getTime();
      time += 3600 * 6 * 1000;
      now.setTime(time);
      // Store the navbar entries in localStorage
      localStorage.setItem("navbar_entries", JSON.stringify(data));
      localStorage.setItem("navbar_entries_expiration", now);
    },
    error: function (xhr, status, error) {
      console.error("Error while loading the navbar entries");
    },
  });
}
function checkNavbarEntries() {
  // Check if the navbar entries exist in localStorage
  if (localStorage.getItem("navbar_entries") === null) {
    fetchNavbarEntries();
  } else {
    // Check if the navbar entries are expired
    expiration = new Date(localStorage.getItem("navbar_entries_expiration"));
    now = new Date();
    if (now > expiration) {
      fetchNavbarEntries();
    }
  }
}
