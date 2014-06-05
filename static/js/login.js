/**
 * Created with JetBrains WebStorm.
 * User: 文君
 * Date: 13-7-28
 * Time: 下午9:08
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function() {
    $('#myModal').modal({keyboard: false,backdrop: 'static'});
    //login
    $('#login').click(function() {
        var name = $('#name').val();
        var pwd = $('#pwd').val();
        var args = {
            name : name,
            pwd : pwd
        };
        $.ajax({
            url : '/validate',
            type : 'POST',
            data : args,
            success : function(response) {
                if(response.status == 'ok') {
                    window.location.href = 'fileupload';
                } else {
                    alert('用户名或密码错误');
                }
            },
            error : function() {
                alert('网络错误!');
            }
        })
    })
});
