from SemanticAnalyzer.SymbolTable import SymbolTable
from SemanticAnalyzer.Symbol import Symbol


class Analyzer(object):
    def __init__(self):
        self.qtdTabelas = 1
        self.symtab = []
        self.symtab.append(SymbolTable())

    def visit_Var(self, var_name):
        var_symbol = self.find(var_name)
        if var_symbol is None:
            raise Exception(
                'Símbolo ' + var_name + ' não declarado'
            )

    def visit_Public(self):
        self.qtdTabelas += 1
        self.symtab.append(SymbolTable())

    def visit_RightCurly(self):
        self.symtab.pop()
        self.qtdTabelas -= 1

    def find(self, name):
        for nivelTabela in reversed(self.symtab):
            varDecl = nivelTabela.find(name)
            if varDecl is not None:
                return varDecl
        return None


if __name__ == '__main__':

    analyzer = Analyzer()
    int_type = 'int'
    boolean_type = 'boolean'

    x = Symbol('x', int_type)
    y = Symbol('y', int_type)
    a = Symbol('a', boolean_type)
    b = Symbol('b', boolean_type)

    analyzer.symtab[analyzer.qtdTabelas-1].insert(x.name, x.type)                #sempre vai inserir na última tabela de símbolos da lista
    analyzer.symtab[analyzer.qtdTabelas-1].insert(y.name, y.type)

    analyzer.symtab[analyzer.qtdTabelas-1].insert(a.name, a.type)
    analyzer.symtab[analyzer.qtdTabelas-1].insert(b.name, b.type)

    print('Tabela de símbolos ' + str(analyzer.qtdTabelas) + '\n')              #tabela 1 com indice 0, que representa as variaveis declaradas em uma class
    print(analyzer.symtab[analyzer.qtdTabelas-1])

    ''' Erros
    x = Symbol('x', boolean_type)
    analyzer.symtab[analyzer.qtdTabelas - 1].insert(x.name, x.type)             #Tenta declarar um x já declarado
    analyzer.visit_Var('z')                                                     #verifica se z já foi declarado
    '''

    analyzer.visit_Public()                                                     #Achou um public, então cria uma nova lista pois é um novo escopo de método

    x = Symbol('x', boolean_type)
    y = Symbol('y', boolean_type)
    z = Symbol('z', int_type)

    analyzer.symtab[analyzer.qtdTabelas-1].insert(x.name, x.type)               #Erro acima não se repete aqui pois é criada uma nova lista
    analyzer.symtab[analyzer.qtdTabelas-1].insert(y.name, y.type)
    analyzer.symtab[analyzer.qtdTabelas-1].insert(z.name, z.type)

    print('Tabela de símbolos ' + str(analyzer.qtdTabelas) + '\n')              # tabela 2
    print(analyzer.symtab[analyzer.qtdTabelas - 1])

    analyzer.visit_Var('z')                                                     # verifica que z já foi declarado

    analyzer.visit_RightCurly()                                                 # remove o último elemento da lista de tabelas hash

    print('Tabela de símbolos ' + str(analyzer.qtdTabelas) + '\n')              # tabela 1
    print(analyzer.symtab[analyzer.qtdTabelas - 1])