from view.dialogs.create_table_dialog import CreateTableDialog
from model.table_model import TableModel
from controller.table_controller import TableController

class MainController:
    def __init__(self, schema_model, main_window):
        self.model = schema_model
        self.view = main_window
        self.table_controller = TableController(self.model, self.view)
        self.view.create_table_action.triggered.connect(
            self.table_controller.create_table_dialog
        )
