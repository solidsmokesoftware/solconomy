

class System:
    def __init__(self, system):
        self.system = system
        self.items = {}

    def set(self, index, value):
        self.items[index] = value

    def add(self, index, value):
        self.items[index] = value

    def has(self, index):
        return index in self.items

    def hasget(self, index):
        if self.has(index):
            return self.items[index]
        else:
            return False

    def get(self, index):
        return self.items[index]

    def remove(self, index):
        del self.items[index]


class Process(System):
    def __init__(self, system):
        System.__init__(self, system)

    def start(self):
        return

    def run(self):
        return