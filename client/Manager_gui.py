# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\Manager.ui'
#
# Created: Mon Dec 15 22:20:35 2014
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mainTab = QtGui.QTabWidget(self.centralwidget)
        self.mainTab.setObjectName(_fromUtf8("mainTab"))
        self.tabPictures = QtGui.QWidget()
        self.tabPictures.setObjectName(_fromUtf8("tabPictures"))
        self.mainTab.addTab(self.tabPictures, _fromUtf8(""))
        self.tabSketches = QtGui.QWidget()
        self.tabSketches.setObjectName(_fromUtf8("tabSketches"))
        self.mainTab.addTab(self.tabSketches, _fromUtf8(""))
        self.tabLinks = QtGui.QWidget()
        self.tabLinks.setObjectName(_fromUtf8("tabLinks"))
        self.mainTab.addTab(self.tabLinks, _fromUtf8(""))
        self.gridLayout.addWidget(self.mainTab, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(mainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_refresh = QtGui.QAction(mainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_refresh.setIcon(icon)
        self.action_refresh.setObjectName(_fromUtf8("action_refresh"))
        self.action_exit = QtGui.QAction(mainWindow)
        self.action_exit.setObjectName(_fromUtf8("action_exit"))
        self.action_upload = QtGui.QAction(mainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/upload.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_upload.setIcon(icon1)
        self.action_upload.setObjectName(_fromUtf8("action_upload"))
        self.action_modify = QtGui.QAction(mainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/modify.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_modify.setIcon(icon2)
        self.action_modify.setObjectName(_fromUtf8("action_modify"))
        self.action_delete = QtGui.QAction(mainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.action_delete.setIcon(icon3)
        self.action_delete.setObjectName(_fromUtf8("action_delete"))
        self.menu.addAction(self.action_refresh)
        self.menu.addSeparator()
        self.menu.addAction(self.action_exit)
        self.menu_2.addAction(self.action_upload)
        self.menu_2.addAction(self.action_modify)
        self.menu_2.addAction(self.action_delete)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.toolBar.addAction(self.action_upload)
        self.toolBar.addAction(self.action_modify)
        self.toolBar.addAction(self.action_delete)

        self.retranslateUi(mainWindow)
        self.mainTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "JyBlog 后台管理", None))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tabPictures), _translate("mainWindow", "Tab 1", None))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tabSketches), _translate("mainWindow", "Tab 2", None))
        self.mainTab.setTabText(self.mainTab.indexOf(self.tabLinks), _translate("mainWindow", "页", None))
        self.menu.setTitle(_translate("mainWindow", "文件", None))
        self.menu_2.setTitle(_translate("mainWindow", "操作", None))
        self.toolBar.setWindowTitle(_translate("mainWindow", "toolBar", None))
        self.action_refresh.setText(_translate("mainWindow", "刷新", None))
        self.action_exit.setText(_translate("mainWindow", "退出", None))
        self.action_upload.setText(_translate("mainWindow", "上传", None))
        self.action_modify.setText(_translate("mainWindow", "修改", None))
        self.action_delete.setText(_translate("mainWindow", "删除", None))

import Manager_rc
