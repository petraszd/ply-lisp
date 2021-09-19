from tinylisp.exceptions import InterpreterError


def at_least_one_param(params):
    n_params = len(params)
    if n_params < 1:
        raise InterpreterError('Not enough parameters: {}'.format(n_params))


def all_numbers(params):
    for param in params:
        print(param)
