import sys
from restoration_GUI import Window
from PyQt5.QtWidgets import QApplication



if __name__ == '__main__':
      
      app = QApplication(sys.argv)
    
      windowObject = Window()

      sys.exit(app.exec_())