from pygments import lexers
from pygments.util import ClassNotFound

def get_lexer_for_file(filename):
    if '.' not in filename:
        return lexers.TextLexer()

    try:
        lexer = lexers.get_lexer_for_filename(filename)
        return lexer
    except ClassNotFound:
        return lexers.TextLexer() 