#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

import sys
import pymongo

CONN_STRING = "mongodb://192.168.1.10:27017"
# CONN_STRING = "mongodb://128.199.189.87:27017"
DB_NAME = 'jyblog'
COL_IMAGES = 'images'
COL_SKETCHES = 'sketches'
COL_LINKS = 'links'
COL_COMMENTS = 'comments'
COL_VISITS = 'visits'

def get_image_by_id(imageid, collection):
    """从指定的文档中获取指定id的图片信息"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        doc = None

        try:
            doc = pictures.find({'_id':imageid})[0]
        except:
            print "Unexcepted error:", sys.exc_info()[0]

        if doc:
            return doc

def get_latest_pictures(collection, page, num):
    """从指定的文档中获取上传时间最近的num张图片"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        result = []
        cursor = None

        try:
            cursor = pictures.find().sort('uploadtime', pymongo.DESCENDING).skip(page*num).limit(num)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result.append(doc)
            return result


def get_images_number(collection):
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]

        try:
            return pictures.find().count()
        except:
            print "Unexpected error:", sys.exc_info()[0]


def find_all_pictures(collection):
    """return all the pictures in DESCENDING order"""
    with pymongo.MongoClient(CONN_STRING) as conn:
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


def add_image(doc_img, collection):
    """把指定的picture数据存入指定的文档"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            if collection == COL_IMAGES:
                if doc_img['cover'] == True:
                    cursor = pictures.find({'cover':True})
                    for doc in cursor:
                        pictures.update({'_id':doc['_id']}, {"$set":{'cover':False}})
            pictures.insert(doc_img)
        except:
            print "Unexpected error:", sys.exc_info()[0]

def update_image(doc_img, collection):
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            if collection == COL_IMAGES:
                if doc_img['cover'] == True:
                    cursor = pictures.find({'cover':True})
                    for doc in cursor:
                        pictures.update({'_id':doc['_id']}, {"$set":{'cover':False}})
                pictures.update({'_id':doc_img['_id']}, {'$set': {
                    'name':doc_img['name'],
                    'cover':doc_img['cover'],
                    'thumbname':doc_img['thumbname'],
                    'uploadtime':doc_img['uploadtime'],
                    'description':doc_img['description']}
                })
            else:
                pictures.update({'_id':doc_img['_id']}, {'$set': {
                    'name':doc_img['name'],
                    'thumbname':doc_img['thumbname'],
                    'uploadtime':doc_img['uploadtime'],
                    'description':doc_img['description']}
                })
        except:
            print("Unexpected error:", sys.exc_info()[0])

def remove_image(imgid, collection):
    """remove an image"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.remove({'_id':imgid})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def cancel_cover_image(imgid, collection):
    """cancel cover image which will show in the main page by its filename"""
    with pymongo.MongoClient(CONN_STRING, safe=True) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.update({'name':imgid}, {"$set":{'cover':False}})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def set_cover_image(imgid, collection):
    """set cover image which will show in the main page by its filename"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        pictures = db[collection]
        try:
            pictures.update({'_id':imgid}, {"$set":{'cover':True}})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def get_cover_image(collection):
    """get cover image, return at most one document"""
    with pymongo.MongoClient(CONN_STRING) as conn:
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
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        result = []
        cursor = None

        try:
            cursor = links.find().sort('_id', pymongo.DESCENDING)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result.append(doc)
            return result


def add_link(doc_link, collection):
    """把指定的link数据存入指定的文档"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        try:
            links.insert(doc_link)
        except:
            print "Unexpected error:", sys.exc_info()[0]

def update_link(doc_link, collection):
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        try:
            links.update({'_id':doc_link['_id']},{
                '$set':{
                    'name':doc_link['name'],
                    'url':doc_link['url']
                }
            })
        except:
            print "Unexpected error:", sys.exc_info()[0]

def remove_link(linkid, collection):
    """把指定的link数据存入指定的文档"""
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        links = db[collection]
        try:
            links.remove({'_id':linkid})
        except:
            print "Unexpected error:", sys.exc_info()[0]


def visit_count(add):
    with pymongo.MongoClient(CONN_STRING) as conn:
        db = conn[DB_NAME]
        visits = db[COL_VISITS]
        cursor = None

        try:
            cursor = visits.find()
        except:
            print "Unexpected error:", sys.exc_info()[0]

        if cursor:
            for doc in cursor:
                result = int(doc['count'])
                if(add):
                    result += 1
                    visits.update({'_id':doc['_id']}, {'count':result})
                return result

if __name__ == '__main__':
    pass