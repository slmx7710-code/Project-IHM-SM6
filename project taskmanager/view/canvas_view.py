from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtGui import QBrush, QPen, QColor, QPainter
from PySide6.QtCore import Qt

class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor(240, 240, 240)))
        
    def clear_canvas(self):
        """Clear Canvas"""
        self.scene.clear()