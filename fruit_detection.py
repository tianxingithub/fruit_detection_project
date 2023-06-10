from sys import argv as sys_argv
from sys import exit as sys_exit
from time import sleep, strftime, localtime
from threading import Thread
# import numpy as np
from numpy import array,argmax,newaxis
import serial
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from pyqt5_plugins.examplebuttonplugin import QtGui
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.preprocessing import image
from pyqt5_plugins.examplebutton import QtWidgets
from keras.models import load_model

from os import getcwd, mkdir, listdir
from os import path as os_path
from qt_material import apply_stylesheet
import Fruit_QTgui

fd1 = serial.Serial("COM1", baudrate=115200, timeout=1)


def QgetFruit(test_img):
    # print('start getFruit')
    img = image.load_img(test_img, target_size=(128, 128))
    # print('-'*40) # 卡在 load_img 也不知道为什么，在其他地方测试都正常 #PIL库版本过低
    img_array = image.img_to_array(img)
    # img_array = img_to_array(img)
    img_array = array(img_array) / 255.0
    predictions = load_model(r'./model/model.h5').predict(img_array[newaxis, ...])
    a = argmax(predictions, axis=-1)
    fruitId = a.tolist()[0]
    return fruitId








# 继承 QObject
class Runthread(QtCore.QObject):
    #  通过类成员对象定义信号对象
    signal = pyqtSignal([str, serial.serialwin32.Serial, int])


    def __init__(self):
        super(Runthread, self).__init__()
        self.flag = True
        self.count = 0
        # print('type fd1:', type(self.fd1))

    def __del__(self):
        print(">>> __del__")

    def getPath(self):
        msg = fd1.readline()
        if len(msg) == 0:
            return 'no pic'
        return msg

    def getPath2(self):
        dir = getcwd()
        dir = dir + '\\' + 'step_picture'
        folder = os_path.exists(dir)
        if not folder:
            mkdir(dir)
        files = listdir(dir)
        if len(files) == 0:
            return "no pic"
        path = dir + '\\'+files[self.count]
        # print(path)
        self.count = self.count + 1
        if self.count == 33:
            self.count = 0
        return path

    def runStep(self):
        path2 = self.getPath2()
        self.signal.emit(path2, fd1)

    def run(self):
        while self.flag:
            # path2 = self.getPath2() # 测试
            path = self.getPath()  # 测试
            if path == 'no pic':
                continue
            else:
                msg = str(path[:-1], 'utf-8')
                qId = QgetFruit(msg)
                self.signal.emit(msg, fd1,qId)  # 注意这里与_signal = pyqtSignal(str)中的类型相同
            # time.sleep(0.2)
            sleep(0.2)
        print(">>> run end: ")

    def hit_fruit(self):
        fd1.write(b'\xff\x01')


