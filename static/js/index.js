$(document).ready(function() {
    var $enterLogo = $('#enter-btn');
    $enterLogo.hover(function() {
        $(this).attr('src','../static/img/index/logo-hover.png')
    }, function() {
        $(this).attr('src','../static/img/index/enter-logo.png');
    });

    $enterLogo.bind('click', function() {
//        $(this).attr('src','img/index/logo-active.png');
        window.location.href = "main"
    })

});