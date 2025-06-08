import sys

from astnode import *
from dfa import *
from parse import *
from lexer import *

def main():
    alphabet = {"a","b","c"}
    regex = "(abc+((ab*+c+b*)))(abc+((ab*+$+b*)))**+c*"
    
    try:
        lexer = Lexer(regex, alphabet)
        DFAConstructor(lexer)
    except LexerError as e:
        print("Lexer error at position", e.position)
        print(e.message)
    except ParserError as e:
        print("Parser error at position", e.position)
        print(e.message)
    
    return 0

if __name__ == "__main__":
    err_code = main()
    sys.exit(err_code)