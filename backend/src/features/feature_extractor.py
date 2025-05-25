# src/features/feature_extractor.py

def extract_features(ast):
    """
    Traverses the AST to collect code metrics:
    - number of functions
    - number of variables
    - number of binary operations
    - average function parameter count
    - number of function calls
    """

    features = {
        "function_count": 0,
        "variable_count": 0,
        "binop_count": 0,
        "avg_param_count": 0.0,
        "function_call_count": 0
    }

    param_counts = []

    def traverse(node):
        if node.type == "FunctionDecl":
            features["function_count"] += 1
            param_counts.append(len(node.children))

        elif node.type == "Variable":
            features["variable_count"] += 1

        elif node.type == "BinOp":
            features["binop_count"] += 1
            for child in node.children:
                traverse(child)

        elif node.type == "FunctionCall":
            features["function_call_count"] += 1
            for arg in node.children:
                traverse(arg)

        elif node.type == "ExpressionStatement":
            for child in node.children:
                traverse(child)

        elif node.type == "Program":
            for child in node.children:
                traverse(child)

        elif node.type == "Number":
            pass

        elif node.type == "Param":
            pass

        else:
            for child in node.children:
                traverse(child)

    traverse(ast)

    if param_counts:
        features["avg_param_count"] = sum(param_counts) / len(param_counts)

    return features
