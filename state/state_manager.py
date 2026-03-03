class StateManager:
    def __init__(self):
        self._state = {}

    def set(self, key, value):
        self._state[key] = value

    def get(self, key):
        return self._state.get(key, None)

    def get_all(self):
        return self._state