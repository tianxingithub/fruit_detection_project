# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FruitPrevision.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 669)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fruitLog = QtWidgets.QTextBrowser(self.centralwidget)
        self.fruitLog.setGeometry(QtCore.QRect(10, 390, 771, 211))
        self.fruitLog.setObjectName("fruitLog")
        self.fruitPic = QtWidgets.QGraphicsView(self.centralwidget)
        self.fruitPic.setGeometry(QtCore.QRect(480, 60, 301, 301))
        self.fruitPic.setObjectName("fruitPic")
        self.fruitInfo = QtWidgets.QTextBrowser(self.centralwidget)
        self.fruitInfo.setGeometry(QtCore.QRect(10, 60, 441, 301))
        self.fruitInfo.setObjectName("fruitInfo")
        self.count0 = QtWidgets.QTextBrowser(self.centralwidget)
        self.count0.setGeometry(QtCore.QRect(10, 10, 131, 41))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.count0.setFont(font)
        self.count0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.count0.setAutoFillBackground(False)
        self.count0.setObjectName("count0")
        self.count1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.count1.setGeometry(QtCore.QRect(160, 10, 131, 41))
        self.count1.setObjectName("count1")
        self.count2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.count2.setGeometry(QtCore.QRect(480, 10, 131, 41))
        self.count2.setObjectName("count2")
        self.count3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.count3.setGeometry(QtCore.QRect(320, 10, 131, 41))
        self.count3.setObjectName("count3")
        self.count4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.count4.setGeometry(QtCore.QRect(650, 10, 131, 41))
        self.count4.setObjectName("count4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.fruitKind = QtWidgets.QMenu(self.menubar)
        self.fruitKind.setObjectName("fruitKind")
        self.fruitStatus = QtWidgets.QMenu(self.menubar)
        self.fruitStatus.setObjectName("fruitStatus")
        self.help = QtWidgets.QMenu(self.menubar)
        self.help.setObjectName("help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionApple = QtWidgets.QAction(MainWindow)
        self.actionApple.setObjectName("actionApple")
        self.actionBanana = QtWidgets.QAction(MainWindow)
        self.actionBanana.setObjectName("actionBanana")
        self.actionOrange = QtWidgets.QAction(MainWindow)
        self.actionOrange.setObjectName("actionOrange")
        self.actionPineApple = QtWidgets.QAction(MainWindow)
        self.actionPineApple.setObjectName("actionPineApple")
        self.actionMonago = QtWidgets.QAction(MainWindow)
        self.actionMonago.setObjectName("actionMonago")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionEnd = QtWidgets.QAction(MainWindow)
        self.actionEnd.setObjectName("actionEnd")
        self.actionStep = QtWidgets.QAction(MainWindow)
        self.actionStep.setObjectName("actionStep")
        self.infome = QtWidgets.QAction(MainWindow)
        self.infome.setObjectName("infome")
        self.about = QtWidgets.QAction(MainWindow)
        self.about.setObjectName("about")
        self.running = QtWidgets.QAction(MainWindow)
        self.running.setObjectName("running")
        self.fruitKind.addAction(self.actionApple)
        self.fruitKind.addAction(self.actionBanana)
        self.fruitKind.addAction(self.actionOrange)
        self.fruitKind.addAction(self.actionMonago)
        self.fruitKind.addAction(self.actionPineApple)
        self.fruitStatus.addAction(self.actionStart)
        self.fruitStatus.addAction(self.actionEnd)
        self.fruitStatus.addAction(self.actionStep)
        self.help.addAction(self.about)
        self.help.addAction(self.running)
        self.menubar.addAction(self.fruitStatus.menuAction())
        self.menubar.addAction(self.fruitKind.menuAction())
        self.menubar.addAction(self.help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fruitKind.setTitle(_translate("MainWindow", "筛选的水果类别"))
        self.fruitStatus.setTitle(_translate("MainWindow", "状态"))
        self.help.setTitle(_translate("MainWindow", "帮助"))
        self.actionApple.setText(_translate("MainWindow", "Apple"))
        self.actionBanana.setText(_translate("MainWindow", "Banana"))
        self.actionOrange.setText(_translate("MainWindow", "Orange"))
        self.actionPineApple.setText(_translate("MainWindow", "PineApple"))
        self.actionMonago.setText(_translate("MainWindow", "Mongo"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionEnd.setText(_translate("MainWindow", "End"))
        self.actionStep.setText(_translate("MainWindow", "Step"))
        self.infome.setText(_translate("MainWindow", "info"))
        self.about.setText(_translate("MainWindow", "关于"))
        self.running.setText(_translate("MainWindow", "使用说明"))
