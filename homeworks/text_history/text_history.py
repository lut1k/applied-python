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

    def _check_position_value(self, position, delete_length=None):
        if position == 0:
            return 0
        if position is None:
            return len(self._text)
        if len(self._text) < position or position < 0:
            raise ValueError("Insert position out of string length")
        if delete_length and position + delete_length > len(self._text):
            raise ValueError("Delete position out of string length")
        return position

    def insert(self, text, pos=None):
        pos = self._check_position_value(pos)
        self._text = self._text[:pos] + text + self._text[pos:]
        self._version += 1
        return self._version

    def replace(self, text, pos=None):
        pos = self._check_position_value(pos)
        self._text = self._text[:pos] + text + self._text[pos+len(text):]
        self._version += 1
        return self._version

    def delete(self, pos, length):
        pos = self._check_position_value(pos, length)
        self._text = self._text[:pos] + self._text[pos + length:]
        self._version += 1
        return self._version


class Action:
    pass


class InsertAction(Action):
    pass


class ReplaceAction(Action):
    pass


class DeleteAction(Action):
    pass


if __name__ == '__main__':
    h = TextHistory()
    h.insert('abc')
    print(h.text, h.version)
    # h.delete(pos=10, length=2)
    print(h.text, h.version)
    h.delete(pos=1, length=3)
    print(h.text, h.version)
    h.delete(pos=-1, length=2)
    print(h.text, h.version)
