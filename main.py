import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget, QHBoxLayout, QWidget
from PyQt5 import QtCore

from main_form import Ui_Menu

from restoration_GUI import Window
from video import VideoBox
from realTime_camera import ShowVideo, ImageViewer


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.width = 600
        # self.height = 500

        self.setWindowTitle('Endoscope Image Restoration & Enhancement')
        self.resize(1200, 900)

        self.center()

        self.buttonWindow1 = QPushButton('Image Function', self)
        self.buttonWindow1.setGeometry(QtCore.QRect(500, 80, 200, 50))
        self.buttonWindow1.clicked.connect(self.imageFunction_onClick)
        
        self.buttonWindow2 = QPushButton('Video Function', self)
        self.buttonWindow2.setGeometry(QtCore.QRect(200, 180, 200, 50))
        self.buttonWindow2.clicked.connect(self.videoFunction_onClick)

        self.buttonWindow3 = QPushButton('Real Time Video', self)
        self.buttonWindow3.setGeometry(QtCore.QRect(200, 280, 200, 50))
        self.buttonWindow3.clicked.connect(self.realtimeVideo_onClick)
        self.show()
        self.cams = -1

    def center(self):
        self.screen = QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move(int((self.screen.width() - self.size.width()) / 2),
                  int((self.screen.height() - self.size.height()) / 2))

    def imageFunction_onClick(self):
        self.cams = Window()
        self.cams.resize(1200,900)
        self.cams.move(int((self.screen.width() - self.size.width()) / 2),
                       int((self.screen.height() - self.size.height()) / 2))
        self.cams.show()

    def videoFunction_onClick(self):
        self.cams = VideoBox()
        self.cams.set_video('./1.mp4', VideoBox.VIDEO_TYPE_OFFLINE, False)
        self.cams.resize(1200,900)
        self.cams.move(int((self.screen.width() - self.size.width()) / 2),
                       int((self.screen.height() - self.size.height()) / 2))
        self.cams.show()

    def realtimeVideo_onClick(self):
        self.thread1 = QtCore.QThread()
        self.thread1.start()
        self.thread2 = QtCore.QThread()
        self.thread2.start()

        self.vid1 = ShowVideo()
        self.vid1.moveToThread(self.thread1)
        self.vid2 = ShowVideo()
        self.vid2.moveToThread(self.thread2)

        self.image_viewer1 = ImageViewer()
        self.image_viewer2 = ImageViewer()

        self.vid1.VideoSignal.connect(self.image_viewer1.setImage)
        self.vid2.VideoSignal.connect(self.image_viewer2.setImage)

        self.push_button1 = QPushButton('Original')
        self.push_button1.clicked.connect(self.vid1.startVideo)
        self.push_button2 = QPushButton('Restored')
        self.push_button2.clicked.connect(self.vid2.startVideo2)
        self.vertical_layout = QHBoxLayout()

        self.vertical_layout.addWidget(self.image_viewer1)
        self.vertical_layout.addWidget(self.image_viewer2)
        self.vertical_layout.addWidget(self.push_button1)
        self.vertical_layout.addWidget(self.push_button2)

        self.layout_widget = QWidget()
        self.layout_widget.setLayout(self.vertical_layout)

        self.cams = QMainWindow()
        self.cams.setCentralWidget(self.layout_widget)
        self.cams.resize(1200,900)
        self.cams.move(int((self.screen.width() - self.size.width()) / 2),
                       int((self.screen.height() - self.size.height()) / 2))
        self.cams.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
