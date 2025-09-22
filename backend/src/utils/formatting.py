# utils/formatting.py
import ast

def format_ast_tree(node, indent_level=0):
    """
    Recursively traverses an official Python AST node and returns a
    formatted, indented string representation of the tree.
    """
    # Set the indentation string for the current level
    indent_str = "  " * indent_level
    
    # If the 'node' is not an AST node, just return its string representation
    if not isinstance(node, ast.AST):
        return f"{indent_str}{repr(node)}"

    # Start with the node's official class name (e.g., "Module", "FunctionDef")
    node_repr = f"{indent_str}{node.__class__.__name__}(\n"
    
    # ast.iter_fields is the correct way to get a node's children and attributes
    for field_name, field_value in ast.iter_fields(node):
        # Add the field's name (e.g., "body=", "name=")
        node_repr += f"{indent_str}  {field_name}="
        
        # Recursively call the function to format the field's value
        if isinstance(field_value, list):
            # If the field contains a list of other nodes
            if not field_value:
                node_repr += "[],\n"
            else:
                node_repr += "[\n"
                for item in field_value:
                    node_repr += f"{format_ast_tree(item, indent_level + 2)},\n"
                node_repr += f"{indent_str}  ],\n"
        else:
            # If the field contains a single value (either another node or a simple type)
            node_repr += f"{format_ast_tree(field_value, indent_level + 1)},\n"
            
    node_repr += f"{indent_str})"
    return node_repr