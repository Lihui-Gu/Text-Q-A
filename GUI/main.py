# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog
from PyQt5.QtGui import *
from mainWindow import Ui_Dialog
import cv2
class DetailUI(Ui_Dialog,QMainWindow):
    def __init__(self):
        super(DetailUI,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('文本问答')
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=DetailUI()
    ex.show()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
