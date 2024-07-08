import sys

from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class Scanner():
    hadError = False

    def error(line: int, message: str):
        Scanner.report(line, "", message)
    
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Scanner.hadError = True

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.hadError = False

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
        elif (TokenType.has_value(char)):
            if (char == "!" or char == "=" or char == "<" or char == ">") and self.match("="):
                char = str(char) + "="
            self.addToken(TokenType(char))
        else:
            Scanner.error(self.line, f"Unexpected character: {char}")

    def scanTokens(self):
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens