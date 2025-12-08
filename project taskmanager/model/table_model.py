class TableModel:
    def __init__(self, name):
        self.name = name
        self.attributes = []  # list of Attribute objects

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def remove_attribute(self, attribute):
        if attribute in self.attributes:
            self.attributes.remove(attribute)