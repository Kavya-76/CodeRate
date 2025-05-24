# src/lexer/lexer.py

import ply.lex as lex
import sys

# List of token names
tokens = (
    'NUMBER', 'IDENTIFIER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN', 'COLON', 'NEWLINE',
    'STRING', 'COMMA'
)

# Reserved keywords
reserved = {
    'def': 'DEF',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'import': 'IMPORT',
    'from': 'FROM',
    'as': 'AS',
    'class': 'CLASS',
    'print': 'PRINT',
    'in': 'IN',
    'range': 'RANGE',
    'True': 'TRUE',
    'False': 'FALSE',
    'None': 'NONE'
}

tokens = tokens + tuple(reserved.values())

# Regular expression rules for simple tokens
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_EQUALS   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COLON    = r':'
t_COMMA    = r','

t_ignore   = ' \t'

# Complex token rules
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

def t_STRING(t):
    r'(\".*?\"|\'.*?\')'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t  # Return token if grammar expects it

def t_comment(t):
    r'\#.*'
    pass  # Ignore comments

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Build the lexer
lexer = lex.lex()

def perform_lexical_analysis(code):
    print("The code is ",code)
    lexer = lex.lex(module=sys.modules[__name__])
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    return tokens_list

# Test function
if __name__ == "__main__":
    # Test the lexer
    test_code = """
def hello():
    print("Hello, World!")
    return 42
"""
    
    try:
        tokens = perform_lexical_analysis(test_code)
        for token in tokens:
            print(token)
    except Exception as e:
        print(f"Error: {e}")