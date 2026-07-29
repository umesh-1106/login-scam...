// =======================================
// Attendance Management System
// script.js
// =======================================

// Show Bootstrap Alerts Automatically
document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "0.5s";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 3000);

    });

});

// =======================================
// Password Show / Hide
// =======================================

function togglePassword(id, iconId) {

    const input = document.getElementById(id);
    const icon = document.getElementById(iconId);

    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }

}

// =======================================
// Mobile Number Validation
// =======================================

function validateMobile(input) {

    input.value = input.value.replace(/\D/g, "");

    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }

}

// =======================================
// Email Validation
// =======================================

function validateEmail(email) {

    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);

}

// =======================================
// Registration Form Validation
// =======================================

function validateRegisterForm() {

    const name = document.getElementById("name").value.trim();
    const mobile = document.getElementById("mobile").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm_password").value;

    if (name === "") {
        alert("Please enter your name.");
        return false;
    }

    if (mobile.length !== 10) {
        alert("Mobile number must contain exactly 10 digits.");
        return false;
    }

    if (!validateEmail(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return false;
    }

    if (password !== confirm) {
        alert("Passwords do not match.");
        return false;
    }

    return true;

}

// =======================================
// Login Validation
// =======================================

function validateLoginForm() {

    const mobile = document.getElementById("mobile").value.trim();
    const password = document.getElementById("password").value;

    if (mobile.length !== 10) {
        alert("Enter a valid 10-digit mobile number.");
        return false;
    }

    if (password === "") {
        alert("Please enter your password.");
        return false;
    }

    return true;

}

// =======================================
// Confirm Logout
// =======================================

function confirmLogout() {

    return confirm("Are you sure you want to logout?");

}

// =======================================
// Search Registered Users (Admin Dashboard)
// =======================================

function searchUsers() {

    const input = document.getElementById("searchInput");

    if (!input) return;

    const filter = input.value.toUpperCase();
    const table = document.getElementById("userTable");

    if (!table) return;

    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {

        let found = false;

        const cols = rows[i].getElementsByTagName("td");

        for (let j = 0; j < cols.length; j++) {

            if (cols[j].textContent.toUpperCase().indexOf(filter) > -1) {
                found = true;
            }

        }

        rows[i].style.display = found ? "" : "none";

    }

}

// =======================================
// Current Date & Time
// =======================================

function updateDateTime() {

    const element = document.getElementById("datetime");

    if (!element) return;

    const now = new Date();

    element.innerHTML = now.toLocaleString();

}

setInterval(updateDateTime, 1000);

// =======================================
// Welcome Message
// =======================================

window.onload = function () {

    updateDateTime();

    console.log("Attendance Management System Loaded Successfully.");

};
