# src/parser/parser.py
import ply.yacc as yacc
from lexer import lexer as lexer_module  # Import the lexer module
import sys

# Get tokens from the lexer module
tokens = lexer_module.tokens

# A simple AST structure
class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children or []
        self.value = value

    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, {self.children})"

# Grammar rules
def p_program(p):
    '''program : statements'''
    p[0] = ASTNode("Program", children=p[1])

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement_func(p):
    '''statement : DEF IDENTIFIER LPAREN params RPAREN COLON NEWLINE'''
    p[0] = ASTNode("FunctionDecl", value=p[2], children=p[4])

def p_statement_expr(p):
    '''statement : expression
                 | expression NEWLINE'''
    p[0] = ASTNode("ExpressionStatement", children=[p[1]])

def p_params_multiple(p):
    '''params : params COMMA IDENTIFIER'''
    p[0] = p[1] + [ASTNode("Param", value=p[3])]

def p_params_single(p):
    '''params : IDENTIFIER'''
    p[0] = [ASTNode("Param", value=p[1])]

def p_params_empty(p):
    '''params : '''
    p[0] = []

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ASTNode("BinOp", children=[p[1], p[3]], value=p[2])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ASTNode("Number", value=p[1])

def p_expression_var(p):
    '''expression : IDENTIFIER'''
    p[0] = ASTNode("Variable", value=p[1])

def p_expression_call(p):
    '''expression : IDENTIFIER LPAREN args RPAREN'''
    p[0] = ASTNode("FunctionCall", value=p[1], children=p[3])

def p_expression_print(p):
    '''expression : PRINT LPAREN args RPAREN'''
    p[0] = ASTNode("PrintCall", children=p[3])

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = ASTNode("String", value=p[1])

def p_args_multiple(p):
    '''args : args COMMA expression'''
    p[0] = p[1] + [p[3]]

def p_args_single(p):
    '''args : expression'''
    p[0] = [p[1]]

def p_args_empty(p):
    '''args : '''
    p[0] = []

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        raise SyntaxError("Syntax error at EOF")

# Entry function
def perform_syntax_analysis(code):
    # Create parser using current module (where the grammar rules are defined)
    parser = yacc.yacc(module=sys.modules[__name__])
    # Use the lexer from the lexer module
    lexer_module.lexer.input(code)
    result = parser.parse(code, lexer=lexer_module.lexer)
    return result