from tinylisp import validators as vld


class Statement:
    def calc(self, environ, params):
        raise NotImplementedError

    def params_validators(self):
        yield from ()

    def validate_params(self, environ, params):
        for validator in self.params_validators():
            validator(params)

    def process_params(self, environ, nodes):
        params = [node.evaluate(environ) for node in nodes]
        self.validate_params(environ, params)
        return params


class Const(Statement):
    def __init__(self, value):
        self.value = value

    def calc(self, environ, params):
        return self.value


class Plus(Statement):
    def params_validators(self):
        yield vld.all_numbers
        yield vld.at_least_one_param

    def calc(self, environ, params):
        # TODO: check if everyone is a number
        return sum(params)


class Minus(Statement):
    def calc(self, environ, params):
        # TODO: check if everyone is a number
        # TODO: check if at least two number
        return params[0] - sum(params[1:])


class ComparisonStatement(Statement):
    def calc(self, environ, params):
        assert len(params) == 2
        # TODO: check if everyone is a number
        return int(self.compare(params[0], params[1]))


class Less(ComparisonStatement):
    def compare(self, a, b):
        return a < b


class LessOrEqual(ComparisonStatement):
    def compare(self, a, b):
        return a <= b


class More(ComparisonStatement):
    def compare(self, a, b):
        return a > b


class MoreOrEqual(ComparisonStatement):
    def compare(self, a, b):
        return a >= b


class Not(Statement):
    def calc(self, environ, params):
        assert len(params) == 1
        # TODO: check if all params are numbers
        return not bool(params[0])


class Let(Statement):
    def process_params(self, environ, nodes):
        assert len(nodes) == 2

        definition, statement_node = nodes
        assert len(definition.children) == 2

        # TODO: probably not safe
        symbol = definition.children[0].name
        value = definition.children[1].evaluate(environ)

        with environ.within_new_frame():
            environ.push_frame()
            environ.define(symbol, Const(value))
            result = [statement_node.evaluate(environ)]

        return result

    def calc(self, environ, params):
        return params[0]


class If(Statement):
    def process_params(self, environ, nodes):
        assert len(nodes) == 3

        comp = nodes[0].evaluate(environ)
        if comp:
            return [nodes[1].evaluate(environ)]
        return [nodes[2].evaluate(environ)]

    def calc(self, environ, params):
        return params[0]


class Proc(Statement):
    def __init__(self, param_names, body_nodes):
        self.param_names = param_names
        self.body_nodes = body_nodes

    def calc(self, environ, params):
        # TODO: check if len(params) == len(self.param_names)
        with environ.within_new_frame():
            for name, value in zip(self.param_names, params):
                environ.define(name, Const(value))
            result = 0
            for node in self.body_nodes:
                result = node.evaluate(environ)
            return result


class Func(Statement):
    def process_params(self, environ, nodes):
        # Allow multiple stamements in the function's body
        assert len(nodes) == 3

        func_name = nodes[0].name
        # TODO: check if symbol

        param_names = [x.name for x in nodes[1].children]
        # TODO: check if all are symbol
        # TODO: check if all are different
        # TODO: check if nodes has enough items

        environ.define(func_name, Proc(param_names, nodes[2:]))

        return []

    def calc(self, environ, params):
        return 0
