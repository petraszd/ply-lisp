import unittest

from ply import lex
from ply import yacc

import tinylisp.lexerrules
from tinylisp.parserrules import ParserWalker


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.lexer = lex.lex(module=tinylisp.lexerrules)
        self.walker = ParserWalker()
        self.parser = yacc.yacc(module=self.walker, debug=False)

    def parse(self, source_code):
        self.parser.parse(source_code, lexer=self.lexer, debug=False)
        return self.walker.root.result()

    def assertParseVal(self, value, source_code):
        self.assertEqual(value, self.parse(source_code).value)

    def assertInError(self, error, source_code):
        parse_error = self.parse(source_code).error or ''
        self.assertIn(error.lower(), parse_error.lower())
