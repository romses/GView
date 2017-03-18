from gui.mainwindow_ui import Ui_FitView
from PyQt5.QtWidgets import QApplication, QMainWindow 
from gui.editwindow_ui import Ui_EditWindow

class EditWindow(QMainWindow, Ui_EditWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_EditWindow.__init__(self)
    