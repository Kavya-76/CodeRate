def format_ast_tree(node, indent=0):
    pad = '  ' * indent
    rep = f"{pad}- {node.type}"
    if node.value is not None:
        rep += f": {node.value}"
    result = [rep]
    for child in node.children:
        result.append(format_ast_tree(child, indent + 1))
    return '\n'.join(result)
