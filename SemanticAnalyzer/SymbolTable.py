class SymbolTable(object):
    def __init__(self):
        self._symbols = {}

    def __str__(self):
        symtab_header = 'Symbol table contents'
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def insert(self, symbol, type):
        print('Insert: ' + symbol + ' with type ' + type)
        self._symbols[symbol] = type

if __name__ == '__main__':
    symtab = SymbolTable()
    int_type = 'int'

    symtab.insert('x', int_type)
    symtab.insert('y', int_type)
    print(symtab)