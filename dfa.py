from parse import Parser

class DFA:
    def __init__(self, start_state, accept_states, transitions):
        # Initialize the DFA with the start state, accept states, and transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
    
    def print_dfa(self):
        # Print the DFA's start state, accept states, and transitions
        print(f"Start State: {self.start_state}")
        print(f"Accept States: {self.accept_states}")
        print("Transitions:")
        for state, trans in self.transitions.items():
            for symbol, next_state in trans.items():
                print(f"  {state} {symbol} {next_state}")


class DFAConstructor:
    def __init__(self, lexer):
        # Initialize the DFAConstructor with a lexer
        self.parser = Parser(lexer)
        self.ast = self.parser.parse()
        self.parser.assign_positions(self.ast)
        
        # Print the AST for debugging
        self.parser.print_ast(self.ast)
            
        # Construct the DFA from the AST
        followpos_table = self.followpos(self.ast)
        for pos, follows in followpos_table.items():
            print(f"Position {pos}: Follow positions -> {follows}")
            
        dfa = self.construct_dfa(self.ast)
        dfa.print_dfa()
        
        
    def nullable(self, node):
        # Determine if the given node is nullable (can produce the empty string) (O(n) time complexity) 
        if node.type == 'SYMBOL': 
            return False
        elif node.type == 'STAR':
            return True
        elif node.type == 'CONCAT':
            return self.nullable(node.left) and self.nullable(node.right)
        elif node.type == 'UNION':
            return self.nullable(node.left) or self.nullable(node.right)
        elif node.type == 'EPSILON':
            return True
        else:
            raise ValueError(f"Unknown node type: {node.type}")
    
    
    def firstpos(self, node):
        # Compute the first positions of the given node (O(n) time complexity)
        if node.type == 'SYMBOL':
            return {node.position}
        elif node.type == 'STAR':
            return self.firstpos(node.value)
        elif node.type == 'CONCAT':
            if self.nullable(node.left):
                return self.firstpos(node.left) | self.firstpos(node.right)
            else:
                return self.firstpos(node.left)
        elif node.type == 'UNION':
            return self.firstpos(node.left) | self.firstpos(node.right)
        elif node.type == 'EPSILON':
            return set()
        else:
            raise ValueError(f"Unknown node type: {node.type}")
    
    
    def lastpos(self, node):
        # Compute the last positions of the given node (O(n) time complexity)
        if node.type == 'SYMBOL':
            return {node.position}
        elif node.type == 'STAR':
            return self.lastpos(node.value)
        elif node.type == 'CONCAT':
            if self.nullable(node.right):
                return self.lastpos(node.left) | self.lastpos(node.right)
            else:
                return self.lastpos(node.right)
        elif node.type == 'UNION':
            return self.lastpos(node.left) | self.lastpos(node.right)
        elif node.type == 'EPSILON':
            return set()
        else:
            raise ValueError(f"Unknown node type: {node.type}")
    
    
    def followpos(self, node):
        # Compute the follow positions for each position in the AST (O(n) time complexity)
        followpos_table = {}

        def init_followpos(node):
            # Initialize the followpos table
            if node is None:
                return
            if node.type == 'SYMBOL':
                followpos_table[node.position] = set()
            init_followpos(node.left)
            init_followpos(node.right)
            if node.type == 'STAR':
                init_followpos(node.value)

        def calculate_followpos(node):
            # Calculate the follow positions
            if node is None:
                return
            if node.type == 'CONCAT':
                for pos in self.lastpos(node.left):
                    followpos_table[pos].update(self.firstpos(node.right))
            if node.type == 'STAR':
                for pos in self.lastpos(node.value):
                    followpos_table[pos].update(self.firstpos(node.value))
            calculate_followpos(node.left)
            calculate_followpos(node.right)
            if node.type == 'STAR':
                calculate_followpos(node.value)

        init_followpos(node)
        calculate_followpos(node)
        return followpos_table
        
        
    def build_ast_by_position(self, node, ast_by_position):
        # Build a dictionary mapping positions to AST nodes
        if node is None:
            return
        if node.type == 'SYMBOL':
            ast_by_position[node.position] = node
        self.build_ast_by_position(node.left, ast_by_position)
        self.build_ast_by_position(node.right, ast_by_position)
        if node.type == 'STAR':
            self.build_ast_by_position(node.value, ast_by_position)


    def construct_dfa(self, ast):
        # Construct the DFA from the AST
        followpos_table = self.followpos(ast)
        ast_by_position = {}
        self.build_ast_by_position(ast, ast_by_position)

        # Get the set of symbols (excluding epsilon)
        symbols = set(self.parser.lexer.alphabet)
        symbols.remove('$')

        # Initialize the DFA's states, transitions, and accept states
        start_state = frozenset(self.firstpos(ast))
        dfa_states = {start_state}
        unmarked_states = [start_state]
        dfa_transitions = {}
        dfa_accept_states = set()

        while unmarked_states:
            T = unmarked_states.pop()
            if T not in dfa_transitions:
                dfa_transitions[T] = {}
            for symbol in symbols:
                U = set()
                for pos in T:
                    if pos in followpos_table and ast_by_position[pos].value == symbol:
                        U.update(followpos_table[pos])
                U = frozenset(U)
                if U:
                    if U not in dfa_states:
                        dfa_states.add(U)
                        unmarked_states.append(U)
                    dfa_transitions[T][symbol] = U
                else:
                    # Handling dead state
                    dead_state = frozenset()
                    if dead_state not in dfa_states:
                        dfa_states.add(dead_state)
                        dfa_transitions[dead_state] = {s: dead_state for s in symbols}
                    dfa_transitions[T][symbol] = dead_state
            if any(pos in ast_by_position for pos in T if ast_by_position[pos].value == '#'):
                dfa_accept_states.add(T)

        # Create a mapping from state sets to state names
        state_map = {state: f'q{index}' for index, state in enumerate(dfa_states)}
        dfa_start_state = state_map[start_state]
        dfa_accept_states = {state_map[state] for state in dfa_accept_states}
        dfa_transitions = {
            state_map[state]: {symbol: state_map[next_state] for symbol, next_state in trans.items()}
            for state, trans in dfa_transitions.items()
        }

        return DFA(dfa_start_state, dfa_accept_states, dfa_transitions)
