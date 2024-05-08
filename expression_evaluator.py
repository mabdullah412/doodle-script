import PySimpleGUI as sg
import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        if self.tokens:
            self.current_token = self.tokens[0]
        else:
            self.current_token = None

    def advance(self):
        self.index += 1
        while self.index < len(self.tokens) and self.tokens[self.index][0] == 'WHITESPACE':
            self.index += 1

        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None
    
    def factor(self):
        if self.current_token[0] == 'NUMBER':
            value = float(self.current_token[1])
            self.advance()
            return value
        elif self.current_token[0] == 'OPERATOR' and self.current_token[1] == '-':
            self.advance()
            return -self.factor()
        elif self.current_token[0] == 'PAREN' and self.current_token[1] == '(':
            self.advance()
            result = self.expression()
            if self.current_token[0] == 'PAREN' and self.current_token[1] == ')':
                self.advance()
                return result
            else:
                raise ValueError("Expected closing parenthesis")
        else:
            raise ValueError("Invalid factor")

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token[0] in ('OPERATOR', '*', '/'):
            op = self.current_token[1]
            self.advance()
            factor_value = self.factor()
            if op == '*':
                result *= factor_value
            elif op == '/':
                result /= factor_value
        return result

    def expression(self):
        result = self.term()
        while self.current_token and self.current_token[0] in ('OPERATOR', '+', '-'):
            op = self.current_token[1]
            self.advance()
            term_value = self.term()
            if op == '+':
                result += term_value
            elif op == '-':
                result -= term_value
        return result

TOKEN_TYPES = {
    'IDENTIFIER': r'[a-zA-Z_]\w*',
    'NUMBER': r'\d+(\.\d+)?',
    'OPERATOR': r'[+\-*/]',
    'PAREN': r'[()]',
    'WHITESPACE': r'\s+',
    'COMMENT': r'#.*',
}

def tokenize(input_string):
    tokens = []
    position = 0

    while position < len(input_string):
        match = None
        for token_type, pattern in TOKEN_TYPES.items():
            regex = re.compile(pattern)
            match = regex.match(input_string, position)
            if match:
                value = match.group()
                if token_type != 'WHITESPACE' and token_type != 'COMMENT':
                    tokens.append((token_type, value))
                    print(f"Token: {value}, Type: {token_type}")  # Debugging
                position = match.end()
                break

        if not match:
            raise ValueError(f"Invalid token at position {position}: {input_string[position]}")

    return tokens


layout = [
    [sg.Text("Enter an expression:"), sg.InputText(key="-EXPR-")],
    [sg.Button("Evaluate"), sg.Button("Exit")],
    [sg.Text("", size=(20, 1), key="-RESULT-")]
]

window = sg.Window("Expression Evaluator", layout)

def main():
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Evaluate":
            try:
                input_expr = values["-EXPR-"]
                tokens = tokenize(input_expr)
                print("Tokens:", tokens)  # Debugging
                parser = Parser(tokens)
                result = parser.expression()
                window["-RESULT-"].update(f"Result: {result}")
            except Exception as e:
                window["-RESULT-"].update(f"Error: {str(e)}")

    window.close()

if __name__ == "__main__":
    main()
