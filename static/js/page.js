$(document).ready(function () {
    console.log("Page loaded");
    load_navbar();
});

navbar_entries = [
    ["/home", "Home"],
    ["/locations", "Location Master"],
    ["/connectivity", "Connectivity Status"],
    ["/sales", "Sales Dashboard"],
    ["/vendors", "Vendor Management"],
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
        li = document.createElement("li");
        li.className = "nav-item";
        li.setAttribute("aria-current", "page");
        if (path === entry[0]) {
            li.setAttribute("active", "");
        }
        ul.appendChild(li);
        a = document.createElement("a");
        a.className = "nav-link";
        a.href = entry[0];
        a.innerHTML = entry[1];
        li.appendChild(a);
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
