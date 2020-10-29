import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget, QHBoxLayout, QWidget
from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from restoration_GUI import Window
from video import VideoBox
from realTime_camera import ShowVideo, ImageViewer


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Endoscope Image Restoration & Enhancement')
        self.setWindowIcon(QtGui.QIcon("./tsinghuaIcon.png"))
        self.resize(1200, 900)

        self.center()

        font = QtGui.QFont()
        font.setFamily('Franklin Gothic Mdeium')
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(50)

        self.buttonWindow1 = QPushButton('Image Restoration', self)
        self.buttonWindow1.setGeometry(QtCore.QRect(400, 150, 400, 100))
        self.buttonWindow1.setFont(font)
        self.buttonWindow1.clicked.connect(self.imageFunction_onClick)
        
        self.buttonWindow2 = QPushButton('Video Restortion', self)
        self.buttonWindow2.setGeometry(QtCore.QRect(400, 350, 400, 100))
        self.buttonWindow2.setFont(font)
        self.buttonWindow2.clicked.connect(self.videoFunction_onClick)

        self.buttonWindow3 = QPushButton('Realtime Video', self)
        self.buttonWindow3.setGeometry(QtCore.QRect(400, 550, 400, 100))
        self.buttonWindow3.setFont(font)
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
        self.cams.set_video('./endoscope.mp4', VideoBox.VIDEO_TYPE_OFFLINE, False)
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

        self.vertical_layout = QHBoxLayout()

        self.vertical_layout.addWidget(self.image_viewer1)
        self.vertical_layout.addWidget(self.image_viewer2)

        self.layout_widget = QWidget()
        self.layout_widget.setLayout(self.vertical_layout)

        self.cams = QMainWindow()
        self.cams.setCentralWidget(self.layout_widget)
        self.cams.setWindowTitle('Endoscope Image Restoration & Enhancement')
        self.cams.setWindowIcon(QIcon("./tsinghuaIcon.png")) 

        # Menu
        self.cams.menu = self.cams.menuBar()
        # Play Menu
        self.playMenu = self.cams.menu.addMenu('Play')
        self.originalAction = QAction('Original Play', self)
        self.playMenu.addAction(self.originalAction)
        self.originalAction.triggered.connect(self.vid1.startVideo)
        # Distoration Menu
        self.corrMenu = self.cams.menu.addMenu('Distoration-Correction')
        self.corrAction = QAction('Distoration-Correction', self)
        self.corrMenu.addAction(self.corrAction)
        # Hist-Normalized Menu
        self.histMenu = self.cams.menu.addMenu('Hist-Normalized')
        self.restorationAction = QAction('Hist-Normalized', self)
        self.histMenu.addAction(self.restorationAction)
        self.restorationAction.triggered.connect(self.vid2.startVideo2)
        # Denoising Menu
        self.denoiseMenu = self.cams.menu.addMenu('Denoising')
        self.denoiseAction = QAction('Denoising', self)
        self.denoiseMenu.addAction(self.denoiseAction)
        # Highlight Removal Menu
        self.highMenu = self.cams.menu.addMenu('Highlight-Removal')
        self.highAction = QAction('Highlight-Removal', self)
        self.highMenu.addAction(self.highAction)
        # Super Resulotion Menu
        self.superMenu = self.cams.menu.addMenu('Super-Resolution')
        self.superAction = QAction('Super-Resolution', self)
        self.superMenu.addAction(self.superAction)

        self.cams.resize(1200,900)
        self.cams.move(int((self.screen.width() - self.size.width()) / 2),
                       int((self.screen.height() - self.size.height()) / 2))
        self.cams.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
