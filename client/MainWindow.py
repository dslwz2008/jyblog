# -*-coding:utf-8-*-
# Authoe: Shen Shen
# Email: dslwz2002@163.com
__author__ = 'Shen Shen'

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Manager_gui import Ui_mainWindow


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class BlogManager(QMainWindow, Ui_mainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.mainTab.setTabText(0, _fromUtf8('图片管理'))
        self.mainTab.setTabText(1, _fromUtf8('草图管理'))
        self.mainTab.setTabText(2, _fromUtf8('链接管理'))

def main():
    app = QApplication(sys.argv)

    manager = BlogManager()
    manager.showMaximized()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()