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

    def _check_version_value(self, from_ver, to_ver=None):
        if to_ver and from_ver >= to_ver or from_ver < 0:
            raise ValueError("Versions value error")
        return from_ver, to_ver

    def insert(self, text, pos=None, to_version=None):
        pos = self._check_position_value(pos)
        self._text = self._text[:pos] + text + self._text[pos:]
        if to_version:
            self._check_version_value(from_ver=self._version, to_ver=to_version)
            self._version = to_version
        else:
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

    def action(self, act: 'Action'):
        self._check_version_value(act.from_version, act.to_version)
        if act.__class__.__name__ == "InsertAction":
            print('tyt')

    def get_actions(self):
        pass


class Action:
    def __init__(self, from_version, to_version):
        self._from_version = from_version
        self._to_version = to_version

    @property
    def from_version(self):
        return self._from_version

    @property
    def to_version(self):
        return self._to_version


class InsertAction(Action):
    def __init__(self, pos, text, from_version, to_version):
        self._text = text
        self._pos = pos
        super().__init__(from_version=from_version, to_version=to_version)

    @property
    def text(self):
        return self._text


class ReplaceAction(Action):
    pass


class DeleteAction(Action):
    pass


if __name__ == '__main__':
    h = TextHistory()
    action = InsertAction(pos=0, text='abc', from_version=1, to_version=10)
    h.action(action)
