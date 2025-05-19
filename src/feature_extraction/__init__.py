from .lexer_features import extract_lexer_features
from .ast_features import extract_ast_features
from .complexity_features import estimate_complexity

def extract_features(code):
    token_count, keyword_count, operator_count, variables = extract_lexer_features(code)
    loop_count, function_call_count, recursion, nesting_depth, branches = extract_ast_features(code)
    time_complexity, space_complexity = estimate_complexity(loop_count, int(recursion), len(variables))

    return [
        token_count,
        keyword_count,
        operator_count,
        len(variables),
        loop_count,
        function_call_count,
        int(recursion),
        nesting_depth,
        branches,
        time_complexity,
        space_complexity
    ]