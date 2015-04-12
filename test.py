# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import requests
import datetime
import time

def test_add_image():
    url = 'http://localhost:8000/add/image'
    files = {'image': open('test/Desert.jpg', 'rb'),
             'thumb':open('test/img (1).jpg', 'rb')}

    data = {'imgurl': 'test1.jpg',
            'cover': 1,
            'thmburl': 'test2.jpg',
            'uploadtime': int(time.time()),
            'description':'something...'}
    r = requests.post(url, data=data, files=files)
    print(r.text)

def test_update_image():
    url = 'http://localhost:8000/update/image'
    files = {'image': open('test/Tulips.jpg', 'rb'),
             'thumb':open('test/img (2).jpg', 'rb')}

    data = {'id':20150408224403,
            'imgurl': 'test3.jpg',
            'cover': 1,
            'thmburl': 'test4.jpg',
            'uploadtime': int(time.time()),
            'description':'something...ABC   \n\n\nasdasd'}
    r = requests.post(url, data=data, files=files)
    print(r.text)

def test_delete_image():
    url = 'http://localhost:8000/delete/image'
    data={'id':20150408224403}
    r = requests.get(url, params = data)
    print(r.url)

def test_add_sketch():
    url = 'http://localhost:8000/add/sketch'
    files = {'image': open('test/Chrysanthemum.jpg', 'rb'),
             'thumb':open('test/img (3).jpg', 'rb')}

    data = {'imgurl': 'test5.jpg',
            'thmburl': 'test6.jpg',
            'uploadtime': int(time.time()),
            'description':'something...ABC   \n\n\nasdasd'}
    r = requests.post(url, data=data, files=files)
    print(r.text)

def test_update_sketch():
    url = 'http://localhost:8000/update/sketch'
    files = {'image': open('test/Hydrangeas.jpg', 'rb'),
             'thumb':open('test/img (4).jpg', 'rb')}

    data = {'id':20150408224404,
            'imgurl': 'test7.jpg',
            'thmburl': 'test8.jpg',
            'uploadtime': int(time.time()),
            'description':'something...ABC   \n\n\nasdasd'}
    r = requests.post(url, data=data, files=files)
    print(r.text)

def test_delete_sketch():
    url = 'http://localhost:8000/delete/sketch'
    data={'id':20150406193344}
    r = requests.get(url, params = data)
    print(r.url)

def test_add_link():
    url = 'http://localhost:8000/add/link'
    data = {'name': 'baidu',
            'url':'http://www.baidu.com'}
    r = requests.post(url, data=data)
    print(r.text)

def test_update_link():
    url = 'http://localhost:8000/update/link'
    data = {'id':20150408224405,
            'name': 'sina',
            'url':'http://www.sina.com.cn'}
    r = requests.post(url, data=data)
    print(r.text)

def test_delete_link():
    url = 'http://localhost:8000/delete/link'
    data={'id':20150406192358}
    r = requests.get(url, params = data)
    print(r.url)

def test_list_image():
    url = 'http://localhost:8000/list'
    data={'type':0}
    r = requests.get(url, params=data)
    print(r.text)
    data={'type':1,'page':1,'npp':1}
    r = requests.get(url, params=data)
    print(r.text)

if __name__ == '__main__':
    test_add_image()
    # test_update_image()
    # test_delete_image()
    # test_add_sketch()
    # test_update_sketch()
    # test_delete_sketch()
    # test_add_link()
    # test_update_link()
    # test_delete_link()
    # test_list_image()
