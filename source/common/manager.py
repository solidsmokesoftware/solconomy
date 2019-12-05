

class Manager:
    def __init__(self):

        self.items = {}

    def __getitem__(self, key):
        return self.items[key]

    def get(self, key):
        return self.items[key]

    def get_all(self):
        return self.items.values()

    def add(self, item, key=None):
        if key == None:
            key = len(self.items)

        self.items[key] = item

    def remove(self, key):
        del self.items[key]

    def update(self):
        for item in self.items:
            pass

