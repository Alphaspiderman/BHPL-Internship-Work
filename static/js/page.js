$(document).ready(function () {
  console.log("Page loaded");
  load_navbar();
});

navbar_entries = [
  ["/home", "Home"],
  {
    Rewards: [
      ["/rewards", "Reward & Recognition"],
      ["/reward/bells", "Award Bells"],
    ],
  },
  {
    Vendors: [
      ["/vendors/vendors", "Vendor Management"],
      ["/vendors/contracts", "Vendor Contracts"],
      ["/vendors/payments", "Vendor Payments"],
    ],
  },
  ["/locations", "Location Master"],
  ["/connectivity", "Connectivity Status"],
];

// Load the navbar
function load_navbar() {
  path = window.location.pathname;
  navbar = document.getElementById("navbarContent");
  // Add an unordered list
  ul = document.createElement("ul");
  ul.className = "navbar-nav me-auto mb-2 mb-lg-0";
  navbar.appendChild(ul);
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
