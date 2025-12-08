from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow
from controller.main_controller import MainController
from model.schema_model import SchemaModel

import sys

def main():
    app = QApplication(sys.argv)

    # MODEL 
    schema_model = SchemaModel()

    # VIEW
    window = MainWindow()

    # CONTROLLER
    controller = MainController(schema_model, window)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
