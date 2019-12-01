from SemanticAnalyzer.SymbolTable import SymbolTable

class Analyzer():
    def __init__(self):
        self.qtdTabelas = 1
        self.symtab = []
        self.symtab.append(SymbolTable())

    def visit_Var(self, var_name):
        var_symbol = self.symtab[analyzer.qtdTabelas-1].find(var_name)
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

if __name__ == '__main__':

    analyzer = Analyzer()
    int_type = 'int'
    boolean_type = 'boolean'

    analyzer.symtab[analyzer.qtdTabelas-1].insert('x', int_type)                #sempre vai inserir na última tabela de símbolos da lista
    analyzer.symtab[analyzer.qtdTabelas-1].insert('y', int_type)

    analyzer.symtab[analyzer.qtdTabelas-1].insert('a', boolean_type)
    analyzer.symtab[analyzer.qtdTabelas-1].insert('b', boolean_type)

    print('Tabela de símbolos ' + str(analyzer.qtdTabelas) + '\n')              #tabela 1 com indice 0, que representa as variaveis declaradas em uma class
    print(analyzer.symtab[analyzer.qtdTabelas-1])

    ''' Erros
    analyzer.symtab[analyzer.qtdTabelas - 1].insert('x', boolean_type)          #Tenta declarar um x já declarado
    analyzer.visit_Var('z')                                                     #verifica se z já foi declarado
    '''

    analyzer.visit_Public()                                                     #Achou um public, então cria uma nova lista pois é um novo escopo de método

    analyzer.symtab[analyzer.qtdTabelas-1].insert('x', boolean_type)            #Erro acima não se repete aqui pois é criada uma nova lista
    analyzer.symtab[analyzer.qtdTabelas-1].insert('y', boolean_type)
    analyzer.symtab[analyzer.qtdTabelas-1].insert('z', int_type)

    print('Tabela de símbolos ' + str(analyzer.qtdTabelas) + '\n')              #tabela 2
    print(analyzer.symtab[analyzer.qtdTabelas - 1])

    analyzer.visit_Var('z')                                                     #verifica que z já foi declarado

    analyzer.visit_RightCurly()                                                 #remove o último elemento da lista de tabelas hash

    print('Tabela de símbolos ' + str(analyzer.qtdTabelas) + '\n')              # tabela 1
    print(analyzer.symtab[analyzer.qtdTabelas - 1])