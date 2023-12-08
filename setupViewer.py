from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
import glob
import setupEditor
import setupMenubar
import setupViewerUi
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.currentImagePos = 0
        self.image_list = []

        self.ui = setupViewerUi.setupViewer()
        self.ui.setupUi(MainWindow)

        self.ui.menu.actionImport.triggered.connect(lambda: self.importImages())
        self.ui.button1.clicked.connect(lambda: self.prevImage())
        self.ui.button2.clicked.connect(lambda: self.nextImage())
        self.ui.button3.clicked.connect(lambda: self.editWindow(MainWindow))

    def showPopupCritical(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR!")
        msg.setText(message)
        msg.setInformativeText("Import files to begin viewing.")
        msg.setDetailedText("Press Ctrl+O or look at the \"File\" menu to import files.")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        x = msg.exec()

    def importImages(self):
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        self.image_list = [filename for i in
                          [glob.glob(self.folderpath + '/*.%s' %ext)
                           for ext in ["jpg", "png", "jpeg", "tiff", "arw"]]for filename in i]
        self.numberOfFiles = len(self.image_list)
        self.nextImage()

    def nextImage(self):
        try:
            if (self.currentImagePos >= 0 and self.currentImagePos + 1 < self.numberOfFiles):
                self.currentImagePos += 1
            elif (self.currentImagePos + 1 >= self.numberOfFiles):
                self.currentImagePos = 0

            self.currentImage = self.image_list[self.currentImagePos]
            self.pixmap = QPixmap(self.currentImage)
            self.ui.label.setPixmap(self.pixmap.scaled(self.ui.label.width(),self.ui.label.height(),QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        except AttributeError:
            self.showPopupCritical("No input files.")

    def prevImage(self):
        try:
            if (self.currentImagePos == 0):
                self.currentImagePos = self.numberOfFiles - 1
            elif (self.currentImagePos <= self.numberOfFiles - 1  and self.currentImagePos > 0):
                self.currentImagePos -= 1
            elif (self.currentImagePos - 1 >= self.numberOfFiles):
                self.currentImagePos = 0

            self.currentImage = self.image_list[self.currentImagePos]
            self.pixmap = QPixmap(self.currentImage)
            self.ui.label.setPixmap(self.pixmap.scaled(self.ui.label.width(),self.ui.label.height(),QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        except AttributeError:
            self.showPopupCritical("No input files.")

    def editWindow(self, MainWindow):
        try:
            editorWindow = setupEditor.editor()
            editorWindow.setupUi(MainWindow, self.currentImage)
        except AttributeError:
            self.showPopupCritical("No image to edit!")
