from tinylisp import statements as st


class Environ:
    def __init__(self):
        self.reserved = {
            'let': st.Let(),
            'if': st.If(),
            'func': st.Func(),
        }

        global_frame = {}
        global_frame['+'] = st.Plus()
        global_frame['-'] = st.Minus()
        global_frame['<'] = st.Less()
        global_frame['<='] = st.LessOrEqual()
        global_frame['>'] = st.More()
        global_frame['>='] = st.MoreOrEqual()
        global_frame['not'] = st.Not()
        self.frames = [global_frame]

    def lookup(self, symbol):
        if symbol in self.reserved:
            return self.reserved[symbol]

        for frame in reversed(self.frames):
            if symbol in frame:
                return frame[symbol]

        assert False, "Can't find `{}`".format(symbol)

    def define(self, symbol, value):
        # TODO: check if it is not `reserved`
        self.frames[-1][symbol] = value

    def within_new_frame(self):  # Just nicer to read
        return self

    def push_frame(self):
        self.frames.append({})

    def pop_frame(self):
        self.frames.pop()

    def __enter__(self):
        self.push_frame()

    def __exit__(self, exc_type, exc_value, traceback):
        self.pop_frame()
