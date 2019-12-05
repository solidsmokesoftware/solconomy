class Collection:
    def __init__(self):
        self.values = {}

    def __getitem__(self, item):
        return self.values[item]

    def set(self, index, value):
        self.values[index] = value

    def add(self, index, value):
        self.values[index] = value

    def has(self, index):
        return index in self.values

    def get(self, index):
        if self.has(index):
            return self.values[index]
        else:
            return False

    def fget(self, index):
        return self.values[index]

    def remove(self, index):
        del self.values[index]

