from lexer import Lexer

def test_lexer_1():
    string = "a+b"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a+b"
    assert lexer.processed_regex == "a+b"
    assert lexer.next().value == "a"
    assert lexer.next().value == "+"
    assert lexer.next().value == "b"
    assert lexer.next().value == "EOF"

def test_lexer_2():
    string = "ab"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "ab"
    assert lexer.processed_regex == "a.b"
    assert lexer.next().value == "a"
    assert lexer.next().value == "."
    assert lexer.next().value == "b"
    assert lexer.next().value == "EOF"

def test_lexer_3():
    string = "a*"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a*"
    assert lexer.processed_regex == "a*"
    assert lexer.next().value == "a"
    assert lexer.next().value == "*"
    assert lexer.next().value == "EOF"

def test_lexer_4():
    string = "a{2}"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a{2}"
    assert lexer.next().value == "a"
    assert lexer.next().value == "{"
    assert lexer.next().value == "2"
    assert lexer.next().value == "}"
    assert lexer.next().value == "EOF"

def test_lexer_5():
    string = "a{2,3}"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a{2,3}"
    assert lexer.processed_regex == "a{2,3}"
    assert lexer.next().value == "a"
    assert lexer.next().value == "{"
    assert lexer.next().value == "2"
    assert lexer.next().value == ","
    assert lexer.next().value == "3"
    assert lexer.next().value == "}"
    assert lexer.next().value == "EOF"
    
def test_lexer_6():
    string = "a{2,}"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a{2,}"
    assert lexer.processed_regex == "a{2,}"
    assert lexer.next().value == "a"
    assert lexer.next().value == "{"
    assert lexer.next().value == "2"
    assert lexer.next().value == ","
    assert lexer.next().value == "}"
    assert lexer.next().value == "EOF"
    
def test_lexer_7():
    string = "a+ab"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a+ab"
    assert lexer.processed_regex == "a+a.b"
    assert lexer.next().value == "a"
    assert lexer.next().value == "+"
    assert lexer.next().value == "a"
    assert lexer.next().value == "."
    assert lexer.next().value == "b"
    assert lexer.next().value == "EOF"

def test_lexer_8():
    string = "aba*"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "aba*"
    assert lexer.processed_regex == "a.b.a*"
    assert lexer.next().value == "a"
    assert lexer.next().value == "."
    assert lexer.next().value == "b"
    assert lexer.next().value == "."
    assert lexer.next().value == "a"
    assert lexer.next().value == "*"
    assert lexer.next().value == "EOF"
    
def test_lexer_9():
    string = "a{2,3}b"
    alphabet = {"a","b"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a{2,3}b"
    assert lexer.processed_regex == "a{2,3}.b"
    assert lexer.next().value == "a"
    assert lexer.next().value == "{"
    assert lexer.next().value == "2"
    assert lexer.next().value == ","
    assert lexer.next().value == "3"
    assert lexer.next().value == "}"
    assert lexer.next().value == "."
    assert lexer.next().value == "b"
    assert lexer.next().value == "EOF"
    
def test_lexer_10():
    string = "((a+b)c)*"
    alphabet = {"a","b","c"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "((a+b)c)*"
    assert lexer.processed_regex == "((a+b).c)*"
    assert lexer.next().value == "("
    assert lexer.next().value == "("
    assert lexer.next().value == "a"
    assert lexer.next().value == "+"
    assert lexer.next().value == "b"
    assert lexer.next().value == ")"
    assert lexer.next().value == "."
    assert lexer.next().value == "c"
    assert lexer.next().value == ")"
    assert lexer.next().value == "*"
    assert lexer.next().value == "EOF"
    
def test_lexer_11():
    string = "a\\+b"
    alphabet = {"a","b", "+"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a\\+b"
    assert lexer.processed_regex == "a.\\+.b"
    assert lexer.next().value == "a"
    assert lexer.next().value == "."
    assert lexer.next().value == "+"
    assert lexer.next().value == "."
    assert lexer.next().value == "b"
    assert lexer.next().value == "EOF"
    
def test_lexer_11():
    string = "a\\+"
    alphabet = {"a","b", "+"}
    lexer = Lexer(string, alphabet)
    assert lexer.regex == "a\\+"
    assert lexer.processed_regex == "a.\\+"
    assert lexer.next().value == "a"
    assert lexer.next().value == "."
    assert lexer.next().value == "+"
    assert lexer.next().value == "EOF"