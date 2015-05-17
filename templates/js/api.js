/**
 * Item Name :
 * Creater : peijiqiu
 * Email : peijiqiu@gmail.com
 * Created Date : 15/4/12.
 */
var api_domain = 'jyblog';
var api_imgList_get = apiUrlFormat('/image/cover'),
    api_coverImg_get = apiUrlFormat('/image/cover');

var def_img_host = 'http://www.jingyin.name/';
def_default_img = 'img/common/blank100.png';
function apiUrlFormat(url) {
    return api_domain + url;
}

