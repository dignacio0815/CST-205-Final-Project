import sys
import sip #Install sip
import shlex
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QHBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from google.cloud import translate
from function import *

translate_client = translate.Client()
results = translate_client.get_languages()

func = ImageToText()
class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Image Translator")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        lay = QVBoxLayout(self.central_widget)
        label = QLabel(self)
        pixmap = QPixmap('welcome.jpg')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.button = QPushButton("Upload Image", self)
        self.uploadLabel = QLabel(self)
        self.button.clicked.connect(self.onClick)
        lay.addWidget(self.button)
        lay.addWidget(self.uploadLabel)
        self.translatebtn = QPushButton("Translate", self)
        self.translatebtn.clicked.connect(self.on_click)
        self.comboBox = QComboBox()
        
        for lang in range(len(results)):
            self.comboBox.addItem(str(lang + 1) + '. ' + results[lang]['name'] + " " + results[lang]['language'])

        lay.addWidget(self.translatebtn)
        lay.addWidget(self.comboBox)
        lay.addWidget(label)
        
    @pyqtSlot()
    def onClick(self):
        global getWords
        fname, _ = QFileDialog.getOpenFileName(self.uploadLabel, 'Open File', '/usr/tmp', "Images (*.jpg *png)")
        getWords = func.getText(fname) #extracted text from image is here
        self.uploadLabel.setPixmap(QPixmap(fname))

    def on_click(self):
        global translated_text
        current_value = self.comboBox.currentText()  
        result = translate_client.detect_language(getWords)
        split = shlex.split(current_value)
        iso_target = split[-1]
        translated_text = func.translate(getWords, iso_target)
        self.display_second_window = Second(translated_text)


class Second (QWidget):
    def __init__(self, text):
        super ().__init__ ()
        self.setWindowTitle("Translated Text")
        self.initUI(text)

    def initUI(self, text):
        label = QLabel()
        label.setText("Your translated text: " + text)#+ translated_text)
        label.adjustSize()
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        self.setLayout(hbox)
        self.show()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )
