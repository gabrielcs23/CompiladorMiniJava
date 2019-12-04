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

    def iterate(self, tree):

        # verificação de produção, se for var ou params é definição de variavel
        if tree.producao == "var" or tree.producao == "params":
            tipo = ""
            nome = ""
            for i in tree.children[0].children:
                tipo += i.rule
            nome = tree.children[1].rule
            self.symtab[self.qtdTabelas-1].insert(nome, tipo)

        # verificação de produção, se for main, insere main
        if tree.producao == "main":
            self.symtab[self.qtdTabelas-1].insert("main", "static void")
            print('Tabela de símbolos ' + str(self.qtdTabelas) + '\n')
            print(self.symtab[self.qtdTabelas - 1])
            self.visit_Public()

        # verificação de produção, se for metodo, verifica a definição do metodo
        if tree.producao == "metodo":
            tipo = ""
            nome = ""
            for i in tree.children[1].children:
                tipo += i.rule
            nome = tree.children[2].rule
            self.symtab[self.qtdTabelas-1].insert(nome, tipo)
            print('Tabela de símbolos ' + str(self.qtdTabelas) + '\n')
            print(self.symtab[self.qtdTabelas - 1])
            self.visit_Public()

        #recursão
        if len(tree.children) != 0:
            for i in tree.children:
                self.iterate(i)
