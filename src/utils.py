class Autoincrementer:
    def __init__(self):
        self.id = 0

    def get_id(self):
        current_id = self.id
        self.id += 1
        return current_id