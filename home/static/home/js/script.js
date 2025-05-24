async function redirectUser() {
    try {
        let response = await fetch("/check-user/", {
            method: "GET",
            credentials: "include"
        });

        let data = await response.json();

        if (data.authenticated) {
            window.location.href = "profile.html"; // Authenticated user
        } else if (data.registered) {
            window.location.href = "login.html"; // Registered but not logged in
        } else {
            window.location.href = "register.html"; // Not registered
        }
    } catch (error) {
        console.error("Error checking authentication:", error);
        window.location.href = "login.html";
    }
}