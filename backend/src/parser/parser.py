# parser/parser.py
import ast

def perform_syntax_analysis(code: str):
    """
    Performs syntax analysis using Python's built-in ast module.
    This replaces the complex PLY yacc parser.
    It returns the official Python Abstract Syntax Tree.
    """
    try:
        # ast.parse() is the definitive Python parser.
        # It performs both tokenization and parsing in one step internally.
        # If the syntax is invalid, it raises a SyntaxError.
        tree = ast.parse(code)
        return tree
    except SyntaxError as e:
        # Re-raise the error so the evaluator can catch it and report it.
        raise e