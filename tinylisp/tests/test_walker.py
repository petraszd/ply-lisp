from tinylisp.tests.parsertestcase import ParserTestCase


class PlusStatementTestCase(ParserTestCase):
    def test_add_simple(self):
        self.assertParseVal(3, "(+ 1 2)")

    def test_add_three_parameters(self):
        self.assertParseVal(6, "(+ 1 2 3)")

    def test_add_nested(self):
        self.assertParseVal(15, "(+ 1 (+ 2 3 4) 5)")


class MinusStatementTestCase(ParserTestCase):
    def test_simple(self):
        self.assertParseVal(3, "(- 5 2)")


class LetStatementTestCase(ParserTestCase):
    def test_simple_let(self):
        self.assertParseVal(999, "(let (a 999) a)")

    def test_two_variables(self):
        self.assertParseVal(8, """
                               (let (a 3)
                                 (let (b 5)
                                   (+ a b)))
                               """)

    def test_override(self):
        self.assertParseVal(2, """
                               (let (a 1)
                                 (let (a 2)
                                   a))
                               """)


class LessStatementTestCase(ParserTestCase):
    def test_simple_when_less(self):
        self.assertParseVal(1, "(< 2 3)")

    def test_simple_when_equal(self):
        self.assertParseVal(0, "(< 2 2)")

    def test_simple_when_more(self):
        self.assertParseVal(0, "(< 3 2)")


class LessOrEqualStatementTestCase(ParserTestCase):
    def test_simple_when_less(self):
        self.assertParseVal(1, "(<= 2 3)")

    def test_simple_when_equal(self):
        self.assertParseVal(1, "(<= 2 2)")

    def test_simple_when_more(self):
        self.assertParseVal(0, "(<= 3 2)")


class MoreStatementTestCase(ParserTestCase):
    def test_simple_when_less(self):
        self.assertParseVal(0, "(> 2 3)")

    def test_simple_when_equal(self):
        self.assertParseVal(0, "(> 2 2)")

    def test_simple_when_more(self):
        self.assertParseVal(1, "(> 3 2)")


class MoreOrEqualStatementTestCase(ParserTestCase):
    def test_simple_when_less(self):
        self.assertParseVal(0, "(>= 2 3)")

    def test_simple_when_equal(self):
        self.assertParseVal(1, "(>= 2 2)")

    def test_simple_when_more(self):
        self.assertParseVal(1, "(>= 3 2)")


class NotStatementTestCase(ParserTestCase):
    def test_when_false(self):
        self.assertParseVal(1, "(not 0)")

    def test_when_true(self):
        self.assertParseVal(0, "(not 1)")

    def test_when_number(self):
        self.assertParseVal(0, "(not 8)")


class IfStatementTestCase(ParserTestCase):
    def test_when_true(self):
        self.assertParseVal(3, "(if (< 1 2) 3 4)")

    def test_when_false(self):
        self.assertParseVal(4, "(if (< 2 1) 3 4)")

    def test_when_true_no_eval_of_false(self):
        self.assertParseVal(3, "(if (< 1 2) 3 does-not-exist)")

    def test_when_false_no_eval_of_true(self):
        self.assertParseVal(4, "(if (< 2 1) does-not-exist 4)")


class RootStatementTestCase(ParserTestCase):
    def test_more_than_one_statement(self):
        self.assertParseVal(9, "(+ 2 2) (+ 3 (+ 3 3))")


class FuncTestCase(ParserTestCase):
    def test_func_definition_and_call(self):
        self.assertParseVal(12, """
                                (func sum-and-double (a b c)
                                    (let (sum (+ a b c))
                                        (+ sum sum)))

                                (sum-and-double 1 2 3)""")

    def test_zero_params(self):
        self.assertParseVal(4,
                            """
                            (func two_plus_two ()
                            (+ 2 2))
                            """)
