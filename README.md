# Regex to DFA Converter

A Python implementation that converts regular expressions to Deterministic Finite Automata (DFA). This project includes a complete lexer, parser, and DFA constructor for handling regular expressions with various operators.

## Features

- **Lexical Analysis**: Tokenizes regular expressions with support for escape sequences
- **Syntax Parsing**: Builds Abstract Syntax Trees (AST) from tokenized input
- **DFA Construction**: Converts AST to DFA using position-based construction
- **Extended Regex Support**: Handles concatenation, union, Kleene star, and repetition operators
- **Ambiguity Detection**: Validates input strings against the alphabet to prevent ambiguous parsing
- **Comprehensive Testing**: Includes unit tests for lexer and DFA construction

## Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Union (OR) | `a+b` matches 'a' or 'b' |
| `.` | Concatenation (implicit) | `ab` becomes `a.b` |
| `*` | Kleene Star (zero or more) | `a*` matches '', 'a', 'aa', etc. |
| `()` | Grouping | `(a+b)*` |
| `{n}` | Exact repetition | `a{3}` matches 'aaa' |
| `{n,}` | At least n repetitions | `a{2,}` matches 'aa', 'aaa', etc. |
| `{n,m}` | Between n and m repetitions | `a{2,4}` matches 'aa', 'aaa', 'aaaa' |
| `$` | Epsilon (empty string) | Used internally |
| `\` | Escape character | `a\+b` treats '+' as literal |

## Project Structure

```
.
├── astnode.py          # AST node definition
├── lexer.py           # Lexical analyzer
├── parse.py           # Recursive descent parser
├── dfa.py             # DFA construction and representation
├── main.py            # Main entry point
├── test_lexer.py      # Lexer unit tests
└── test_dfa.py        # DFA construction tests
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/danitdrvc/regex-to-dfa.git
cd regex-to-dfa
```

2. Ensure you have Python 3.7+ installed:
```bash
python --version
```

## Usage

### Basic Usage

```python
from lexer import Lexer
from dfa import DFAConstructor

# Define your alphabet and regex
alphabet = {"a", "b", "c"}
regex = "(ab+c)*"

# Create lexer and construct DFA
lexer = Lexer(regex, alphabet)
dfa_constructor = DFAConstructor(lexer)
```

### Running the Example

```bash
python main.py
```

This will run the default example with:
- Alphabet: `{"a", "b", "c"}`
- Regex: `"(abc+((ab*+c+b*)))(abc+((ab*+$+b*)))**+c*"`

### Custom Examples

```python
# Simple concatenation
alphabet = {"a", "b"}
regex = "ab"
lexer = Lexer(regex, alphabet)
dfa_constructor = DFAConstructor(lexer)

# Union operation
regex = "a+b"
lexer = Lexer(regex, alphabet)
dfa_constructor = DFAConstructor(lexer)

# Kleene star
regex = "a*"
lexer = Lexer(regex, alphabet)
dfa_constructor = DFAConstructor(lexer)
```

## Algorithm Overview

### 1. Lexical Analysis
- Processes input regex and handles concatenation insertion
- Detects and prevents ambiguous symbol sequences
- Supports escape sequences for literal operators

### 2. Parsing
- Uses recursive descent parsing to build AST
- Handles operator precedence: `*` > `.` > `+`
- Supports repetition syntax `{n}`, `{n,}`, `{n,m}`

### 3. DFA Construction
The DFA construction follows these key steps:

1. **Position Assignment**: Each symbol in the AST gets a unique position
2. **Nullable Calculation**: Determines which nodes can produce empty strings
3. **First/Last Position Computation**: Calculates possible start/end positions
4. **Follow Position Calculation**: Determines which positions can follow others
5. **State Construction**: Builds DFA states from position sets
6. **Transition Function**: Creates transitions based on follow positions

## Testing

Run the test suite:

```bash
# Test lexer functionality
python -m pytest test_lexer.py -v

# Test DFA construction
python -m pytest test_dfa.py -v

# Run all tests
python -m pytest -v
```

## Examples

### Example 1: Simple Union
```
Input: a+b
Alphabet: {a, b}
Result: DFA that accepts strings "a" or "b"
```

### Example 2: Concatenation with Kleene Star
```
Input: a*b
Alphabet: {a, b}
Result: DFA that accepts "b", "ab", "aab", "aaab", etc.
```

### Example 3: Complex Expression
```
Input: (a+b)*c
Alphabet: {a, b, c}
Result: DFA that accepts strings ending with 'c' preceded by any combination of 'a' and 'b'
```

## Time Complexity

- **Lexer**: O(n²) where n is the regex length
- **Parser**: O(n) where n is the number of tokens
- **DFA Construction**: O(n³) in worst case, where n is the number of positions

## Error Handling

The implementation includes comprehensive error handling:

- `LexerError`: Invalid tokens or ambiguous strings
- `ParserError`: Syntax errors in regex
- Position tracking for precise error reporting

## Acknowledgments

- Based on the Berry-Sethi algorithm for direct DFA construction
- Implements concepts from compiler design and formal language theory
- Inspired by classic automata theory literature
