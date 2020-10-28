import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget
from PyQt5 import QtCore

from main_form import Ui_Menu

# Music Player
from music_player import MainWindowMusicPlayer
# Video Player
from video_player import MainWindowVideoPlayer
# Have Fun
# from have_fun import MyFunWidget
# Image Function
from restoration_GUI import Window
from camera import ShowVideo, ImageViewer


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window
        self.width = 600
        self.height = 500

        self.setWindowTitle('Endoscope Image Restoration & Enhancement')
        self.setGeometry(200, 200, self.width, self.height)

        # set the window in the center
        size = self.geometry()
        self.center()

        # video play button
        self.buttonWindow1 = QPushButton('Image Function', self)
        # self.buttonWindow1.move(size.width()/2, size.height()/2)
        self.buttonWindow1.setGeometry(QtCore.QRect(200, 80, 200, 50))
        self.buttonWindow1.clicked.connect(
            self.buttonWindow1_onClick)
        
        # image play button
        self.buttonWindow2 = QPushButton('Video Function', self)
        self.buttonWindow2.setGeometry(QtCore.QRect(200, 180, 200, 50))
        self.buttonWindow2.clicked.connect(
            self.buttonWindow2_onClick)

        # real time video
        self.buttonWindow3 = QPushButton('Real Time Video', self)
        self.buttonWindow3.setGeometry(QtCore.QRect(200, 280, 200, 50))
        self.buttonWindow3.clicked.connect(
            self.buttonWindow3_onClick)
        self.show()
        self.cams = -1

    # center setting
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # Function that closes the main menu and
    # opens the music player
    @pyqtSlot()
    def buttonWindow1_onClick(self):
        self.cams = Window()
        self.cams.show()
        # self.close()

    # Function that closes the main menu and
    # opens the video player
    @pyqtSlot()
    def buttonWindow2_onClick(self):
        self.cams = MainWindowVideoPlayer()
        self.cams.show()
        # self.close()

    # Function that closes the main menu and
    # opens Have Fun
    @pyqtSlot()
    def buttonWindow3_onClick(self):
        self.cams = ShowVideo()
        self.cams.show()
        # self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
