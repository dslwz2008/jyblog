$(function(){
    $('.date-picker').datetimepicker();
    $('ul#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
    getGalleryImg();
    function getGalleryImg() {
        //get imgList
        cLib.ajax.get({
            'url': 'jyblog/list',
            'data': {
                type: 0
            },
            'success': function(response) {
                if(response.totalCount && response.totalCount>0) {
                    cLib.base.renderPagination($("#imgPaing"),response.totalCount, 12, function(page) {
                        getImgList(0, page-1, 12, function(imgList) {
                            var str = '';
                            for(var i in imgList) {
                                str+='<li>' +
                                '<input type="checkbox" class="pic" id="pic-'+imgList[i]._id.$oid+'">'+
                                '<img class="thumb" src="'+cLib.jyblog.getImgUrl(imgList[i].thumburl)+'">'+
                                '<img class="bigpic" src="'+cLib.jyblog.getImgUrl(imgList[i].imgurl)+'">'+
                                '<p class="desc">'+imgList[i].description+'</p>'+
                                '</li>'
                            }
                            $('#imgList').html(str);
                        })
                    })
                }
            },
            'fail': function(desc) {
                alert(desc)
            }
        });
    }

    //delpic
    $('#delPic').click(function() {
        var delIds = '';
        $('#imgList').find('.pic:checked').each(function() {
            delIds+=this.id.split('-')[1]+',';
        });
        delIds = delIds.substring(0, delIds.length-1);
        cLib.ajax.get({
            'url': 'jyblog/delete/image',
            'data': {
                id: delIds
            },
            'success': function(response) {
                $('.pic:checked').each(function() {
                    $(this).parent().remove();
                });
                alert('成功删除');
            }
        })
    });

    // set cover
    $('#setCover').click(function() {
        var id = $('.pic:checked').attr('id').split('-')[1];
        if(id) {
            cLib.ajax.get({
                'url': 'jyblog/image/setcover',
                'data': {
                    id: id
                },
                'success': function(response) {
                    alert('设置成功');
                },
                'fail': function(desc) {
                    alert(desc)
                }
            })
        } else {
            alert('请选择要设置成封面的图片');
        }
    });

    $('#uploadImage').click(function() {
        $('#uploadPicForm').fadeToggle();
    });

    $('#uploadPicForm').submit(function() {
        // submit the form
        $(this).ajaxSubmit(function() {
            alert('成功上传图片');
            getGalleryImg();
        });
        // return false to prevent normal browser submit and page navigation
        return false;
    });
    $('#submitImg').click(function() {
        var endtime = $('#p-time').datetimepicker('getDate').getTime();
        $('#formtime').val(endtime);
        $('#p-submit').click();
    });

    //del sketch
    $('#delSketch').click(function() {
        var delIds = '';
        $('#caoTuList').find('.pic:checked').each(function() {
            delIds+=this.id.split('-')[1]+',';
        });

        delIds = delIds.substring(0, delIds.length-1);
        cLib.ajax.get({
            'url': 'jyblog/delete/sketch',
            'data': {
                id: delIds
            },
            'success': function(response) {
                $('.pic:checked').each(function() {
                    $(this).parent().remove();
                });
                alert('成功删除');
            }
        })
    });

    getCommunicationImg();
    function getCommunicationImg() {
        //get caotu
        cLib.ajax.get({
            'url': 'jyblog/list',
            'data': {
                type: 1
            },
            'success': function(response) {
                if(response.totalCount && response.totalCount>0) {
                    cLib.base.renderPagination($("#caotuPaing"),response.totalCount, 12, function(page) {
                        getImgList(1,page-1, 12, function(imgList) {
                            var str = '';
                            for(var i in imgList) {
                                str+='<li>' +
                                '<input type="checkbox" class="pic" id="pic-'+imgList[i]._id.$oid+'">'+
                                '<img class="thumb" src="'+cLib.jyblog.getImgUrl(imgList[i].thumburl)+'">'+
                                '<img class="bigpic" src="'+cLib.jyblog.getImgUrl(imgList[i].imgurl)+'">'+
                                '<p class="desc">'+imgList[i].description+'</p>'+
                                '</li>'
                            }
                            $('#caoTuList').html(str);
                        })
                    })
                }
            },
            'fail': function(desc) {
                alert(desc)
            }
        });
    }

    $('#uploadSketchImg').click(function() {
        $('#uploadSketchForm').fadeToggle();
    });

    $('#submitSketchImg').click(function() {
        var endtime = $('#s-time').datetimepicker('getDate').getTime();
        $('#sformtime').val(endtime);
        $('#uploadSketchForm').submit(function() {
            // submit the form
            $(this).ajaxSubmit(function() {
                alert('成功上传图片');
                getCommunicationImg();
            });
            // return false to prevent normal browser submit and page navigation
            return false;
        });
        $('#s-submit').click();
    });

    function getImgList(type, page, npp, fn) {
        cLib.ajax.get({
            'url': 'jyblog/list',
            'data': {
                type: type,  //0 图片 1草图
                page:page,
                npp: npp
            },
            'beforeSend':function(request){
                request.setRequestHeader('Cache-Control','no-cache')
            },
            'success': function(response) {
                if(fn) fn(response.images);
            }
        });
    }

    getLinks();
    function getLinks() {
        cLib.ajax.get({
            'url': 'jyblog/list/link',
            'data': {

            },
            'beforeSend':function(request){
                request.setRequestHeader('Cache-Control','no-cache')
            },
            'success': function(response) {
                if(response.links) {
                    var str = '';
                    for(var i in response.links) {
                        str += '<li>' +
                        '<input type="checkbox" class="linkitem" id="link-'+response.links[i]._id.$oid+'">' +
                        '<a href="'+response.links[i].url+'">'+response.links[i].name+'</a>' +
                        '</li>'
                    }
                    $('#linklist').html(str);
                }
            }
        });
    }

    $('#addlink').click(function() {
        var name = $('#linkname').val();
        var url = $('#linkurl').val();
        cLib.ajax.post({
            'url': 'jyblog/add/link',
            'data': {
                name: name,
                url: url

            },
            'beforeSend':function(request){
                request.setRequestHeader('Cache-Control','no-cache')
            },
            'success': function(response) {
                alert('添加成功');
                getLinks();
            }
        });
    });

    //del sektch
    $('#delUrl').click(function() {
        var delIds = '';
        $('#linklist').find('.linkitem:checked').each(function() {
            delIds+=this.id.split('-')[1]+',';
        });

        delIds = delIds.substring(0, delIds.length-1);
        cLib.ajax.get({
            'url': 'jyblog/delete/link',
            'data': {
                id: delIds
            },
            'success': function(response) {
                alert('成功删除');
                getLinks();
            }
        })
    })
});