class FruitWindow(QtWidgets.QMainWindow):
    _startThread = pyqtSignal()

    # _startThread2 = pyqtSignal()
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
        # self._startThread2.connect(self.myT.runStep)  # 只能通过信号-槽启动线程处理函数
        self.myT.signal.connect(self.call_backlog)

    def call_backlog(self, msg, fd, qId): #
        # msg为图片路径
        self.addLog(msg)
        # fID = self.getFruit(msg)
        self.showFruit(msg)
        self.showFruitInfo(self.fruitDict[qId])
        self.chooseFruit(qId,fd)

    def getFruit(self, test_img):
        # print('start getFruit')
        img = image.load_img(test_img, target_size=(128, 128))
        # print('-'*40) # 卡在 load_img 也不知道为什么，在其他地方测试都正常 #PIL库版本过低
        img_array = image.img_to_array(img)
        # img_array = img_to_array(img)
        img_array = array(img_array) / 255.0
        predictions = self.model.predict(img_array[newaxis, ...])
        a = argmax(predictions, axis=-1)
        fruitId = a.tolist()[0]
        return fruitId

    def __start2(self):
        self.addLog('check start')
        if self.thread.isRunning():
            return
        self.myT.flag = True
        self.thread.start()
        self._startThread.emit()

    def step2(self):
        self.addLog('check step')
        # self._startThread2.emit()
        path = self.getPath3()
        # self.addLog(path)
        self.showFruit(path)
        # print(path)
        fID = self.getFruit(path)
        # 显示信息并增加个数
        self.showFruitInfo(self.fruitDict[fID])
        self.countFruit(fID)
        self.updateCount()
        # if fID == self.fruitID:
        #     self.myT.hit_fruit()

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

    def getPath3(self):
        dir = getcwd()
        dir = dir + '\\' + 'step_picture'
        folder = os_path.exists(dir)
        if not folder:
            mkdir(dir)
        files = listdir(dir)
        if len(files) == 0:
            return "no pic"
        path = dir + '\\'+files[self.count]
        # print(path)
        self.count = self.count + 1
        if self.count == len(files):
            self.count = 0
        return path

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

    def hit(self):
        self.addLog('click hit')
        self.myT.hit_fruit()

    def end(self):
        self.addLog('end')
        if not self.thread.isRunning():
            return
        self.myT.flag = False
        self.thread.quit()  # 退出
        self.thread.wait()  # 回收资源

    def addLog(self, info):
        # tt = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime())
        tt = strftime(" %Y-%m-%d %H:%M:%S", localtime())
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

    def chooseFruit(self, id, fd):
        self.countFruit(id)
        if id == self.fruitID:
            fd.write(b'\xff\x01')
        self.updateCount()

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
        info = self.txtwindow(fruit)
        self.ui.fruitInfo.setText(info)

    def txtwindow(self, str):
        fruit_dic = {
            'Apple': '苹果，属于蔷薇科大宗水果，不仅是我国最主要的果品，也是世界上种植最广、产量最多的果品。\n'
                     '其味道酸甜适口，营养丰富。据测定，每百克苹果含果糖6.5~11.2克，葡萄糖2.5~3.5克，蔗糖1.0~5.2克;\n'
                     '还含有微量元素锌、钙、磷、铁、钾及维生素B1、维生素B2、维生素C和胡萝卜素等。\n'
                     '价格:8元/公斤菜谱推荐：苹果可以做成拔丝苹果、苹果派、苹果脆片等，\n'
                     '还可以榨汁做成苹果汁或做成苹果醋等饮料，苹果还可以和其他水果一起做成水果沙拉。\n',
            'Orange': '橘子性温，味甘酸，有生津止咳的作用，用于胃肠燥热之症；\n'
                      '有和胃利尿的功效，用于腹部不适、小便不利等症；\n'
                      '有润肺化痰的作用，适用于肺热咳嗽之症。\n'
                      '橘子有抑制葡萄球菌的作用，可使血压升高、心脏兴奋、抑制胃肠、子宫蠕动，\n'
                      '还可降低毛细血管的脆性，减少微血管出血。\n'
                      '价格：12元/斤\n'
                      '菜谱推荐：橘子果冻\n'
                      '准备食材如下：橘子1500克，鱼胶粉30克，草莓5颗\n'
                      '具体做法如下：将橘子去皮取肉出来，留100克果肉备用，剩余的果肉用工具挤压出新鲜果汁，差不多把橘子瓣都捣烂的时候，用滤网过滤取纯果汁备用；\n'
                      '草莓洗干净，鱼胶粉用少许的果汁泡一下，取出的果汁倒入奶锅中，中小火煮开，隔水将鱼胶粉融化成液体状，在温热的水中保存液状，别让鱼胶粉凝固，\n'
                      '果汁煮开的同时倒入鱼胶粉溶液，然后不停的慢慢搅拌果汁，直到鱼胶粉完全融合，果汁煮开为止，再倒入装有橘子果肉的小模具里，凝固即可！\n',
            'Mango': '芒果糖类及维生素含量很高，尤其维生素A含量为水果之首，有名目作用。\n'
                     '含芒果酮酸、异芒果醇等三醋酸和多酚类化合物，具有抗癌药理作用。\n'
                     '芒果汁能增加胃肠蠕动、缩短粪便在结肠停留时间，对防止结肠癌很有裨益。\n'
                     '芒果中含的芒果苷有祛痰止咳的功效，对咳嗽有辅助治疗作用。\n'
                     '维生素含量较高，常吃可以补充维生素C的消耗，防止心血管疾病。\n'
                     '未成熟的芒果、树皮、茎和叶的提取物有抑制华农球菌、大肠杆菌等作用。\n'
                     '价格：20元/斤\n'
                     '菜谱推荐：芒果双皮奶。\n'
                     '原料：芒果、牛奶、鸡蛋、白砂糖糖。\n'
                     '将牛奶倒入锅中加热一下再倒到杯子中晾凉备用，将一个鸡蛋的蛋清分离出来加入两小勺白砂糖。\n'
                     '牛奶凉了之后表面会有一层奶皮，用筷子扎一个小口，将牛奶倒出去，留下奶皮。\n'
                     '将蛋清倒到牛奶中，搅拌均匀。然后，将其沿着杯边倒回留有奶皮的杯中。\n'
                     '最后，包上保鲜膜，清蒸十分钟。关上火，将其拿出来，放入以切好的芒果粒。\n'
                     '冷藏后口味更佳哦！\n',
            'Banana': '香蕉味甘、性寒，入肺、大肠经；\n'
                      '具有清热，生津止渴，润肺滑肠的功效；\n'
                      '主治温热病、口烦渴、大便秘结、痔疮出血等症。\n'
                      '价格：5元/斤菜谱推荐：拔丝香蕉材料：香蕉5条 白糖2两面粉2两 鸡蛋1个做法：\n'
                      '1. 切好香蕉，五跟切断\n'
                      '2. 倒入能末过香蕉的油量\n'
                      '3. 用生粉或则面粉和香蕉。\n'
                      '4. 油烧热，放入榨香蕉，有点黄的时候拿出\n'
                      '5. 拿出香蕉\n'
                      '6. 加入少许油，糖和水，把糖煮化。\n'
                      '7. 不停的打圈，让他起泡，大泡。不停的滑动。火不可一下子很大，容易糊。\n'
                      ' 8. 糖金黄时倒入香蕉，拔丝。\n',
            'PineApple': '菠萝，酸甜多汁，营养丰富，含有大量的果糖、葡萄糖、维生素B、维生素C、磷、柠檬酸和蛋白酶等物质。\n'
                         '能清热解暑、利尿消肿、增进食欲、美容护肤，其大量的纤维素还能促进肠胃蠕动，防止便秘。\n'
                         '价格：4元/斤\n'
                         '菜谱推荐：菠萝鸡翅\n'
                         '原料：鸡翅500克，菠萝200克，盐、白糖、料酒、胡椒粉、高汤适量。\n'
                         '做法：将鸡翅清洗干净，并用厨房用纸吸去多余的水分;菠萝洗净，切成小块;\n'
                         '炒锅倒入适量油，烧热后放入鸡翅，带鸡皮的一面朝下，煎好一面再煎另一面，然后取出控油;\n'
                         '锅内留底油，加入白糖，炒至溶化并变成金红色，再倒入鸡翅中，加入盐、料酒、高汤、胡椒粉，大火煮开，加入菠萝块，转小火炖至汤汁浓稠即可。\n'
        }
        if str not in fruit_dic.keys():
            return "检查水果名字是否错误\n"
        return fruit_dic[str]

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys_argv)
    window = FruitWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.setWindowTitle("水果识别")
    window.setWindowIcon(QIcon("fruit.jpg"))
    window.show()
    sys_exit(app.exec_())
