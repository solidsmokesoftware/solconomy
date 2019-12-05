import glooey
import pyglet


class Manager:
    def __init__(self, game):
        self.game = game
        self.scenes = {}

    def load(self, scene):
        scene = scene(self)
        print('Loading %s' % scene.key)
        return scene

    def add(self, scene):
        print('Adding %s' % scene.key)
        self.scenes[scene.key] = scene
        self.game.gui.add(scene.items)

    def remove(self, scene):
        print('Removing %s' % scene.key)
        self.game.gui.remove(scene.items)
        del self.scenes[scene.key]


class Scene:
    def __init__(self, manager, key):
        self.key = key
        self.manager = manager
        self.items = None


class World(Scene):
    def __init__(self, manager):
        Scene.__init__(self, manager, 'World')
        #pyglet.clock.schedule_interval(self.send_input, 1/15.0)

        self.items = glooey.VBox()
        label = Label('World map')

        self.items.add(label)

        sublabel = Sublabel('')

    def send_input(self, delta):
        print('sending input')


class MainMenu(Scene):
    def __init__(self, manager):
        Scene.__init__(self, manager, 'MainMenu')

        self.items = glooey.VBox()
        self.items.alignment = 'center'

        label = Label('Solconomy')
        sublabel = Sublabel('A game')

        nameBox = glooey.HBox()
        nameLabel = Sublabel('Username:')
        self.nameForm = Form('Revvy')
        #self.addForm.push_handlers(on_unfocus=self.get_text)
        nameBox.add(nameLabel)
        nameBox.add(self.nameForm)

        passBox = glooey.HBox()
        passLabel = Sublabel('Password:')
        self.passForm = Form('none')
        #self.addForm.push_handlers(on_unfocus=self.get_text)
        passBox.add(passLabel)
        passBox.add(self.passForm)

        addBox = glooey.HBox()
        addLabel = Sublabel('Address:')
        self.addForm = Form('127.0.0.1')
        #self.addForm.push_handlers(on_unfocus=self.get_text)
        addBox.add(addLabel)
        addBox.add(self.addForm)

        portBox = glooey.HBox()
        portLabel = Sublabel('Port:')
        self.portForm = Form('45456')
        #self.portForm.push_handlers(on_unfocus=self.get_text)
        portBox.add(portLabel)
        portBox.add(self.portForm)

        button = Button('Join', 'Joined')
        button.push_handlers(on_click=self.join)

        self.items.add(label)
        self.items.add(sublabel)
        self.items.add(nameBox)
        self.items.add(passBox)
        self.items.add(addBox)
        self.items.add(portBox)
        self.items.add(button)

    def join(self, widget):
        address = self.addForm.text
        port = int(self.portForm.text)
        username = self.nameForm.text
        password = self.passForm.text

        print('Main Menu: Attempting to join %s:%s' % (address, port))
        game = self.manager.game
        game.set_host(username, password, address, port)

        print('Main Menu: Starting server')
        game.start_connection()

        world = self.manager.load(World)
        self.manager.add(world)
        self.manager.remove(self)
        print('Main Menu: Join Function Complete')






class Label(glooey.Label):
    custom_color = '#bcbcaa'
    custom_font_size = 26


class Sublabel(glooey.Label):
    custom_color = '#454566'
    custom_font_size = 16


class Button(glooey.Button):
    foreground = Label
    custom_alignment = 'fill'

    class Base(glooey.Background):
        custom_color = '#121233'

    class Over(glooey.Background):
        custom_color = '#787899'

    class Down(glooey.Background):
        custom_color = '#141477'

    def __init__(self, text, response):
        glooey.Button.__init__(self, text)
        self.response = response

    def on_click(self, widget):
        print(self.response)


class Form(glooey.Form):
    custom_alignment = 'center'
    custom_width_hint = 200

    class Label(glooey.EditableLabel):
        custom_font_size = 16
        custom_color = '#454566'

    class Base(glooey.Background):
        custom_color = '#898977'