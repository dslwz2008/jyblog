/**
 * Item Name : 通用js类库
 * Creater : peijiqiu
 * Email : peijiqiu@gmail.com
 * Created Date : 2014/7/15.
 */
/**
 * @namespace 通用工具函数.
 * @type {{}}
 */
var cLib = {},
    pageId = '#page',
    loadId = '#loading-gif',
    tipId = '#tipDialog',
    cUser = {},
    viewDic = {},
    pageTimer = {}, //定时器全局变量
    ajaxDic = {}, //搜索ajax字典
    freeBookNum = 3, //免费阅读次数
    freeCartoonNum = 3, //免费观看视频次数
    freeDMNum = 1, //  免费阅读电子刊次数
    ajaxLib = {};
(function(lib) {
    //base命名空间下的所有function不依赖任何插件 ，采用原生javascript编写
    base = {
        /**
         * 浏览器类型以及版本判断
         */
        isIE: window.ActiveXObject ? true : false,
        isMozilla: (typeof document.implementation != 'undefined') && (typeof document.implementation.createDocument != 'undefined') && (typeof HTMLDocument != 'undefined'),
        isFirefox: (navigator.userAgent.toLowerCase().indexOf("firefox") != - 1),
        isSafari: (navigator.userAgent.toLowerCase().indexOf("safari") != - 1),
        isOpera: (navigator.userAgent.toLowerCase().indexOf("opera") != - 1),
        isSupportJquery: typeof($)!='undefined' && $ != null,
        ieVersion: (function(){
            //判断ie版本号只到9，ie10及以上会返回false
            var v = 3, div = document.createElement('div'), all = div.getElementsByTagName('i');
            while (
                div.innerHTML = '<!--[if gt IE ' + (++v) + ']><i></i><![endif]-->',
                    all[0]
                ) {
            }
            return v > 4 ? v : false ;
        }()),

        /**
         * 设置cookie
         * @param c_name cookie名称
         * @param value  cookie值
         * @param expiredays 过期时间day
         * @param path cookie路径
         */
        setCookie: function(c_name, value, expiredays, path) {
            var exdate = new Date();
            exdate.setDate(exdate.getDate() + expiredays);
            document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString()) + ((path == null) ? "" : ";path=" + path);
        },

        /**
         * 获取cookie
         * @param c_name cookie名称
         * @returns {*}
         */
        getCookie: function(c_name) {
            if(document.cookie.length > 0) {
                var c_start = document.cookie.indexOf(c_name + "=");
                if(c_start != -1) {
                    c_start = c_start + c_name.length + 1;
                    var c_end = document.cookie.indexOf(";",c_start);
                    if(c_end == -1) { c_end = document.cookie.length; }
                    return unescape(document.cookie.substring(c_start,c_end));
                }
            }
            return "";
        },
        /**
         * 获取URL参数
         * @param name 参数名
         * @returns {*}
         */
        getUrlParam : function(name){
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)","i");
            var r = (window.location.search || window.location.hash).substr(1).match(reg);
            if (r!=null) {
                //将有空格的参数进行解码，负责返回%20...
                return decodeURI(r[2]);
            }
            return null;
        },
        /**
         * 清除字符串左右空格字符
         * @param text string
         * @returns {*}
         */
        trim : function(text){
            if (typeof(text) == "string") {
                return text.replace(/^\s*|\s*$/g, "");
            } else {
                return text;
            }
        },
        /**
         * 判断值是否为空
         * @param val string
         * @returns {*}
         */
        isEmpty : function(val){
            switch (typeof(val)) {
                case 'string':
                    return val.replace(/^\s\s*/, '' ).replace(/\s\s*$/, '' ).length == 0 ? true : false;
                case 'object':
                    return val == null;
                case 'array':
                    return val.length == 0;
                default:
                    return true;
            }
        },
        /**
         * show loading
         */
        showLoading: function() {
            $('body').isLoading({'tpl':''}).css('overflow','hidden');
            $('#loading-circle').show();
        },
        /**
         * hideloading
         */
        hideLoading: function() {
            $('body').isLoading("hide").css('overflow','auto');
            $('#loading-circle').hide();
        },
        /**
         * 长整型转日期
         * @param lmsd
         * @returns {string}
         */
        longToDate:function(lmsd){
            var dateObj = {};
            dateObj.isvalid = false;
            dateObj.date = {};

            if(!isNaN(lmsd)) {
                dateObj.isvalid = true;
                var date = new Date();
                date.setTime(lmsd);
                var day = date.getDate().toString();
                dateObj.date.day = day.length==1? '0'+ day : day;
                var month = (date.getMonth() + 1).toString();
                dateObj.date.month = month.length==1? '0'+ month : month;
                dateObj.date.year = date.getFullYear().toString();
                var hour = date.getHours().toString();
                dateObj.date.h = hour.length==1? '0'+ hour : hour;
                var min = date.getMinutes().toString();
                dateObj.date.m = min.length==1? '0'+ min : min;
                var second = date.getSeconds().toString();
                dateObj.date.s = second.length==1? '0'+ second : second;
                return dateObj.date.year +'-'+dateObj.date.month +'-'+
                    dateObj.date.day;

            } else {
                return '无'
            }
        },
        /**
         * 长整型转时间
         * @param lmsd
         * @returns {string}
         */
        longToTime: function(lmsd) {
            var dateObj = {};
            dateObj.isvalid = false;
            dateObj.date = {};

            if(!isNaN(lmsd)) {
                dateObj.isvalid = true;
                var date = new Date();
                date.setTime(lmsd);
                var day = date.getDate().toString();
                dateObj.date.day = day.length==1? '0'+ day : day;
                var month = (date.getMonth() + 1).toString();
                dateObj.date.month = month.length==1? '0'+ month : month;
                dateObj.date.year = date.getFullYear().toString();
                var hour = date.getHours().toString();
                dateObj.date.h = hour.length==1? '0'+ hour : hour;
                var min = date.getMinutes().toString();
                dateObj.date.m = min.length==1? '0'+ min : min;
                var second = date.getSeconds().toString();
                dateObj.date.s = second.length==1? '0'+ second : second;
                return dateObj.date.year +'-'+dateObj.date.month +'-'+
                    dateObj.date.day+' '+dateObj.date.h+':'+dateObj.date.m+':'+dateObj.date.s;

            } else {
                return '无'
            }
        },
        strEllipsis: function(maxLength, str) {
            if(str.length > maxLength){
                return str.substring(0,maxLength)+'...';
            } else {
                return str;
            }
        },
        /**
         * 创建页码panel
         * @$page p agediv
         * @param nTotal 总条目数
         * @param nPageSize 每页条数
         * @param fn 回调函数
         */
        renderPagination: function($page, nTotal, nPageSize, fn) {
            $page.paging(nTotal, {
                format: "< nnnnnnn! >",
                perpage: nPageSize,
                lapping: 0,
                page: 1,
                onSelect: function(page) {
                    fn(page);
                },
                onFormat: function(type) {
                    switch (type) {
                        case 'block':
                            if (!this.active)
                                return '<span class="disabled">' + this.value + '</span>';
                            else if (this.value != this.page)
                                return '<em><a href="#' + this.value + '">' + this.value + '</a></em>';
                            return '<span class="current">' + this.value + '</span>';

                        case '下一页':

                            if (this.active)
                                return '<a href="#' + this.value + '" class="next">下一页 »</a>';
                            return '<span class="disabled">下一页 »</span>';

                        case '上一页':

                            if (this.active)
                                return '<a href="#' + this.value + '" class="prev">« 上一页</a>';
                            return '<span class="disabled">« 上一页</span>';

                        case 'first':

                            if (this.active)
                                return '<a href="#' + this.value + '" class="first">|<</a>';
                            return '<span class="disabled">|<</span>';

                        case 'last':

                            if (this.active)
                                return '<a href="#' + this.value + '" class="last">>|</a>';
                            return '<span class="disabled">>|</span>';

                        case "leap":

                            if (this.active)
                                return "...";
                            return "";

                        case 'fill':

                            if (this.active)
                                return "...";
                            return "";
                    }
                }
            });
        },
        /**
         * 上传类型验证（只允许上传图片）
         * @param type
         * @returns {boolean}
         */
        fileTypeSupport:function(type){
            var spTypes = ["jpg","jpeg","png","Png"];
            for(var each in spTypes){
                if(spTypes[each]){
                    if(spTypes[each] == type) return true;
                }
            }
            return false;
        },
        /**
         * 清除定时
         */
        clearTimer: function() {
            for (var each in pageTimer) {
                clearInterval(pageTimer[each]);
            }
        },
        //判断字符是否有中文字符
       isHasChn: function(s){
        var patrn= /[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/gi;
        if (!patrn.exec(s)){
            return false;
        }else{
            return true;
        }
    },
    //判断字符是否全是中文字符
       isAllChn :function(str){
            var reg = /^[\u4E00-\u9FA5]+$/;
            if(!reg.test(str)){
                alert("不是中文");
                return false;
            }
            alert("中文");
            return true;
       }
    };

    //common regExp
    regTest = {
        /**
         *  text输入值是否为邮箱
         * @param text
         * @returns {boolean}
         */
        isEmail: function(text) {
            var reg =/.+@.+\..+/i;
            return reg.test(text);
        },
        /**
         * 判断是否为手机号
         * @param text
         * @returns {boolean}
         */
        isMPhoneNum: function(text) {
            var reg = /^(0|86|17951)?(13[0-9]|15[012356789]|18[0-9]|14[57])[0-9]{8}$/;
            return reg.test(text);
        },
        /**
         * 正则过滤表达式，防止sql注入
         * @param s
         * @returns {string}
         */
        filterStr: function(s) {
            var pattern = new RegExp("[%--`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）——| {}【】‘；：”“'。，、？]");       //格式 RegExp("[在中间定义特殊过滤字符]")
            return pattern.test(s);
            //var rs = "";
            //for (var i = 0; i < s.length; i++) {
            //    rs = rs+s.substr(i, 1).replace(pattern, '');
            //}
            //return rs;
        }
    };

    //项目通用函数
    jyblog = {
        /**
         * 格式化图片路径
         * @param cover
         * @returns {string}
         */
        getImgUrl: function(cover) {
            var imgUrl = (cover==''|| cover == null||cover==undefined) ? def_default_img :
                (cover.search('http') ==-1?def_img_host+cover : cover);
            return imgUrl;
        }

    };

    //ajax异步请求
    ajax = {
        get : function(options) {
            var needLogin = true;
            if(options.needLogin == 0) needLogin = false;
            if(needLogin)
            {
                if(!options.data) options.data = {};
                //options.data.token = cUser.token;
            }
            if(options.async == 0) {
                options.isasync = false;
            } else {
                options.isasync = true;
            }

            ajaxLib[options.url] = $.ajax({
                'url': options.url,
                'async': options.isasync,
                'type': 'get',
                'dataType': 'json',
                'data' : options.data,
                'beforeSend':function(jqXHR,settings){
                    jqXHR.setRequestHeader('Cache-Control','no-cache');
                },
                'success': function(response){
                    if(response){
                        switch (response.code){
                            //请求成功
                            case 1:
                                options.success(response);
                                break;
                            default :
                                if(options.fail) {
                                    options.fail(response.message);
                                }
                                if(options.showData) {
                                    options.showData(response)
                                }
                                break;
                        }
                    }
                },
                'complete' : function(jqXHR,textStatus){
                    if(options.loading) $('#loading-gif').hide();
                    if(options.complete) options.complete(jqXHR, textStatus);
                },
                'error':function(jqXHR, textStatus, errorThrown){
                    if(options.error) options.error(jqXHR, textStatus, errorThrown);
                }
            });
            return ajaxLib[options.url];
        },
        post: function(options) {
            var needLogin = true;
            if(options.needLogin == 0) needLogin = false;
            if(needLogin)
            {
                if(!options.data) options.data = {};
                options.data.token = cUser.token;
            }
            options.data.platform_type = 'web_teacher';
            ajaxLib[options.url] = $.ajax({
                'url': options.url,
                'type': 'post',
                'dataType': 'json',
                'data' : options.data,
                'beforeSend':function(jqXHR,settings){
                    if(options.loading) {
                        $(options.loading).isLoading({ text: "Loading" })
                    }
                },
                'success': function(response){
                    if(response){
                        switch (response.code){
                            //请求成功
                            case 1:
                                options.success(response);
                                break;
                            default :
                                if(options.fail) {
                                    options.fail(response.message);
                                }
                                break;

                        }
                        if(options.repexcute) options.repexcute(response);
                    }
                },
                'complete' : function(jqXHR,textStatus){
                    if(options.loading) $(options.loading).isLoading("hide");
                },
                'error':function(jqXHR, textStatus, errorThrown){

                }
            });
            return ajaxLib[options.url];
        }
    };
    lib.base = base;
    lib.regTest = regTest;
    lib.jyblog = jyblog;
    lib.ajax = ajax;
})(cLib);

function clearViews($scoll) {
    $(pageId).html('');
    $('.isloading-overlay').remove();
    for (var each in viewDic) {
        if(each){
            viewDic[each].remove();
        }
    }
//    $('.nicescroll-rails').remove();
}

function clearAjax(name){
    if(name){
        if(ajaxDic[name])
        {
            ajaxDic[name].abort();
        }
    }else{
        for (var each in ajaxDic) {
            var ajax = ajaxDic[each];
            if(ajax) ajax.abort();
        }
    }
}

