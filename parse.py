from astnode import ASTNode
from lexer import Token, Lexer

class Parser:
    def __init__(self, lexer):
        self.lexer: Lexer = lexer
    
    
    def print_ast(self, node, indent=0):
        # Print the abstract syntax tree (AST) (O(n) time complexity)
        if node is None:
            return
        indent_str = ' ' * indent
        if node.type == 'SYMBOL' or node.type == 'EPSILON':
            print(f"{indent_str}{node.type}('{node.value}', pos={node.position})")
        elif node.type == 'STAR':
            print(f"{indent_str}{node.type}(pos={node.position})")
            self.print_ast(node.value, indent + 2)
        elif node.type in {'CONCAT', 'UNION'}:
            print(f"{indent_str}{node.type}(pos={node.position})")
            self.print_ast(node.left, indent + 2)
            self.print_ast(node.right, indent + 2)


    def assign_positions(self, node, position=1):
        # Assign positions to each node in the AST (O(n) time complexity)
        if node is None:
            return position
        if node.type == 'SYMBOL':
            node.position = position
            return position + 1
        if node.type == 'CONCAT' or node.type == 'UNION':
            position = self.assign_positions(node.left, position)
            position = self.assign_positions(node.right, position)
        elif node.type == 'STAR':
            position = self.assign_positions(node.value, position)
        return position


    def parse(self):
        # Parse the regex and return the root of the AST (O(n) time complexity)
        head = ASTNode('CONCAT', left=self.regex_rule(), right=ASTNode('SYMBOL', value='#'))
        return head


    def regex_rule(self):
        # Parse a regex rule
        return self.union()


    def union(self):
        # Parse a union operation
        left = self.concat()
        while self.peek().value == '+':
            self.consume('+')
            right = self.concat()
            left = ASTNode('UNION', left=left, right=right)
        return left


    def concat(self):
        # Parse a concatenation operation
        left = self.star()
        while self.peek().value == '.':
            self.consume('.')
            right = self.star()
            left = ASTNode('CONCAT', left=left, right=right)
        return left


    def star(self):
        # Parse a star (Kleene star) operation
        node = self.factor()
        while self.peek().value == '*':
            self.consume('*')
            node = ASTNode('STAR', value=node)
        return node


    def factor(self):
        # Parse a factor, which can be a symbol, epsilon, or a sub-expression in parentheses
        if self.peek().value == '(':
            self.consume('(')
            node = self.regex_rule()
            self.consume(')')
            # Handle {N}, {N,}, {N,M} syntax for repetition
            if self.peek().value == '{':
                return self.repeatFunctions(node)
            return node
        elif self.peek().value == '$':  # Handle epsilon
            self.consume('$')
            return ASTNode('EPSILON')
        elif self.peek().type == 'SYMBOL':
            symbol = self.consume().value
            node = ASTNode('SYMBOL', value=symbol)
            # Handle {N}, {N,}, {N,M} syntax for repetition
            if self.peek().value == '{':
                return self.repeatFunctions(node)
            return node
        else:
            raise ParserError(f"Unexpected character: {self.peek()}", self.lexer.index)


    def repeatFunctions(self, node):
        # Handle repetition syntax: {N}, {N,}, {N,M}
        self.consume('{')
        n = self.consume().value
        if self.peek().value == '}':
            self.consume('}')
            return self.repeat(node, int(n))
        elif self.peek().value == ',':
            self.consume(',')
            if self.lexer.processed_regex[self.lexer.index].isdigit():
                m = self.consume().value
                self.consume('}')
                return self.repeat_between(node, int(n), int(m))
            else:
                self.consume('}')
                return self.repeat_at_least(node, int(n))


    def copy_pattern(self, node):
        # Create a deep copy of the pattern in the AST (O(n) time complexity)
        if node.type == 'SYMBOL' or node.type == 'EPSILON':
            return ASTNode('SYMBOL', value=node.value)
        if node.type == 'STAR':
            return ASTNode('STAR', value=self.copy_pattern(node.value))
        if node.type in {'CONCAT', 'UNION'}:
            return ASTNode(node.type, left=self.copy_pattern(node.left), right=self.copy_pattern(node.right))
        raise ParserError(f"Unknown node type: {node.type}", self.lexer.index)
    
    
    def repeat(self, pattern, n):
        # Repeat the pattern exactly n times (O(n^2) time complexity)
        if n < 1:
            raise ParserError("Number of repetitions must be a positive integer", self.lexer.index)
        if n == 1:
            return self.copy_pattern(pattern)
        current = self.copy_pattern(pattern)
        for _ in range(1, n):
            current = ASTNode('CONCAT', left=current, right=self.copy_pattern(pattern))
        return current


    def repeat_at_least(self, pattern, n):
        # Repeat the pattern at least n times, followed by a Kleene star
        if n < 1:
            raise ParserError("Number of repetitions must be a positive integer", self.lexer.index)
        return ASTNode('CONCAT', left=self.repeat(pattern, n), right=ASTNode('STAR', value=self.copy_pattern(pattern)))


    def repeat_between(self, pattern, n, m):
        # Repeat the pattern between n and m times
        if n < 1 or m < n:
            raise ParserError("Invalid range for repetition", self.lexer.index)
        
        result = self.repeat(pattern, n)
        for i in range(n + 1, m + 1):
            result = ASTNode('UNION', left=result, right=self.repeat(pattern, i))
        return result


    def peek(self) -> Token:
        # Peek at the next token without consuming it
        return self.lexer.peek()


    def consume(self, expected=None) -> Token:
        # Consume the next token, optionally checking if it matches an expected value
        if expected is not None and self.peek().value != expected:
            raise ParserError(f'Expected {expected} but got {self.peek().value}', self.lexer.index)       
        return self.lexer.next()
    
    
class ParserError(ValueError):
    def __init__(self, message: str, position: int):
        self.message: str = message
        self.position: int = position
