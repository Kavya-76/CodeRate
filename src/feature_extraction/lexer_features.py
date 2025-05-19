import ply.lex as lex

# Token list
reserved = {
    'def': 'DEF',
    'return': 'RETURN',
    'for': 'FOR',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT'
}

tokens = [
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'EQUALS', 'NAME', 'NEWLINE'
] + list(reserved.values())


# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_NEWLINE = r'\n'
t_ignore = ' \t'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    t.lexer.skip(1)

def extract_lexer_features(code):
    lexer = lex.lex()
    lexer.input(code)
    token_count = 0
    keyword_count = 0
    operator_count = 0
    variables = set()

    while True:
        tok = lexer.token()
        if not tok:
            break
        token_count += 1
        if tok.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS']:
            operator_count += 1
        if tok.type in ['DEF', 'RETURN', 'FOR', 'WHILE', 'IF', 'ELSE']:
            keyword_count += 1
        if tok.type == 'NAME':
            variables.add(tok.value)

    return token_count, keyword_count, operator_count, variables