from app.Lox.Token import Token

class Expression():
    pass

class Expression(Expression):
    class Binary(Expression):
        def __init__(self, left: Expression, operator: Token, right: Expression):
            self.left = left
            self.operator = operator
            self.right = right
    
        def __str__(self) -> str:
            return f"({self.operator.lexeme} {self.left} {self.right})"
        
        def __repr__(self) -> str:
            return self.__str__()

    class Grouping(Expression):
        def __init__(self, expression: Expression):
            self.expression = expression
        
        def __str__(self) -> str:
            return f"(group {str(self.expression)})"
        
        def __repr__(self) -> str:
            return self.__str__()
    
    class Literal(Expression):
        def __init__(self, value: object):
            self.value = value
        
        def __str__(self) -> str:
            return str(self.value)
        
        def __repr__(self) -> str:
            return self.__str__()
    
    class Unary(Expression):
        def __init__(self, operator: Token, right: Expression):
            self.operator = operator
            self.right = right
        
        def __str__(self) -> str:
            return f"({self.operator.lexeme} {self.right})"
        
        def __repr__(self) -> str:
            return self.__str__()
        
