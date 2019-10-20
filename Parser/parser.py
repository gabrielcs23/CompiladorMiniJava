from pathlib import Path

import ply.yacc as yacc
import Scanner.lex
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
    p[0] = ("prog", p[1], p[2])


def p_classe_r(p):
    """classe_r : classe_r classe
                | empty"""
    if len(p) == 3:
        p[0] = ("classe_r", p[1], p[2])
    else:
        p[0] = ("classe_r", p[1])


def p_main(p):
    """main : RW_CLASS ID LCURLY RW_PUBLIC RW_STATIC RW_VOID RW_MAIN LPAREN RW_STRING LBRACK RBRACK ID RPAREN LCURLY cmd RCURLY RCURLY"""
    p[0] = ("main", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17])


def p_classe(p):
    """classe : RW_CLASS ID extends_o LCURLY var_r metodo_r RCURLY"""
    p[0] = ("classe", p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_extends_o(p):
    """extends_o    : RW_EXTENDS ID
                    | empty"""
    if len(p) == 3:
        p[0] = ("extends_o", p[1], p[2])
    else:
        p[0] = ("extends_o", p[1])


def p_var(p):
    """var : tipo ID P_SEMICOLON"""
    p[0] = ("var", p[1], p[2], p[3])


def p_metodo(p):
    """metodo : RW_PUBLIC tipo ID LPAREN params_o RPAREN LCURLY var_r cmd_r RW_RETURN exp P_SEMICOLON RCURLY"""
    p[0] = ("metodo", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13])


def p_metodo_r(p):
    """metodo_r : metodo_r metodo
                | empty"""
    if len(p) == 3:
        p[0] = ("metodo_r", p[1], p[2])
    else:
        p[0] = ("metodo_r", p[1])


def p_var_r(p):
    """var_r    : var_r var
                | empty """
    if len(p) == 3:
        p[0] = ("var_r", p[1], p[2])
    else:
        p[0] = ("var_r", p[1])


def p_cmd_r(p):
    """cmd_r    : cmd cmd_r
                | empty"""
    if len(p) == 3:
        p[0] = ("cmd_r", p[1], p[2])
    else:
        p[0] = ("cmd_r", p[1])


def p_params(p):
    """params : tipo ID tipo_r"""
    p[0] = ("params", p[1], p[2], p[3])


def p_tipo_r(p):
    """tipo_r   : tipo_r P_COMMA tipo ID
                | empty"""
    if len(p) == 5:
        p[0] = ("tipo_r", p[1], p[2], p[3], p[4])
    else:
        p[0] = ("tipo_r", p[1])


def p_params_o(p):
    """params_o : params
                | empty"""
    p[0] = ("params_o", p[1])


def p_tipo(p):
    """tipo : RW_INT LBRACK RBRACK
            | RW_BOOLEAN
            | RW_INT
            | ID"""
    if len(p) == 4:
        p[0] = ("tipo", p[1], p[2], p[3])
    else:
        p[0] = ("tipo", p[1])


def p_cmd(p):
    """cmd  : LCURLY cmd_r RCURLY
            | RW_IF LPAREN exp RPAREN cmd
            | RW_IF LPAREN exp RPAREN cmd RW_ELSE cmd
            | RW_WHILE LPAREN exp RPAREN cmd
            | RW_SOUT LPAREN exp RPAREN P_SEMICOLON
            | ID OP_ATTR exp P_SEMICOLON
            | ID LBRACK exp RBRACK OP_ATTR exp P_SEMICOLON"""
    # print(p[1])
    if len(p) == 3:
        p[0] = ("cmd", p[1], p[2])
    elif len(p) == 6:
        p[0] = ("cmd", p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 8:
        p[0] = ("cmd", p[1], p[2], p[3], p[4], p[5], p[6], p[7])
    elif len(p) == 5:
        p[0] = ("cmd", p[1], p[2], p[3], p[4])


def p_exp(p):
    """exp  : exp OP_AND rexp
            | rexp"""
    if len(p) == 4:
        p[0] = ("exp", p[1], p[2], p[3])
    else:
        p[0] = ("exp", p[1])


def p_rexp(p):
    """rexp : rexp OP_LESSER aexp
            | rexp OP_EQUAL aexp
            | rexp OP_NOT_EQUAL aexp
            | aexp """
    if len(p) == 4:
        p[0] = ("rexp", p[1], p[2], p[3])
    else:
        p[0] = ("rexp", p[1])


def p_aexp(p):
    """aexp : aexp OP_PLUS mexp
            | aexp OP_MINUS mexp
            | mexp"""
    if len(p) == 4:
        p[0] = ("aexp", p[1], p[2], p[3])
    else:
        p[0] = ("aexp", p[1])


def p_mexp(p):
    """mexp : mexp OP_MULTIPLY sexp
            | mexp OP_DIVISION sexp
            | sexp"""
    if len(p) == 4:
        p[0] = ("mexp", p[1], p[2], p[3])
    else:
        p[0] = ("mexp", p[1])


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
    if len(p) == 3:
        p[0] = ("sexp", p[1], p[2])
    elif len(p) == 2:
        p[0] = ("sexp", p[1])
    elif len(p) == 6:
        p[0] = ("sexp", p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 4:
        p[0] = ("sexp", p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = ("sexp", p[1], p[2], p[3], p[4])


def p_pexp(p):
    """pexp : ID
            | RW_THIS
            | RW_NEW ID LPAREN RPAREN
            | LPAREN exp RPAREN
            | pexp P_POINT ID
            | pexp P_POINT ID LPAREN exps_o RPAREN"""
    if len(p) == 2:
        p[0] = ("pexp", p[1])
    elif len(p) == 7:
        p[0] = ("pexp", p[1], p[2], p[3], p[4], p[5], p[6])
    elif len(p) == 4:
        p[0] = ("pexp", p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = ("pexp", p[1], p[2], p[3], p[4])


def p_exps_o(p):
    """exps_o : exps
            | empty"""
    p[0] = ("exps_o", p[1])


def p_exps(p):
    """exps : exp exp_r"""
    p[0] = ("exps", p[1], p[2])


def p_exp_r(p):
    """exp_r : exp_r P_COMMA exp
             | empty"""
    if len(p) == 4:
        p[0] = ("exp_r", p[1], p[2], p[3])
    else:
        p[0] = ("exp_r", p[1])


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    if not p:
        print("Unexpected EOF")
        return
    print("Syntax error at line %d in token %s. Bad expression" % (p.lineno - lines, p.type))
    # Just discard the token and continue to parse
    parser.errok()


parser = yacc.yacc(debug=True)
s = Path("entrada.txt").read_text()
parserOut = parser.parse(s)
if parserOut:
    print(parserOut)
