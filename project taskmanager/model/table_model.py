class Attribute:
    def __init__(self, name, data_type="TEXT", primary_key=False):
        self.name = name
        self.data_type = data_type
        self.primary_key = primary_key

class Table:
    def __init__(self, name):
        self.name = name
        self.attributes = []

    def add_attribute(self, attr):
        self.attributes.append(attr)

    def generate_create_sql(self):
        sql = f"CREATE TABLE {self.name} (\n"
        col_defs = []
        for attr in self.attributes:
            col_def = f"  {attr.name} {attr.data_type}"
            if attr.primary_key:
                col_def += " PRIMARY KEY"
            col_defs.append(col_def)
        sql += ",\n".join(col_defs)
        if hasattr(self, "foreign_keys"):
            for fk in self.foreign_keys:
                sql += f",\n  FOREIGN KEY ({fk['column']}) REFERENCES {fk['ref_table']}({fk['ref_column']})"
        sql += "\n);"
        return sql
