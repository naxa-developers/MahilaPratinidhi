
$(document).ready(function () {

    scrollTab();
    $(window).resize(function () {
        scrollTab();
    });
    function scrollTab() {
        var devicewidth = $(window).width();
        if (devicewidth < 769) {
            $(".mapTab .tabHolder li ").click(function () {

                $('html, body').animate({
                    scrollTop: $(".mapHolder").offset().top
                }, 1000);
            });
        }
    }

    $(".btnholder").click(function () {

        $(".btnholder i,.showhidelist,.tbtn ").toggleClass("show");
        $(".tabs ").toggleClass("icons");
        $("").toggleClass("show");


    })

    scrollProvience();
    $(window).resize(function () {
        scrollProvience();
    });
    function scrollProvience() {
        var devicewidth = $(window).width();

        $("#exTab3 li ").click(function () {

            $('html, body').animate({
                scrollTop: $("#exTab3 .tab-content").offset().top
            }, 1000);
        });

    }




});

