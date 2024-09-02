from copy import deepcopy
from typing import Dict

from app.Lox.LoxError import LoxRuntimeError
from app.Lox.Token import Token

class Environment():
    pass

class Environment(Environment):
    def __init__(self, outer: Environment = None):
        if outer:
            self.values = deepcopy(outer.values)
        else:
            self.values = {}
    
    def define(self, name: str, value: object) -> None:
        self.values[name] = value
    
    def get(self, name: Token) -> object:
        if (name.lexeme in self.values):
            return self.values[name.lexeme]
        
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
