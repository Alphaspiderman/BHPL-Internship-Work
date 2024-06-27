window.onload = function() {
    // Listen for button click
    document.getElementById('login-btn').addEventListener('click', function() {
        window.location.href = "/api/login";
    });
}
