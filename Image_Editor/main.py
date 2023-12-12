import setupViewer
import sys
from PyQt6 import QtWidgets

app =QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = setupViewer.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())
