from threading import Lock


class SharedList:
    def __init__(self):
        self.lock = Lock()
        self.items = {}

    def give(self, message, address):
        if not self.has(address):
            self.items[address] = []
        self.items[address].append(message)

    def has(self, address):
        results = False
        if address in self.items:
            if len(self.items[address]) > 0:
                results = True
        return results

    def get(self, address):
        self.lock.acquire()
        if address in self.items:
            items = self.items[address]
        else:
            items = []
        self.items[address] = []
        self.lock.release()
        return items
