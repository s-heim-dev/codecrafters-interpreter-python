import sys

from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class ParseError(RuntimeError):
    pass

class LoxError():
    hadError = False

    def error(line: int, message: str):
        LoxError.report(line, "", message)
    
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        LoxError.hadError = True

    def parseError(token: Token, message: str):
        if (token.tokenType == TokenType.EOF):
            LoxError.report(token.line, " at end", message)
        else:
            LoxError.report(token.line, " at '" + token.lexeme + "'", message)

        raise ParseError(message)

