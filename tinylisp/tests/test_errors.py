from tinylisp.tests.parsertestcase import ParserTestCase


class BlockStatementErrorsTestCase(ParserTestCase):
    def test_zero_statements(self):
        self.assertInError('parser error', "(+ 1 ())")


class PlusStatementErrorsTestCase(ParserTestCase):
    def test_no_params(self):
        self.assertInError('Not enough parameters', "(+)")

    def test_not_everyone_is_number(self):
        self.assertInError('Not numbers',
                           """
                           (func a_func (a) a)
                           (+ 1 2 a_func 1)
                           """)
