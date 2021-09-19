tokens = (
    'NUMBER',
    'SYMBOL',
    'S_BEGIN',
    'S_END',
)
t_ignore = '\t\n '


def t_S_BEGIN(t):
    r'\('
    t.value = ''
    return t


def t_S_END(t):
    r'\)'
    t.value = ''
    return t


def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_SYMBOL(t):
    r'[^\d\s][^\s()]*'
    return t


def t_error(t):
    # TODO: Better error reporting
    print('Syntax error near: "{code}". Line={line}; Pos={pos}'.format(
        line=t.lineno, pos=t.lexpos, code=t.value[0:3]
    ))
    t.lexer.skip(1)
