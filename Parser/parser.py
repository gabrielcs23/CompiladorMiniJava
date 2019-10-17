import ply.yacc as yacc
import Scanner.lex
from Scanner.lex import tokens

def p_prog(p):
    """prog : main classe_r"""


def p_classe_r(p):
    """classe_r : classe_r classe
                | empty"""


def p_main(p):
    """main : RW_CLASS ID LCURLY RW_PUBLIC RW_STATIC RW_VOID RW_MAIN LPAREN RW_STRING LBRACK RBRACK ID RPAREN LCURLY cmd RCURLY RCURLY"""


def p_classe(p):
    """classe : RW_CLASS ID extends_o LCURLY var_r metodo_r RCURLY"""


def p_extends_o(p):
    """extends_o    : RW_EXTENDS ID
                    | empty"""


def p_var(p):
    """var : tipo ID P_SEMICOLON"""


def p_metodo(p):
    """metodo : RW_PUBLIC tipo ID LPAREN params_o RPAREN LCURLY var_r cmd_r RW_RETURN exp P_SEMICOLON RCURLY"""


def p_metodo_r(p):
    """metodo_r : metodo_r metodo
                | empty"""


def p_var_r(p):
    """var_r    : var_r var
                | empty """


def p_cmd_r(p):
    """cmd_r    : cmd_r cmd
                | empty"""


def p_params(p):
    """params : tipo ID tipo_r"""


def p_tipo_r(p):
    """tipo_r   : tipo_r P_COMMA tipo ID
                | ID"""


def p_params_o(p):
    """params_o : params
                | empty"""


def p_tipo(p):
    """tipo : RW_INT LBRACK RBRACK
            | RW_BOOLEAN
            | RW_INT
            | ID"""


def p_cmd(p):
    """cmd  : LCURLY cmd_r RCURLY
            | RW_IF LPAREN exp RPAREN cmd
            | RW_IF LPAREN exp RPAREN cmd RW_ELSE cmd
            | RW_WHILE LPAREN exp RPAREN cmd
            | RW_SOUT LPAREN exp RPAREN P_SEMICOLON
            | ID OP_ATTR exp P_SEMICOLON
            | ID LBRACK exp RBRACK OP_ATTR exp P_SEMICOLON"""


def p_exp(p):
    """exp  : exp OP_AND rexp
            | rexp"""


def p_rexp(p):
    """rexp : rexp OP_LESSER aexp
            | rexp OP_EQUAL aexp
            | rexp OP_NOT_EQUAL aexp
            | aexp """


def p_aexp(p):
    """aexp : aexp OP_PLUS mexp
            | aexp OP_MINUS mexp
            | mexp"""


def p_mexp(p):
    """mexp : mexp OP_MULTIPLY sexp
            | mexp OP_DIVISION sexp
            | sexp"""


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


def p_pexp(p):
    """pexp : ID
            | RW_THIS
            | RW_NEW ID LPAREN RPAREN
            | LPAREN exp RPAREN
            | pexp P_POINT ID
            | pexp P_POINT ID LPAREN exps_o RPAREN"""


def p_exps_o(p):
    """exps_o : exps
            | empty"""


def p_exps(p):
    """exps : exp exp_r"""


def p_exp_r(p):
    """exp_r : exp P_COMMA exp
             | empty"""


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    print(p)


yacc.yacc()
