# src/semantic/semantic_analyzer.py

class SemanticContext:
    def __init__(self):
        self.symbols = {}  # Stores variables/functions
        self.errors = []
        self.builtin_functions = {
            'print': {'type': 'builtin', 'params': -1},  # -1 means variable args
            'range': {'type': 'builtin', 'params': -1},
            'len': {'type': 'builtin', 'params': 1},
        }

    def define(self, name, value):
        if name in self.symbols:
            self.errors.append(f"Duplicate identifier: {name}")
        else:
            self.symbols[name] = value

    def resolve(self, name):
        if name not in self.symbols and name not in self.builtin_functions:
            self.errors.append(f"Undefined identifier: {name}")
            return None
        return self.symbols.get(name) or self.builtin_functions.get(name)

    def is_function(self, name):
        symbol = self.resolve(name)
        return symbol and symbol.get('type') in ['function', 'builtin']

def analyze_node(node, context):
    if not node:
        return
        
    if node.type == "Program":
        for stmt in node.children:
            analyze_node(stmt, context)

    elif node.type == "FunctionDecl":
        func_name = node.value
        params = [param.value for param in node.children if param.type == "Param"]
        context.define(func_name, {"type": "function", "params": params})
        
        # Analyze function parameters in a new scope (simplified)
        for param in node.children:
            if param.type == "Param":
                analyze_node(param, context)

    elif node.type == "Assignment":
        var_name = node.value
        # Analyze the right-hand side expression first
        if node.children:
            analyze_node(node.children[0], context)
        # Define/update the variable
        context.define(var_name, {"type": "variable"})

    elif node.type == "ExpressionStatement":
        for child in node.children:
            analyze_node(child, context)

    elif node.type == "BinOp":
        # Analyze both operands
        if len(node.children) >= 2:
            analyze_node(node.children[0], context)
            analyze_node(node.children[1], context)
        else:
            context.errors.append("Binary operation missing operands")

    elif node.type == "Variable":
        context.resolve(node.value)

    elif node.type == "FunctionCall":
        func_name = node.value
        args = node.children
        
        # Check if function exists
        func_info = context.resolve(func_name)
        if func_info:
            # Check argument count for user-defined functions
            if func_info.get('type') == 'function':
                expected_params = func_info.get('params', [])
                if len(expected_params) != len(args):
                    context.errors.append(
                        f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(args)}"
                    )
            # For builtin functions with variable args, we're more lenient
            elif func_info.get('type') == 'builtin':
                expected_count = func_info.get('params', -1)
                if expected_count > 0 and len(args) != expected_count:
                    context.errors.append(
                        f"Builtin function '{func_name}' expects {expected_count} arguments, got {len(args)}"
                    )
        
        # Analyze all arguments
        for arg in args:
            analyze_node(arg, context)

    elif node.type == "PrintCall":
        # Handle print statements specifically
        for arg in node.children:
            analyze_node(arg, context)

    elif node.type == "Number":
        pass  # Numbers are always valid

    elif node.type == "String":
        pass  # Strings are always valid

    elif node.type == "Param":
        # Define parameter in current scope
        context.define(node.value, {"type": "param"})

    else:
        # Handle unknown node types gracefully
        context.errors.append(f"Unknown AST node type: {node.type}")
        # Still try to analyze children if they exist
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                analyze_node(child, context)

def perform_semantic_analysis(ast):
    """
    Performs semantic analysis on the given AST and returns a list of errors.
    """
    if not ast:
        return ["No AST provided for semantic analysis"]
    
    context = SemanticContext()
    try:
        analyze_node(ast, context)
    except Exception as e:
        context.errors.append(f"Semantic analysis error: {str(e)}")
    
    return context.errors