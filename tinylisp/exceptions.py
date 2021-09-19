class TinyLispError(Exception):
    def __init__(self, message='Unknown'):
        self.message = message


class ParseError(TinyLispError):
    pass


class InterpreterError(TinyLispError):
    pass
