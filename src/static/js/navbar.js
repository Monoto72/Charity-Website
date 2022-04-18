const navMenuDiv = document.querySelector("#nav-content");
const navMenu = document.querySelector("#nav-toggle");
const navbar = document.querySelector("#header");
const navHeading = document.querySelector("#header-heading");
const goToTop = document.querySelector("#go-top");

const pageURL = JSON.parse(document.querySelector(`#pageURL`).textContent);
const navList = document.querySelector("#main-list").querySelectorAll("li").forEach(li => {
    li = li.querySelector("a");
    if (li.innerHTML == pageURL) {
        li.classList.add("font-black", "pointer-events-none")
    }
})

let active = undefined;
let toggleNav = false;

const scrollHandler = (scroll) => {
    if (scroll >= 10 || window.scrollY >= 10) {
        goToTop.classList.replace("hidden", "block");
        navbar.classList.add("bg-white");
        navHeading.classList.replace("text-white", "text-black");
    } else if (toggleNav && (scroll <= 9 || window.scrollY <= 9)) {
        navbarToggle(1);
    } else {
        if (toggleNav) return;
        goToTop.classList.replace("block", "hidden");
        navbar.classList.remove("bg-white");
        navHeading.classList.replace("text-black", "text-white");
    }
}

const navbarToggle = (val) => {
    console.log(val)
    if (val == 0) {
        if (navMenuDiv.classList.contains("hidden")) {
            toggleNav = true;
            navMenuDiv.classList.remove("hidden");
            navMenuDiv.classList.add("text-center", "bg-white")
            navbar.classList.add("bg-white")
            navHeading.classList.replace("text-white", "text-black")
        } else {
            if (window.scrollY == 0) {
                navbar.classList.remove("bg-white");
                navHeading.classList.replace("text-black", "text-white")
            }
            toggleNav = false;
            navMenuDiv.classList.add("hidden");
            navMenuDiv.classList.remove("text-center", "bg-white")
        }
    } else {
        if (!toggleNav) {
            if (window.scrollY == 0) {
                goToTop.classList.replace("block", "hidden")
            }
            goToTop.classList.replace("block", "hidden");
            navbar.classList.remove("bg-white");
            navHeading.classList.replace("text-black", "text-white");
        } else {
            goToTop.classList.replace("block", "hidden")
        }
    }
}

const goTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

window.addEventListener('load', () => {
    let scrollLoc = window.scrollY;
    return scrollHandler(scrollLoc)
});

document.addEventListener('scroll', scrollHandler);

document.querySelector("#nav-toggle").addEventListener("click", () => navbarToggle(0));
document.querySelector("#go-top").addEventListener("click", goTop)