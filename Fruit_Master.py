import sys
import time
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QLabel, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton
import quarter
from keras.models import Sequential,load_model
import serial
from tensorflow.keras.preprocessing import image


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.label = None
        self.fd1 = serial.Serial("COM1", baudrate=115200, timeout=1)
        self.model = load_model(r'./model/model.h5')
        self.choseFruitId = 0
        self.initUI()
        self.cc = 0
        self.fruitDict = {
            'Apple' : 0,
            'Orange' : 0,
            'Mango' : 0,
            'Banana' : 0,
            'Pineapple' : 0
        }

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()
    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
    def initUI(self):

        """Creates UI window on launch."""
        # Button for generating the master list.

        btnGenMast = QPushButton('start', self)
        # btnGenMast.move(450, 50)
        btnGenMast.setGeometry(QtCore.QRect(40, 630, 120, 40))
        btnGenMast.clicked.connect(self.genMastClicked)

        btnGenMast = QPushButton('Working', self)
        # btnGenMast.move(450, 50)
        btnGenMast.setGeometry(QtCore.QRect(600, 630, 120, 40))
        btnGenMast.clicked.connect(self.stillwork)

        btnGenMast1 = QPushButton('apple', self)
        btnGenMast1.setGeometry(QtCore.QRect(40, 20, 120, 40))
        btnGenMast1.clicked.connect(self.clickButton1)
        # btnGenMast1.setstylesheet("qpushbutton{border-image: url(img/1.png)}")

        btnGenMast2 = QPushButton('orange', self)
        btnGenMast2.setGeometry(QtCore.QRect(180, 20, 120, 40))
        btnGenMast2.clicked.connect(self.clickButton2)

        btnGenMast3 = QPushButton('mango', self)
        btnGenMast3.setGeometry(QtCore.QRect(320, 20, 120, 40))
        btnGenMast3.clicked.connect(self.clickButton3)

        btnGenMast4 = QPushButton('banana', self)
        btnGenMast4.setGeometry(QtCore.QRect(460, 20, 120, 40))
        btnGenMast4.clicked.connect(self.clickButton4)

        btnGenMast5 = QPushButton('pineapple', self)
        btnGenMast5.setGeometry(QtCore.QRect(600, 20, 120, 40))
        btnGenMast5.clicked.connect(self.clickButton5)

        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(200)
        self.process.move(40, 400)

        # 文本框
        self.info = QTextEdit(self, readOnly=True)
        self.info.ensureCursorVisible()
        self.info.setFixedWidth(680)
        self.info.setFixedHeight(250)
        self.info.move(40, 120)

        # label
        self.lab1 = QLabel(self)  # 设置图片显示label
        self.lab1.setFixedSize(260, 200)  # 设置图片大小
        self.lab1.move(460, 400)  # 设置图片位置
        self.lab1.setStyleSheet("QLabel{background:white;}")  # 设置label底色

        # 文本框
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(40, 70)
        self.textbox1.resize(120, 41)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(180, 70)
        self.textbox2.resize(120, 41)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(320, 70)
        self.textbox3.resize(120, 41)

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(460, 70)
        self.textbox4.resize(120, 41)

        self.textbox5 = QLineEdit(self)
        self.textbox5.move(600, 70)
        self.textbox5.resize(120, 41)

        # Set window size and title, then show the window.
        self.resize(760, 700)
        self.setWindowTitle('Fruit Master')
        self.show()
    # 显示图片
    def openimage(self,img_path):  # 显示图片函数
        self.showImage = QPixmap(img_path).scaled(self.lab1.width(), self.lab1.height())  # 适应窗口大小
        self.lab1.setPixmap(self.showImage)  # 显示图片

    def getPath(self):
        msg = self.fd1.readlines()
        if len(msg) == 0:
            return 'no pic'
        return msg[-1]

    # 找到指定种类就发送 ff 01
    def chooseFruit(self, fd1):
        self.fd1.write(b'\xff\x01')

    def stillwork(self):
        print(time.localtime())
        self.process.append('开始自动化处理：应该有两次输出')
        for i in range(10):
            auto = f'这是第 {i} 次处理'
            self.process.append(auto)
            self.genMastClicked()
            time.sleep(1)
        self.process.append('结束自动化处理.........')
        print(time.localtime())

    def genMastClicked(self, a=None):
        FRUITS = {
            0: 'Apple',
            1: 'Banana',
            2: 'Mango',
            3: 'Orange',
            4: 'Pineapple'
        }
        path = self.getPath()
        if path == 'no pic':
            tt = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime())
            info = tt + ' 未识别到水果'
            self.process.append(info)
        else:
            spath = str(path[:-1], 'utf-8')
            self.openimage(spath)
            num = self.classify(spath)
            if num == self.choseFruitId:
                interface.chooseFruit(self.fd1)
            self.numResult(FRUITS[num])


    def classify(self, test_img):
        img = image.load_img(test_img, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.array(img_array) / 255.0
        predictions = self.model.predict(img_array[np.newaxis, ...], verbose=None)
        a = np.argmax(predictions, axis=-1)
        fruitId = a.tolist()[0]
        return fruitId

    def numResult(self,str):
        self.cc = self.cc + 1
        tt = time.strftime(" %Y-%m-%d %H:%M:%S", time.localtime())
        info = tt + ' fruit is ' + str
        self.process.append(info)
        self.fruitDict[str] = self.fruitDict[str]+1
        number = (self.fruitDict[str])
        self.showInfo(str)
        if str == 'Apple':
            ss = (f' Apple is {number}')
            self.textbox1.setText(ss)
        elif str == 'Orange':
            ss = (f' Orange is {number}')
            self.textbox2.setText(ss)
        elif str == 'Mango':
            ss = (f' Mango is {number}')
            self.textbox3.setText(ss)
        elif str == 'Banana':
            ss = (f' Banana is {number}')
            self.textbox4.setText(ss)
        elif str == 'Pineapple':
            ss = (f' Pineapple is {number}')
            self.textbox5.setText(ss)


    def showInfo(self,str):
        info2 = quarter.txtwindow(str)
        self.info.setPlainText(info2)

    # A的响应函数
    def clickButton1(self):
        self.choseFruitId = 0

    # B响应函数
    def clickButton2(self):
        self.choseFruitId = 3

    # C响应函数
    def clickButton3(self):
        self.choseFruitId = 2

    # D响应函数
    def clickButton4(self):
        self.choseFruitId = 1

    def clickButton5(self):
        self.choseFruitId = 4


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main = MainWindow()
    main.show()

    sys.exit(app.exec_())