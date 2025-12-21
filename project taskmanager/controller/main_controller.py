from controller.table_controller import TableController
from controller.sql_controller import SQLController
from model.schema_model import Schema
from view.main_window import MainWindow

class MainController:
    def __init__(self):
        self.schema = Schema()
        self.window = MainWindow()

        # Pass controller reference to window
        self.window.controller = self

        self.table_controller = TableController(self.schema, self.window)
        self.sql_controller = SQLController(self.window)

        self.window.show()