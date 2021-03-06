# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import tornado.web
import dbengine
import datetime
import base64
import os
import os.path
import util
from commons import *
from bson.json_util import *


class AddImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        # dbengine.visit_count(True)
        items = {}
        # items['_id'] = int(datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
        items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                # print(pic['filename'])
                # print(pic['content_type'])
                uname = util.uuid_name(pic['filename'])
                items['imgurl'] = 'images/' + uname
                with open(IMAGES_DIR + uname, 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                uthumbname = util.uuid_name(pic['filename'])
                items['thumburl'] = 'images/' + uthumbname
                with open(IMAGES_DIR + uthumbname, 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.add_image(items, dbengine.COL_IMAGES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class ModifyImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        # dbengine.visit_count(True)
        items = {}
        items['_id'] = self.get_argument('id')
        uname = util.uuid_name(datetime.datetime.now().strftime('%H%M%S%f'))
        items['imgurl'] = unicode('images/' + uname)
        items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        uthumbname = util.uuid_name(datetime.datetime.now().strftime('%H%M%S%f'))
        items['thumburl'] = unicode('images/' + uthumbname)
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(IMAGES_DIR + uname, 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(IMAGES_DIR + uthumbname, 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.update_image(items, dbengine.COL_IMAGES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class DeleteImageHandler(tornado.web.RequestHandler):
    def get(self):
        # dbengine.visit_count(True)
        imgids = self.get_argument('id')
        for i in imgids.split(','):
            docs = dbengine.get_image_by_id(i, dbengine.COL_IMAGES)
            if len(docs) > 0:
                doc_img = docs[0]
                imgfile = IMAGES_DIR + doc_img['imgurl'].split('/')[-1]
                if os.path.exists(imgfile):
                    os.remove(imgfile)
                thumbfile = IMAGES_DIR + doc_img['thumburl'].split('/')[-1]
                if os.path.exists(thumbfile):
                    os.remove(thumbfile)
                dbengine.remove_image(i, dbengine.COL_IMAGES)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))

class ListHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        dbengine.visit_count(True)
        type = int(self.get_argument('type', 0))
        page = int(self.get_argument('page', -1))
        npp = int(self.get_argument('npp', 9))
        coll = dbengine.COL_IMAGES if type == 0 else dbengine.COL_SKETCHES
        self.set_header('Content-Type', 'application/json')
        self.set_header('Cache-Control', 'no-cache')
        result = {}
        result['code'] = 1
        if type == 1:# sketches , 8 images at most
            images = dbengine.find_all_pictures(coll)[:8]
            # for i in range(8 - len(images)):
            #     doc = {'thumburl' : 'sketches/blank100.png'}
            #     images.append(doc)
            result['totalCount'] = 8
            result['images'] = images
        else:
            if page == -1:
                images = dbengine.find_all_pictures(coll)
                result['totalCount'] = len(images)
                result['images'] = images
            else:
                images = dbengine.get_latest_pictures(coll, page, npp)
                # for i in range(npp - len(images)):
                #     doc = {'thumburl' : 'images/blank200.png'}
                #     images.append(doc)
                result['totalCount'] = dbengine.get_images_number(coll)
                result['images'] = images
        self.write(dumps(result))

class AddSketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        # dbengine.visit_count(True)
        items = {}
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                uname = util.uuid_name(pic['filename'])
                items['imgurl'] = 'sketches/' + uname
                with open(SKETCHES_DIR + uname, 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                uthumbname = util.uuid_name(pic['filename'])
                items['thumburl'] = 'sketches/' + uthumbname
                with open(SKETCHES_DIR + uthumbname, 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.add_image(items, dbengine.COL_SKETCHES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class ModifySketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        # dbengine.visit_count(True)
        items = {}
        items['_id'] = int(self.get_argument('id'))
        items['imgurl'] = self.get_argument('imgurl')
        # items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        items['thumburl'] = self.get_argument('thumburl')
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(SKETCHES_DIR + items['imgurl'], 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(SKETCHES_DIR + items['thumburl'], 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.update_image(items, dbengine.COL_SKETCHES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class DeleteSketchHandler(tornado.web.RequestHandler):
    def get(self):
        # dbengine.visit_count(True)
        imgids = self.get_argument('id')
        for i in imgids.split(','):
            docs = dbengine.get_image_by_id(i, dbengine.COL_SKETCHES)
            if len(docs) > 0:
                doc_img = docs[0]
                imgfile = SKETCHES_DIR + doc_img['imgurl'].split('/')[-1]
                if os.path.exists(imgfile):
                    os.remove(imgfile)
                thumbfile = SKETCHES_DIR + doc_img['thumburl'].split('/')[-1]
                if os.path.exists(thumbfile):
                    os.remove(thumbfile)
                dbengine.remove_image(i, dbengine.COL_SKETCHES)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class AddLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        # dbengine.visit_count(True)
        items = {}
        items['name'] = self.get_argument('name')
        items['url'] = self.get_argument('url')
        result = {}
        dbengine.add_link(items, dbengine.COL_LINKS)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class ModifyLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        # dbengine.visit_count(True)
        items = {}
        items['_id'] = int(self.get_argument('id'))
        items['imgurl'] = self.get_argument('imgurl')
        items['url'] = self.get_argument('url')
        result = {}
        dbengine.update_link(items, dbengine.COL_LINKS)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class DeleteLinkHandler(tornado.web.RequestHandler):
    def get(self):
        # dbengine.visit_count(True)
        linkids = self.get_argument('id')
        for i in linkids.split(','):
            dbengine.remove_link(i, dbengine.COL_LINKS)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))

class CoverImageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        dbengine.visit_count(True)
        doc = dbengine.get_cover_image(dbengine.COL_IMAGES)[0]
        result = {}
        result['code'] = 1
        result['image'] = doc
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class SetCoverHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        imageid = self.get_argument('id')
        dbengine.cancel_cover_image(dbengine.COL_IMAGES)
        dbengine.set_cover_image(imageid, dbengine.COL_IMAGES)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))



class ListLinkHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        dbengine.visit_count(True)
        links = dbengine.get_all_links(dbengine.COL_LINKS)[:8]
        result = {}
        result['code'] = 1
        result['links'] = links
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))

class UserValidateHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        # dbengine.visit_count(True)
        name = self.get_argument('name')
        password = self.get_argument('pwd')
        result = {}
        if name == 'jingyin' and password == '3856975':
            result['code'] = 1
            crypto = base64.b64encode(SECRET)
            result['token'] = crypto
            self.set_cookie(COOKIE_NAME, crypto, expires_days=7)
        else:
            result['message'] = u'user or password error!'
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))


class VisitCountHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        result = {}
        result['code'] = 1
        result['count'] = list(str(dbengine.visit_count(False)))
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(result))

    def post(self, *args, **kwargs):
        pass

