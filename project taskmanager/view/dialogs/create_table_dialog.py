from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class CreateTableDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create New Table")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Table name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        self.ok_button = QPushButton("Create")
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
