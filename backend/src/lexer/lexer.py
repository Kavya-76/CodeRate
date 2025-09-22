# lexer/lexer.py
import tokenize
import io

# A mapping from tokenize type constants to readable names
TOKEN_TYPE_MAP = {
    tokenize.ENDMARKER: 'ENDMARKER',
    tokenize.NAME: 'NAME',
    tokenize.NUMBER: 'NUMBER',
    tokenize.STRING: 'STRING',
    tokenize.NEWLINE: 'NEWLINE',
    tokenize.INDENT: 'INDENT',
    tokenize.DEDENT: 'DEDENT',
    tokenize.LPAR: 'LPAR',
    tokenize.RPAR: 'RPAR',
    tokenize.LSQB: 'LSQB',
    tokenize.RSQB: 'RSQB',
    tokenize.COLON: 'COLON',
    tokenize.COMMA: 'COMMA',
    tokenize.SEMI: 'SEMI',
    tokenize.PLUS: 'PLUS',
    tokenize.MINUS: 'MINUS',
    tokenize.STAR: 'STAR',
    tokenize.SLASH: 'SLASH',
    tokenize.VBAR: 'VBAR',
    tokenize.AMPER: 'AMPER',
    tokenize.LESS: 'LESS',
    tokenize.GREATER: 'GREATER',
    tokenize.EQUAL: 'EQUAL',
    tokenize.DOT: 'DOT',
    tokenize.PERCENT: 'PERCENT',
    tokenize.LBRACE: 'LBRACE',
    tokenize.RBRACE: 'RBRACE',
    tokenize.EQEQUAL: 'EQEQUAL',
    tokenize.NOTEQUAL: 'NOTEQUAL',
    tokenize.LESSEQUAL: 'LESSEQUAL',
    tokenize.GREATEREQUAL: 'GREATEREQUAL',
    tokenize.TILDE: 'TILDE',
    tokenize.CIRCUMFLEX: 'CIRCUMFLEX',
    tokenize.LEFTSHIFT: 'LEFTSHIFT',
    tokenize.RIGHTSHIFT: 'RIGHTSHIFT',
    tokenize.DOUBLESTAR: 'DOUBLESTAR',
    tokenize.PLUSEQUAL: 'PLUSEQUAL',
    tokenize.MINEQUAL: 'MINEQUAL',
    tokenize.STAREQUAL: 'STAREQUAL',
    tokenize.SLASHEQUAL: 'SLASHEQUAL',
    tokenize.PERCENTEQUAL: 'PERCENTEQUAL',
    tokenize.AMPEREQUAL: 'AMPEREQUAL',
    tokenize.VBAREQUAL: 'VBAREQUAL',
    tokenize.CIRCUMFLEXEQUAL: 'CIRCUMFLEXEQUAL',
    tokenize.LEFTSHIFTEQUAL: 'LEFTSHIFTEQUAL',
    tokenize.RIGHTSHIFTEQUAL: 'RIGHTSHIFTEQUAL',
    tokenize.DOUBLESTAREQUAL: 'DOUBLESTAREQUAL',
    tokenize.DOUBLESLASH: 'DOUBLESLASH',
    tokenize.DOUBLESLASHEQUAL: 'DOUBLESLASHEQUAL',
    tokenize.AT: 'AT',
    tokenize.ATEQUAL: 'ATEQUAL',
    tokenize.RARROW: 'RARROW',
    tokenize.ELLIPSIS: 'ELLIPSIS',
    tokenize.COLONEQUAL: 'COLONEQUAL',
    tokenize.OP: 'OPERATOR',
    tokenize.AWAIT: 'AWAIT',
    tokenize.ASYNC: 'ASYNC',
    tokenize.TYPE_IGNORE: 'TYPE_IGNORE',
    tokenize.TYPE_COMMENT: 'TYPE_COMMENT',
    tokenize.SOFT_KEYWORD: 'SOFT_KEYWORD',
    tokenize.ERRORTOKEN: 'ERRORTOKEN',
    tokenize.COMMENT: 'COMMENT',
    tokenize.NL: 'NL',
    tokenize.ENCODING: 'ENCODING',
}

def perform_lexical_analysis(code: str):
    """
    Performs lexical analysis using Python's built-in tokenizer.
    This is far more robust than a custom PLY lexer.
    """
    tokens_list = []
    try:
        # The `tokenize` module works with file-like objects, so we use io.StringIO
        code_io = io.StringIO(code)
        
        # generate_tokens is a generator that yields token info
        for token_info in tokenize.generate_tokens(code_io.readline):
            token_type_name = TOKEN_TYPE_MAP.get(token_info.type, 'UNKNOWN')
            # We create a simple object-like dictionary for compatibility
            token_obj = {
                "type": token_type_name,
                "value": token_info.string,
                "start": token_info.start,
                "end": token_info.end,
                "line": token_info.line.strip()
            }
            # For your project, you might only need the formatted string
            tokens_list.append(f"{token_type_name}: '{token_info.string}'")
            
    except tokenize.TokenError as e:
        # Handle cases like unterminated strings
        raise SyntaxError(f"Lexical Error: {e}")
        
    return tokens_list