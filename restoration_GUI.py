import sys

from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QAction, QFileDialog, QApplication
from PyQt5.QtGui import  QPixmap, QFont
from PyQt5.QtCore import Qt


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *

from data_preprocessing import predict, convert_cv_qt
from SRCNN_model import model
from keras import backend



class Window(QMainWindow):
      
      def __init__(self):
            super().__init__()
            
            # main window
            self.width = 950
            self.height = 500
            
            self.setWindowTitle("Endoscope Image Restoration & Enhancement")
            self.setGeometry(200, 200, self.width, self.height)
#            self.setWindowIcon(QIcon("icon.jpg"))           
                         
            self.showMenubar()
            self.center()
            
            self.labels()   
            
            self.showSaveButton()
            
            self.inputImageShow()
            self.outputImageShow()
            
            self.model = model()
            
            self.show()
            
            
      def __del__(self):
            del self.model 
            backend.clear_session()

      # center setting
      def center(self):
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
            
            
      def showMenubar(self):
            menu = self.menuBar()
            
            # file mune
            fileMenu = menu.addMenu('File')
            # open
            openAction = QAction('Open', self)  
            fileMenu.addAction(openAction)
            openAction.triggered.connect(self.openImage)
            # save
            saveAction = QAction('Save', self)
            fileMenu.addAction(saveAction)
            # saveAction.triggered.connect(self.openImage)

            # distortion menu
            distormenu = menu.addMenu('Distortion-Correction')
            # Distortion Correction
            distroAction = QAction('Distortion-Correction', self)
            distormenu.addAction(distroAction)
            # histnormalized
            histAction = QAction('Hist-Normalized', self)
            distormenu.addAction(histAction)
            histAction.triggered.connect(self.histNormalized)

            # denoising
            denoisingmenu = menu.addMenu('Denoising')
            # denoising
            denoisingAction = QAction('Denoising', self)
            denoisingmenu.addAction(denoisingAction)

            # highlight removal
            highlightmenu = menu.addMenu('Highlight-removal')
            # highlight removal
            hightlightAction = QAction('Hightlight', self)
            highlightmenu.addAction(hightlightAction)

            # restoration menu
            ResMenu = menu.addMenu('Super-resolution')
            SRCNNAction = QAction('SRCNN', self)  
            ResMenu.addAction(SRCNNAction)
            SRCNNAction.triggered.connect(self.SRCNNImage)
            
            
      def openImage(self):
            self.imagePath, _ = QFileDialog.getOpenFileName(self, filter="Image Files (*.jpg *.bmp *.png *.mp4)")
            pixmap = QPixmap(self.imagePath)
            self.setInputPixmap(pixmap)
            
            
      def labels(self):
            self.labelInputText = QLabel("Input ", self)
            self.labelInputText.move(50,40)
            self.labelInputText.setFont(QFont("Arial", 9, QFont.Bold))
            
            self.labelOutputText = QLabel("Output ", self)
            self.labelOutputText.move(500,40)
            self.labelOutputText.setFont(QFont("Arial", 9, QFont.Bold))
                              
            
      def inputImageShow(self):
            self.inputImage = QLabel(self)
            self.inputImage.resize(400, 400)
            self.inputImage.move(50, 80)
            
            
      def outputImageShow(self):
            self.outputImage = QLabel(self)
            self.outputImage.resize(400, 400)
            self.outputImage.move(500, 80)
            
            
      def showSaveButton(self):
            self.saveBtn = QPushButton("Save", self)
            self.saveBtn.move(800,40)
            
            self.saveBtn.clicked.connect(self.saveBtnFunction)
          
      def setInputPixmap(self, pixmap):   
            smaller_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.inputImage.setPixmap(smaller_pixmap)
            
            
      def setOutputPixmap(self, qImage):
            self.qImage_scaled = qImage.scaled(400, 400, Qt.KeepAspectRatio)
            self.outputImage.setPixmap(QPixmap.fromImage(self.qImage_scaled))

      
      def SRCNNImage(self):
            ret_model = self.model.get_model()
            srcnn_BGR = predict(self.imagePath, ret_model)
            self.srcnn_qt = convert_cv_qt(srcnn_BGR)
            self.setOutputPixmap(self.srcnn_qt)

      def histNormalized(self):
            img = imread(self.imagePath)
            b, g, r = split(img)
            b_equal = equalizeHist(b)
            g_equal = equalizeHist(g)
            r_equal = equalizeHist(r)
            result = merge([b_equal, g_equal, r_equal])
            self.srcnn_qt = convert_cv_qt(result)
            self.setOutputPixmap(self.srcnn_qt)

      def saveBtnFunction(self):
            self.imagePath, _ = QFileDialog.getSaveFileName(self, filter="Image Files (*.jpg *.bmp *.png *.mp4)")
            self.srcnn_qt.save(self.imagePath, format="bmp")
            # self.srcnn_qt.save(self.imagePath.split("/")[-1], format="bmp")



if __name__ == '__main__':
      
      app = QApplication(sys.argv)
    
      windowObject = Window()

      sys.exit(app.exec_())