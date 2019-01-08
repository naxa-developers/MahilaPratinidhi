$(document).ready(function () {
    $('.slider').slick({
        autoplay: false,
        dots: true,
        arrows: false


    });
    ScrollReveal().reveal('.reveal');

    ScrollReveal().reveal('.reveal', {
        delay: 50,
        duration: 400,
        viewFactor: 0.5,
        reset: false
    });


});