$(document).ready(function() {

    //一级导航hover图片变换
    //画廊
    $('#galleryPage').hover(function() {
        $(this).attr('src', '../static/img/main/gallery-link-hover.png');
    }, function() {
        $(this).attr('src', '../static/img/main/gallery-link.png');
    });

    //交流
    $('#acPage').hover(function() {
        $(this).attr('src', '../static/img/main/ac-link-hover.png');
    }, function() {
        $(this).attr('src', '../static/img/main/ac-link.png');
    });
});