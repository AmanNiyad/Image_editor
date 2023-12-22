from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
import setupMenubar


class setupViewer():
    def setupUi(self, MainWindow, MainWidget):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("""
                    background-color: #333333;
                    color: #FFFFFF;
                    """)

        self.centralwidget = QtWidgets.QWidget(MainWidget)
        self.centralwidget.setObjectName("centralwidget")

        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(310, 975, 100, 45))
        self.button1.setObjectName("button1")

        self.button2 = QtWidgets.QPushButton(self.centralwidget)
        self.button2.setGeometry(QtCore.QRect(1510, 975, 100, 45))
        self.button2.setObjectName("button2")

        self.button3 = QtWidgets.QPushButton(self.centralwidget)
        self.button3.setGeometry(QtCore.QRect(900, 975, 100, 45))
        self.button3.setObjectName("button3")

        self.menu = setupMenubar.Menubar()

        self.menu.setupBar(MainWindow)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setVisible(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button1.setText(_translate("MainWindow", "Previous"))
        self.button1.setStatusTip(_translate("MainWindow", "Previous Image"))
        self.button2.setText(_translate("MainWindow", "Next"))
        self.button2.setStatusTip(_translate("MainWindow", "Next Image"))
        self.button3.setText(_translate("MainWindow", "Edit"))
