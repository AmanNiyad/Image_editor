from PyQt6 import QtCore, QtGui, QtWidgets
import setupMenubar
import pyqtgraph as pg
from PIL import Image

class setupEditor(object):
    def setupUi(self, MainWindow, MainWidget, img):

        self.font = QtGui.QFont()
        self.setAppFont()

        self.edit_panel = QtWidgets.QWidget(MainWidget)
        self.edit_panel.setGeometry(QtCore.QRect(1600, 0, 320, 1000))
        self.edit_panel.setObjectName("widget_2")

        self.setupBrightness()
        self.setupContrast()
        self.setupVibrance()
        self.setupSharpness()
        self.setupCrop()
        self.setupHistogram(img)

        self.menu = setupMenubar.Menubar()
        self.menu.setupBar(MainWindow)

        self.retranslateUi(MainWindow)

    def setupHistogram(self, img):
        image = Image.open(img)
        self.hist = image.histogram()

        self.plot = pg.PlotWidget(parent = self.edit_panel)

        self.plt1 = pg.PlotCurveItem(self.hist[0:256])
        self.plt2 = pg.PlotCurveItem(self.hist[256:512])
        self.plt3 = pg.PlotCurveItem(self.hist[512:768])

        self.plot.setLimits(xMin=0,yMin=0,xMax=256,yMax=max(self.hist))
        self.plot.setAspectLocked(None)
        self.plot.hideAxis('bottom')
        self.plot.hideAxis('left')

        self.plotCurves()

        self.plot.addItem(self.plt1)
        self.plot.addItem(self.plt2)
        self.plot.addItem(self.plt3)
        self.plot.setGeometry(2,2,316,200)

    def updateHistogram(self, img):
        self.plot.removeItem(self.plt1)
        self.plot.removeItem(self.plt2)
        self.plot.removeItem(self.plt3)
        self.hist = img.histogram()

        self.plt1 = pg.PlotCurveItem(self.hist[0:256], antialias=True)
        self.plt2 = pg.PlotCurveItem(self.hist[256:512], antialias=True)
        self.plt3 = pg.PlotCurveItem(self.hist[512:768], antialias=True)

        self.plotCurves()

        self.plot.addItem(self.plt1)
        self.plot.addItem(self.plt2)
        self.plot.addItem(self.plt3)

    def plotCurves(self):
        self.plt1.setBrush("Red")
        self.plt1.setFillLevel(0)
        self.plt1.setPen(None)
        self.plt1.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Plus)
        self.plt2.setBrush("Green")
        self.plt2.setFillLevel(0)
        self.plt2.setPen(None)
        self.plt2.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Plus)
        self.plt3.setBrush("Blue")
        self.plt3.setFillLevel(0)
        self.plt3.setPen(None)
        self.plt3.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Plus)

    def setAppFont(self):
        self.font.setFamily("Iosevka Nerd Font Mono")
        self.font.setPointSize(11)
        self.font.setBold(False)
        self.font.setItalic(False)
        self.font.setWeight(50)

    def setupBrightness(self):
        self.Brightness = QtWidgets.QLabel(self.edit_panel)
        self.Brightness.setGeometry(QtCore.QRect(30, 250, 90, 15))
        self.Brightness.setFont(self.font)
        self.Brightness.setObjectName("Brightness")

        self.Brightness_scroll = QtWidgets.QSlider(self.edit_panel)
        self.Brightness_scroll.setGeometry(QtCore.QRect(30, 270, 160, 16))
        self.Brightness_scroll.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Brightness_scroll.setObjectName("Brightness_scroll")
        self.Brightness_scroll.setRange(0, 3000)
        self.Brightness_scroll.setSingleStep(2)
        self.Brightness_scroll.setValue(1000)

        self.Brightness_input_box = QtWidgets.QDoubleSpinBox(self.edit_panel)
        self.Brightness_input_box.setGeometry(QtCore.QRect(130, 250, 60, 20))
        self.Brightness_input_box.setObjectName("Brightness_input_box")

    def setupContrast(self):
        self.Contrast = QtWidgets.QLabel(self.edit_panel)
        self.Contrast.setGeometry(QtCore.QRect(30, 360, 90, 15))
        self.Contrast.setFont(self.font)
        self.Contrast.setObjectName("Contrast")

        self.Contrast_scroll = QtWidgets.QSlider(self.edit_panel)
        self.Contrast_scroll.setGeometry(QtCore.QRect(30, 380, 160, 16))
        self.Contrast_scroll.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Contrast_scroll.setObjectName("Contrast_scroll")
        self.Contrast_scroll.setRange(0, 3000)
        self.Contrast_scroll.setSingleStep(2)
        self.Contrast_scroll.setValue(1000)

        self.Contrast_input_box = QtWidgets.QDoubleSpinBox(self.edit_panel)
        self.Contrast_input_box.setGeometry(QtCore.QRect(130, 360, 60, 20))
        self.Contrast_input_box.setObjectName("Contrast_input_box")

    def setupVibrance(self):
        self.Vibrance = QtWidgets.QLabel(self.edit_panel)
        self.Vibrance.setGeometry(QtCore.QRect(30, 470, 90, 15))
        self.Vibrance.setFont(self.font)
        self.Vibrance.setObjectName("Vibrance")

        self.Vibrance_scroll = QtWidgets.QSlider(self.edit_panel)
        self.Vibrance_scroll.setGeometry(QtCore.QRect(30, 490, 160, 16))
        self.Vibrance_scroll.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Vibrance_scroll.setObjectName("Vibrance_scroll")
        self.Vibrance_scroll.setRange(0, 3000)
        self.Vibrance_scroll.setSingleStep(2)
        self.Vibrance_scroll.setValue(1000)

        self.Vibrance_input_box = QtWidgets.QDoubleSpinBox(self.edit_panel)
        self.Vibrance_input_box.setGeometry(QtCore.QRect(130, 470, 60, 20))
        self.Vibrance_input_box.setObjectName("Vibrance_input_box")

    def setupSharpness(self):
        self.Sharpness = QtWidgets.QLabel(self.edit_panel)
        self.Sharpness.setGeometry(QtCore.QRect(30, 580, 90, 15))
        self.Sharpness.setFont(self.font)
        self.Sharpness.setObjectName("Sharpness")

        self.Sharpness_scroll = QtWidgets.QSlider(self.edit_panel)
        self.Sharpness_scroll.setGeometry(QtCore.QRect(30, 600, 160, 16))
        self.Sharpness_scroll.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Sharpness_scroll.setObjectName("Sharpness_scroll")
        self.Sharpness_scroll.setRange(0, 3000)
        self.Sharpness_scroll.setSingleStep(2)
        self.Sharpness_scroll.setValue(1000)

        self.Sharpness_input_box = QtWidgets.QDoubleSpinBox(self.edit_panel)
        self.Sharpness_input_box.setGeometry(QtCore.QRect(130, 580, 60, 20))
        self.Sharpness_input_box.setObjectName("Sharpness_input_box")

    def setupCrop(self):
        self.cropButton = QtWidgets.QPushButton("Crop", self.edit_panel)
        self.cropButton.setGeometry(QtCore.QRect(30, 630, 160, 15))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Brightness.setText(_translate("MainWindow", "Brightness"))
        self.Contrast.setText(_translate("MainWindow", "Contrast"))
        self.Vibrance.setText(_translate("MainWindow", "Vibrance"))
        self.Sharpness.setText(_translate("MainWindow", "Sharpness"))
