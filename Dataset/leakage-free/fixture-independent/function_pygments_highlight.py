from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def format_code_to_html_with_highlight(code):
    lexer = PythonLexer()  
    formatter = HtmlFormatter()  #
    highlighted_code = highlight(code, lexer, formatter)
    print(highlighted_code)
    return highlighted_code
