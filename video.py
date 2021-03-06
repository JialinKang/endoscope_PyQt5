import time
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QPushButton, QStyle, QHBoxLayout, QDesktopWidget, QAction
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *

from data_preprocessing import predict_img, convert_cv_qt
from SRCNN_model import model


class VideoBox(QMainWindow):

    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1

    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    video_url = ""

    def __init__(self, video_url="", video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        super().__init__()
        self.video_url = video_url
        self.video_type = video_type  # 0: offline  1: realTime
        self.auto_play = auto_play
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause

        self.setWindowTitle('Endoscope Image Restoration & Enhancement')
        self.setWindowIcon(QIcon("./tsinghuaIcon.png")) 

        self.pictureLabel = QLabel(self)
        self.pictureLabel.resize(600, 600)
        self.pictureLabel.move(100, 20)
        self.init_image = QPixmap("./original.png")#.scaled(400, 400)
        self.pictureLabel.setPixmap(self.init_image)

        self.pictureLabel2 = QLabel(self)
        self.pictureLabel2.resize(600, 600)
        self.pictureLabel2.move(650, 20)
        self.init_image = QPixmap("./output.png")#.scaled(400, 400)
        self.pictureLabel2.setPixmap(self.init_image)

        self.playButton = QPushButton(self)
        self.playButton.move(300, 800)
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.switch_video)

        self.control_box = QHBoxLayout(self)
        self.control_box.setContentsMargins(0, 0, 0, 0)
        self.control_box.addWidget(self.playButton)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.pictureLabel)
        self.layout.addWidget(self.pictureLabel2)
        self.layout.addLayout(self.control_box)

        self.model = model()

        self.showMenubar()
        
        self.setLayout(self.layout)

        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.srcnn_img)

        self.playCapture = VideoCapture()
        if self.video_url != "":
            self.set_timer_fps()
            if self.auto_play:
                self.switch_video()
            # self.videoWriter = VideoWriter('*.mp4', VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, size)

    def showMenubar(self):
        self.menu = self.menuBar()

        # File Menu
        self.fileMenu = self.menu.addMenu('File')
        self.openAction = QAction('Open', self)
        self.fileMenu.addAction(self.openAction)
        self.openAction.triggered.connect(self.openVideo)
        # Distoration Menu
        self.distormenu = self.menu.addMenu('Distoration-Correction')
        self.distorAction = QAction('Distoration-Correction', self)
        self.distormenu.addAction(self.distorAction)
        # Histnormalized Menu
        self.histmenu = self.menu.addMenu('Hist-Normalized')
        self.histAction = QAction('Hist-Normalized', self)
        self.histmenu.addAction(self.histAction)
        self.histAction.triggered.connect(self.show_video_images)
        # Denoising Menu
        self.denoisemenu = self.menu.addMenu('Denoising')
        self.denoiseAction = QAction('Denoising', self)
        self.denoisemenu.addAction(self.denoiseAction)
        # Highlight Menu
        self.highmenu = self.menu.addMenu('Hightlight-Removal')
        self.highAction = QAction('Hightlight-Removal', self)
        self.highmenu.addAction(self.highAction)
        # Super Resolution
        self.supermenu = self.menu.addMenu('Super-Resolution')
        self.superAction = QAction('Super-Resolution', self)
        self.supermenu.addAction(self.superAction)

    def openVideo(self):
        self.videoPath, _ = QFileDialog.getOpenFileName(self)
        self.set_video(self.videoPath, VideoBox.VIDEO_TYPE_OFFLINE, False)

    def center(self):
        screen = QDesktopWidget.screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = VideoBox.STATUS_INIT
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_timer_fps(self):
        self.playCapture.open(self.video_url)
        fps = self.playCapture.get(CAP_PROP_FPS)
        self.timer.set_fps(fps)
        self.playCapture.release()

    def set_video(self, url, video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        self.reset()
        self.video_url = url
        self.video_type = video_type
        self.auto_play = auto_play
        self.set_timer_fps()
        if self.auto_play:
            self.switch_video()

    def play(self):
        if self.video_url == "" or self.video_url is None:
            return
        if not self.playCapture.isOpened():
            self.playCapture.open(self.video_url)
        self.timer.start()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.status = VideoBox.STATUS_PLAYING

    def stop(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.playCapture.isOpened():
            self.timer.stop()
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.status = VideoBox.STATUS_PAUSE

    def re_play(self):
        if self.video_url == "" or self.video_url is None:
            return
        self.playCapture.release()
        self.playCapture.open(self.video_url)
        self.timer.start()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.status = VideoBox.STATUS_PLAYING

    def srcnn_img(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                ret_model = self.model.get_model()
                result = predict_img(frame, ret_model)
                
                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                temp_image2 = QImage(result.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap2 = QPixmap.fromImage(temp_image2)
                self.pictureLabel.setPixmap(temp_pixmap)
                self.pictureLabel2.setPixmap(temp_pixmap2)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoBox.VIDEO_TYPE_OFFLINE:
                    print("play finished")
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                r, g, b = split(rgb)
                r_equal = equalizeHist(r)
                g_equal = equalizeHist(g)
                b_equal = equalizeHist(b)
                result = merge([r_equal, g_equal, b_equal])
                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                temp_image2 = QImage(result.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap2 = QPixmap.fromImage(temp_image2)
                self.pictureLabel.setPixmap(temp_pixmap)
                self.pictureLabel2.setPixmap(temp_pixmap2)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoBox.VIDEO_TYPE_OFFLINE:
                    print("play finished")
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def CopyPlay(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                temp_image2 = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap2 = QPixmap.fromImage(temp_image2)
                self.pictureLabel.setPixmap(temp_pixmap)
                self.pictureLabel2.setPixmap(temp_pixmap2)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoBox.VIDEO_TYPE_OFFLINE:
                    print("play finished")
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def switch_video(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.status is VideoBox.STATUS_INIT:
            self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        elif self.status is VideoBox.STATUS_PLAYING:
            self.timer.stop()
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.status is VideoBox.STATUS_PAUSE:
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        self.status = (VideoBox.STATUS_PLAYING,
                       VideoBox.STATUS_PAUSE,
                       VideoBox.STATUS_PLAYING)[self.status]


class Communicate(QObject):

    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps


if __name__ == "__main__":
    mapp = QApplication(sys.argv)
    mw = VideoBox()
    mw.set_video("./endoscope.mp4", VideoBox.VIDEO_TYPE_OFFLINE, False)
    mw.show()
    sys.exit(mapp.exec_())