#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ide： PyCharm
import sys, os

import torch
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import cv2
from detect import Yolov5
from utils.XThread import Thread

class Ui_MainWindow(object):  # 定义主窗口
    imgSignal = pyqtSignal(object)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1042, 700)  # 定义窗口大小
        self.centralwidget = QtWidgets.QWidget(MainWindow)  # QtWidgets构建界面的一系列UI元素组件
        self.centralwidget.setObjectName("centralwidget")  # 设置触发控制命令的名称

        # 显示摄像头画面
        self.cam_frame = QtWidgets.QFrame(self.centralwidget)  # 有边框的容器
        # self.cam_frame.setGeometry(QtCore.QRect(10, 110, 521, 571))  # 尺寸 左上角坐标+长宽
        self.cam_frame.setGeometry(QtCore.QRect(10, 110, 221, 571))  # 尺寸 左上角坐标+长宽
        self.cam_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cam_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cam_frame.setObjectName("cam_frame")

        self.label_img_show = QtWidgets.QLabel(self.cam_frame)
        # self.label_img_show.setGeometry(QtCore.QRect(10, 10, 501, 551))
        self.label_img_show.setGeometry(QtCore.QRect(10, 10, 201, 551))
        self.label_img_show.setObjectName("label_img_show")
        self.label_img_show.setScaledContents(True)

        # 显示检测画面
        self.detect_frame = QtWidgets.QFrame(self.centralwidget)
        # self.detect_frame.setGeometry(QtCore.QRect(540, 110, 491, 571))
        self.detect_frame.setGeometry(QtCore.QRect(240, 110, 791, 571))
        self.detect_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.detect_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.detect_frame.setObjectName("detect_frame")
        self.label_detect_show = QtWidgets.QLabel(self.detect_frame)
        # self.label_detect_show.setGeometry(QtCore.QRect(10, 10, 481, 551))
        self.label_detect_show.setGeometry(QtCore.QRect(10, 10, 781, 551))
        self.label_detect_show.setObjectName("label_detect_show")
        self.label_detect_show.setScaledContents(True)

        # 按钮框架
        self.btn_frame = QtWidgets.QFrame(self.centralwidget)
        self.btn_frame.setGeometry(QtCore.QRect(10, 20, 1021, 80))
        self.btn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btn_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btn_frame.setObjectName("frame_3")

        # 按钮水平布局
        self.widget = QtWidgets.QWidget(self.btn_frame)
        self.widget.setGeometry(QtCore.QRect(20, 10, 844, 60))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 视频检测
        self.btn_vedio = QtWidgets.QPushButton(self.widget)
        self.btn_vedio.setMinimumHeight(41)
        self.btn_vedio.setMinimumWidth(141)
        self.btn_vedio.setObjectName("btn_vedio")
        self.horizontalLayout.addWidget(self.btn_vedio)
        
        # 图片检测
        self.btn_img = QtWidgets.QPushButton(self.widget)
        self.btn_img.setMinimumHeight(41)
        self.btn_img.setMinimumWidth(141)
        self.btn_img.setObjectName("btn_img")
        self.horizontalLayout.addWidget(self.btn_img)

        # 打开摄像头
        self.btn_opencam = QtWidgets.QPushButton(self.widget)
        self.btn_opencam.setMinimumHeight(41)
        self.btn_opencam.setMinimumWidth(141)
        self.btn_opencam.setObjectName("btn_opencam")
        self.horizontalLayout.addWidget(self.btn_opencam)

        # 开始检测
        self.btn_detect = QtWidgets.QPushButton(self.widget)
        self.btn_detect.setMinimumHeight(41)
        self.btn_detect.setMinimumWidth(141)
        self.btn_detect.setObjectName("btn_detect")
        self.horizontalLayout.addWidget(self.btn_detect)
        # 退出
        self.btn_exit = QtWidgets.QPushButton(self.widget)
        self.btn_exit.setMinimumHeight(41)
        self.btn_exit.setMinimumWidth(141)
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout.addWidget(self.btn_exit)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1042, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        # 打开摄像头
        self.btn_opencam.clicked.connect(self.opencam)
        # 开始识别
        self.btn_detect.clicked.connect(self.init_detect_thread)
        self.btn_vedio.clicked.connect(self.openvideo)
        self.btn_img.clicked.connect(self.openimg)
        # 这里是将btn_exit按钮和Form窗口相连，点击按钮发送关闭窗口命令
        self.btn_exit.clicked.connect(MainWindow.close)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.btn_beautiful()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "目标检测"))
        self.label_img_show.setText(_translate("MainWindow", "请选择路径或摄像头"))
        self.label_detect_show.setText(_translate("MainWindow", "实时检测效果"))
        self.btn_vedio.setText(_translate("MainWindow", "选择视频地址"))
        self.btn_img.setText(_translate("MainWindow", "选择图片地址"))
        self.btn_opencam.setText(_translate("MainWindow", "打开摄像头"))
        self.btn_detect.setText(_translate("MainWindow", "开始检测"))
        self.btn_exit.setText(_translate("MainWindow", "退出"))

    def btn_beautiful(self):
        self.btn_vedio.setStyleSheet("""
                QPushButton{
                    font: 14pt "楷体";
                    background-color: qlineargradient(spread:pad, x1:0.06, y1:0.108, x2:1, y2:1, stop:0.179104 rgba(23, 165, 57, 246), stop:1 rgba(25, 235, 224, 255));
                    border-radius:20px;}
                QPushButton::hover{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.91, y2:0.9375, stop:0.149254 rgba(95, 235, 192, 255), stop:0.935323 rgba(23, 165, 57, 229));
                    border-radius:20px;}
                QPushButton::pressed{
                    color: rgb(170, 0, 0);}
        """)
        self.btn_img.setStyleSheet("""
                QPushButton{
                    font: 14pt "楷体";
                    background-color: qlineargradient(spread:pad, x1:0.06, y1:0.108, x2:1, y2:1, stop:0.179104 rgba(23, 165, 57, 246), stop:1 rgba(25, 235, 224, 255));
                    border-radius:20px;}
                QPushButton::hover{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.91, y2:0.9375, stop:0.149254 rgba(95, 235, 192, 255), stop:0.935323 rgba(23, 165, 57, 229));
                    border-radius:20px;}
                QPushButton::pressed{
                    color: rgb(170, 0, 0);}
        """)
        self.btn_opencam.setStyleSheet("""
                QPushButton{
                    font: 14pt "楷体";
                    background-color: qlineargradient(spread:pad, x1:0.06, y1:0.108, x2:1, y2:1, stop:0.179104 rgba(23, 165, 57, 246), stop:1 rgba(25, 235, 224, 255));
                    border-radius:20px;}
                QPushButton::hover{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.91, y2:0.9375, stop:0.149254 rgba(95, 235, 192, 255), stop:0.935323 rgba(23, 165, 57, 229));
                    border-radius:20px;}
                QPushButton::pressed{
                    color: rgb(170, 0, 0);}
                """)
        self.btn_detect.setStyleSheet("""
                QPushButton{
                    font: 14pt "楷体";
                    background-color: qlineargradient(spread:pad, x1:0.06, y1:0.108, x2:1, y2:1, stop:0.179104 rgba(23, 165, 57, 246), stop:1 rgba(25, 235, 224, 255));
                    border-radius:20px;}
                QPushButton::hover{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.91, y2:0.9375, stop:0.149254 rgba(95, 235, 192, 255), stop:0.935323 rgba(23, 165, 57, 229));
                    border-radius:20px;}
                QPushButton::pressed{
                    color: rgb(170, 0, 0);}
                """)
        self.btn_exit.setStyleSheet("""
                QPushButton{
                    font: 14pt "楷体";
                    background-color: qlineargradient(spread:pad, x1:0.06, y1:0.108, x2:1, y2:1, stop:0.179104 rgba(23, 165, 57, 246), stop:1 rgba(25, 235, 224, 255));
                    border-radius:20px;}
                QPushButton::hover{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.91, y2:0.9375, stop:0.149254 rgba(95, 235, 192, 255), stop:0.935323 rgba(23, 165, 57, 229));
                    border-radius:20px;}
                QPushButton::pressed{
                    color: rgb(170, 0, 0);}
                """)

    def opencam(self):
        self.btn_vedio.setEnabled(False)
        self.btn_img.setEnabled(False)
        if self.btn_opencam.text() == "取消摄像头":
            self.sources = '0'
            self.btn_vedio.setEnabled(True)
            self.btn_img.setEnabled(True)
            self.label_img_show.setText("请选择方式")
        else:
            self.sources = '0'
            self.btn_opencam.setText(u"取消摄像头")
        self.label_img_show.setText(self.sources)

    def openvideo(self):
        self.btn_opencam.setEnabled(False)
        self.btn_img.setEnabled(False)
        if self.btn_vedio.text() == "取消视频地址":
            self.sources = '0'
            self.btn_opencam.setEnabled(True)
            self.btn_img.setEnabled(True)
            self.label_img_show.setText("请选择方式")
            self.btn_vedio.setText("选择视频地址")
        else:
            self.sources = self.load_videopath()
            if self.sources != "":
                self.btn_vedio.setText(u"取消视频地址")
                self.label_img_show.setText(self.sources)
            else:
                pass
    def openimg(self):
        self.btn_opencam.setEnabled(False)
        self.btn_vedio.setEnabled(False)
        if self.btn_img.text() == "取消图片地址":
            self.sources = '0'
            self.btn_opencam.setEnabled(True)
            self.btn_vedio.setEnabled(True)
            self.label_img_show.setText("请选择方式")
            self.btn_img.setText("选择图片地址")
        else:
            self.sources = self.load_imgpath()
            if self.sources != "":
                self.btn_img.setText(u"取消图片地址")
                self.label_img_show.setText(self.sources)
            else:
                pass

    def init_detect_thread(self):
        yolov5 = Yolov5()
        yolov5.opt.source = self.sources
        print(self.sources)
        self.detect_thread = Thread(lambda :self.detected(yolov5))
        self.detect_thread.signal.connect(self.ui_show)
        self.detect_thread.start()

    def detected(self,yolov5):
        # 默认的参数设置
        with torch.no_grad():
            yolov5.detect(signal_images=self.detect_thread.signal)

    def ui_show(self,img):
        show = img
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],show.shape[1] * 3, QtGui.QImage.Format_RGB888)
        self.label_detect_show.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def load_videopath(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "📝选取本地视频文件", r'./',
                                                   "*.mp4;;*.flv;;*.MPEG;;*.AVI;;*.MOV;;*.WMV;;")
        return file_path

    def load_imgpath(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "📝选取本地图片文件", r'./',
                                                        "*.jpg;;*.png")
        return file_path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    # 向主窗口上添加控件
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
