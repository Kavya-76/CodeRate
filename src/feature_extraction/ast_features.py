import ast

def extract_ast_features(code):
    loop_count = 0
    function_call_count = 0
    recursion = False
    nesting_depth = 0
    branches = 0

    def calculate_depth(node, current=0):
        nonlocal nesting_depth
        if isinstance(node, (ast.If, ast.For, ast.While, ast.FunctionDef)):
            current += 1
            nesting_depth = max(nesting_depth, current)
        for child in ast.iter_child_nodes(node):
            calculate_depth(child, current)

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                loop_count += 1
            elif isinstance(node, ast.Call):
                function_call_count += 1
                if isinstance(node.func, ast.Name) and node.func.id in code:
                    recursion = True
            elif isinstance(node, ast.If):
                branches += 1
        calculate_depth(tree)
    except Exception:
        pass

    return loop_count, function_call_count, recursion, nesting_depth, branches
