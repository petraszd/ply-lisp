from ply import lex
from ply import yacc

import tinylisp.lexerrules
from tinylisp.parserrules import ParserWalker


lexer = lex.lex(module=tinylisp.lexerrules)

walker = ParserWalker()
parser = yacc.yacc(module=walker)

formulas = [
    "(+ 1 2)",
    "(+ 1 2 3)",
    "(+ 1)",
    "(+ 1 (let (a 2) (+ a a a)))",
    "(+ 3 (let (a 2) (let (a 3) (+ a a a))))",
    """
(func fibonacci-number (a b n)
    (if (< n 0)
        a
        (fibonacci-number b (+ a b) (- n 1))))

(fibonacci-number 0 1 9)
    """
]
for formula in formulas:
    walker.reset()
    parser.parse(formula, lexer=lexer)

    result = walker.root.result()
    if result.error is None:
        print("Result:", result.value)
    else:
        print("-- Error --:", result.error)
