# -*- coding:utf-8 -*- 

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import util
import dbengine
import datetime
import base64
import Image
import json
from bson.binary import Binary

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

settings = {
    "static_path" : os.path.join(os.path.dirname(__file__), "static"), 
    "template_path" : os.path.join(os.path.dirname(__file__), "templates")
}

#图片和缩略图都放在这个文件夹中
IMAGES_DIR = "static/imagedb/images/"
IMAGES_THUMB_DIR = "static/imagedb/images_thumb/"
SKETCHES_DIR = "static/imagedb/sketches/"
SKETCHES_THUMB_DIR = "static/imagedb/sketches_thumb/"
LINKS_IMG_DIR = "static/imagedb/links_img/"
USERNAME = "jingyin"
PASSWORD = "3856975"
SECRET = PASSWORD + USERNAME
COOKIE_NAME = 'crypto'
ERROR_NO_DESCRIPTION = u'这家伙很懒，没有留下任何描述'

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # doc = dbengine.get_latest_pictures(dbengine.COL_IMAGES, 1)[0]
        doc = dbengine.get_cover_image(dbengine.COL_IMAGES)[0]
        filename = IMAGES_DIR + doc['name']
        # #先检查缓存中是不是存在
        # if not os.path.isfile(filename):
        #     util.save_binary_to_file(doc['data'], filename)
        self.render('main.html', filename = filename, desc = doc.get('description', ERROR_NO_DESCRIPTION))

class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        value = self.get_cookie(COOKIE_NAME)
        if not value:
            self.redirect('login')
            return

        secret_str = base64.b64decode(value)
        if secret_str == SECRET:
            self.render('fileupload.html', error = '',  items = None)
        else:
            self.redirect('login')
    def post(self):
        target = self.get_argument('target')
        # upload images
        if target == dbengine.COL_IMAGES:
            if not self.request.files or not self.request.files.get('picture') or not self.request.files.get('thumbnail'):
                error_nofile = u'没有选择图片文件'
                self.render('fileupload.html', error = error_nofile,  items = None)
                return
            items = self.upload_image_to_collection(dbengine.COL_IMAGES)
            self.render('fileupload.html', error = '', items = items.values())
        # upload sketches
        elif target == dbengine.COL_SKETCHES:
            if not self.request.files or not self.request.files.get('picture') or not self.request.files.get('thumbnail'):
                error_nofile = u'没有选择图片文件'
                self.render('fileupload.html', error = error_nofile,  items = None)
                return
            items = self.upload_image_to_collection(dbengine.COL_SKETCHES)
            self.render('fileupload.html', error = '', items = items.values())
        # upload links
        elif target == dbengine.COL_LINKS:
            if not self.request.files or not self.request.files.get('picture'):
                error_nofile = u'没有选择图片文件'
                self.render('fileupload.html', error = error_nofile,  items = None)
                return
            if not self.get_argument('name') or not self.get_argument('url'):
                error_params = u'缺少必要的参数'
                self.render('fileupload.html', error = error_params,  items = None)
            items = self.upload_link_to_collection(dbengine.COL_LINKS)
            self.render('fileupload.html', error = '', items = items.values())
        # further
        elif target == 'comments':
            #not yet
            pass

    def upload_link_to_collection(self, collection):
        items = {}
        items['name'] = self.get_argument('name')
        items['url'] = self.get_argument('url')
        for pic in self.request.files['picture']:
            #要去掉名字中间的空格
            filename = items['imagename'] = ''.join(pic['filename'].split(' '))
            # items['imagedata'] = Binary(pic['body'])
            with open(LINKS_IMG_DIR + filename, 'wb') as fp:
                fp.write(pic['body'])
        dbengine.add_link(items, collection)
        return items

    def upload_image_to_collection(self, collection):
        items = {}
        images_dir = ''
        thumbnail_dir = ''
        if collection == dbengine.COL_IMAGES:
            images_dir = IMAGES_DIR
            thumbnail_dir = IMAGES_THUMB_DIR
        else:
            images_dir = SKETCHES_DIR
            thumbnail_dir = SKETCHES_THUMB_DIR

        #全部图片均直接存储在数据库collection中
        for pic in self.request.files['picture']:
            #要去掉名字中间的空格
            filename = items['name'] = ''.join(pic['filename'].split(' '))
            # items['data'] = Binary(pic['body'])
            with open(images_dir + filename, 'wb') as fp:
                fp.write(pic['body'])
        
        for tn in self.request.files['thumbnail']:
            #要去掉名字中间的空格
            filename = items['thumbname'] = ''.join(tn['filename'].split(' '))
            # items['thumbdata'] = Binary(tn['body'])
            with open(thumbnail_dir + filename, 'wb') as fp:
                fp.write(tn['body'])

        if self.get_argument('uploadtime'):
            upload_time = self.get_argument('uploadtime')
            items['uploadtime'] = util.datetime_from_string(upload_time)
        else:
            items['uploadtime'] = datetime.datetime.now()
            
        if self.get_argument('description'):
            desc = self.get_argument('description')
            items['description'] = desc
        
        # if cover image exists
        cvr_img = dbengine.get_cover_image(collection)
        if len(cvr_img) != 0:
            dbengine.cancel_cover_image(cvr_img[0], collection)
        items['cover'] = True
        dbengine.add_image(items, collection)
        return items

class GalleryHandler(tornado.web.RequestHandler):
    def get(self):
        pictures = dbengine.find_all_pictures(dbengine.COL_IMAGES)
        #这里存放缩略图，不用取大图
        thumbnames = []
        fullnames = []
        for pic in pictures:
            fullnames.append(pic['name'])
            #need to display
            thumbfile = IMAGES_THUMB_DIR + pic['thumbname']
            thumbnames.append(thumbfile)
        #计算空白页的数量
        whole = util.get_min_wholepage_mount(len(pictures))
        self.render('gallery.html', thumbnames = thumbnames,
                    fullnames = fullnames, blank_count = whole - len(pictures))

class PictureHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')
        doc = dbengine.get_picture_by_name(dbengine.COL_IMAGES, name)
        filename = IMAGES_DIR + name
        #print filename
        self.render('picture.html', filename = filename, desc = doc.get('description', ERROR_NO_DESCRIPTION))
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
        value = self.get_cookie('test')
        #print value
        self.render('communication.html')

class UserValidateHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name')
        password = self.get_argument('pwd')
        result = {}
        if name == 'jingyin' and password == '3856975':
            result['status'] = 'ok'
            crypto = base64.b64encode(SECRET)
            self.set_cookie(COOKIE_NAME, crypto, expires_days = 7)
        else:
            result['status'] = 'error'
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

class SubmitCommentHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name', u'无名氏')
        comment = self.get_argument('comment')
        doc_comment = {'name':name, 'comment':comment}
        dbengine.add_comment(comment, dbengine.COL_COMMENTS)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/fileupload', FileUploadHandler),
                  (r'/submit-comment', SubmitCommentHandler),
                  (r'/login', LoginHandler),
                  (r'/validate', UserValidateHandler),
                  (r'/picture', PictureHandler),
                  (r'/gallery', GalleryHandler),
                  (r'/communication', CommunicationHandler),
                  (r'/main', MainHandler), 
                  (r'/', IndexHandler),
                  ], **settings
                  )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
