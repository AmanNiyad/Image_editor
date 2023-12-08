from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PIL import Image, ImageEnhance
import setupEditorUi

class editor(object):
    def setupUi(self, MainWindow, im):
        self.ui = setupEditorUi.setupEditor()
        self.ui.setupUi(MainWindow)

        self.Brightness_value = 1
        self.Contrast_value = 1
        self.Vibrance_value = 1
        self.Sharpness_value = 1

        self.image = Image.open(im)
        self.pixmap = QPixmap(im)
        self.ui.label.setPixmap(self.pixmap.scaled(self.ui.label.width(), self.ui.label.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        self.ui.Brightness_scroll.valueChanged.connect(lambda: self.brightnessChanged())
        self.ui.Contrast_scroll.valueChanged.connect(lambda: self.contrastChanged())
        self.ui.Vibrance_scroll.valueChanged.connect(lambda: self.vibranceChanged())
        self.ui.Sharpness_scroll.valueChanged.connect(lambda: self.sharpnessChanged())

    def brightnessChanged(self):
        self.Brightness_value = self.ui.Brightness_scroll.value()/1000
        self.updateImg()
        self.ui.Brightness_input_box.setValue(self.ui.Brightness_scroll.value()/1000)

    def contrastChanged(self):
        self.Contrast_value = self.ui.Contrast_scroll.value()/1000
        self.updateImg()
        self.ui.Contrast_input_box.setValue(self.ui.Contrast_scroll.value()/1000)

    def vibranceChanged(self):
        self.Vibrance_value = self.ui.Vibrance_scroll.value()/1000
        self.updateImg()
        self.ui.Vibrance_input_box.setValue(self.ui.Vibrance_scroll.value()/1000)

    def sharpnessChanged(self):
        self.Sharpness_value = self.ui.Sharpness_scroll.value()/1000
        self.updateImg()
        self.ui.Sharpness_input_box.setValue(self.ui.Sharpness_scroll.value()/1000)

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
        self.ui.label.setPixmap(pixmap.scaled(self.ui.label.width(), self.ui.label.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

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
