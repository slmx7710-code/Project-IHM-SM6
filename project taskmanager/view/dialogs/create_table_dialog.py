from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class TableDialog(QDialog):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        file = QFile("ui/table_dialog.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()