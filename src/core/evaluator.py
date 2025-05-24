# src/core/evaluator.py

from lexer.lexer import perform_lexical_analysis
from parser.parser import perform_syntax_analysis
from semantic.semantic_analyzer import perform_semantic_analysis
from features.feature_extractor import extract_features
from ml_model.model import predict_score

def evaluate_code(code: str):
    try:
        # Step 1: Lexical Analysis (for validation and debugging)
        tokens = perform_lexical_analysis(code)
        print("Lexical analysis done")

        if not tokens:
            return {
                "status": "error",
                "stage": "lexical",
                "message": "Lexical analysis failed. No valid tokens found."
            }

        # Step 2: Syntax Analysis (pass the original code, not tokens)
        try:
            ast = perform_syntax_analysis(code)  # ✅ Pass code string, not tokens
            print("AST generation done")
            
            # Optional: Print tokens for debugging
            print("Tokens found:")
            for token in tokens:
                print(token)
                
        except SyntaxError as se:
            return {
                "status": "error",
                "stage": "syntax",
                "message": str(se)
            }

        # Step 3: Semantic Analysis
        semantic_errors = perform_semantic_analysis(ast)
        if semantic_errors:
            return {
                "status": "error",
                "stage": "semantic",
                "message": "Semantic analysis failed.",
                "errors": semantic_errors
            }

        # Step 4: Feature Extraction
        features = extract_features(ast)

        # Step 5: ML Scoring
        try:
            score = predict_score(features)
        except Exception as ml_error:
            return {
                "status": "error",
                "stage": "ml",
                "message": f"ML prediction failed: {str(ml_error)}"
            }

        return {
            "status": "success",
            "score": score,
            "features": features
        }

    except Exception as e:
        return {
            "status": "error",
            "stage": "general",
            "message": "Unexpected error occurred.",
            "details": str(e)
        }