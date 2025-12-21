from PySide6.QtWidgets import (
    QWidget, QMainWindow, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QTextEdit, QTableWidget, QGraphicsView, QGraphicsScene
)
from PySide6.QtGui import QColor  # ✅ أضف هذا

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Database Schema Designer")
        MainWindow.resize(1300, 700)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.mainLayout = QHBoxLayout(self.centralwidget)

        # ===== LEFT PANEL =====
        self.leftPanel = QWidget()
        self.leftLayout = QVBoxLayout(self.leftPanel)

        self.tableNameInput = QLineEdit()
        self.tableNameInput.setPlaceholderText("Table name")
        self.leftLayout.addWidget(self.tableNameInput)

        self.addTableButton = QPushButton("Add Table")
        self.leftLayout.addWidget(self.addTableButton)

        self.deleteTableButton = QPushButton("Delete Table")
        self.leftLayout.addWidget(self.deleteTableButton)

        self.tableList = QListWidget()
        self.leftLayout.addWidget(self.tableList)

        self.editAttributeButton = QPushButton("Edit Attribute")
        self.leftLayout.addWidget(self.editAttributeButton)

        self.deleteAttributeButton = QPushButton("Delete Attribute")
        self.leftLayout.addWidget(self.deleteAttributeButton)

        self.addRelationshipButton = QPushButton("Add Relationship")
        self.leftLayout.addWidget(self.addRelationshipButton)

        self.deleteRelationshipButton = QPushButton("Delete Relationship")
        self.leftLayout.addWidget(self.deleteRelationshipButton)

        self.mainLayout.addWidget(self.leftPanel)

        # ===== CENTER =====
        self.schemaCanvas = QGraphicsView()
        self.schemaCanvas.setScene(QGraphicsScene())
        self.schemaCanvas.setBackgroundBrush(QColor(230, 240, 255))
        self.mainLayout.addWidget(self.schemaCanvas)

        # ===== RIGHT PANEL =====
        self.rightPanel = QWidget()
        self.rightLayout = QVBoxLayout(self.rightPanel)

        self.sqlOutput = QTextEdit()
        self.sqlOutput.setReadOnly(True)
        self.rightLayout.addWidget(QLabel("Generated SQL"))
        self.rightLayout.addWidget(self.sqlOutput)

        self.queryInput = QTextEdit()
        self.queryInput.setPlaceholderText("Write SQL query here...")
        self.rightLayout.addWidget(QLabel("Execute SQL"))
        self.rightLayout.addWidget(self.queryInput)

        self.executeQueryButton = QPushButton("Execute Query")
        self.rightLayout.addWidget(self.executeQueryButton)

        self.resultTable = QTableWidget()
        self.rightLayout.addWidget(self.resultTable)

        self.mainLayout.addWidget(self.rightPanel)