class Attribute:
    def __init__(self, name, data_type, primary_key=False):
        self.name = name
        self.data_type = data_type
        self.primary_key = primary_key