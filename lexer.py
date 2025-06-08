class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, regex, alphabet):
        # Initialize the lexer with the given regex and alphabet
        self.regex = regex
        self.alphabet = alphabet
        self.alphabet.add('$')  # Add epsilon symbol to the alphabet
        self.index = 0 
        self.processed_regex = self.process_regex(regex)  # Process the regex to handle concatenation and escape sequences
        print(self.processed_regex)
        
        
    def peek(self) -> Token:
        old_index: int = self.index
        token: Token = self.next()
        self.index = old_index
        return token
    
    
    def next(self) -> Token:
        # Get the next token from the processed regex (O(n) time complexity)
        
        while self.index < len(self.processed_regex) and self.processed_regex[self.index].isspace():
            # Skip any whitespace characters
            self.index += 1

        if self.index == len(self.processed_regex):
            # End of input reached
            return Token(type='EOF', value='EOF')
        elif self.index > len(self.processed_regex):
            # Index out of bounds
            raise Exception()

        char = self.processed_regex[self.index]
        self.index += 1

        if char == '\\':
            # Handle escape sequences
            if self.index < len(self.processed_regex):
                if self.processed_regex[self.index] in self.alphabet:
                    char = self.processed_regex[self.index]
                    self.index += 1
                    return Token(type='SYMBOL', value=char)
                else:
                    raise LexerError(f"Invalid escape sequence: {self.processed_regex[self.index]}", self.index)
            else:
                raise LexerError(f"Reached end of regex", self.index)

        if char in '+*().{},':  # Check if the character is an operator
            return Token(type='OPERATOR', value=char)
        else:
            # Handle numbers and symbols
            if char.isdigit() and char not in self.alphabet:
                # If the character is a digit but not in the alphabet, read it as a number
                buffer = [char]
                while self.index < len(self.processed_regex) and self.processed_regex[self.index].isdigit():
                    buffer.append(self.processed_regex[self.index])
                    self.index += 1
                value = ''.join(buffer)
                return Token(type='NUMBER', value=value)
            else:
                # Read alphanumeric symbols
                buffer = [char]
                while self.index < len(self.processed_regex) and self.processed_regex[self.index].isalnum():
                    buffer.append(self.processed_regex[self.index])
                    self.index += 1
                value = ''.join(buffer)
                if value in self.alphabet:
                    return Token(type='SYMBOL', value=value)
                else:
                    raise LexerError(f"Unexpected token: {value}", self.index)
                 

    def get_symbol_list(self, string : str) -> list[str]:
        # Get a list of symbols from the input string, ensuring no ambiguity (O(n^2) time complexity
        self.check_ambigous_string(string)  # Check for ambiguity in the string
        token_set = set(self.alphabet)
        n = len(string)
        dp = [False] * (n + 1)  # Dynamic programming table to store whether a substring can be formed
        dp[0] = True  # Empty string can always be formed
        tokenized_result = [[] for _ in range(n + 1)]  # List to store the resulting tokens

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and string[j:i] in token_set:
                    dp[i] = True
                    tokenized_result[i] = tokenized_result[j] + [string[j:i]]
                    break  # No need to check further if the substring can be formed

        if dp[n]:
            return tokenized_result[n]  # Return the list of tokens if the string can be formed
        else:
            raise LexerError(f"String {string} cannot be formed by alphabet {self.alphabet}", self.index)
        
        
    def insert_concatenation_operators(self, tokens: list[str]) -> str:
        # Insert concatenation operators ('.') between tokens (O(n) time complexity)
        result = []
        for i in range(len(tokens)):
            result.append(tokens[i])
            if i < len(tokens) - 1:
                result.append('.')
        return ''.join(result)


    def process_regex(self, regex: str) -> str:
        # Process the regex to handle concatenation and escape sequences (O(n^2) time complexity
        n = len(regex)
        buffer = []  # Buffer to store consecutive characters
        result = []  # Result to store the processed regex
        i = 0

        while i < n:
            char = regex[i]
            if char in '+*()}{\\':
                # Handle operators and escape sequences
                if buffer:
                    tokens = self.get_symbol_list(''.join(buffer))
                    result.append(self.insert_concatenation_operators(tokens))
                    buffer.clear()  # Clear the buffer after processing

                # Insert concatenation operator if needed
                if char == '(' and result and result[-1] not in "().+*{\\":
                    result.append('.')
                if char == '\\' and result and result[-1] not in "().+*{\\":
                    result.append('.')
                if char == '+' and i == 0:
                    result.append('$')
                
                result.append(char)
                
                # Handle special cases for operators and escape sequences
                if char == '(' and regex[i+1] == ')' and i < n - 1:
                    result.append('$')
                if char == '\\' and i < n - 1:
                    result.append(regex[i + 1])
                    i += 1
                    if i < n - 1 and regex[i + 1] not in ").+*}{":
                        result.append('.')
                if char == '+' and i < n - 1 and regex[i + 1] == '+':
                    result.append('$')
                if char == '+' and i == n - 1:
                    result.append('$')
                if char in '*)}' and i < n - 1 and regex[i + 1] not in ").+*}{":
                    result.append('.')
                if char == '{':
                    while i < n and regex[i + 1] != '}':
                        i += 1
                        result.append(regex[i])
            else:
                buffer.append(char)
            i += 1

        if buffer:
            # Process remaining buffer
            tokens = self.get_symbol_list(''.join(buffer))
            result.append(self.insert_concatenation_operators(tokens))
        return ''.join(result)
    
    
    def check_ambigous_string(self, string: str):
        # Check if the string can be formed in more than one way using the alphabet (O(n^2) time complexity)
        n = len(string)
        dp = [0] * (n + 1)  # Dynamic programming table to store the number of ways to form substrings
        dp[0] = 1  # There is one way to form an empty string
        alphabet_set = set(self.alphabet)

        for i in range(1, n + 1):
            for j in range(i):
                if string[j:i] in alphabet_set:
                    dp[i] += dp[j]  # Add the number of ways to form the substring [j:i]

        if dp[n] < 1:
            # If the string cannot be formed
            raise LexerError(f"String {string} cannot be formed by alphabet {self.alphabet}", self.index)
        if dp[n] > 1:
            # If the string can be formed in more than one way
            raise LexerError(f"String {string} can be formed by alphabet {self.alphabet} in more than one way", self.index)

        
        
class LexerError(ValueError):
    def __init__(self, message: str, position: int):
        self.message: str = message
        self.position: int = position