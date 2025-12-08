class SchemaModel:
    def __init__(self):
        # List of all tables in the project
        self.tables = []

    def add_table(self, table):
        self.tables.append(table)

    def remove_table(self, table):
        if table in self.tables:
            self.tables.remove(table)
