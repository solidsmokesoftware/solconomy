


class State:
    def __init__(self, name, transitions):
        self.name = name
        self.transitions = transitions

class Statemachine:
    def __init__(self, state):
        self.state = state
        self.states = {state.name:state}

    def add(self, state):
        self.states[state.name] = state

    def remove(self, state):
        del self.states[state.name]

    def transition(self, state):
        results = False
        if state in self.state.transitions:
            self.state = state
            results = True
        return results