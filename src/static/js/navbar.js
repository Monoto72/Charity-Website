const navMenuDiv = document.getElementById("nav-content");
const navMenu = document.getElementById("nav-toggle");

const navbarToggle = () => {
    if (navMenuDiv.classList.contains("hidden")) {
        navMenuDiv.classList.remove("hidden");
    } else {
        navMenuDiv.classList.add("hidden");
    }
}

document.getElementById("nav-toggle").addEventListener("click", navbarToggle);