from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PIL import Image, ImageEnhance
from numpy import asarray
import setupEditorUi


class resizableRubberBand(QWidget):
    def __init__(self, MainWindow, im):
        super(resizableRubberBand, self).__init__(MainWindow.gv)
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
        self.MainWidget = QtWidgets.QWidget(MainWindow)
        self.MainWidget.setObjectName("mainwidget")
        MainWindow.setCentralWidget(self.MainWidget)

        self.ui = setupEditorUi.setupEditor()
        self.ui.setupUi(MainWindow, self.MainWidget, im)

        self.Brightness_value = 1
        self.Contrast_value = 1
        self.Vibrance_value = 1
        self.Sharpness_value = 1
        self.zoom_factor = 1
        self.gv = QGraphicsView(MainWindow)
        self.scene = QGraphicsScene()
        self.gv.setGeometry(QtCore.QRect(0, 20, 1600, 1000))

        self.image = Image.open(im)
        self.originalImage = self.image
        self.pixmap = QPixmap(im)

        self.scene_img = self.scene.addPixmap(self.pixmap)
        self.gv.setScene(self.scene)
        self.gv.show()
        self.fitInView()

        self.ui.Brightness_scroll.valueChanged.connect(lambda: self.brightnessChanged())
        self.ui.Brightness_scroll.sliderReleased.connect(lambda: self.updateImg())
        self.ui.Contrast_scroll.valueChanged.connect(lambda: self.contrastChanged())
        self.ui.Contrast_scroll.sliderReleased.connect(lambda: self.updateImg())
        self.ui.Vibrance_scroll.valueChanged.connect(lambda: self.vibranceChanged())
        self.ui.Vibrance_scroll.sliderReleased.connect(lambda: self.updateImg())
        self.ui.Sharpness_scroll.valueChanged.connect(lambda: self.sharpnessChanged())
        self.ui.Sharpness_scroll.sliderReleased.connect(lambda: self.updateImg())
        self.ui.cropButton.clicked.connect(lambda: self.cropping(MainWindow))

    def get_zoom_factor(self):
        return(self.zoom_factor)

    def brightnessChanged(self):
        self.Brightness_value = self.ui.Brightness_scroll.value()/1000
        brightness_enhancer = ImageEnhance.Brightness(self.image)
        image_copy = brightness_enhancer.enhance(self.Brightness_value)
        self.pil2pixmap(image_copy)
        self.ui.Brightness_input_box.setValue(self.ui.Brightness_scroll.value()/1000)

    def contrastChanged(self):
        self.Contrast_value = self.ui.Contrast_scroll.value()/1000
        contrast_enhancer = ImageEnhance.Contrast(self.image)
        image_copy = contrast_enhancer.enhance(self.Contrast_value)
        self.pil2pixmap(image_copy)
        self.ui.Contrast_input_box.setValue(self.ui.Contrast_scroll.value()/1000)

    def vibranceChanged(self):
        self.Vibrance_value = self.ui.Vibrance_scroll.value()/1000
        vibrance_enhancer = ImageEnhance.Color(self.image)
        image_copy = vibrance_enhancer.enhance(self.Vibrance_value)
        self.pil2pixmap(image_copy)
        self.ui.Vibrance_input_box.setValue(self.ui.Vibrance_scroll.value()/1000)

    def sharpnessChanged(self):
        self.Sharpness_value = self.ui.Sharpness_scroll.value()/1000
        sharpness_enhancer = ImageEnhance.Sharpness(self.image)
        image_copy = sharpness_enhancer.enhance(self.Sharpness_value)
        self.pil2pixmap(image_copy)
        self.ui.Sharpness_input_box.setValue(self.ui.Sharpness_scroll.value()/1000)

    def cropping(self, MainWindow):
        self.rb = resizableRubberBand(self, self.image)
        self.rb.setGeometry(0, 0, 1600, 1010)

        self.cropWidget = QWidget(self.ui.edit_panel)
        self.cropWidget.setGeometry(QtCore.QRect(30, 645, 160, 40))

        confirmButton = QPushButton("Confirm", self.cropWidget)
        confirmButton.setGeometry(QtCore.QRect(37, 5, 93, 15))
        cancelButton = QPushButton("Cancel", self.cropWidget)
        cancelButton.setGeometry(QtCore.QRect(37, 20, 93, 15))

        confirmButton.clicked.connect(lambda: self.cropConfirm())
        cancelButton.clicked.connect(lambda: self.cropCancel())

        self.cropWidget.show()
        self.ui.cropButton.hide()
        confirmButton.show()
        cancelButton.show()

    def cropConfirm(self):
        self.rb.update_dim()

        image_copy = self.image.crop((self.rb.left/ self.zoom_factor, self.rb.top / self.zoom_factor,
                                      self.rb.right / self.zoom_factor,self.rb.bottom / self.zoom_factor))
        self.image = image_copy
        image_copy = image_copy.reduce(4)
        self.pil2pixmap(image_copy)
        self.rb.close()
        for i in (self.cropWidget.findChildren(QtWidgets.QWidget)):
            i.deleteLater()

        self.updateImg()

        self.ui.cropButton.show()

    def pil2pixmap(self, im):
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
        pixmap = QtGui.QPixmap.fromImage(qim)
        self.scene.removeItem(self.scene_img)
        self.scene_img= self.scene.addPixmap(pixmap)
        self.fitInView()

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

    def updateImg(self):
        brightness_enhancer = ImageEnhance.Brightness(self.image)
        image_copy = brightness_enhancer.enhance(self.Brightness_value)
        contrast_enhancer = ImageEnhance.Contrast(image_copy)
        image_copy = contrast_enhancer.enhance(self.Contrast_value)
        vibrance_enhancer = ImageEnhance.Color(image_copy)
        image_copy = vibrance_enhancer.enhance(self.Vibrance_value)
        sharpness_enhancer = ImageEnhance.Sharpness(image_copy)
        image_copy = sharpness_enhancer.enhance(self.Sharpness_value)
        self.pil2pixmap(image_copy)
        self.ui.updateHistogram(image_copy)
