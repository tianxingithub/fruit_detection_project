import sys
import time

import cv2
import numpy as np
import serial
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from pyqt5_plugins.examplebuttonplugin import QtGui
from tensorflow.keras.preprocessing import image
from pyqt5_plugins.examplebutton import QtWidgets
from keras.models import load_model
import fruitInformation

import FruitPrevision

class FruitWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = FruitPrevision.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.start2)
        self.ui.actionStep.triggered.connect(self.step2)
        self.ui.actionEnd.triggered.connect(self.end)
        self.ui.actionApple.triggered.connect(self.changeFruit0)
        self.ui.actionBanana.triggered.connect(self.changeFruit1)
        self.ui.actionOrange.triggered.connect(self.changeFruit2)
        self.ui.actionMonago.triggered.connect(self.changeFruit3)
        self.ui.actionPineApple.triggered.connect(self.changeFruit4)
        self.ui.running.triggered.connect(self.howRun)
        self.ui.about.triggered.connect(self.aboutme)

        self.count = 1
        self.fd1 = serial.Serial("COM1", baudrate=115200, timeout=1)
        self.going = True
        self.fruitID = 0
        self.model = load_model(r'./model/model.h5')
        self.fruitDict = {
            0:'Apple',
            1:'Banana',
            2:'Orange',
            3:'Mongo',
            4:'PineApple'
        }
        self.fruitCount = {
            'Apple':0,
            'Banana':0,
            'Orange':0,
            'Mongo':0,
            'PineApple':0
        }
        self.updateCount()

    def aboutme(self):
        QMessageBox.about(self,'关于','【hqyj实习项目】\n基于Python的人工智能水果识别\n使用CNN实现')

    def howRun(self):
        QMessageBox.about(self, '菜单栏说明',
                          '【状态】：\n\t'
                          '[Start]:连续读取10张照片，用Opencv显示图片\n\t'
                          '[End]:暂无实际意义\n\t'
                          '[Step]:一次读取一张照片，用QImage在系统界面显示\n'
                          '【筛选的水果类别】:\n\t'
                          '默认当识别出苹果后，给模拟机械臂发出指定弹出水果\n\t'
                          '选择哪个下拉菜单就弹出哪个种类水果')

    def printFruitCount(self,fruit):
        self.fruitCount[fruit] = self.fruitCount[fruit]+1
        print(f'    Have chose {fruit} {self.fruitCount[fruit]} times')

    def getFruit(self,test_img):
        img = image.load_img(test_img, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.array(img_array) / 255.0
        predictions = self.model.predict(img_array[np.newaxis, ...], verbose=None)
        a = np.argmax(predictions, axis=-1)
        fruitId = a.tolist()[0]
        return fruitId

    def getPath(self):
        msg = self.fd1.readline()
        if len(msg) == 0:
            return 'no pic'
        return msg

    def getPath2(self):
        path = f'./test/{self.count}.png'
        if self.count == 32:
            self.count = 0
        self.count = self.count+1
        return path

    def start(self):
        self.addLog('check start')
        for i in range(10):
            pp = self.getPath2()
            if pp == 'no pic':
                pass
            else:
                pp = str(pp[:-1], 'utf-8')
                fID = self.getFruit(pp)
                self.showFruit2(pp)
                print('fruit is ',self.fruitDict[fID])
                self.chooseFruit(fID)
        print('='*40)
        self.addLog('start is over')

    def start2(self):
        self.addLog('check start')
        for i in range(10):
            pp = self.getPath2()
            if pp == 'no pic':
                pass
            else:
                # pp = str(pp[:-1], 'utf-8')
                fID = self.getFruit(pp)
                self.showFruit2(pp)
                print('fruit is ',self.fruitDict[fID])
                self.chooseFruit(fID)
        print('='*40)
        self.addLog('start is over')

    def step(self):
        self.addLog('check step')
        msg = self.fd1.readlines()
        pp = msg[-1]
        pp = str(pp[:-1], 'utf-8')
        self.showFruit(pp)
        fID = self.getFruit(pp)
        self.chooseFruit(fID)

    def step2(self):
        self.addLog('check step')
        path = self.getPath2()
        self.showFruit(path)
        fID = self.getFruit(path)
        self.chooseFruit(fID)

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

    def changeID(self,ID):
        self.fruitID = ID
        self.addLog(f'changed fruit, now fruit is {self.fruitDict[ID]}')

    def end(self):
        self.addLog('end')
        self.going = False
        self.setStyle()

    def addLog(self,info):
        tt = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime())
        inser = tt + ' '+info
        self.ui.fruitLog.append(inser)

    def showFruit(self,path):
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
        img = cv2.resize(img,(400,300))
        cv2.imshow("Fruit", img)
        cv2.waitKey(1)

    def chooseFruit(self,id):
        self.countFruit(id)
        if id == self.fruitID:
            self.fd1.write(b'\xff\x01')
            # self.printFruitCount(self.fruitDict[id])
        self.updateCount()

    def setStyle(self):


        print('style')

    def countFruit(self,id):
        fruit = self.fruitDict[id]
        self.fruitCount[fruit] = self.fruitCount[fruit] + 1
        self.showFruitInfo(fruit)

    def updateCount(self):
        # f1 = (self.fruitCount['Apple'])
        self.ui.count0.setText('apple : '+str(self.fruitCount['Apple']))
        self.ui.count1.setText('Banana : '+str(self.fruitCount['Banana']))
        self.ui.count2.setText('Orange : '+str(self.fruitCount['Orange']))
        self.ui.count3.setText('Mongo : '+str(self.fruitCount['Mongo']))
        self.ui.count4.setText('PineApple : '+str(self.fruitCount['PineApple']))
        # print(f1)

    def showFruitInfo(self,fruit):
        info = fruitInformation.txtwindow(fruit)
        self.ui.fruitInfo.setText(info)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FruitWindow()
    window.show()
    sys.exit(app.exec_())