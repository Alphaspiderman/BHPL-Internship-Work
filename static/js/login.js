window.onload = function () {
  // Listen for button click
  document.getElementById("login-btn").addEventListener("click", function () {
    window.location.href = "/api/login";
  });
  // Get the query string
  var queryString = window.location.search;
  // If query string is not empty
  if (queryString) {
    // Get the query string
    var params = new URLSearchParams(queryString);
    // Get the error message
    var error = params.get("error");
    // If error message is not empty
    if (error) {
      err_msg = {
        invalid_token: "Login Failed",
        replay_attack: "Contact IT Team (Replay)",
        invalid_request: "Please try again",
        invalid_domain: "Please use a burmanhospitality.com account",
        user_not_found: "Contact IT Team (Account missing)",
        too_many_users: "Contact IT Team (Duplicate account detected)",
      };
      // Display the error message
      var elem = document.getElementById("error-message");
      elem.hidden = false;
      elem.innerHTML = "<strong> Error! </strong>" + err_msg[error];
    }
  }
};
