$( window ).on("load", function() { 
    var initCarousel = function() {
        var carousel = $("painting-carousel")
        var rgx = /active=(\d+)/
        /*
        * new URLSearchParams(window.location.search).get('active')
        * would be cleaner but is not supported by Safari on iOS. See:
        * https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams#Browser_compatibility
        */
        var activeIdx = Number.parseInt(window.location.search.match(rgx)[1]) || 0

        $("#painting-carousel .carousel-inner").children(
            "div:nth-child({X})".replace("{X}", activeIdx + 1) // nth-child selector is not zerobased
        ).addClass("active")
    }
    initCarousel()
})
