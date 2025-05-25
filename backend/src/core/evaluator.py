from lexer.lexer import perform_lexical_analysis
from parser.parser import perform_syntax_analysis
from semantic.semantic_analyzer import perform_semantic_analysis
from features.feature_extractor import extract_features
from ml_model.model import predict_score
from utils.formatting import format_ast_tree  # Make sure to import it correctly

def evaluate_code(code: str, debug: bool = False):
    try:
        # Lexical Analysis
        tokens = perform_lexical_analysis(code)
        if not tokens:
            return {
                "status": "error",
                "stage": "lexical",
                "message": "Lexical analysis failed. No valid tokens found."
            }

        # Syntax Analysis
        try:
            ast = perform_syntax_analysis(code)
        except SyntaxError as se:
            return {
                "status": "error",
                "stage": "syntax",
                "message": str(se)
            }

        # Semantic Analysis
        semantic_errors = perform_semantic_analysis(ast)
        if semantic_errors:
            return {
                "status": "error",
                "stage": "semantic",
                "message": "Semantic analysis failed.",
                "errors": semantic_errors,
                "tokens": [f"{t.type}: {t.value}" for t in tokens],
                "ast_tree": format_ast_tree(ast)
            }

        # Feature Extraction
        features = extract_features(ast)

        # ML Score
        try:
            score = predict_score(features)
        except Exception as ml_error:
            return {
                "status": "error",
                "stage": "ml",
                "message": f"ML prediction failed: {str(ml_error)}",
                "tokens": [f"{t.type}: {t.value}" for t in tokens],
                "ast_tree": format_ast_tree(ast),
                "features": features
            }

        return {
            "status": "success",
            "tokens": [f"{t.type}: {t.value}" for t in tokens],
            "ast_tree": format_ast_tree(ast),
            "features": features,
            "score": score,
            "debug_info": {
                "raw_ast": repr(ast),
                "raw_tokens": [str(t) for t in tokens]
            } if debug else None
        }

    except Exception as e:
        return {
            "status": "error",
            "stage": "general",
            "message": "Unexpected error occurred.",
            "details": str(e)
        }
