from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class CanvasView(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

    def paintEvent(self, event):
       
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.grey)
