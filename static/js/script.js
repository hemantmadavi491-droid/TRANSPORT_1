function toggleMenu() {
    const menu = document.getElementById("dropdownMenu");

    if (menu) {
        menu.classList.toggle("show");
    }
}

// Close dropdown when clicking outside
document.addEventListener("click", function(event) {

    const menu = document.getElementById("dropdownMenu");
    const profilePic = document.querySelector(".profile-pic");

    if (
        menu &&
        !menu.contains(event.target) &&
        !profilePic.contains(event.target)
    ) {
        menu.classList.remove("show");
    }
});