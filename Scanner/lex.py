import ply.lex as lexer
from pathlib import Path
import re

LOOKAHEAD = False

reserved = {
    'if': 'RW_IF',
    'else': 'RW_ELSE',
    'while': 'RW_WHILE',
    'boolean': 'RW_BOOLEAN',
    'class': 'RW_CLASS',
    'extends': 'RW_EXTENDS',
    'public': 'RW_PUBLIC',
    'static': 'RW_STATIC',
    'void': 'RW_VOID',
    'main': 'RW_MAIN',
    'return': 'RW_RETURN',
    'int': 'RW_INT',
    'System.out.println': 'RW_SOUT',
    'this': 'RW_THIS',
    'true': 'RW_TRUE',
    'false': 'RW_FALSE',
    'new': 'RW_NEW',
    'null': 'RW_NULL',
    'length': 'RW_LENGTH',
    'String': 'RW_STRING'
}

tokens = [
             "WHITESPACE",
             "COMMENT",
             "LPAREN",
             "RPAREN",
             "LBRACK",
             "RBRACK",
             "LCURLY",
             "RCURLY",
             'P_SEMICOLON',
             'P_COMMA',
             'P_POINT',
             "OP_ATTR",
             "OP_GREATER",
             "OP_LESSER",
             "OP_GREATER_EQ",
             "OP_LESSER_EQ",
             "OP_EQUAL",
             "OP_NOT_EQUAL",
             "OP_MINUS",
             "OP_PLUS",
             "OP_MULTIPLY",
             "OP_DIVISION",
             "OP_AND",
             "OP_NOT",
             "ID",
             "NUMBER"
         ] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_P_SEMICOLON = r';'
t_P_COMMA = r'\,'
t_P_POINT = r'\.'
t_OP_ATTR = r'='
t_OP_GREATER = r'>'
t_OP_LESSER = r'<'
t_OP_GREATER_EQ = r'>='
t_OP_LESSER_EQ = r'<='
t_OP_EQUAL = r'=='
t_OP_NOT_EQUAL = r'!='
t_OP_MINUS = r'\-'
t_OP_PLUS = r'\+'
t_OP_MULTIPLY = r'\*'
t_OP_DIVISION = r'/'
t_OP_AND = r'&&'
t_OP_NOT = r'!'

def t_COMMENT(t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    pass


def t_WHITESPACE(t):
    r'\s'
    pass


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'(System\.out\.println)|([a-zA-Z_][a-zA-Z_0-9]*)'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_error(t):
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

#entrada = "System.out.println"

#print(re.search(entrada, Path("entrada.txt").read_text()))

entrada = Path("entrada.txt").read_text()

lex = lexer.lex()
lex.input(entrada)

while True:
    token = lex.token()
    if not token:
        break
    print(token)
