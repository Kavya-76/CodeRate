# src/semantic/semantic_analyzer.py

class SemanticContext:
    def __init__(self):
        self.symbols = {}  # Stores variables/functions
        self.errors = []

    def define(self, name, value):
        if name in self.symbols:
            self.errors.append(f"Duplicate identifier: {name}")
        else:
            self.symbols[name] = value

    def resolve(self, name):
        if name not in self.symbols:
            self.errors.append(f"Undefined identifier: {name}")

def analyze_node(node, context):
    if node.type == "Program":
        for stmt in node.children:
            analyze_node(stmt, context)

    elif node.type == "FunctionDecl":
        func_name = node.value
        params = [param.value for param in node.children]
        context.define(func_name, {"type": "function", "params": params})

    elif node.type == "ExpressionStatement":
        for child in node.children:
            analyze_node(child, context)

    elif node.type == "BinOp":
        analyze_node(node.children[0], context)
        analyze_node(node.children[1], context)

    elif node.type == "Variable":
        context.resolve(node.value)

    elif node.type == "FunctionCall":
        func_name = node.value
        args = node.children
        if func_name in context.symbols:
            expected_params = context.symbols[func_name]["params"]
            if len(expected_params) != len(args):
                context.errors.append(
                    f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(args)}"
                )
        else:
            context.errors.append(f"Call to undefined function '{func_name}'")

        for arg in args:
            analyze_node(arg, context)

    elif node.type == "Number":
        pass  # Numbers are always valid

    elif node.type == "Param":
        context.define(node.value, {"type": "param"})

    # You can extend this for more semantic rules like type checking

def perform_semantic_analysis(ast):
    context = SemanticContext()
    analyze_node(ast, context)
    return context.errors
