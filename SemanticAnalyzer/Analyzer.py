from SemanticAnalyzer.SymbolTable import SymbolTable
from SemanticAnalyzer.Symbol import Symbol


class Analyzer(object):
    def __init__(self):
        self.qtdTabelas = 1
        self.symtab = []
        self.symtab.append(SymbolTable())
        self.qtdClasses = 0
        self.declClasses = []

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

    def firstPass(self, tree):
        if tree.producao == "classe":
            tipo = "class"
            nome = tree.children[1].rule
            self.qtdClasses += 1
            self.declClasses.append(SymbolTable())
            self.declClasses[self.qtdClasses - 1].insert(nome, tipo)
        # verificação de produção, se for var ou params é definição de variavel
        if (tree.producao == "var" or tree.producao == "params") and tree.parent.producao == 'classe':
            tipo = ""
            nome = ""
            for i in tree.children[0].children:
                tipo += i.rule
            nome = tree.children[1].rule
            self.declClasses[self.qtdClasses - 1].insert(nome, tipo)

        # verificação de produção, se for main, insere main
        if tree.producao == "main":
            tipo = "class"
            nome = tree.children[1].rule
            # insere classe inicial
            self.qtdClasses += 1
            self.declClasses.append(SymbolTable())
            self.declClasses[self.qtdClasses - 1].insert(nome, tipo)

            # insere método main
            self.declClasses[self.qtdClasses - 1].insert("main", "static void")

        # verificação de produção, se for metodo, verifica a definição do metodo
        if tree.producao == "metodo":
            tipo = ""
            nome = ""
            for i in tree.children[1].children:
                tipo += i.rule
            nome = tree.children[2].rule
            self.declClasses[self.qtdClasses - 1].insert(nome, tipo)

        # recursão
        if len(tree.children) != 0:
            for i in tree.children:
                self.firstPass(i)

    def secondPass(self, tree):
        escopo = 0
        if tree.producao == "classe":
            tipo = "class"
            nome = tree.children[1].rule
            self.symtab[self.qtdTabelas-1].insert(nome, tipo)
            self.visit_Public()
            escopo += 1
        if tree.producao == "cmd" or tree.producao == "pexp":
            if tree.simbolos[0] == "ID":
                variavel = tree.children[0].rule
                self.visit_Var(variavel)
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
            tipo = "class"
            nome = tree.children[1].rule
            self.symtab[self.qtdTabelas-1].insert(nome, tipo)
            self.visit_Public()
            self.symtab[self.qtdTabelas-1].insert("main", "static void")
            self.visit_Public()
            escopo += 2

        # verificação de produção, se for metodo, verifica a definição do metodo
        if tree.producao == "metodo":
            tipo = ""
            nome = ""
            for i in tree.children[1].children:
                tipo += i.rule
            nome = tree.children[2].rule
            self.symtab[self.qtdTabelas-1].insert(nome, tipo)
            self.visit_Public()
            escopo += 1

        # resolver chamadas de métodos
        # PEXP   -> P_POINT id
        #         | PEXP P_POINT id lparen EXPS_O rparen
        #         | new id lparen rparen
        if tree.producao == "pexp":
            # entrar em cada PEXP recursivo e concatenar referencias e.g:
            # checkPEXP([]) { if(PEXP) then checkPEXP(lista) else lista.insert(0,id)}
            pass


        # recursão
        if len(tree.children) != 0:
            for i in tree.children:
                self.iterate(i)
                if i.rule == "}" and escopo > 0:
                    escopo -= 1
                    self.visit_RightCurly()
