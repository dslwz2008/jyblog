/**
 * Item Name :
 * Creater : peijiqiu
 * Email : peijiqiu@gmail.com
 * Created Date : 15/4/25.
 */
$(function() {

    //get skecters
    cLib.ajax.get({
        'url': 'jyblog/list',
        'data': {
            type: 1
        },
        'success': function(response) {
            if(response.images && response.images.length>0) {
                var str = '';
                for(var i in response.images) {
                    str += '<li><img src="'+cLib.jyblog.getImgUrl(response.images[i].thumburl)+'"></li>'
                }
                $('#sketchList').html(str);
            }
        }
    });

    //get links
    cLib.ajax.get({
        'url': 'jyblog/list/link',
        'data': {

        },
        'success': function(response) {
            if(response.links) {
                var str = '';
                for(var i=0;i<8;i++) {
                    if(response.links[i] != undefined) {
                        str+='<li><a target="_blank" href="'+response.links[i].url+'">'+response.links[i].name+'</a></li>'
                    } else {
                        str +='<li></li>'
                    }
                }

                $('#linkList').html(str);
            }
        }
    });

    //get count
    cLib.ajax.get({
        'url': 'jyblog/visitcount',
        'data': {

        },
        'success': function(response) {
            if(response.count && response.count.length > 0) {
                var str = '';
                for(var i in response.count) {
                    str+='<li>'+response.count[i]+'</li>'
                }
            }
            $('#count').html(str);
        }
    });
});