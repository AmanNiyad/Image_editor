from PyQt6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from PIL import Image
import sys

class setupEditor(object):
    def setupUi(self, MainWindow, img):
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.createSlidingMenu()
        self.createDisplayPanel()
        self.createEditingPanel()

        self.imageProcessingButton.clicked.connect(lambda: self.showProcessingPage())
        self.imageOperationsButton.clicked.connect(lambda: self.showOperationsPage())
        self.imageEffectsButton.clicked.connect(lambda: self.showEffectsPage())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def hideSlidingMenuButtons(self):
        self.saveButton.hide()
        self.saveAsButton.hide()
        self.quitButton.hide()
        self.textBrowser.hide()
        self.line_3.hide()
        self.line_4.hide()

    def showSlidingMenuButtons(self):
        self.saveButton.show()
        self.saveAsButton.show()
        self.quitButton.show()
        self.textBrowser.show()
        self.line_3.show()
        self.line_4.show()

    def createSlidingMenu(self):
        self.slidingMenuFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.slidingMenuFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.slidingMenuFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.slidingMenuFrame.setObjectName("slidingMenuFrame")

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.slidingMenuFrame)
        self.verticalLayout_5.setSpacing(8)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Buttton to toggle menu
        self.toggleMenuButton = QtWidgets.QPushButton(parent=self.slidingMenuFrame)
        self.toggleMenuButton.setObjectName("toggleMenuButton")
        self.verticalLayout_5.addWidget(self.toggleMenuButton)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)

        self.line_4 = QtWidgets.QFrame(parent=self.slidingMenuFrame)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_5.addWidget(self.line_4)

        # Save Button
        self.saveButton = QtWidgets.QPushButton(parent=self.slidingMenuFrame)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_5.addWidget(self.saveButton)
        self.saveAsButton = QtWidgets.QPushButton(parent=self.slidingMenuFrame)
        self.saveAsButton.setObjectName("saveAsButton")
        self.verticalLayout_5.addWidget(self.saveAsButton)

        self.line_3 = QtWidgets.QFrame(parent=self.slidingMenuFrame)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_5.addWidget(self.line_3)

        self.textBrowser = QtWidgets.QTextBrowser(parent=self.slidingMenuFrame)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_5.addWidget(self.textBrowser)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)

        # QuitButton
        self.quitButton = QtWidgets.QPushButton(parent=self.slidingMenuFrame)
        self.quitButton.setObjectName("quitButton")
        self.verticalLayout_5.addWidget(self.quitButton)

        self.verticalLayout_5.setStretch(6, 1)
        self.horizontalLayout_2.addWidget(self.slidingMenuFrame)

    def createDisplayPanel(self):
        self.displayFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.displayFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.displayFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.displayFrame.setObjectName("displayFrame")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.displayFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.gv = QtWidgets.QGraphicsView(parent=self.displayFrame)
        self.gv.setObjectName("gv")
        self.gv.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2.addWidget(self.gv)

        self.infoLabel = QtWidgets.QLabel(parent=self.displayFrame)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout_2.addWidget(self.infoLabel)

        self.verticalLayout_2.setStretch(0, 2)

        self.horizontalLayout_2.addWidget(self.displayFrame)

    def createEditingPanel(self):
        self.editingPanel = QtWidgets.QFrame(parent=self.centralwidget)
        self.editingPanel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.editingPanel.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.editingPanel.setObjectName("editingPanel")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.editingPanel)
        self.verticalLayout.setObjectName("verticalLayout")

        self.createGraphWidget()
        self.createEditingPanelMenu()
        self.createStackedWidget()

        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(2, 6)
        self.verticalLayout.setStretch(3, 3)

        self.horizontalLayout_2.addWidget(self.editingPanel)
        self.horizontalLayout_2.setStretch(1, 8)
        self.horizontalLayout_2.setStretch(2, 1)

    def createGraphWidget(self):
        self.plot = pg.PlotWidget()
        self.verticalLayout.addWidget(self.plot)

    def createEditingPanelMenu(self):
        font = QtGui.QFont()
        font.setFamily("CodeNewRoman Nerd Font")
        self.menuFrame = QtWidgets.QFrame(parent=self.editingPanel)
        self.menuFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.menuFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.menuFrame.setObjectName("menuFrame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.menuFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.imageProcessingButton = QtWidgets.QPushButton(parent=self.menuFrame)
        self.imageProcessingButton.setFont(font)
        self.imageProcessingButton.setObjectName("imageProcessingButton")
        self.horizontalLayout.addWidget(self.imageProcessingButton)

        self.line = QtWidgets.QFrame(parent=self.menuFrame)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line
                                        )
        self.imageOperationsButton = QtWidgets.QPushButton(parent=self.menuFrame)
        self.imageOperationsButton.setFont(font)
        self.imageOperationsButton.setObjectName("imageOperationsButton")
        self.horizontalLayout.addWidget(self.imageOperationsButton)

        self.line_2 = QtWidgets.QFrame(parent=self.menuFrame)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)

        self.imageEffectsButton = QtWidgets.QPushButton(parent=self.menuFrame)
        self.imageEffectsButton.setFont(font)
        self.imageEffectsButton.setObjectName("imageEffectsButton")
        self.horizontalLayout.addWidget(self.imageEffectsButton)

        self.verticalLayout.addWidget(self.menuFrame)

    def createStackedWidget(self):
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.editingPanel)
        self.stackedWidget.setObjectName("stackedWidget")

        self.createProcessingPage()
        self.createOperationsPage()
        self.createEffectsPage()

        self.verticalLayout.addWidget(self.stackedWidget)

    def createProcessingPage(self):
        self.processingPage = QtWidgets.QWidget()
        self.processingPage.setObjectName("processingPage")

        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.processingPage)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # Brightness
        self.brightnessWidget = QtWidgets.QWidget(parent=self.processingPage)
        self.brightnessWidget.setObjectName("brightnessWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.brightnessWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.brightnessSlider = QtWidgets.QSlider(parent=self.brightnessWidget)
        self.brightnessSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.gridLayout.addWidget(self.brightnessSlider, 1, 0, 1, 2)
        self.brightnessInputBox = QtWidgets.QDoubleSpinBox(parent=self.brightnessWidget)
        self.brightnessInputBox.setObjectName("brightnessInputBox")
        self.gridLayout.addWidget(self.brightnessInputBox, 0, 1, 1, 1)
        self.brightnessLabel = QtWidgets.QLabel(parent=self.brightnessWidget)
        self.brightnessLabel.setObjectName("brightnessLabel")
        self.gridLayout.addWidget(self.brightnessLabel, 0, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.brightnessWidget)

        self.line_5 = QtWidgets.QFrame(parent=self.processingPage)
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_6.addWidget(self.line_5)

        # Contrast
        self.contrastWidget = QtWidgets.QWidget(parent=self.processingPage)
        self.contrastWidget.setObjectName("contrastWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.contrastWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.contrastLabel = QtWidgets.QLabel(parent=self.contrastWidget)
        self.contrastLabel.setObjectName("contrastLabel")
        self.gridLayout_2.addWidget(self.contrastLabel, 0, 0, 1, 1)
        self.contrastInputBox = QtWidgets.QDoubleSpinBox(parent=self.contrastWidget)
        self.contrastInputBox.setObjectName("contrastInputBox")
        self.gridLayout_2.addWidget(self.contrastInputBox, 0, 1, 1, 1)
        self.contrastSlider = QtWidgets.QSlider(parent=self.contrastWidget)
        self.contrastSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.gridLayout_2.addWidget(self.contrastSlider, 1, 0, 1, 2)
        self.verticalLayout_6.addWidget(self.contrastWidget)

        self.line_6 = QtWidgets.QFrame(parent=self.processingPage)
        self.line_6.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_6.addWidget(self.line_6)

        # Vibrance
        self.vibranceWidget = QtWidgets.QWidget(parent=self.processingPage)
        self.vibranceWidget.setObjectName("vibranceWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.vibranceWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.vibranceLabel = QtWidgets.QLabel(parent=self.vibranceWidget)
        self.vibranceLabel.setObjectName("vibranceLabel")
        self.gridLayout_3.addWidget(self.vibranceLabel, 0, 0, 1, 1)
        self.vibranceInputBox = QtWidgets.QDoubleSpinBox(parent=self.vibranceWidget)
        self.vibranceInputBox.setObjectName("vibranceInputBox")
        self.gridLayout_3.addWidget(self.vibranceInputBox, 0, 1, 1, 1)
        self.vibranceSlider = QtWidgets.QSlider(parent=self.vibranceWidget)
        self.vibranceSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.vibranceSlider.setObjectName("vibranceSlider")
        self.gridLayout_3.addWidget(self.vibranceSlider, 1, 0, 1, 2)
        self.verticalLayout_6.addWidget(self.vibranceWidget)

        self.line_7 = QtWidgets.QFrame(parent=self.processingPage)
        self.line_7.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_6.addWidget(self.line_7)

        # Highlights
        self.highlightsWidget = QtWidgets.QWidget(parent=self.processingPage)
        self.highlightsWidget.setObjectName("highlightsWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.highlightsWidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.highlightsLabel = QtWidgets.QLabel(parent=self.highlightsWidget)
        self.highlightsLabel.setObjectName("highlightsLabel")
        self.gridLayout_4.addWidget(self.highlightsLabel, 0, 0, 1, 1)
        self.highlightsInputBox = QtWidgets.QDoubleSpinBox(parent=self.highlightsWidget)
        self.highlightsInputBox.setObjectName("highlightsInputBox")
        self.gridLayout_4.addWidget(self.highlightsInputBox, 0, 1, 1, 1)
        self.highlightsSlider = QtWidgets.QSlider(parent=self.highlightsWidget)
        self.highlightsSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.highlightsSlider.setObjectName("highlightsSlider")
        self.gridLayout_4.addWidget(self.highlightsSlider, 1, 0, 1, 2)
        self.verticalLayout_6.addWidget(self.highlightsWidget)

        self.line_8 = QtWidgets.QFrame(parent=self.processingPage)
        self.line_8.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_6.addWidget(self.line_8)

        # Shadows
        self.shadowsWidget = QtWidgets.QWidget(parent=self.processingPage)
        self.shadowsWidget.setObjectName("shadowsWidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.shadowsWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.shadowsLabel = QtWidgets.QLabel(parent=self.shadowsWidget)
        self.shadowsLabel.setObjectName("shadowsLabel")
        self.gridLayout_5.addWidget(self.shadowsLabel, 0, 0, 1, 1)
        self.shadowsInputBox = QtWidgets.QDoubleSpinBox(parent=self.shadowsWidget)
        self.shadowsInputBox.setObjectName("shadowsInputBox")
        self.gridLayout_5.addWidget(self.shadowsInputBox, 0, 1, 1, 1)
        self.shadowsSlider = QtWidgets.QSlider(parent=self.shadowsWidget)
        self.shadowsSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.shadowsSlider.setObjectName("shadowsSlider")
        self.gridLayout_5.addWidget(self.shadowsSlider, 1, 0, 1, 2)
        self.verticalLayout_6.addWidget(self.shadowsWidget)

        self.line_10 = QtWidgets.QFrame(parent=self.processingPage)
        self.line_10.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_10.setObjectName("line_10")
        self.verticalLayout_6.addWidget(self.line_10)

        self.stackedWidget.addWidget(self.processingPage)

    def createOperationsPage(self):
        self.operationsPage = QtWidgets.QWidget()
        self.operationsPage.setObjectName("operationsPage")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.operationsPage)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        # Crop
        self.cropWidget = QtWidgets.QWidget(parent=self.operationsPage)
        self.cropWidget.setObjectName("cropWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.cropWidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.cropButton = QtWidgets.QPushButton(parent=self.cropWidget)
        self.cropButton.setObjectName("cropButton")
        self.gridLayout_6.addWidget(self.cropButton, 0, 0, 1, 2)
        self.cropConfirmButton = QtWidgets.QPushButton(parent=self.cropWidget)
        self.cropConfirmButton.setObjectName("cropConfirmButton")
        self.gridLayout_6.addWidget(self.cropConfirmButton, 1, 0, 1, 1)
        self.cropCancelButton = QtWidgets.QPushButton(parent=self.cropWidget)
        self.cropCancelButton.setObjectName("cropCancelButton")
        self.gridLayout_6.addWidget(self.cropCancelButton, 1, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.cropWidget)

        self.line_9 = QtWidgets.QFrame(parent=self.operationsPage)
        self.line_9.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_9.setObjectName("line_9")
        self.verticalLayout_7.addWidget(self.line_9)

        # Rotate
        self.rotateWidget = QtWidgets.QWidget(parent=self.operationsPage)
        self.rotateWidget.setObjectName("rotateWidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.rotateWidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.rotateButton = QtWidgets.QPushButton(parent=self.rotateWidget)
        self.rotateButton.setObjectName("rotateButton")
        self.gridLayout_7.addWidget(self.rotateButton, 0, 0, 1, 2)
        self.rotateSlider = QtWidgets.QSlider(parent=self.rotateWidget)
        self.rotateSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rotateSlider.setObjectName("rotateSlider")
        self.gridLayout_7.addWidget(self.rotateSlider, 1, 0, 1, 2)
        self.rotateConfirmButton = QtWidgets.QPushButton(parent=self.rotateWidget)
        self.rotateConfirmButton.setObjectName("rotateConfirmButton")
        self.gridLayout_7.addWidget(self.rotateConfirmButton, 2, 0, 1, 1)
        self.rotateCancelButton = QtWidgets.QPushButton(parent=self.rotateWidget)
        self.rotateCancelButton.setObjectName("rotateCancelButton")
        self.gridLayout_7.addWidget(self.rotateCancelButton, 2, 1, 1, 1)
        self.verticalLayout_7.addWidget(self.rotateWidget)

        self.line_11 = QtWidgets.QFrame(parent=self.operationsPage)
        self.line_11.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_11.setObjectName("line_11")
        self.verticalLayout_7.addWidget(self.line_11)

        self.stackedWidget.addWidget(self.operationsPage)

    def createEffectsPage(self):
        self.effectsPage = QtWidgets.QWidget()
        self.effectsPage.setObjectName("effectsPage")

        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.effectsPage)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        # Sharpness
        self.sharpnessWidget = QtWidgets.QWidget(parent=self.effectsPage)
        self.sharpnessWidget.setObjectName("sharpnessWidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.sharpnessWidget)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.sharpnessLabel = QtWidgets.QLabel(parent=self.sharpnessWidget)
        self.sharpnessLabel.setObjectName("sharpnessLabel")
        self.gridLayout_8.addWidget(self.sharpnessLabel, 0, 0, 1, 1)
        self.sharpnessInputBox = QtWidgets.QDoubleSpinBox(parent=self.sharpnessWidget)
        self.sharpnessInputBox.setObjectName("sharpnessInputBox")
        self.gridLayout_8.addWidget(self.sharpnessInputBox, 0, 1, 1, 1)
        self.sharpnessSlider = QtWidgets.QSlider(parent=self.sharpnessWidget)
        self.sharpnessSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sharpnessSlider.setObjectName("sharpnessSlider")
        self.gridLayout_8.addWidget(self.sharpnessSlider, 1, 0, 1, 2)
        self.verticalLayout_8.addWidget(self.sharpnessWidget)

        self.line_12 = QtWidgets.QFrame(parent=self.effectsPage)
        self.line_12.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_12.setObjectName("line_12")
        self.verticalLayout_8.addWidget(self.line_12)

        # Edges
        self.edgesWidget = QtWidgets.QWidget(parent=self.effectsPage)
        self.edgesWidget.setObjectName("edgesWidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.edgesWidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.edgesConfirmButton = QtWidgets.QPushButton(parent=self.edgesWidget)
        self.edgesConfirmButton.setObjectName("edgesConfirmButton")
        self.gridLayout_9.addWidget(self.edgesConfirmButton, 1, 0, 1, 1)
        self.edgesCancelButton = QtWidgets.QPushButton(parent=self.edgesWidget)
        self.edgesCancelButton.setObjectName("edgesCancelButton")
        self.gridLayout_9.addWidget(self.edgesCancelButton, 1, 1, 1, 1)
        self.edgesButton = QtWidgets.QPushButton(parent=self.edgesWidget)
        self.edgesButton.setObjectName("edgesButton")
        self.gridLayout_9.addWidget(self.edgesButton, 0, 0, 1, 2)
        self.verticalLayout_8.addWidget(self.edgesWidget)

        self.line_13 = QtWidgets.QFrame(parent=self.effectsPage)
        self.line_13.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_13.setObjectName("line_13")
        self.verticalLayout_8.addWidget(self.line_13)

        # Smooth
        self.smoothWidget = QtWidgets.QWidget(parent=self.effectsPage)
        self.smoothWidget.setObjectName("smoothWidget")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.smoothWidget)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.smoothConfirmButton = QtWidgets.QPushButton(parent=self.smoothWidget)
        self.smoothConfirmButton.setObjectName("smoothConfirmButton")
        self.gridLayout_10.addWidget(self.smoothConfirmButton, 1, 0, 1, 1)
        self.smoothButton = QtWidgets.QPushButton(parent=self.smoothWidget)
        self.smoothButton.setObjectName("smoothButton")
        self.gridLayout_10.addWidget(self.smoothButton, 0, 0, 1, 2)
        self.smoothCancelButton = QtWidgets.QPushButton(parent=self.smoothWidget)
        self.smoothCancelButton.setEnabled(True)
        self.smoothCancelButton.setObjectName("smoothCancelButton")
        self.gridLayout_10.addWidget(self.smoothCancelButton, 1, 1, 1, 1)
        self.verticalLayout_8.addWidget(self.smoothWidget)

        self.line_14 = QtWidgets.QFrame(parent=self.effectsPage)
        self.line_14.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_14.setObjectName("line_14")
        self.verticalLayout_8.addWidget(self.line_14)

        # Blur
        self.blurWidget = QtWidgets.QWidget(parent=self.effectsPage)
        self.blurWidget.setObjectName("blurWidget")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.blurWidget)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.blurConfirmButton = QtWidgets.QPushButton(parent=self.blurWidget)
        self.blurConfirmButton.setObjectName("blurConfirmButton")
        self.gridLayout_11.addWidget(self.blurConfirmButton, 2, 0, 1, 2)
        self.blurButton = QtWidgets.QPushButton(parent=self.blurWidget)
        self.blurButton.setObjectName("blurButton")
        self.gridLayout_11.addWidget(self.blurButton, 0, 0, 1, 4)
        self.blurCancelButton = QtWidgets.QPushButton(parent=self.blurWidget)
        self.blurCancelButton.setObjectName("blurCancelButton")
        self.gridLayout_11.addWidget(self.blurCancelButton, 2, 2, 1, 2)
        self.boxBlurRadioButton = QtWidgets.QRadioButton(parent=self.blurWidget)
        self.boxBlurRadioButton.setObjectName("boxBlurRadioButton")
        self.gridLayout_11.addWidget(self.boxBlurRadioButton, 1, 2, 1, 2)
        self.gaussionBlurRadioButton = QtWidgets.QRadioButton(parent=self.blurWidget)
        self.gaussionBlurRadioButton.setObjectName("gaussionBlurRadioButton")
        self.gridLayout_11.addWidget(self.gaussionBlurRadioButton, 1, 0, 1, 2)
        self.verticalLayout_8.addWidget(self.blurWidget)
        self.line_15 = QtWidgets.QFrame(parent=self.effectsPage)
        self.line_15.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_15.setObjectName("line_15")
        self.verticalLayout_8.addWidget(self.line_15)

        self.stackedWidget.addWidget(self.effectsPage)

    def showProcessingPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showOperationsPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def showEffectsPage(self):
        self.stackedWidget.setCurrentIndex(2)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toggleMenuButton.setText(_translate("MainWindow", "Menu"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.saveAsButton.setText(_translate("MainWindow", "SaveAs"))
        self.quitButton.setText(_translate("MainWindow", "Quit"))
        self.infoLabel.setText(_translate("MainWindow", "TextLabel"))
        self.imageProcessingButton.setText(_translate("MainWindow", "Proccesing"))
        self.imageOperationsButton.setText(_translate("MainWindow", "Operations"))
        self.imageEffectsButton.setText(_translate("MainWindow", "Effects"))
        self.brightnessLabel.setText(_translate("MainWindow", "Brightness"))
        self.contrastLabel.setText(_translate("MainWindow", "Contrast"))
        self.vibranceLabel.setText(_translate("MainWindow", "Vibrance"))
        self.highlightsLabel.setText(_translate("MainWindow", "Highlights"))
        self.shadowsLabel.setText(_translate("MainWindow", "Shadows"))
        self.cropButton.setText(_translate("MainWindow", "Crop"))
        self.cropConfirmButton.setText(_translate("MainWindow", "Confirm"))
        self.cropCancelButton.setText(_translate("MainWindow", "Cancel"))
        self.rotateButton.setText(_translate("MainWindow", "Rotate"))
        self.rotateConfirmButton.setText(_translate("MainWindow", "Confirm"))
        self.rotateCancelButton.setText(_translate("MainWindow", "Cancel"))
        self.sharpnessLabel.setText(_translate("MainWindow", "Sharpness"))
        self.edgesConfirmButton.setText(_translate("MainWindow", "Confirm"))
        self.edgesCancelButton.setText(_translate("MainWindow", "Cancel"))
        self.edgesButton.setText(_translate("MainWindow", "Edges"))
        self.smoothConfirmButton.setText(_translate("MainWindow", "Confirm"))
        self.smoothButton.setText(_translate("MainWindow", "Smooth"))
        self.smoothCancelButton.setText(_translate("MainWindow", "Cancel"))
        self.blurConfirmButton.setText(_translate("MainWindow", "Confirm"))
        self.blurButton.setText(_translate("MainWindow", "Blur"))
        self.blurCancelButton.setText(_translate("MainWindow", "Cancel"))
        self.boxBlurRadioButton.setText(_translate("MainWindow", "Box"))
        self.gaussionBlurRadioButton.setText(_translate("MainWindow", "Gaussian"))
