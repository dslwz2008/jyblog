#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

import tempfile
import datetime
from PIL import Image

def get_min_wholepage_mount(count, mount_per_page=12):
    """计算比当前数量多的最小的满页数量"""
    i = 1
    result = 0
    while True:
        result = mount_per_page * i
        if result < count:
            i = i + 1
        else:
            break
    return result

# def upload_and_delete(key, localpath):
#     """upload local file to S3, then delete local file"""
#     key = s3engine.store_data_from_filename(key, localpath)
#     print 'upload success!' if key else 'upload failed!'
#     os.remove(localpath)
#     print 'delete local file successfully!'

# def upload_delete_in_new_thread(key, localpath):
#     """upload local file to S3, then delete local file in another thread"""
#     thread.start_new_thread(upload_and_delete, (key, localpath))

def save_file(file, path, prefix=''):
    """save file to the path with prefix.
    file is an tornado.httputil.HTTPFile instance."""
    filename = file['filename']
    tf = tempfile.NamedTemporaryFile()
    tf.write(file['body'])
    tf.seek(0)
    img = Image.open(tf.name)
    img.save(path + prefix + filename)
    tf.close()

def datetime_from_string(timestr, format = '%m/%d/%Y %H:%M'):
    """construct datetime instance from format string"""
    return datetime.datetime.strptime(timestr, format)
    
def datetime_to_string(dt, format = '%m/%d/%Y %H:%M'):
    """convert datetime instance to string object"""
    return dt.strftime(format)

def save_binary_to_file(binary, filename):
    """把二进制流存成指定的文件"""
    fp = open(filename, 'w')
    fp.write(binary)

if __name__ == '__main__':
    print get_min_wholepage_mount(2)
    print get_min_wholepage_mount(13)
    print get_min_wholepage_mount(24)
