from SemanticAnalyzer.SymbolTable import SymbolTable
from SemanticAnalyzer.Symbol import Symbol

qtd_true_branch = 0
qtd_false_branch = 0
qtd_endif_branch = 0
qtd_while = 0
this_ref = "main"
class_call_ref = ""


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
        global this_ref
        escopo = 0
        if tree.producao == "classe":
            tipo = "class"
            nome = tree.children[1].rule
            this_ref = nome
            self.symtab[self.qtdTabelas - 1].insert(nome, tipo)
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
            self.symtab[self.qtdTabelas - 1].insert(nome, tipo)

        # verificação de produção, se for main, insere main
        if tree.producao == "main":
            tipo = "class"
            nome = tree.children[1].rule
            self.symtab[self.qtdTabelas - 1].insert(nome, tipo)
            self.visit_Public()
            self.symtab[self.qtdTabelas - 1].insert("main", "static void")
            self.visit_Public()
            escopo += 2

        # verificação de produção, se for metodo, verifica a definição do metodo
        if tree.producao == "metodo":
            tipo = ""
            nome = ""
            for i in tree.children[1].children:
                tipo += i.rule
            nome = tree.children[2].rule
            self.symtab[self.qtdTabelas - 1].insert(nome, tipo)
            self.visit_Public()
            escopo += 1

        # resolver chamadas de métodos
        # PEXP   -> id ✓
        #         | this ✓
        #         | PEXP P_POINT id ✓
        #         | PEXP P_POINT id lparen EXPS_O rparen ✓
        #         | new id lparen rparen ✓
        if tree.producao == "pexp":
            # o caso 'lparen EXP rparen' não precisa ser avaliado aqui. a recursão cuida de EXP
            if len(tree.simbolos) > 2 and tree.simbolos[1] != "exp":
                # entrar em cada PEXP recursivo e concatenar referencias e.g:
                if tree.parent.producao != "pexp":  # se o pai foi 'pexp' significa que este nó já foi verificado
                    lista = []
                    self.buildChainedPEXP(tree, lista)
                    if len(lista) > 1 and lista[0][0].isupper():  # apenas interessa os casos onde primeiro elem é class
                        self.checkChainedPEXP(lista)


        # recursão
        if len(tree.children) != 0:
            for i in tree.children:
                self.secondPass(i)
                if i.rule == "}" and escopo > 0:
                    escopo -= 1
                    self.visit_RightCurly()

        # limpando referência da classe após terminar busca em profundidade
        if tree.producao == "classe":
            this_ref = ''

    def buildChainedPEXP(self, tree, lista):
        if tree.simbolos[0] == "pexp":
            self.buildChainedPEXP(tree.children[0], lista)
            lista.append(tree.children[2].rule)
        elif tree.simbolos[0] == "ID":
            lista.append(tree.children[0].rule)
        elif tree.simbolos[0] == "RW_THIS":
            lista.append(this_ref)
        elif tree.simbolos[1] == "ID":
            lista.append(tree.children[1].rule)

    def checkChainedPEXP(self, varList):
        classTable = None
        declClasse = None
        for declClasse in self.declClasses:
            classTable = declClasse.find(varList[0])
            if classTable is not None:
                break
        if classTable is not None:
            for var in varList[1:]:
                var_symbol = declClasse.find(var)
                if var_symbol is None:
                    raise Exception(
                        'Método %s não declarado na classe %s' % (var, varList[0])
                    )
        else:
            raise Exception(
                'Classe %s não declarada' % varList[0]
            )

    # método para retornar o valor resultante de uma série de operações de somas, multiplicações, subtrações e divisões
    def evaluate(self, tree):
        # se chegar em sexp, verifica se a produção gera um numero ou um numero negativo
        if tree.producao == "sexp":
            if tree.simbolos[0] == "NUMBER" or tree.simbolos[0] == "RW_TRUE" or tree.simbolos[0] == "RW_FALSE":
                return tree.children[0].rule
            elif tree.simbolos[0] == "OP_MINUS":
                child_eval = self.evaluate(tree.children[1])
                if child_eval is not None:
                    return child_eval * -1
                else:
                    return None
            else:
                return None
        # ao chegar em mexp, verifica o resultado da divisao ou multiplicação
        if tree.producao == "mexp":
            if len(tree.children) == 1:
                return self.evaluate(tree.children[0])
            op1 = self.evaluate(tree.children[0])
            op2 = self.evaluate(tree.children[2])
            if op1 is not None and op2 is not None and op1 != 'true' and op1 != 'false' and op2 != 'true' and op2 != 'false':
                if tree.simbolos[1] == "OP_MULTIPLY":
                    return op1 * op2
                elif tree.simbolos[1] == "OP_DIVISION":
                    if op2 != 0:
                        return op1 / op2
                    else:
                        return None
                else:
                    return None
            else:
                return None
        # ao chegar em aexp, verifica o resultado da soma ou subtração
        if tree.producao == "aexp":
            if len(tree.children) == 1:
                return self.evaluate(tree.children[0])
            op1 = self.evaluate(tree.children[0])
            op2 = self.evaluate(tree.children[2])
            if op1 is not None and op2 is not None and op1 != 'true' and op1 != 'false' and op2 != 'true' and op2 != 'false':
                if tree.simbolos[1] == "OP_PLUS":
                    return op1 + op2
                elif tree.simbolos[1] == "OP_MINUS":
                    return op1 - op2
                else:
                    return None
            else:
                return None
        # ao chegar em rexp, verifica o resultado das operações de comparação
        if tree.producao == "rexp":
            if len(tree.children) == 1:
                return self.evaluate(tree.children[0])
            op1 = self.evaluate(tree.children[0])
            op2 = self.evaluate(tree.children[2])
            if op1 is not None and op2 is not None:
                if tree.simbolos[
                    1] == "OP_LESSER" and op1 != 'true' and op1 != 'false' and op2 != 'true' and op2 != 'false':
                    return op1 < op2
                elif tree.simbolos[1] == "OP_EQUAL":
                    return op1 == op2
                elif tree.simbolos[1] == "OP_NOT_EQUAL":
                    return op1 != op2
                else:
                    return None
            else:
                return None
        # ao chegar em exp, verifica o resultado da operação and
        if tree.producao == "exp":
            if len(tree.children) == 1:
                return self.evaluate(tree.children[0])
            op1 = self.evaluate(tree.children[0])
            op2 = self.evaluate(tree.children[2])
            if op1 is not None and op2 is not None:
                if tree.simbolos[1] == "OP_AND" and (op1 == 'true' or op1 == 'false') and (
                        op2 == 'true' or op2 == 'false'):
                    return op1 and op2
                else:
                    return None
            else:
                return None

    def thirdPass(self, tree):
        if tree.producao == "exp":
            value = self.evaluate(tree)
            print(self.evaluate(tree))
            if value is not None:
                # se value for true ou false, substitui por 1 ou 0 para facilitar na geração de código
                if type(value) == str:
                    if value == 'true':
                        value = 1
                    else:
                        value = 0
                tree.rule = value
                tree.children = []

        # recursão
        if len(tree.children) != 0:
            for i in tree.children:
                self.thirdPass(i)

    def cgen(self, tree, file):
        global qtd_endif_branch
        global qtd_true_branch
        global qtd_false_branch
        global qtd_while
        global this_ref
        global class_call_ref
        if tree.producao == "num":
            file.write("li $a0 " + str(tree.rule) + "\n")
        elif tree.producao == "sexp":
            if len(tree.children) == 1:
                self.cgen(tree.children[0], file)
            elif len(tree.children) == 2:
                if tree.simbolos[0] == "OP_MINUS":
                    self.cgen(tree.children[1], file)
                    file.write("subu $a0 $zero $a0\n")
                elif tree.simbolos[0] == "OP_NOT":
                    self.cgen(tree.children[1], file)
                    file.write("xori $a0 $a0 1\n")
        elif tree.producao == "aexp" or tree.producao == "mexp" or tree.producao == "rexp" or tree.producao == "exp":
            if len(tree.children) == 1:
                self.cgen(tree.children[0], file)
            elif len(tree.children) == 3:
                self.cgen(tree.children[0], file)
                file.write("sw $a0 0($sp)\n")
                file.write("addiu $sp $sp -4\n")
                self.cgen(tree.children[2], file)
                file.write("lw $t1 4($sp)\n")
                if tree.simbolos[1] == "OP_PLUS":
                    file.write("add $a0 $t1 $a0\n")
                elif tree.simbolos[1] == "OP_MINUS":
                    file.write("sub $a0 $t1 $a0\n")
                elif tree.simbolos[1] == "OP_MULTIPLY":
                    file.write("mult $t1 $a0\n")
                    file.write("mflo $a0\n")
                elif tree.simbolos[1] == "OP_DIVISION":
                    file.write("div $t1 $a0\n")
                    file.write("mflo $a0\n")
                elif tree.simbolos[1] == "OP_LESSER":
                    file.write("slt $a0 $t1 $a0\n")
                elif tree.simbolos[1] == "OP_EQUAL":
                    file.write("subu $t2, $a0, $t1\n")
                    file.write("sltu $t2, $zero, $t2\n")
                    file.write("xori $a0, $t2, 1\n")
                elif tree.simbolos[1] == "OP_NOT_EQUAL":
                    file.write("subu $t2, $a0, $t1\n")
                    file.write("sltu $t2, $zero, $t2\n")
                elif tree.simbolos[1] == "OP_AND":
                    file.write("and $a0 $a0 $t1\n")
                file.write("addiu $sp $sp 4\n")
        elif tree.producao == "cmd":
            if tree.simbolos[0] == "RW_IF":
                if len(tree.children) == 7:
                    self.cgen(tree.children[2], file)
                    file.write("addiu $t1 $zero 1\n")
                    file.write("beq $a0 $t1 true_branch" + str(qtd_true_branch) + "\n")
                    file.write("false_branch" + str(qtd_false_branch) + ":\n")
                    self.cgen(tree.children[4], file)
                    file.write("j end_if" + str(qtd_endif_branch) + "\n")
                    file.write("true_branch" + str(qtd_true_branch) + ":\n")
                    self.cgen(tree.children[6], file)
                    file.write("end_if" + str(qtd_endif_branch) + ":\n")
                    qtd_false_branch += 1
                    qtd_true_branch += 1
                    qtd_endif_branch += 1
                elif len(tree.children) == 5:
                    self.cgen(tree.children[2], file)
                    file.write("addiu $t1 $zero 1\n")
                    file.write("beq $a0 $t1 true_branch" + str(qtd_true_branch) + "\n")
                    file.write("j end_if" + str(qtd_endif_branch) + "\n")
                    file.write("true_branch" + str(qtd_true_branch) + ":\n")
                    self.cgen(tree.children[4], file)
                    file.write("end_if" + str(qtd_endif_branch) + ":\n")
                    qtd_true_branch += 1
                    qtd_endif_branch += 1
            elif tree.simbolos[0] == "RW_SOUT":
                self.cgen(tree.children[2], file)
                file.write("li $v0 1\n")
                file.write("syscall\n")
            elif tree.simbolos[0] == "RW_WHILE":
                file.write("while%s:\n" % qtd_while)
                self.cgen(tree.children[2], file)
                file.write("beq $a0 $zero endWhile%s\n" % qtd_while)
                self.cgen(tree.children[4], file)
                file.write("j while%s\n" % qtd_while)
                qtd_while += 1
            elif tree.simbolos[1] == "cmd_r":
                self.cgen(tree.children[1], file)
        elif tree.producao == "cmd_r" or tree.producao == "var_r" or tree.producao == "metodo_r" or tree.producao == "classe_r":
            if len(tree.children) > 0:
                self.cgen(tree.children[0], file)
                self.cgen(tree.children[1], file)
        elif tree.producao == "params_o":
            if tree.simbolos[0] == "params":
                self.cgen(tree.children[0], file)
        elif tree.producao == "pexp":
            if tree.simbolos[0] == "ID":
                class_call_ref = tree.children[0].rule
            elif tree.simbolos[0] == "RW_THIS":
                class_call_ref = this_ref
            elif tree.simbolos[0] == "RW_NEW":
                class_call_ref = tree.children[1].rule
            elif tree.simbolos[0] == "LPAREN":
                self.cgen(tree.children[1], file)
            elif tree.simbolos[0] == "pexp":
                if len(tree.children) == 6:
                    self.cgen(tree.children[0], file)
                    nome_func = tree.children[2].rule
                    file.write("sw $fp 0($sp)\n")
                    file.write("addiu $sp $sp -4\n")
                    i = tree.children[4]
                    if i.simbolos[0] != "empty":
                        i = i.children[0]
                        self.cgen(i, file)
                        file.write("sw $a0 0($sp)\n")
                        file.write("addiu $sp $sp -4\n")
                        i = i.children[1]
                        while i.simbolos[0] != "empty":
                            self.cgen(i.children[2], file)
                            file.write("sw $a0 0($sp)\n")
                            file.write("addiu $sp $sp -4\n")
                            i = i.children[0]
                    file.write("sw $a0 0($sp)\n")
                    file.write("addiu $sp $sp -4\n")
                    file.write("jal %s.%s_entry\n" % (class_call_ref, nome_func))
                    class_call_ref = ""
                # elif len(tree.children) == 3:
                #     # vai ser similar ao caso com 6 acima em alguns pontos
        elif tree.producao == "metodo":
            # public TIPO id lparen PARAMS_O rparen lcurly VAR_R CMD_R return EXP P_SEMICOLON rcurly
            # PARAMS_O -> PARAMS | Ɛ
            # PARAMS -> TIPO id TIPO_R
            # TIPO_R -> TIPO_R P_COMMA TIPO ID | Ɛ
            # o que fazer com VAR_R?
            z = 0

            i = tree.children[4]
            if i.simbolos[0] != "empty":
                i = i.children[0].children[2]
                z += 1
                while i.simbolos[0] != "empty":
                    i = i.children[0]
                    z += 1
            file.write(self.getNomeMetodo(tree))
            file.write("move $fp $sp\n")
            file.write("sw $ra 0($sp)\n")
            file.write("addiu $sp $sp -4\n")
            self.cgen(tree.children[8], file)
            self.cgen(tree.children[10], file)
            file.write("lw $ra 4($sp)\n")
            file.write("addiu $sp $sp " + str(4 * z + 8) + "\n")
            file.write("lw $fp 0($sp)\n")
            file.write("jr $ra\n")

        else:
            for i in tree.children:
                self.cgen(i, file)

    def getNomeMetodo(self, node):
        nomeClasse = node.parent.parent.children[1].rule
        return "%s.%s_entry:\n" % (nomeClasse, node.children[2].rule)
