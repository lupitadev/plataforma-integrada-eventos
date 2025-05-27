document.addEventListener("DOMContentLoaded", function () {
    var userAuthenticated = JSON.parse(document.getElementById("auth_status").textContent);

    if (!userAuthenticated) {
        window.location.href = loginUrl;
    }
});