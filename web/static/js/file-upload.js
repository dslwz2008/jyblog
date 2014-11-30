$(document).ready(function(){
    $('#myModal').modal({keyboard: false,backdrop: 'static'});
    $('.date-picker').datetimepicker();
    $('ul#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
});