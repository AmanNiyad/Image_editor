from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PIL import Image, ImageEnhance
from PIL.ImageQt import ImageQt
import time
import pyqtgraph as pg
import setupEditorUI_new
import numpy as np
from numpy.fft import fft2, ifft2
import subprocess
try:
    import cusignal,cupy as cp
except ImportError:
    print("Operating in CPU mode")

class resizableRubberBand(QWidget):
    def __init__(self, MainWindow, im):
        super(resizableRubberBand, self).__init__(MainWindow.ui.gv)
        self.get_zoom_factor = MainWindow.get_zoom_factor
        self.draggable, self.mousePressPos, self.mouseMovePos = True, None, None
        self.left, self.right, self.top, self.bottom = None, None, None, None
        self.borderRadius = 0
        self.width, self.height = im.size

        self.setWindowFlags(Qt.WindowType.SubWindow)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        self._band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self._band.show()
        self.show()

    def update_dim(self):
        self.left, self.top = self.pos().x(), self.pos().y()
        self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top

    def resizeEvent(self, event):
        try:
            self.left, self.top = self.pos().x(), self.pos().y()
            self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top
        except:
            pass
        self._band.resize(self.size())

    def paintEvent(self, event):
        window_size = self.size()
        qp = QPainter(self)
        qp.drawRoundedRect(0, 0, window_size.width(), window_size.height(), self.borderRadius, self.borderRadius)

    def mousePressEvent(self, event):
        self.zoom_factor = self.get_zoom_factor()
        if self.draggable and event.button() == Qt.MouseButton.LeftButton:
            self.mousePressPos = event.globalPosition()  # global
            self.mouseMovePos = event.globalPosition().toPoint() - self.pos()  # local

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.MouseButton.LeftButton:
            if self.right <= int(self.width * self.zoom_factor) and self.bottom <= \
                    int(self.height * self.zoom_factor) and self.left >= 0 and self.top >= 0:
                globalPos = event.globalPosition()
                globalPos = globalPos.toPoint()
                diff = globalPos - self.mouseMovePos
                self.move(diff)  # move window
                self.mouseMovePos = globalPos - self.pos()

            self.left, self.top = self.pos().x(), self.pos().y()
            self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top

    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            if event.button() == Qt.MouseButton.LeftButton:
                self.mousePressPos = None

        if self.left < 0:
            self.left = 0
            self.move(0, self.top)
        if self.right > int(self.width * self.zoom_factor):
            self.left = int(self.width * self.zoom_factor) - self._band.width()
            self.move(self.left, self.top)
        if self.bottom > int(self.height * self.zoom_factor):
            self.top = int(self.height * self.zoom_factor) - self._band.height()
            self.move(self.left, self.top)
        if self.top < 0:
            self.top = 0
            self.move(self.left, 0)


