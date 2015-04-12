# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import tornado.web
import dbengine
import datetime
import uuid
import json
import os
import util
from commons import *


class AddImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        items = {}
        items['_id'] = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        uname = util.uuid_name(self.get_argument('imgurl'))
        items['imgurl'] = IMAGES_DIR + uname
        items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        uthumbname = util.uuid_name(self.get_argument('thmburl'))
        items['thmburl'] = IMAGES_DIR + uthumbname
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(items['imgurl'], 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(items['thmburl'], 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.add_image(items, dbengine.COL_IMAGES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class ModifyImageHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        items = {}
        items['_id'] = int(self.get_argument('id'))
        items['imgurl'] = self.get_argument('imgurl')
        items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        items['thmburl'] = self.get_argument('thmburl')
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(IMAGES_DIR + items['imgurl'], 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(IMAGES_DIR + items['thmburl'], 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.update_image(items, dbengine.COL_IMAGES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class DeleteImageHandler(tornado.web.RequestHandler):
    def get(self):
        imgid = int(self.get_argument('id'))
        doc_img = dbengine.get_image_by_id(imgid, dbengine.COL_IMAGES)
        os.remove(IMAGES_DIR + doc_img['imgurl'])
        os.remove(IMAGES_DIR + doc_img['thmburl'])
        dbengine.remove_image(imgid, dbengine.COL_IMAGES)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

class ListHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        type = int(self.get_argument('type', 0))
        page = int(self.get_argument('page', -1))
        npp = int(self.get_argument('npp', 9))
        coll = dbengine.COL_IMAGES if type == 0 else dbengine.COL_SKETCHES
        self.set_header('Content-Type', 'application/json')
        result = {}
        result['code'] = 1
        if page == -1:
            images = dbengine.find_all_pictures(coll)
            result['images'] = json.dumps(images)
        else:
            images = dbengine.get_latest_pictures(coll, page, npp)
            result['images'] = json.dumps(images)
        self.write(result)

class AddSketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        items = {}
        items['_id'] = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        name = self.get_argument('imgurl')
        items['imgurl'] = IMAGES_DIR + str(uuid.uuid5(uuid.NAMESPACE_URL, imgurl))
        # items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        thmburl = self.get_argument('thmburl')
        items['thmburl'] = IMAGES_DIR + uuid.uuid5(uuid.NAMESPACE_URL, thmburl)
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(SKETCHES_DIR + items['imgurl'], 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(SKETCHES_DIR + items['thmburl'], 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.add_image(items, dbengine.COL_SKETCHES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class ModifySketchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        items = {}
        items['_id'] = int(self.get_argument('id'))
        items['imgurl'] = self.get_argument('imgurl')
        # items['cover'] = True if int(self.get_argument('cover')) == 1 else False
        items['thmburl'] = self.get_argument('thmburl')
        items['uploadtime'] = int(self.get_argument('uploadtime'))
        items['description'] = self.get_argument('description', '')
        result = {}
        if self.request.files.get('image') is not None:
            for pic in self.request.files['image']:
                with open(SKETCHES_DIR + items['imgurl'], 'wb') as fp:
                    fp.write(pic['body'])
        if self.request.files.get('thumb') is not None:
            for pic in self.request.files['thumb']:
                with open(SKETCHES_DIR + items['thmburl'], 'wb') as fp:
                    fp.write(pic['body'])
        # result['code'] = 'error'
        #     result['error'] = 'no file upload'
        dbengine.update_image(items, dbengine.COL_SKETCHES)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class DeleteSketchHandler(tornado.web.RequestHandler):
    def get(self):
        imgid = int(self.get_argument('id'))
        doc_img = dbengine.get_image_by_id(imgid, dbengine.COL_SKETCHES)
        os.remove(SKETCHES_DIR + doc_img['imgurl'])
        os.remove(SKETCHES_DIR + doc_img['thmburl'])
        dbengine.remove_image(imgid, dbengine.COL_SKETCHES)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class AddLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        items = {}
        items['_id'] = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        items['imgurl'] = self.get_argument('imgurl')
        items['url'] = self.get_argument('url')
        result = {}
        dbengine.add_link(items, dbengine.COL_LINKS)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class ModifyLinkHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        items = {}
        items['_id'] = int(self.get_argument('id'))
        items['imgurl'] = self.get_argument('imgurl')
        items['url'] = self.get_argument('url')
        result = {}
        dbengine.update_link(items, dbengine.COL_LINKS)
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))


class DeleteLinkHandler(tornado.web.RequestHandler):
    def get(self):
        linkid = int(self.get_argument('id'))
        dbengine.remove_link(linkid, dbengine.COL_LINKS)
        result = {}
        result['code'] = 1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

class CoverImageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        doc = dbengine.get_cover_image(dbengine.COL_IMAGES)[0]
        result = {}
        result['code'] = 1
        result['image'] = doc
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

