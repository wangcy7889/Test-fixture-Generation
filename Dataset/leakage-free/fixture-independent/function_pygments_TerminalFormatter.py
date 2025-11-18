from pygments import lexers, highlight
from pygments.formatters import TerminalFormatter

def format_code_for_terminal(code, language="python"):
    lexer = lexers.get_lexer_by_name(language)  
    formatter = TerminalFormatter()  
    highlighted_code = highlight(code, lexer, formatter)  
    
    return highlighted_code
