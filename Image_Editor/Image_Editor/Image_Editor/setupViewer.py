from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMessageBox
import glob
import setupEditor
import setupViewerUi


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.currentImagePos = 0
        self.image_list = []

        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setObjectName("mainwidget")

        MainWindow.setCentralWidget(self.MainWidget)

        self.ui = setupViewerUi.setupViewer()
        self.ui.setupUi(MainWindow, self.MainWidget)
        self.gv = QGraphicsView(self.MainWidget)
        self.scene = QGraphicsScene()
        self.gv.setGeometry(QtCore.QRect(0, 10, 1920, 950))

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
        if (self.currentImagePos >= 0 and self.currentImagePos + 1 < self.numberOfFiles):
            self.currentImagePos += 1
        elif (self.currentImagePos + 1 >= self.numberOfFiles):
            self.currentImagePos = 0
        self.currentImage = self.image_list[self.currentImagePos]
        self.pixmap = QPixmap(self.currentImage)
        self.scene_img = self.scene.addPixmap(self.pixmap)
        self.gv.setScene(self.scene)
        self.gv.show()
        self.fitInView()

    def nextImage(self):
        try:
            if (self.currentImagePos >= 0 and self.currentImagePos + 1 < self.numberOfFiles):
                self.currentImagePos += 1
            elif (self.currentImagePos + 1 >= self.numberOfFiles):
                self.currentImagePos = 0

            self.updateImage()


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

            self.updateImage()
        except AttributeError:
            self.showPopupCritical("No input files.")

    def editWindow(self, MainWindow):
        #try:
            for i in (self.MainWidget.findChildren(QtWidgets.QWidget)):
                i.deleteLater()

            self.ui.menu.menubar.deleteLater()

            editorWindow = setupEditor.editor()
            editorWindow.setupUi(MainWindow, self.currentImage)
        #except AttributeError:
        #    self.showPopupCritical("Attribute Error")

    def fitInView(self):
        rect = QtCore.QRectF(self.pixmap.rect())
        if not rect.isNull():
            self.gv.setSceneRect(rect)

            unity = self.gv.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.gv.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.gv.viewport().rect()
            scene_rect = self.gv.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.gv.scale(factor, factor)
            self._zoom = 0
            self.zoom_factor = factor

    def updateImage(self):
        self.scene.removeItem(self.scene_img)
        self.currentImage = self.image_list[self.currentImagePos]
        self.pixmap = QPixmap(self.currentImage)
        self.scene_img = self.scene.addPixmap(self.pixmap)
        self.gv.setScene(self.scene)
        self.gv.show()
        self.fitInView()
