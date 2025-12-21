class Schema:
    def __init__(self):
        self.tables = []
        self.relationships = []

    def add_table(self, table):
        self.tables.append(table)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)
      
        if relationship.rel_type == "1-N":
            if not hasattr(relationship.table2, "foreign_keys"):
                relationship.table2.foreign_keys = []
            fk_column = f"{relationship.table1.name.lower()}_id"
            relationship.table2.foreign_keys.append({
                "column": fk_column,
                "ref_table": relationship.table1.name,
                "ref_column": "id"
            })
