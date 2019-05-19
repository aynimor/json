import urllib.parse


def dumps(jsonobj):
    return str(jsonobj)


class ParseJson(object):
    def __init__(self, jsonstr):
        self._str = jsonstr.replace("'", '"')
        self._pos = 0

    def _blank(self):
        if self._pos < len(self._str) and self._str[self._pos] in [' ', '\n', '\r', '\t']:
            self._pos += 1
            self._blank()

    # 获取当前 _pos 对应的 char
    def _current_char(self):
        return self._str[self._pos]

    # 主函数, 判断 JSON 格式
    def parse(self):
        # self._blank()
        ch = self._current_char()
        if ch == '{':
            self._pos += 1
            return self._parse_object()
        elif ch == '[':
            self._pos += 1
            return self._parse_array()
        else:
            print('JSON parse ERROR')

    def _parse_string(self):
        start = end = self._pos
        # 0     2     2
        while self._str[end] != '"':
            if self._str[end] == '"':
                break
            end += 1
            if self._str[end] == '\\':
                end += 1
                if self._str[end] in '"\\/rntubf':
                    end += 1
        self._pos = end
        self._pos += 1
        return self._str[start: end]

    def _parse_number(self):
        start = end = self._pos
        print(self._str[start])
        while self._str[end] not in ' \n\t\r,}]':   # 数字结束的字符串
            end += 1
        number = self._str[start:end]
        try:
            # 尝试进行转换
            if '.' in number or 'e' in number or 'E' in number:
                res = float(number)
            else:
                res = int(number)
            self._pos = end
        except ValueError as e:
            # 错误处理
            print(e.with_traceback())

        return res

    def _parse_value(self):
        c = self._current_char()
        if c == '{':
            self._pos += 1
            return self._parse_object()
        elif c == '[':
            self._pos += 1
            return self._parse_array()
        elif c == '"':
            self._pos += 1
            return self._parse_string()
        elif c == "'":
            self._pos += 1
            return self._parse_string("'")
        elif c == 't' and self._str[self._pos:self._pos + 4] == 'true':
            self._pos += 4
            self._blank()
            return True
        elif c == 'f' and self._str[self._pos:self._pos + 5] == 'false':
            self._pos += 5
            self._blank()
            return False
        elif c == 'n' and self._str[self._pos:self._pos + 4] == 'null':
            self._pos += 4
            self._blank()
            return None
        else:
            self._blank()
            return self._parse_number()

    def _parse_array(self):
        array = []
        self._blank()

        if self._current_char() == ']':
            self._pos += 1
            return array
        while True:
            item = self._parse_value()

            array.append(item)
            self._blank()

            if self._current_char() is ',':
                self._pos += 1
                self._blank()

            elif self._current_char() is ']':
                self._pos += 1
                return array
            else:
                print('array json parse error')
                return None

    def _parse_object(self):
        obj = {}
        self._blank()
        if self._current_char() == '}':
            self._pos += 1
            return obj
        self._pos += 1
        while True:
            key = self._parse_string()
            self._blank()
            self._pos += 1
            self._blank()
            value = self._parse_value()
            obj[key] = value
            self._blank()
            if self._current_char() == ',':
                self._pos += 1
                self._blank()
                self._pos += 1
            if self._current_char() == '}':
                self._pos += 1
                break
        return obj


if __name__ == '__main__':
    a = '''{
        "test": {
            'test1': ['1', '2', '3'],
            " another ": {
                "c": {
                    "n": {
                        "d": -126387E1,
                        "123": 'cjadhj'
                    }
                }
            },
            'test3': ['1', '2', '3']
        }
    }'''

    # a = '''['one', ['1', '23', '4', '21', '23'], 'test', 'three', 'abcdefg', {'test': 'haha'}]'''
    # a = '''{'test':"haha"}'''
    json = ParseJson(a)
    obj = json.parse()
    print('parser', obj)
    print('parser t', type(obj))
    print('dumps', dumps(obj))
    print('dumps t', type(dumps(obj)))
