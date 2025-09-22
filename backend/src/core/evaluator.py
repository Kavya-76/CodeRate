# core/evaluator.py

import ast
from lexer.lexer import perform_lexical_analysis
from parser.parser import perform_syntax_analysis
from semantic.semantic_analyzer import perform_semantic_analysis
from features.feature_extractor import extract_features
from ml_model.model import predict_score
# I'm assuming format_ast_tree exists, if not, this can be a simple str()
# For now, let's create a placeholder if it's missing.
try:
    from utils.formatting import format_ast_tree
except ImportError:
    def format_ast_tree(node):
        return ast.dump(node) # A simple fallback representation

def evaluate_code(code: str, debug: bool = False):
    try:
        # Lexical Analysis
        tokens = perform_lexical_analysis(code)
        if not tokens:
            return {
                "status": "error", "stage": "lexical",
                "message": "Lexical analysis failed. No valid tokens found."
            }

        # Syntax Analysis
        ast_obj = perform_syntax_analysis(code) # Renamed to ast_obj to avoid conflict

        # Semantic Analysis
        semantic_errors = perform_semantic_analysis(ast_obj)
        if semantic_errors:
            return {
                "status": "error",
                "stage": "semantic",
                "message": "Semantic analysis failed.",
                "errors": semantic_errors,
                "tokens": tokens,  # <-- FIX 1: Use the 'tokens' list directly
                "ast_tree": format_ast_tree(ast_obj)
            }

        # Feature Extraction
        features = extract_features(ast_obj)

        # ML Score
        score = predict_score(features)

        # This is the successful return
        return {
            "status": "success",
            "tokens": tokens,  # <-- FIX 2: Use the 'tokens' list directly
            "ast_tree": format_ast_tree(ast_obj),
            "features": features,
            "score": score,
            "debug_info": {
                "raw_ast": ast.dump(ast_obj),
                "raw_tokens": tokens # <-- FIX 3: Also simplified here
            } if debug else None
        }

    except SyntaxError as se:
        return {
            "status": "error",
            "stage": "syntax",
            "message": f"Invalid Python syntax: {se.msg} at line {se.lineno}",
        }
    except Exception as e:
        # This catches errors from the ML model or other unexpected issues
        # and now also correctly handles the token formatting.
        # We need to re-run analysis up to the failure point to get partial data.
        
        # A simple general error for now to avoid complexity.
        # The original code's error handling here was complex and might re-error.
        return {
            "status": "error",
            "stage": "general",
            "message": "An unexpected error occurred during evaluation.",
            "details": str(e)
        }