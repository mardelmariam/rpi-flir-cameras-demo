"""!@brief Ejemplo de funcionamiento de cámaras Raspberry Pi y FLIR Lepton

@author: Maryam del Mar Correa
@version 1.0
@date 2021

"""

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

import numpy as np
from cv2 import cv2
from pylepton import Lepton
from picamera import PiCamera

import sys
import time

resHeight = 0
resWidth = 0
camera = PiCamera()

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo de cámaras para Raspberry Pi")
        self.setGeometry(100, 100, int(resWidth*0.7), int(resHeight*0.45))
        self.UI()
        
    def UI(self):
        
        # Establishing layouts
        mainLayout = QGridLayout()
        
        # Setting up widgets for layouts
        self.text1 = QLabel("FLIR Lepton Camera", self)
        self.text1.resize(200, 30)
        self.text2 = QLabel("Raspberry Pi Camera", self)
        self.text2.resize(200, 30)
        self.image1 = QLabel(self)
        self.image1.setPixmap(QPixmap('output22.jpg'))
        self.image1.move(150, 50)
        self.image2 = QLabel(self)
        camera.capture('foto.jpg')
        
        #Adding widgets to layouts
        mainLayout.addWidget(self.text1, 0, 0, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.image1, 1, 0, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.text2, 0, 1, QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.image2, 1, 1, QtCore.Qt.AlignCenter)
        
        #Setting up timer for image acquisition
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.loadImage)
        self.timer.start()
        
        #Show UI
        self.setLayout(mainLayout)
        self.show()
        
    def loadImage(self):
        
        # Show picture from Lepton camera
        with Lepton() as l:
            a,_ = l.capture()
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
        np.right_shift(a, 8, a) # fit data into 8 bits
        cv2.imwrite("output22.jpg", np.uint8(a))
        original_pixmap = QPixmap('output22.jpg')
        bigger_pixmap = original_pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.image1.setPixmap(bigger_pixmap)
        self.image1.move(150, 50)
        
        # Show picture from Raspberry camera
        camera.capture('foto.jpg')
        original_pixmap = QPixmap('foto.jpg')
        smaller_pixmap = original_pixmap.scaled(480, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.image2.setPixmap(smaller_pixmap)
        self.image2.move(150, 50)
        
        #Refresh UI
        self.show()
        
def main():
    App = QApplication(sys.argv)
    global resWidth
    global resHeight
    resWidth = App.desktop().screenGeometry().width()
    resHeight = App.desktop().screenGeometry().height()
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
