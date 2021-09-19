from tinylisp import exceptions
from tinylisp.environ import Environ
from tinylisp.result import Result


class Node:
    def __init__(self, *args, **kwargs):
        self.children = []
        self.init_node(*args, **kwargs)

    def init_node(self, *args, **kwargs):
        pass

    def add_child(self, node):
        self.children.append(node)

    def evaluate(self, environ):
        raise NotImplementedError(str(self))


class Root(Node):
    def result(self):
        try:
            return Result(value=self.evaluate(Environ()))
        except exceptions.TinyLispError as e:
            return Result(error=e.message)

    def evaluate(self, environ):
        result_val = 0
        for child in self.children:
            result_val = child.evaluate(environ)
        return result_val


class ParseErrorRoot(Root):
    def __init__(self, line, row, *args, **kwargs):
        self.line = line
        self.row = row
        super().__init__(*args, **kwargs)

    def evaluate(self, environ):
        raise exceptions.ParseError(
            'Parser error: line {line}; row {row}'.format(
                line=self.line, row=self.row
            )
        )


class Block(Node):
    def evaluate(self, environ):
        assert len(self.children) > 0
        statement_symbol, param_nodes = self.children[0], self.children[1:]
        assert isinstance(statement_symbol, Symbol)

        statement = environ.lookup(statement_symbol.name)
        params = statement.process_params(environ, param_nodes)
        return statement.calc(environ, params)


class Number(Node):
    def init_node(self, value):
        self.value = value

    def evaluate(self, environ):
        return self.value


class Symbol(Node):
    def init_node(self, name):
        self.name = name

    def evaluate(self, environ):
        return environ.lookup(self.name).calc(environ, [])