class editor(object):
    def setupUi(self, MainWindow, im):
        self.ui = setupEditorUI_new.setupEditor()
        self.ui.setupUi(MainWindow, im)

        self.previousBrightnessValue = 0
        self.previousContrastValue = 0
        self.previousVibranceValue = 0
        self.previousSharpnessValue = 0
        self.zoom_factor = 1
        self.scene = QGraphicsScene()

        self.image = Image.open(im)
        self.originalImage = self.image
        self.pixmap = QPixmap(im)

        # Histogram
        hist = self.image.histogram()

        self.plt1 = pg.PlotCurveItem(hist[0:256], antialias = True)
        self.plt2 = pg.PlotCurveItem(hist[256:512], antialias = True)
        self.plt3 = pg.PlotCurveItem(hist[512:768], antialias = True)

        self.ui.plot.setLimits(xMin = 0, yMin = 0,
                            xMax = 256, yMax = max(hist))
        self.plotCurves()

        self.ui.plot.addItem(self.plt1)
        self.ui.plot.addItem(self.plt2)
        self.ui.plot.addItem(self.plt3)

        self.ui.shadowsSlider.setEnabled(False)
        self.threadpool = QThreadPool()
        worker = Worker(self.calculateLUT, self.image)
        self.threadpool.start(worker)

        # Display
        self.scene_img = self.scene.addPixmap(self.pixmap)
        self.ui.gv.setScene(self.scene)
        self.ui.gv.ensureVisible(self.scene_img)
        self.ui.gv.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.gv.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.gv.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        QtCore.QTimer.singleShot(0, self.handle_timeout)
        self.contrastUpdated = True
        self.brightnessUpdated = True

        self.side_Menu_Pos = 1
        self.updateCounter = 1

        """
        Operation Codes:
            1 : Brightness
            2 : Contrast
            3 : Vibrance
            4 : Sharpness
        """

        self.cachedResults = {1: None, 2: None, 3: None, 4: None}

        self.image = self.image.convert('HSV')
        self.lut_main = np.asarray(self.image, dtype = float)
        self.lut1 = self.lut_main.copy()
        self.lut2 = self.lut_main.copy()

        self.ui.toggleMenuButton.clicked.connect(lambda: self.side_Menu_Def_0())
        self.ui.brightnessSlider.valueChanged.connect(lambda: self.brightnessChanged())
        #self.ui.brightnessSlider.sliderReleased.connect(lambda: self.updateImg(1))
        self.ui.contrastSlider.valueChanged.connect(lambda: self.contrastChanged())
        #self.ui.contrastSlider.sliderReleased.connect(lambda: self.updateImg(2))
        self.ui.vibranceSlider.valueChanged.connect(lambda: self.vibranceChanged())
        #self.ui.vibranceSlider.sliderReleased.connect(lambda: self.updateImg(3))
        self.ui.sharpnessSlider.valueChanged.connect(lambda: self.sharpnessChanged())
        #self.ui.sharpnessSlider.sliderReleased.connect(lambda: self.updateImg(4))
        self.ui.shadowsSlider.valueChanged.connect(lambda: self.shadowsChanged())
        self.ui.shadowsSlider.sliderReleased.connect(lambda: self.updateImg(5))
        self.ui.cropButton.clicked.connect(lambda: self.cropping())


    def side_Menu_Def_0(self):
        if self.side_Menu_Pos == 0:
            self.animation1 = QtCore.QPropertyAnimation(self.ui.slidingMenuFrame, b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(40)
            self.animation1.setEndValue(280)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
            self.animation1.start()

            self.animation2 = QtCore.QPropertyAnimation(self.ui.slidingMenuFrame, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(40)
            self.animation2.setEndValue(280)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
            self.animation2.start()
            self.side_Menu_Pos = 1
            self.ui.showSlidingMenuButtons()

        else:
            self.animation1 = QtCore.QPropertyAnimation(self.ui.slidingMenuFrame, b"maximumWidth")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(280)
            self.animation1.setEndValue(40)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
            self.animation1.start()

            self.animation2 = QtCore.QPropertyAnimation(self.ui.slidingMenuFrame, b"minimumWidth")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(280)
            self.animation2.setEndValue(40)
            self.animation2.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
            self.animation2.start()
            self.side_Menu_Pos = 0
            self.ui.hideSlidingMenuButtons()

    def handle_timeout(self):
        self.ui.gv.fitInView(self.scene_img, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.gv.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def get_zoom_factor(self):
        return (self.zoom_factor)

    def brightnessChanged(self):
        self.currentBrightnessValue = self.ui.brightnessSlider.value()/10        #self.currentContrastValue = self.ui.contrastSlider.value()/1000

        self.lut1[..., 2] = self.lut_main[..., 2].copy()
        self.lut1[..., 2] = np.clip(self.lut1[..., 2] + self.currentBrightnessValue, 0, 255)

        self.pil2pixmap()
        self.ui.brightnessInputBox.setValue(self.ui.brightnessSlider.value()/10)

    def contrastChanged(self):
        self.currentContrastValue = self.ui.contrastSlider.value()/20      #contrast_enhancer = ImageEnhance.Contrast(self.image)

        self.lut2[..., 2] = self.lut_main[..., 2].copy()
        self.lut2[..., 2] = np.clip(128 + self.currentContrastValue * self.lut1[...,2] - self.currentContrastValue * 128, 0, 255)

        self.pil2pixmap()
        self.ui.contrastInputBox.setValue(self.ui.contrastSlider.value())

    def vibranceChanged(self):
        #self.Vibrance_value = self.ui.vibranceSlider.value()/1000
        #vibrance_enhancer = ImageEnhance.Color(self.image)
        #image_copy = vibrance_enhancer.enhance(self.Vibrance_value)
        #self.pil2pixmap(image_copy)
        self.updateImg()
        self.ui.vibranceInputBox.setValue(self.ui.vibranceSlider.value()/1000)

    def sharpnessChanged(self):
        #self.Sharpness_value = self.ui.sharpnessSlider.value()/1000
        #sharpness_enhancer = ImageEnhance.Sharpness(self.image)
        #image_copy = sharpness_enhancer.enhance(self.Sharpness_value)
        #self.pil2pixmap(image_copy)
        self.updateImg()
        self.ui.sharpnessInputBox.setValue(self.ui.sharpnessSlider.value()/1000)

    def shadowsChanged(self):
        self.Shadow_value = self.ui.shadowsSlider.value()
        self.transpose[self.mean_arr < self.threshold/2] -= int(self.Shadow_value)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+1)] -= int(self.Shadow_value/7)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+3)] -= int(self.Shadow_value/7)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+5)] -= int(self.Shadow_value/8)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+7)] -= int(self.Shadow_value/9)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+9)] -= int(self.Shadow_value/9)
        self.lut[..., 2] = self.transpose

        image_copy = Image.fromarray(self.lut.astype('uint8'), mode = 'HSV')

        self.threadpool = QThreadPool()
        worker = Worker(self.calculateLUT, self.image)
        self.threadpool.start(worker)

        image_copy = image_copy.convert('RGB')
        self.pil2pixmap(image_copy)
        self.ui.shadowsInputBox.setValue(self.ui.shadowsSlider.value())

    def cropping(self):
        self.ui.gv.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.rb = resizableRubberBand(self, self.image) 

        self.rb.setGeometry(self.ui.gv.geometry())
        self.ui.cropConfirmButton.show()
        self.ui.cropCancelButton.show()
        self.ui.cropButton.setEnabled(False)

        self.ui.cropConfirmButton.clicked.connect(lambda: self.cropConfirm())
        self.ui.cropCancelButton.clicked.connect(lambda: self.cropCancel())

    def cropConfirm(self):
        self.viewingScale = self.image.width / self.ui.gv.viewport().rect().size().width()
        self.rb.update_dim()

        image_copy = self.image.crop((self.rb.left * self.viewingScale, self.rb.top * self.viewingScale,
                                      self.rb.right * self.viewingScale, self.rb.bottom * self.viewingScale))

        self.image = image_copy
        image_copy = image_copy.reduce(4)
        self.pil2pixmap(image_copy)
        self.rb.close()
        self.ui.cropConfirmButton.hide()
        self.ui.cropCancelButton.hide()

        self.ui.cropButton.setEnabled(True)

    def pil2pixmap(self):
        if (self.updateCounter == 7):
            avg = (self.lut1 + self.lut2)/2
            im = Image.fromarray(avg.astype('uint8'), mode = 'HSV')
            im = im.convert('RGB')
            if im.mode == "RGB":
                r, g, b = im.split()
                im = Image.merge("RGB", (b, g, r))
            elif im.mode == "RGBA":
                r, g, b, a = im.split()
                im = Image.merge("RGBA", (b, g, r, a))
            elif im.mode == "L":
                im = im.convert("RGBA")
            im2 = im.convert("RGBA")
            data = im2.tobytes("raw", "RGBA")
            qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format.Format_ARGB32)
            self.pixmap = QtGui.QPixmap.fromImage(qim)
            self.scene.removeItem(self.scene_img)
            self.scene_img = self.scene.addPixmap(self.pixmap)
            self.ui.gv.ensureVisible(self.scene_img)
            #QtCore.QTimer.singleShot(0, self.handle_timeout)
        else:
            self.updateCounter += 1

        """

        image_new = Image.fromarray(self.lut1.astype('uint8'), mode = 'HSV')
        image_new = image_new.convert('RGB')
        qim = ImageQt(image_new)
        self.pixmap = QtGui.QPixmap.fromImage(qim)
        self.scene.removeItem(self.scene_img)
        self.scene_img = self.scene.addPixmap(self.pixmap)
        self.ui.gv.ensureVisible(self.scene_img)
        """
    # Put a seperate thread for displaying the image!
    """
    def updateImg(self):
        brightness_enhancer = ImageEnhance.Brightness(self.image)
        image_copy = brightness_enhancer.enhance(self.Brightness_value)
        contrast_enhancer = ImageEnhance.Contrast(image_copy)
        image_copy = contrast_enhancer.enhance(self.Contrast_value)
        vibrance_enhancer = ImageEnhance.Color(image_copy)
        image_copy = vibrance_enhancer.enhance(self.Vibrance_value)
        sharpness_enhancer = ImageEnhance.Sharpness(image_copy)
        image_copy = sharpness_enhancer.enhance(self.Sharpness_value)
        self.threadpool = QThreadPool()
        worker = Worker(self.calculateLUT, image_copy)
        self.threadpool.start(worker)
        nnect eactime.sleep(0.5)
        self.Shadow_value = self.ui.shadowsSlider.value()
        self.transpose[self.mean_arr < self.threshold/2] -= int(self.Shadow_value)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+1)] -= int(self.Shadow_value/7)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+3)] -= int(self.Shadow_value/7)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+5)] -= int(self.Shadow_value/8)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+7)] -= int(self.Shadow_value/9)
        self.transpose[np.logical_and(self.threshold/2 < self.mean_arr, self.mean_arr < (self.threshold/2)+9)] -= int(self.Shadow_value/9)
        self.lut[..., 2] = self.transpose

        image_copy = Image.fromarray(self.lut.astype('uint8'), mode = 'HSV')

        image_copy = image_copy.convert('RGB')

        self.pil2pixmap(image_copy)
        self.updateHistogram(image_copy)
    """
    def updateImg(self):
        self.currentBrightnessValue = self.ui.brightnessSlider.value()/1000
        self.currentContrastValue = self.ui.contrastSlider.value()/1000
        self.currentVibranceValue = self.ui.vibranceSlider.value()/1000
        self.currentSharpnessValue = self.ui.sharpnessSlider.value()/1000

        image_copy = self.image
        if(self.currentBrightnessValue != self.previousBrightnessValue):
            brightness_enhancer = ImageEnhance.Brightness(image_copy)
            image_copy = brightness_enhancer.enhance(self.currentBrightnessValue)
        if(self.currentContrastValue != self.previousContrastValue):
            contrast_enhancer = ImageEnhance.Contrast(image_copy)
            image_copy = contrast_enhancer.enhance(self.currentContrastValue)
        if(self.currentVibranceValue != self.previousVibranceValue):
            vibrance_enhancer = ImageEnhance.Color(image_copy)
            image_copy = vibrance_enhancer.enhance(self.currentVibranceValue)
        if(self.currentSharpnessValue != self.previousSharpnessValue):
            sharpness_enhancer = ImageEnhance.Sharpness(image_copy)
            image_copy = sharpness_enhancer.enhance(self.currentSharpnessValue)
        self.pil2pixmap(image_copy)


    def updateHistogram(self, im):
        hist = im.histogram()
        self.ui.plot.removeItem(self.plt1)
        self.ui.plot.removeItem(self.plt2)
        self.ui.plot.removeItem(self.plt3)

        self.plt1 = pg.PlotCurveItem(hist[0:256], antialias = True)
        self.plt2 = pg.PlotCurveItem(hist[256:512], antialias = True)
        self.plt3 = pg.PlotCurveItem(hist[512:768], antialias = True)

        self.ui.plot.setLimits(xMin = 0, yMin = 0,
                            xMax = 256, yMax = max(hist))

        self.plotCurves()

        self.ui.plot.addItem(self.plt1)
        self.ui.plot.addItem(self.plt2)
        self.ui.plot.addItem(self.plt3)

    def plotCurves(self):
        self.plt1.setBrush("#9d3530")
        self.plt1.setFillLevel(0)
        self.plt1.setPen(None)
        self.plt1.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Plus)
        self.plt2.setBrush("#349c33")
        self.plt2.setFillLevel(0)
        self.plt2.setPen(None)
        self.plt2.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Plus)
        self.plt3.setBrush("#2d2d9b")
        self.plt3.setFillLevel(0)
        self.plt3.setPen(None)
        self.plt3.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Plus)

    def np_fftconvolve(self, A, B):
        return np.real(ifft2(fft2(A)*fft2(B, s=A.shape)))

    def mean_values_cpu(self):
        kernel = np.ones((25,25))
        kernel[1,1] =0

        nsum = self.np_fftconvolve(self.transpose, kernel)
        nnei = self.np_fftconvolve(np.ones(self.transpose.shape), kernel)

        self.mean_arr = nsum/nnei

    def mean_values_gpu(self):
        kernel = np.ones((35,35))
        kernel[1,1] =0

        nsum = cp.asnumpy(cusignal.convolve2d(self.transpose, kernel, mode='same'))
        nnei = cp.asnumpy(cusignal.convolve2d(np.ones(self.transpose.shape), kernel, mode='same'))

        self.mean_arr = nsum/nnei

    def calculateLUT(self, image):
        image = image.convert('HSV')

        self.lut = np.asarray(image, dtype = int)
        self.transpose = self.lut[..., 2]
        self.threshold = np.max(self.transpose)

        try:
            subprocess.check_output('nvidia-smi')
            self.mean_values_gpu()
        except Exception:
            self.mean_values_cpu()

        self.ui.shadowsSlider.setEnabled(True)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)
