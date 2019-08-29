

class Data:
    def __init__(self):
        self.values = {}

    def add(self, item, value):
        self.values[item] = value

    def set(self, item, value):
        self.values[item] = value

    def remove(self, item):
        del self.values[item]

    def has(self, item):
        return item in self.values

    def get(self, item):
        return self.values[item]

    def hasget(self, item):
        if self.has(item):
            return self.get(item)
        else:
            return False