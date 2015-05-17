/**
 * Item Name :
 * Creater : peijiqiu
 * Email : peijiqiu@gmail.com
 * Created Date : 15/4/25.
 */
$(function() {
    var url = getUrlParam('url');
    var desc = getUrlParam('desc');
    $('#cover').html('<img id="coverPic" src="'+cLib.jyblog.getImgUrl(url)+'">');
    $('#desc').text(desc);

    function getUrlParam (name){
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)","i");
        var r = (window.location.search || window.location.hash).substr(1).match(reg);
        if (r!=null) {
            //将有空格的参数进行解码，负责返回%20...
            return decodeURI(r[2]);
        }
        return null;
    }
});