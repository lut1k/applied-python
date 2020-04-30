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

    def _check_position_value(self, position, length_text):
        if position == 0:
            return 0
        if position is None:
            return length_text
        if len(self._text) < position or position < 0:
            raise ValueError("Insert position out of string length")
        return position

    def insert(self, text, pos=None):
        pos = self._check_position_value(pos, len(self._text))
        self._text = self._text[:pos] + text + self._text[pos:]
        self._version += 1
        return self._version

    def replace(self, text, pos=None):
        pos = self._check_position_value(pos, len(self._text))
        self._text = self._text[:pos] + text
        self._version += 1
        return self._version

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


if __name__ == '__main__':
    h = TextHistory()
    print(h.text, h.version)
    h.insert('abc')
    print(h.text, h.version)
    h.insert('abc', pos=10)
    print(h.text, h.version)
    # h.replace('abc')
    # print(h.text, h.version)
    # h.replace('xyz', pos=2)
    # print(h.text, h.version)
    # h.replace('X', pos=2)
    # print(h.text, h.version)
    # h.replace('END')
    # print(h.text, h.version)
