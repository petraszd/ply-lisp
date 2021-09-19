import tinylisp.lexerrules
from tinylisp import nodes


class ParserWalker:
    tokens = tinylisp.lexerrules.tokens

    def __init__(self):
        self.reset()

    def reset(self):
        self.root = nodes.Root()
        self.node_stack = [self.root]

    def p_root(self, t):
        'root : blocks'

    def p_blocks_multi(self, t):
        'blocks : block blocks'

    def p_block_one(self, t):
        'blocks : block'

    def p_block_literal(self, t):
        'block : begin elements end'

    def p_elements_one(self, t):
        'elements : elem'

    def p_elements_multi(self, t):
        'elements : elem elements'

    def p_elem_block(self, t):
        'elem : block'

    def p_begin(self, t):
        'begin : S_BEGIN'
        block = nodes.Block()

        self.node_stack[-1].add_child(block)
        self.node_stack.append(block)

    def p_end(self, t):
        'end : S_END'
        self.node_stack.pop()

    def p_elem_number(self, t):
        'elem : NUMBER'
        self.node_stack[-1].add_child(nodes.Number(t[1]))

    def p_elem_symbol(self, t):
        'elem : SYMBOL'
        self.node_stack[-1].add_child(nodes.Symbol(t[1]))

    def p_error(self, t):
        if t is None:
            line, row = 1, 1
        else:
            line, row = t.lineno, t.lexpos
        self.root = nodes.ParseErrorRoot(line=line, row=row)
        self.node_stack[0] = self.root
