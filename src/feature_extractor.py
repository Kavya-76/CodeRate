import tokenize
import ast
from io import BytesIO

def extract_features(code: str) -> list:
    features = {}

    # Lexical analysis
    tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
    features['num_tokens'] = len([t for t in tokens if t.type not in [tokenize.ENCODING, tokenize.ENDMARKER]])
    features['num_keywords'] = sum(1 for t in tokens if t.type == tokenize.NAME and t.string in {'for', 'if', 'def', 'return', 'while', 'try', 'except', 'with', 'class'})
    features['num_operators'] = sum(1 for t in tokens if t.string in {'+', '-', '*', '/', '**', '=', '==', '<', '>', '>=', '<='})

    # Syntactic analysis
    tree = ast.parse(code)
    features['num_func_defs'] = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))
    features['num_for_loops'] = sum(isinstance(n, ast.For) for n in ast.walk(tree))
    features['num_if_statements'] = sum(isinstance(n, ast.If) for n in ast.walk(tree))
    features['num_calls'] = sum(isinstance(n, ast.Call) for n in ast.walk(tree))
    features['num_classes'] = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))

    return list(features.values())