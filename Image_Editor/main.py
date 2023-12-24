import setupViewer
import sys
from PyQt6 import QtWidgets

app =QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()
rect = screen.availableGeometry()
MainWindow = QtWidgets.QMainWindow()
MainWindow.resize(rect.width(), rect.height())
ui = setupViewer.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())
