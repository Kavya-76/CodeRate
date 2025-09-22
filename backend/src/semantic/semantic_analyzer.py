# semantic/semantic_analyzer.py
import ast

class SemanticAnalyzer(ast.NodeVisitor):
    """
    Visits AST nodes to perform semantic checks, such as checking for
    undefined variables.
    """
    def __init__(self):
        # --- THIS IS THE FIX ---
        # A set of common built-in functions and types.
        built_in_names = {
            'print', 'len', 'range', 'int', 'str', 'list', 
            'dict', 'set', 'tuple', 'abs', 'max', 'min', 'sum'
        }
        # The global scope (the first item in our scope stack)
        # now starts pre-populated with these built-in names.
        self.scopes = [{name: 'BUILTIN' for name in built_in_names}]
        self.errors = []
        # --- END OF FIX ---

    def visit_FunctionDef(self, node):
        # Define the function's name in the current (outer) scope.
        self.scopes[-1][node.name] = 'FUNCTION'
        
        # Create a new, empty scope for the function's body.
        self.scopes.append({})
        
        # Add all function arguments to this new inner scope.
        for arg in node.args.args:
            self.scopes[-1][arg.arg] = 'VARIABLE'
            
        # Visit all nodes inside the function.
        self.generic_visit(node)
        
        # Once we're done with the function, pop its scope off the stack.
        self.scopes.pop()

    def visit_Assign(self, node):
        # First, visit the right-hand side of the assignment to ensure
        # any variables used there are already defined.
        self.visit(node.value)

        # Then, define the new variable(s) in the current scope.
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.scopes[-1][target.id] = 'VARIABLE'

    def visit_Name(self, node):
        # This method is called whenever a variable name is used.
        # We only care when a variable is being loaded/read.
        if isinstance(node.ctx, ast.Load):
            found = False
            # Check for the name in all scopes, from innermost to outermost.
            for scope in reversed(self.scopes):
                if node.id in scope:
                    found = True
                    break
            
            # --- SIMPLIFIED CHECK ---
            # If the name was not found in any scope (including our
            # built-ins), then it's an undefined variable.
            if not found:
                self.errors.append(
                    f"Semantic Error: Name '{node.id}' is not defined."
                )
        
        # Continue visiting other nodes.
        self.generic_visit(node)

def perform_semantic_analysis(ast_tree):
    """
    Performs semantic analysis on the given official AST.
    Returns a list of errors found.
    """
    if not ast_tree:
        return ["No AST provided for semantic analysis."]
    
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast_tree)
    return analyzer.errors