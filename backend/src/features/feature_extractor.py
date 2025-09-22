# features/feature_extractor.py
import ast

class FeatureVisitor(ast.NodeVisitor):
    """
    A dedicated class to visit AST nodes and collect code metrics.
    Using NodeVisitor is the standard, robust way to traverse the official AST.
    """
    def __init__(self):
        # Raw counters that we'll increment during traversal
        self.function_count = 0
        self.total_params = 0
        self.function_call_count = 0
        self.binary_operator_count = 0
        # We use a set to automatically handle unique variable names
        self.assigned_variables = set()

    def visit_FunctionDef(self, node):
        """Called for every function definition."""
        self.function_count += 1
        self.total_params += len(node.args.args)
        # We must call generic_visit() to ensure we visit nodes inside this function
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Called for assignment statements like 'x = 5'."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Add the variable name to our set of unique variables
                self.assigned_variables.add(target.id)
        self.generic_visit(node)
        
    def visit_AugAssign(self, node):
        """Called for augmented assignments like 'x += 1'."""
        if isinstance(node.target, ast.Name):
            self.assigned_variables.add(node.target.id)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """Called for binary operators like '+', '-', '*', '/'."""
        self.binary_operator_count += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        """Called for any function call."""
        self.function_call_count += 1
        self.generic_visit(node)


def extract_features(ast_tree):
    """
    Initializes the visitor, traverses the given AST, and returns the
    calculated features in a dictionary.
    
    Args:
        ast_tree: A valid AST object from ast.parse().
        
    Returns:
        A dictionary containing the code metrics.
    """
    # 1. Create an instance of our visitor
    visitor = FeatureVisitor()
    
    # 2. Start the traversal from the root of the tree
    visitor.visit(ast_tree)
    
    # 3. Calculate final metrics after the traversal is complete
    if visitor.function_count > 0:
        avg_param_count = round(visitor.total_params / visitor.function_count, 2)
    else:
        avg_param_count = 0

    # 4. Assemble the final features dictionary
    features = {
        "function_count": visitor.function_count,
        "variable_count": len(visitor.assigned_variables),
        "binary_operator_count": visitor.binary_operator_count,
        "avg_param_count": avg_param_count,
        "function_call_count": visitor.function_call_count
    }
    
    return features