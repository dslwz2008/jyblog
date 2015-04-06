/**
 * Created with JetBrains WebStorm.
 * User: peijiqiu
 * Date: 13-4-14
 * Time: 下午9:49
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function() {
    //一级导航hover图片变换
    //首页
    $('#indexPage').hover(function() {
        $(this).attr('src','../static/img/main/index-link-hover.png');
    }, function() {
        $(this).attr('src','../static/img/main/index-link.png')
    });

    //画廊
    $('#galleryPage').hover(function() {
        $(this).attr('src','../static/img/main/gallery-link-hover.png');
    }, function() {
        $(this).attr('src','../static/img/main/gallery-link.png');
    });

    //交流
    $('#acPage').hover(function() {
        $(this).attr('src','../static/img/main/ac-link-hover.png');
    }, function() {
        $(this).attr('src','../static/img/main/ac-link.png');
    })


});



