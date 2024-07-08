from app.Lox.TokenType import TokenType

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