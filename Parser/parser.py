from pathlib import Path

import ply.yacc as yacc
from ply.lex import LexToken

import Scanner.lex
from Parser.Tree import Tree
from Scanner.lex import tokens

lines = 0
blank_lines = 0
with open('entrada.txt') as f:
    for line in f:
        if line.isspace():
            blank_lines = blank_lines + 1
        elif '\n' in line:
            blank_lines = 1
        else:
            blank_lines = 0
        lines = lines + 1

if blank_lines == 0:
    lines = lines - 1


precedence = (
    ('left', 'RPAREN'),
    ('left', 'RW_ELSE'),
)


def p_prog(p):
    """prog : main classe_r"""
    p[0] = (get_rule(p), p[1:])


def p_classe_r(p):
    """classe_r : classe_r classe
                | empty"""
    p[0] = (get_rule(p), p[1:])


def p_main(p):
    """main : RW_CLASS ID LCURLY RW_PUBLIC RW_STATIC RW_VOID RW_MAIN LPAREN RW_STRING LBRACK RBRACK ID RPAREN LCURLY cmd RCURLY RCURLY"""
    p[0] = (get_rule(p), p[1:])


def p_classe(p):
    """classe : RW_CLASS ID extends_o LCURLY var_r metodo_r RCURLY"""
    p[0] = (get_rule(p), p[1:])


def p_extends_o(p):
    """extends_o    : RW_EXTENDS ID
                    | empty"""
    p[0] = (get_rule(p), p[1:])


def p_var(p):
    """var : tipo ID P_SEMICOLON"""
    p[0] = (get_rule(p), p[1:])


def p_metodo(p):
    """metodo : RW_PUBLIC tipo ID LPAREN params_o RPAREN LCURLY var_r cmd_r RW_RETURN exp P_SEMICOLON RCURLY"""
    p[0] = (get_rule(p), p[1:])


def p_metodo_r(p):
    """metodo_r : metodo_r metodo
                | empty"""
    p[0] = (get_rule(p), p[1:])


def p_var_r(p):
    """var_r    : var_r var
                | empty """
    p[0] = (get_rule(p), p[1:])


def p_cmd_r(p):
    """cmd_r    : cmd cmd_r
                | empty"""
    p[0] = (get_rule(p), p[1:])


def p_params(p):
    """params : tipo ID tipo_r"""
    p[0] = (get_rule(p), p[1:])


def p_tipo_r(p):
    """tipo_r   : tipo_r P_COMMA tipo ID
                | empty"""
    p[0] = (get_rule(p), p[1:])


def p_params_o(p):
    """params_o : params
                | empty"""
    p[0] = (get_rule(p), p[1:])


def p_tipo(p):
    """tipo : RW_INT LBRACK RBRACK
            | RW_BOOLEAN
            | RW_INT
            | ID"""
    p[0] = (get_rule(p), p[1:])


def p_cmd(p):
    """cmd  : LCURLY cmd_r RCURLY
            | RW_IF LPAREN exp RPAREN cmd
            | RW_IF LPAREN exp RPAREN cmd RW_ELSE cmd
            | RW_WHILE LPAREN exp RPAREN cmd
            | RW_SOUT LPAREN exp RPAREN P_SEMICOLON
            | ID OP_ATTR exp P_SEMICOLON
            | ID LBRACK exp RBRACK OP_ATTR exp P_SEMICOLON"""
    p[0] = (get_rule(p), p[1:])


def p_exp(p):
    """exp  : exp OP_AND rexp
            | rexp"""
    p[0] = (get_rule(p), p[1:])


def p_rexp(p):
    """rexp : rexp OP_LESSER aexp
            | rexp OP_EQUAL aexp
            | rexp OP_NOT_EQUAL aexp
            | aexp """
    p[0] = (get_rule(p), p[1:])


def p_aexp(p):
    """aexp : aexp OP_PLUS mexp
            | aexp OP_MINUS mexp
            | mexp"""
    p[0] = (get_rule(p), p[1:])


def p_mexp(p):
    """mexp : mexp OP_MULTIPLY sexp
            | mexp OP_DIVISION sexp
            | sexp"""
    p[0] = (get_rule(p), p[1:])


def p_sexp(p):
    """sexp : OP_NOT sexp
            | OP_MINUS sexp
            | RW_TRUE
            | RW_FALSE
            | RW_NULL
            | NUMBER
            | RW_NEW RW_INT LBRACK exp RBRACK
            | pexp P_POINT RW_LENGTH
            | pexp LBRACK exp RBRACK
            | pexp"""
    p[0] = (get_rule(p), p[1:])


def p_pexp(p):
    """pexp : ID
            | RW_THIS
            | RW_NEW ID LPAREN RPAREN
            | LPAREN exp RPAREN
            | pexp P_POINT ID
            | pexp P_POINT ID LPAREN exps_o RPAREN"""
    p[0] = (get_rule(p), p[1:])


def p_exps_o(p):
    """exps_o : exps
            | empty"""
    p[0] = (get_rule(p), p[1:])


def p_exps(p):
    """exps : exp exp_r"""
    p[0] = (get_rule(p), p[1:])


def p_exp_r(p):
    """exp_r : exp_r P_COMMA exp
             | empty"""
    p[0] = (get_rule(p), p[1:])


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if not p:
        print("Unexpected EOF")
        return
    print("Syntax error at line %d in token %s. Bad expression" % (p.lineno - lines, p.type))
    parser.errok()
    # Just discard the token and continue to parse
    while True:
        tok = parser.token()  # Get the next token
        if not tok or tok.type == 'RCURLY':
            while tok and tok.type == 'RCURLY':
                tok = parser.token()
            break
    parser.restart()


def get_rule(p: yacc.YaccProduction):
    rule = str(p.slice[0]) + " ->"
    for i in range(1, len(p)):
        if isinstance(p.slice[i], LexToken):
            rule += " " + str(p.slice[i].type)
        else:
            rule += " " + str(p.slice[i])
    return rule


def get_tree(parser_out):
    if parser_out is not None and not isinstance(parser_out, int) and not isinstance(parser_out, str):
        root = Tree(parser_out[0])
        if len(parser_out) > 1:
            for i in parser_out[1]:
                child = get_tree(i)
                if child is not None:
                    root.children.append(child)
    elif parser_out is not None:
        root = Tree(parser_out)
    else:
        root = None
    return root


parser = yacc.yacc(debug=True)
s = Path("entrada.txt").read_text()
parserOut = parser.parse(s)
if parserOut:
    tree = get_tree(parserOut)
    print(tree)
