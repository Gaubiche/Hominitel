class Adapter:
    def print(self, text: str):
        raise NotImplementedError("_print method must be implemented")

    def pos(self, row: int, col: int):
        raise NotImplementedError("pos method must be implemented")

    def cls(self):
        raise NotImplementedError("cls method must be implemented")

    def inverse(self):
        raise NotImplementedError("inverse method must be implemented")

    def echo_off(self):
        raise NotImplementedError("echo_off method must be implemented")

    def get_input(self):
        raise NotImplementedError("read method must be implemented")

    def message(self, row: int, col: int, delay: int, message: str, bip: bool = False):
        raise NotImplementedError("message method must be implemented")