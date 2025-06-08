from dfa import *
from lexer import *
from parse import *

def test_simple_regex_1():
    alphabet = {'a', 'b', 'c'}
    regex = 'a'
    lexer = Lexer(regex, alphabet)
    dfa_constructor = DFAConstructor(lexer)
    dfa = dfa_constructor.construct_dfa(dfa_constructor.ast)

    assert dfa.start_state == 'q2'
    assert dfa.accept_states == {'q1'}
    assert dfa.transitions == {
        'q0': {'a': 'q0', 'b': 'q0', 'c': 'q0'},
        'q1': {'a': 'q0', 'b': 'q0', 'c': 'q0'},
        'q2': {'a': 'q1', 'b': 'q0', 'c': 'q0'}
    }
    
def test_simple_regex_2():
    alphabet = {'a', 'b', 'c'}
    regex = 'a+b'
    lexer = Lexer(regex, alphabet)
    dfa_constructor = DFAConstructor(lexer)
    dfa = dfa_constructor.construct_dfa(dfa_constructor.ast)

    assert dfa.start_state == 'q2'
    assert dfa.accept_states == {'q0'}
    assert dfa.transitions == {
        'q0': {'a': 'q1', 'b': 'q1', 'c': 'q1'},
        'q1': {'a': 'q1', 'b': 'q1', 'c': 'q1'},
        'q2': {'a': 'q0', 'b': 'q0', 'c': 'q1'}
    }
    
def test_simple_regex_3():
    alphabet = {'a', 'b', 'c'}
    regex = 'a*b'
    lexer = Lexer(regex, alphabet)
    dfa_constructor = DFAConstructor(lexer)
    dfa = dfa_constructor.construct_dfa(dfa_constructor.ast)

    assert dfa.start_state == 'q2'
    assert dfa.accept_states == {'q0'}
    assert dfa.transitions == {
        'q0': {'a': 'q1', 'b': 'q1', 'c': 'q1'},
        'q1': {'a': 'q1', 'b': 'q1', 'c': 'q1'},
        'q2': {'a': 'q2', 'b': 'q0', 'c': 'q1'}
    }