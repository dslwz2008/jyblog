#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

import sys
import pymongo
from bson.binary import Binary
from bson.objectid import ObjectId

CONN_STRING = "mongodb://128.199.189.87"
DB_NAME = 'jyblog'
COL_IMAGES = 'images'
COL_SKETCHES = 'sketches'
COL_LINKS = 'links'
COL_COMMENTS = 'comments'

def get_picture_by_name(collection, name):
    """从指定的文档中获取指定名字的图片信息"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        doc = None

        try:
            doc = pictures.find({'name':name})[0]
        except:
            print "Unexcepted error:", sys.exc_info()[0]

        if doc:
            return doc

def get_latest_pictures(collection, num):
    """从指定的文档中获取上传时间最近的num张图片"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        result = []
        cursor = None

        try:
            cursor = pictures.find().sort('uploadtime', pymongo.DESCENDING).limit(num)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result.append(doc)
            return result


def find_all_pictures(collection):
    """return all the pictures in DESCENDING order"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        result = []
        cursor = None

        try:
            cursor = pictures.find().sort('uploadtime', pymongo.DESCENDING)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result.append(doc)
            return result


def add_image(doc_picture, collection):
    """把指定的picture数据存入指定的文档"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.insert(doc_picture)
        except:
            print "Unexpected error:", sys.exc_info()[0]


def remove_image(img_name, collection):
    """remove an image"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.remove({'name':img_name})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def cancel_cover_image(doc, collection):
    """cancel cover image which will show in the main page by its filename"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.update({'name':doc['name']}, {"$set":{'cover':False}})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def set_cover_image(name, collection):
    """set cover image which will show in the main page by its filename"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.update({'name':name}, {"$set":{'cover':True}})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def get_cover_image(collection):
    """get cover image, return at most one document"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        result = []
        cursor = None
        try:
            cursor = pictures.find({'cover':True})
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result.append(doc)
            return result


def get_all_links(collection):
    """return all the pictures in DESCENDING order"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        result = []
        cursor = None

        try:
            cursor = links.find().sort('name', pymongo.DESCENDING)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result.append(doc)
            return result


def add_link(doc_link, collection):
    """把指定的link数据存入指定的文档"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        try:
            links.insert(doc_link)
        except:
            print "Unexpected error:", sys.exc_info()[0]


def remove_link(link_name, collection):
    """把指定的link数据存入指定的文档"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        try:
            links.remove({'name':link_name})
        except:
            print "Unexpected error:", sys.exc_info()[0]


# def test_binary():
#     with pymongo.Connection(CONN_STRING, safe=True) as conn:
#         db = conn[DB_NAME]
#         links = db['links']
#         image = open('./static/pictures/200910310.jpg', 'rb')
#         links.insert({'name':'a cow', 'image':Binary(image.read()),
#                       'url':'http://www.ytxwz.com'})
#
# def test_read_picture():
#     with pymongo.Connection(CONN_STRING, safe=True) as conn:
#         db = conn[DB_NAME]
#         links = db['links']
#         entry = links.find_one()
#         fp = open('./static/pictures/test1.png', 'w')
#         fp.write(entry['image'])

# cpmments is not used in version 1.0
def add_comment(doc_comment, collection):
    """添加评论"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        comments = db[collection]
        try:
            comments.insert(doc_comment)
        except:
            print "Unexpected error:", sys.exc_info()[0]

def add_reply_to_comment(str_id, collection, reply):
    """给评论添加回复"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        comments = db[collection]
        try:
            comments.update({'_id':ObjectId(str_id)},
                {'$push':{'replies':reply}})
        except:
            print "Unexpected error:", sys.exc_info()[0]

def get_comment(collection):
    """添加评论"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        comments = db[collection]
        try:
            result = comments.find_one({'_id':ObjectId('5219c638421aa904e041cfae')})
            print(result)
        except:
            print "Unexpected error:", sys.exc_info()[0]

def delete_comment(str_id, collection):
    """删除指定的评论"""
    with pymongo.Connection(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        comments = db[collection]
        try:
            comments.remove({'_id':ObjectId(str_id)})
        except:
            print "Unexpected error:", sys.exc_info()[0]

if __name__ == '__main__':
#    print find_all_pictures()
#    add_picture({u'thumbname': u'thumb_aaa.jpg', 
#    u'uploadtime': u'123',  
#    u'name': u'xbox360.jpg', 
#    u'description': u'another game machine'})
    #print get_latest_pictures(5)
    #print get_picture_by_name('IMAG0013.jpg')
    #test_binary()
    #test_read_picture()
    # add_comment({u'name':u"阿萨德", u'comment':u'不错呀'}, COL_COMMENTS)
    # add_comment({u'name':u"小数", u'comment':u'不错呀'}, COL_COMMENTS)
    # add_comment({u'name':u"天天", u'comment':u'不错呀'}, COL_COMMENTS)
    #get_comment(COL_COMMENTS)
    # add_reply_to_comment('5219c638421aa904e041cfae', COL_COMMENTS, u'通过pymongo添加')
    pass