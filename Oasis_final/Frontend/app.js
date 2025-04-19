document.addEventListener("DOMContentLoaded", function () {
    // Signup Form
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/signup", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
            });

            if (response.ok) {
                window.location.href = "/login"; 
            } else {
                alert("Signup failed! User may already exist.");
            }
        });
    }

    // Login Form
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
            });

            if (response.ok) {
                window.location.href = "/"; 
            } else {
                alert("Invalid credentials!");
            }
        });
    }
});
