# fruit_detection_project

基于Python的水果识别项目，模型训练使用的卷积神经网络（CNN），界面使用的Qt5，识别的水果图片是从串口获取的

项目运行流程：从模拟机械臂中读取水果（实际是读取照片的路径），将图片放入模型进行识别，将识别的结果返回在界面

模型构建：使用了Conv2D、MaxPooling2D、Flatten、Dense、Dropout层，输入张量形状是(128, 128, 3)，输出的结果是5个水果种类的概率

主要的py文件说明：
fruit_detection.py：主文件，运行时的文件
Fruit_detection.py：主文件，运行时的文件
FruitPrevision.py：QT界面文件
FruitClassifyTraing.py：模型训练
FruitClassifyTest.py：模型测试
fruitInformation：返回该水果的信息，可用爬虫实现

# 2022-11-15
增加线程来实现显示图片
用爬虫来实现动态爬取数据