# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import requests
import datetime

def test_add_image():
    url = 'http://localhost:8000/add/image'
    files = {'image': open('test/Desert.jpg', 'rb'),
             'thumb':open('test/img (1).jpg')}
    time = datetime.datetime.now()
    data = {'_id':int(time.strftime('%Y%m%d%H%M%S')),
            'name': 'test1.jpg',
            'cover': 0,
            'thumbname': 'test2.jpg',
            'uploadtime': time,
            'description':'somwthing...'}
    r = requests.post(url, data=data, files=files)
    print(r.text)

if __name__ == '__main__':
    test_add_image()
