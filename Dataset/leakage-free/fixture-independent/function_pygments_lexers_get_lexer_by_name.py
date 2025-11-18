from pygments import lex
from pygments.lexers import get_lexer_by_name

def lex_code(language, code):
    try:
        lexer = get_lexer_by_name(language)
        tokens = list(lex(code, lexer))
        return tokens
    except Exception as e:
        print(f"Error lexing code: {e}")
        return None
