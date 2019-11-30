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
        print('Insert: ' + symbol + ' with type ' + type + '\n')
        resposta = self.find(symbol)
        if resposta is None: #só insere declaração se não tiver nenhuma
            self._symbols[symbol] = type
        else:
            raise Exception(
                'Símbolo ' + symbol + ' já declarado como ' + resposta
            )

    def find(self, name):
        symbol = self._symbols.get(name)
        return symbol