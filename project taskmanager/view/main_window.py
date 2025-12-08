from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget, QVBoxLayout
from view.canvas_view import CanvasView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Schema Designer (Week 1)")

        # Menu Bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # File menu
        file_menu = QMenu("Tables", self)
        menu_bar.addMenu(file_menu)

        # Actions
        self.create_table_action = file_menu.addAction("Create Table")

        # Canvas 
        self.canvas = CanvasView()
        self.setCentralWidget(self.canvas)
