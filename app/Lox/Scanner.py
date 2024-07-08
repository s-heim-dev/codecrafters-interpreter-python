from app.Lox.LoxError import LoxError
from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Scanner():
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> chr:
        char = self.source[self.current]
        self.current += 1
        return char

    def match(self, expected: chr) -> bool:
        if (self.isAtEnd()):
            return False
        
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True

    def addToken(self, tokenType: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def peek(self):
        if (self.isAtEnd()):
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if (self.current + 1 >= len(self.source)):
            return '\0'
        return self.source[self.current + 1]

    def peek_is_alphanum(self):
        peek = self.peek()
        return peek.isalnum() or peek == "_"

    def string(self):
        while (self.peek() != "\"" and not self.isAtEnd()):
            if (self.peek() == "\n"):
                self.line += 1
            self.advance()
        
        if (self.isAtEnd()):
            LoxError.error(self.line, "Unterminated string.")
            return
        
        self.advance()
        string = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.STRING, string)

    def number(self):
        while (self.peek().isdigit()):
            self.advance()
        
        if (self.peek() == "." and self.peek_next().isdigit()):
            self.advance()

        while (self.peek().isdigit()):
            self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))
    
    def identifier(self):
        while (self.peek_is_alphanum()):
            self.advance()

        string = self.source[self.start:self.current]

        if TokenType.is_keyword(string):
            self.addToken(TokenType(string))
        else:
            self.addToken(TokenType.IDENTIFIER)

    def scanToken(self):
        char = self.advance()

        if char == "\n":
            self.line += 1
            return
        elif char == " " or char == "\t":
            return
        elif char == "/" and self.match("/"):
            while(self.peek() != "\n" and not self.isAtEnd()):
                self.advance()
        elif char == "\"":
            self.string()
        elif char.isdigit():
            self.number()
        elif char.isalpha() or char == "_":
            self.identifier()
        elif (TokenType.has_value(char)):
            if (char == "!" or char == "=" or char == "<" or char == ">") and self.match("="):
                char = str(char) + "="
            self.addToken(TokenType(char))
        else:
            LoxError.error(self.line, f"Unexpected character: {char}")

    def scanTokens(self):
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens