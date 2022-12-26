import sys
import time
from threading import Thread
import cv2
import numpy as np
import serial
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from pyqt5_plugins.examplebuttonplugin import QtGui
from tensorflow.keras.preprocessing import image
from pyqt5_plugins.examplebutton import QtWidgets
from keras.models import load_model
import fruitInformation

import Fruit_QTgui

# 继承 QObject
class Runthread(QtCore.QObject):
    #  通过类成员对象定义信号对象
    signal = pyqtSignal([str,serial.serialwin32.Serial])

    def __init__(self):
        super(Runthread, self).__init__()
        self.flag = True
        self.count = 0
        self.fd1 = serial.Serial("COM1", baudrate=115200, timeout=1)
        # print('type fd1:', type(self.fd1))

    def __del__(self):
        print(">>> __del__")

    def getPath(self):
        msg = self.fd1.readline()
        if len(msg) == 0:
            return 'no pic'
        return msg

    def getPath2(self):
        path = f'./test_picture/{self.count}.png'
        self.count = self.count + 1
        if self.count == 33:
            self.count = 0
        return path

    def runStep(self):
        path2 = self.getPath2()
        self.signal.emit(path2, self.fd1)

    def run(self):
        while self.flag:
            # path2 = self.getPath2() # 测试
            path = self.getPath() # 测试
            if path == 'no pic':
                continue
            else:
                msg = str(path[:-1],'utf-8')
                print(msg)
            self.signal.emit(msg, self.fd1)  # 注意这里与_signal = pyqtSignal(str)中的类型相同
            time.sleep(0.2)
        print(">>> run end: ")

    def hit_fruit(self):
        self.fd1.write(b'\xff\x01')

class FruitWindow(QtWidgets.QMainWindow):
    _startThread = pyqtSignal()
    _startThread2 = pyqtSignal()
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Fruit_QTgui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.__start2)
        self.ui.actionStep.triggered.connect(self.step2)
        self.ui.actionEnd.triggered.connect(self.end)
        self.ui.actionApple.triggered.connect(self.changeFruit0)
        self.ui.actionBanana.triggered.connect(self.changeFruit1)
        self.ui.actionOrange.triggered.connect(self.changeFruit2)
        self.ui.actionMonago.triggered.connect(self.changeFruit3)
        self.ui.actionPineApple.triggered.connect(self.changeFruit4)
        self.ui.running.triggered.connect(self.howRun)
        self.ui.about.triggered.connect(self.aboutme)
        self.ui.hitButton.clicked.connect(self.hit)


        self.fruitID = 0
        self.model = load_model(r'./model/model.h5')
        self.fruitDict = {
            0: 'Apple',
            1: 'Banana',
            2: 'Orange',
            3: 'Mongo',
            4: 'PineApple'
        }
        self.fruitCount = {
            'Apple': 0,
            'Banana': 0,
            'Orange': 0,
            'Mongo': 0,
            'PineApple': 0
        }
        self.updateCount()
        self.count = 0

        self.myT = Runthread()  # 创建线程对象
        self.thread = QThread(self)  # 初始化QThread子线程
        # 把自定义线程加入到QThread子线程中
        self.myT.moveToThread(self.thread)
        self._startThread.connect(self.myT.run)  # 只能通过信号-槽启动线程处理函数
        self._startThread2.connect(self.myT.runStep)  # 只能通过信号-槽启动线程处理函数
        self.myT.signal.connect(self.call_backlog)

    def hit(self):
        self.addLog('click hit')
        self.myT.hit_fruit()

    def call_backlog(self, msg, fd):
        # msg为图片路径
        self.addLog(msg)
        fID = self.getFruit(msg)
        self.showFruit(msg)
        self.chooseFruit(fID,fd)

    def aboutme(self):
        QMessageBox.about(self, '关于', '【hqyj实习项目】\n\t'
                                      '基于Python的人工智能水果识别\n'
                                      '更多：bravos.04.segue@icloud.com(留下回信地址)')

    def howRun(self):
        QMessageBox.about(self, '菜单栏说明',
                          '【状态】：\n\t'
                          '[Start]:连续读取摄像头照片，并在界面显示图片\n\t'
                          '[End]:停止连续读取照片\n\t'
                          '[Step]:一次读取一张本地照片(test_picture文件夹内)，在系统界面显示\n'
                          '【筛选的水果类别】:\n\t'
                          '默认当识别出苹果后，给模拟机械臂发出指定弹出水果\n\t'
                          '选择哪个下拉菜单就弹出哪个种类水果')

    def printFruitCount(self, fruit):
        self.fruitCount[fruit] = self.fruitCount[fruit] + 1
        print(f'    Have chose {fruit} {self.fruitCount[fruit]} times')

    def getFruit(self, test_img):
        img = image.load_img(test_img, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.array(img_array) / 255.0
        predictions = self.model.predict(img_array[np.newaxis, ...], verbose=None)
        a = np.argmax(predictions, axis=-1)
        fruitId = a.tolist()[0]
        return fruitId

    def getPath2(self):
        path = f'./test_picture/{self.count}.png'
        self.count = self.count + 1
        if self.count == 33:
            self.count = 0
        return path

    def __start2(self):
        self.addLog('check start')
        if self.thread.isRunning():
            return
        self.myT.flag=True
        self.thread.start()
        self._startThread.emit()

    def step2(self):
        self.addLog('check step')
        # self._startThread2.emit()
        # path = self.getPath2()
        # self.addLog(path)
        # self.showFruit(path)
        # fID = self.getFruit(path)
        # if fID == self.fruitID:
        #     self.myT.hit_fruit()

    def changeFruit0(self):
        self.changeID(0)

    def changeFruit1(self):
        self.changeID(1)

    def changeFruit2(self):
        self.changeID(2)

    def changeFruit3(self):
        self.changeID(3)

    def changeFruit4(self):
        self.changeID(4)

    def changeID(self, ID):
        self.fruitID = ID
        self.addLog(f'CHANEGED! If fruit is {self.fruitDict[ID]}, then move it.')

    def end(self):
        self.addLog('end')
        if not self.thread.isRunning():
            return
        self.myT.flag=False
        self.thread.quit()  # 退出
        self.thread.wait()  # 回收资源

    def addLog(self, info):
        tt = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime())
        inser = tt + ' ' + info
        self.ui.fruitLog.append(inser)

    def showFruit(self, path):
        frame = QImage(path)
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(pix)  # fitInView(item)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.ui.fruitPic.setScene(scene)
        self.ui.fruitPic.fitInView(item)
        self.ui.fruitPic.show()

    def showFruit2(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (400, 300))
        cv2.imshow("Fruit", img)
        cv2.waitKey(1)

    def chooseFruit(self, id,fd):
        self.countFruit(id)
        if id == self.fruitID:
            fd.write(b'\xff\x01')
        self.updateCount()

    def setStyle(self):

        print('style')

    def countFruit(self, id):
        fruit = self.fruitDict[id]
        self.fruitCount[fruit] = self.fruitCount[fruit] + 1
        self.showFruitInfo(fruit)

    def updateCount(self):
        # f1 = (self.fruitCount['Apple'])
        self.ui.count0.setText('apple : ' + str(self.fruitCount['Apple']))
        self.ui.count1.setText('Banana : ' + str(self.fruitCount['Banana']))
        self.ui.count2.setText('Orange : ' + str(self.fruitCount['Orange']))
        self.ui.count3.setText('Mongo : ' + str(self.fruitCount['Mongo']))
        self.ui.count4.setText('PineApple : ' + str(self.fruitCount['PineApple']))
        # print(f1)

    def showFruitInfo(self, fruit):
        info = fruitInformation.txtwindow(fruit)
        self.ui.fruitInfo.setText(info)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FruitWindow()
    window.show()
    sys.exit(app.exec_())
