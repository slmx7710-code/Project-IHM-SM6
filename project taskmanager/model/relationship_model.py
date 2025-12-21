class Relationship:
    def __init__(self, table1, table2, rel_type="1-N"):
        self.table1 = table1
        self.table2 = table2
        self.rel_type = rel_type
