from source.system.system import System
from source.system.component import Component

class Entity(System):
    def __init__(self, system):
        System.__init__(self, system)
        self.component = self.system.component
        self.value = -1

    def add(self):
        self.value += 1
        self.items[self.value] = True
        return self.value

    def set(self, index):
        self.items[index] = True
        if index > self.value:
            self.value = index

    def add_actor(self, x, y, image=None, index=None):
        if index:
            self.set(index)
        else:
            index = self.add()

        pos = self.component.position(x, y)
        self.system.spatial.add(index, pos)

        if image:
            self.system.visual.add_actor(index, image)

        return index

    def add_chunk(self, x, y, index=None):
        if index:
            self.set(index)
        else:
            index = self.add()

        pos = self.component.position(x, y)
        self.system.spatial.add(index, pos)

        chunk = self.component.chunk()
        self.system.world.add(index, chunk)

        return index


    def add_tile(self, x, y, value, image=None, index=None):
        if index:
            self.set(index)
        else:
            index = self.add()

        pos = self.component.position(x, y)
        self.system.spatial.add(index, pos)

        data = self.component.data()
        data.add('value', value)
        self.system.value.add(index, data)

        if image:
            self.system.visual.add_tile(index, value)

        return index

    def add_block(self, x, y, value, image=None, index=None):
        if index:
            self.set(index)
        else:
            index = self.add()

        pos = self.component.position(x, y)
        self.system.spatial.add(index, pos)

        data = self.component.data()
        data.add('value', value)
        self.system.value.add(index, data)

        if image:
            self.system.visual.add_block(index, value)

        return index

    def add_item(self, x, y, value, image=None, index=None):
        if index:
            self.set(index)
        else:
            index = self.add()

        pos = self.component.position(x, y)
        self.system.spatial.add(index, pos)

        data = self.component.data()
        data.add('value', value)
        self.system.value.add(index, data)

        if image:
            self.system.visual.add_item(index, value)

        return index

    def add_menu(self, x, y, image, index=None):
        if index:
            self.set(index)
        else:
            index = self.add()

        pos = self.component.position(x, y)
        self.system.spatial.add(index, pos)
        self.system.visual.add_menu(index, image)

        return index