/**
 * Item Name :
 * Creater : peijiqiu
 * Email : peijiqiu@gmail.com
 * Created Date : 15/4/25.
 */
$(function() {
    cLib.ajax.get({
        'url': 'jyblog/list',
        'data': {
            type: 0,  //0 图片 1草图
            page:0,
            npp: 1
        },
        'success': function(response) {
            if(response.totalCount && response.totalCount>0) {
                cLib.base.renderPagination($("#paging"),response.totalCount, 12, function(page) {
                    getImgList(page-1, 12, function(imgList) {
                        var str = '';
                        for(var i=0;i<12;i++) {
                            if(imgList[i] != undefined) {
                                str+='<li><a target="_blank" href="picture.html?url='+imgList[i].imgurl+'&desc='+imgList[i].description+'"><img src="'+cLib.jyblog.getImgUrl(imgList[i].thumburl)+'"></a></li>'
                            } else {
                                str +='<li></li>'
                            }
                        }
                        $('#imgList').html(str);
                    })
                })
            }
        }
    });

    function getImgList(page, npp, fn) {
        cLib.ajax.get({
            'url': 'jyblog/list',
            'data': {
                type: 0,  //0 图片 1草图
                page:page,
                npp: npp
            },
            'success': function(response) {
                if(fn) fn(response.images);
            }
        });
    }

});