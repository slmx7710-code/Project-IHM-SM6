from view.dialogs.create_table_dialog import CreateTableDialog
from model.table_model import TableModel

class TableController:
    def __init__(self, schema_model, main_window):
        self.model = schema_model
        self.view = main_window

    def create_table_dialog(self):
        dialog = CreateTableDialog()

      
        dialog.ok_button.clicked.connect(lambda: self._create(dialog))
        dialog.exec()

    def _create(self, dialog):
        name = dialog.name_input.text().strip()

        if name == "":
            print("Table name cannot be empty.")
            return

        table = TableModel(name)
        self.model.add_table(table)

        print(f"Table created: {name}")
        dialog.accept()
