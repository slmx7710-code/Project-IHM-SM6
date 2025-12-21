from PySide6.QtWidgets import QMainWindow
from ui.main_window_ui import Ui_MainWindow 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Database Schema Designer")
        self.setMinimumSize(1300, 700)