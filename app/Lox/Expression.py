from app.Lox.Token import Token

class Expr():
    pass

class Expr(Expr):
    class Binary(Expr):
        def __init__(self, left: Expr, operator: Token, right: Expr):
            self.left = left
            self.operator = operator
            self.right = right
    
        def __str__(self) -> str:
            return f"({self.operator.lexeme} {self.left} {self.right})"
        
        def __repr__(self) -> str:
            return self.__str__()

    class Grouping(Expr):
        def __init__(self, expression: Expr):
            self.expression = expression
        
        def __str__(self) -> str:
            return f"(group {str(self.expression)})"
        
        def __repr__(self) -> str:
            return self.__str__()
    
    class Literal(Expr):
        def __init__(self, value: object):
            self.value = value
        
        def __str__(self) -> str:
            if (self.value == None):
                return "nil"
            if (type(self.value) == bool):
                return str(self.value).lower()
                
            return str(self.value)
        
        def __repr__(self) -> str:
            return self.__str__()
    
    class Unary(Expr):
        def __init__(self, operator: Token, right: Expr):
            self.operator = operator
            self.right = right
        
        def __str__(self) -> str:
            return f"({self.operator.lexeme} {self.right})"
        
        def __repr__(self) -> str:
            return self.__str__()
        
