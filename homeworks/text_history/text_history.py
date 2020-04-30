class TextHistory:
    def __init__(self, text='', version=0):
        self._text = text
        self._version = version

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version

    def _check_is_position_in_length(self, position):
        if len(self._text) < position or position < 0:
            raise ValueError("Insert position out of string length")

    def insert(self, text, pos=None):
        if pos is None:
            self._text += text
        else:
            self._check_is_position_in_length(pos)
            self._text = self.text[:pos] + text + self.text[pos:]
        self._version += 1
        return self._version

    def replace(self, text, pos=None):
        if pos is None:
            self._text += text
        else:
            self._check_is_position_in_length(pos)

    def delete(self, pos, length):
        pass


class Action:
    pass


class InsertAction(Action):
    pass


class ReplaceAction(Action):
    pass


class DeleteAction(Action):
    pass


h = TextHistory()
print(h.text)
print(h.version)
h.insert('abc', 0)
print(h.text)
print(h.version)


