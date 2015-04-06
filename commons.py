# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

# 图片和缩略图都放在这个文件夹中
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
PAGE_VIEWS = 10000

# Database
CONN_STRING = "mongodb://128.199.189.87"
DB_NAME = 'jyblog'
COL_IMAGES = 'images'
COL_SKETCHES = 'sketches'
COL_LINKS = 'links'
COL_COMMENTS = 'comments'