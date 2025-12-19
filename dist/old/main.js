// jshint esversion: 8
var navbar = document.querySelector('.hero .hero-head .navbar');
var burger = navbar.querySelector('.navbar-burger');
var menu = navbar.querySelector('.navbar-menu');

burger.addEventListener('click', function() {
    burger.classList.toggle('is-active');
    menu.classList.toggle('is-active');
});

const links = menu.querySelectorAll("a.go-element");

function clickHandler(e) {
    e.preventDefault();
    const href = this.getAttribute("href");

    document.querySelector(href).scrollIntoView({
        behavior: "smooth"
    });
}

for (const link of links) {
    link.addEventListener("click", clickHandler);
}

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        navbar.style.top = "0";
    } else {
        navbar.style.top = "-500px";
    }
    prevScrollpos = currentScrollPos;
};