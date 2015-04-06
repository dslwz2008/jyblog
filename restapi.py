# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import tornado.web
import dbengine
import datetime
import json
from commons import *

class AddImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        items = {}
        items['_id'] = self.get_argument('_id')
        items['name'] = self.get_argument('name')
        items['cover'] = self.get_argument('cover')
        items['thumbname'] = self.get_argument('thumbname')
        items['uploadtime'] = self.get_argument('uploadtime', datetime.datetime.now())
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(IMAGES_DIR + items['name'], 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(IMAGES_DIR + items['name'], 'wb') as fp:
                    fp.write(pic['body'])
        #     result['status'] = 'error'
        #     result['error'] = 'no file upload'
        print(dbengine.add_image(items, dbengine.COL_IMAGES))
        result['status'] = 'ok'
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

class ModifyImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        pass

class DeleteImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class AddSketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class ModifySketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class DeleteSketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class AddLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class ModifyLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class DeleteLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        value = self.get_cookie(COOKIE_NAME)
        if not value:
            self.redirect('login')
            return

        secret_str = base64.b64decode(value)
        if secret_str == SECRET:
            self.render('fileupload.html', error='', items=None)
        else:
            self.redirect('login')

    def post(self):
        target = self.get_argument('target')
        # upload images
        if target == dbengine.COL_IMAGES:
            if not self.request.files or not self.request.files.get('picture') or not self.request.files.get(
                    'thumbnail'):
                error_nofile = u'没有选择图片文件'
                self.render('fileupload.html', error=error_nofile, items=None)
                return
            items = self.upload_image_to_collection(dbengine.COL_IMAGES)
            self.render('fileupload.html', error='', items=items.values())
        # upload sketches
        elif target == dbengine.COL_SKETCHES:
            if not self.request.files or not self.request.files.get('picture') or not self.request.files.get(
                    'thumbnail'):
                error_nofile = u'没有选择图片文件'
                self.render('fileupload.html', error=error_nofile, items=None)
                return
            items = self.upload_image_to_collection(dbengine.COL_SKETCHES)
            self.render('fileupload.html', error='', items=items.values())
        # upload links
        elif target == dbengine.COL_LINKS:
            # if not self.request.files or not self.request.files.get('picture'):
            # error_nofile = u'没有选择图片文件'
            #     self.render('fileupload.html', error = error_nofile,  items = None)
            #     return
            if not self.get_argument('name') or not self.get_argument('url'):
                error_params = u'缺少必要的参数'
                self.render('fileupload.html', error=error_params, items=None)
            items = self.upload_link_to_collection(dbengine.COL_LINKS)
            self.render('fileupload.html', error='', items=items.values())
        # further
        elif target == 'comments':
            # not yet
            pass

    def upload_link_to_collection(self, collection):
        items = {}
        items['name'] = self.get_argument('name')
        items['url'] = self.get_argument('url')
        if self.request.files.get('picture') is not None:
            for pic in self.request.files['picture']:
                # 要去掉名字中间的空格
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

        # 全部图片均直接存储在数据库collection中
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
