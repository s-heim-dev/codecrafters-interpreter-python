import sys

from app.Lox.Token import Token
from app.Lox.TokenType import TokenType

class ParseError(RuntimeError):
    pass

class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token

class LoxError():
    hadError = False
    hadRuntimeError = False

    def error(line: int, message: str) -> None:
        LoxError.report(line, "", message)
    
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        LoxError.hadError = True

    def parseError(token: Token, message: str) -> None:
        if (token.tokenType == TokenType.EOF):
            LoxError.report(token.line, " at end", message)
        else:
            LoxError.report(token.line, " at '" + token.lexeme + "'", message)

        raise ParseError(message)
    
    def runtimeError(error: LoxRuntimeError) -> None:
        print(str(error) + "\n[line " + str(error.token.line) + "]", file=sys.stderr)
        LoxError.hadRuntimeError = True

