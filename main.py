# -*- coding:utf-8 -*- 

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import util
import dbengine
import base64
import json
import restapi
from commons import *
from bson.binary import Binary

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")
}

def accum_page_views():
    global PAGE_VIEWS
    PAGE_VIEWS += 1


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        accum_page_views()
        self.render('index.html')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        accum_page_views()
        doc = dbengine.get_cover_image(dbengine.COL_IMAGES)[0]
        filename = IMAGES_DIR + doc['name']
        self.render('main.html', filename=filename, desc=doc.get('description', ERROR_NO_DESCRIPTION))


class GalleryHandler(tornado.web.RequestHandler):
    def get(self):
        accum_page_views()
        pictures = dbengine.find_all_pictures(dbengine.COL_IMAGES)
        # 这里存放缩略图，不用取大图
        thumbnames = []
        fullnames = []
        for pic in pictures:
            fullnames.append(pic['name'])
            #need to display
            thumbfile = IMAGES_THUMB_DIR + pic['thumbname']
            thumbnames.append(thumbfile)
        #计算空白页的数量
        whole = util.get_min_wholepage_mount(len(pictures))
        self.render('gallery.html', thumbnames=thumbnames,
                    fullnames=fullnames, blank_count=whole - len(pictures))


class PictureHandler(tornado.web.RequestHandler):
    def get(self):
        accum_page_views()
        pic_type = self.get_argument('type')
        collection = dbengine.COL_IMAGES
        images_dir = IMAGES_DIR
        if pic_type == 'sketch':
            collection = dbengine.COL_SKETCHES
            images_dir = SKETCHES_DIR
        name = self.get_argument('name')
        doc = dbengine.get_picture_by_name(collection, name)
        filename = images_dir + name
        # print filename
        self.render('main.html', filename=filename, desc=doc.get('description', ERROR_NO_DESCRIPTION))
        # #直接返回图片数据的版本
        # self.set_header("Cache-Control", "public")
        # self.set_header('Content-Type', 'image/jpeg')
        # data = open(filename,'rb').read()
        # self.set_header('Content_Length', len(data))
        # self.write(data)
        # #利用ajax请求返回返回图片宽、高、路径等信息
        # pic = Image.open(filename)
        # result = {}
        # if pic:
        #     result['width'] = pic.size[0]
        #     result['height'] = pic.size[1]
        #     result['filename'] = filename
        # else:
        #     result['error'] = 'sorry...'
        # self.set_header('Content-Type', 'application/json')
        # self.write(json.dumps(result))


class CommunicationHandler(tornado.web.RequestHandler):
    def get(self):
        accum_page_views()
        # value = self.get_cookie('test')
        # print value
        sketches = dbengine.find_all_pictures(dbengine.COL_SKETCHES)
        rslt_skchs = sketches[0:8] if len(sketches) > 8 else sketches
        links = dbengine.get_all_links(dbengine.COL_LINKS)
        rslt_links = links[0:8] if len(links) > 8 else links
        view_count = util.pageview_to_string(PAGE_VIEWS)
        self.render('ac.html', sketches=rslt_skchs, links=rslt_links, count=view_count)


class UserValidateHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name')
        password = self.get_argument('pwd')
        result = {}
        if name == 'jingyin' and password == '3856975':
            result['status'] = 'ok'
            crypto = base64.b64encode(SECRET)
            self.set_cookie(COOKIE_NAME, crypto, expires_days=7)
        else:
            result['status'] = 'error'
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')


class ManageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('manage.html')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/add/image', restapi.AddImageHandler),
                  (r'/modify/image', restapi.ModifyImageHandler),
                  (r'/delete/image', restapi.DeleteImageHandler),
                  (r'/add/sketch', restapi.AddSketchHandler),
                  (r'/modify/sketch', restapi.ModifySketchHandler),
                  (r'/delete/sketch', restapi.DeleteSketchHandler),
                  (r'/add/link', restapi.AddLinkHandler),
                  (r'/modify/link', restapi.ModifySketchHandler),
                  (r'/delete/link', restapi.DeleteLinkHandler),
                  (r'/manage', ManageHandler),
                  (r'/login', LoginHandler),
                  (r'/validate', UserValidateHandler),
                  (r'/picture', PictureHandler),
                  (r'/gallery', GalleryHandler),
                  (r'/ac', CommunicationHandler),
                  (r'/main', MainHandler),
                  (r'/', IndexHandler),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
