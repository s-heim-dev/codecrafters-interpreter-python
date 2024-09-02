from app.Lox.LoxError import LoxRuntimeError
from app.Lox.Token import Token

class Environment():
    def __init__(self):
        self.values = {}
    
    def define(self, name: str, value: object) -> None:
        self.values[name] = value
    
    def get(self, name: Token) -> object:
        if (name.lexeme in self.values):
            return self.values[name.lexeme]
        
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")