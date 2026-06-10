// =========================
// Transport Management System
// script.js
// =========================

document.addEventListener("DOMContentLoaded", () => {

    console.log("Transport Management System Loaded");

    // Sidebar Active Menu
    const links = document.querySelectorAll(".sidebar a");

    links.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });

});


// =========================
// Confirm Delete
// =========================

function confirmDelete() {

    return confirm("Are you sure you want to delete this record?");

}


// =========================
// Search Table
// =========================

function searchTable() {

    let input = document.getElementById("searchInput");
    let filter = input.value.toUpperCase();

    let table = document.getElementById("dataTable");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let found = false;

        let td = tr[i].getElementsByTagName("td");

        for (let j = 0; j < td.length; j++) {

            if (
                td[j].innerHTML.toUpperCase().indexOf(filter) > -1
            ) {
                found = true;
            }
        }

        tr[i].style.display = found ? "" : "none";
    }
}


// =========================
// Live Clock
// =========================

function updateClock() {

    let now = new Date();

    let time =
        now.toLocaleDateString() +
        " " +
        now.toLocaleTimeString();

    let clock = document.getElementById("clock");

    if (clock) {
        clock.innerHTML = time;
    }
}

setInterval(updateClock, 1000);


// =========================
// Dashboard Counter Animation
// =========================

function animateCounter(id, target) {

    let element = document.getElementById(id);

    if (!element) return;

    let count = 0;

    let speed = Math.ceil(target / 50);

    let interval = setInterval(() => {

        count += speed;

        if (count >= target) {

            count = target;
            clearInterval(interval);

        }

        element.innerHTML = count;

    }, 30);
}


// Example Usage:
// animateCounter("vehicleCount", 120);
// animateCounter("driverCount", 45);
// animateCounter("customerCount", 300);
// animateCounter("tripCount", 850);


// =========================
// Dark / Light Mode
// =========================

function toggleTheme() {

    document.body.classList.toggle("light-mode");

    let mode = document.body.classList.contains("light-mode")
        ? "light"
        : "dark";

    localStorage.setItem("theme", mode);
}


window.onload = function () {

    let savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light-mode");
    }

};


// =========================
// Notification Popup
// =========================

function showNotification(message) {

    let notification = document.createElement("div");

    notification.className = "notification";

    notification.innerHTML = message;

    document.body.appendChild(notification);

    setTimeout(() => {

        notification.remove();

    }, 3000);
}


// Example:
// showNotification("Vehicle Added Successfully!");


// =========================
// Form Validation
// =========================

function validateVehicleForm() {

    let vehicleNo =
        document.getElementById("vehicle_no").value;

    if (vehicleNo.trim() === "") {

        alert("Vehicle Number is required!");
        return false;
    }

    return true;
}