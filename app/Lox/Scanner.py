from enum import Enum

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"

    # One or two character tokens.
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    # Literals.
    IDENTIFIER = "<Identifier>"
    STRING = "<String>"
    NUMBER = "<Number>"

    # Keywords.
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = "EOF"

    def __str__(self):
        return self.name


class Token():
    def __init__(self, tokenType: TokenType, lexeme: str, literal: object, line: int):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal if literal else "null"
        self.line = line

    def __str__(self):
        return f"{self.tokenType} {self.lexeme} {self.literal}"

    def __repr__(self):
        return self.__str__()


class Scanner():
    hadError = False

    def error(line: int, message: str):
        report(line, "", message)
    
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        Scanner.hadError = True

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.hadError = False

    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def addToken(self, tokenType: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))


    def scanToken(self):
        char = self.advance()

        if char == "\n":
            self.line += 1
            return

        tokenType = TokenType(char)
        self.addToken(TokenType(char))

    def scanTokens(self):
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens