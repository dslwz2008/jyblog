/**
 * Item Name :
 * Creater : peijiqiu
 * Email : peijiqiu@gmail.com
 * Created Date : 15/4/20.
 */
$(function() {
    $.ajax({
        'url': 'jyblog/image/cover',
        'async': true,
        'type': 'get',
        'dataType': 'json',
        'data': {},
        'success': function (response) {
            if(response.image) {
                $('#cover').html('<img id="coverPic" src="'+cLib.jyblog.getImgUrl(response.image.imgurl)+'">')
                $('#desc').text(response.image.description);
            }
        },
        'complete': function (jqXHR, textStatus) {

        },
        'error': function (jqXHR, textStatus, errorThrown) {

        }
    })
});